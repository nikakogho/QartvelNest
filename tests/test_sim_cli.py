import subprocess
import sys
from pathlib import Path

def test_sim_help():
    root = Path(__file__).resolve().parents[1]
    script = root / "modules" / "simulator" / "sim.py"
    result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "QartvelSat-1" in result.stdout
