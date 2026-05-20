---
name: gh-assets-branch-mgmt
description: "Manages GitHub assets branch for persistent image hosting in PRs. Creates orphan branch, uploads files, generates raw URLs. Bypasses transient CDN tokens. Triggers on keywords: assets branch, upload screenshots, pr images, persistent images, github assets"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# GitHub Assets Branch Management

Automates the "assets branch" strategy for persistent image hosting in GitHub PRs. Solves the problem of transient CDN tokens (`?jwt=...`) that expire on private repo images.

## Playwright CLI Integration

**CRITICAL**: When using playwright-cli for E2E testing, video recording is explicit.

### Video Recording

Start and stop recording explicitly with playwright-cli:
```bash
playwright-cli video-start    # Start recording
# ... perform browser actions ...
playwright-cli video-stop     # Stop and save video file
```
- **Storage**: `outputs/e2e/` directory (or configured `outputDir`)
- **Format**: Video files saved by playwright-cli
- **Resolution**: Configured in `playwright-cli.json` `saveVideo` settings (default: `1920x1080`)

### Evidence Upload Workflow

When adding visual evidence to PRs:

| Evidence Type | Source | Tool |
|---------------|--------|------|
| Screenshots | `playwright-cli screenshot` | Direct capture via Bash |
| Video | `outputs/e2e/*.webm` | **Use recorded file** |

**DO NOT** re-record video when adding video evidence. Use the file from the E2E session.

### Standard Workflow

1. **Screenshots**: Use `playwright-cli screenshot` during E2E validation
2. **Video**: After E2E session completes (after `video-stop`), find the video in `outputs/e2e/`
3. **Upload**: Use this skill to upload screenshots + video (auto-converts to MP4+GIF)

```bash
# Upload all evidence (screenshots + video)
/gh-assets-branch-mgmt upload outputs/screenshots/*.png outputs/e2e/*.webm --context pr-42
```

The video will be automatically converted to H.264 MP4 (8x speed) + GIF for PR embedding.

## Commands

| Command | Description |
|---------|-------------|
| `init` | Create orphan `assets` branch if not exists |
| `upload <files/glob> --context <id>` | Upload files to `assets` branch under context path |
| `list --context <id>` | List all assets for a context |
| `cleanup --context <id>` | Remove all assets for a context |
| `url <file> --context <id>` | Get raw URL for a specific file |
| `convert-video <input> [options]` | Convert video to optimized H.264 MP4 |
| `download-video <context> [options]` | Download videos from assets branch |

## Usage

### Initialize Assets Branch

```bash
/gh-assets-branch-mgmt init
```

Creates an orphan `assets` branch with no commit history using Git's well-known empty tree SHA.

### Upload Files

```bash
/gh-assets-branch-mgmt upload outputs/screenshots/*.png --context pr-42
```

Uploads all matching files to `assets` branch under `pr-42/` path.

### Get URLs

```bash
/gh-assets-branch-mgmt url screenshot.png --context pr-42
```

Returns: `https://raw.githubusercontent.com/OWNER/REPO/assets/pr-42/screenshot.png`

### Upload Videos

Videos are automatically converted and uploaded as **both GIF + MP4**:

```bash
/gh-assets-branch-mgmt upload ./recording.mov --context pr-42
```

The tool:
1. Detects video by extension (mov, mp4, webm, avi, mkv, m4v)
2. Converts to H.264 MP4 (720p, CRF 28, **8x speed by default**)
3. Generates GIF **from the output MP4** (720px, 10fps, palette optimized)
4. Uploads **both** GIF (for inline embed) and MP4 (for download)
5. Outputs markdown for GIF embed + download link for MP4
6. Cleans up temporary files

**Output format:**
```markdown
![recording_converted](https://github.com/.../recording_converted.gif?raw=true)

[Download Recording](https://github.com/.../recording_converted.mp4?raw=true)
```

**Why both?** GIF embeds inline, MP4 provides full quality download option.

**Note:** Videos are sped up 8x by default (144s input -> 18s output). Audio is dropped.

### Convert Video (Standalone)

```bash
/gh-assets-branch-mgmt convert-video ./demo.mov --preset pr-medium
```

**Video Options:**
- `--preset <name>` - Compression preset (see table below)
- `--max-size <mb>` - Target file size in MB (enables two-pass encoding)
- `--output <path>` - Custom output path
- `--speed <factor>` - Playback speed multiplier (default: 8 = 8x faster)

**GIF Options:**
- `--gif` - Also generate GIF from output MP4
- `--gif-only` - Generate only GIF, remove MP4 after
- `--gif-fps <n>` - GIF frame rate (default: 10)
- `--gif-width <px>` - GIF max width (default: 720)

Examples:
```bash
# Default: 8x speed, pr-small preset (MP4 only)
./gh-video-convert.sh demo.mov

# Generate MP4 + GIF
./gh-video-convert.sh demo.mov --gif

# Generate only GIF (no MP4 kept)
./gh-video-convert.sh demo.mov --gif-only

# Custom GIF settings
./gh-video-convert.sh demo.mov --gif --gif-width 1080 --gif-fps 24

# Original speed (no speedup)
./gh-video-convert.sh demo.mov --speed 1
```

**Processing Pipeline:**
```
Input Video -> MP4 (scaled, sped up) -> GIF (from MP4)
```

The GIF is **always** generated from the output MP4, ensuring visual consistency.

