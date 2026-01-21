from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import typer


@dataclass(frozen=True)
class PluginMeta:
    name: str
    version: str
    description: str


class ToolkitPlugin(Protocol):
    meta: PluginMeta

    def register(self, app: typer.Typer) -> None:
        ...
