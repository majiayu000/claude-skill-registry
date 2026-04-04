---
name: meshy-3d-generation
description: Generate 3D models, textures, images, rig characters, and animate them using the Meshy AI API. Handles API key detection, setup, and all generation workflows via direct HTTP calls. Use when the user asks to create 3D models, convert text/images to 3D, texture models, rig or animate characters, or interact with the Meshy API.
license: MIT
compatibility: Requires Python 3 with requests package. Works with Claude Code, Cursor, and all Agent Skills compatible tools.
metadata:
  author: meshy-dev
  version: "1.0.0"
  homepage: https://github.com/meshy-dev/meshy-3d-agent
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Meshy 3D Generation

Directly communicate with the Meshy AI API to generate 3D assets. This skill handles the complete lifecycle: environment setup, API key detection, task creation, polling, downloading, and chaining multi-step pipelines.

For full endpoint reference (all parameters, response schemas, error codes), read [reference.md](reference.md).

---

## IMPORTANT: 3D Printing → Use `meshy-3d-printing` Skill

**If the user's request involves 3D printing** (keywords: print, 3d print, slicer, slice, bambu, orca, prusa, cura, multicolor, 3mf, figurine, miniature, statue, physical model), **use the `meshy-3d-printing` skill instead of this one for the entire workflow.** The printing skill handles generation with correct print-optimized parameters (e.g. `target_formats` with `"3mf"` for multicolor), slicer detection, coordinate conversion, and slicer launch — all in one pipeline.

This skill's `create_task`/`poll_task`/`download` template functions are reused by the printing skill, but the **workflow orchestration** (what to generate, which formats, what to do after) must come from the printing skill when printing is involved.

**Do NOT generate a model with this skill and then hand off to the printing skill** — the printing skill needs to control parameters from the start (e.g. `target_formats`, `should_texture`).

---

## IMPORTANT: First-Use Session Notice

When this skill is first activated in a session, inform the user:

> All generated files will be saved to `meshy_output/` in the current working directory. Each project gets its own folder (`{YYYYMMDD_HHmmss}_{prompt}_{id}/`) with model files, textures, thumbnails, and metadata. History is tracked in `meshy_output/history.json`.

This only needs to be said **once per session**, at the beginning.

## IMPORTANT: File Organization

All downloaded files MUST go into a structured `meshy_output/` directory in the current working directory. **Do NOT scatter files randomly.**

- Each project gets its own folder: `meshy_output/{YYYYMMDD_HHmmss}_{prompt_slug}_{task_id_prefix}/`
- For chained tasks (preview → refine → rig), reuse the same `project_dir`
- Track tasks in `metadata.json` per project, and global `history.json`
- Auto-download thumbnails alongside models

The Reusable Script Template below includes `get_project_dir()`, `record_task()`, and `save_thumbnail()` helpers.

---

## IMPORTANT: Shell Command Rules

**Use only standard POSIX tools in shell commands.** Do NOT use `rg` (ripgrep), `fd`, or other non-standard CLI tools — they may not be installed. Use these standard alternatives instead:

| Do NOT use | Use instead |
|---|---|
| `rg` | `grep` |
| `fd` | `find` |
| `bat` | `cat` |
| `exa` / `eza` | `ls` |

---

## IMPORTANT: Run Long Tasks Properly

Meshy generation tasks take 1–5 minutes. When running Python scripts that poll for completion:

- Write the entire create → poll → download flow as **ONE Python script** and execute it in a single Bash call. Do NOT split into multiple commands. This keeps the API key, task IDs, and session in one process context.
- Use `python3 -u script.py` (unbuffered) so progress output is visible in real time.
- Be patient with long-running scripts — do NOT interrupt or kill them prematurely. Tasks at 99% for 30–120s is normal finalization, not a failure.

---

## Step 0: Environment Detection (ALWAYS RUN FIRST)

Before any API call, detect whether the environment is ready:

