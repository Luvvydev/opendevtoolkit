<p align="center">
  <img src="assets/odt-plugins.png" width="800" />
</p>

# OpenDevToolkit

A modular CLI toolkit that groups small developer utilities under one command, with a plugin system built on Python entry points.

## Install

Local dev install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

Run:

```bash
odt --help
odt plugins
```

## Usage

```bash
odt --help
odt plugins
odt readme check README.md
odt time start "test"
odt time stop
odt time report --days 7


## Included tools

### Time tracking

Start and stop sessions:

```bash
odt time start "LuvvyAIO"
odt time status
odt time stop
odt time report --days 7
odt time export --out time.json
```

### README auditor

```bash
odt readme check README.md
```

Exit code is 0 if checks pass, 2 if something fails.

## Data directory

By default OpenDevToolkit writes state to a per-user data directory.

Override with:

```bash
odt --data-dir ./_odt_data time status
```

## Development

Run tests:

```bash
pip install -e ".[dev]"  # optional if you add dev extras
pytest
```

## License

MIT. See LICENSE.
