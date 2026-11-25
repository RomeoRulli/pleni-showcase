# Past the Limite mensal da IA, chats use the free Gemini key

Pleni enforces the Limite mensal da IA itself (`LLM_MONTHLY_BUDGET_USD`, US$ 20 by default, per Brasília month). Every paid call (Gemini on the paid key, and Claude as fallback, in chats and in the report) adds its cost to `llm_spend`. Once the month reaches the limit, chats and the report go to the free Gemini key (`GEMINI_API_KEY`) without Claude until the 1st (`app/llm/budget.py`). This partly reverses ADR 0003, which keeps church members' messages off the free tier: past the limit, they go to the free tier for the rest of the month.

Why: the owner could not find where to set a US$ 20 monthly cap in the Anthropic and Google consoles (11/18). Google's budget only sends an email and doesn't stop the spending. A hard cap that Pleni enforces is the only one that stops the spending, and the free key keeps the bot answering instead of going silent for up to two weeks. The owner accepted that, past the limit, members' messages fall under the free tier's terms (Google may use them to improve its products) and its daily caps.

## Considered Options

- **Caps in the Anthropic and Google consoles**: not available to the owner (see above). Rejected.
- **Stop answering past the limit** (a fixed "IA indisponível até dia 1" reply): keeps members' messages off the free tier, but leaves 150 people without the bot for the rest of the month. Rejected.
- **Keep Claude past the limit**: Claude is always paid, so the limit would not be a limit. Rejected.

## Consequences

- Past the limit, chats go back to the policy for Gemini without Claude (rounds with waits of 2, 5 and 10 s within 90 s). `tests/test_llm_monthly_budget.py` pins this, alongside the paid-key policy that `tests/test_llm_wiring.py` pins under ADR 0003.
- The owner gets a Telegram alert at 80% and another at the limit, once each per month and per limit value. The alert at the limit is also sent from the check that routes a call to the free key. That covers a lowered limit and a Telegram failure on the call that crossed it, cases where no paid call follows.
- `llm-check` adds its cost to the month but never switches keys, because it exists to check the paid policy end to end.
- Without `GEMINI_API_KEY`, a call past the limit fails as if every model had failed (`BudgetExhausted`), and the member gets `UNAVAILABLE_REPLY`.
- `LLM_MONTHLY_BUDGET_USD=0` turns the limit off. Raising the limit mid-month re-arms both alerts.
