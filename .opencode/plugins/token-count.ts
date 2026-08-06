import type { Plugin } from "@opencode-ai/plugin"
import { readFile, writeFile, mkdir } from "node:fs/promises"
import { join, dirname } from "node:path"
import { homedir } from "node:os"

type Tokens = {
  input: number
  output: number
  reasoning: number
  cacheRead: number
  cacheWrite: number
}

type CallRecord = {
  messageID: string
  time: number
  model: string
  tokens: Tokens
  cost: number
}

type SessionState = {
  callsCount: number
  calls: CallRecord[]
  tokens: Tokens
  cost: number
}

type Ledger = {
  sessions: Record<string, SessionState>
  total: Tokens & { cost: number }
}

const ZERO: Tokens = { input: 0, output: 0, reasoning: 0, cacheRead: 0, cacheWrite: 0 }

const defaultLedgerPath = () => {
  const base = process.env.XDG_DATA_HOME || join(homedir(), ".local", "share")
  return join(base, "opencode", "token-count.json")
}

export const TokenCountPlugin: Plugin = async (input, rawOptions) => {
  const { client } = input

  const opts = { keepCalls: 200, toast: false, log: true, ...(rawOptions ?? {}) }
  const ledgerPath =
    typeof opts.ledgerPath === "string" && opts.ledgerPath.length > 0
      ? opts.ledgerPath
      : defaultLedgerPath()
  const keepCalls = typeof opts.keepCalls === "number" ? Math.max(1, opts.keepCalls) : 200
  const toastEnabled = opts.toast !== false
  const logEnabled = opts.log !== false

  const states = new Map<string, SessionState>()
  const lastSeen = new Map<string, Tokens>()
  const lastCost = new Map<string, number>()
  const recorded = new Set<string>()
  const lastToasted = new Map<string, number>()

  const add = (a: Tokens, b: Tokens) => {
    a.input += b.input
    a.output += b.output
    a.reasoning += b.reasoning
    a.cacheRead += b.cacheRead
    a.cacheWrite += b.cacheWrite
  }

  const anyPositive = (t: Tokens) =>
    t.input > 0 || t.output > 0 || t.cacheRead > 0 || t.cacheWrite > 0

  const getState = (id: string): SessionState => {
    let s = states.get(id)
    if (!s) {
      s = { callsCount: 0, calls: [], tokens: { ...ZERO }, cost: 0 }
      states.set(id, s)
    }
    return s
  }

  const hydrate = async () => {
    try {
      const raw = await readFile(ledgerPath, "utf8")
      const ledger = JSON.parse(raw) as Ledger
      for (const [id, s] of Object.entries(ledger.sessions ?? {})) {
        s.tokens = { ...ZERO, ...s.tokens }
        states.set(id, s)
      }
    } catch {
      // no ledger yet
    }
  }

  let writing: Promise<void> = Promise.resolve()
  const persist = () => {
    writing = writing
      .then(async () => {
        const total: Tokens & { cost: number } = { ...ZERO, cost: 0 }
        for (const s of states.values()) {
          add(total, s.tokens)
          total.cost += s.cost
        }
        const ledger: Ledger = { sessions: Object.fromEntries(states), total }
        await mkdir(dirname(ledgerPath), { recursive: true })
        await writeFile(ledgerPath, JSON.stringify(ledger, null, 2))
      })
      .catch(() => {})
    return writing
  }

  const fmt = (n: number) => new Intl.NumberFormat("en-US").format(Math.round(n))

  const handleMessageUpdated = async (info: any) => {
    if (info?.role !== "assistant" || !info.tokens) return
    const t: Tokens = {
      input: info.tokens.input ?? 0,
      output: info.tokens.output ?? 0,
      reasoning: info.tokens.reasoning ?? 0,
      cacheRead: info.tokens.cache?.read ?? 0,
      cacheWrite: info.tokens.cache?.write ?? 0,
    }
    const state = getState(info.sessionID)
    const prev = lastSeen.get(info.id) ?? ZERO
    const delta: Tokens = {
      input: Math.max(0, t.input - prev.input),
      output: Math.max(0, t.output - prev.output),
      reasoning: Math.max(0, t.reasoning - prev.reasoning),
      cacheRead: Math.max(0, t.cacheRead - prev.cacheRead),
      cacheWrite: Math.max(0, t.cacheWrite - prev.cacheWrite),
    }
    lastSeen.set(info.id, t)
    const prevCost = lastCost.get(info.id) ?? 0
    const costDelta = Math.max(0, (info.cost ?? 0) - prevCost)
    lastCost.set(info.id, info.cost ?? 0)

    if (!anyPositive(delta) && costDelta <= 0) return
    add(state.tokens, delta)
    state.cost += costDelta

    if (logEnabled) {
      try {
        await client.app.log({
          body: {
            service: "token-count",
            level: "info",
            message: `call ${info.providerID}/${info.modelID}`,
            extra: {
              sessionID: info.sessionID,
              messageID: info.id,
              tokens: delta,
              cost: costDelta,
            },
          },
        })
      } catch {}
    }

    if (info.time?.completed && !recorded.has(info.id)) {
      recorded.add(info.id)
      state.callsCount++
      state.calls.push({
        messageID: info.id,
        time: info.time.completed,
        model: `${info.providerID}/${info.modelID}`,
        tokens: { ...t },
        cost: info.cost ?? 0,
      })
      if (state.calls.length > keepCalls) {
        state.calls.splice(0, state.calls.length - keepCalls)
      }
      await persist()
    }
  }

  const handleSessionIdle = async (sessionID: string) => {
    const state = getState(sessionID)
    if (state.callsCount === lastToasted.get(sessionID)) return
    lastToasted.set(sessionID, state.callsCount)
    await persist()
    if (!toastEnabled) return

    const t = state.tokens
    const last = state.calls[state.calls.length - 1]
    const reasoning = t.reasoning > 0 ? ` (+${fmt(t.reasoning)} reasoning)` : ""
    const msg = last
      ? `token-count: call ${state.callsCount} — ${fmt(last.tokens.input)} in / ${fmt(last.tokens.output)} out; session ${fmt(t.input)} in / ${fmt(t.output)} out (${state.callsCount} calls)${reasoning}`
      : `token-count: session ${fmt(t.input)} in / ${fmt(t.output)} out (${state.callsCount} calls)${reasoning}`
    try {
      await client.tui.showToast({ body: { message: msg, variant: "info" } })
    } catch {}
  }

  await hydrate()

  return {
    dispose: () => persist(),

    event: async ({ event }) => {
      switch (event.type) {
        case "message.updated":
          await handleMessageUpdated((event.properties as any).info)
          break
        case "session.idle":
          await handleSessionIdle(event.properties.sessionID)
          break
        case "session.deleted":
          states.delete(event.properties.info.id)
          await persist()
          break
      }
    },
  }
}
