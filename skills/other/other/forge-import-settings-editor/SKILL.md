---
name: forge-import-settings-editor
description: Add per-asset import settings with TOML sidecar files, three-layer merge (schema → global → per-asset), a settings editor form with type-specific controls, and single-asset re-processing from the web UI. Use when someone needs configurable per-file processing overrides, settings UI, or sidecar-based configuration.
---

# forge-import-settings-editor

Add per-asset import settings to a pipeline web UI. Assets get individual
`.import.toml` sidecar files that override global config, and a browser-based
editor form renders type-specific controls for each setting.

## When to use this skill

- Adding per-asset configuration overrides to a processing pipeline
- Building a settings editor form driven by a schema definition
- Implementing three-layer settings merge (defaults → global → per-item)
- Adding TOML sidecar file I/O without a third-party TOML writer
- Triggering single-item re-processing from a web UI

## Key functions and endpoints

| Component | Function / Route | Purpose |
|---|---|---|
| `import_settings.py` | `sidecar_path(source)` | Return `.import.toml` path for a source file |
| `import_settings.py` | `load_sidecar(source)` | Parse sidecar TOML, empty dict if missing |
| `import_settings.py` | `save_sidecar(source, settings)` | Write settings to sidecar file |
| `import_settings.py` | `delete_sidecar(source)` | Remove sidecar (revert to defaults) |
| `import_settings.py` | `merge_settings(global, per_asset)` | Two-layer overlay merge |
| `import_settings.py` | `get_effective_settings(plugin, global, per_asset)` | Three-layer merge with schema defaults |
| `import_settings.py` | `get_schema(plugin_name)` | Return schema dict for a plugin type |
| `server.py` | `GET /api/assets/{id}/settings` | Read schema + global + per-asset + effective |
| `server.py` | `PUT /api/assets/{id}/settings` | Save per-asset overrides as `.import.toml` |
| `server.py` | `DELETE /api/assets/{id}/settings` | Remove sidecar (revert to defaults) |
| `server.py` | `POST /api/assets/{id}/process` | Re-process with effective settings |

## Architecture

Three-layer settings merge:

```text
Schema Defaults ──> Global Config (pipeline.toml) ──> Per-Asset (.import.toml)
       │                      │                              │
       └──────────────────────┴──────────────────────────────┘
                                    │
                              get_effective_settings()
                                    │
                              Effective Settings
```

Each layer overrides the previous. `get_effective_settings()` starts with
schema defaults, overlays global settings, then per-asset overrides.

## Correct order

### Backend

1. Define settings schemas in `import_settings.py` — one dict per plugin type
   with `type`, `label`, `description`, `default`, and optional constraints
2. Implement sidecar CRUD — `sidecar_path`, `load_sidecar`, `save_sidecar`,
   `delete_sidecar`
3. Implement merge functions — `merge_settings`, `get_effective_settings`
4. Add API endpoints to `server.py` — GET, PUT, DELETE for settings, POST for
   process
5. Integrate sidecars into CLI processing — load sidecars in `_process_files()`,
   include settings in fingerprint cache key

### Frontend

1. Add TypeScript types for `ImportSettingsResponse`, `SettingsSchemaField`,
   `ProcessResponse` in `api.ts`
2. Add API functions — `fetchImportSettings`, `saveImportSettings`,
   `deleteImportSettings`, `processAsset`
3. Add UI primitives — `Label`, `Select`, `Switch`, `Separator` in
   `components/ui/`
4. Build `ImportSettings` component with schema-driven form rendering
5. Mount on the asset detail page below the preview panel
6. Wire TanStack Query cache invalidation on mutations

## Settings schema definition

Each plugin type has a schema dict describing its configurable fields:

```python
TEXTURE_SETTINGS_SCHEMA: dict[str, dict] = {
    "max_size": {
        "type": "int",           # Control type: bool, int, float, str, list[float]
        "label": "Max size",     # Human-readable label
        "description": "Clamp width and height to this limit (pixels).",
        "default": 2048,         # Schema default value
        "min": 1,                # Optional: numeric minimum
        "max": 8192,             # Optional: numeric maximum
    },
    "compression": {
        "type": "str",
        "label": "GPU compression",
        "description": "GPU block-compression codec.",
        "default": "none",
        "options": ["none", "basisu", "astc"],  # Optional: enum values
    },
    "normal_map": {
        "type": "bool",
        "label": "Normal map",
        "description": "Treat as a normal map (BC5, linear color space).",
        "default": False,
    },
}

SETTINGS_SCHEMAS: dict[str, dict[str, dict]] = {
    "texture": TEXTURE_SETTINGS_SCHEMA,
    "mesh": MESH_SETTINGS_SCHEMA,
}
```

## TOML sidecar format

Sidecars are flat key-value TOML files. Only overridden keys are present:

```toml
normal_map = true
compression = "basisu"
basisu_quality = 200
```

Write TOML with string formatting — no third-party serializer needed for flat
tables. Check `isinstance(value, bool)` before `isinstance(value, int)` since
`bool` is a subclass of `int` in Python.

## Frontend control mapping

| Schema `type` | UI control | Notes |
|---|---|---|
| `bool` | `Switch` toggle | `onCheckedChange` callback |
| `str` with `options` | `Select` dropdown | Renders `<option>` per entry |
| `int` | `Input type="number"` | Uses `min`/`max` from schema |
| `float` | `Input type="number"` | `step={0.01}` |
| `list[float]` | `Input type="text"` | Comma-separated, parsed on change |

## Common mistakes

1. **Forgetting bool-before-int check in TOML formatting.** Python's `bool` is
   a subclass of `int`, so `isinstance(True, int)` is `True`. Always check
   `isinstance(value, bool)` first.

2. **Not including settings in the fingerprint cache key.** If only the content
   hash is cached, changing a sidecar does not trigger reprocessing. Combine
   the content hash with a JSON digest of the merged settings.

3. **Mutating the global settings dict during merge.** `merge_settings()` must
   return a new dict — never `.update()` the input.

4. **Not invalidating the right TanStack Query keys.** After processing, both
   `["asset", id]` and `["assets"]` (list) must be invalidated so the status
   badge and preview update.

5. **Missing error handling for malformed sidecars.** `load_sidecar()` should
   catch `TOMLDecodeError` and raise a clear `ValueError`. The CLI should
   log a warning and fall back to global settings; the API should return 400.

## Ready-to-use template

### import_settings.py — core pattern

```python
from pathlib import Path
import tomllib

SIDECAR_SUFFIX = ".import.toml"

def sidecar_path(source: Path) -> Path:
    return source.parent / (source.name + SIDECAR_SUFFIX)

def load_sidecar(source: Path) -> dict:
    path = sidecar_path(source)
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Malformed sidecar {path}: {exc}") from exc

def get_effective_settings(plugin_name: str, global_s: dict, per_asset: dict) -> dict:
    schema = SETTINGS_SCHEMAS.get(plugin_name, {})
    result = {key: spec["default"] for key, spec in schema.items()}
    result.update(global_s)
    result.update(per_asset)
    return result
```

### API endpoint pattern

```python
@app.get("/api/assets/{asset_id}/settings")
async def get_import_settings(asset_id: str):
    asset = _get_cached_asset(asset_id)
    plugin_name = _plugin_name_for_type(asset.asset_type)
    schema = get_schema(plugin_name)
    global_settings = config.plugin_settings.get(plugin_name, {})
    per_asset = load_sidecar(Path(asset.source_path))
    effective = get_effective_settings(plugin_name, global_settings, per_asset)
    return {
        "schema_fields": schema,
        "global_settings": global_settings,
        "per_asset": per_asset,
        "effective": effective,
        "has_overrides": bool(per_asset),
    }
```

### React component pattern

```tsx
const { data: settings } = useQuery({
  queryKey: ["settings", assetId],
  queryFn: () => fetchImportSettings(assetId),
})

const saveMutation = useMutation({
  mutationFn: (overrides) => saveImportSettings(assetId, overrides),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["settings", assetId] })
  },
})
```
