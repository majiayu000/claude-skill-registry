---
name: meshy-3d-agent
description: Generate 3D models, textures, images, rig characters, animate them, and prepare for 3D printing using the Meshy AI API. Handles API key detection, task creation, polling, downloading, and full 3D print pipeline with slicer integration. Use when the user asks to create 3D models, convert text/images to 3D, texture models, rig or animate characters, 3D print a model, or interact with the Meshy API.
license: MIT-0
compatibility: Requires Python 3 with requests package. Compatible with OpenClaw and all Agent Skills tools.
metadata:
  openclaw:
    primaryEnv: MESHY_API_KEY
    requires:
      env:
        - MESHY_API_KEY
      bins:
        - python3
        - curl
    install:
      - kind: uv
        package: requests
allowed-tools: Bash, Write
---

# Meshy 3D — Generation + Printing

Directly communicate with the Meshy AI API to generate and print 3D assets. Covers the complete lifecycle: API key setup, task creation, exponential backoff polling, downloading, multi-step pipelines, and 3D print preparation with slicer integration.

---

## SECURITY MANIFEST

**Environment variables accessed:**
- `MESHY_API_KEY` — API authentication token sent in HTTP `Authorization: Bearer` header only. Never logged, never written to any file except `.env` in the current working directory when explicitly requested by the user.

**External network endpoints:**
- `https://api.meshy.ai` — Meshy AI API (task creation, status polling, model/image downloads)

**File system access:**
- Read: `.env` in the current working directory only (API key lookup)
- Write: `.env` in the current working directory only (API key storage, only on user request)
- Write: `./meshy_output/` in the current working directory (downloaded model files, metadata)
- Read: files explicitly provided by the user (e.g., local images passed for image-to-3D conversion), accessed only at the exact path the user specifies
- No access to home directories, shell profiles, or any path outside the above

**Data leaving this machine:**
- API requests to `api.meshy.ai` include the `MESHY_API_KEY` in the Authorization header and user-provided text prompts or image URLs. No other local data is transmitted. Downloaded model files are saved locally only.

---

## IMPORTANT: First-Use Session Notice

When this skill is first activated in a session, inform the user:

> All generated files will be saved to `meshy_output/` in the current working directory. Each project gets its own folder (`{YYYYMMDD_HHmmss}_{prompt}_{id}/`) with model files, textures, thumbnails, and metadata. History is tracked in `meshy_output/history.json`.

This only needs to be said **once per session**.

---

## IMPORTANT: File Organization

All downloaded files MUST go into a structured `meshy_output/` directory in the current working directory. **Do NOT scatter files randomly.**

- Each project: `meshy_output/{YYYYMMDD_HHmmss}_{prompt_slug}_{task_id_prefix}/`
- Chained tasks (preview → refine → rig) reuse the same `project_dir`
- Track tasks in `metadata.json` per project, and global `history.json`
- Auto-download thumbnails alongside models

---

## IMPORTANT: Shell Command Rules

Use only standard POSIX tools. Do NOT use `rg`, `fd`, `bat`, `exa`/`eza`.

---

## IMPORTANT: Run Long Tasks Properly

Meshy generation takes 1–5 minutes. Write the entire create → poll → download flow as **ONE Python script** and execute in a single Bash call. Use `python3 -u script.py` for unbuffered output. Tasks sitting at 99% for 30–120s is normal finalization — do NOT interrupt.

---

## Step 0: API Key Detection (ALWAYS RUN FIRST)

**Only check the current session environment and the `.env` file in the current working directory. Do NOT scan home directories or shell profile files.**

```bash
echo "=== Meshy API Key Detection ==="

# 1. Check current env var
if [ -n "$MESHY_API_KEY" ]; then
  echo "ENV_VAR: FOUND (${MESHY_API_KEY:0:8}...)"
else
  echo "ENV_VAR: NOT_FOUND"
fi

# 2. Check .env in current working directory only
if [ -f ".env" ] && grep -q "MESHY_API_KEY" ".env" 2>/dev/null; then
  echo "DOTENV(.env): FOUND"
  export MESHY_API_KEY=$(grep "^MESHY_API_KEY=" ".env" | head -1 | cut -d'=' -f2- | tr -d '"'"'" )
fi

# 3. Final status
if [ -n "$MESHY_API_KEY" ]; then
  echo "READY: key=${MESHY_API_KEY:0:8}..."
else
  echo "READY: NO_KEY_FOUND"
fi

# 4. Python requests check
python3 -c "import requests; print('PYTHON_REQUESTS: OK')" 2>/dev/null || echo "PYTHON_REQUESTS: MISSING (run: pip install requests)"

echo "=== Detection Complete ==="
```

