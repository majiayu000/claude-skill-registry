---
name: example-presentation-automation
description: Update the weekly rolling presentation with JIRA progress data. Use this skill when asked to "update the presentation", "add weekly slides", "create presentation slides", or prepare slides for team meetings. Covers Google Slides API operations, template slide IDs, proper slide duplication workflow, and content formatting guidelines for the Orient Task Force rolling presentation.
---

# Weekly Presentation Updates

## Presentation Details

- **Name**: Franklin - Orient Task Force - Rolling Presentation
- **ID**: 1j4UMDKszRU-r29Kt8w3NRP3t5ocYCrmz99m23cAMiuM

## Template Slide IDs

| Template    | ID                  | Purpose                    |
| ----------- | ------------------- | -------------------------- |
| Date Header | `g3ada04fdc99_0_0`  | "Dec 8th 2025" style       |
| Agenda      | `g3ada04fdc99_0_5`  | "Today's Agenda"           |
| Content     | `g3ada04fdc99_0_20` | "TF - Orient" main content |

## Standard Update Process

### 1. Gather JIRA Data

Query JIRA using JQL: `project = YOUR_PROJECT AND component = "YOUR_COMPONENT"`

- New tickets created (last 7 days)
- Tickets completed (status changed to Done)
- Tickets in progress
- Any blockers

### 2. Create Slides (in order)

**Date Header** (index 1):

```
Template: g3ada04fdc99_0_0
Replacement: "Dec 8th 2025" → "Dec [Current Date] 2025"
```

**Agenda/Summary** (index 2):

```
Template: g3ada04fdc99_0_5
Content: High-level summary with key metrics
```

**Content Slides** (index 3+):

```
Template: g3ada04fdc99_0_20
Break content across multiple slides if needed
```

## Critical Rules

❌ **DO NOT** paste content directly onto template slides
❌ **DO NOT** modify original template slides (g3ada04fdc99\_\*)
❌ **DO NOT** create overly long slides
❌ **DO NOT** forget ticket IDs

✅ **DO** always duplicate template slides first
✅ **DO** insert slides in chronological order (newest at top)
✅ **DO** break content across multiple slides if needed
✅ **DO** include ticket IDs in format (PROJ-XXXXX)

## Formatting Guidelines

**Text Formatting:**

- Use emojis sparingly for section headers (🎯 🤖 📝 📚 🔧 📊)
- Keep bullet points concise
- Include ticket IDs in format (PROJ-XXXXX)
- Mark priority items with ⭐
- Include assignee names

**Content Organization:**

- Group related tickets by Epic
- Maximum 5-7 items per slide
- Break into multiple slides if needed

## ⚠️ API Formatting Limitations

The Google Slides text replacement API (`replaceAllText`) has important limitations:

### What the API CAN'T do:

- ❌ Apply **bold**, _italic_, or other text styling
- ❌ Create nested/indented bullet lists
- ❌ Change font sizes or colors
- ❌ Control bullet levels (all replaced text inherits the original bullet level)

### What the API CAN do:

- ✅ Replace text content while preserving the original formatting
- ✅ Insert newlines (but each line becomes a separate bullet if in a bulleted text box)

### Formatting Workarounds

**Problem**: Multi-line content in bullet lists creates flat bullets (not nested)

**Solution**: Use single-line format with em-dash separators:

```
❌ BAD - Creates separate bullets:
Initiative Name
Description of the initiative

✅ GOOD - Single line with em-dash:
Initiative Name — Description of the initiative
```

**Problem**: Can't make headers bold

**Solution**: Use visual separators and capitalization:

- Use "—" (em-dash) to separate title from description
- Use ALL CAPS for emphasis (sparingly)
- Use emoji prefixes for visual distinction: "🎯 Initiative Name — description"

### Example Initiative Formatting

```
// DON'T do this (creates 6 separate bullets with empty lines):
Initiatives

Agent Observability Dashboard
Track agent actions and costs

Build Your Own Agent Framework
Template and toolkit for teams

// DO this instead (creates 3 clean bullets, no empty lines):
Initiatives
Agent Observability Dashboard — Track agent actions and costs
Build Your Own Agent Framework — Template and toolkit for teams
```

**Key Rule**: Use SINGLE newlines (`\n`) between items, NOT double newlines (`\n\n`). Double newlines create empty bullet points.

### When Rich Formatting is Required

If you need bold text, nested bullets, or other rich formatting:

1. The agent should inform the user about the limitation
2. User must manually edit the slide in Google Slides UI
3. Consider using template slides with pre-formatted placeholders

## MCP Tools

- `ai_first_slides_get_presentation` - Get presentation metadata
- `ai_first_slides_get_slide` - Get specific slide content
- `ai_first_slides_duplicate_template` - **Use this to create slides**
- `ai_first_slides_update_text` - Update text globally
- `ai_first_slides_update_slide_text` - Update text on specific slide
- `ai_first_slides_delete_slide` - Delete a slide
- `ai_first_slides_update_weekly` - Automated weekly update

## Example Workflow

```
1. npm run workflow:end-week (or query JIRA data)
2. Duplicate date header → insert at index 1
3. Duplicate agenda → insert at index 2
4. Duplicate content template(s) → insert at index 3+
5. Apply replacements to duplicated slides
6. Verify slides look correct
```

## Slide Structure Example

```
Index 0: Title slide (existing)
Index 1: "Dec 9th 2025" (duplicated)
Index 2: "This Week's Progress" (duplicated)
Index 3: "TF - Orient" - Epics (duplicated)
Index 4: "TF - Orient (Continued)" - Skills (duplicated)
Index 5: Previous week slides continue...
```
