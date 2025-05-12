# QartvelNest
Ground station software + hardware instructions for QartvelSat-1, Georgia’s first CubeSat.

## Overview
This repository contains the software stack, simulations, hardware setup instructions and documentation for the QartvelNest ground station.

## Modules
- **downlink**: SDR receiver based on SatNOGS client.
- **demod**: GMSK demodulator & AX.25 decoder.
- **telemetry**: Parser, database, and REST API.
- **web-ui**: Public web-based telemetry viewer.
- **admin-ui**: Desktop Electron-based admin console.
- **uplink**: AX.25 packetizer and AFSK modulator.
- **simulator**: QartvelSat-1 software emulator for testing.
- **ci**: Continuous integration and automated testing.

## Contributing
See [CONTRIBUTING.md](docs/CONTRIBUTING.md).