### Decision After Detection

- **Key found** → Proceed to Step 1.
- **Key NOT found** → Go to Step 0a.
- **Python requests missing** → Run `pip install requests`.

---

## Step 0a: API Key Setup (Only If No Key Found)

Tell the user:

> To use the Meshy API, you need an API key:
>
> 1. Go to **https://www.meshy.ai/settings/api**
> 2. Click **"Create API Key"**, name it, and copy the key (starts with `msy_`)
> 3. The key is shown **only once** — save it somewhere safe
>
> **Note:** API access requires a **Pro plan or above**. Free-tier accounts cannot create API keys.

Once the user provides the key, set it for the current session and optionally persist to `.env`:

```bash
# Set for current session only
export MESHY_API_KEY="msy_PASTE_KEY_HERE"

# Verify the key
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $MESHY_API_KEY" \
  https://api.meshy.ai/openapi/v1/balance)

if [ "$STATUS" = "200" ]; then
  BALANCE=$(curl -s -H "Authorization: Bearer $MESHY_API_KEY" https://api.meshy.ai/openapi/v1/balance)
  echo "Key valid. $BALANCE"
else
  echo "Key invalid (HTTP $STATUS). Please check the key and try again."
fi
```

**To persist the key (current project only):**

```bash
# Write to .env in current working directory
echo 'MESHY_API_KEY=msy_PASTE_KEY_HERE' >> .env
echo "Saved to .env"

# IMPORTANT: add .env to .gitignore to avoid leaking the key
grep -q "^\.env" .gitignore 2>/dev/null || echo ".env" >> .gitignore
echo ".env added to .gitignore"
```

> **Security reminder:** The key is stored only in `.env` in your current project directory. Never commit this file to version control. `.env` has been automatically added to `.gitignore`.

---

## Step 1: Confirm Plan With User Before Spending Credits

**CRITICAL**: Before creating any task, present the user with a cost summary and wait for confirmation:

```
I'll generate a 3D model of "<prompt>" using the following plan:

  1. Preview (mesh generation) — 20 credits
  2. Refine (texturing with PBR) — 10 credits
  3. Download as .glb

  Total cost: 30 credits
  Current balance: <N> credits

  Shall I proceed?
```

For multi-step pipelines (text-to-3d → rig → animate), show the FULL pipeline cost upfront.

> **Note:** Rigging automatically includes walking + running animations at no extra cost. Only add `Animate` (3 credits) for custom animations beyond those.

### Intent → API Mapping

| User wants to... | API | Endpoint | Credits |
|---|---|---|---|
| 3D model from text | Text to 3D | `POST /openapi/v2/text-to-3d` | 5–20 (preview) + 10 (refine) |
| 3D model from one image | Image to 3D | `POST /openapi/v1/image-to-3d` | 5–30 |
| 3D model from multiple images | Multi-Image to 3D | `POST /openapi/v1/multi-image-to-3d` | 5–30 |
| New textures on existing model | Retexture | `POST /openapi/v1/retexture` | 10 |
| Change mesh format/topology | Remesh | `POST /openapi/v1/remesh` | 5 |
| Add skeleton to character | Auto-Rigging | `POST /openapi/v1/rigging` | 5 |
| Animate a rigged character | Animation | `POST /openapi/v1/animations` | 3 |
| 2D image from text | Text to Image | `POST /openapi/v1/text-to-image` | 3–9 |
| Transform a 2D image | Image to Image | `POST /openapi/v1/image-to-image` | 3–9 |
| Check credit balance | Balance | `GET /openapi/v1/balance` | 0 |
| 3D print a model (white) | → See Print Pipeline section | — | 20 |
| Multi-color 3D print | Multi-Color Print | `POST /openapi/v1/print/multi-color` | 10 (+ generation) |

---

## Step 2: Execute the Workflow

### Reusable Script Template

Use this as the base for ALL workflows. It loads the API key securely from environment or `.env` in the current directory only:

```python
#!/usr/bin/env python3
"""Meshy API task runner. Handles create → poll → download."""
import requests, time, os, sys, re, json
from datetime import datetime

# --- Secure API key loading ---
def load_api_key():
    """Load MESHY_API_KEY from environment, then .env in cwd only."""
    key = os.environ.get("MESHY_API_KEY", "").strip()
    if key:
        return key
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("MESHY_API_KEY=") and not line.startswith("#"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    return ""

API_KEY = load_api_key()
if not API_KEY:
    sys.exit("ERROR: MESHY_API_KEY not set. Run Step 0a to configure it.")

# Never log the full key — only first 8 chars for traceability
print(f"API key loaded: {API_KEY[:8]}...")

BASE = "https://api.meshy.ai"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SESSION = requests.Session()
SESSION.trust_env = False  # bypass any system proxy settings

def create_task(endpoint, payload):
    resp = SESSION.post(f"{BASE}{endpoint}", headers=HEADERS, json=payload, timeout=30)
    if resp.status_code == 401:
        sys.exit("ERROR: Invalid API key (401). Re-run Step 0a.")
    if resp.status_code == 402:
        try:
            bal = SESSION.get(f"{BASE}/openapi/v1/balance", headers=HEADERS, timeout=10)
            balance = bal.json().get("balance", "unknown")
            sys.exit(f"ERROR: Insufficient credits (402). Balance: {balance}. Top up at https://www.meshy.ai/pricing")
        except Exception:
            sys.exit("ERROR: Insufficient credits (402). Check balance at https://www.meshy.ai/pricing")
    if resp.status_code == 429:
        sys.exit("ERROR: Rate limited (429). Wait and retry.")
    resp.raise_for_status()
    task_id = resp.json()["result"]
    print(f"TASK_CREATED: {task_id}")
    return task_id

def poll_task(endpoint, task_id, timeout=300):
    """Poll with exponential backoff (5s→30s, fixed 15s at 95%+)."""
    elapsed, delay, max_delay, backoff, finalize_delay, poll_count = 0, 5, 30, 1.5, 15, 0
    while elapsed < timeout:
        poll_count += 1
        resp = SESSION.get(f"{BASE}{endpoint}/{task_id}", headers=HEADERS, timeout=30)
        resp.raise_for_status()
        task = resp.json()
        status = task["status"]
        progress = task.get("progress", 0)
        bar = f"[{'█' * int(progress/5)}{'░' * (20 - int(progress/5))}] {progress}%"
        print(f"  {bar} — {status} ({elapsed}s, poll #{poll_count})", flush=True)
        if status == "SUCCEEDED":
            return task
        if status in ("FAILED", "CANCELED"):
            msg = task.get("task_error", {}).get("message", "Unknown")
            sys.exit(f"TASK_{status}: {msg}")
        current_delay = finalize_delay if progress >= 95 else delay
        time.sleep(current_delay)
        elapsed += current_delay
        if progress < 95:
            delay = min(delay * backoff, max_delay)
    sys.exit(f"TIMEOUT after {timeout}s ({poll_count} polls)")

def download(url, filepath):
    """Download a file into a project directory (within cwd/meshy_output/)."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    print(f"Downloading {filepath}...", flush=True)
    resp = SESSION.get(url, timeout=300, stream=True)
    resp.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"DOWNLOADED: {filepath} ({os.path.getsize(filepath)/1024/1024:.1f} MB)")

# --- File organization helpers ---
OUTPUT_ROOT = os.path.join(os.getcwd(), "meshy_output")
os.makedirs(OUTPUT_ROOT, exist_ok=True)
HISTORY_FILE = os.path.join(OUTPUT_ROOT, "history.json")

def get_project_dir(task_id, prompt="", task_type="model"):
    slug = re.sub(r'[^a-z0-9]+', '-', (prompt or task_type).lower())[:30].strip('-')
    folder = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{slug}_{task_id[:8]}"
    project_dir = os.path.join(OUTPUT_ROOT, folder)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir

def record_task(project_dir, task_id, task_type, stage, prompt="", files=None):
    meta_path = os.path.join(project_dir, "metadata.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {
        "project_name": prompt or task_type, "folder": os.path.basename(project_dir),
        "root_task_id": task_id, "created_at": datetime.now().isoformat(), "tasks": []
    }
    meta["tasks"].append({"task_id": task_id, "task_type": task_type, "stage": stage,
                          "files": files or [], "created_at": datetime.now().isoformat()})
    meta["updated_at"] = datetime.now().isoformat()
    json.dump(meta, open(meta_path, "w"), indent=2)
    history = json.load(open(HISTORY_FILE)) if os.path.exists(HISTORY_FILE) else {"version": 1, "projects": []}
    folder = os.path.basename(project_dir)
    entry = next((p for p in history["projects"] if p["folder"] == folder), None)
    if entry:
        entry.update({"task_count": len(meta["tasks"]), "updated_at": meta["updated_at"]})
    else:
        history["projects"].append({"folder": folder, "prompt": prompt, "task_type": task_type,
            "root_task_id": task_id, "created_at": meta["created_at"],
            "updated_at": meta["updated_at"], "task_count": len(meta["tasks"])})
    json.dump(history, open(HISTORY_FILE, "w"), indent=2)

def save_thumbnail(project_dir, url):
    path = os.path.join(project_dir, "thumbnail.png")
    if os.path.exists(path): return
    try:
        r = SESSION.get(url, timeout=15); r.raise_for_status()
        open(path, "wb").write(r.content)
    except Exception: pass
```

