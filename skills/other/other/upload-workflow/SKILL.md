---
name: synapse-upload-workflow
description: >
  Use when user mentions "upload", "data collection", "file specifications",
  "data units", "organize files", "map files to specs", "bulk upload",
  "s3 upload", "cloud storage", "multi-path", "excel metadata".
---

# Synapse Upload Workflow

Core knowledge for uploading files to Synapse data collections. Covers local and cloud sources, single-path and multi-path modes, and Excel metadata integration.

## Interactive-First Principle

This workflow is designed to be **fully interactive**. When the user invokes the upload with missing parameters (or no parameters at all), use `AskUserQuestion` to guide them through each step. Never fail or show usage text for missing arguments — always ask conversationally. Offer to list data collections from the API and show the default storage if the user doesn't know the IDs. Validate each input immediately and re-ask if invalid.

## Prerequisites Validation

Before starting any upload workflow, ensure the `synapse` CLI is available and validate the environment.

### Finding synapse CLI

```bash
# 1. Try the current shell first (venv may already be activated)
synapse --version

# 2. If not found, search for a venv directory in cwd
ls -d *venv* .venv 2>/dev/null
# Activate the first match, e.g.: source .venv/bin/activate
```

If no venv is found and `synapse` is not on PATH, guide the user to activate their environment or install: `uv pip install "synapse-sdk>=2026.1.39"`

### Assert version

```bash
python3 -c "
from importlib.metadata import version
v = version('synapse-sdk')
parts = [int(x) for x in v.split('.')[:3]]
assert parts >= [2026, 1, 39], f'synapse-sdk {v} is too old, need >= 2026.1.39'
print(f'synapse-sdk {v} OK')
"
```

### Validate environment

```bash
synapse doctor
```

This validates in one shot:
- Config file exists at `~/.synapse/config.json`
- CLI authentication (host + access token)
- Token validity (not expired)
- Agent configuration

**Required**: Authentication and token checks must pass. MCP warnings are non-blocking for uploads.

If auth fails: `synapse login` to re-authenticate.

## Key Concepts

### Data Collection File Specifications

A data collection defines **file specifications** — the expected file types for each data unit:

```json
[
  {
    "id": 101,
    "name": "image_1",
    "file_type": "image",
    "extensions": [".png", ".jpg", ".jpeg"],
    "is_required": true
  },
  {
    "id": 102,
    "name": "label_1",
    "file_type": "document",
    "extensions": [".json"],
    "is_required": true
  },
  {
    "id": 103,
    "name": "dicom_1",
    "file_type": "medical",
    "extensions": [".dcm", ".dicom"],
    "is_required": false
  }
]
```

Each data unit must have files matching the **required** specs. Optional specs may be omitted.

### Data Units

A **data unit** is one logical record in a data collection. It contains one file per spec, plus optional **metadata**:

```
Data Unit "patient_001":
  image_1 → patient_001/scan.png
  label_1 → patient_001/annotations.json
  dicom_1 → patient_001/original.dcm
  meta    → {"patient_id": "P001", "age": 45, "diagnosis": "normal"}
```

### Data Unit Metadata (`DataUnit.meta`)

Every data unit has a `meta` field — a JSON object for storing arbitrary per-data-unit metadata (patient info, acquisition parameters, source filenames, custom tags, etc.).

**Key facts:**
- `meta` is a `dict[str, Any]` passed via `DataUnitCreateRequest.meta` when creating data units
- If the data collection defines a **`data_unit_meta_schema`** (JSON Schema), the backend validates every data unit's `meta` against it — invalid meta will be rejected
- The schema is stored in `DataCollection.meta['data_unit_meta_schema']`

**Always check for a meta schema** when fetching the data collection:

```python
dc = client.get_data_collection(DC_ID)
meta_schema = dc.get('meta', {}).get('data_unit_meta_schema')
if meta_schema:
    print(f"Data unit meta schema: {json.dumps(meta_schema, indent=2)}")
    # Example schema:
    # {"type": "object", "required": ["patient_id"], "properties": {
    #     "patient_id": {"type": "string"},
    #     "age": {"type": "integer"},
    #     "diagnosis": {"type": "string"}
    # }}
```

