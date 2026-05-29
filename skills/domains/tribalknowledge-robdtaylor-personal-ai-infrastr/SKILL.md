---
name: Tribalknowledge
description: Capture and preserve machinist expertise before it retires. Structured knowledge extraction for CNC operations, troubleshooting, and process optimization. USE WHEN user says 'capture knowledge', 'document expertise', 'what does [name] know', 'troubleshooting tips', 'how do we handle', 'interview machinist', or 'tribal knowledge'.
---

# TribalKnowledge - Expertise Preservation System

**Purpose:** Extract, structure, and preserve the hard-won knowledge in your machinists' heads before they retire or leave.

## The Problem

- Average machinist age: 55+
- Years to develop expertise: 10-20
- Time to capture it: Now
- Cost of lost knowledge: Scrap, rework, downtime, lost customers

## When to Activate

- "Capture what Dave knows about the Swiss machines"
- "Document troubleshooting for [problem]"
- "Interview template for machinist knowledge"
- "What tips do we have for [operation/material/machine]?"
- "Add tribal knowledge entry"
- Before someone retires or leaves

---

## Knowledge Categories

### 1. Machine-Specific Knowledge

#### DMG MORI Mills (NMV3000, DMU50, NHX500)
```yaml
Category: Machine Tips
Machine: [specific model]
Topics:
  - Warm-up procedures
  - Spindle characteristics
  - Known quirks/issues
  - Best practices for accuracy
  - Pallet system tips
  - CELOS shortcuts
  - Probe calibration secrets
  - Coolant management
```

#### DMG MORI Lathes (NLX2500, ALX2000)
```yaml
Category: Machine Tips
Machine: [specific model]
Topics:
  - Chuck pressure settings by material
  - Sub-spindle synchronization
  - Live tooling alignment
  - Bar feeder setup tricks
  - Tailstock usage
  - Steady rest positioning
  - Tool turret indexing issues
```

#### HARDINGE
```yaml
Category: Machine Tips
Machine: Hardinge Twin Spindle
Topics:
  - Achieving ±0.003mm consistently
  - Temperature compensation
  - Collet selection
  - Transfer accuracy
  - Spindle warm-up ritual
```

#### CITIZEN Swiss
```yaml
Category: Machine Tips
Machine: [Laser Head / LFV]
Topics:
  - Guide bushing selection and setup
  - Oil viscosity effects
  - LFV parameter tuning
  - Gang tool alignment
  - Bar stock quality issues
  - Chip evacuation
  - Sub-spindle pickup
```

#### MITSUBISHI EDM
```yaml
Category: Machine Tips
Machine: [Wire / Spark]
Topics:
  - Wire threading tricks
  - Cutting hardened materials
  - Surface finish optimization
  - Electrode wear compensation
  - Flushing strategies
  - Dielectric maintenance
```

#### Haas
```yaml
Category: Machine Tips
Machine: [Mini Mill / Tool Room Lathe]
Topics:
  - Quick setup tricks
  - Vice alignment
  - Tool length shortcuts
  - When to use vs. production machines
```

---

### 2. Material-Specific Knowledge

```yaml
Category: Material Tips
Material: [e.g., 316 Stainless Steel]
Properties:
  - Machinability notes
  - Work hardening behavior
  - Chip formation
  - Heat sensitivity
Recommended:
  - Cutting speeds
  - Feed rates
  - Depth of cut limits
  - Tool grades
  - Coolant type
Warnings:
  - Common failures
  - Things to avoid
Machine_Specific:
  - Best machine for this material
  - Special settings
```

#### Common Materials at MNMUK
- Aluminium (6061, 7075, 2024)
- Stainless (303, 304, 316, 17-4PH)
- Steel (4140, 4340, 1018, 1045)
- Tool Steel (D2, H13, S7, A2)
- Titanium (Ti-6Al-4V, CP Ti)
- Inconel (718, 625)
- Brass/Bronze
- Plastics (Delrin, PEEK, Nylon)