---

### Text to 3D (Preview + Refine)

Append to the template above:

```python
PROMPT = "USER_PROMPT"

# Preview
preview_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview",
    "prompt": PROMPT,
    "ai_model": "latest",
    # "pose_mode": "t-pose",   # Use "t-pose" if rigging/animating later
})
task = poll_task("/openapi/v2/text-to-3d", preview_id)
project_dir = get_project_dir(preview_id, prompt=PROMPT)
download(task["model_urls"]["glb"], os.path.join(project_dir, "preview.glb"))
record_task(project_dir, preview_id, "text-to-3d", "preview", prompt=PROMPT, files=["preview.glb"])
if task.get("thumbnail_url"):
    save_thumbnail(project_dir, task["thumbnail_url"])
print(f"\nPREVIEW COMPLETE — Task: {preview_id} | Project: {project_dir}")

# Refine
refine_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "refine",
    "preview_task_id": preview_id,
    "enable_pbr": True,
    "ai_model": "latest",
})
task = poll_task("/openapi/v2/text-to-3d", refine_id)
download(task["model_urls"]["glb"], os.path.join(project_dir, "refined.glb"))
record_task(project_dir, refine_id, "text-to-3d", "refined", prompt=PROMPT, files=["refined.glb"])
print(f"\nREFINE COMPLETE — Task: {refine_id} | Formats: {', '.join(task['model_urls'].keys())}")
```

> **Note:** All models (meshy-5, meshy-6, latest) support both preview and refine. The preview and refine ai_model should match to avoid 400 errors.

---

### Image to 3D

```python
import base64

# For local files: convert to data URI
# with open("photo.jpg", "rb") as f:
#     image_url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

task_id = create_task("/openapi/v1/image-to-3d", {
    "image_url": "IMAGE_URL_OR_DATA_URI",
    "should_texture": True,
    "enable_pbr": True,
    "ai_model": "latest",
})
task = poll_task("/openapi/v1/image-to-3d", task_id)
project_dir = get_project_dir(task_id, task_type="image-to-3d")
download(task["model_urls"]["glb"], os.path.join(project_dir, "model.glb"))
record_task(project_dir, task_id, "image-to-3d", "complete", files=["model.glb"])
```

---

### Multi-Image to 3D

```python
task_id = create_task("/openapi/v1/multi-image-to-3d", {
    "image_urls": ["URL_1", "URL_2", "URL_3"],  # 1–4 images
    "should_texture": True,
    "enable_pbr": True,
    "ai_model": "latest",
})
task = poll_task("/openapi/v1/multi-image-to-3d", task_id)
project_dir = get_project_dir(task_id, task_type="multi-image-to-3d")
download(task["model_urls"]["glb"], os.path.join(project_dir, "model.glb"))
```

---

### Retexture

**IMPORTANT**: Ask user for texture style first — `text_style_prompt` OR `image_style_url` (one required, image takes precedence if both given).

```python
# REQUIRED: ask user for text_style_prompt OR image_style_url
task_id = create_task("/openapi/v1/retexture", {
    "input_task_id": "PREVIOUS_TASK_ID",
    "text_style_prompt": "wooden texture",     # REQUIRED if no image_style_url
    # "image_style_url": "URL",               # REQUIRED if no prompt (takes precedence)
    "enable_pbr": True,
    # "target_formats": ["glb", "3mf"],  # 3mf must be explicitly requested
})
task = poll_task("/openapi/v1/retexture", task_id)
project_dir = get_project_dir(task_id, task_type="retexture")
download(task["model_urls"]["glb"], os.path.join(project_dir, "retextured.glb"))
```

