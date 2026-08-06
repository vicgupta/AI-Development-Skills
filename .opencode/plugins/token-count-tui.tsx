import type { TuiPlugin, TuiPluginApi, TuiPluginModule } from "@opencode-ai/plugin/tui"
import type { AssistantMessage } from "@opencode-ai/sdk/v2"
import { createMemo, For, Show } from "solid-js"

const id = "opencode-token-count"

const fmt = new Intl.NumberFormat("en-US")
const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" })

type CallSummary = {
  input: number
  output: number
  reasoning: number
  cacheRead: number
  cacheWrite: number
  cost: number
}

type Totals = CallSummary & { count: number }

function summarize(calls: CallSummary[]): Totals {
  const t: Totals = { input: 0, output: 0, reasoning: 0, cacheRead: 0, cacheWrite: 0, cost: 0, count: calls.length }
  for (const c of calls) {
    t.input += c.input
    t.output += c.output
    t.reasoning += c.reasoning
    t.cacheRead += c.cacheRead
    t.cacheWrite += c.cacheWrite
    t.cost += c.cost
  }
  return t
}

function TokenCountView(props: { api: TuiPluginApi; session_id: string; maxCalls: number }) {
  const theme = () => props.api.theme.current

  const calls = createMemo<CallSummary[]>(() =>
    props.api.state.session
      .messages(props.session_id)
      .filter((m): m is AssistantMessage => m.role === "assistant")
      .map((m) => ({
        input: m.tokens?.input ?? 0,
        output: m.tokens?.output ?? 0,
        reasoning: m.tokens?.reasoning ?? 0,
        cacheRead: m.tokens?.cache?.read ?? 0,
        cacheWrite: m.tokens?.cache?.write ?? 0,
        cost: m.cost ?? 0,
      }))
      .filter((c) => c.input > 0 || c.output > 0 || c.reasoning > 0),
  )
  const totals = createMemo(() => summarize(calls()))
  const recent = createMemo(() => calls().slice(-props.maxCalls))
  const firstIndex = () => calls().length - recent().length

  return (
    <box>
      <text fg={theme().text}>
        <b>Token Usage</b>
      </text>
      <text fg={theme().textMuted}>
        {fmt.format(totals().input)} in / {fmt.format(totals().output)} out
      </text>
      <Show when={totals().reasoning > 0}>
        <text fg={theme().textMuted}>+{fmt.format(totals().reasoning)} reasoning</text>
      </Show>
      <Show when={totals().cacheRead > 0}>
        <text fg={theme().textMuted}>{fmt.format(totals().cacheRead)} cache read</text>
      </Show>
      <Show when={totals().cacheWrite > 0}>
        <text fg={theme().textMuted}>{fmt.format(totals().cacheWrite)} cache written</text>
      </Show>
      <text fg={theme().textMuted}>
        {totals().count} call{totals().count === 1 ? "" : "s"} · {money.format(totals().cost)}
      </text>
      <For each={recent()}>
        {(call, i) => (
          <text fg={theme().textMuted}>
            {firstIndex() + i() + 1}. {fmt.format(call.input)} in / {fmt.format(call.output)} out
          </text>
        )}
      </For>
    </box>
  )
}

const tui: TuiPlugin = async (api, options) => {
  const opts = { maxCalls: 3, order: 200, ...(options ?? {}) }
  const maxCalls = typeof opts.maxCalls === "number" ? Math.min(20, Math.max(1, Math.round(opts.maxCalls))) : 3
  const order = typeof opts.order === "number" ? opts.order : 200

  api.slots.register({
    order,
    slots: {
      sidebar_content(_ctx, props) {
        return <TokenCountView api={api} session_id={props.session_id} maxCalls={maxCalls} />
      },
    },
  })
}

export default { id, tui } satisfies TuiPluginModule
