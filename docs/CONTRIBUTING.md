# Contributing to **QartvelNest**

Welcome! Together we are building the first Georgian CubeSat ground‑station. This guide explains how to collaborate efficiently and keep the project healthy.

---

## 1 — Project Layout

```
/docs            ── Architecture, hardware docs, high‑level specs
/modules/*       ── One folder per software module
                  /downlink  /demod  /telemetry  /web-ui ...
DEV_DIARY.md     ── Global chronological log (high‑level)
docs/TODO.md     ── Global task list (root‑level decisions)
modules/*/TODO.md── Per‑module task lists
```

Generated artefacts (`dist/`, `.wav`, `.iq`, build caches) **must not** be committed.

---

## 2 — Branching Model

| Branch                 | Purpose                                                         |
| ---------------------- | --------------------------------------------------------------- |
| `master`               | Production mainline; CI green; deployable simulation.           |
| `module/<name>`        | Optional long‑lived integration branches (e.g. `module/demod`). |
| `feat/<module>-<desc>` | Short‑lived feature branches; merge via PR only.                |

Before merging a PR you **must**:

1. Rebase onto `master` (avoid merge commits).
2. Pass all module unit tests **and** full‑stack simulation CI.
3. Obtain at least **one** review approval from a maintainer outside your module.

---

## 3 — Coding Standards

| Language   | Lint / Formatter     | Test Framework       |
| ---------- | -------------------- | -------------------- |
| Python 3   | `ruff`, `black`      | `pytest`             |
| TypeScript | `eslint`, `prettier` | `jest`, `playwright` |
| Markdown   | `markdownlint`       | —                    |

Local `pre‑commit` hooks are provided under `.githooks/`; CI re‑runs the same checks.

---

## 4 — Commit Guidelines

* Follow the **Conventional Commits** spec (`feat:`, `fix:`, `docs:`, `ci:`, etc.).
* Limit subject lines to 72 characters; wrap body at 100.
* Reference issue IDs (`closes #42`) when relevant.

---

## 5 — Pull‑Request Template

```
### What & Why
<short description>

### How
<key implementation points>

### Testing
- [ ] Unit tests pass
- [ ] Integration simulation (`npm run sim:e2e`) passes
- [ ] Documentation updated

### Checklist
- [ ] I ran `pre-commit run --all-files`
- [ ] Relevant TODO.md items updated
```

---

## 6 — Release Process

1. Maintainer triggers **Release** GitHub Action.
2. CI tags `vX.Y.Z`, generates a changelog from commit messages, and publishes Docker images.
3. Docs site auto‑deploys from `master`.

---

## 7 — Code of Conduct

We follow the [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). Be respectful, inclusive, and patient. Violations can be reported privately to the maintainers.

---

**Gaumarjos QartvelSat‑1 / QartvelNest!**
