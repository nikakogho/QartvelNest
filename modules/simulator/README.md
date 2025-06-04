# Simulator Module

The QartvelSat‑1 simulator provides a standalone software model of the satellite. It publishes AX.25 telemetry, accepts simple commands and can emulate a basic visibility window. The tool is complete and ready for integration with the rest of the ground‑station stack.

## Features

- Periodic telemetry frames built from an in‑memory `SatelliteState`
- Configurable beacon interval via `--interval SECONDS`
- Frames published over a ZeroMQ PUB socket chosen with `--pub`
- `--once` option to send a single frame then exit
- `--orbit` mode: only transmit during the first 30 seconds of each minute
- Basic command handler for `SET_BEACON_INTERVAL` (0x10)
- Falls back to printing the state when pyzmq is not available

## Usage Examples

Show the available options:

```bash
$ python sim.py --help
```

Run continuously with defaults (publishes to `tcp://*:5567` every 5 seconds):

```bash
$ python sim.py
```

Use a faster beacon interval and a custom endpoint:

```bash
$ python sim.py --interval 1 --pub tcp://*:5556
```

Transmit a single frame and exit. When pyzmq is missing this prints the state:

```bash
$ python sim.py --once
SatelliteState(uptime=0, batt_mv=3000, panel_temp=25, beacon_interval=5)
```

Enable orbit mode so frames are only sent during visibility windows:

```bash
$ python sim.py --orbit --interval 2
```

In orbit mode the simulator waits when the satellite is "out of view" and resumes transmission at the next pass.
