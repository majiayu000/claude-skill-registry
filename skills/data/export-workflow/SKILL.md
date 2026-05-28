---
name: synapse-export-workflow
description: >
  Use when user mentions "export", "download annotations", "ground truth",
  "export project", "COCO format", "YOLO format", "Pascal VOC",
  "export assignments", "export tasks", "download labels".
---

# Synapse Export Workflow

Core knowledge for exporting annotation data, ground truth datasets, and task data from Synapse. Covers three export targets, multiple output formats, and both plugin-based and script-based execution.

## Interactive-First Principle

This workflow is designed to be **fully interactive**. When the user invokes the export with missing parameters, use `AskUserQuestion` to guide them through each step. Never fail or show usage text for missing arguments — always ask conversationally.

## Prerequisites Validation

Before starting any export workflow, ensure the `synapse` CLI is available and validate the environment.

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

**Required**: Authentication and token checks must pass.

If auth fails: `synapse login` to re-authenticate.

## Key Concepts

### Export Targets

Synapse exports data from one of three **targets** — each represents a different stage of the annotation pipeline:

| Target | Description | Required Filter | Use Case |
|--------|-------------|----------------|----------|
| `assignment` | Annotation work by labelers/reviewers | `project` ID | Export labeled results, QA reviews |
| `ground_truth` | Curated reference datasets for ML | `ground_truth_dataset_version` ID | Export training/validation data |
| `task` | Tasks with data unit links and annotations | `project` ID | Export task metadata + annotations |

### Target Data Structure

Each export target yields items with this structure:

```python
{
    'data': { ... },    # Annotation data (DM Schema v1 format)
    'files': { ... },   # File metadata (URLs, dimensions, etc.)
    'id': 123,          # Record ID (assignment/ground_truth_event/task)
}
```

**Annotation data** follows the **DM Schema v1** format:
```json
{
    "assignmentId": "job-123",
    "annotations": {
        "image_1": [
            {"id": "abc123", "type": "bbox", "data": [100, 200, 50, 80], "classification": "car", ...},
            {"id": "def456", "type": "polygon", "data": [[10,20],[30,40],...], "classification": "road", ...}
        ]
    },
    "annotationsData": {
        "image_1": [
            {"id": "abc123", "type": "bbox", ...},
            {"id": "def456", "type": "polygon", ...}
        ]
    },
    "relations": {},
    "annotationGroups": {},
    "extra": {}
}
```

**Key annotation types** in `annotations`:
- **bbox** (bounding box): `data: [x, y, width, height]`
- **polygon**: `data: [[x1,y1], [x2,y2], ...]`
- **polyline**: `data: [[x1,y1], [x2,y2], ...]`
- **keypoint**: `data: [[x1,y1], [x2,y2], ...]` with skeleton
- **classification**: label-only, no spatial data

### Export Formats

Common output formats the skill should support:

| Format | Extension | Description |
|--------|-----------|-------------|
| **Synapse JSON** | `.json` | Raw DM Schema — lossless, full fidelity |
| **COCO** | `.json` | MS COCO format — bbox, segmentation, keypoints |
| **YOLO** | `.txt` | YOLO darknet — one `.txt` per image with `class x_center y_center width height` |
| **Pascal VOC** | `.xml` | VOC XML format — bounding boxes |
| **CSV** | `.csv` | Tabular — flatten annotations to rows |
| **Custom** | varies | User-defined transformation |

The SDK includes converters for some formats:
```python
from synapse_sdk.utils.converters.coco.from_dm import DMtoCOCOConverter
# converter = DMtoCOCOConverter()
# coco_data = converter.convert(dm_v1_data, output_dir, original_file_dir)
```

### Storage

Export output is written to a **storage** destination. This can be:
- The agent's mounted storage (accessible from Ray worker)
- A remote storage (S3, GCS, MinIO) via `get_pathlib()`
- Local filesystem on the Ray worker (temporary)

### Project & Ground Truth Discovery

