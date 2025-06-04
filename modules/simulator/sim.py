import argparse
from dataclasses import dataclass

# Command identifiers (from docs/commands.md)
SET_BEACON_INTERVAL = 0x10


@dataclass
class SatelliteState:
    """Simple representation of satellite state."""

    uptime: int = 0
    batt_mv: int = 3000
    panel_temp: int = 25
    beacon_interval: int = 5


def crc16_ibm(data: bytes) -> int:
    """Return CRC-16/IBM of *data* (polynomial 0xA001, init 0xFFFF)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the simulator CLI."""
    parser = argparse.ArgumentParser(
        description="QartvelSat-1 software simulator"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Beacon interval in seconds",
    )
    return parser


def handle_command(payload: bytes, state: SatelliteState) -> bytes:
    """Parse *payload* and mutate *state*. Return ACK bytes."""
    if len(payload) < 4:
        raise ValueError("payload too short")

    cmd_id = payload[0]
    param_len = payload[1]
    params = payload[2 : 2 + param_len]
    crc_given = int.from_bytes(payload[2 + param_len : 4 + param_len], "little")
    if crc16_ibm(payload[: 2 + param_len]) != crc_given:
        raise ValueError("CRC mismatch")

    if cmd_id == SET_BEACON_INTERVAL and param_len == 1:
        state.beacon_interval = params[0]
        status = 0
    else:
        status = 1

    return bytes([cmd_id, status])


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Initialize the satellite state with the provided beacon interval
    state = SatelliteState(beacon_interval=args.interval)

    # For now just print the state for manual verification
    print(state)


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
