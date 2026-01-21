from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

import typer
from rich import print
from rich.table import Table

from ..types import PluginMeta


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _dt_from_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _dt_to_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class Session:
    project: str
    start: datetime
    end: Optional[datetime] = None

    def duration_seconds(self) -> int:
        return int(((self.end or _utc_now()) - self.start).total_seconds())


class TimeTrackerPlugin:
    meta = PluginMeta(
        name="time-tracker",
        version="0.1.0",
        description="Simple time tracking sessions stored in a local JSON file.",
    )

    def register(self, app: typer.Typer) -> None:
        plugin_app = typer.Typer(no_args_is_help=True, help=self.meta.description)

        @plugin_app.callback()
        def _tt_ctx(ctx: typer.Context) -> None:
            data_dir: Path = ctx.find_object(dict)["data_dir"]  # set by root callback
            state_dir = data_dir / "time_tracker"
            state_dir.mkdir(parents=True, exist_ok=True)
            ctx.obj = {"state_path": state_dir / "state.json"}

        @plugin_app.command("start")
        def start(ctx: typer.Context, project: str = typer.Argument(..., help="Project name")) -> None:
            state_path: Path = ctx.obj["state_path"]
            state = load_state(state_path)
            active = get_active_session(state)
            if active:
                print(f"[red]Already tracking:[/red] {active.project} (started {_dt_to_iso(active.start)})")
                raise typer.Exit(code=2)

            sess = Session(project=project, start=_utc_now(), end=None)
            state["sessions"].append({"project": sess.project, "start": _dt_to_iso(sess.start), "end": None})
            save_state(state_path, state)
            print(f"[green]Started[/green] {project}")

        @plugin_app.command("stop")
        def stop(ctx: typer.Context) -> None:
            state_path: Path = ctx.obj["state_path"]
            state = load_state(state_path)
            idx = find_active_index(state)
            if idx is None:
                print("[yellow]No active session.[/yellow]")
                return

            state["sessions"][idx]["end"] = _dt_to_iso(_utc_now())
            save_state(state_path, state)
            print("[green]Stopped[/green]")

        @plugin_app.command("status")
        def status(ctx: typer.Context) -> None:
            state_path: Path = ctx.obj["state_path"]
            state = load_state(state_path)
            active = get_active_session(state)
            if not active:
                print("No active session.")
                return
            secs = active.duration_seconds()
            print(f"Tracking [bold]{active.project}[/bold] for {format_duration(secs)}")

        @plugin_app.command("report")
        def report(
            ctx: typer.Context,
            days: int = typer.Option(7, help="Lookback window (days)."),
            project: Optional[str] = typer.Option(None, help="Filter by project."),
        ) -> None:
            state_path: Path = ctx.obj["state_path"]
            state = load_state(state_path)

            cutoff = _utc_now() - timedelta(days=days)
            sessions = parse_sessions(state)
            sessions = [s for s in sessions if (s.end or _utc_now()) >= cutoff]
            if project:
                sessions = [s for s in sessions if s.project == project]

            totals: Dict[str, int] = {}
            for s in sessions:
                # Only count completed sessions in reports by default
                if s.end is None:
                    continue
                totals[s.project] = totals.get(s.project, 0) + s.duration_seconds()

            table = Table(title=f"Time Report (last {days} days)")
            table.add_column("Project", style="bold")
            table.add_column("Time")

            for proj, secs in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
                table.add_row(proj, format_duration(secs))

            if not totals:
                print("[yellow]No completed sessions in range.[/yellow]")
                return

            print(table)

        @plugin_app.command("export")
        def export(
            ctx: typer.Context,
            out: Path = typer.Option(Path("time_tracker_export.json"), help="Output JSON path"),
        ) -> None:
            state_path: Path = ctx.obj["state_path"]
            state = load_state(state_path)
            out.write_text(json.dumps(state, indent=2), encoding="utf-8")
            print(f"Wrote {out}")

        app.add_typer(plugin_app, name="time", help="Track time in small sessions.")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"sessions": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"sessions": []}


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def parse_sessions(state: dict) -> List[Session]:
    sessions: List[Session] = []
    for raw in state.get("sessions", []):
        try:
            start = _dt_from_iso(raw["start"])
            end = _dt_from_iso(raw["end"]) if raw.get("end") else None
            sessions.append(Session(project=raw["project"], start=start, end=end))
        except Exception:
            continue
    return sessions


def find_active_index(state: dict) -> Optional[int]:
    for i, raw in enumerate(state.get("sessions", [])):
        if raw.get("end") in (None, ""):
            return i
    return None


def get_active_session(state: dict) -> Optional[Session]:
    sessions = parse_sessions(state)
    active = [s for s in sessions if s.end is None]
    return active[-1] if active else None


def format_duration(secs: int) -> str:
    if secs < 0:
        secs = 0
    h = secs // 3600
    m = (secs % 3600) // 60
    s = secs % 60
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def plugin_factory() -> TimeTrackerPlugin:
    return TimeTrackerPlugin()
