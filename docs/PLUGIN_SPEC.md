# Plugin spec (MVP)

Plugins are discovered via Python entry points.

Group name:

- `opendevtoolkit.plugins`

Each entry point should point to a callable that returns an object with:

- `meta: PluginMeta`
- `register(app: typer.Typer) -> None`

See `src/opendevtoolkit/types.py` for the shape.
