# Simulator Module

This module emulates the behaviour of **QartvelSat‑1** so that the rest of the
ground‑station stack can be tested without any physical hardware.  It will
accept uplinked commands, mutate an in‑memory satellite state, and periodically
emit telemetry frames over ZeroMQ.

Development follows the milestones in [`TODO.md`](TODO.md).  The first goal is a
minimal command line interface that can be executed locally:

```bash
python sim.py --help
```

Later milestones will introduce the state machine, command parsing, downlink
payload generation, and basic orbit simulation toggles.
