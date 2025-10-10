"""Utility helpers shared between Dash components."""

from pathlib import Path


def load_markdown(path: Path) -> str:
    """Read markdown content from disk."""
    return path.read_text(encoding="utf-8")

