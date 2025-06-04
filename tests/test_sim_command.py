import sys
from pathlib import Path
import pytest

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


def test_handle_command_crc_mismatch():
    state = SatelliteState()
    # Build a command with an invalid CRC (last two bytes zero)
    bad_cmd = bytes([SET_BEACON_INTERVAL, 1, 15, 0, 0])
    with pytest.raises(ValueError, match="CRC mismatch"):
        handle_command(bad_cmd, state)


def test_handle_command_payload_too_short():
    state = SatelliteState()
    with pytest.raises(ValueError, match="payload too short"):
        handle_command(b"\x10", state)


def test_handle_command_unknown_cmd():
    state = SatelliteState()
    cmd = _build_cmd(0xFF, [1])
    ack = handle_command(cmd, state)
    assert ack == bytes([0xFF, 1])