---

### 3. Operation-Specific Knowledge

```yaml
Category: Operation Tips
Operation: [e.g., Thread Milling]
Applicable_Machines:
  - List of machines
Setup:
  - Key setup considerations
Parameters:
  - Recommended starting points
  - Adjustment guidelines
Quality:
  - How to verify
  - Common issues
Troubleshooting:
  - Problem → Solution pairs
```

#### Key Operations
- OD Turning (rough/finish)
- ID Boring
- Threading (single-point, thread mill, tapping)
- Drilling (standard, peck, gun)
- Face milling
- Pocket milling
- Contouring
- 5-axis simultaneous
- Wire EDM profiling
- Spark EDM cavities
- Swiss sliding head turning
- Part-off operations
- Knurling
- Grooving

---

### 4. Troubleshooting Knowledge

```yaml
Category: Troubleshooting
Problem: [Clear description of symptom]
Symptoms:
  - What operator sees/hears/measures
Possible_Causes:
  - Cause 1
  - Cause 2
  - Cause 3
Diagnosis:
  - How to identify root cause
Solutions:
  - Solution for each cause
Prevention:
  - How to avoid in future
Machine_Specific: [if applicable]
Added_By: [Name]
Date: [YYYY-MM-DD]
```

#### Common Problem Categories
- Dimensional issues (oversize, undersize, taper)
- Surface finish problems
- Tool wear/breakage
- Chatter/vibration
- Chip control issues
- Machine alarms
- Coolant problems
- Workholding failures

---

### 5. Setup Secrets

```yaml
Category: Setup Secret
Title: [Descriptive title]
Applies_To:
  - Machine(s)
  - Operation(s)
  - Part type(s)
The_Secret:
  - What to do (step by step)
Why_It_Works:
  - Explanation
Time_Saved: [estimate]
Discovered_By: [Name]
Date: [YYYY-MM-DD]
```

---

### 6. Customer/Part-Specific Knowledge

```yaml
Category: Customer Knowledge
Customer: [Name]
Part_Numbers:
  - List of parts
Special_Requirements:
  - Quality expectations
  - Packaging
  - Documentation
  - Certifications
History:
  - Past issues
  - What worked
  - What to avoid
Key_Contacts:
  - Name, role, preferences
```

---

## Knowledge Capture Templates

### Quick Capture (5 minutes)

Use this for capturing knowledge on-the-fly:

```markdown
## Quick Tip

**Date:** YYYY-MM-DD
**From:** [Name]
**Category:** [ ] Machine [ ] Material [ ] Operation [ ] Troubleshooting [ ] Setup
**Machine:** [if applicable]
**Material:** [if applicable]

### The Situation
[When does this apply?]

### The Tip
[What's the knowledge?]

### Why It Matters
[What happens if you don't know this?]
```

### Structured Interview (30-60 minutes)

Use this for deep knowledge extraction sessions:

```markdown
# Knowledge Capture Session

**Date:** YYYY-MM-DD
**Expert:** [Name]
**Interviewer:** [Name]
**Years Experience:**
**Specialty Areas:**

---

## Opening Questions

1. What machine(s) do you know best?
2. What's the trickiest material you work with regularly?
3. What job are you most proud of getting right?

---

## Machine Deep-Dive: [Machine Name]

### Setup
- What's the first thing you do when setting up a new job?
- What do most people forget or skip?
- What's your warm-up routine?

### Running
- How do you know when something's about to go wrong?
- What sounds/vibrations do you listen for?
- What do you check during a long run?

### Troubleshooting
- What's the most common problem on this machine?
- Walk me through your diagnosis process
- What's a problem that looks like X but is actually Y?

### Tips
- If you could tell a new operator one thing about this machine?
- What took you years to figure out?
- What does the manual not tell you?

---

## Material Deep-Dive: [Material]

- What's different about machining this vs. mild steel?
- What tool grades work best?
- What feeds/speeds do you actually use (vs. book values)?
- How do you handle chip control?
- What coolant settings?
- What failures have you seen?

---

## Operation Deep-Dive: [Operation]

- Walk me through your approach
- What's the critical step most people rush?
- How do you verify quality?
- What's your backup plan when it's not working?

---

## Problem Scenarios

"What do you do when..."

1. [Specific problem 1]
2. [Specific problem 2]
3. [Specific problem 3]

---

## The Question

"If you were retiring tomorrow and could only pass on three things, what would they be?"

1.
2.
3.

---

## Follow-Up Items
- [ ] Item to clarify
- [ ] Documentation to create
- [ ] Demonstration to observe
```

