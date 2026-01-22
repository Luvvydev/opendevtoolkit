from pathlib import Path
import typer
from rich import print

from ..types import PluginMeta
from ..paths import user_data_dir


class NotesPlugin:
    meta = PluginMeta(
        name="notes",
        version="0.1.0",
        description="Very simple local text notes.",
    )

    def register(self, app: typer.Typer) -> None:
        plugin_app = typer.Typer(no_args_is_help=True, help=self.meta.description)

        notes_dir = user_data_dir("opendevtoolkit") / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        @plugin_app.command("add")
        def add(text: str) -> None:
            note_file = notes_dir / "notes.txt"
            with note_file.open("a") as f:
                f.write(text + "\n")
            print("Note added.")

        @plugin_app.command("list")
        def list_notes() -> None:
            note_file = notes_dir / "notes.txt"
            if not note_file.exists():
                print("No notes yet.")
                return

            print(note_file.read_text())

        app.add_typer(plugin_app, name="notes", help="Local plain-text notes.")


def plugin_factory():
    return NotesPlugin()