---

### Remesh / Format Conversion

```python
task_id = create_task("/openapi/v1/remesh", {
    "input_task_id": "TASK_ID",
    "target_formats": ["glb", "fbx", "obj"],
    "topology": "quad",
    "target_polycount": 10000,
})
task = poll_task("/openapi/v1/remesh", task_id)
project_dir = get_project_dir(task_id, task_type="remesh")
for fmt, url in task["model_urls"].items():
    download(url, os.path.join(project_dir, f"remeshed.{fmt}"))
```

---

### Auto-Rigging + Animation

**When the user asks to rig or animate, the generation step MUST use `pose_mode: "t-pose"`.**

```python
# Pre-rig check: polycount must be ≤ 300,000
source_endpoint = "/openapi/v2/text-to-3d"  # adjust to match source task endpoint
source_task_id = "TASK_ID"
check = SESSION.get(f"{BASE}{source_endpoint}/{source_task_id}", headers=HEADERS, timeout=30)
check.raise_for_status()
face_count = check.json().get("face_count", 0)
if face_count > 300000:
    sys.exit(f"ERROR: {face_count:,} faces exceeds 300,000 limit. Remesh first.")

# Rig
rig_id = create_task("/openapi/v1/rigging", {
    "input_task_id": source_task_id,
    "height_meters": 1.7,
})
rig_task = poll_task("/openapi/v1/rigging", rig_id)
project_dir = get_project_dir(rig_id, task_type="rigging")
download(rig_task["result"]["rigged_character_glb_url"], os.path.join(project_dir, "rigged.glb"))
download(rig_task["result"]["basic_animations"]["walking_glb_url"], os.path.join(project_dir, "walking.glb"))
download(rig_task["result"]["basic_animations"]["running_glb_url"], os.path.join(project_dir, "running.glb"))

# Custom animation (optional, 3 credits — only if user needs beyond walking/running)
# anim_id = create_task("/openapi/v1/animations", {"rig_task_id": rig_id, "action_id": 1})
# anim_task = poll_task("/openapi/v1/animations", anim_id)
# download(anim_task["result"]["animation_glb_url"], os.path.join(project_dir, "animated.glb"))
```

---

### Text to Image / Image to Image

```python
# Text to Image
task_id = create_task("/openapi/v1/text-to-image", {
    "ai_model": "nano-banana-pro",
    "prompt": "a futuristic spaceship",
})
task = poll_task("/openapi/v1/text-to-image", task_id)
# Result URL: task["image_url"]

# Image to Image
task_id = create_task("/openapi/v1/image-to-image", {
    "ai_model": "nano-banana-pro",
    "prompt": "make it look cyberpunk",
    "reference_image_urls": ["URL"],
})
task = poll_task("/openapi/v1/image-to-image", task_id)
```

---

## 3D Printing Workflow

**IMPORTANT: When the user's request involves 3D printing, use this section for the ENTIRE workflow — including model generation.** Do NOT run the generation workflows above and then come here. This section controls `target_formats` and other print-specific parameters from the start.

Trigger when the user mentions: print, 3d print, slicer, slice, bambu, orca, prusa, cura, multicolor, multi-color, 3mf, figurine, miniature, statue, physical model, desk toy, phone stand.

### Decision: White Model vs Multicolor

1. **Detect installed slicers** first (see script below)
2. Ask the user: "White model (single-color) or multicolor?"
3. If **multicolor**: check for multicolor-capable slicer (OrcaSlicer, Bambu Studio, Creality Print, Elegoo Slicer, Anycubic Slicer Next), ask max_colors (1-16, default 4) and max_depth (3-6, default 4), confirm cost: 40 credits

