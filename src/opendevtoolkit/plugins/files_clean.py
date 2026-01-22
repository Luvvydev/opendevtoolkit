from pathlib import Path
import typer
from rich import print

from ..types import PluginMeta


JUNK_PATTERNS = [
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
]


class FilesCleanPlugin:
    meta = PluginMeta(
        name="files-clean",
        version="0.1.0",
        description="Lists or removes common junk files and folders.",
    )

    def register(self, app: typer.Typer) -> None:
        plugin_app = typer.Typer(no_args_is_help=True, help=self.meta.description)

        @plugin_app.command("clean")
        def clean(
            path: Path = Path("."),
            apply: bool = typer.Option(False, help="Actually delete files"),
        ) -> None:
            matches = []

            for pattern in JUNK_PATTERNS:
                matches.extend(path.rglob(pattern))

            if not matches:
                print("No junk files found.")
                return

            for m in matches:
                print(f"{'DELETE' if apply else 'FOUND '} {m}")

            if apply:
                for m in matches:
                    if m.is_dir():
                        for child in m.rglob("*"):
                            child.unlink(missing_ok=True)
                        m.rmdir()
                    else:
                        m.unlink(missing_ok=True)

                print(f"Removed {len(matches)} item(s).")
            else:
                print("Dry run only. Use --apply to delete.")

        app.add_typer(plugin_app, name="files", help="List or remove junk files.")


def plugin_factory():
    return FilesCleanPlugin()
