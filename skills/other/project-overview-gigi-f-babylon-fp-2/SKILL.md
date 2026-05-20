---
name: Project Overview
description: Get overview of the Babylon.js first-person game project structure, statistics, and health metrics. Use when the user asks about project structure, codebase stats, file counts, or wants a project summary.
---

# Project Overview

Quick overview and statistics for the babylon_fp project.

## Quick Stats

### Line count by file type
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "TypeScript files:"
find src -name "*.ts" -exec wc -l {} + | tail -1
echo -e "\nHTML files:"
find tools -name "*.html" -exec wc -l {} + | tail -1
echo -e "\nJSON data files:"
find public/data -name "*.json" -exec wc -l {} + | tail -1
echo -e "\nTest files:"
find tests -name "*.test.ts" -exec wc -l {} + | tail -1
```

### File counts
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "Source files: $(find src -name '*.ts' | wc -l)"
echo "Test files: $(find tests -name '*.test.ts' | wc -l)"
echo "Config files: $(find . -maxdepth 1 -name '*.json' -o -name '*.config.*' | wc -l)"
echo "Tools: $(find tools -name '*.html' | wc -l)"
echo "Data files: $(find public/data -name '*.json' | wc -l)"
```

## Project Structure

### Main directories
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
tree -L 2 -d src/
```

### List key systems
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Core Systems ==="
ls -1 src/systems/*.ts | sed 's/.*\///' | sed 's/.ts$//'
echo -e "\n=== Controllers ==="
ls -1 src/controllers/*.ts 2>/dev/null | sed 's/.*\///' | sed 's/.ts$//' || echo "None"
echo -e "\n=== UI Components ==="
ls -1 src/ui/*.ts 2>/dev/null | sed 's/.*\///' | sed 's/.ts$//' || echo "None"
```

## Code Health

### TypeScript compilation check
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npx tsc --noEmit 2>&1 | head -20
```

### Find TODO/FIXME comments
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== TODOs ==="
grep -r "TODO" src/ --include="*.ts" | wc -l
echo "=== FIXMEs ==="
grep -r "FIXME" src/ --include="*.ts" | wc -l
```

### List TODO items
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== TODO List ==="
grep -rn "TODO" src/ --include="*.ts" | head -10
```

## Dependencies

### Show installed packages
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Main Dependencies ==="
node -e "console.log(Object.keys(require('./package.json').dependencies || {}).join('\n'))"
echo -e "\n=== Dev Dependencies ==="
node -e "console.log(Object.keys(require('./package.json').devDependencies || {}).join('\n'))"
```

### Check for outdated packages
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm outdated
```

### Check Babylon.js version
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
npm list @babylonjs/core
```

## Data Overview