If a schema exists, **you must inform the user** about the required/expected fields and ensure the upload script populates `meta` accordingly. Sources of metadata:
- **Excel file** (`--metadata`): Each row provides metadata keyed by a grouping column
- **Directory names**: e.g., `{"name": "patient_001"}`
- **Filename patterns**: Parse structured filenames (e.g., `P001_45_male.png` → `{"patient_id": "P001", "age": 45, "sex": "male"}`)
- **User-provided values**: Ask the user interactively what metadata to set
- **Sidecar files**: JSON/YAML files alongside the data files

If no schema exists, `meta` is still useful — populate it with at least a descriptive `name` or `dataset_key` for traceability.

### Storage

Files are uploaded to a **storage** (S3, GCS, MinIO, Azure, SFTP, or local filesystem). The storage ID identifies the target. Upload uses presigned URLs for efficient parallel transfer.

## Source Path Types & Validation

Source paths can be local or remote. **Always validate before exploring.**

### Path Type Detection

| Path Pattern | Type | Provider | Example |
|-------------|------|----------|---------|
| `/absolute/path` | Local filesystem | `local` | `/mnt/data/scans` |
| `./relative` or `~/home` | Local filesystem | `local` | `./data/scans` |
| `s3://bucket/prefix` | Amazon S3 / MinIO | `s3` | `s3://my-bucket/datasets/ct` |
| `gs://bucket/prefix` | Google Cloud Storage | `gcs` | `gs://my-bucket/datasets/ct` |
| `sftp://host/path` | SFTP server | `sftp` | `sftp://nas.local/data` |
| No scheme, no leading `/` | Storage-relative | (from storage config) | `datasets/batch_42` |

### Validation Snippets

You are an AI assistant — write temporary Python to validate any path type:

**Local path:**
```python
from pathlib import Path
p = Path("/data/scans")
if not p.exists():
    raise FileNotFoundError(f"Path not found: {p}")
if not p.is_dir():
    raise NotADirectoryError(f"Not a directory: {p}")
print(f"OK: {sum(1 for _ in p.rglob('*') if _.is_file())} files")
```

**Cloud / remote paths via SDK:**
```python
from synapse_sdk.utils.storage import get_pathlib

# Option A: Use storage config from the backend
from synapse_sdk.clients.backend import BackendClient
import json, os
config_path = os.path.expanduser('~/.synapse/config.json')
with open(config_path) as f:
    cfg = json.load(f)
client = BackendClient(
    base_url=cfg['host'],
    access_token=cfg['access_token'],
)
storage = client.get_storage(<STORAGE_ID>)
storage_config = {"provider": storage["provider"], "configuration": storage["configuration"]}
root = get_pathlib(storage_config, "<user_path>")

# Option B: Construct directly for a known provider
root = get_pathlib({"provider": "s3", "configuration": {
    "bucket_name": "my-bucket",
    "access_key": os.environ["AWS_ACCESS_KEY_ID"],
    "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region_name": "us-east-1",
}}, "datasets/ct")

# Validate
assert root.exists(), f"Path not accessible: {root}"
entries = list(root.iterdir())
print(f"OK: {len(entries)} top-level entries")
```

**`get_pathlib()` returns:**
- `pathlib.Path` for local filesystem
- `upath.UPath` for S3, GCS, SFTP (same API: `.iterdir()`, `.rglob()`, `.stat()`, `.is_dir()`, `.is_file()`)

### Exploring Cloud Sources

Cloud paths can't use Bash `ls`/`find`. Write Python with `UPath`:

```python
from synapse_sdk.utils.storage import get_pathlib
from collections import Counter
import json

root = get_pathlib(storage_config, user_path)

# Top-level listing
for item in sorted(root.iterdir(), key=lambda x: x.name)[:30]:
    kind = "dir" if item.is_dir() else f"file ({item.stat().st_size} bytes)"
    print(f"  {item.name} [{kind}]")

# Extension counts (sample for large datasets)
exts = Counter()
for f in root.rglob("*"):
    if f.is_file():
        exts[f.suffix.lower()] += 1
        if sum(exts.values()) > 5000:
            print("(sampled 5000 files)")
            break
print(json.dumps(dict(exts.most_common(20))))
```

## Upload Modes

### Single-Path Mode (default)

All file specifications share one source directory. The upload plugin scans this directory and maps files to specs.

```json
{
  "use_single_path": true,
  "path": "/data/patient_scans",
  "is_recursive": true,
  "storage": 11,
  "data_collection": 42
}
```

