import subprocess
import sys
import time
from pathlib import Path

import pytest

try:
    import zmq  # type: ignore
except Exception:
    zmq = None

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))


@pytest.mark.skipif(zmq is None, reason="pyzmq not installed")
def test_simulator_sends_frame_over_zmq():
    script = ROOT / "modules" / "simulator" / "sim.py"
    endpoint = "tcp://127.0.0.1:5590"

    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect(endpoint)

    # Start simulator subprocess after subscriber is ready to avoid missing the message
    proc = subprocess.Popen(
        [sys.executable, str(script), "--pub", endpoint, "--interval", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Allow ZeroMQ handshake
    time.sleep(0.5)

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    events = dict(poller.poll(3000))  # wait up to 3 seconds
    assert sub in events, f"No frame received: stdout={proc.stdout.read()}"
    frame = sub.recv()

    proc.terminate()
    proc.wait(timeout=1)

    from modules.simulator.sim import crc16_x25, crc16_ccitt

    prefix = bytes.fromhex("7E A6 82 A8 62 40 40 60 9C 8A A6 A8 40 40 61 03 F0")
    assert frame.startswith(prefix)

    payload = frame[len(prefix):-3]
    fcs = int.from_bytes(frame[-3:-1], "little")
    assert crc16_x25(frame[1:-3]) == fcs
    assert crc16_ccitt(payload[:-2]) == int.from_bytes(payload[-2:], "little")
