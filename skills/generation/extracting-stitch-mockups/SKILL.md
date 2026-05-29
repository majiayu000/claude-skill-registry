---
name: extracting-stitch-mockups
description: >
  Extracts generated mockup images from Google Stitch project pages.
  Use when user provides a Stitch project URL (stitch.withgoogle.com/projects/...),
  mentions extracting/downloading Stitch mockups, saving Stitch designs, or wants to
  archive generated design assets. Requires authenticated Chrome browser profile.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Extract Stitch Mockups

## Quick Start
1. **Get project URL** - User provides `https://stitch.withgoogle.com/projects/{id}`
2. **Resolve feature directory** - Determine where to save using fallback chain
3. **Run extraction script** - Execute `scripts/extract_images.py` with Playwright
4. **Save to exports** - Images saved to `design-intent/google-stitch/{feature}/exports/`

---

## Feature Directory Resolution

Determine target feature directory using this fallback chain:

1. **User specifies** - Optional `--feature` argument provided
2. **Auto-detect** - Match Stitch project title to existing `design-intent/google-stitch/{feature}/` directories
3. **Prompt user** - List existing directories and ask user to select or create new

### Auto-Detection Logic
- Extract project title from Stitch page (e.g., "Eco-Travel Home Screen")
- Normalize to feature format: lowercase, hyphens, strip special chars
- Search for matching directory in `design-intent/google-stitch/`
- If multiple partial matches, prompt user to select

---

## Extraction Process

### Prerequisites
- Chrome browser with active Google session
- uv installed (https://github.com/astral-sh/uv)
- Playwright browsers: `uv run playwright install chromium`

### Script Execution
```bash
# Basic usage
uv run scripts/extract_images.py "https://stitch.withgoogle.com/projects/123"

# With explicit feature directory
uv run scripts/extract_images.py "https://stitch.withgoogle.com/projects/123" --feature dashboard

# Or run directly (after chmod +x)
./scripts/extract_images.py "https://stitch.withgoogle.com/projects/123"
```

### Image Filtering
- Source: `lh3.googleusercontent.com/aida/...` URLs only
- Size filter: Images with dimensions >= 400px (mockups, not UI elements)
- Excludes: avatars, icons, UI chrome

### Generation Check
Script checks for "Generating..." status on page:
- If detected: Exit with message to retry after generation completes
- If complete: Proceed with extraction

---

## Output Structure

Images saved to existing feature's `exports/` directory:

```
design-intent/google-stitch/{feature}/exports/
├── mockup-1.png
├── mockup-2.png
└── mockup-N.png
```

### File Naming
- Sequential numbering: `mockup-{index}.png`
- Index starts at 1
- Preserves original image format (typically PNG)

---

## Report

After extraction, display summary:

```
Extracted {N} mockups from Stitch project

Project: {project-title}
URL: {project-url}

Saved to: design-intent/google-stitch/{feature}/exports/
  - mockup-1.png (400x800)
  - mockup-2.png (400x800)
  - ...

Feature directory:
  design-intent/google-stitch/{feature}/
  ├── prompt-v{N}.md
  ├── exports/          <- Mockups saved here
  │   ├── mockup-1.png
  │   └── mockup-2.png
  └── wireframes/
```

---

## Common Issues

- **Not authenticated** - Open Chrome, sign into Google, then retry
- **Still generating** - Wait for Stitch to complete, then retry
- **No feature directory** - Run authoring-stitch-prompts first, or specify `--feature`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## Reference Files
- [WORKFLOW.md](WORKFLOW.md) - Detailed browser automation steps
- [EXAMPLES.md](EXAMPLES.md) - Sample extractions
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error handling
