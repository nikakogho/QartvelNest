import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator.sim import (
    SatelliteState,
    build_telemetry_payload,
    build_ax25_frame,
)


def test_build_payload_crc():
    state = SatelliteState(uptime=60, batt_mv=3000, panel_temp=30, beacon_interval=5)
    payload = build_telemetry_payload(state)
    expected = bytes.fromhex("01 3C 00 B8 0B 1E 05 FA 99")
    assert payload == expected


def test_ax25_frame_matches_golden():
    state = SatelliteState(uptime=60, batt_mv=3000, panel_temp=30, beacon_interval=5)
    payload = build_telemetry_payload(state)
    frame = build_ax25_frame(payload)
    expected_hex = (ROOT / "testdata" / "golden_downlink.hex").read_text().strip()
    expected = bytes.fromhex(expected_hex)
    assert frame == expected

