# QartvelNest Ground‑Station Architecture

*Version 0.1 — 2025‑05‑12*

---

## 1  Purpose & Scope

This document captures the **authoritative, first‑principles design** of Georgia’s QartvelNest ground‑station system that supports **QartvelSat‑1**. It is the single reference that all software and hardware tasks flow from.  Update this file whenever an interface or design decision changes and tag the commit accordingly.

---

## 2  Guiding Design Principles

|  ID   | Principle                            | Rationale                                                                                                           |
| ----- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
|  P‑01 | **Simulation First**                 | Entire RF chain is emulated end‑to‑end to enable parallel software development before hardware arrives.             |
|  P‑02 | **Modular Boundaries**               | Strict interface definitions (FIFO, ZeroMQ, REST, WebSocket) let teams work independently and swap implementations. |
|  P‑03 | **COTS & Open‑Source**               | Reuse SatNOGS, GNU Radio, Hamlib, TimescaleDB, React—to minimise cost and maximise community support.               |
|  P‑04 | **Windows‑Friendly**                 | Developers can work on Windows 10+; Linux‑only tools run inside WSL 2 or Docker.                                    |
|  P‑05 | **Infrastructure‑as‑Code**           | CI spins up a complete simulated constellation on every push so regressions are caught immediately.                 |
|  P‑06 | **Single Repo, Polyglot Workspaces** | One GitHub repo (`QartvelNest`) contains all modules under `/modules/*` with language‑native workspaces.            |

---

## 3  System Context (Level 0)

```
+-----------------+                                              +-----------------+
|  Public Viewer  |  <-- HTTPS/WebSocket -->  [Backend/API]  <-- |  Admin Console  |
+-----------------+                                              +-----------------+
        ^                                                           |
        |                                                           |  REST / CLI
        |                                                           v
+-----------------------------------------------------------------------+
|                     QartvelNest Ground Segment                         |
| +-----------+   FIFO   +---------+  ZMQ  +--------------+  ZMQ  +---+ |
| |  SatNOGS  |--------->| Demod & |----->| Telemetry DB  |<-----|Sim| |
| |  Client   |  bits    |  AX.25  |      |   +  API      |      |   | |
| +-----------+          +---------+      +--------------+      +---+ |
|     | SDR (RTL/HackRF)     ^                                 ^       |
|     | UHF Rx 437 MHz       | raw bytes                       | cmd    |
|     v                      |                                 |        |
|  Antenna + LNA             |                                 |        |
|                              +-- ZMQ 1200 bps Bell 202 AFSK --+        |
+-----------------------------------------------------------------------+
```

Legend: solid lines = in‑production links; dotted lines = simulation loopbacks.

---

## 4  Component Overview (Level 1)

|  ID    | Module (folder) | Language       | Runs On        | External Dependencies               | Primary Responsibilities                                                                              |
| ------ | --------------- | -------------- | -------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
|  M‑DL  | **downlink**    | Python 3       | Linux/WSL      | SatNOGS‑client, GNU Radio, SoapySDR | Control SDR, capture UHF 9 600 bps GMSK, write hard bits to FIFO.                                     |
|  M‑DM  | **demod**       | Python 3       | Any            | bitarray, crcmod                    | Detect AX.25 frames, verify FCS, publish payload JSON over ZeroMQ (`tcp://*:5557`).                   |
|  M‑TM  | **telemetry**   | Python 3       | Any            | FastAPI, TimescaleDB                | Parse payload → typed fields, store in DB, expose REST+WebSocket API.                                 |
|  M‑WU  | **web‑ui**      | React TS       | Browser        | chart.js, Recoil                    | Public dashboard of selected telemetry and pass predictions.                                          |
|  M‑AC  | **admin‑ui**    | Electron+React | Windows/macOS  | ipcRenderer                         | Build & dispatch commands, monitor engineering telemetry.                                             |
|  M‑UL  | **uplink**      | Python 3       | Any            | numpy/scipy, FastAPI                | Packetize AX.25 UI frames, generate Bell 202 AFSK `.wav`, push to ZMQ (`tcp://*:5566`).               |
|  M‑SIM | **simulator**   | Python 3       | Any            | pyorbital (optional)                | Emulate satellite: accept uplink bytes, mutate state, emit downlink payloads on ZMQ (`tcp://*:5567`). |
|  CI    | **ci**          | Bash           | GitHub Actions | Docker                              | Spin full stack in Docker; run integration tests and Playwright headless UI tests.                    |

