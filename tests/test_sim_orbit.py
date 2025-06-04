import threading
import sys
from pathlib import Path

import pytest
import zmq

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator import sim

@pytest.mark.skipif(not hasattr(sim, "zmq") or sim.zmq is None, reason="pyzmq not available")
def test_orbit_blocks_frames_outside_pass(monkeypatch):
    ctx = zmq.Context()
    monkeypatch.setattr(sim, "zmq", zmq)
    monkeypatch.setattr(sim.zmq, "Context", lambda: ctx)
    monkeypatch.setattr(sim, "in_pass", lambda elapsed: False)

    sub = ctx.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect("inproc://orbit0")

    thread = threading.Thread(
        target=sim.main,
        args=([
            "--pub",
            "inproc://orbit0",
            "--interval",
            "1",
            "--orbit",
            "--once",
        ],),
    )
    thread.start()
    thread.join(timeout=1)
    assert not thread.is_alive()

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    events = dict(poller.poll(100))
    assert sub not in events, "Frame sent despite orbit block"

    sub.close()
    ctx.term()


@pytest.mark.skipif(not hasattr(sim, "zmq") or sim.zmq is None, reason="pyzmq not available")
def test_orbit_allows_frames_inside_pass(monkeypatch):
    ctx = zmq.Context()
    monkeypatch.setattr(sim, "zmq", zmq)
    monkeypatch.setattr(sim.zmq, "Context", lambda: ctx)
    monkeypatch.setattr(sim, "in_pass", lambda elapsed: True)

    sub = ctx.socket(zmq.SUB)
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    sub.connect("inproc://orbit1")

    thread = threading.Thread(
        target=sim.main,
        args=([
            "--pub",
            "inproc://orbit1",
            "--interval",
            "1",
            "--orbit",
            "--once",
        ],),
    )
    thread.start()
    thread.join(timeout=1)
    assert not thread.is_alive()

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    events = dict(poller.poll(500))
    assert sub in events, "No frame received inside pass"
    frame = sub.recv()
    assert len(frame) > 0

    sub.close()
    ctx.term()
