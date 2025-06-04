import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator.sim import SatelliteState


def test_state_defaults():
    state = SatelliteState()
    assert state.uptime == 0
    assert state.batt_mv == 3000
    assert state.panel_temp == 25
    assert state.beacon_interval == 5