```bash
echo "=== Meshy API Key Detection ==="

# 1. Check current env var
if [ -n "$MESHY_API_KEY" ]; then
  echo "ENV_VAR: FOUND (${MESHY_API_KEY:0:8}...)"
else
  echo "ENV_VAR: NOT_FOUND"
fi

# 2. Check .env files in workspace
for f in .env .env.local; do
  if [ -f "$f" ] && grep -q "MESHY_API_KEY" "$f" 2>/dev/null; then
    echo "DOTENV($f): FOUND"
    export $(grep "MESHY_API_KEY" "$f" | head -1)
  fi
done

# 3. Check shell profiles
for f in ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile; do
  if [ -f "$f" ] && grep -q "MESHY_API_KEY" "$f" 2>/dev/null; then
    echo "SHELL_PROFILE: FOUND in $f"
  fi
done

# 4. Final status
if [ -n "$MESHY_API_KEY" ]; then
  echo "READY: key=${MESHY_API_KEY:0:12}..."
else
  echo "READY: NO_KEY_FOUND"
fi

# 5. Python requests check
python3 -c "import requests; print('PYTHON_REQUESTS: OK')" 2>/dev/null || echo "PYTHON_REQUESTS: MISSING (run: pip install requests)"

echo "=== Detection Complete ==="
```

### Decision After Detection

- **Key found** → Proceed to Step 1.
- **Key NOT found** → Go to Step 0a.
- **Python requests missing** → Run `pip install requests`.

## Step 0a: API Key Setup (Only If No Key Found)

Tell the user:

> To use the Meshy API, you need an API key. Here's how to get one:
>
> 1. Go to **https://www.meshy.ai/settings/api**
> 2. Click **"Create API Key"**, give it a name, and copy the key (it starts with `msy_`)
> 3. The key is only shown once — save it somewhere safe
>
> **Note:** API access requires a **Pro plan or above**. Free-tier accounts cannot create API keys. If you see "Please upgrade to a premium plan to create API tasks", you'll need to upgrade at https://www.meshy.ai/pricing first.

Once the user provides their key, set it and verify:

**macOS (zsh):**
```bash
export MESHY_API_KEY="msy_PASTE_KEY_HERE"

# Verify
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $MESHY_API_KEY" \
  https://api.meshy.ai/openapi/v1/balance)

if [ "$STATUS" = "200" ]; then
  BALANCE=$(curl -s -H "Authorization: Bearer $MESHY_API_KEY" https://api.meshy.ai/openapi/v1/balance)
  echo "Key valid. $BALANCE"
  echo 'export MESHY_API_KEY="msy_PASTE_KEY_HERE"' >> ~/.zshrc
  echo "Persisted to ~/.zshrc"
else
  echo "Key invalid (HTTP $STATUS). Check the key and try again."
fi
```

**Linux (bash):**
```bash
export MESHY_API_KEY="msy_PASTE_KEY_HERE"

# Verify (same as above), then persist to ~/.bashrc
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $MESHY_API_KEY" \
  https://api.meshy.ai/openapi/v1/balance)

if [ "$STATUS" = "200" ]; then
  BALANCE=$(curl -s -H "Authorization: Bearer $MESHY_API_KEY" https://api.meshy.ai/openapi/v1/balance)
  echo "Key valid. $BALANCE"
  echo 'export MESHY_API_KEY="msy_PASTE_KEY_HERE"' >> ~/.bashrc
  echo "Persisted to ~/.bashrc"
else
  echo "Key invalid (HTTP $STATUS). Check the key and try again."
fi
```

**Windows (PowerShell):**
```powershell
$env:MESHY_API_KEY = "msy_PASTE_KEY_HERE"

# Verify
$status = (Invoke-WebRequest -Uri "https://api.meshy.ai/openapi/v1/balance" -Headers @{Authorization="Bearer $env:MESHY_API_KEY"} -UseBasicParsing).StatusCode
if ($status -eq 200) {
    Write-Host "Key valid."
    # Persist permanently
    [System.Environment]::SetEnvironmentVariable("MESHY_API_KEY", $env:MESHY_API_KEY, "User")
    Write-Host "Persisted to user environment variables. Restart terminal to take effect."
} else {
    Write-Host "Key invalid (HTTP $status). Check the key and try again."
}
```

**Alternative (all platforms):** Create a `.env` file in your project root:
```
MESHY_API_KEY=msy_PASTE_KEY_HERE
```

---

## Step 1: Confirm Plan With User Before Spending Credits

**CRITICAL**: Before creating any task, present the user with a summary and get confirmation:

```
I'll generate a 3D model of "<prompt>" using the following plan:

  1. Preview (mesh generation) — 5-20 credits (meshy-6/lowpoly: 20, others: 5)
  2. Refine (texturing with PBR) — 10 credits
  3. Download as .glb

  Total cost: 30 credits
  Current balance: <N> credits

  Shall I proceed?
```

