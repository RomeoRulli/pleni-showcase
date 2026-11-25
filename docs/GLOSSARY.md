# Pleni glossary

The project keeps one canonical word for each concept, in Portuguese, because that is the language its users speak. Code, tests, commit messages and conversations with AI agents all use these words. Each entry also lists the synonyms the project avoids, so the same thing is never called by two names.

This is an English translation of the project's `GLOSSARY.md`. The canonical terms stay in Portuguese, with a gloss in parentheses.

## Schedules and notifications

**Escala** (schedule):
The assignment of a person to a position in a team, for a service (a plan) in Planning Center.
_Avoid_: agendamento, schedule

**Escala pendente** (pending schedule):
A schedule the person has neither accepted nor declined yet.
_Avoid_: não confirmada, a confirmar

**Escala aceita** (accepted schedule):
A schedule the person said they will serve.
_Avoid_: confirmada, confirmado (Planning Center's "C")

**Escala recusada** (declined schedule):
A schedule the person said they cannot serve.
_Avoid_: cancelada (reserved for when the leader removes the person from the schedule)

**Notificação** (notification):
A message the bot sends on its own initiative to a volunteer about one of their schedules. The kinds are the aviso de escala, the lembrete and the aviso de cancelamento.
_Avoid_: alerta (reserved for the owner), push

**Aviso de escala** (schedule notice):
A notification that the person was scheduled and still has to accept or decline.
_Avoid_: convite, pedido de escala, notificação de escala

**Lembrete** (reminder):
A notification, before the service, about an accepted or still pending schedule.
_Avoid_: reminder, lembrete pré-culto

**Bloco da escala** (schedule block):
The part of a notification that says when, where and in what role the volunteer serves: one bold date line per time of theirs in the plan, the service, and the team and position. No year and no schedule ID.
_Avoid_: card, resumo da escala

**Dica** (tip):
A short, separate message after a notification or a reply from the bot, suggesting something the volunteer can ask for. It appears now and then, not every time, rotating among a few suggestions.
_Avoid_: tip, rodapé

**Conversa** (conversation):
Messages exchanged between the volunteer and the bot with no pause longer than one hour.

**Interação** (interaction):
What counts toward the Dica: a notification that went out, or a conversation. Every three, one Dica is due.

**Só pelo WhatsApp** (WhatsApp only):
A volunteer's choice to get notifications from the bot instead of Planning Center's SMS and push. Planning Center's email keeps arriving.
_Avoid_: centralizar, opt-out do Planning

**Envio por iniciativa do bot** (bot-initiated send):
Any message the bot sends when the person has not just written. It only goes to people who have already written to the bot and have not sent PARAR (stop).
_Avoid_: mensagem proativa, disparo

## Songs

**Repertório** (repertoire):
The church's songs registered in Planning Center, without the hidden ones.
_Avoid_: catálogo, biblioteca de músicas

**Músicas do culto** (service songs):
The songs a service will play, each with its key. Musicians get them in the lembrete.
_Avoid_: repertório (reserved for all the church's songs), setlist

## Notices to leaders

**Responsável pelas respostas** (person responsible for answers):
The person Planning Center records to receive the acceptance or decline of a schedule.
_Avoid_: quem escalou, scheduler, responds_to

**Aviso de recusa** (decline notice):
An immediate message to the responsável pelas respostas saying that someone declined a schedule, with the reason.
_Avoid_: alerta de recusa

**Resumo do líder** (leader summary):
A daily message to a leader with the boards of the coming services that need some action, and the new blocked dates in their team. It is only sent when there is something to tell.
_Avoid_: digest, aviso de aceite

**Quadro do culto** (service board):
Who from a team is scheduled for a service, with each person's status (pending, declined, accepted), and the positions still open.
_Avoid_: roster, escalação, lista de escalados

**Vaga** (open position):
A team position in a service that has nobody scheduled yet.
_Avoid_: gap, needed position

## Report to the owner

**Relatório semanal** (weekly report):
A summary sent to the owner on Telegram every Monday at 9am, covering the whole previous week (Monday to Sunday).
_Avoid_: relatório diário, relatório periódico

**Limite mensal da IA** (monthly AI limit):
A cap in dollars on what the paid Gemini key and the Claude fallback may spend in a calendar month (US$ 20). The owner is told at 80% and at the limit; past the limit, chats and the report use the free Gemini key until the 1st. The weekly report shows how much of the limit the month has used.
_Avoid_: orçamento, budget, cota

**Alerta de problema** (problem alert):
An immediate message to the owner on Telegram when something goes wrong with the bot: an error, an unknown number, the send cap, or an unmet demand.
_Avoid_: notificação por interação

**Proposta de melhoria** (improvement proposal):
A change to the bot suggested to the owner, with problem, evidence, expected behaviour, implementation path, effort and priority. It comes from a volunteer's suggestion, an unmet demand, or an AI finding.
_Avoid_: sugestão de melhoria, feature, melhoria

**Sugestão do voluntário** (volunteer suggestion):
What a volunteer proposes when answering the weekly improvement survey.
_Avoid_: feedback

**Demanda não atendida** (unmet demand):
Something a person asked the bot for that it could not do.
_Avoid_: pedido não atendido, unmet demand

**Achado da IA** (AI finding):
A problem in how the bot is used that the AI finds by reading the week's conversations, even when nobody complained.
_Avoid_: insight, diagnóstico
