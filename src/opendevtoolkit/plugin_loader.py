from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import typer

from .types import ToolkitPlugin, PluginMeta

try:
    # Python 3.10+
    from importlib.metadata import entry_points
except Exception:  # pragma: no cover
    entry_points = None  # type: ignore


@dataclass(frozen=True)
class LoadedPlugin:
    meta: PluginMeta
    plugin: ToolkitPlugin


def _load_entrypoint_plugins(group: str = "opendevtoolkit.plugins") -> List[LoadedPlugin]:
    if entry_points is None:
        return []

    eps = entry_points()
    # Python 3.10 vs 3.11 API differences.
    if hasattr(eps, "select"):
        candidates = eps.select(group=group)
    else:  # pragma: no cover
        candidates = eps.get(group, [])

    loaded: List[LoadedPlugin] = []
    for ep in candidates:
        try:
            cls_or_factory = ep.load()
            plugin = cls_or_factory() if callable(cls_or_factory) else cls_or_factory
            meta = getattr(plugin, "meta", None)
            if not meta:
                continue
            loaded.append(LoadedPlugin(meta=meta, plugin=plugin))
        except Exception:
            # Keep plugin failures isolated; users still get the rest of the CLI.
            continue
    return loaded


def load_plugins() -> List[LoadedPlugin]:
    # For MVP we rely on installed entry points.
    # Later we can support a local plugins directory with dynamic loading.
    return _load_entrypoint_plugins()


def register_plugins(app: typer.Typer) -> List[LoadedPlugin]:
    plugins = load_plugins()
    for lp in plugins:
        try:
            lp.plugin.register(app)
        except Exception:
            # Avoid breaking the whole CLI.
            continue
    return plugins