For multi-step pipelines (e.g., text-to-3d → rig → animate), present the FULL pipeline cost upfront:

| Step | API | Credits |
|---|---|---|
| Preview | Text to 3D | 20 |
| Refine | Text to 3D | 10 |
| Rig | Auto-Rigging | 5 |
| **Total** | | **35** |

> **Note:** Rigging automatically includes basic walking + running animations for free (in `result.basic_animations`). Only add `Animate` (3 credits) if the user needs a custom animation beyond walking/running.

Wait for user confirmation before executing.

### Intent → API Mapping

| User wants to... | API | Endpoint | Credits |
|---|---|---|---|
| 3D model from text | Text to 3D | `POST /openapi/v2/text-to-3d` | 5–20 (preview) + 10 (refine) |
| 3D model from one image | Image to 3D | `POST /openapi/v1/image-to-3d` | 5–30 |
| 3D model from multiple images | Multi-Image to 3D | `POST /openapi/v1/multi-image-to-3d` | 5–30 |
| New textures on existing model | Retexture | `POST /openapi/v1/retexture` | 10 |
| Change mesh format/topology | Remesh | `POST /openapi/v1/remesh` | 5 |
| Add skeleton to character | Auto-Rigging | `POST /openapi/v1/rigging` | 5 (includes walking + running) |
| Animate a rigged character (custom) | Animation | `POST /openapi/v1/animations` | 3 |
| 2D image from text | Text to Image | `POST /openapi/v1/text-to-image` | 3–9 |
| Transform a 2D image | Image to Image | `POST /openapi/v1/image-to-image` | 3–9 |
| Check credit balance | Balance | `GET /openapi/v1/balance` | 0 |
| Multi-color 3D print | Multi-Color Print | `POST /openapi/v1/print/multi-color` | 10 |

---

## Step 2: Execute the Workflow

### CRITICAL: Async Task Model

All generation endpoints return `{"result": "<task_id>"}`, NOT the model. You MUST poll.

**NEVER** read `model_urls` from the POST response.

### Reusable Script Template

Use this as the base for ALL generation workflows:

```python
#!/usr/bin/env python3
"""Meshy API task runner. Handles create → poll → download."""
import requests, time, os, sys

API_KEY = os.environ.get("MESHY_API_KEY", "")
if not API_KEY:
    sys.exit("ERROR: MESHY_API_KEY not set")

BASE = "https://api.meshy.ai"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SESSION = requests.Session()
SESSION.trust_env = False  # bypass any system proxy settings

def create_task(endpoint, payload):
    resp = SESSION.post(f"{BASE}{endpoint}", headers=HEADERS, json=payload, timeout=30)
    if resp.status_code == 401:
        sys.exit("ERROR: Invalid API key (401)")
    if resp.status_code == 402:
        try:
            bal = SESSION.get(f"{BASE}/openapi/v1/balance", headers=HEADERS, timeout=10)
            balance = bal.json().get("balance", "unknown")
            sys.exit(f"ERROR: Insufficient credits (402). Current balance: {balance}. Top up at https://www.meshy.ai/pricing")
        except Exception:
            sys.exit("ERROR: Insufficient credits (402). Check balance at https://www.meshy.ai/pricing")
    if resp.status_code == 429:
        sys.exit("ERROR: Rate limited (429). Wait and retry.")
    resp.raise_for_status()
    task_id = resp.json()["result"]
    print(f"TASK_CREATED: {task_id}")
    return task_id

def poll_task(endpoint, task_id, timeout=300):
    """Poll task with exponential backoff (5s→30s, fixed 15s at 95%+)."""
    elapsed = 0
    delay = 5            # Initial delay: 5s
    max_delay = 30       # Cap: 30s
    backoff = 1.5        # Backoff multiplier
    finalize_delay = 15  # Fixed delay during finalization (95%+)
    poll_count = 0
    while elapsed < timeout:
        poll_count += 1
        resp = SESSION.get(f"{BASE}{endpoint}/{task_id}", headers=HEADERS, timeout=30)
        resp.raise_for_status()
        task = resp.json()
        status = task["status"]
        progress = task.get("progress", 0)
        filled = int(progress / 5)
        bar = f"[{'█' * filled}{'░' * (20 - filled)}] {progress}%"
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
    """Download a file to the given path (within a project directory)."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    print(f"Downloading {filepath}...", flush=True)
    resp = SESSION.get(url, timeout=300, stream=True)
    resp.raise_for_status()
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"DOWNLOADED: {filepath} ({size_mb:.1f} MB)")

# --- File organization helpers (see File Organization section above) ---
import re, json
from datetime import datetime

OUTPUT_ROOT = os.path.join(os.getcwd(), "meshy_output")
os.makedirs(OUTPUT_ROOT, exist_ok=True)
HISTORY_FILE = os.path.join(OUTPUT_ROOT, "history.json")

def get_project_dir(task_id, prompt="", task_type="model"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r'[^a-z0-9]+', '-', (prompt or task_type).lower())[:30].strip('-')
    folder = f"{timestamp}_{slug}_{task_id[:8]}"
    project_dir = os.path.join(OUTPUT_ROOT, folder)
    os.makedirs(project_dir, exist_ok=True)
    return project_dir

def record_task(project_dir, task_id, task_type, stage, prompt="", files=None):
    meta_path = os.path.join(project_dir, "metadata.json")
    if os.path.exists(meta_path):
        meta = json.load(open(meta_path))
    else:
        meta = {"project_name": prompt or task_type, "folder": os.path.basename(project_dir),
                "root_task_id": task_id, "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(), "tasks": []}
    meta["tasks"].append({"task_id": task_id, "task_type": task_type, "stage": stage,
                          "files": files or [], "created_at": datetime.now().isoformat()})
    meta["updated_at"] = datetime.now().isoformat()
    json.dump(meta, open(meta_path, "w"), indent=2)
    # Update global history
    if os.path.exists(HISTORY_FILE):
        history = json.load(open(HISTORY_FILE))
    else:
        history = {"version": 1, "projects": []}
    folder = os.path.basename(project_dir)
    entry = next((p for p in history["projects"] if p["folder"] == folder), None)
    if entry:
        entry["task_count"] = len(meta["tasks"])
        entry["updated_at"] = meta["updated_at"]
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

### Text to 3D (Preview + Refine)

Append this to the template above and run as one script:

```python
PROMPT = "USER_PROMPT"  # max 600 chars

