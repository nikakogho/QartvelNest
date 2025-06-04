import subprocess
import sys
from pathlib import Path

def test_sim_help():
    root = Path(__file__).resolve().parents[1]
    script = root / "modules" / "simulator" / "sim.py"
    result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "QartvelSat-1" in result.stdout


def test_sim_interval_output():
    """Ensure CLI prints state with the requested beacon interval."""
    root = Path(__file__).resolve().parents[1]
    script = root / "modules" / "simulator" / "sim.py"
    cmd = (
        "import runpy, sys; sys.modules['zmq']=None;"
        "sys.argv=['sim.py','--interval','12'];"
        "runpy.run_path('modules/simulator/sim.py', run_name='__main__')"
    )
    result = subprocess.run(
        [sys.executable, "-c", cmd],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "beacon_interval=12" in result.stdout