### Map data summary
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Map Data ==="
for map in public/data/maps/*.json; do
  echo "$(basename $map): $(wc -l < $map) lines"
done
```

### NPC data summary
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== NPC Data ==="
echo "NPCs: $(ls -1 public/data/npcs/*.json 2>/dev/null | wc -l)"
for npc in public/data/npcs/*.json; do
  echo "  - $(basename $npc .json)"
done
```

### Event & Investigation data
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "Events: $(ls -1 public/data/events/*.json 2>/dev/null | wc -l)"
echo "Investigations: $(ls -1 public/data/investigations/*.json 2>/dev/null | wc -l)"
```

## Tools Overview

### List available tools
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Editor Tools ==="
for tool in tools/*.html; do
  NAME=$(grep -o '<title>.*</title>' "$tool" | sed 's/<title>\(.*\)<\/title>/\1/' | head -1)
  echo "  - $(basename $tool): $NAME"
done
```

## Recent Activity

### Recent file changes (git)
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Recent Commits ==="
git log --oneline -10 2>/dev/null || echo "Not a git repository or no commits"
```

### Recently modified files
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Recently Modified (last 7 days) ==="
find src tests -name "*.ts" -mtime -7 -exec ls -lh {} \; | awk '{print $6, $7, $8, $9}'
```

## Build Info

### Check build configuration
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Vite Config ==="
ls -lh vite.config.ts
echo -e "\n=== TypeScript Config ==="
ls -lh tsconfig.json
```

### Check dist folder
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
if [ -d "dist" ]; then
  echo "Build output size: $(du -sh dist | cut -f1)"
  echo "Files in dist: $(find dist -type f | wc -l)"
else
  echo "No dist folder (run 'npm run build')"
fi
```

## Quick Health Check

Run a comprehensive health check:
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Babylon FP Project Health Check ==="
echo -e "\n1. TypeScript Compilation:"
npx tsc --noEmit && echo "✓ No errors" || echo "✗ Has errors"
echo -e "\n2. Dependencies:"
npm list --depth=0 > /dev/null 2>&1 && echo "✓ All installed" || echo "✗ Missing dependencies"
echo -e "\n3. Tests:"
npm test > /dev/null 2>&1 && echo "✓ All passing" || echo "✗ Some failing"
echo -e "\n4. Data Files:"
for f in public/data/**/*.json; do node -e "JSON.parse(require('fs').readFileSync('$f'))" 2>/dev/null || echo "✗ Invalid: $f"; done | grep -q "Invalid" && echo "✗ Invalid JSON found" || echo "✓ All valid"
```

## Recent Features & Enhancements

### Game Systems
- **Pause System**: Press 'P' to pause/resume game
  - Freezes all movement, camera control, and time progression
  - Exits pointer lock to show cursor
  - Visual pause indicator in HUD
  - Implemented in: `src/Game.ts`, `src/controllers/firstPersonController.ts`, `src/systems/dayNightCycle.ts`

- **Enhanced Map Editor** (`tools/map-editor.html`):
  - **NPC Type Modal**: On-demand dropdown for selecting NPC types (no always-visible UI clutter)
  - **Auto Schedule Editor**: Opens automatically when NPC selected/placed, closes when done
  - **Editable Waypoint Times**: Click time fields in schedule list to edit directly
  - **Import/Export**: Full map JSON import functionality with schedule preservation
  - **Click-and-Drag Painting**: Paint multiple wall/floor/window tiles by dragging
  - **Select Tool**: Click NPCs to edit schedules, default tool on load
  - **Default Player Spawn**: Auto-creates center spawn on new maps
  - **Schedule Validation**: Ensures waypoint times are sequential

### Editor Workflow Improvements
- NPC type selector only appears when placing NPCs (cleaner UI)
- Schedule editor context-aware (shows NPC name, emoji, position)
- Save & Close button for schedule editor (returns to select tool)
- JSON import reconstructs grid positions, rotations, and full NPC schedules
- Drag painting works with zoom and pan, detects grid changes smartly

### Code Organization
- Modular functions: `openScheduleEditor()`, `closeScheduleEditor()`, `placeTile()`
- Separated paintable tools (wall/floor/window) from special tools (door/spawn)
- Helper functions for time conversion: `timeStringToMinutes()`, `minutesToTimeString()`

## Project Summary

Generate a complete summary:
```bash
cd /home/gianfiorenzo/Documents/Vs\ Code/babylon_fp
echo "=== Babylon FP - First Person Game ==="
echo "Babylon.js Version: $(npm list @babylonjs/core | grep @babylonjs/core | awk '{print $2}')"
echo "Source Files: $(find src -name '*.ts' | wc -l) TypeScript files"
echo "Test Files: $(find tests -name '*.test.ts' | wc -l) test files"
echo "Total Lines: $(find src -name '*.ts' -exec cat {} + | wc -l) lines of code"
echo "Tools: Map Editor (2000+ lines), NPC Editor"
echo "Core Systems: Day/Night Cycle, NPC Scheduling, Photo System, Door System, Pause System"
echo "Controllers: First-Person Camera with enable/disable support"
echo "Data: $(find public/data -name '*.json' | wc -l) data files (NPCs, Maps, Events, Investigations)"
echo "Features: Pausable gameplay, schedule editor, map import/export, drag painting"
```
