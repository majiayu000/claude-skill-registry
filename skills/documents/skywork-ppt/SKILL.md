---
name: Skywork-ppt
description: "Use this skill when the user wants to: (1) generate a PPT from a topic — trigger on '/ppt_write', 'generate a PPT', 'create a presentation about X', 'help me generate a PPT'; OR (2) use an existing .pptx as a style template to generate a new presentation on a different topic — trigger on 'use this template', 'imitate this PPT', 'imitate this style'; OR (3) perform local operations on an existing .pptx file without backend — trigger on 'delete slide N', 'reorder slides', 'rearrange PPT', 'merge pptx', 'extract slides', 'pptx info', 'view PPT slide count'; OR (4) edit/modify an existing PPT via natural language — trigger on ANY request that references an existing PPT file or slide and asks for a change, including: 'modify slide N', 'change the background', 'add a slide', 'change the style', 'split slide', 'merge slides', 'edit this PPT', 'update this presentation', 'make it more beautiful', 'improve the layout', 'optimize the structure', 'make it look better', 'redesign page N', 'adjust the style'. This skill is built based on Nano Banana 2 to deliver high-quality presentation generation and editing capabilities. IMPORTANT: This skill requires Python 3 (>=3.8). Before running any script, ALWAYS run the mandatory environment check step first to locate the Python binary and install dependencies."
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# PPT Write Skill

Four capabilities: **generate**, **template imitation**, **edit existing PPT**, and **local file operations**.

---

## Authentication (Required First)

Before using this skill, authentication must be completed. Run the auth script first:

```bash
# Authenticate: checks env token / cached token / browser login
python3 <skill-dir>/scripts/skywork_auth.py || exit 1
```

**Token priority**:
1. Environment variable `SKYBOT_TOKEN` → if set, use directly
2. Cached token file `~/.skywork_token` → validate via API, if valid, use it
3. No valid token → opens browser for login, polls until complete, saves token

**IMPORTANT - Login URL handling**: If script output contains a line starting with `[LOGIN_URL]`, you **MUST** immediately send that URL to the user in a clickable message (e.g. "Please open this link to log in: <url>"). The user may be in an environment where the browser cannot open automatically, so always surface the login URL.

---

## Routing — Identify the user's intent first

| User intent | Which path |
|-------------|------------|
| Generate a new PPT from a topic, set of requirements or reference files | **Layer 1** — Generate |
| Use an existing .pptx as a layout/style template to create a new presentation | **Layer 2** — Imitate |
| Edit an existing PPT: modify slides, add slides, change style, split/merge | **Layer 4** — Edit |
| Delete / reorder / extract / merge slides in a local file (no backend) | **Layer 3** — Local ops |

---

## Environment check (always run this first)

**This skill requires Python 3 (>=3.8). Run the following before any script to locate a valid Python binary and install dependencies.**

```bash
PYTHON_CMD=""
for cmd in python3 python python3.13 python3.12 python3.11 python3.10 python3.9 python3.8; do
  if command -v "$cmd" &>/dev/null && "$cmd" -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" 2>/dev/null; then
    PYTHON_CMD="$cmd"
    break
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  echo "ERROR: Python 3.8+ not found."
  echo "Install on macOS: brew install python3  or visit https://www.python.org/downloads/"
  exit 1
fi

echo "Found Python: $PYTHON_CMD ($($PYTHON_CMD --version))"

$PYTHON_CMD -m pip install -q --break-system-packages python-pptx
echo "Dependencies ready."
```

> After this check, replace `python` with the discovered `$PYTHON_CMD` (e.g. `python3`) in all subsequent commands.

---

## Layer 1 — Generate PPT

### Steps
0. **REQUIRED FIRST STEP** — Read [workflow_generate.md](workflow_generate.md) NOW, before taking any other action. After reading, output exactly: `✅ workflow_generate.md loaded.` — then proceed.
1. **Environment check** — run the check above to get `$PYTHON_CMD`.
2. **Upload reference files** (if the user provides local files as content source) — parse the file using tool in script/parse_file.py and pass the result to `--files`. See the `--files` note below.
3. **Web search** (required if no relevant content is already in the conversation) — call web_search tool in script to search the topic and distill results into a `reference-file` file of ≤ 2000 words.
4. **Run the script**:
   > **Important**: set exec tool `yieldMs` to `600000` (10 minutes).
