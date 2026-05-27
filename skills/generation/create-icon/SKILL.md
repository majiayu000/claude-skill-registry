---
name: create-icon
description: >
  Create icons for Stream Deck or other uses.
  Fetches from web, resizes to 72x72, creates white/active states.
allowed-tools: ["Bash", "Read", "Write", "surf"]
triggers:
  - create icon
  - generate icon
  - make icon
  - fetch icon
  - stream deck icon
  - process icon
metadata:
  short-description: "Create icons (72x72, Stream Deck compatible)"
---

# create-icon

Centralized utility for creating high-quality Stream Deck icons with consistent aesthetics.

## Features

- **Automated Fetching**: Uses `surf` to find and download icons from Flaticon or other free providers.
- **Pre-flight Standardization**: Automatically resizes to 72x72 and ensures PNG format.
- **State Generation**:
  - `inactive`: High-contrast white.
  - `active`: Vibrant "active" color (default: cyan/yellow).
- **Collaborative Workflow**: Search for multiple candidates and pick the best one via personal interview.

## Usage

```bash
# Fetch a NEW icon by keyword
./run.sh fetch "folder" --name "my_folder"

# Generate states for an EXISTING icon
./run.sh generate "/path/to/icon.png" --name "my_icon"

# COLLABORATIVE search and selection
./run.sh collaborative "camera" --name "my_camera"

# DIRECT AI-driven creation
./run.sh create "terminal prompt inside a rounded rectangle" --name "my_terminal"
```

## How It Works

1. **Fetch**: Uses `surf` to search for icons, picks the first result, and downloads it.
2. **Process**: Uses ImageMagick (`convert`) or Pillow to:
   - Resize to 72x72.
   - Use `+level-colors` or tinting to create the two required states.
3. **Output**: Saves to the local `icon/` directory of the calling project.

## Commands

| Command | Description |
|---------|-------------|
| `fetch <keyword>` | Search web and download icon |
| `generate <path>` | Create states from existing icon |
| `collaborative <keyword>` | Interactive search and selection |
| `create <prompt>` | AI-driven icon generation |

## Output Structure

```
icon/
├── my_icon_inactive.png  # White/gray (72x72)
├── my_icon_active.png    # Colored state (72x72)
└── my_icon_original.png  # Source file
```

## Dependencies

- `surf` skill for web fetching
- ImageMagick or Pillow for image processing