**Listing projects:**
```python
# No SDK method for listing projects directly — use the backend API
import requests
resp = requests.get(
    f"{os.environ['SYNAPSE_HOST']}/api/annotation/projects/",
    headers={"Authorization": f"Token {os.environ['SYNAPSE_ACCESS_TOKEN']}"},
)
projects = resp.json()['results']
for p in projects:
    print(f"  ID {p['id']}: {p['name']}")
```

**Listing ground truth datasets:**
```python
from synapse_sdk.clients.backend import BackendClient
client = BackendClient(
    base_url=os.environ['SYNAPSE_HOST'],
    access_token=os.environ['SYNAPSE_ACCESS_TOKEN'],
)
# List GT versions for a dataset
versions = client.list_ground_truth_versions(params={'ground_truth_dataset': <dataset_id>})
```

## Export Approaches

### Approach 1: Script-Based Export (Recommended)

Write a custom Python export script and submit via `synapse script submit`. This gives full control over:
- Output format (COCO, YOLO, CSV, custom)
- Filtering and post-processing
- File organization
- Local or remote output

**Script pattern:**
```python
#!/usr/bin/env python3
"""Export annotations from project <PROJECT_ID>."""
import json
import os
from pathlib import Path
from synapse_sdk.clients.backend import BackendClient

client = BackendClient(
    base_url=os.environ['SYNAPSE_HOST'],
    access_token=os.environ['SYNAPSE_ACCESS_TOKEN'],
)

PROJECT_ID = <project_id>
OUTPUT_DIR = Path('/tmp/export_output')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Fetch all assignments for the project
# list_all=True returns (generator, count) tuple
results_gen, count = client.list_assignments(
    params={'project': PROJECT_ID},
    list_all=True,
)
print(f"Found {count} assignments to export")

# Export each assignment
for i, assignment in enumerate(results_gen):
    data = assignment['data']       # DM Schema v1 annotation data (from hitl_assignment.data)
    files = assignment.get('file')  # File metadata
    assignment_id = assignment['id']

    # === CONVERT TO DESIRED FORMAT HERE ===
    # Example: save as raw JSON
    output_path = OUTPUT_DIR / f'{assignment_id}.json'
    with open(output_path, 'w') as f:
        json.dump({'data': data, 'files': files, 'id': assignment_id}, f, indent=2)

    if (i + 1) % 100 == 0:
        print(f"Exported {i + 1}/{count}...")

print(f"\nDone! Exported {count} assignments to {OUTPUT_DIR}")
```

**Adapt the conversion section** to the desired output format (COCO, YOLO, etc.).

### Approach 2: Plugin-Based Export

If an export plugin is installed on the agent, use the plugin framework:

```bash
synapse plugin run export --plugin <plugin-code> --mode job --params '{
    "name": "My Export",
    "target": "assignment",
    "filter": {"project": 123},
    "storage": 11,
    "path": "/exports/my_export",
    "save_original_file": true,
    "extra_params": {}
}'
```

Tell the user how to monitor and stop:
```bash
synapse plugin job get <job-id>
synapse plugin job logs <job-id> --follow
synapse script stop <job-id>
```

**When to use plugin-based export:**
- An export plugin is already installed and configured
- The plugin supports the desired output format
- The user wants the standard export pipeline (fetch → convert → save to storage)

## Export Parameters (Plugin Mode)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `name` | string | Yes | — | Human-readable export name |
| `description` | string | No | null | Export description |
| `target` | string | Yes | — | `assignment`, `ground_truth`, or `task` |
| `filter` | dict | Yes | — | Target-specific filter (see below) |
| `storage` | int | Yes | — | Destination storage ID |
| `path` | string | Yes | — | Export path within storage |
| `save_original_file` | bool | No | true | Include original data files |
| `extra_params` | dict | No | null | Format-specific options |

### Filter by Target

| Target | Required Fields | Optional Fields |
|--------|----------------|-----------------|
| `assignment` | `project` (int) | `status`, `user`, `tags`, date range |
| `ground_truth` | `ground_truth_dataset_version` (int) | `category` (train/validation/test) |
| `task` | `project` (int) | `status`, `tags`, date range |

