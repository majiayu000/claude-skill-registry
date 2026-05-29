---
name: energyplus-assistant
description: Use this skill when analyzing EnergyPlus IDF building energy models, including QA/QC validation, HVAC topology analysis, ECM testing, or running simulations. Supports fast validation without Docker (direct parsing) and comprehensive analysis with MCP tools when needed. Handles Windows path formats, environment detection, and intelligent method selection. (project)
---

# EnergyPlus Assistant

Specialized assistant for EnergyPlus building energy modeling workflows with intelligent method selection based on environment and task requirements.

## Core Capabilities

1. **Pre-Simulation QA/QC** - Fast validation using direct parsing (< 5 seconds)
2. **IDF Repair** - Automated fixing of corrupt objects, field shifts, version mismatches
3. **HVAC System Analysis** - Topology discovery and visualization
4. **ECM Testing** - Parametric energy conservation measure evaluation
5. **Environment-Aware** - Adapts to Windows/macOS, Docker available/unavailable

---

## Quick Start (Always Start Here)

### Step 1: Environment Check

```bash
# Check Docker availability
docker ps > /dev/null 2>&1 && echo "✓ Docker available" || echo "✗ Docker unavailable"

# Check Python/eppy
python -c "import eppy; print('✓ eppy available')" 2>/dev/null || echo "⚠ Need: pip install eppy"

# Verify IDF file exists
test -f "$IDF_PATH" && echo "✓ File found" || echo "✗ File not found: $IDF_PATH"
```

### Step 2: Choose Method Based on Task

| Your Task | Best Method | Time | Details |
|-----------|-------------|------|---------|
| **QA/QC validation** | Direct parsing | < 5 sec | [./direct-parsing-methods.md](./direct-parsing-methods.md) |
| **Object counts** | Direct parsing | < 5 sec | [./direct-parsing-methods.md](./direct-parsing-methods.md) |
| **Fix corrupt objects** | fix-equipment-lists.py | < 5 sec | See "IDF Repair" section below |
| **Version mismatch** | fix-equipment-lists.py | < 5 sec | Auto-updates IDF version |
| **HVAC topology** | MCP (if Docker available) | 30+ sec | [./mcp-server-usage.md](./mcp-server-usage.md) |
| **Simulations** | EnergyPlus CLI | Minutes | Native EnergyPlus installation |
| **ECM testing** | MCP or scripts | Varies | [./ecm-testing-workflows.md](./ecm-testing-workflows.md) |

**Key Decision:** For QA/QC (most common), use direct parsing—no Docker required, 10x faster.

---

## Priority Workflows

### 1. Pre-Simulation QA/QC (Most Common)

**Fast Method - Direct Parsing (< 5 seconds):**

```bash
# Install once
pip install eppy

# Run analysis
python ~/.claude/skills/energyplus-assistant/scripts/qaqc-direct.py "$IDF_PATH"
```

**What it checks:**
- Building, zones, surfaces, fenestration
- Constructions and materials
- HVAC systems (air loops, plant loops, zone equipment)
- Internal loads (people, lights, equipment)
- Simulation settings (RunPeriod, SimulationControl)
- Output variables and meters

**Output:**
- Object count summary
- Validation status (PASS/FAIL)
- Critical errors and warnings
- Recommendations for next steps

**When Docker/MCP needed instead:**
- Detailed HVAC connectivity validation
- Automated output variable discovery
- Simulation test runs
- See [./mcp-server-usage.md](./mcp-server-usage.md) for MCP workflows

**Complete documentation:** [./direct-parsing-methods.md](./direct-parsing-methods.md)

---

### 2. HVAC Topology Analysis

**When to use:**
- Understanding existing HVAC before modifications
- Troubleshooting equipment connections
- Visualizing system architecture
- Validating loop configurations

**Methods available:**
1. **MCP Tools** (if Docker available) - Most comprehensive
2. **Text pattern matching** - Quick checks without Docker
3. **IDF Editor** - Visual inspection

**Full documentation:** [./mcp-server-usage.md](./mcp-server-usage.md)

---

### 3. IDF Repair and Fixing Corrupt Objects

**When to use:**
- Fatal errors from corrupt ZoneHVAC:EquipmentList objects
- Field shifting issues (data in wrong field positions)
- IDF version mismatches between file and EnergyPlus installation
- Duplicate object errors preventing simulation

**fix-equipment-lists.py** - Automated repair tool

```bash
# Fix corrupted equipment lists + update version
python ~/.claude/skills/energyplus-assistant/scripts/fix-equipment-lists.py input.idf output.idf
```

**What it does:**
1. **Detects corruption patterns:**
   - Blank object types with present names (field shift)
   - Equipment names in numeric sequence fields
   - Non-numeric values in cooling/heating sequence fields

