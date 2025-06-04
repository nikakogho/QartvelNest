import argparse
import time
from dataclasses import dataclass

try:  # Optional dependency for the CLI loop
    import zmq  # type: ignore
except Exception:  # pragma: no cover - module may not be installed
    zmq = None

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


def crc16_ccitt(data: bytes) -> int:
    """Return CRC-16/CCITT of *data* (poly 0x1021, init 0xFFFF)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc & 0xFFFF


def crc16_x25(data: bytes) -> int:
    """Return CRC-16/X25 used for AX.25 frame FCS."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0x8408
            else:
                crc >>= 1
    return (~crc) & 0xFFFF


def _encode_ax25_address(name: str, ssid: int, final: bool) -> bytes:
    """Encode callsign and SSID into AX.25 address field."""
    name = name.ljust(6)
    addr = bytearray(ord(c) << 1 for c in name)
    last_bit = 1 if final else 0
    addr.append(((ssid & 0x0F) << 1) | 0x60 | last_bit)
    return bytes(addr)


def build_telemetry_payload(state: SatelliteState) -> bytes:
    """Return 9-byte telemetry payload with CRC appended."""
    body = bytearray(7)
    body[0] = 1  # Packet ID
    body[1:3] = state.uptime.to_bytes(2, "little")
    body[3:5] = state.batt_mv.to_bytes(2, "little")
    body[5] = (state.panel_temp & 0xFF)
    body[6] = state.beacon_interval & 0xFF
    crc = crc16_ccitt(body)
    body += crc.to_bytes(2, "little")
    return bytes(body)


def build_ax25_frame(payload: bytes) -> bytes:
    """Wrap *payload* in an AX.25 UI frame including FCS and flags."""
    dest = _encode_ax25_address("SAT1", 0, False)
    src = _encode_ax25_address("NEST", 0, True)
    frame_no_fcs = dest + src + bytes([0x03, 0xF0]) + payload
    fcs = crc16_x25(frame_no_fcs).to_bytes(2, "little")
    return bytes([0x7E]) + frame_no_fcs + fcs + bytes([0x7E])


def in_pass(elapsed: float) -> bool:
    """Return True if the satellite is in view at *elapsed* seconds."""
    return int(elapsed) % 60 < 30


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
    parser.add_argument(
        "--orbit",
        action="store_true",
        help="Enable simple visibility window simulation",
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
    parser.add_argument(
        "--pub",
        default="tcp://*:5567",
        help="ZeroMQ PUB endpoint for telemetry",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Send a single frame and exit",
    )
    args = parser.parse_args(argv)

    # Initialize the satellite state with the provided beacon interval
    state = SatelliteState(beacon_interval=args.interval)

    if zmq is None:
        # Graceful fallback for environments without ZeroMQ. Used in tests.
        print(state)
        return

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind(args.pub)

    try:
        start = time.time()
        while True:
            visible = not args.orbit or in_pass(time.time() - start)
            if visible:
                payload = build_telemetry_payload(state)
                frame = build_ax25_frame(payload)
                sock.send(frame)
                if args.once:
                    # Give ZeroMQ time to flush before closing
                    time.sleep(0.1)
                    break
            else:
                if args.once:
                    break

            time.sleep(state.beacon_interval)
            state.uptime += state.beacon_interval
    except KeyboardInterrupt:  # pragma: no cover - interactive use
        pass


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
