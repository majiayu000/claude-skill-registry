---
name: meshy-3d-printing
description: 3D print models generated with Meshy AI. Handles slicer detection, white model printing, multi-color printing via API, and print-optimized download workflows. Use when the user mentions 3D printing, slicing, Bambu, OrcaSlicer, Prusa, Cura, Creality Print, Elegoo, Anycubic, multicolor, multi-color, 3mf, or wants to print a figurine, miniature, or physical model.
license: MIT
compatibility: Requires Python 3 with requests package. Depends on meshy-3d-generation skill. Works with Claude Code, Cursor, and all Agent Skills compatible tools.
metadata:
  author: meshy-dev
  version: "0.3.0"
  homepage: https://github.com/meshy-dev/meshy-3d-agent
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Meshy 3D Printing

Prepare and send Meshy-generated 3D models to a slicer for 3D printing. Supports white model (single-color) and multicolor printing workflows with automatic slicer detection.

**Prerequisite:** This skill reuses the utility functions (`create_task`, `poll_task`, `download`, `get_project_dir`, etc.) and environment setup from `meshy-3d-generation`. However, **when the user wants to 3D print, this skill controls the entire workflow** — including generation, format selection, downloading, and slicer integration. Do NOT run `meshy-3d-generation`'s workflow first and then hand off here — this skill must control parameters from the start (e.g. `target_formats` with `"3mf"` for multicolor).

---

## Intent Detection

Proactively suggest 3D printing when these keywords appear in the user's request:
- **Direct**: print, 3d print, slicer, slice, bambu, orca, prusa, cura, multicolor, multi-color, 3mf
- **Implied**: figurine, miniature, statue, physical model, desk toy, phone stand

When detected, guide the user through the appropriate print pipeline below.

---

## Decision Tree: White Model vs Multicolor

**IMPORTANT**: When the user wants to 3D print, follow this flow:

1. **Detect installed slicers** first (see Slicer Detection Script below)
2. **Ask the user**: "Do you want a single-color (white) print or multicolor?"
3. If **white model** → follow White Model Pipeline
4. If **multicolor**:
   a. Check if a multicolor-capable slicer is installed
   b. Supported multicolor slicers: **OrcaSlicer, Bambu Studio, Creality Print, Elegoo Slicer, Anycubic Slicer Next**
   c. If no multicolor slicer detected, warn the user and suggest installing one
   d. Ask: "How many colors? (default: 4, max: 16)" and "Segmentation depth? (3=coarse, 6=fine, default: 4)"
   e. Confirm cost: generation (20) + texture (10) + multicolor (10) = **40 credits total** (+10 if repair is needed)
   f. Follow Multicolor Pipeline
5. **(Recommended)** Insert a **printability analysis** step (`POST /openapi/v1/print/analyze`, FREE) after generation in either pipeline. Run **`POST /openapi/v1/print/repair`** (10 credits) only if analyze flags errors.

---

## Slicer Detection Script

Append this to the reusable script template from `meshy-3d-generation`:

```python
import subprocess, shutil, platform, os, glob as glob_mod

SLICER_MAP = {
    "OrcaSlicer":           {"mac_app": "OrcaSlicer",          "win_exe": "orca-slicer.exe",         "win_dir": "OrcaSlicer",          "linux_exe": "orca-slicer"},
    "Bambu Studio":         {"mac_app": "BambuStudio",         "win_exe": "bambu-studio.exe",        "win_dir": "BambuStudio",         "linux_exe": "bambu-studio"},
    "Creality Print":       {"mac_app": "Creality Print",      "win_exe": "CrealityPrint.exe",       "win_dir": "Creality Print*",     "linux_exe": None},
    "Elegoo Slicer":        {"mac_app": "ElegooSlicer",        "win_exe": "elegoo-slicer.exe",       "win_dir": "ElegooSlicer",        "linux_exe": None},
    "Anycubic Slicer Next": {"mac_app": "AnycubicSlicerNext",  "win_exe": "AnycubicSlicerNext.exe",  "win_dir": "AnycubicSlicerNext",  "linux_exe": None},
    "PrusaSlicer":          {"mac_app": "PrusaSlicer",         "win_exe": "prusa-slicer.exe",        "win_dir": "PrusaSlicer",         "linux_exe": "prusa-slicer"},
    "UltiMaker Cura":       {"mac_app": "UltiMaker Cura",      "win_exe": "UltiMaker-Cura.exe",     "win_dir": "UltiMaker Cura*",     "linux_exe": None},
}
MULTICOLOR_SLICERS = {"OrcaSlicer", "Bambu Studio", "Creality Print", "Elegoo Slicer", "Anycubic Slicer Next"}

def detect_slicers():
    """Detect installed slicer software. Returns list of {name, path, multicolor}."""
    found = []
    system = platform.system()
    for name, info in SLICER_MAP.items():
        path = None
        if system == "Darwin":
            app = info.get("mac_app")
            if app and os.path.exists(f"/Applications/{app}.app"):
                path = f"/Applications/{app}.app"
        elif system == "Windows":
            win_dir = info.get("win_dir", "")
            win_exe = info.get("win_exe", "")
            for base in [os.environ.get("ProgramFiles", r"C:\Program Files"),
                         os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]:
                if "*" in win_dir:
                    matches = glob_mod.glob(os.path.join(base, win_dir, win_exe))
                    if matches:
                        path = matches[0]
                        break
                else:
                    candidate = os.path.join(base, win_dir, win_exe)
                    if os.path.exists(candidate):
                        path = candidate
                        break
        else:  # Linux
            exe = info.get("linux_exe")
            if exe:
                path = shutil.which(exe)
        if path:
            found.append({"name": name, "path": path, "multicolor": name in MULTICOLOR_SLICERS})
    return found

def open_in_slicer(file_path, slicer_name):
    """Open a model file in the specified slicer."""
    info = SLICER_MAP.get(slicer_name, {})
    system = platform.system()
    abs_path = os.path.abspath(file_path)
    if system == "Darwin":
        app = info.get("mac_app", slicer_name)
        subprocess.run(["open", "-a", app, abs_path])
    elif system == "Windows":
        exe = info.get("win_exe")
        exe_path = shutil.which(exe) if exe else None
        if exe_path:
            subprocess.Popen([exe_path, abs_path])
        else:
            os.startfile(abs_path)
    else:
        exe = info.get("linux_exe")
        exe_path = shutil.which(exe) if exe else None
        if exe_path:
            subprocess.Popen([exe_path, abs_path])
        else:
            subprocess.run(["xdg-open", abs_path])
    print(f"Opened {abs_path} in {slicer_name}")

# --- Detect slicers ---
slicers = detect_slicers()
if slicers:
    print("Installed slicers:")
    for s in slicers:
        mc = " [multicolor]" if s["multicolor"] else ""
        print(f"  - {s['name']}{mc}: {s['path']}")
else:
    print("No slicer software detected. Install one of: OrcaSlicer, Bambu Studio, PrusaSlicer, etc.")
```

---

## Printability Analysis & Repair (FREE → optional 10-credit fix)

Before downloading and printing, run the **automated printability check** to decide whether the mesh needs repair. The analyze step is FREE (0 credits), so there's no reason to skip it for production prints.

### Analyze Script

```python
# Run after the generation/refine/retexture step that produced your printable mesh
INPUT_TASK_ID = refine_id  # or whatever produced the textured / final mesh
# IMPORTANT: input_task_id MUST refer to a task that used Meshy 6 or any Preview model.
# For Meshy 4/5 outputs, pass `model_url` (the GLB download URL) instead.

analyze_id = create_task("/openapi/v1/print/analyze", {
    "input_task_id": INPUT_TASK_ID,
    # OR: "model_url": "https://example.com/model.glb"
})

analyze_task = poll_task("/openapi/v1/print/analyze", analyze_id)

p = analyze_task.get("printability") or {}
metrics = p.get("metrics", {})
status = p.get("status", "unknown")

print(f"Printability: {status} (issues: {p.get('issue_count', 0)} = "
      f"errors {p.get('error_count', 0)} + warnings {p.get('warning_count', 0)})")
print(f"  watertight={metrics.get('is_watertight')}, "
      f"volume={metrics.get('volume')} m³, "
      f"non_manifold_edges={metrics.get('non_manifold_edges')}, "
      f"degenerate_faces={metrics.get('degenerate_faces')}, "
      f"holes={metrics.get('holes')}")

needs_repair = status == "error"  # warning is optional; error means won't print well
```