2. **Automatically fixes:**
   - Removes ALL corrupted equipment lists (no duplicates)
   - Reconstructs with correct field structure
   - Sets proper cooling/heating sequences (1, 2, 3...)

3. **Updates IDF version:**
   - Detects current version (e.g., 24.2)
   - Updates to match installed EnergyPlus (e.g., 25.1)
   - No separate transition tool needed

**Output:**
- Analysis report of corrupted vs clean objects
- Fixed IDF file ready for simulation
- Summary of changes made

**Philosophy:** "Let tools handle syntax, let humans handle logic"
- eppy ensures syntactically correct IDF format
- You specify the logic (what fields should contain)
- Tool guarantees proper file structure

**Example error this fixes:**
```
** Severe ** processZoneEquipmentInput: ZoneHVAC:EquipmentList = "THERMAL ZONE: CARDIO 1 EQUIPMENT LIST".
**   ~~~   ** invalid zone_equipment_cooling_sequence=[2].
**   ~~~   ** equipment sequence must be > 0 and <= number of equipments in the list.
**   ~~~   ** only 1 in the list.
**  Fatal  ** GetZoneEquipmentData: Errors found in getting Zone Equipment input.
```

**Related scripts:**
- validate-idf-fields.py (coming soon) - Pre-flight field validation
- add-outputs.py (coming soon) - Automated output variable injection

---

### 4. ECM Testing

**When to use:**
- Testing lighting upgrades
- Evaluating plug load reductions
- Infiltration reduction strategies
- Occupancy schedule changes

**Full documentation:** [./ecm-testing-workflows.md](./ecm-testing-workflows.md)

---

## Environment-Specific Guidance

### Windows Users

Docker path formats, console encoding, Git Bash considerations:
**See [./windows-setup.md](./windows-setup.md)**

Key points:
- Use forward slashes in Docker mounts: `C:/Users/...`
- Git Bash: Double slashes for workdir: `//workspace//...`
- PowerShell: Single slashes work fine
- Set UTF-8 encoding: `$env:PYTHONIOENCODING = "utf-8"`

### macOS/Linux Users

Generally straightforward:
- Docker paths use native format
- UTF-8 typically default
- Bash commands work as documented

---

## Supporting Resources

### Scripts

Located in `./scripts/`:

**Completed:**
- **qaqc-direct.py** - Fast Python-based QA/QC (no Docker, < 5 sec)
- **fix-equipment-lists.py** - Repair corrupt ZoneHVAC:EquipmentList + version update
- **validate-idf-structure.py** - Comprehensive field validation (< 10 sec)

**In Development (see [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)):**
- **add-standard-outputs.py** - Automated output variable injection (Phase 1)
- **extract-results.py** - Parse results for deliverables (Phase 1)
- **fix-node-connections.py** - Repair HVAC node connections (Phase 2)
- **fix-schedules.py** - Repair schedule references (Phase 2)
- **add-ideal-loads.py** - Replace HVAC with ideal loads (Phase 3)
- **apply-ecm-lighting.py** - LPD reduction ECM (Phase 4)
- **apply-ecm-envelope.py** - Insulation/window ECM (Phase 4)
- **compare-models.py** - Diff two IDF files (Phase 5)

**Full Development Roadmap:** [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) - Complete specifications for 17+ scripts

### Documentation

- **[./DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md)** - Complete toolkit development roadmap (17+ scripts)
- **[./scripts/README.md](./scripts/README.md)** - Script usage guide and documentation
- **[./direct-parsing-methods.md](./direct-parsing-methods.md)** - Python/Node.js QA/QC without Docker
- **[./windows-setup.md](./windows-setup.md)** - Windows-specific setup and troubleshooting
- **[./mcp-server-usage.md](./mcp-server-usage.md)** - Docker/MCP tools for complex analysis
- **[./ecm-testing-workflows.md](./ecm-testing-workflows.md)** - ECM parametric studies
- **[./SKILL_OPTIMIZATION_ANALYSIS.md](./SKILL_OPTIMIZATION_ANALYSIS.md)** - Lessons learned and optimization rationale

---

## Decision Tree

