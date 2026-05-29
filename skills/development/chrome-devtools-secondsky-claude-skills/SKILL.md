---
name: chrome-devtools
description: Browser automation with Puppeteer CLI scripts. Use for screenshots, performance analysis, network monitoring, web scraping, form automation, or encountering JavaScript debugging, browser automation errors.
license: Apache-2.0
---

# Chrome DevTools Agent Skill

Browser automation via executable Puppeteer scripts. All scripts output JSON for easy parsing.

## Quick Start

**CRITICAL**: Always check `pwd` before running scripts.

### Installation

#### Step 1: Install System Dependencies (Linux/WSL only)

On Linux/WSL, Chrome requires system libraries. Install them first:

```bash
pwd  # Should show current working directory
cd .claude/skills/chrome-devtools/scripts
./install-deps.sh  # Auto-detects OS and installs required libs
```

Supports: Ubuntu, Debian, Fedora, RHEL, CentOS, Arch, Manjaro

**macOS/Windows**: Skip this step (dependencies bundled with Chrome)

#### Step 2: Install Node Dependencies

```bash
# Preferred: Using bun (faster)
bun install  # Installs puppeteer, debug, yargs

# Alternative: Using npm
npm install
```

#### Step 3: Install ImageMagick (Optional, Recommended)

ImageMagick enables automatic screenshot compression to keep files under 5MB:

**macOS:**
```bash
brew install imagemagick
```

**Ubuntu/Debian/WSL:**
```bash
sudo apt-get install imagemagick
```

**Verify:**
```bash
magick -version  # or: convert -version
```

Without ImageMagick, screenshots >5MB will not be compressed (may fail to load in Gemini/Claude).

### Test
```bash
bun navigate.js --url https://example.com
# Output: {"success": true, "url": "https://example.com", "title": "Example Domain"}
```

## Available Scripts

All scripts are in `.claude/skills/chrome-devtools/scripts/`

**CRITICAL**: Always check `pwd` before running scripts.

### Script Usage
- `./scripts/README.md`

### Core Automation
- `navigate.js` - Navigate to URLs
- `screenshot.js` - Capture screenshots (full page or element)
- `click.js` - Click elements
- `fill.js` - Fill form fields
- `evaluate.js` - Execute JavaScript in page context

### Analysis & Monitoring
- `snapshot.js` - Extract interactive elements with metadata
- `console.js` - Monitor console messages/errors
- `network.js` - Track HTTP requests/responses
- `performance.js` - Measure Core Web Vitals + record traces

## Usage Patterns

### Single Command
```bash
pwd  # Should show current working directory
cd .claude/skills/chrome-devtools/scripts
bun screenshot.js --url https://example.com --output ./docs/screenshots/page.png
```
**Important**: Always save screenshots to `./docs/screenshots` directory.

### Automatic Image Compression
Screenshots are **automatically compressed** if they exceed 5MB to ensure compatibility with Gemini API and Claude Code (which have 5MB limits). This uses ImageMagick internally:

```bash
# Default: auto-compress if >5MB
bun screenshot.js --url https://example.com --output page.png

# Custom size threshold (e.g., 3MB)
bun screenshot.js --url https://example.com --output page.png --max-size 3

# Disable compression
bun screenshot.js --url https://example.com --output page.png --no-compress
```

**Compression behavior:**
- PNG: Resizes to 90% + quality 85 (or 75% + quality 70 if still too large)
- JPEG: Quality 80 + progressive encoding (or quality 60 if still too large)
- Other formats: Converted to JPEG with compression
- Requires ImageMagick installed (see imagemagick skill)

**Output includes compression info:**
```json
{
  "success": true,
  "output": "/path/to/page.png",
  "compressed": true,
  "originalSize": 8388608,
  "size": 3145728,
  "compressionRatio": "62.50%",
  "url": "https://example.com"
}
```

### Chain Commands (reuse browser)
```bash
# Keep browser open with --close false
bun navigate.js --url https://example.com/login --close false
bun fill.js --selector "#email" --value "user@example.com" --close false
bun fill.js --selector "#password" --value "secret" --close false
bun click.js --selector "button[type=submit]"
```

### Parse JSON Output
```bash
# Extract specific fields with jq
bun performance.js --url https://example.com | jq '.vitals.LCP'

# Save to file
bun network.js --url https://example.com --output /tmp/requests.json
```

## Execution Protocol

### Working Directory Verification

BEFORE executing any script:
1. Check current working directory with `pwd`
2. Verify in `.claude/skills/chrome-devtools/scripts/` directory
3. If wrong directory, `cd` to correct location
4. Use absolute paths for all output files

Example:
```bash
pwd  # Should show: .../chrome-devtools/scripts
# If wrong:
cd .claude/skills/chrome-devtools/scripts
```

### Output Validation

AFTER screenshot/capture operations:
1. Verify file created with `ls -lh <output-path>`
2. Read screenshot using Read tool to confirm content
3. Check JSON output for success:true
4. Report file size and compression status

Example:
```bash
bun screenshot.js --url https://example.com --output ./docs/screenshots/page.png
ls -lh ./docs/screenshots/page.png  # Verify file exists
# Then use Read tool to visually inspect
```

5. Restart working directory to the project root.

### Error Recovery

If script fails:
1. Check error message for selector issues
2. Use snapshot.js to discover correct selectors
3. Try XPath selector if CSS selector fails
4. Verify element is visible and interactive

Example:
```bash
# CSS selector fails
bun click.js --url https://example.com --selector ".btn-submit"
# Error: waiting for selector ".btn-submit" failed

# Discover correct selector
bun snapshot.js --url https://example.com | jq '.elements[] | select(.tagName=="BUTTON")'

# Try XPath
bun click.js --url https://example.com --selector "//button[contains(text(),'Submit')]"
```

## Common Options

All scripts support:
- `--headless false` - Show browser window (default: true)
- `--close false` - Keep browser open after script
- `--timeout 30000` - Timeout in milliseconds (default: 30000)
- `--help` - Show script-specific help

## Troubleshooting

**Browser fails to launch (Linux)**:
```bash
./install-deps.sh  # Install missing system libraries
```

**Large screenshots**:
- Enable ImageMagick for automatic compression
- Use `--max-size` to set custom threshold
- Or capture specific element instead of full page

**Element not found**:
- Use `snapshot.js` first to discover selectors
- Check if element is dynamically loaded (wait longer)
- Try XPath if CSS fails

**Script not found**:
- Verify you're in the correct directory
- Check script name spelling
- Use absolute path: `bun /path/to/scripts/navigate.js`
