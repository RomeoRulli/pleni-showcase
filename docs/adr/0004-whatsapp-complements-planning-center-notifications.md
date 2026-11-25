# WhatsApp notifications complement Planning Center's, they don't replace them

The owner asked for every volunteer notification to come through WhatsApp. The bot keeps sending its notifications (aviso de escala, lembrete, aviso de cancelamento, and the leader notices) on top of Planning Center's own emails, and never tries to switch Planning Center off. A volunteer who picks **Só pelo WhatsApp** gets steps to turn off Planning Center's SMS and app push themselves; Planning Center's email keeps arriving.

Why: the Services API has no per-person switch for Planning Center's notifications. `Person` has no notification-preference field, reminder settings exist only per plan time and team (`PlanTime.team_reminders`) or per plan (`Plan.reminders_disabled`), and no endpoint sends or suppresses Planning Center's emails (checked against the API docs on 2026-11-16). SMS and push are opt-ins each person controls in their own profile and app. The bot also can't reach everyone. It only sends by its own initiative to people who have written to it and haven't sent PARAR, which is the anti-ban rule (`send_rules`). Turning Planning Center off for the whole church would leave everyone who never wrote to the bot with no notice at all.

## Considered Options

- **Turn off Planning Center's notifications for the whole church**: this cuts off every volunteer who hasn't written to the bot. Rejected.
- **Remove a person's email from Planning Center to silence it**: this breaks their login and password reset. Rejected.
- **Make WhatsApp opt-in, so the bot notifies only those who ask**: this would take away the reminders people already get today, and PARAR already covers people who don't want WhatsApp. Rejected.

## Consequences

- People who chose Só pelo WhatsApp still get Planning Center's emails. The bot must not promise that they will stop.
- The bot mirrors Planning Center's timing where the API exposes it, so the two channels don't contradict each other. The lembrete goes out at 10:00 on the same day as Planning Center's reminder. The gap-alert setting isn't in the API, so the Resumo do líder uses a fixed 13:00.
