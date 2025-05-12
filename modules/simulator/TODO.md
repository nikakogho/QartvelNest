# Simulator Module — Milestones

| Status |   #   | Commit Tag      | Goal                                  | Testable Result                                                |
| :----: | :---: | --------------- | ------------------------------------- | -------------------------------------------------------------- |
|   ⬜️   | **0** | `sim-scaffold`  | Basic project skeleton + argparse     | `python sim.py --help` prints usage.                           |
|   ⬜️   | **1** | `state-machine` | Dataclass for satellite state         | Unit test: default state values asserted.                      |
|   ⬜️   | **2** | `cmd-handler`   | Parse AX.25 payload, mutate state     | Send `SET_BEACON_INTERVAL`; state updates; ACK frame produced. |
|   ⬜️   | **3** | `telemetry-tx`  | Emit downlink payload every N seconds | Subscribed demod receives frame; CRC correct.                  |
|   ⬜️   | **4** | `orbit-toggle`  | Simple vis window on/off              | Config flag triggers no packets outside pass; test passes.     |
