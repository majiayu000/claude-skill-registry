---
name: file-download
description: |
  Download files from websites, save PDFs, and read downloaded content.
  Trigger when the user asks to: download a file, save a PDF, export a document,
  fetch a file from a URL, grab a report, download and read a PDF, or save page content as a file.
allowed-tools: Bash(openbrowser-ai:*) Bash(curl:*) Bash(uv:*) Bash(irm:*) Read Write
---

# File Download

Download files from websites using the browser's authenticated session. Handles PDFs, CSVs, images, and any downloadable content. Preserves cookies and login sessions for authenticated downloads.

All code runs via `openbrowser-ai -c`. The daemon starts automatically and persists variables across calls. All browser functions are async -- use `await`.

The CLI daemon also persists cookies and login state in `~/.config/openbrowser/profiles/daemon/storage_state.json`, so authenticated sessions can be reused across later runs.

## Setup

Before running, verify openbrowser-ai is installed:

```bash
openbrowser-ai --help
```

If not found, install:

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.ps1 | iex
```

## Workflow

### Step 1 -- Navigate and find download links

```bash
openbrowser-ai -c - <<'EOF'
await navigate("https://example.com/reports")

# Get browser state to find clickable download links
state = await browser.get_browser_state_summary()
for idx, el in state.dom_state.selector_map.items():
    text = el.get_all_children_text(max_depth=1)
    if "download" in text.lower() or "pdf" in text.lower() or "export" in text.lower():
        print(f"[{idx}] {el.tag_name}: {text}")
EOF
```

### Step 2 -- Download a file by URL

Use `download_file()` to download directly. This uses the browser's JavaScript `fetch` internally, preserving cookies and authentication:

```bash
openbrowser-ai -c - <<'EOF'
path = await download_file("https://example.com/reports/annual-report.pdf")
print(f"Saved to: {path}")
EOF
```

With a custom filename:

```bash
openbrowser-ai -c - <<'EOF'
path = await download_file(
    "https://example.com/api/export?format=csv",
    filename="sales-data.csv"
)
print(f"Saved to: {path}")
EOF
```

### Step 3 -- Extract a download URL from the page

When the download URL is not directly visible, extract it from a link or button:

```bash
openbrowser-ai -c - <<'EOF'
# Extract href from a download link
download_url = await evaluate("""
(function(){
  const link = document.querySelector("a[href$=\".pdf\"]");
  return link ? link.href : null;
})()
""")

if download_url:
    path = await download_file(download_url)
    print(f"Downloaded: {path}")
else:
    print("No PDF link found")
EOF
```

### Step 4 -- Read a downloaded PDF

After downloading, use `pypdf` to extract text (requires `pip install openbrowser-ai[pdf]`):

```bash
openbrowser-ai -c - <<'EOF'
from pypdf import PdfReader

reader = PdfReader(path)
print(f"Pages: {len(reader.pages)}")

# Extract text from all pages
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"--- Page {i+1} ---")
    print(text[:500])
EOF
```

### Step 5 -- Read other file types

```bash
openbrowser-ai -c - <<'EOF'
from pathlib import Path

file_path = Path(path)

# CSV
if file_path.suffix == ".csv":
    import pandas as pd
    df = pd.read_csv(file_path)
    print(df.to_string())

# JSON
if file_path.suffix == ".json":
    import json
    data = json.loads(file_path.read_text())
    print(json.dumps(data, indent=2))

# Plain text
if file_path.suffix in (".txt", ".md", ".log"):
    print(file_path.read_text())
EOF
```

### Step 6 -- Download multiple files

```bash
openbrowser-ai -c - <<'EOF'
urls = [
    "https://example.com/report-q1.pdf",
    "https://example.com/report-q2.pdf",
    "https://example.com/report-q3.pdf",
]

paths = []
for url in urls:
    path = await download_file(url)
    paths.append(path)
    print(f"Downloaded: {path}")

print(f"Total files: {len(paths)}")
EOF
```

### Step 7 -- List all downloads

```bash
openbrowser-ai -c - <<'EOF'
files = list_downloads()
for f in files:
    print(f)
print(f"Total: {len(files)} files")
EOF
```

### Step 8 -- Download from authenticated pages

`download_file()` preserves the browser's login session. Log in first, then download:

```bash
openbrowser-ai -c - <<'EOF'
# Navigate and log in
await navigate("https://portal.example.com/login")
await input_text(username_index, "user@example.com")
await input_text(password_index, "password")
await click(login_button_index)
await wait(2)

# Now download an authenticated resource
path = await download_file("https://portal.example.com/api/reports/confidential.pdf")
print(f"Downloaded: {path}")
EOF
```

## Tips

- Code is piped via stdin using heredoc (`-c - <<'EOF'`), so all Python syntax works without shell escaping issues.
- Use `download_file(url)` instead of `navigate(url)` for files. `navigate()` opens PDFs in the browser viewer but does not save them.
- `download_file()` preserves cookies and authentication -- no need to re-authenticate.
- Filename conflicts are handled automatically with `(N)` suffix (e.g., `report (1).pdf`).
- If no filename is provided, it is derived from the URL path.
- Use `list_downloads()` to see all files saved in the downloads directory.
- For large files, `download_file()` has a 120-second timeout.
- The fallback strategy uses Python `requests` if the browser fetch fails (e.g., CORS restrictions), but without browser cookies.

## Cleanup

This step is **mandatory**. Run it after every download run, whether the file landed successfully or the request failed. Without it, the daemon keeps Chrome running until its 10-minute idle timeout, leaving a stale browser process, a locked profile, and (on macOS/Linux desktop) a visible window.

Stop the daemon, then verify it is gone:

```bash
openbrowser-ai daemon stop
openbrowser-ai daemon status
```

`daemon stop` closes every tab, exits Chrome, flushes saved cookies/login state to the profile, and shuts down the daemon process. `daemon status` should report the daemon is not running. If it still reports running, the daemon is wedged, force-kill it:

```bash
pkill -f 'openbrowser.*daemon' || true
```

If a download can fail mid-workflow (timeout, 4xx/5xx, CORS), guarantee cleanup with a shell trap so the browser is never left orphaned:

```bash
trap 'openbrowser-ai daemon stop >/dev/null 2>&1 || true' EXIT
# ... openbrowser-ai -c calls here ...
```

Downloaded files in `~/.config/openbrowser/downloads/` survive `daemon stop`, only the browser process is terminated. Do not rely on the idle timeout. Do not call `done()` as a substitute, `done()` only marks the task complete inside the agent loop, it does not close the browser.
