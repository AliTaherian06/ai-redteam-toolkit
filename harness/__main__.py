"""Module entrypoint for python -m harness."""

from harness.cli import app


def main() -> None:
    """Runs the command line app."""
    app()


if __name__ == "__main__":
    main()
