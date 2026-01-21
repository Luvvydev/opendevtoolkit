from __future__ import annotations

import os
from pathlib import Path


def user_data_dir(app_name: str = "opendevtoolkit") -> Path:
    # Simple, cross-platform-ish directory selection without extra deps.
    # Windows: %APPDATA%\app_name
    # macOS/Linux: ~/.local/share/app_name (or ~/Library/Application Support/app_name if desired later)
    if os.name == "nt":
        root = os.getenv("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(root) / app_name

    xdg = os.getenv("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / app_name

    return Path.home() / ".local" / "share" / app_name
