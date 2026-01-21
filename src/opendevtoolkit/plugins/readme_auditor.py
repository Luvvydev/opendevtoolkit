from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import typer
from rich import print
from rich.table import Table

from ..types import PluginMeta


class ReadmeAuditorPlugin:
    meta = PluginMeta(
        name="readme-auditor",
        version="0.1.0",
        description="Checks a README for common presentation gaps (headers, install, usage, license, screenshots).",
    )

    def register(self, app: typer.Typer) -> None:
        plugin_app = typer.Typer(no_args_is_help=True, help=self.meta.description)

        @plugin_app.command("check")
        def check(
            path: Path = typer.Argument(Path("README.md"), help="Path to a README file."),
            min_sections: int = typer.Option(3, help="Minimum recommended number of top-level sections."),
        ) -> None:
            if not path.exists():
                raise typer.BadParameter(f"File not found: {path}")

            text = path.read_text(encoding="utf-8", errors="replace")
            findings = audit_readme(text, min_sections=min_sections)

            table = Table(title=f"README Audit: {path}")
            table.add_column("Check", style="bold")
            table.add_column("Result")
            table.add_column("Notes")

            for name, ok, notes in findings:
                table.add_row(name, "OK" if ok else "FAIL", notes)

            print(table)

            failed = [f for f in findings if not f[1]]
            if failed:
                raise typer.Exit(code=2)

        app.add_typer(plugin_app, name="readme", help="Audit README presentation and completeness.")


def audit_readme(text: str, min_sections: int = 3) -> List[Tuple[str, bool, str]]:
    t = text.strip()
    checks: List[Tuple[str, bool, str]] = []

    has_title = bool(re.search(r"^#\s+\S+", t, re.MULTILINE))
    checks.append(("Title header", has_title, "Expected a '# Title' at the top."))

    section_headers = re.findall(r"^##\s+(.+)$", t, re.MULTILINE)
    checks.append(("Sections", len(section_headers) >= min_sections, f"Found {len(section_headers)} '##' sections."))

    has_install = bool(re.search(r"\binstall\b|\bsetup\b|pip install|brew install", t, re.IGNORECASE))
    checks.append(("Install instructions", has_install, "Look for 'pip install ...' or explicit setup steps."))

    has_usage = bool(re.search(r"\busage\b|\bquickstart\b|\bexamples?\b", t, re.IGNORECASE))
    checks.append(("Usage section", has_usage, "Include a minimal command or example."))

    has_license = bool(re.search(r"\blicense\b", t, re.IGNORECASE))
    checks.append(("License mentioned", has_license, "Mention license and include a LICENSE file."))

    has_screenshot = bool(re.search(r"!\[[^\]]*\]\([^\)]+\)", t))
    checks.append(("Screenshot or image", has_screenshot, "One screenshot near the top helps adoption."))

    has_badges = bool(re.search(r"shields\.io|badge", t, re.IGNORECASE))
    checks.append(("Badges", has_badges, "Optional, but can help: CI, license, version, etc."))

    return checks


def plugin_factory() -> ReadmeAuditorPlugin:
    return ReadmeAuditorPlugin()
