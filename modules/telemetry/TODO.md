# Telemetry Module — Milestones

| Status |   #   | Commit Tag          | Goal                                           | Testable Result                                                |
| :----: | :---: | ------------------- | ---------------------------------------------- | -------------------------------------------------------------- |
|   ⬜️   | **0** | `telemetry-compose` | Docker‑compose Postgres+Timescale skeleton     | `docker compose up` starts DB, health‑check OK.                |
|   ⬜️   | **1** | `fastapi-skeleton`  | FastAPI project with `/alive` endpoint         | `curl /alive` returns `{status:"ok"}`; CI test passes.         |
|   ⬜️   | **2** | `schema-draft`      | Import `docs/telemetry.yml` and autogen parser | Golden payload decoded to dict; unit test green.               |
|   ⬜️   | **3** | `db-insert-worker`  | ZMQ subscriber bulk‑inserts to Timescale       | Integration test shows 100 packets stored; query returns rows. |
|   ⬜️   | **4** | `websocket-feed`    | WebSocket `/ws` pushes new packet each second  | Playwright connects, receives ≥3 messages in 5 s.              |
