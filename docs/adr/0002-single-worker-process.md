# One uvicorn worker per brain, by design

The brain runs as a single uvicorn process with one event loop (`scripts/run-fastapi.sh`, pm2 `pleni-fastapi`). Its coordination state lives in that process's memory: the per-user rate limiter and the global Gemini limiter (`app/api/dependencies.py`), the per-user lock that keeps one reply in flight per person (`_user_processing_locks` in `app/api/routes/whatsapp.py`), the new-number pacing guard (`_shared` in `app/services/new_number_guard.py`), the report retry counter (`ReportJob` in `app/jobs.py`), the lock around the AI-failure alert state (`ReplyAlerts` in `app/services/reply_alerts.py`; the state itself is in SQLite) and the Planning Center request window (`PCOClient`). A second worker would split each of these in two and double every limit.

## Considered Options

- **Several workers, state in SQLite**: every limiter and lock becomes a write on the one SQLite writer the replies already wait on, for a load (one church, a few hundred volunteers) that one event loop serves.
- **Several workers, state in Redis**: a new service to run and secure on the server for the same load.

## Consequences

`scheduler_locks` in SQLite does not coordinate workers; it only stops a `cli.py` command run in parallel from repeating a cycle the scheduler (`app/scheduler.py`) is running. Scaling out means first moving the state listed above out of process memory.
