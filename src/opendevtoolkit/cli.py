from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from . import __version__
from .plugin_loader import register_plugins, load_plugins
from .paths import user_data_dir


app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="OpenDevToolkit: a modular CLI with small, practical tools.",
)

console = Console()


@app.callback()
def _root(
    ctx: typer.Context,
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir",
        help="Override the user data directory (where toolkit modules can store state).",
    ),
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["data_dir"] = data_dir or user_data_dir("opendevtoolkit")
    ctx.obj["data_dir"].mkdir(parents=True, exist_ok=True)


@app.command()
def version() -> None:
    print(f"opendevtoolkit {__version__}")


@app.command()
def plugins() -> None:
    """List installed plugins discovered via entry points."""
    plugins = load_plugins()
    if not plugins:
        print("[yellow]No plugins found.[/yellow]")
        return

    table = Table(title="Plugins")
    table.add_column("Name", style="bold")
    table.add_column("Version")
    table.add_column("Description")

    for lp in sorted(plugins, key=lambda x: x.meta.name.lower()):
        table.add_row(lp.meta.name, lp.meta.version, lp.meta.description)

    console.print(table)


@app.command()
def doctor(ctx: typer.Context) -> None:
    """Basic sanity checks and paths."""
    data_dir: Path = ctx.obj["data_dir"]
    print("[bold]OpenDevToolkit Doctor[/bold]")
    print(f"Data dir: {data_dir}")
    print(f"Writable: {data_dir.exists() and data_dir.is_dir()}")
    # Keep this simple for now.


def main() -> None:
    register_plugins(app)
    app()


if __name__ == "__main__":
    main()
