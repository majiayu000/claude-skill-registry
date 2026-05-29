---
description: Search INAV wiki documentation for implementation guidance
triggers:
  - search wiki
  - find in wiki
  - wiki docs
  - search documentation
  - find in docs
  - lookup documentation
  - search inav docs
---

# Wiki Documentation Search

Search through INAV wiki documentation to find implementation guidance, technical details, and user documentation.

## Wiki Location

The INAV documentation wiki should be located at:
- `inavwiki/` directory (if cloned locally)
- Or online at the INAV GitHub wiki

## Quick Search

### Search for Keywords

```bash
# Search all wiki markdown files (ripgrep - preferred)
rg "keyword" inavwiki/

# Case-insensitive search
rg -i "keyword" inavwiki/

# Search with context (3 lines before/after)
rg -i "keyword" inavwiki/ -C 3

# Search only markdown files
rg -i "keyword" inavwiki/ -g "*.md"
```

**Fallback with grep (if ripgrep not available):**
```bash
grep -r "keyword" inavwiki/ --include="*.md"
```

### Using Claude's Grep Tool

For better results, use Claude's built-in Grep tool:

```
pattern: "your search term"
path: inavwiki/
glob: "*.md"
output_mode: "content"
-i: true
```

## Common Documentation Topics

### Flight Controller Features

Search for flight controller functionality:
```bash
# GPS navigation
rg -i "gps" inavwiki/

# Return to home
rg -i "rth|return to home" inavwiki/

# Waypoints
rg -i "waypoint" inavwiki/

# Failsafe
rg -i "failsafe" inavwiki/
```

### Configuration

Search for configuration documentation:
```bash
# CLI commands
rg -i "cli|command" inavwiki/

# Settings
rg -i "setting|parameter" inavwiki/

# Modes
rg -i "mode" inavwiki/
```

### Hardware Support

Search for supported hardware:
```bash
# Sensors
rg -i "sensor|accelerometer|gyro|compass" inavwiki/

# GPS modules
rg -i "gps|ublox|m8n|m9n" inavwiki/

# Flight controllers
rg -i "board|target" inavwiki/
```

### MSP Protocol

Search for MSP documentation:
```bash
# MSP commands
rg -i "msp" inavwiki/

# Communication
rg -i "serial|uart" inavwiki/
```

## Finding Specific Documentation Files

### List Files Containing Pattern

```bash
# List files with matches (no content)
rg -l "keyword" inavwiki/

# Count matches per file
rg -c "keyword" inavwiki/
```

### Search by Filename

```bash
# Find files by name pattern
rg --files inavwiki/ | rg "gps"
rg --files inavwiki/ | rg "navigation"
rg --files inavwiki/ | rg "programming"

# Or use find
find inavwiki -name "*gps*.md"
```

## Searching for Code Examples

### Find Code Blocks

```bash
# Find files with code blocks
rg "^\`\`\`" inavwiki/ -g "*.md"

# Find specific language code blocks
rg "^\`\`\`c" inavwiki/ -g "*.md"      # C code
rg "^\`\`\`bash" inavwiki/ -g "*.md"   # Bash
```

### Find Configuration Examples

```bash
# Find CLI command examples
rg "^set " inavwiki/ -g "*.md"

# Find configuration snippets
rg "^\# config" inavwiki/ -g "*.md"
```

## Browse Documentation Structure

### Common Wiki Sections

Typical wiki organization:
- `/docs/` - Main documentation
- `/docs/Getting Started/` - Installation and setup
- `/docs/Features/` - Feature documentation
- `/docs/Hardware/` - Supported hardware
- `/docs/Programming/` - Developer documentation
- `/docs/CLI/` - CLI command reference

### View Directory Structure

```bash
# Show wiki structure
tree inavwiki/ -L 2

# Or list all markdown files
rg --files inavwiki/ -g "*.md"
```

## Search Strategies

### When Searching for Implementation Guidance

1. **Start broad, then narrow:**
   ```bash
   # First, find relevant files
   rg -l "feature name" inavwiki/

   # Then search within those files with context
   rg -i "feature name" inavwiki/ -C 5
   ```

2. **Search for related terms:**
   ```bash
   # Use multiple related terms (regex OR)
   rg -i "optical flow|opflow|pmw3901" inavwiki/
   ```

3. **Limit to specific file types:**
   ```bash
   # Markdown and text files
   rg -i "keyword" inavwiki/ -g "*.{md,txt}"
   ```

### When Looking for API Documentation

```bash
# Search for function names
rg -i "function_name" inavwiki/

# Search for struct definitions
rg "struct.*name" inavwiki/

# Search for MSP commands
rg "MSP_" inavwiki/
```

## Viewing Documentation

### Quick Preview

```bash
# View file in terminal
cat inavwiki/path/to/file.md

# View with paging
less inavwiki/path/to/file.md

# View specific section
rg -A 20 "^## Section Title" inavwiki/path/to/file.md
```

### Using Claude's Read Tool

Use Claude's Read tool to view full documentation files:
```
file_path: inavwiki/path/to/file.md
```

## Example Searches

### Find GPS Configuration Docs

```bash
# Search for GPS documentation
rg -l "gps.*config" inavwiki/

# Search for GPS protocol info with context
rg -i "ublox|nmea|gps.*protocol" inavwiki/ -C 3
```

### Find Programming Documentation

```bash
# Find developer documentation
rg -l "developer|programming|api" inavwiki/

# Find build instructions with context
rg -i "build|compile|cmake" inavwiki/ -C 5
```

### Find Sensor Documentation

```bash
# Search for sensor docs
rg -l "sensor|barometer|magnetometer" inavwiki/

# Find specific sensor
rg -i "pmw3901|vl53l1x|qmc5883" inavwiki/
```

## Ripgrep Tips

1. **Smart case** - Use lowercase patterns for case-insensitive, uppercase for case-sensitive
2. **Include context** - Use `-C 3` to see surrounding lines
3. **List files only** - Use `-l` to just see which files match
4. **File type filtering** - Use `-g "*.md"` or `-t markdown`
5. **Ignore .gitignore** - Use `--no-ignore` if you need to search ignored files
6. **Count matches** - Use `-c` to count matches per file

## Resources

- **Online wiki:** https://github.com/iNavFlight/inav/wiki
- **Local copy:** `inavwiki/` directory
- **Ripgrep guide:** `rg --help` or `man rg`

---

## Related Skills

- **find-symbol** - Find function/struct definitions in code
