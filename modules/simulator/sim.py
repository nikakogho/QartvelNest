import argparse


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
    parser.parse_args(argv)


if __name__ == "__main__":  # pragma: no cover - manual entry point
    main()