### Multi-Path Mode

Each file specification has its own source path and recursive setting. Use when data is split across different locations — possibly different storage types.

```json
{
  "use_single_path": false,
  "assets": {
    "image_1": {"path": "/mnt/nas/images", "is_recursive": true},
    "label_1": {"path": "s3://ml-data/annotations", "is_recursive": true},
    "dicom_1": {"path": "/archive/dicoms", "is_recursive": false}
  },
  "storage": 11,
  "data_collection": 42
}
```

**When to use multi-path:**
- Files for different specs live in different directories
- Some specs come from cloud storage, others from local disk
- Image files on NAS, labels on S3, metadata on local disk
- Each spec has different recursive scan needs

**Multi-path validation:**
- Validate each asset path independently (they can be different types)
- Each asset maps to exactly one file spec name
- The spec names in `assets` must match the data collection's file specifications

### AssetConfig Structure

Each entry in `assets` is an `AssetConfig`:

```json
{
  "path": "/data/images",     // Source path (local, s3://, gs://, sftp://, or storage-relative)
  "is_recursive": true         // Whether to recursively scan subdirectories (default: true)
}
```

## Excel Metadata

Upload supports an optional Excel metadata file that provides additional per-data-unit metadata.

### How It Works

1. The Excel file is passed via `excel_metadata_path` parameter
2. The upload plugin reads it during the metadata extraction step
3. Metadata from the Excel file is merged into each data unit's metadata

### Path Resolution

The `excel_metadata_path` is resolved in this order:
1. **Absolute path**: `/data/meta.xlsx` → used directly
2. **Relative to storage default path**: `meta.xlsx` → resolved via `get_pathlib(storage, "meta.xlsx")`
3. **Relative to working directory** (single-path mode): `./meta.xlsx` → resolved relative to the `path` parameter

### Expected Excel Format

Standard filenames: `meta.xlsx`, `meta.xls`, `metadata.xlsx`, `metadata.xls`

The Excel file typically contains:
- One row per data unit
- A column that serves as the grouping key (matching directory names or file stems)
- Additional columns with metadata values

### Passing Metadata to Upload

```json
{
  "name": "Upload with Metadata",
  "path": "/data/scans",
  "storage": 11,
  "data_collection": 42,
  "excel_metadata_path": "/data/meta.xlsx"
}
```

Or for storage-relative:
```json
{
  "excel_metadata_path": "metadata/batch_42.xlsx"
}
```

### Validating Excel Before Upload

Write a quick check:

```python
import openpyxl
wb = openpyxl.load_workbook("/data/meta.xlsx", read_only=True)
ws = wb.active
headers = [cell.value for cell in ws[1]]
row_count = ws.max_row - 1  # exclude header
print(f"Headers: {headers}")
print(f"Data rows: {row_count}")
wb.close()
```

## Directory Patterns

### Pattern 1: Nested Subdirectories (most common)

```
data/
├── patient_001/
│   ├── image.png
│   ├── label.json
│   └── scan.dcm
├── patient_002/
│   ├── image.png
│   ├── label.json
│   └── scan.dcm
└── ...
```

**Grouping**: Each subdirectory = one data unit.
**Mapping**: Match files by extension to specs.
**Mode**: Single-path.

### Pattern 2: Type-Separated Directories

```
data/
├── images/
│   ├── 001.png
│   ├── 002.png
│   └── ...
├── labels/
│   ├── 001.json
│   ├── 002.json
│   └── ...
└── dicoms/
    ├── 001.dcm
    └── ...
```

**Grouping**: Match files across directories by filename stem.
**Mapping**: Directory name or extension determines spec.
**Mode**: Single-path (if under one root) or multi-path (if in different locations).

### Pattern 3: Flat Directory with Matching Stems

```
data/
├── sample_001.png
├── sample_001.json
├── sample_002.png
├── sample_002.json
└── ...
```

**Grouping**: Group by filename stem (before extension).
**Mapping**: Extension determines spec.
**Mode**: Single-path.

### Pattern 4: Deeply Nested with Type Subdirs

```
data/
├── patient_001/
│   ├── img/
│   │   └── scan.png
│   ├── json/
│   │   └── label.json
│   └── mask/
│       └── segmentation.png
└── patient_002/
    ├── img/
    │   └── scan.png
    └── json/
        └── label.json
```