# --- Preview ---
preview_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "preview",
    "prompt": PROMPT,
    "ai_model": "latest",
    # "model_type": "standard",    # "standard" | "lowpoly"
    # "topology": "triangle",      # "triangle" | "quad"
    # "target_polycount": 30000,   # 100–300000
    # "should_remesh": False,
    # "symmetry_mode": "auto",     # "auto" | "on" | "off"
    # "pose_mode": "t-pose",       # "" | "a-pose" | "t-pose" (use "t-pose" if rigging/animating later)
})

task = poll_task("/openapi/v2/text-to-3d", preview_id)
project_dir = get_project_dir(preview_id, prompt=PROMPT)
download(task["model_urls"]["glb"], os.path.join(project_dir, "preview.glb"))
record_task(project_dir, preview_id, "text-to-3d", "preview", prompt=PROMPT, files=["preview.glb"])
if task.get("thumbnail_url"):
    save_thumbnail(project_dir, task["thumbnail_url"])

print(f"\nPREVIEW COMPLETE")
print(f"  Task ID: {preview_id}")
print(f"  Project: {project_dir}")
print(f"  Formats: {', '.join(task['model_urls'].keys())}")

# --- Refine ---
refine_id = create_task("/openapi/v2/text-to-3d", {
    "mode": "refine",
    "preview_task_id": preview_id,
    "enable_pbr": True,
    "ai_model": "latest",
    # "texture_prompt": "",
    # "remove_lighting": True,     # Remove baked lighting (meshy-6/latest only, default True)
})

task = poll_task("/openapi/v2/text-to-3d", refine_id)
download(task["model_urls"]["glb"], os.path.join(project_dir, "refined.glb"))
record_task(project_dir, refine_id, "text-to-3d", "refined", prompt=PROMPT, files=["refined.glb"])

print(f"\nREFINE COMPLETE")
print(f"  Task ID: {refine_id}")
print(f"  Project: {project_dir}")
print(f"  Formats: {', '.join(task['model_urls'].keys())}")
```

> **Refine compatibility**: All models (meshy-5, meshy-6, latest) support both preview and refine. The preview and refine `ai_model` should match — mismatched models may return 400 (model mismatch).

### Image to 3D

```python
import base64

# For local files, convert to data URI:
# with open("photo.jpg", "rb") as f:
#     image_url = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