## Export Plugin Architecture

Export plugins extend `BaseExporter` from `synapse_sdk.plugins.categories.export.templates.plugin`. Understanding the plugin structure helps when building custom exports or debugging existing ones.

### Plugin Item Structure

The SDK provides each export item with these fields:

```python
item = {
    'id': 12345,                    # assignment ID
    'file': {...},                   # file references (use get_original_file_name())
    'data': {...},                   # annotation data (DM Schema v1 payload)
    'task': {'id': 678, 'tags': [...]},  # task metadata
    'tags': [...],                   # assignment-level tags
    'data_unit': {
        'meta': {...},              # DataUnit.meta (filename, category, group, etc.)
        'files': {
            'video_1': {'path_original': '...'},  # per-spec file paths
        },
    },
}
```

### Annotation Data Structure (Video)

For video-type data, annotations are keyed by spec name:

```python
data['annotations']['video_1']  # list of annotation objects
```

Each annotation object has a `classification` dict:

```python
{
    'classification': {
        'class': 'object_description',    # classification type
        'description_kr': '...',          # annotation content
    }
}
```

### Plugin Output Conventions

- **File naming**: Built from the original file stem + a postfix suffix: `{Path(get_original_file_name(result['files'])).stem}_{postfix}.json`
- **Directory structure**: Output files go into `category`-based subdirectories (using `data_unit_meta['category']` for the subfolder name)
- **One assignment → multiple files**: Plugins iterate over classification types and create a separate output file for each classification present in the annotation. Not every assignment has all types, so file count per assignment varies.

## Format Conversion Reference

### DM Schema v1 → COCO

```python
from synapse_sdk.utils.converters.coco.from_dm import DMtoCOCOConverter

converter = DMtoCOCOConverter()
# Input: DM v1 data dict
# Output: COCO JSON saved to output_dir
converter.convert(dm_v1_data, output_dir='/tmp/coco_output', original_file_dir='/tmp/images')
```

COCO output structure:
```json
{
    "images": [{"id": 1, "file_name": "img.png", "width": 1920, "height": 1080}],
    "annotations": [{"id": 1, "image_id": 1, "category_id": 1, "bbox": [x,y,w,h], "area": 4000, ...}],
    "categories": [{"id": 1, "name": "car"}]
}
```

### DM Schema v1 → YOLO

Manual conversion (no SDK converter yet):

```python
def dm_to_yolo(annotations, image_width, image_height, class_map):
    """Convert DM annotations to YOLO format.

    Args:
        annotations: List of annotation dicts from DM Schema
        image_width: Image width in pixels
        image_height: Image height in pixels
        class_map: {class_name: class_id} mapping

    Returns:
        List of YOLO lines: "class_id x_center y_center width height"
    """
    lines = []
    for ann in annotations:
        if ann.get('type') != 'bbox':
            continue
        x, y, w, h = ann['data']
        class_id = class_map.get(ann['classification'], 0)
        # YOLO uses normalized center coordinates
        x_center = (x + w / 2) / image_width
        y_center = (y + h / 2) / image_height
        norm_w = w / image_width
        norm_h = h / image_height
        lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}")
    return lines
```

### DM Schema v1 → Pascal VOC

Manual conversion:

```python
def dm_to_voc_xml(annotations, image_info, filename):
    """Convert DM annotations to Pascal VOC XML."""
    import xml.etree.ElementTree as ET
    root = ET.Element('annotation')
    ET.SubElement(root, 'filename').text = filename
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(image_info.get('width', 0))
    ET.SubElement(size, 'height').text = str(image_info.get('height', 0))
    ET.SubElement(size, 'depth').text = str(image_info.get('channels', 3))

    for ann in annotations:
        if ann.get('type') != 'bbox':
            continue
        x, y, w, h = ann['data']
        obj = ET.SubElement(root, 'object')
        ET.SubElement(obj, 'name').text = ann['classification']
        bbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(int(x))
        ET.SubElement(bbox, 'ymin').text = str(int(y))
        ET.SubElement(bbox, 'xmax').text = str(int(x + w))
        ET.SubElement(bbox, 'ymax').text = str(int(y + h))

    return ET.tostring(root, encoding='unicode')
```

