# OpenDevToolkit

![CI](https://github.com/Luvvydev/opendevtoolkit/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

<p align="center">
  <img src="assets/odt-plugins.png" width="800" />
</p>

A modular, project-agnostic command-line toolkit that bundles small developer utilities under a single CLI using a plugin-based architecture.

OpenDevToolkit is local-first and explicit by design. It does not require accounts, configuration files, or external services. Tools operate only on what the user directly points them at.

---

## Install

Local development install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

Verify installation:

```bash
odt --help
odt plugins
```

---

## Usage

General commands:

```bash
odt --help
odt plugins
```

### README auditor

Checks a README file for common presentation gaps that reduce adoption.

```bash
odt readme check README.md
```

The command exits with a non-zero status if checks fail, making it suitable for CI.

---

### Time tracker

Lightweight, local-only time tracking stored in JSON.

```bash
odt time start "my-project"
odt time status
odt time stop
odt time report --days 7
odt time export --out time.json
```

No accounts. No sync. No cloud storage.

---

## Data storage

By default, OpenDevToolkit stores state in a per-user data directory.

You can override it explicitly:

```bash
odt --data-dir ./_odt_data time status
```

---

## Plugin system

OpenDevToolkit discovers plugins via Python entry points.

Each plugin:
- Declares metadata (name, version, description)
- Registers its own subcommands
- Runs independently of other plugins

See `docs/PLUGIN_SPEC.md` for the minimal plugin interface.

---

## Development

Run tests locally:

```bash
pip install pytest
pytest
```

CI runs tests automatically on push and pull requests.

---

## What this tool is

- A single CLI that replaces scattered scripts
- A container for small, focused developer utilities
- Local-first and explicit
- Extensible without modifying the core

## What this tool is not

- Not a framework
- Not a SaaS
- Not tied to any specific GitHub repository
- Not opinionated about workflow

---

## License

MIT License. See `LICENSE` for details.
