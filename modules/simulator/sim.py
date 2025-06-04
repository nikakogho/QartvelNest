import argparse
from dataclasses import dataclass


@dataclass
class SatelliteState:
    """Simple representation of satellite state."""

    uptime: int = 0
    batt_mv: int = 3000
    panel_temp: int = 25
    beacon_interval: int = 5


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


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Initialize the satellite state with the provided beacon interval
    state = SatelliteState(beacon_interval=args.interval)

    # For now just print the state for manual verification
    print(state)


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