**Grouping**: Top-level subdirectory = one data unit.
**Mapping**: Sub-directory name + extension determines spec.
**Mode**: Single-path.

### Pattern 5: Mixed Sources (multi-path)

```
Source A (NAS):        /mnt/nas/project_x/images/*.png
Source B (S3):         s3://ml-data/project_x/labels/*.json
Source C (Local):      /tmp/converted/masks/*.png
```

**Grouping**: Match by filename stem across sources.
**Mapping**: Each source → one spec.
**Mode**: Multi-path with assets config.

## Upload Pipeline Stages

1. **Initialize** — Validate storage access, resolve paths (local or cloud via `get_pathlib`)
2. **Analyze Collection** — Fetch data collection specs and `data_unit_meta_schema` from backend API
3. **Explore Source** — Understand file structure (adapt method to path type)
4. **Organize Files** — Map files to specs, group into data units
5. **Prepare Metadata** — Check if `data_unit_meta_schema` exists; gather metadata from Excel, filenames, sidecar files, or user input; validate against schema
6. **Validate** — Check all required specs are satisfied per data unit; validate meta against schema
7. **Upload** — Transfer files to storage via presigned URLs (parallel workers)
8. **Create Data Units** — Register uploaded files as data units with `meta` populated
9. **Report** — Summary of results

## SDK Helper Snippets

### Listing Data Collections (for interactive wizard)

When the user doesn't know their data collection ID, list available ones:

```bash
python3 -c "
from synapse_sdk.clients.backend import BackendClient
import os
config_path = os.path.expanduser('~/.synapse/config.json')
with open(config_path) as f:
    cfg = json.load(f)
client = BackendClient(
    base_url=cfg['host'],
    access_token=cfg['access_token'],
)
dcs = client.list_data_collections()
for dc in dcs.get('results', [])[:20]:
    specs = dc.get('file_specifications', [])
    spec_count = len(specs)
    print(f\"  ID {dc['id']}: {dc.get('name', 'Unnamed')} ({spec_count} specs)\")
"
```

### Getting Storage (for interactive wizard)

When the user doesn't know their storage ID, get the default storage or look up by ID:

```bash
python3 -c "
from synapse_sdk.clients.backend import BackendClient
import json, os
config_path = os.path.expanduser('~/.synapse/config.json')
with open(config_path) as f:
    cfg = json.load(f)
client = BackendClient(
    base_url=cfg['host'],
    access_token=cfg['access_token'],
)
# Get default storage
default = client.get_default_storage()
print(f\"Default storage — ID {default['id']}: {default.get('name', 'Unnamed')} [{default.get('provider', '?')}]\")

# Or get a specific storage by ID
# storage = client.get_storage(<id>)
"
```

**Note**: The SDK does not have a `list_storages` method. Available methods are `get_default_storage()` and `get_storage(id)`. If the user needs help finding a storage, show them the default storage and ask if that's the right one, or ask them to provide the ID directly.

### Fetching Data Collection Specs & Meta Schema

```bash
python3 -c "
from synapse_sdk.clients.backend import BackendClient
import json, os
config_path = os.path.expanduser('~/.synapse/config.json')
with open(config_path) as f:
    cfg = json.load(f)
client = BackendClient(
    base_url=cfg['host'],
    access_token=cfg['access_token'],
)
dc = client.get_data_collection(<DATA_COLLECTION_ID>)
meta_schema = dc.get('meta', {}).get('data_unit_meta_schema')
print(json.dumps({
    'name': dc.get('name', ''),
    'file_specifications': dc.get('file_specifications', []),
    'data_unit_meta_schema': meta_schema,
}, indent=2, default=str))
"
```

If `data_unit_meta_schema` is not `null`, inform the user about required metadata fields and ensure the upload script populates `meta` accordingly.

