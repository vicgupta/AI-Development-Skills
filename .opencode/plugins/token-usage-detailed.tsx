/** @jsxImportSource @opentui/solid */
import { createMemo, For, Show } from "solid-js"
import type { AssistantMessage } from "@opencode-ai/sdk/v2"
import type { TuiPlugin, TuiPluginApi, TuiPluginModule } from "@opencode-ai/plugin/tui"
import type { RGBA } from "@opentui/core"

const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" })
const nf = new Intl.NumberFormat("en-US")

const fmtCost = (value: number) => {
  if (!Number.isFinite(value) || value <= 0) return "$0.00"
  if (value < 0.01) return `$${value.toFixed(4)}`
  return money.format(value)
}

const stepTokens = (m: AssistantMessage) =>
  m.tokens.input + m.tokens.output + m.tokens.reasoning + m.tokens.cache.read + m.tokens.cache.write

const BAR_WIDTH = 12

function View(props: { api: TuiPluginApi; session_id: string }) {
  const theme = () => props.api.theme.current

  const steps = createMemo(() =>
    props.api.state.session
      .messages(props.session_id)
      .filter((m): m is AssistantMessage => m.role === "assistant" && !m.error && m.tokens.output > 0),
  )

  const totals = createMemo(() => {
    let cost = 0
    let input = 0
    let output = 0
    let reasoning = 0
    let cacheRead = 0
    let cacheWrite = 0
    for (const m of steps()) {
      cost += m.cost
      input += m.tokens.input
      output += m.tokens.output
      reasoning += m.tokens.reasoning
      cacheRead += m.tokens.cache.read
      cacheWrite += m.tokens.cache.write
    }
    return { cost, input, output, reasoning, cacheRead, cacheWrite }
  })

  const total = createMemo(() => {
    const t = totals()
    return t.input + t.output + t.reasoning + t.cacheRead + t.cacheWrite
  })

  const last = createMemo(() => steps().at(-1))

  const model = createMemo(() => {
    const m = last()
    if (!m) return undefined
    return props.api.state.provider.find((p) => p.id === m.providerID)?.models[m.modelID]
  })

  const context = createMemo(() => {
    const m = last()
    const mod = model()
    if (!m || !mod?.limit?.context) return undefined
    const used = stepTokens(m)
    const pct = Math.min(100, (used / mod.limit.context) * 100)
    return { used, limit: mod.limit.context, pct }
  })

  const recent = createMemo(() => steps().slice(-5).reverse())

  const row = (label: string, value: string, fg?: RGBA) => (
    <box flexDirection="row" justifyContent="space-between" width="100%">
      <text fg={theme().textMuted}>{label}</text>
      <text fg={fg ?? theme().text}>{value}</text>
    </box>
  )

  const bar = (pct: number) => {
    const filled = Math.round((Math.max(0, Math.min(100, pct)) / 100) * BAR_WIDTH)
    return (
      <text>
        <span style={{ fg: theme().accent }}>{"▓".repeat(filled)}</span>
        <span style={{ fg: theme().border }}>{"░".repeat(BAR_WIDTH - filled)}</span>
      </text>
    )
  }

  return (
    <box
      border
      borderColor={theme().border}
      backgroundColor={theme().backgroundPanel}
      paddingTop={1}
      paddingBottom={1}
      paddingLeft={2}
      paddingRight={2}
      flexDirection="column"
      gap={0}
    >
      <text fg={theme().accent}>
        <b>Detailed Token Usage</b>
      </text>

      <Show when={steps().length > 0} fallback={<text fg={theme().textMuted}>No token usage yet</text>}>
        <box flexDirection="column" gap={0}>
          {row("Total tokens", nf.format(total()))}
          {row("Cost", fmtCost(totals().cost), theme().success)}

          <box flexDirection="column" gap={0}>
            <text fg={theme().textMuted}>
              <b>Breakdown</b>
            </text>
            {row("Input", nf.format(totals().input))}
            {row("Cache read", nf.format(totals().cacheRead))}
            {row("Cache write", nf.format(totals().cacheWrite))}
            {row("Reasoning", nf.format(totals().reasoning))}
            {row("Output", nf.format(totals().output))}
          </box>

          <Show when={context()}>
            {(c) => (
              <box flexDirection="column" gap={0}>
                <text fg={theme().textMuted}>
                  <b>Context</b>
                </text>
                <box flexDirection="row" alignItems="center" gap={1}>
                  {bar(c().pct)}
                  <text fg={theme().text}>{Math.round(c().pct)}%</text>
                  <text fg={theme().textMuted}>of {nf.format(c().limit)}</text>
                </box>
                <Show when={model()}>
                  {(mod) => <text fg={theme().textMuted}>{mod().name}</text>}
                </Show>
              </box>
            )}
          </Show>

          <Show when={recent().length > 0}>
            <box flexDirection="column" gap={0}>
              <text fg={theme().textMuted}>
                <b>Recent steps</b>
              </text>
              <For each={recent()}>
                {(m, i) => (
                  <box flexDirection="row" justifyContent="space-between" width="100%">
                    <text fg={theme().textMuted}>#{steps().length - i()}</text>
                    <text fg={theme().text}>{nf.format(stepTokens(m))}</text>
                    <text fg={theme().text}>{fmtCost(m.cost)}</text>
                  </box>
                )}
              </For>
            </box>
          </Show>
        </box>
      </Show>
    </box>
  )
}

const tui: TuiPlugin = async (api) => {
  api.slots.register({
    order: 150,
    slots: {
      sidebar_content(_ctx, value) {
        return <View api={api} session_id={value.session_id} />
      },
    },
  })
}

export default {
  id: "token-usage-detailed",
  tui,
} satisfies TuiPluginModule