task_id = create_task("/openapi/v1/image-to-3d", {
    "image_url": "IMAGE_URL_OR_DATA_URI",
    "should_texture": True,
    "enable_pbr": True,            # Default is False; set True for metallic/roughness/normal maps
    "ai_model": "latest",
    # "image_enhancement": True,   # Optimize input image (meshy-6/latest only, default True)
    # "remove_lighting": True,     # Remove baked lighting from texture (meshy-6/latest only, default True)
})

task = poll_task("/openapi/v1/image-to-3d", task_id)
download(task["model_urls"]["glb"], "model.glb")
```

### Multi-Image to 3D

```python
task_id = create_task("/openapi/v1/multi-image-to-3d", {
    "image_urls": ["URL_1", "URL_2", "URL_3"],  # 1–4 images
    "should_texture": True,
    "enable_pbr": True,            # Default is False; set True for metallic/roughness/normal maps
    "ai_model": "latest",
    # "image_enhancement": True,   # Optimize input images (meshy-6/latest only, default True)
    # "remove_lighting": True,     # Remove baked lighting from texture (meshy-6/latest only, default True)
})
task = poll_task("/openapi/v1/multi-image-to-3d", task_id)
download(task["model_urls"]["glb"], "model.glb")
```

### Retexture

**IMPORTANT**: Before calling, ask the user to provide a texture style:
- **Text prompt**: e.g. "rusty metal", "cartoon style" → `text_style_prompt`
- **Reference image**: URL of style image → `image_style_url`
One of these is **required**. If both provided, `image_style_url` takes precedence.

```python
# REQUIRED: ask user for text_style_prompt OR image_style_url before calling
task_id = create_task("/openapi/v1/retexture", {
    "input_task_id": "PREVIOUS_TASK_ID",      # or "model_url": "URL"
    "text_style_prompt": "wooden texture",     # REQUIRED if no image_style_url
    # "image_style_url": "URL",               # REQUIRED if no text_style_prompt (takes precedence)
    "enable_pbr": True,
    # "remove_lighting": True,     # Remove baked lighting (meshy-6/latest only, default True)
    # "target_formats": ["glb", "3mf"],  # 3mf must be explicitly requested
    # "auto_size": True,           # AI auto-estimate real-world height
})
task = poll_task("/openapi/v1/retexture", task_id)
download(task["model_urls"]["glb"], "retextured.glb")
```

### Remesh / Format Conversion

```python
task_id = create_task("/openapi/v1/remesh", {
    "input_task_id": "TASK_ID",
    "target_formats": ["glb", "fbx", "obj"],
    "topology": "quad",
    "target_polycount": 10000,
})
task = poll_task("/openapi/v1/remesh", task_id)
for fmt, url in task["model_urls"].items():
    download(url, f"remeshed.{fmt}")
```

### Auto-Rigging + Animation

**IMPORTANT: When the user explicitly asks to rig or animate, the generation step (text-to-3d / image-to-3d) MUST use `pose_mode: "t-pose"` for best rigging results.** If the model was already generated without t-pose, recommend regenerating with `pose_mode: "t-pose"` first.

**Before rigging, verify the model's polygon count is under 300,000.** The script should auto-check and block if exceeded:

```python
# Pre-rig check: verify face count (MUST be ≤ 300,000)
source_endpoint = "/openapi/v2/text-to-3d"  # adjust to match the source task's endpoint
source_task_id = "TASK_ID"
check_resp = SESSION.get(f"{BASE}{source_endpoint}/{source_task_id}", headers=HEADERS, timeout=30)
check_resp.raise_for_status()
source = check_resp.json()
face_count = source.get("face_count", 0)
if face_count > 300000:
    print(f"ERROR: Model has {face_count:,} faces (limit: 300,000). Remesh first:")
    print(f"  create_task('/openapi/v1/remesh', {{'input_task_id': '{source_task_id}', 'target_polycount': 100000}})")
    sys.exit("Rigging blocked: face count too high")
```

```python
# Rig (humanoid bipedal characters only, polycount must be ≤ 300,000)
rig_id = create_task("/openapi/v1/rigging", {
    "input_task_id": "TASK_ID",
    "height_meters": 1.7,
})
rig_task = poll_task("/openapi/v1/rigging", rig_id)
download(rig_task["result"]["rigged_character_glb_url"], "rigged.glb")

