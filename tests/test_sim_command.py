import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator.sim import (
    SatelliteState,
    SET_BEACON_INTERVAL,
    crc16_ibm,
    handle_command,
)


def _build_cmd(cmd_id: int, params: list[int]) -> bytes:
    body = bytes([cmd_id, len(params), *params])
    crc = crc16_ibm(body)
    return body + crc.to_bytes(2, "little")


def test_set_beacon_interval_command():
    state = SatelliteState()
    cmd = _build_cmd(SET_BEACON_INTERVAL, [12])
    ack = handle_command(cmd, state)
    assert state.beacon_interval == 12
    assert ack == bytes([SET_BEACON_INTERVAL, 0])