### Slicer Detection + Opening

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
    found = []
    system = platform.system()
    for name, info in SLICER_MAP.items():
        path = None
        if system == "Darwin":
            app = info.get("mac_app")
            if app and os.path.exists(f"/Applications/{app}.app"):
                path = f"/Applications/{app}.app"
        elif system == "Windows":
            win_dir, win_exe = info.get("win_dir", ""), info.get("win_exe", "")
            for base in [os.environ.get("ProgramFiles", r"C:\Program Files"),
                         os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]:
                if "*" in win_dir:
                    matches = glob_mod.glob(os.path.join(base, win_dir, win_exe))
                    if matches: path = matches[0]; break
                else:
                    candidate = os.path.join(base, win_dir, win_exe)
                    if os.path.exists(candidate): path = candidate; break
        else:
            exe = info.get("linux_exe")
            if exe: path = shutil.which(exe)
        if path:
            found.append({"name": name, "path": path, "multicolor": name in MULTICOLOR_SLICERS})
    return found

def open_in_slicer(file_path, slicer_name):
    info = SLICER_MAP.get(slicer_name, {})
    system, abs_path = platform.system(), os.path.abspath(file_path)
    if system == "Darwin":
        subprocess.run(["open", "-a", info.get("mac_app", slicer_name), abs_path])
    elif system == "Windows":
        exe_path = shutil.which(info.get("win_exe", ""))
        (subprocess.Popen([exe_path, abs_path]) if exe_path else os.startfile(abs_path))
    else:
        exe_path = shutil.which(info.get("linux_exe", ""))
        (subprocess.Popen([exe_path, abs_path]) if exe_path else subprocess.run(["xdg-open", abs_path]))
    print(f"Opened {abs_path} in {slicer_name}")

slicers = detect_slicers()
for s in slicers:
    mc = " [multicolor]" if s["multicolor"] else ""
    print(f"  - {s['name']}{mc}: {s['path']}")
```

### White Model Pipeline

| Step | Action | Credits |
|------|--------|---------|
| 1 | Generate untextured model | 20 |
| 2 | Download OBJ | 0 |
| 3 | Fix OBJ (`fix_obj_for_printing`) | 0 |
| 4 | Open in slicer | 0 |

Generate with `target_formats` including `"obj"`, then fix for printing:

```python
# --- Generate for white model printing ---
# Text to 3D:
task_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview", "prompt": "USER_PROMPT", "ai_model": "latest",
    "target_formats": ["obj"],  # Only OBJ for white model printing
})
# OR Image to 3D:
# task_id = create_task("/openapi/v1/image-to-3d", {
#     "image_url": "URL", "should_texture": False,
#     "target_formats": ["glb", "obj"],
# })
task = poll_task("/openapi/v2/text-to-3d", task_id)
project_dir = get_project_dir(task_id, "print")

obj_url = task["model_urls"].get("obj") or task["model_urls"].get("glb")
obj_path = os.path.join(project_dir, "model.obj")
download(obj_url, obj_path)

def fix_obj_for_printing(input_path, output_path=None, target_height_mm=75.0):
    if output_path is None: output_path = input_path
    lines = open(input_path, "r").readlines()
    rotated, min_x, max_x, min_y, max_y, min_z, max_z = [], float("inf"), float("-inf"), float("inf"), float("-inf"), float("inf"), float("-inf")
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
            rotated.append(("vn", float(parts[1]), -float(parts[3]), float(parts[2]), []))
        else:
            rotated.append(("line", line))
    h = max_z - min_z
    s = target_height_mm / h if h > 1e-6 else 1.0
    xo, yo, zo = -(min_x+max_x)/2*s, -(min_y+max_y)/2*s, -(min_z*s)
    with open(output_path, "w") as f:
        for item in rotated:
            if item[0] == "v":
                _, rx, ry, rz, extra = item
                e = " "+" ".join(extra) if extra else ""
                f.write(f"v {rx*s+xo:.6f} {ry*s+yo:.6f} {rz*s+zo:.6f}{e}\n")
            elif item[0] == "vn":
                f.write(f"vn {item[1]:.6f} {item[2]:.6f} {item[3]:.6f}\n")
            else:
                f.write(item[1])
    print(f"OBJ fixed: scaled to {target_height_mm:.0f}mm, Z-up, centered")

fix_obj_for_printing(obj_path, target_height_mm=75.0)
if slicers: open_in_slicer(obj_path, slicers[0]["name"])
```

### Multicolor Pipeline

| Step | Action | Credits |
|------|--------|---------|
| 1 | Generate + texture | 30 |
| 2 | Multi-color processing | 10 |
| 3 | Download 3MF | 0 |
| 4 | Open in multicolor slicer | 0 |

```python
mc_slicers = [s for s in slicers if s["multicolor"]]
if not mc_slicers:
    print("WARNING: No multicolor slicer detected. Install: OrcaSlicer, Bambu Studio, etc.")