### Video Presets

| Preset | Target Size | Resolution | CRF | Use Case |
|--------|-------------|------------|-----|----------|
| `pr-small` | ~8MB | 720p | 28 | GitHub free plan, short demos |
| `pr-medium` | ~25MB | 720p | 24 | Longer demos |
| `pr-large` | ~50MB | 1080p | 23 | High quality demos |
| `demo` | ~80MB | 1080p | 20 | Maximum quality |

### Download Videos

Download uploaded videos from the assets branch:

```bash
/gh-assets-branch-mgmt download-video pr-42
```

Downloads the latest video and opens it automatically.

**Options:**
- `--all` - Download all videos (default: latest only)
- `--list` - List videos without downloading
- `--no-open` - Don't open video after download
- `--output <dir>` - Download directory (default: /tmp)
- `--repo <owner/repo>` - Repository (default: current repo)

**Examples:**
```bash
# Download & open latest video
./gh-assets-download.sh pr-42

# Download all videos
./gh-assets-download.sh pr-42 --all

# List available videos
./gh-assets-download.sh pr-42 --list

# Download to specific directory
./gh-assets-download.sh pr-42 --output ./downloads
```

### Cleanup After PR Merge

```bash
/gh-assets-branch-mgmt cleanup --context pr-42
```

Removes all files under `pr-42/` from the assets branch.

## Implementation Details

### Orphan Branch Creation

Uses Git's well-known empty tree SHA to create a branch with no history:

```bash
EMPTY_TREE="4b825dc642cb6eb9a060e54bf8d69288fbee4904"
COMMIT=$(gh api repos/$OWNER/$REPO/git/commits -X POST \
  -f message="chore: initialize assets branch" \
  -f tree="$EMPTY_TREE" --jq '.sha')
gh api repos/$OWNER/$REPO/git/refs -X POST \
  -f ref="refs/heads/assets" -f sha="$COMMIT"
```

### File Upload Strategy

**CRITICAL**: Files must be uploaded sequentially (not in parallel). Use the bash script:

```bash
./gh-assets-upload.sh <source-dir> <context> <owner/repo>
```

Each file is uploaded via GitHub Contents API with inline base64 encoding:

```bash
gh api repos/OWNER/REPO/contents/{context}/{filename} -X PUT \
  -f message="assets({context}): add {filename}" \
  -f content="$(base64 -i {filepath})" \
  -f branch="assets" \
  --jq '.content.sha'
```

### URL Format

Use blob URL with `?raw=true` for embedding (works for both public and private repos):

```
https://github.com/{owner}/{repo}/blob/assets/{context}/{filename}?raw=true
```

Markdown syntax:
```markdown
![Alt Text](https://github.com/{owner}/{repo}/blob/assets/{context}/{filename}?raw=true)
```

### Directory Structure on Assets Branch

```
assets/
├── pr-1/
│   ├── screenshot1.png
│   └── screenshot2.png
├── pr-42/
│   └── demo.gif
└── README.md  (optional)
```

## Bash Script Tools

Scripts are located in this skill directory:

- `gh-assets-upload.sh` - Batch upload with auto video conversion
- `gh-video-convert.sh` - Standalone video conversion tool
- `gh-assets-download.sh` - Download videos from assets branch

Usage (from skill directory):
```bash
./gh-assets-upload.sh ./screenshots pr-42
./gh-video-convert.sh demo.mov --gif
./gh-assets-download.sh pr-42
```

## Error Handling

- **Branch exists**: Skip creation, proceed with upload
- **File exists**: Update (PUT) overwrites existing file
- **Upload fails**: Log error, continue with remaining files
- **Invalid context**: Must match pattern `[a-z0-9-]+`
- **Video conversion fails**: Falls back to uploading original file
- **ffmpeg not found**: Logs error, skips video conversion

## Limitations

### Private Repo Image Embedding

For private repos, use the **blob URL with `?raw=true`** format:

```markdown
![Screenshot](https://github.com/OWNER/REPO/blob/assets/pr-1/screenshot.png?raw=true)
```

**URL Format Comparison:**

| Format | Private Repo | Public Repo |
|--------|--------------|-------------|
| `raw.githubusercontent.com/.../assets/...` | 404 | Works |
| `github.com/.../blob/assets/...?raw=true` | Works | Works |

**Correct Pattern:**
```
https://github.com/{owner}/{repo}/blob/assets/{context}/{filename}?raw=true
```

### Video Size Limits

GitHub has different video size limits by plan:

| Plan | Max Video Size |
|------|----------------|
| Free | 10MB |
| Paid | 100MB |

Use `--preset pr-small` for free plan compatibility, or `--max-size <mb>` for precise control.

### GIF Size Guidance

| Duration | Approx GIF Size (720px, 10fps) |
|----------|--------------------------------|
| 10s | ~5-8MB |
| 30s | ~15-25MB |
| 60s | ~25-40MB |

For large GIFs, try `--gif-width 480` or `--gif-fps 8`.

### Other Limitations

- File size: GitHub API limits (~100MB per file)
- Rate limits: Sequential uploads to avoid GitHub API rate limiting
- Public repos: Raw URLs work for embedding without issues
- Video formats: MP4 output is H.264, GIF uses palette optimization
- Audio: Dropped when speed > 1 (use `--speed 1` to preserve audio)
- GIF: Generated from output MP4, not raw input (ensures consistency)