```
User Request: Analyze EnergyPlus model
    ↓
What's the primary need?
    ↓
├─ QA/QC Validation (most common)
│   ↓
│   Is Docker available?
│   ├─ YES → Still use direct parsing (faster)
│   └─ NO  → Use direct parsing (only option)
│   ↓
│   python ./scripts/qaqc-direct.py model.idf
│
├─ IDF Repair (corrupt objects)
│   ↓
│   What type of error?
│   ├─ ZoneHVAC:EquipmentList errors
│   │   └─ python ./scripts/fix-equipment-lists.py input.idf output.idf
│   ├─ Version mismatch
│   │   └─ python ./scripts/fix-equipment-lists.py input.idf output.idf (auto-updates version)
│   └─ Field validation
│       └─ python ./scripts/validate-idf-fields.py model.idf (coming soon)
│
├─ HVAC Topology Analysis
│   ↓
│   Is Docker available?
│   ├─ YES → Use MCP tools (detailed analysis)
│   └─ NO  → Use text pattern matching (basic)
│   ↓
│   See: ./mcp-server-usage.md
│
├─ Run Simulation
│   ↓
│   Is EnergyPlus installed locally?
│   ├─ YES → Use energyplus CLI (fastest)
│   └─ NO  → Use MCP if Docker available
│   ↓
│   energyplus -w weather.epw model.idf
│
└─ ECM Testing
    ↓
    See: ./ecm-testing-workflows.md
```

---

## Example Project Context

**Current Project:** Example Recreation Center Model
**Deadline:** 2025-11-27 (Pre-Thanksgiving)
**Deliverables:** EUI, GHG, Utility Cost

**Model Location:**
```
Local: C:\Users\mcoalson\Documents\WorkPath\User-Files\work-tracking\example-recreation-center\energy-model\
Container: /workspace/models/ (when using Docker)
```

**Key Files:**
- `Example_Model_v3_WaterLoop_RTUHP_DOAS_Pool/run/in.idf`
- `Example_Model_v3_WaterLoop_RTUHP_DOAS_Pool/run/in_cleaned.idf` ✓ QA/QC passed

**Recent Work:**
- ✓ QA/QC completed on in_cleaned.idf (2025-11-24)
- ✓ Model validated: 24 zones, 295 surfaces, 58 HVAC equipment
- ✓ Status: Ready for simulation

---

## Troubleshooting

### "Docker not available"
→ Use direct parsing methods (faster anyway for QA/QC)

### "MCP startup slow (30+ seconds)"
→ Use direct parsing for QA/QC, reserve MCP for complex HVAC analysis

### "Unicode/encoding errors on Windows"
→ See [./windows-setup.md](./windows-setup.md) for console encoding setup

### "Path format errors in Docker"
→ See [./windows-setup.md](./windows-setup.md) for Windows path guidance

### "eppy not installed"
```bash
pip install eppy
```

---

## Performance Expectations

| Task | Direct Parsing | MCP Tools | Native EnergyPlus |
|------|----------------|-----------|-------------------|
| QA/QC | < 5 sec | 30+ sec startup | N/A |
| Object counts | < 5 sec | 30+ sec startup | N/A |
| HVAC topology | Basic (< 5 sec) | Detailed (30+ sec) | N/A |
| 1-day simulation | N/A | Minutes | Seconds to minutes |
| Annual simulation | N/A | Hours | Hours |

**Recommendation:** Start with fast methods, escalate to slower methods only when needed.

---

## Integration with Work Command Center

This skill can be invoked from `work-command-center` when:
- User mentions "recreation center energy model"
- User requests "energy model QA/QC"
- User asks to "validate EnergyPlus model"
- User needs "HVAC topology analysis"
- User wants to "test ECM scenarios"

**Communication Style:**
- Concise and technical (Matt is an expert)
- Focus on actionable insights
- Flag errors/warnings immediately
- Provide numerical results with units
- Suggest next steps

---

## Context Awareness

This skill integrates with work-command-center session tracking:

**Check Active Context:**

```bash
node .claude/skills/work-command-center/tools/session-state.js status
```

Returns: Project name, project number, duration, and deliverables context

**Log Activity Checkpoints:**

```bash
node .claude/skills/work-command-center/tools/session-state.js checkpoint \
  --activity "energyplus-assistant: QA/QC validation complete, found 3 warnings"
```

**Signal Completion (called by WCC after skill returns):**

```bash
node .claude/skills/work-command-center/tools/session-state.js skill-complete \
  --skill-name "energyplus-assistant" \
  --summary "Model validation: 3 warnings, 0 errors. HVAC topology verified." \
  --outcome "success"
```

**Benefits:**

- WCC tracks time spent in this skill
- Session logs include skill work breakdown
- Context visible across skill transitions
- Deliverables auto-update from skill outcomes

---

## Version History

- **v1.0** (2025-11-23): Initial release - MCP-focused
- **v2.0** (2025-11-24): Optimized with direct parsing, environment detection, Windows support

**Last Updated:** 2025-11-24
**Status:** Active - Replaces `diagnosing-energy-models` skill


## Saving Next Steps

When energyplus-assistant work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "energyplus-assistant" \
  --content "## Priority Tasks
1. Complete QA/QC validation on IDF model
2. Run simulation and extract results
3. Analyze HVAC topology for ECM opportunities"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