## SDK Methods Reference

| Method | Purpose |
|--------|---------|
| `client.list_assignments(params, list_all=True)` | Fetch all assignments for a project |
| `client.list_tasks(params, list_all=True)` | Fetch all tasks for a project (expand: data_unit, assignment, workshop) |
| `client.list_ground_truth_events(params, list_all=True)` | Fetch GT events for a dataset version |
| `client.get_project(id)` | Get project details and configuration |
| `client.get_ground_truth_version(id)` | Get GT dataset version details |
| `client.get_storage(id)` | Get storage configuration |
| `client.get_default_storage()` | Get default storage |
| `client.get_data_collection(id)` | Get data collection specs |

## Directory Patterns

### Standard Export Layout

```
export_output/
├── annotations/        # Converted annotation files (JSON/COCO/YOLO/VOC)
│   ├── 001.json
│   ├── 002.json
│   └── ...
├── images/             # Original files (if save_original_file=true)
│   ├── 001.png
│   ├── 002.png
│   └── ...
├── metadata/           # Export metadata
│   └── export_summary.json
└── classes.txt         # Class list (for YOLO/COCO)
```

### COCO Layout

```
coco_export/
├── annotations/
│   ├── instances_train.json    # COCO annotations
│   └── instances_val.json
├── images/
│   ├── train/
│   └── val/
└── classes.json
```

### YOLO Layout

```
yolo_export/
├── images/
│   ├── train/
│   │   ├── 001.png
│   │   └── ...
│   └── val/
├── labels/
│   ├── train/
│   │   ├── 001.txt
│   │   └── ...
│   └── val/
├── data.yaml           # YOLO dataset config
└── classes.txt
```

## Database & Model Reference

These are critical details about the Synapse backend data model, discovered through production usage.

### Django Models & Tables

| Model | Table | Key Fields |
|-------|-------|-----------|
| `DataUnit` (`data_collection.DataUnit`) | `data_collection_dataunit` | `id`, `data_collection_id`, `meta` (JSONField), `files` |
| `Task` (`annotation.Task`) | `annotation_task` | `id`, `project_id` (direct FK — no join needed), `data_unit_id`, `data` (JSONField), `workshop_id` |
| `Workshop` (`hitl.Workshop`) | `hitl_workshop` (NOT `annotation_workshop`) | `id`, `project_id`, `name`, `status` |
| `Assignment` (`hitl.Assignment`) | `hitl_assignment` | `id`, `task_id`, `status_label`, `status_review`, `data` (JSONField — **this is the annotation data**) |
| `AssignmentData` (`hitl.AssignmentData`) | `hitl_assignmentdata` | `id`, `assignment_id`, `file`, `checksum`, `size` — **stores files, NOT annotation JSON** |
| `AssignmentFile` (`hitl.AssignmentFile`) | `hitl_assignmentfile` | File attachments |

### Critical: Where Annotation Data Lives

- **Assignment annotation data** is in `hitl_assignment.data` (a JSONField), NOT in `hitl_assignmentdata`.
- `AssignmentData` is a misleading name — it stores binary file references (file path, checksum, size), not annotation JSON.
- The `data` field on `hitl_assignment` contains the full DM Schema v1 annotation payload.

### Export Rule: Always Export Data Only

When exporting annotation files, **write only the `data` field contents** — do NOT wrap it in metadata (id, task_id, status, etc.). Each exported `.json` file should contain the raw DM Schema v1 annotation payload directly. This keeps exports clean and compatible with downstream tools and converters.

### psycopg2 JSONB Gotcha

When fetching JSONB fields via Django's raw SQL cursor (`connection.cursor()`), psycopg2 returns the value as a **Python string**, not a parsed dict. Always parse it before writing:

