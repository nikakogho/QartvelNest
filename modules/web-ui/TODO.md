# Web‑UI Module — Milestones

| Status |   #   | Commit Tag        | Goal                               | Testable Result                                              |
| :----: | :---: | ----------------- | ---------------------------------- | ------------------------------------------------------------ |
|   ⬜️   | **0** | `webui-scaffold`  | Vite+React+TS scaffold with ESLint | `pnpm dev` serves placeholder page, lint passes.             |
|   ⬜️   | **1** | `chart-component` | `TelemetryChart` using Chart.js    | Storybook shows line chart with mock data.                   |
|   ⬜️   | **2** | `api-service`     | REST + WebSocket wrapper           | Mock server test: component updates on WS push.              |
|   ⬜️   | **3** | `dashboard-page`  | Live dashboard layout              | Playwright E2E: receives 3 packets → graph renders 3 points. |
|   ⬜️   | **4** | `gh-pages-deploy` | GitHub Pages CI deployment         | `https://<user>.github.io/QartvelNest` shows dashboard.      |
