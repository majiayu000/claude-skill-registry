---
name: ic-generate
description: Generate IC10 code from natural language descriptions. Use when user wants to create new IC10 code, asks for automation scripts, or needs IC10 implementation for devices like vents, furnaces, sensors, or any Stationeers automation.
---

# IC10 Code Generation (Curation-First)

Find existing IC10 resources first, generate custom code only when needed.

## Workflow

### 1. Curation Phase (Primary)

Use Task tool to spawn:
- `resource-curator` - Search external sources for existing solutions

### 2. Evaluation Phase

Review curator results:
- **Found good resources**: Present guide and ask if user wants custom code
- **Found partial matches**: Present options, offer to generate adapted version
- **Nothing found**: Proceed to generation

### 3. Research Phase (If Generating)

If user wants custom code OR nothing found, spawn in parallel:
- `instruction-researcher` - Find relevant IC10 instructions
- `device-researcher` - Find device logic types
- `pattern-finder` - Find local patterns to build from

### 4. Generation Phase (If Needed)

Use Task tool to spawn:
- `code-generator` - Generate IC10 code from requirements + research

### 5. Documentation Phase

Use Task tool to spawn:
- `code-documenter` - Add proper documentation

## Decision Flow

```
User Request
    |
    v
resource-curator -----> Guide created in guides/
    |
    v
Found resources?
    |
    +-- YES --> Present top resources
    |           Ask: "Want custom code?"
    |               |
    |               +-- NO --> Done
    |               |
    |               +-- YES --+
    |                         |
    +-- NO -------------------+
                              |
                              v
                      Research Phase
                      (parallel agents)
                              |
                              v
                      code-generator
                              |
                              v
                      code-documenter
```

## Instructions

When the user asks to generate IC10 code:

1. **Check for bypass phrases** - If user says "generate new", "write fresh", "create from scratch", or "don't search", skip to step 4.

2. **First, curate external resources**:
   - Launch `resource-curator` with the topic
   - Wait for results

3. **If resources found**:
   - Present top 3-5 resources with summaries
   - Note the guide location: `guides/[topic]-resources.md`
   - Ask: "I found these existing solutions. Would you like me to generate custom code instead?"
   - If user says no, done
   - If user says yes, continue to step 4

4. **If user wants custom code** (or nothing found, or bypass):
   - Launch research agents in PARALLEL:
     - `instruction-researcher`
     - `device-researcher`
     - `pattern-finder`

5. **Generate code**:
   - Launch `code-generator` with research findings

6. **Document code**:
   - Launch `code-documenter`

7. **Present final code** with:
   - Summary of what it does
   - Device setup requirements
   - Customization points
   - Link to resources guide (if one was created)

## Example Triggers

- "Create IC10 code for..." -> Curate first, then offer generation
- "Write a script that..." -> Curate first, then offer generation
- "Generate new code for..." -> Skip curation, go straight to generation
- "Write fresh IC10 for..." -> Skip curation, go straight to generation

## Bypass Curation

User can skip curation with explicit phrases:
- "Generate new code for..."
- "Write fresh code..."
- "Create from scratch..."
- "Don't search, just create..."
- "I want original code for..."

## Example Response After Curation

```
## Found Resources for "solar tracking"

I searched external sources and found 6 relevant resources.

### Top Matches

1. **jhillacre/solar-tracking.ic10** - Dual-axis tracking with efficiency optimization
   https://github.com/jhillacre/stationeers-scripts/blob/main/solar-tracking.ic10

2. **Wiki: Solar Panel Automation** - Basic single-axis tracking tutorial
   https://stationeers-wiki.com/Solar_Panel

3. **Reddit: Advanced Solar Array** - Multi-panel coordination script
   https://reddit.com/r/stationeers/...

Full guide saved to: `guides/solar-tracking-resources.md`

Would you like me to generate custom code instead, or would one of these work for your needs?
```