# --- Generate + texture with target_formats including 3mf ---
preview_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview", "prompt": "USER_PROMPT", "ai_model": "latest",
    # No target_formats needed — 3MF comes from multi-color API
})
poll_task("/openapi/v2/text-to-3d", preview_id)

refine_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "refine", "preview_task_id": preview_id, "enable_pbr": True,
})
poll_task("/openapi/v2/text-to-3d", refine_id)
project_dir = get_project_dir(preview_id, "multicolor-print")

# --- Multi-color processing ---
mc_task_id = create_task("/openapi/v1/print/multi-color", {
    "input_task_id": refine_id,
    "max_colors": 4,   # 1-16, ask user
    "max_depth": 4,     # 3-6, ask user
})
task = poll_task("/openapi/v1/print/multi-color", mc_task_id)
threemf_path = os.path.join(project_dir, "multicolor.3mf")
download(task["model_urls"]["3mf"], threemf_path)
if mc_slicers: open_in_slicer(threemf_path, mc_slicers[0]["name"])
```

### Printability Checklist

| Check | Recommendation |
|-------|---------------|
| Wall thickness | Min 1.2mm FDM, 0.8mm resin |
| Overhangs | Keep below 45° or add supports |
| Manifold mesh | Watertight, no holes |
| Minimum detail | 0.4mm FDM, 0.05mm resin |
| Base stability | Flat base or add brim/raft in slicer |
| Floating parts | All parts connected or printed separately |

---

## Step 3: Report Results

After task succeeds:
1. Downloaded file paths and sizes
2. Task IDs (for follow-up: refine, rig, retexture)
3. Available formats (list `model_urls` keys)
4. Credits consumed + current balance
5. Suggested next steps:
   - Preview done → "Want to refine (add textures)?"
   - Model done → "Want to rig this character?"
   - Rigged → "Want to apply a custom animation?"
   - Any textured model → "Want to 3D print this? Multicolor printing is available!"
   - Any model → "Want to 3D print this?"

---

## Error Recovery

| HTTP Status | Meaning | Action |
|---|---|---|
| 401 | Invalid API key | Re-run Step 0; ask user to check key |
| 402 | Insufficient credits | Show balance, link https://www.meshy.ai/pricing |
| 422 | Cannot process | Explain (e.g., non-humanoid for rigging) |
| 429 | Rate limited | Auto-retry after 5s (max 3 times) |
| 5xx | Server error | Auto-retry after 10s (once) |

Task `FAILED` messages:
- `"The server is busy..."` → retry with backoff (5s, 10s, 20s)
- `"Internal server error."` → simplify prompt, retry once

---

## Known Behaviors & Constraints

- **99% stall**: Normal finalization (30–120s). Do NOT interrupt.
- **Asset retention**: Files deleted after **3 days** (non-Enterprise). Download immediately.
- **PBR maps**: Must set `enable_pbr: true` explicitly.
- **Refine**: All models support both preview and refine. Preview and refine ai_model should match.
- **Rigging**: Humanoid bipedal only, polycount ≤ 300,000.
- **Printing formats**: White model → OBJ with `fix_obj_for_printing()`. Multicolor → 3MF from Multi-Color Print API. Always detect slicer first.
- **Download format**: Ask the user which format they need before downloading. GLB (viewing), OBJ (printing), 3MF (multicolor), FBX (games), USDZ (AR). Do NOT download all formats.
- **3MF for multicolor**: Multi-Color Print API outputs 3MF directly — no need to request 3MF from generate/refine. For non-print use cases needing 3MF, pass `"3mf"` in `target_formats`.
- **Timestamps**: All API timestamps are Unix epoch **milliseconds**.

---

## Execution Checklist

- [ ] Ran API key detection (Step 0) — checked env var and `.env` only
- [ ] API key verified (never printed in full)
- [ ] Presented cost summary and got user confirmation
- [ ] Wrote complete workflow as single Python script
- [ ] Ran with `python3 -u` for unbuffered output
- [ ] Reported file paths, formats, task IDs, and balance
- [ ] Suggested next steps

---

## Additional Resources

For the complete API endpoint reference including all parameters, response schemas, and error codes, read [reference.md](reference.md).
