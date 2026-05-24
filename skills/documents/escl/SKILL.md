---
name: escl-generator
description: Convert complete electrical schematic PDFs to ESCL (Electrical Schematic Context Language) format with batch processing and pause/continue support. Use when user uploads a multi-page electrical schematic PDF and wants it converted to structured ESCL text format.
---

# ESCL Generator v2

Convert multi-page electrical schematic PDFs to ESCL format with batch processing support.

## Quick Start

1. User provides PDF path
2. Agent creates project directory, extracts all pages as images
3. Agent generates ESCL page by page (can pause/continue anytime)
4. Agent consolidates fragments into master ESCL file

## Project Structure

```
projects/
  <project_name>/
    images/
      page_001.png
      page_002.png
      ...
    fragments/
      page_001.escl
      page_002.escl
      ...
    state.json
    <project_name>.escl    (master file)
```

## State File (state.json)

```json
{
  "project_name": "example",
  "source_pdf": "/path/to/schematic.pdf",
  "created_at": "2026-01-24T10:30:00Z",
  "total_pages": 45,
  "dpi": 150,
  "phases": {
    "extraction": {
      "status": "pending|in_progress|completed",
      "completed_pages": []
    },
    "generation": {
      "status": "pending|in_progress|completed",
      "completed_pages": [],
      "current_page": null
    },
    "consolidation": {
      "status": "pending|completed"
    }
  },
  "inventory": {
    "components": {},
    "potentials": {},
    "cables": {},
    "cross_refs": {}
  }
}
```

---

## Phase 1: Project Setup

**When:** User provides a PDF path to convert

**Actions:**
1. Extract project name from PDF filename (remove extension, sanitize)
2. Create directory: `projects/<project_name>/`
3. Create subdirectories: `images/`, `fragments/`
4. Initialize `state.json`:
   ```bash
   # Count pages first
   node extract-pdf.js <pdf> --info-only
   ```
5. Confirm with user before proceeding

**State after:** `extraction.status = "pending"`

---

## Phase 2: Image Extraction

**When:** Project exists, `extraction.status != "completed"`

**Actions:**
1. Run the extraction script:
   ```bash
   node extract-pdf.js "<source_pdf>" "projects/<name>/images" --dpi 150
   ```
2. Script outputs JSON progress to stdout
3. Update `state.json` after extraction completes
4. Verify all images were created

**Resumable:** If interrupted, re-run will regenerate missing pages.

**State after:** `extraction.status = "completed"`, `extraction.completed_pages = [1..N]`

---

## Phase 3: ESCL Generation (Page by Page)

**When:** `extraction.status = "completed"`, `generation.status != "completed"`

**Actions for each unprocessed page:**

1. Read `state.json` to find next page to process
2. Read the page image: `projects/<name>/images/page_XXX.png`
3. Analyze the image:
   - Identify page type (power_distribution, motor_drive, plc_io, safety, asi, control, terminals)
   - Skip if TOC, cover, or non-schematic page
4. Extract components, potentials, cables, cross-references
5. Generate ESCL fragment following syntax rules
6. Save as: `projects/<name>/fragments/page_XXX.escl`
7. Update `state.json`:
   - Add page to `generation.completed_pages`
   - Update `inventory` with discovered components/potentials
   - Set `generation.current_page` to next page

**Batch Mode:** Process N pages at a time, then pause for user confirmation.

**Resumable:** Can stop anytime. On resume, continues from last incomplete page.

**State after each page:** `generation.completed_pages` grows, `inventory` accumulates

---

## Phase 4: Consolidation

**When:** `generation.status = "completed"`, `consolidation.status = "pending"`

**Actions:**
1. Read all fragment files in order
2. Build master ESCL file:
   - Project metadata header
   - Potentials section (deduplicated, merged from all pages)
   - Components grouped by page
   - Cables section
   - Cross-reference index
3. Save as: `projects/<name>/<project_name>.escl`
4. Update `state.json`: `consolidation.status = "completed"`

**State after:** Project complete, master ESCL file ready

---

## Resume/Continue Commands

To check project status:
```
Read state.json and report:
- Current phase
- Pages extracted: X/Y
- Pages generated: X/Y
- Next action needed
```

To continue an existing project:
```
1. Read state.json
2. Determine current phase
3. Continue from where it stopped
```

---

## ESCL Syntax Quick Reference