**Status meanings**:
- `healthy` — print as-is.
- `warning` — degenerate faces or holes present. Repair is OPTIONAL but recommended for thin-feature prints.
- `error` — non-watertight, non-positive volume, or non-manifold edges. **Recommend repair before printing.**
- `unknown` — analyze couldn't process the model. Inspect manually or retry.

### Repair Script (only if analyze flagged errors)

```python
if needs_repair:
    repair_id = create_task("/openapi/v1/print/repair", {
        "input_task_id": INPUT_TASK_ID,    # output is GLB
        # OR: "model_url": "https://example.com/model.stl"   # output is STL
    })
    repair_task = poll_task("/openapi/v1/print/repair", repair_id)

    # Output format mirrors input. Find the populated field:
    repaired_url = next(
        (url for url in repair_task["model_urls"].values() if url),
        None
    )
    # Use this repaired URL for downstream download / multicolor / slicer steps.
```

**Note**: repair preserves geometry only, not textures. If you need a textured + repaired model for multicolor printing, run `repair` first, then re-texture (or feed `repair`'s task_id to `multi-color` directly — the API handles re-texturing internally if applicable).

---

## White Model Print Pipeline

| Step | Action | Credits | Notes |
|------|--------|---------|-------|
| 1 | Detect installed slicers | 0 | Run slicer detection script |
| 2 | Generate untextured model | 5–20 | Text to 3D or Image to 3D (`should_texture: False`) |
| 3 | Download OBJ | 0 | OBJ format for slicer compatibility |
| 4 | Fix OBJ for printing | 0 | Coordinate conversion (see below) |
| 5 | Open in slicer | 0 | `open_in_slicer(obj_path, slicer_name)` |

### White Model Generation + Print Script

Use the `create_task`/`poll_task`/`download`/`get_project_dir` helpers from `meshy-3d-generation`, then:

```python
# --- Step 2: Generate untextured model for printing ---
# Text to 3D:
task_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview",
    "prompt": "USER_PROMPT",
    "ai_model": "latest",
    "target_formats": ["obj"],  # Only OBJ for white model printing
})
# OR Image to 3D:
# task_id = create_task("/openapi/v1/image-to-3d", {
#     "image_url": "IMAGE_URL",
#     "should_texture": False,          # White model — no texture
#     "target_formats": ["glb", "obj"], # OBJ needed for slicer
# })

task = poll_task("/openapi/v2/text-to-3d", task_id)  # adjust endpoint for image-to-3d
project_dir = get_project_dir(task_id, task.get("prompt", "print"))

# --- Step 3-4: Download OBJ + fix for printing ---
obj_url = task["model_urls"].get("obj")
if not obj_url:
    print("OBJ format not available. Available:", list(task["model_urls"].keys()))
    print("Download GLB and import manually into your slicer.")
    obj_url = task["model_urls"].get("glb")

obj_path = os.path.join(project_dir, "model.obj")
download(obj_url, obj_path)

# --- Post-process OBJ for slicer compatibility ---
def fix_obj_for_printing(input_path, output_path=None, target_height_mm=75.0):
    """
    Fix OBJ coordinate system, scale, and position for 3D printing slicers.
    - Rotates from glTF Y-up to slicer Z-up: (x, y, z) -> (x, -z, y)
    - Scales model to target_height_mm (default 75mm)
    - Centers model on XY plane
    - Aligns model bottom to Z=0
    """
    if output_path is None:
        output_path = input_path

    lines = open(input_path, "r").readlines()

    rotated = []
    min_x, max_x = float("inf"), float("-inf")
    min_y, max_y = float("inf"), float("-inf")
    min_z, max_z = float("inf"), float("-inf")
    for line in lines:
        if line.startswith("v "):
            parts = line.split()
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            rx, ry, rz = x, -z, y
            min_x, max_x = min(min_x, rx), max(max_x, rx)
            min_y, max_y = min(min_y, ry), max(max_y, ry)
            min_z, max_z = min(min_z, rz), max(max_z, rz)
            rotated.append(("v", rx, ry, rz, parts[4:]))
        elif line.startswith("vn "):
            parts = line.split()
            nx, ny, nz = float(parts[1]), float(parts[2]), float(parts[3])
            rotated.append(("vn", nx, -nz, ny, []))
        else:
            rotated.append(("line", line))

    model_height = max_z - min_z
    scale = target_height_mm / model_height if model_height > 1e-6 else 1.0
    x_offset = -(min_x + max_x) / 2.0 * scale
    y_offset = -(min_y + max_y) / 2.0 * scale
    z_offset = -(min_z * scale)

    with open(output_path, "w") as f:
        for item in rotated:
            if item[0] == "v":
                _, rx, ry, rz, extra = item
                tx = rx * scale + x_offset
                ty = ry * scale + y_offset
                tz = rz * scale + z_offset
                extra_str = " " + " ".join(extra) if extra else ""
                f.write(f"v {tx:.6f} {ty:.6f} {tz:.6f}{extra_str}\n")
            elif item[0] == "vn":
                _, nx, ny, nz, _ = item
                f.write(f"vn {nx:.6f} {ny:.6f} {nz:.6f}\n")
            else:
                f.write(item[1])

    print(f"OBJ fixed: rotated Y-up→Z-up, scaled to {target_height_mm:.0f}mm, centered, bottom at Z=0")
    print(f"Output: {os.path.abspath(output_path)}")

fix_obj_for_printing(obj_path, target_height_mm=75.0)

# --- Open in slicer ---
if slicers:
    open_in_slicer(obj_path, slicers[0]["name"])
else:
    print(f"\nModel ready: {os.path.abspath(obj_path)}")
    print("Open this file in your preferred slicer: File → Import / Open")
```

> **Parameters:**
> - `target_height_mm`: Default 75mm. Adjust based on user's request (e.g. "print at 15cm" → `150.0`).

---

## Multicolor Print Pipeline

| Step | Action | Credits | Notes |
|------|--------|---------|-------|
| 1 | Detect slicers + check multicolor | 0 | Warn if no multicolor slicer |
| 2 | Generate 3D model | 20 | Text to 3D or Image to 3D |
| 3 | Add textures | 10 | Refine or Retexture (REQUIRED) |
| 4 | Multi-color processing | 10 | POST /openapi/v1/print/multi-color |
| 5 | Poll until SUCCEEDED | 0 | GET /openapi/v1/print/multi-color/{id} |
| 6 | Download 3MF | 0 | From model_urls["3mf"] |
| 7 | Open in multicolor slicer | 0 | `open_in_slicer(path, slicer)` |
| **Total** | | **40** | |

### Multi-Color Full Script

Use the `create_task`/`poll_task`/`download`/`get_project_dir` helpers from `meshy-3d-generation`:

```python
# --- Step 1: Check for multicolor slicer (already done above) ---
mc_slicers = [s for s in slicers if s["multicolor"]]
if not mc_slicers:
    print("WARNING: No multicolor-capable slicer detected.")
    print("Supported: OrcaSlicer, Bambu Studio, Creality Print, Elegoo Slicer, Anycubic Slicer Next")
    print("Install one before proceeding.")
else:
    print(f"Multicolor slicer(s): {', '.join(s['name'] for s in mc_slicers)}")

# --- Step 2-3: Generate + texture (with 3mf in target_formats!) ---
# Text to 3D preview:
preview_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview",
    "prompt": "USER_PROMPT",
    "ai_model": "latest",
    # No target_formats needed — 3MF comes from the multi-color API, not from generate/refine
})
poll_task("/openapi/v2/text-to-3d", preview_id)

# Refine (add textures — REQUIRED for multicolor):
refine_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "refine",
    "preview_task_id": preview_id,
    "enable_pbr": True,
})
refine_task = poll_task("/openapi/v2/text-to-3d", refine_id)
project_dir = get_project_dir(preview_id, "multicolor-print")

# OR for Image to 3D with texture:
# task_id = create_task("/openapi/v1/image-to-3d", {
#     "image_url": "IMAGE_URL",
#     "should_texture": True,
#     # No target_formats needed — 3MF comes from multi-color API
# })
# refine_task = poll_task("/openapi/v1/image-to-3d", task_id)

INPUT_TASK_ID = refine_id  # Use the textured task
MAX_COLORS = 4   # 1-16, ask user
MAX_DEPTH = 4    # 3-6, ask user

mc_task_id = create_task("/openapi/v1/print/multi-color", {
    "input_task_id": INPUT_TASK_ID,
    "max_colors": MAX_COLORS,
    "max_depth": MAX_DEPTH,
})
print(f"Multi-color task created: {mc_task_id} (10 credits)")

task = poll_task("/openapi/v1/print/multi-color", mc_task_id)

# --- Download 3MF ---
threemf_url = task["model_urls"]["3mf"]
threemf_path = os.path.join(project_dir, "multicolor.3mf")
download(threemf_url, threemf_path)
print(f"3MF ready: {os.path.abspath(threemf_path)}")

# --- Open in multicolor slicer ---
if mc_slicers:
    open_in_slicer(threemf_path, mc_slicers[0]["name"])
else:
    print(f"Open {threemf_path} in a multicolor-capable slicer manually.")
```

---

## Manual Sanity Checks (in addition to the automated analyze API)

The analyze API covers geometric correctness (watertight, manifold edges, degenerate faces, holes). Some print-quality concerns still need a human eye in the slicer:

| Check | Recommendation | Where to verify |
|-------|---------------|-----------------|
| Wall thickness | Minimum 1.2mm for FDM, 0.8mm for resin | Slicer (after import) |
| Overhangs | Keep below 45° or add supports | Slicer support generation |
| Minimum detail | At least 0.4mm for FDM, 0.05mm for resin | Visual inspection in slicer |
| Base stability | Flat base or add brim/raft in slicer | Slicer plate adhesion |
| Hollowing | Consider hollowing for figurines/miniatures | Slicer hollow tool (resin) |

The automated analyze API now handles: watertightness, volume, non-manifold edges, degenerate faces, holes — these no longer require manual inspection.

---

## Key Rules for Print Workflow

- **Always detect slicer first** and report results to the user before proceeding
- **Always run analyze (FREE)** for production / functional prints, miniatures with thin features, mechanical parts
- **Repair is conditional**: only when analyze status = error, or warning if the user cares about quality
- **White model**: Download OBJ format, apply `fix_obj_for_printing()` for coordinate conversion
- **Multicolor**: The multi-color API outputs 3MF directly — no coordinate conversion needed (3MF uses Z-up natively)
- **3MF for multicolor**: The Multi-Color Print API outputs 3MF directly — no need to request 3MF from generate/refine via `target_formats`. For non-print use cases that need 3MF, pass `"3mf"` in `target_formats` at generation time.
- **For multicolor, verify slicer supports it** before proceeding with the (costly) pipeline
- After opening in slicer, remind user to check print settings (layer height, infill, supports)
- **If OBJ is not available**: Download GLB and guide user to import manually
- **Repair caveat**: textures are NOT preserved. For a multicolor print on a model that needs repair, run repair first, then re-texture, then multicolor.

---

## Additional Resources

For the complete API endpoint reference, read [reference.md](reference.md).