## Upload Parameters (UploadParams)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | string | Yes | — | Descriptive name for the upload |
| `use_single_path` | bool | No | true | Single-path vs multi-path mode |
| `path` | string | Yes* | — | Source path (single-path mode) — local or cloud |
| `is_recursive` | bool | No | true | Recursively scan subdirectories (single-path) |
| `assets` | dict | Yes** | null | Per-spec path config (multi-path mode) |
| `storage` | int | Yes | — | Storage ID |
| `data_collection` | int | Yes | — | Data collection ID |
| `project` | int | No | null | Project ID for task creation |
| `excel_metadata_path` | string | No | null | Path to Excel metadata file |
| `max_file_size_mb` | int | No | 50 | Max file size in MB |
| `creating_data_unit_batch_size` | int | No | 1 | Batch size for data unit creation |
| `use_async_upload` | bool | No | true | Use async upload processing |
| `extra_params` | dict | No | null | Extra parameters for the action |

*Required when `use_single_path=true`. **Required when `use_single_path=false`.

## Running Upload via Script Submission

Uploads run as Python scripts submitted to the agent's Ray cluster via `synapse script submit`. Claude writes a dataset-specific upload script using `BackendClient`, then submits it. Credentials are auto-injected.

### Workflow

1. Write an upload script to `/tmp/synapse_upload_<name>.py` using `BackendClient`
2. Submit: `synapse script submit /tmp/synapse_upload_<name>.py`
3. Tell user: `synapse script logs <job-id> --follow` to monitor

### Script Pattern

```python
#!/usr/bin/env python3
"""Upload script — adapt to dataset structure."""
import os
from pathlib import Path
from synapse_sdk.clients.backend import BackendClient

client = BackendClient(
    base_url=os.environ['SYNAPSE_HOST'],
    access_token=os.environ['SYNAPSE_ACCESS_TOKEN'],
)

# 1. Fetch specs
dc = client.get_data_collection(<DC_ID>)
specs = dc['file_specifications']

# 2. Walk source, group files into data units
#    (adapt grouping logic to the specific dataset)

# 3. Upload files
result = client.upload_files_bulk(all_file_paths, max_workers=32)

# 4. Create data units in batches
#    'meta' is optional but recommended — if the collection has a
#    data_unit_meta_schema, meta MUST conform to it or creation will fail.
client.create_data_units([{
    'data_collection': <DC_ID>,
    'files': {spec_name: {'checksum': checksum, 'path': filename}},
    'meta': {'name': group_key, ...},  # populate from Excel, filenames, user input, etc.
}])
```

### Key SDK Methods

| Method | Purpose |
|--------|---------|
| `client.get_data_collection(id)` | Fetch specs, meta schema (`dc['meta']['data_unit_meta_schema']`) |
| `client.upload_files_bulk(paths, max_workers=32)` | Upload files via presigned URLs with parallel workers |
| `client.create_data_units(data)` | Link uploaded files to data collection as data units (each entry can include `meta`) |
| `client.get_default_storage()` | Get default storage config |
| `client.get_storage(id)` | Get specific storage config |

### Submission

```bash
# Submit script (returns job ID immediately)
synapse script submit /tmp/synapse_upload_<name>.py

# Submit with extra requirements
synapse script submit /tmp/synapse_upload_<name>.py -r requirements.txt
```

Tell the user how to monitor after submission:

```bash
# Stream logs in real-time
synapse script logs <job-id> --follow

# Check logs later
synapse script logs <job-id>

# Stop a running job
synapse script stop <job-id>
```

The script runs on the agent's Ray cluster with auto-injected `SYNAPSE_HOST` and `SYNAPSE_ACCESS_TOKEN` and storage mount access.

## Large Dataset Strategies (10K+ files)

1. **Sample, don't enumerate**: Look at 2-3 representative subdirs, then infer the pattern
2. **Use glob patterns**: Count files instead of listing them
3. **High batch size**: Set `creating_data_unit_batch_size` to 50-100 for faster data unit creation
4. **Job mode**: Use `--mode job` for long uploads to avoid CLI timeouts
5. **Tell user how to monitor**: `synapse script logs <job-id> --follow`
6. **organize_files_by_pattern**: For the ai-upload-plugin, use the batch tool with glob patterns and a grouping regex

## Batch Pattern Organization (ai-upload-plugin)

For large datasets, use `organize_files_by_pattern` with:

```json
{
  "root": "/data/patients",
  "file_rules": [
    {"pattern": "**/img/*.png", "spec_name": "image_1"},
    {"pattern": "**/json/*.json", "spec_name": "label_1"}
  ],
  "group_key_regex": "(.+?)/(?:img|json)/",
  "dataset_key_template": "{group_key}"
}
```

This processes thousands of files without enumerating each one individually.
