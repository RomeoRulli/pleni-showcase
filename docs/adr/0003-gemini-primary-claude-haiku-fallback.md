# Gemini on the paid key first, Claude Haiku as fallback only

Chats call Gemini on the paid key (`GEMINI_PAID_API_KEY`). When Gemini fails, the same call goes to Claude Haiku 5.5 (`claude-haiku-5-5`, `ANTHROPIC_API_KEY`), and the daily report does the same. Gemini gets one pass through its model list, at most 12 s per call and about 15 s in total, before Claude takes over. The switch happens per call, inside the tool loop: Claude receives the turn so far, including tool calls Gemini already ran and their results, so no tool runs twice (`app/llm/fallback.py`). Once Claude has answered in a turn, the rest of the turn stays on Claude. The production values live in `app/llm/wiring.py`, and `tests/test_llm_wiring.py` fails if any of them changes.

Why: on 11/04 at 15:03 every Gemini model (`3.6-flash`, `3.5-flash-lite`, `3.8-flash`) returned `503 UNAVAILABLE "high demand"` at the same moment. The old policy retried for up to 90 s (waits of 2, 5 and 10 s between rounds), so replies in the week of 10/28 to 11/04 took a median of 6 s, p90 73 s and max 249 s (read-only from `interaction_audit_logs` on the server). Retrying Gemini doesn't help when a 503 means Google is out of capacity for every model and every key. A second provider does. The paid key is primary because the free tier has daily caps that 150 people would hit, and Google may use free-tier content to improve its products, a poor fit for church members' messages.

## Considered Options

- **Keep retrying Gemini for longer**: the 11/04 outage outlasted the 90 s budget, and the user waited the whole time.
- **OpenAI as the fallback**: a third SDK and a third console with no gain over Claude for this load. Not done.
- **Claude as primary**: Gemini Flash costs about the same per reply and has carried the bot since the start. Claude stays the fallback only and never answers first.

## Consequences

- Without `ANTHROPIC_API_KEY` there is no fallback, and chats keep the old Gemini policy (rounds with waits of 2, 5 and 10 s within 90 s, 25 s per call).
- Claude calls are always paid. They count in `paid_calls` and `cost_micro_usd` (prices in `app/agent/llm_pricing.py`, cache writes at 1.25× input) and record `provider=anthropic`. A turn that starts on Gemini and finishes on Claude records `provider=gemini+anthropic`, with a per-provider breakdown under `providers`.
- Claude requests never send `temperature` (Haiku 5.5 rejects non-default sampling) and use `effort: low` for chat. A refusal (`stop_reason == "refusal"`) counts as a failure, and the turn answers `UNAVAILABLE_REPLY`, as when every model fails.
- Prompt caching: breakpoints on the last tool and at the end of the fixed rules in the system prompt (`stable_system_chars` in `app/agent/prompts.py`). The user's context block comes after the breakpoint, so the cached prefix stays byte-stable across turns.
- The user gets the "just a moment" message (`SLOW_REPLY_NOTICE`) once, when the call moves to Claude.
- Past the Limite mensal da IA, chats and the report use the free key without Claude until the 1st. ADR 0005 replaces this ADR's "members' messages stay off the free tier" for that period.
