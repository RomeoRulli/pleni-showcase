# One brain on the server, two numbers, the old number's gateway on the Mac

While users move from the old WhatsApp number to the new one in waves, one brain (FastAPI + the database) on the server talks through two gateways: the new number's on the server, and the old number's left on the Mac, linked by an SSH tunnel, with the Mac marked gateway-only. Who migrated, who wrote and what was notified must live in one place, or two brains send duplicate reminders and drift apart. The old gateway stays on the Mac because its session is already paired there on a home IP, and re-pairing from the server's datacenter IP is what got the new number logged out on the first cutover attempt (10/28).

## Considered Options

- **Two brains, one per number** (the interim phase, 10/29–10/31): no shared state, so migrated people could get every message twice and waves can't see who is left.
- **Both gateways on the server**: no tunnel, but the old number needs re-pairing from the datacenter IP and risks the same logout.
- **Brain stays on the Mac, new gateway on the server**: the development machine becomes the single point of failure for everyone.

## Consequences

While anyone is on the old number, the Mac and the tunnel must stay up, and the server's sshd needs a keepalive so a dropped tunnel can reconnect. Procedure, alerts and the brain rollback are in a private runbook.

## Update 2026-11-09: one number

The old number is retired: the server serves everyone from the new number and has no `antigo` gateway, and the Mac runs no WhatsApp (`PLENI_ROLE=backup`). The old number's session stays paired on the Mac, switched off, as the spare for a ban. Recovery points the server's `novo` connection back at the Mac through the tunnel, so the reason above for keeping it off the datacenter IP still holds (private runbook).