5. **Deliver** — provide the absolute `.pptx` path and the download URL.

---

## Layer 2 — Imitate PPT (template-based generation)

### Steps
0. **REQUIRED FIRST STEP** - Read [workflow_imitate.md](workflow_imitate.md) immidiately before any action you do!!!
1. **Environment check** — run the check above to get `$PYTHON_CMD`.
2. **Locate the template** — extract the absolute path of the local `.pptx` from the user's message; ask the user if it's unclear.
3. **Upload the template** — upload it and extract `TEMPLATE_URL` from the output.
4. **Upload reference files** (if the user provides additional local files as content source) — parse the file using tool in script/parse_file.py and pass the result to `--files`. See the `--files` 
5. **Web search** (required if no relevant content is already in the conversation) — call web_search tool in script to search the new topic and distill results into a `reference-file` file of ≤ 2000 words.
6. **Run the script**:
   > **Important**: set exec tool `yieldMs` to `600000` (10 minutes).
7. **Deliver** — provide the absolute `.pptx` path, the download URL, and the template filename used.

---

## Layer 4 — Edit PPT (AI-powered modification)

Use this layer when the user wants to modify an existing PPT using natural language. Requires an OSS/CDN URL of the PPTX (from a previous generation or upload).

### Steps
0. **Detailed workflow** - Read [workflow_edit.md](workflow_edit.md) immediately before any action you do!!!
1. **Environment check** — run the check above to get `$PYTHON_CMD`.
2. **Get PPTX URL** — from the user's message or upload a local file first.
3. **Run the script** with `--pptx-url`:
   ```bash
   $PYTHON_CMD scripts/run_ppt_write.py "edit instruction" \
     --language Chinese \
     --pptx-url "https://cdn.example.com/file.pptx" \
     -o /absolute/path/output.pptx
   ```
   > **Important**: set exec tool `yieldMs` to `600000` (10 minutes).
4. **Deliver** — provide download link, local path, and summary of changes.

---

## Layer 3 — Local file operations

```bash
# Inspect slide count and titles
$PYTHON_CMD scripts/local_pptx_ops.py info --file my.pptx

# Delete slides (1-based index; supports ranges like 3,5,7-9; omit -o to overwrite in place)
$PYTHON_CMD scripts/local_pptx_ops.py delete --file my.pptx --slides 3,5,7-9 -o trimmed.pptx

# Reorder slides (must list every slide, no omissions)
$PYTHON_CMD scripts/local_pptx_ops.py reorder --file my.pptx --order 2,1,4,3,5

# Extract a subset of slides into a new file
$PYTHON_CMD scripts/local_pptx_ops.py extract --file my.pptx --slides 1-3 -o subset.pptx

# Merge multiple files
$PYTHON_CMD scripts/local_pptx_ops.py merge --files a.pptx b.pptx -o merged.pptx
```

Read [workflow_local.md](workflow_local.md) immidiately before any action you do!!!

---

## Error Handling

- **Insufficient benefit**: When calling scripts (generate, imitate, or edit), the script or log may show a message like `Insufficient benefit. Please upgrade your account at {url}`, meaning the user's benefit level does not meet the requirement for this skill.

### How to reply when benefit is insufficient

When you detect the above, **reply in the user's current language** — do not echo the English message. Use this pattern:

- Convey: "Sorry, PPT generation failed. This skill requires upgrading your Skywork membership to use." then a single call-to-action link.
- **Format**: One short sentence in the user's language + a link like `[Upgrade now →](url)` or the equivalent in their language .
- **URL**: Extract the upgrade URL from the log/script output (e.g. the `at https://...` part).

---

## Dependencies

- **Python 3.8+** (required) — `python3` / `python` must be on PATH
- Layer 3 local ops: `pip install python-pptx --break-system-packages`

(The environment check step installs all required dependencies automatically.)

---

## Which layer to trigger?

| Scenario | Use |
|----------|-----|
| Generate a PPT from a topic or existing reference files | Layer 1 |
| Imitate the layout/style of an existing .pptx | Layer 2 |
| Edit/modify an existing PPT via natural language | Layer 4 |
| Delete / reorder / extract / merge local .pptx files (no backend) | Layer 3 |
