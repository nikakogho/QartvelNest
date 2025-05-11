# QartvelNest — Global Milestones

| Status |   #   | Commit Tag          | Goal                                    | Testable Result                                                                       |
| :----: | :---: | ------------------- | --------------------------------------- | ------------------------------------------------------------------------------------- |
|   ☑️   | **0** | `init-repo`         | **Initial repository scaffold**         | README, LICENSE, .gitignore, baseline folders committed on `master`.                  |
|   ⬜️   | **1** | `telemetry-schema`  | **Freeze telemetry.yml**                | Parser unit tests pass against golden payload vectors; no schema changes thereafter.  |
|   ⬜️   | **2** | `command-set`       | **Uplink command table defined**        | Packetizer builds all commands; simulator ACKs correctly in end‑to‑end CI.            |
|   ⬜️   | **3** | `contributing-doc`  | **Publish CONTRIBUTING.md & hooks**     | PRs fail CI if lint/tests fail; pre‑commit hook operational.                          |
|   ⬜️   | **4** | `hardware-doc-rev1` | **Rewrite hardware build instructions** | Assembly\_Instructions.md reviewed; BOM prices & part numbers validated.              |
|   ⬜️   | **5** | `uplink-security`   | **Anti‑replay & sequence numbers**      | Integration test rejects duplicate frame; accepts fresh sequence; documented in spec. |
