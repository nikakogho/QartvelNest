# Admin‑UI Module — Milestones

| Status |   #   | Commit Tag          | Goal                                         | Testable Result                                                    |
| :----: | :---: | ------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
|   ⬜️   | **0** | `admin-scaffold`    | Electron+React template builds on Windows    | `npm start` opens empty window; lint passes.                       |
|   ⬜️   | **1** | `shared-components` | Import `TelemetryChart` from web‑ui          | Storybook shows component rendered in Electron context.            |
|   ⬜️   | **2** | `command-form`      | JSON‑schema driven command composer          | Enter params, click send → POST to mock `/send`, log success.      |
|   ⬜️   | **3** | `console-log`       | Live log panel (tail)                        | Simulator injects logs; UI auto‑scrolls; Spectron test green.      |
|   ⬜️   | **4** | `installer`         | Build Windows installer via electron‑builder | `dist/QartvelNestSetup.exe` outputs; smoke‑test install/uninstall. |