### Exit Interview Checklist

When someone is leaving, capture:

```markdown
# Exit Knowledge Capture: [Name]

**Last Day:** YYYY-MM-DD
**Years at MNMUK:**
**Primary Machines:**

## Critical Knowledge Areas

### Must Capture Before They Leave
- [ ] [Specific knowledge item 1]
- [ ] [Specific knowledge item 2]
- [ ] [Specific knowledge item 3]

### Jobs Only They Know How to Run
| Part Number | Customer | What's Special |
|-------------|----------|----------------|
| | | |

### Relationships
- Key customer contacts they manage
- Supplier relationships
- Internal people they mentor

### Undocumented Processes
- Things they do that aren't in any setup sheet
- Workarounds they've developed
- Calibration routines they follow

### Scheduled Sessions
| Date | Topic | Duration | Captured |
|------|-------|----------|----------|
| | | | [ ] |
```

---

## Knowledge Storage Format

Store captured knowledge in: `~/.claude/skills/TribalKnowledge/knowledge/`

### File Naming Convention
```
{category}_{machine/material}_{topic}_{date}.md

Examples:
- troubleshooting_nlx2500_chatter_2024-01-15.md
- material_316ss_swiss_tips_2024-01-10.md
- setup_nvm3000_pallet_alignment_2024-01-08.md
- customer_acme_threading_specs_2024-01-05.md
```

### Searchable Tags
Each entry should include:
```yaml
tags:
  - machine:[machine_name]
  - material:[material]
  - operation:[operation]
  - problem:[problem_type]
  - expert:[person_name]
  - confidence:[high/medium/low]
```

---

## Integration Points

### → CNCSetup Skill
Knowledge entries auto-populate "Tips" sections in setup sheets:
- Machine-specific tips for that machine's template
- Material tips when material is specified
- Operation tips for relevant operations

### → PlantCapability Skill
Material knowledge informs machine selection:
- "316SS? Swiss machines with LFV work best"
- "Inconel? Consider EDM for complex features"

### → AutomotiveManufacturing Skill
Tribal knowledge feeds into:
- Work instruction quality notes
- Control plan special considerations
- Training materials

---

## Quick Reference: Interview Questions

### For Any Machine
1. What's the first thing you check?
2. What sound tells you something's wrong?
3. What does everyone get wrong at first?
4. What's not in the manual?

### For Any Material
1. What's different about this vs. steel?
2. What tool coating works?
3. What coolant settings?
4. How do you get good chips?

### For Any Problem
1. What does it look like when this happens?
2. What causes it?
3. How do you diagnose it?
4. How do you fix it?
5. How do you prevent it?

---

## Knowledge Capture Priorities

### Urgent (Capture Now)
- Anyone over 60 or discussing retirement
- Single points of failure (only one person knows)
- High-value/high-complexity jobs
- Customer-specific requirements

### Important (Schedule Sessions)
- Machine specialists for each platform
- Material experts (exotic alloys, plastics)
- Quality/inspection expertise
- Tooling and workholding knowledge

### Ongoing (Continuous Capture)
- Quick tips as they arise
- Problem resolutions
- New discoveries
- Process improvements

---

## Example Entries

### Example: Troubleshooting Entry

