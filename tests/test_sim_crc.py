import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from modules.simulator.sim import crc16_ibm, crc16_ccitt, crc16_x25

VEC = b"123456789"

def test_crc16_ibm_vector():
    assert crc16_ibm(VEC) == 0x4B37


def test_crc16_ccitt_vector():
    assert crc16_ccitt(VEC) == 0x29B1


def test_crc16_x25_vector():
    assert crc16_x25(VEC) == 0x906E
