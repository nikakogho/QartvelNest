# Assembly Instructions for QartvelNest Ground Station

## 1. Mechanical Assembly

### Rotator Setup
- Download and 3D-print parts from [SatNOGS Rotator v3](https://gitlab.com/librespacefoundation/satnogs/satnogs-rotator).
- Assemble with NEMA17 motors, M5 rods; calibrate backlash to ≤0.5°.

### Antenna Assembly
- Follow provided DX Engineering instructions for UHF/VHF Yagis.
- Mount antennas on cross-boom using stainless U-bolts.

### Cabling & Mast Installation
- Route 50m LMR-400 coax through bearings, adding ferrite chokes every 1m.
- Mount outdoor mast (6m) securely with guy wires, aligned precisely to true North (±2°).

---

## 2. Electronics & Software Setup

### Controller Setup
- Flash Arduino Mega with [SatNOGS rotator-controller firmware](https://github.com/satnogs/satnogs-rotator-controller).

### Raspberry Pi Configuration
- Install SatNOGS-client via [official SatNOGS docs](https://wiki.satnogs.org/SatNOGS_Client_Setup).
- Connect RTL-SDR dongle via USB; verify frequency calibration (~0.5 ppm).

### GNU Radio Setup
- Install GNU Radio and gr-satellites, build a flowgraph for 9.6 kbps GMSK (example available in community repositories).

### Hamlib (ICOM IC-910H Control)
- Configure hamlib (`rigctld`, `rotctld`) for ICOM IC-910H.
- Integrate and verify Doppler tracking via GPredict.

### Initial Operational Verification
- Schedule a test observation on SatNOGS network; decode ISS beacon as initial verification.

---

## 3. Final Checks & Validation

- Verify daily TLE updates via automated scripts.
- Weekly: Inspect antennas visually; perform SWR measurements (< 1.3).
- Confirm telemetry decoding and storage in the database after each pass.
- Safety: Disconnect antennas during severe weather (lightning risk).
