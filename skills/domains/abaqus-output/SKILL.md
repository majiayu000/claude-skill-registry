---
name: abaqus-output
description: Configure output requests - field outputs, history outputs. Use when user asks what results to save, output variables, reduce output file size, or history output.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Output Skill

Configure what results to save from Abaqus analyses. Controls field outputs (full-field data for contour plots) and history outputs (time series at specific points).

## When to Use This Skill

**Route here when user mentions:**
- "What results should I save?" / "Output variables"
- "Track displacement over time" / "History output"
- "ODB file too large" / "Reduce output"
- "Monitor a specific node"

**Route elsewhere:**
- Extracting/reading results from ODB → `/abaqus-odb`
- Running the analysis → `/abaqus-job`

## Key Decisions

### 1. Field vs History Output

| Type | Use For | Data Scope |
|------|---------|------------|
| Field Output | Contour plots, full-field visualization | All nodes/elements |
| History Output | Time series plots, monitoring | Specific points/regions |

### 2. Common Output Variables

| Variable | Description |
|----------|-------------|
| S | Stress tensor (includes Mises) |
| U | Displacement |
| RF | Reaction forces |
| E | Total strain |
| PE, PEEQ | Plastic strain |
| V, A | Velocity, acceleration (dynamic) |
| NT, HFL | Temperature, heat flux (thermal) |
| CSTRESS, CDISP | Contact stress/displacement |

### 3. Analysis-Specific Recommendations

| Analysis Type | Essential Variables |
|---------------|---------------------|
| Static | S, U, RF |
| Dynamic | S, U, V, A, RF, ENER |
| Thermal | NT, HFL, RFL |
| Contact | CSTRESS, CDISP, COPEN |
| Plastic | S, PE, PEEQ |

### 4. Output Frequency

| Scenario | Setting | Effect |
|----------|---------|--------|
| Full detail | frequency=1 | Every increment (large files) |
| Balanced | frequency=5-10 | Every N increments |
| Space-saving | numIntervals=20 | Fixed number of frames |

## What to Ask User

If unclear, ask:
1. **What results do you need?** Stress, displacement, reaction forces?
2. **Track a specific point over time?** → Need history output
3. **Large model or long analysis?** → May need reduced frequency

## Workflow: Configuring Output

### Step 1: Identify Needed Variables
Based on analysis type: Static needs S, U, RF minimum. Dynamic adds V, A, energy.

### Step 2: Create Field Output Request
Required: Step name + variables tuple. Optional: frequency, region.

### Step 3: Create History Output (if needed)
For time-series: Create node set at location, then HistoryOutputRequest with that region. Use component variables (U1, U2, U3).

### Step 4: Manage File Size (large models)
Options: Reduce frequency, use numIntervals, limit variables, output to specific regions only.

## Validation Checklist

- [ ] Field output covers essential variables (S, U, RF)
- [ ] History output region/set exists before referencing
- [ ] Frequency appropriate for analysis length
- [ ] Contact analysis has contact-specific outputs

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Variable not available" | Wrong element/analysis type | Check compatibility |
| ODB file too large | Too much output | Reduce frequency or variables |
| No history data | Bad region spec | Verify set exists |

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