```markdown
# Chatter on NLX2500 Finishing Passes

**Category:** Troubleshooting
**Machine:** DMG MORI NLX2500
**Added By:** Dave Smith
**Date:** 2024-01-15
**Confidence:** High

## Problem
Chatter marks appearing on OD finish passes, especially on parts >150mm diameter.

## Symptoms
- Visible pattern on surface (typically 0.8-1.2mm pitch)
- Audible high-frequency noise
- Inconsistent surface finish (Ra varying)

## Causes
1. **Tool overhang too long** (most common)
2. Worn insert edge
3. Incorrect nose radius for DOC
4. Part not rigid in chuck
5. Coolant pressure inconsistent

## Diagnosis
1. Check tool stickout - should be <4x shank diameter
2. Inspect insert under magnification
3. Verify nose radius vs. programmed DOC
4. Check chuck pressure and jaw contact
5. Monitor coolant flow during cut

## Solutions
1. Reduce overhang or use larger boring bar
2. Replace insert
3. Reduce DOC or change nose radius
4. Increase chuck pressure, check jaw contact area
5. Adjust coolant pump, check filters

## Prevention
- Standard: Max 3x overhang for finishing
- Log insert usage, change proactively
- Match nose radius to DOC (rule: DOC < 2/3 nose radius)

tags:
  - machine:nlx2500
  - operation:od-turning
  - problem:chatter
  - expert:dave-smith
  - confidence:high
```

### Example: Material Entry

```markdown
# 316 Stainless Steel - Swiss Machining Tips

**Category:** Material Tips
**Material:** 316 Stainless Steel
**Machine:** CITIZEN Swiss (both models)
**Added By:** Mike Johnson
**Date:** 2024-01-12
**Confidence:** High

## Material Behavior
- Work hardens quickly - don't dwell or rub
- Gummy chips, wants to weld to tool
- Heat builds up fast, limited escape path in Swiss

## Recommended Parameters (Starting Points)
| Operation | Speed (m/min) | Feed (mm/rev) | Notes |
|-----------|---------------|---------------|-------|
| OD Rough | 80-100 | 0.08-0.12 | Stay aggressive |
| OD Finish | 120-150 | 0.04-0.06 | Sharp insert critical |
| Drilling | 60-80 | 0.05-0.08 | Peck every 1xD |
| Threading | 40-60 | Per pitch | Single-point preferred |

## Tool Recommendations
- **Insert grade:** PVD coated carbide (avoid CVD - too hot)
- **Geometry:** Sharp, positive rake
- **Coating:** TiAlN or AlTiN
- **Replace at:** First sign of built-up edge, don't push it

## LFV Settings (Game Changer)
- **Use LFV:** YES - makes 316 much easier
- **Frequency:** 10-15 Hz
- **Amplitude:** 0.05-0.1mm
- **Result:** Chips break into small segments, no bird nests

## Coolant
- High-pressure oil essential (min 50 bar)
- Keep oil clean - 316 swarf is abrasive
- Check oil concentration weekly

## Common Failures
1. **Built-up edge** → Increase speed, sharper insert
2. **Work hardening** → Don't make light passes, stay aggressive
3. **Stringy chips** → Enable LFV, adjust feed
4. **Tool welding** → Better coating, more coolant

## Tips from the Floor
- "First pass has to cut, not rub. I start heavier than the book says."
- "When the sound changes, the edge is going. Don't wait."
- "LFV on this machine is the best thing ever for 316."

tags:
  - material:316ss
  - machine:citizen-swiss
  - operation:turning
  - expert:mike-johnson
  - confidence:high
```

---

## Commands

- `"Capture knowledge about [topic]"` → Start structured entry
- `"Interview template for [person/topic]"` → Generate interview guide
- `"What do we know about [machine/material/problem]?"` → Search knowledge base
- `"Add troubleshooting entry for [problem]"` → Create troubleshooting record
- `"Exit interview checklist for [name]"` → Generate capture checklist