---

## 5  Interface Contracts (Level 2)

### 5.1 FIFO: `/tmp/saksat/downlink.bits`

*Type:* POSIX named pipe (byte‑oriented).
*Producer:* M‑DL
*Consumer:* M‑DM
*Rate:* ≤ 10 kbit/s.

### 5.2 ZeroMQ Topics

| Topic                                | Direction    | Payload                           | Notes                                                 |
| ------------------------------------ | ------------ | --------------------------------- | ----------------------------------------------------- |
| `ax25.raw` (`tcp://*:5557`)          | M‑DM → M‑TM  | `{timestamp:str, bytes:hex}`      | One message per successfully CRC‑checked AX.25 frame. |
| `cmd.wav` (`tcp://*:5566`)           | M‑UL → M‑SIM | Raw audio bytes (Bell 202 48 kHz) | Only in simulation mode.                              |
| `telemetry.payload` (`tcp://*:5567`) | M‑SIM → M‑DL | Raw signed bytes pre‑AX.25        | Simulator injects “air‑frame”.                        |

### 5.3 REST / HTTP

|  Endpoint                         | Module | Method | Format                            | Description                     |
| --------------------------------- | ------ | ------ | --------------------------------- | ------------------------------- |
| `/api/v1/telemetry/latest?field=` | M‑TM   |  GET   | JSON                              | Latest value of a field.        |
| `/api/v1/telemetry/range`         | M‑TM   | GET    | JSON                              | Time‑range query.               |
| `/send`                           | M‑UL   | POST   | JSON `{cmd_id:int, params:[int]}` | Build + transmit command frame. |

### 5.4 WebSocket

`ws://<host>/ws` streams the most recent telemetry packet to any subscriber every second.

---

## 6  Data Formats

### 6.1 Downlink Telemetry Payload (draft)

| Byte Offset | Field           | Type    | Scale        | Unit    |
| ----------- | --------------- | ------- | ------------ | ------- |
| 0           | Packet ID       |  U8     | –            | –       |
| 1           | Uptime          |  U16 LE | 1            | seconds |
| 3           | Battery Voltage | U16 LE  | /1000        | volts   |
| 5           | Panel Temp      |  S8     | +40 → °C     | °C      |
| 6           | Beacon Interval | U8      | 1            | seconds |
| 7           | CRC (16‑bit)    | U16 LE  | CRC‑16/CCITT | –       |

Total payload length: **9 bytes**. Wrapped in AX.25 UI frame.

### 6.2 Uplink Command Payload (draft)

```
[ CMD_ID (1) ][ LEN (1) ][ PARAMS (LEN) ][ CRC16‑IBM (2) ]
```

Examples: `0x10` → Set beacon interval (`PARAMS[0] = seconds`).

---

## 7  Deployment Modes

| Mode               | Description                                  | Differences                                                  |
| ------------------ | -------------------------------------------- | ------------------------------------------------------------ |
| **Sim‑solo**       | Everything in Docker on developer laptop.    | Mock SDR source files; uplink loopback.                      |
| **Local‑no‑rotor** | Real SDRs + antennas, no az/el tracking.     | M‑DL radio device = RTL‑SDR; uplink via HackRF on low power. |
| **Full Ops**       | Fielded station with rotator, LNA, PA, mast. | Adds Hamlib rotor control and PA keying; safety interlocks.  |