# Rigging automatically includes basic walking + running animations — download them:
download(rig_task["result"]["basic_animations"]["walking_glb_url"], "walking.glb")
download(rig_task["result"]["basic_animations"]["running_glb_url"], "running.glb")

# Only call meshy_animate if you need a CUSTOM animation beyond walking/running:
# anim_id = create_task("/openapi/v1/animations", {
#     "rig_task_id": rig_id,
#     "action_id": 1,  # from Animation Library
# })
# anim_task = poll_task("/openapi/v1/animations", anim_id)
# download(anim_task["result"]["animation_glb_url"], "animated.glb")
```

### Text to Image / Image to Image

```python
# Text to Image
task_id = create_task("/openapi/v1/text-to-image", {
    "ai_model": "nano-banana-pro",
    "prompt": "a futuristic spaceship",
})
task = poll_task("/openapi/v1/text-to-image", task_id)
# Result: task["image_url"]

# Image to Image
task_id = create_task("/openapi/v1/image-to-image", {
    "ai_model": "nano-banana-pro",
    "prompt": "make it look cyberpunk",
    "reference_image_urls": ["URL"],
})
task = poll_task("/openapi/v1/image-to-image", task_id)
```

---

## Step 3: Report Results

After task succeeds, report:

1. **Downloaded file paths** and sizes
2. **Task IDs** (for follow-up operations like refine, rig, retexture)
3. **Available formats** (list `model_urls` keys — may include glb, fbx, obj, usdz, 3mf)
4. **Thumbnail URL** if present
5. **Credits consumed** and remaining balance (run balance check)
6. **Suggested next steps**:
   - Preview done → "Want to refine (add textures)?"
   - Model done → "Want to rig this character for animation?"
   - Rigged → "Want to apply an animation?"
   - Any model → "Want to remesh / export to another format?"
   - Any textured model → "Want to 3D print this? Multicolor printing is available!" (requires `meshy-3d-printing` skill)
   - Any model → "Want to 3D print this model?" (requires `meshy-3d-printing` skill)

---

## Error Recovery

| HTTP Status | Meaning | Action |
|---|---|---|
| 401 | Invalid API key | Re-run Step 0; ask user to check key |
| 402 | Insufficient credits | Auto-query balance (`GET /openapi/v1/balance`), show current balance, link https://www.meshy.ai/pricing |
| 422 | Cannot process | Explain limitation (e.g., non-humanoid for rigging) |
| 429 | Rate limited | Auto-retry after 5s (max 3 times) |
| 5xx | Server error | Auto-retry after 10s (once) |

Task `FAILED` messages:
- `"The server is busy..."` → retry with backoff (5s, 10s, 20s)
- `"Internal server error."` → simplify prompt, retry once

---

## Known Behaviors & Constraints

- **99% progress stall**: Tasks commonly sit at 99% for 30–120s during finalization. This is normal. Do NOT kill or restart.
- **CORS**: API blocks browser requests. Always server-side.
- **Asset retention**: Files deleted after **3 days** (non-Enterprise). Download immediately.
- **PBR maps**: Must set `enable_pbr: true` explicitly.
- **Format availability**: Check keys in `model_urls` before downloading — not all formats are always present. 3MF is available from the Multi-Color Print API.
- **Download format**: ALWAYS ask the user which format they need before downloading. Recommend: GLB (viewing), OBJ (white model printing), 3MF (multicolor printing), FBX (game engines), USDZ (AR). Do NOT download all formats.
- **3MF format**: 3MF is NOT included in default output of generation endpoints. To get 3MF from generate/remesh/retexture, pass `"3mf"` in `target_formats`. For multicolor 3D printing, the Multi-Color Print API outputs 3MF directly — no need to request it from generate/refine.
- **Timestamps**: All API timestamps are Unix epoch **milliseconds**.
- **Large files**: Refined models can be 50–200 MB. Use streaming downloads with timeouts.

---

## Execution Checklist

- [ ] Ran environment detection (Step 0)
- [ ] API key present and verified
- [ ] Presented cost summary and got user confirmation
- [ ] Wrote complete workflow as single Python script
- [ ] Ran script with `python3 -u` for unbuffered output
- [ ] Reported file paths, formats, task IDs, and balance
- [ ] Suggested next steps

## Additional Resources

For the complete API endpoint reference including all parameters, response schemas, deprecated fields, and detailed error codes, read [reference.md](reference.md).