### Locations
```
=section/page.column    # Full ref: =20/5.3
/page.column            # Local ref: /7.1
```

### Components
```escl
<type> <tag> "description" {
  attribute: value
  block { nested: value }
}
```

Types: `motor`, `vfd`, `contactor`, `breaker`, `relay`, `safety_relay`, `plc_module`, `asi_master`, `asi_slave`, `power_supply`, `reactor`, `transformer`, `sensor`, `fuse`, `safety_plc`, `valve`, `resistor`

### Potentials
```escl
@potential NAME {
  description: "text"
  type: AC|DC
  voltage: 24V
  origin: -component =location
  consumers: [-comp1, -comp2]
}
```

### Cables
```escl
@cable -TAG {
  type: "ÖLFLEX 110"
  spec: "4x2.5mm²"
  length: 21m
  from: -component =location
  to: -component =location
}
```

### Connections
```
<- source       # comes from
-> destination  # goes to
<-> [refs]      # appears in multiple places
```

### Contacts
```
13-14.NO    # Normally open
21-22.NC    # Normally closed
1-2, 3-4    # Main contacts
```

## Common Potential Names

| Name | Type | Description |
|------|------|-------------|
| L1, L2, L3 | AC 400V | Three-phase |
| L500 | DC 24V | Before E-Stop |
| L501 | DC 0V | Reference |
| L502 | DC 24V | After E-Stop |
| L504 | DC 24V | Drives enabled |
| L200 | AC 230V | After E-Stop |
| L218 | AC 230V | Before E-Stop |
| PE | - | Protective Earth |

## Fragment File Format

Each `page_XXX.escl` fragment:

```escl
# ============================================================
# Page XXX - [Title/Description]
# Type: [page_type]
# Section: =[section]
# ============================================================

# Components on this page
breaker -Q5 "Motorschutzschalter" {
  rating: 16A
  location: =9/3.2
}

motor -M7 "Förderband Antrieb" {
  power: 7.5kW
  fed_by: -U1 =9/4.5
}

# Potentials discovered (for inventory)
# @potential_ref L500 [used on this page]
# @potential_ref L502 [used on this page]

# Cross-references from this page
# -K1M -> =7/1.4
# -U1 -> =26/1.3
```

## Master File Format

Final `<project>.escl`:

```escl
# ============================================================
# ESCL Document
# Generated from: [filename]
# Pages processed: [X] of [Y]
# Generated: [timestamp]
# ============================================================

@project "[extracted or Unknown]"
@customer "[extracted or Unknown]"
@drawing "[extracted or Unknown]"

# ============================================================
# POTENTIALS
# ============================================================

@potential L500 {
  description: "24VDC vor Not-Aus"
  type: DC
  voltage: 24V
  origin: -G1 =3/4.2
  pages: [3, 4, 7, 9, 20]
  consumers: [-K1, -K2, -S1]
}

# ============================================================
# COMPONENTS BY PAGE
# ============================================================

# ------------------------------------------------------------
# Page 3 - Einspeisung (power_distribution)
# Section: =1
# ------------------------------------------------------------

[components from page 3]

# ------------------------------------------------------------
# Page 9 - Frequenzumrichter (motor_drive)
# Section: =9
# ------------------------------------------------------------

[components from page 9]

# ============================================================
# CABLES
# ============================================================

@cable -W7 {
  type: "ÖLFLEX 110 CY"
  spec: "4x2.5mm²"
  length: 21m
  from: -U1 =9/4.5
  to: -M7 +ANL
}

# ============================================================
# CROSS-REFERENCE INDEX
# ============================================================

# -K1M: defined =7/1.4, referenced =4/1.6, =9/3.2, =20/5.0
# -U1: defined =9/4.3, referenced =26/1.3, =33/1.2
```

## Important Rules

1. **Preserve exact tags** - Use -M7 not -M07, exact spelling from schematic
2. **Track all cross-references** - Every =x/y.z location must be noted
3. **Don't invent data** - Only extract what's visible on the page
4. **Mark uncertainties** - Use `# UNCLEAR:` comments when needed
5. **Skip non-schematic pages** - TOC, cover sheets, parts lists (mark as skipped in state)
6. **Consolidate potentials** - Define once in master, track pages where used
7. **Update inventory continuously** - Each page adds to the running inventory
8. **Save state after each page** - Enables resume capability
