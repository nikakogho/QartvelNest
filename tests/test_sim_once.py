import threading
import sys
import time
from pathlib import Path

import pytest
import zmq

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator import sim


@pytest.mark.skipif(not hasattr(sim, "zmq") or sim.zmq is None, reason="pyzmq not available")
def test_simulator_once_flag_sends_single_frame(monkeypatch):
    ctx = zmq.Context()
    # Use the same context inside the simulator
    monkeypatch.setattr(sim, "zmq", zmq)
    monkeypatch.setattr(sim.zmq, "Context", lambda: ctx)

    sub = ctx.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect("inproc://testonce")

    thread = threading.Thread(
        target=sim.main,
        args=([
            "--pub",
            "inproc://testonce",
            "--interval",
            "1",
            "--once",
        ],),
    )
    thread.start()
    # Give the simulator time to bind and send the frame
    time.sleep(0.1)

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    events = dict(poller.poll(1000))
    assert sub in events, "No frame received"
    frame = sub.recv()

    thread.join(timeout=1)
    assert not thread.is_alive()

    events = dict(poller.poll(500))
    assert sub not in events, f"Additional frame received: {len(frame)}"

    sub.close()
    ctx.term()