```python
data = json.loads(data_str) if isinstance(data_str, str) else data_str
```

### DataUnit Meta Structure

`DataUnit.meta` is a JSONField. A typical example:
```json
{
    "fps": 29.97,
    "group": "B82026Z",
    "ratio": "16:9",
    "width": 1920,
    "height": 1080,
    "bitrate": 15,
    "category": "1. 자연",
    "duration": "00:01:00",
    "filename": "B82026Z_2018_HD_6_0001.mp4",
    "created_at": "2025-11-30T04:21:03.775098",
    "dataset_key": "1. 자연/B82026Z_B82026Z_2018_HD_6_0001",
    "origin_file_stem": "B82026Z_2018_HD_6_0001",
    "origin_file_extension": ".mp4"
}
```

**Identifying data units by filename**: Use `meta->>'filename'` (minus extension) as the reliable identifier, NOT `origin_file_stem`. The `origin_file_stem` field is inconsistent — sometimes it contains the full name (e.g., `B82026Z_2018_HD_6_0001`), other times just a short fragment (e.g., `0003`). To match reliably:

```sql
replace(meta->>'filename', meta->>'origin_file_extension', '') as file_stem
```

**Using `meta.category` for output paths**: When creating category-based directory structures, use the `meta->>'category'` value directly (e.g., `"1. 자연"`, `"2. 도시"`). Do not remap or strip the number prefix — downstream tools and existing exports expect the exact DB value.

**Warning**: Django's JSONField `__in` lookup does NOT work for nested key filtering (e.g., `meta__origin_file_stem__in=[...]` returns 0 results). Use raw SQL instead.

### Project Info

- Project model key for the name field is `title`, not `name` (i.e., `project.get('title')` via API, not `project.get('name')`)
- Task has a **direct `project_id`** foreign key — no need to join through workshop to filter by project

## SDK API Behavior

### Return Types

| Method | `list_all=False` (default) | `list_all=True` |
|--------|---------------------------|-----------------|
| `client.list_assignments()` | `dict` with `count`, `results` | `(generator, count)` tuple |
| `client.list_tasks()` | `dict` with `count`, `results` | `(generator, count)` tuple |
| `client.list_data_units()` | `dict` with `count`, `results` | `(generator, count)` tuple |

The generator yields individual item dicts. Example:
```python
gen, count = client.list_data_units(params={...}, list_all=True)
for du in gen:
    print(du['id'], du.get('meta', {}).get('origin_file_stem'))
```

### Pagination Limits

- **Page size is capped at 100** for data units — the server ignores larger `limit` values
- `list_data_units(page_size=500)` still returns only 100 items per page
- The `search` parameter works on tasks but **does NOT work on data units**
- Task search does NOT match on data unit file names/metadata

### Performance: Paginated API is Slow

For large datasets (100K+ data units), the paginated API is extremely slow:
- 134K data units at 100/page = 1,343 sequential API calls
- Each page takes ~4s from a local client, ~2-4s from Ray
- **Full scan via API: 30-90 minutes**

Always use the export plugin system (`BaseExporter` + `synapse script submit`) for large datasets — the SDK handles pagination internally.

### `synapse script submit` Gotchas

- The command packages the **working directory** as a runtime env for Ray
- **Never submit from `/tmp`** — it may contain files with restricted permissions (e.g., `snap-private-tmp/.gitignore`) that cause `Permission denied` errors
- Always create a clean subdirectory or use the project directory

## Large Dataset Strategies

For projects with 10,000+ data units, **do NOT scan all data units via the API**. Instead:

### Approach 1: Export Plugin (Recommended)

Use the export plugin system. `BaseExporter` receives pre-fetched items via `params['results']` — the SDK handles all pagination internally. Submit via `synapse script submit`.

See the **Export Plugin Architecture** section above for the item structure and output conventions.

### Approach 2: Streaming with `list_all=True` (Small datasets only)

Only use for smaller datasets (< 10K items):
```python
gen, count = client.list_data_units(params={...}, list_all=True)
for du in gen:
    # process item...
```
