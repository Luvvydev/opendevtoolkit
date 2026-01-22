from pathlib import Path
import typer
from rich import print
from rich.table import Table

from ..types import PluginMeta


class RepoCheckPlugin:
    meta = PluginMeta(
        name="repo-check",
        version="0.1.0",
        description="Checks a repository folder for basic hygiene issues.",
    )

    def register(self, app: typer.Typer) -> None:
        plugin_app = typer.Typer(no_args_is_help=True, help=self.meta.description)

        @plugin_app.command("check")
        def check(path: Path = Path(".")) -> None:
            table = Table(title=f"Repository check: {path.resolve()}")
            table.add_column("Check", style="bold")
            table.add_column("Result")
            table.add_column("Notes")

            def exists(p: Path) -> bool:
                return (path / p).exists()

            checks = [
                ("README.md", exists(Path("README.md")), "Top-level README file"),
                ("LICENSE", exists(Path("LICENSE")), "License file present"),
                (".gitignore", exists(Path(".gitignore")), "Git ignore rules"),
                ("src/", exists(Path("src")), "Source directory"),
            ]

            for name, ok, note in checks:
                table.add_row(name, "OK" if ok else "WARN", note)

            junk = list(path.glob("**/.DS_Store"))
            table.add_row(
                "Junk files",
                "OK" if not junk else "WARN",
                f"{len(junk)} .DS_Store file(s) found",
            )

            print(table)

        app.add_typer(plugin_app, name="repo", help="Basic repository hygiene checks.")


def plugin_factory():
    return RepoCheckPlugin()
