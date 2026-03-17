---
name: customize-templates
context: fork
description: Manage custom template overrides for vault skills
model: opus
---

# /customize-templates

Manage custom template overrides for vault skills. Copies default templates to `Templates/Custom/` where they can be modified without touching the original.

## Usage

```
/customize-templates                        # List all templates and override status
/customize-templates <skill-name>           # Copy default template to Custom/ for editing
/customize-templates reset <skill-name>     # Remove custom template (revert to default)
/customize-templates diff <skill-name>      # Show differences between custom and default
```

## Examples

```
/customize-templates                        # Show which skills have templates and which are overridden
/customize-templates adr                    # Copy Templates/ADR.md to Templates/Custom/adr-template.md
/customize-templates meeting                # Copy Templates/Meeting.md to Templates/Custom/meeting-template.md
/customize-templates diff adr              # Show what changed in the custom ADR template
/customize-templates reset meeting         # Delete custom meeting template, revert to default
```

## Skill-to-Template Mapping

| Skill | Default Template | Custom Override Path |
|-------|-----------------|---------------------|
| `/adr` | `Templates/ADR.md` | `Templates/Custom/adr-template.md` |
| `/meeting` | `Templates/Meeting.md` | `Templates/Custom/meeting-template.md` |
| `/daily` | `Templates/Daily.md` | `Templates/Custom/daily-template.md` |
| `/task` | `Templates/Task.md` | `Templates/Custom/task-template.md` |
| `/person` | `Templates/Person.md` | `Templates/Custom/person-template.md` |
| `/system` | `Templates/System.md` | `Templates/Custom/system-template.md` |
| `/email` | `Templates/Email.md` | `Templates/Custom/email-template.md` |
| `/incubator` | `Templates/Incubator.md` | `Templates/Custom/incubator-template.md` |
| `/project` | `Templates/Project.md` | `Templates/Custom/project-template.md` |
| `/trip` | `Templates/Trip.md` | `Templates/Custom/trip-template.md` |
| `/dataasset` | `Templates/DataAsset.md` | `Templates/Custom/dataasset-template.md` |
| `/book` | `Templates/Book.md` | `Templates/Custom/book-template.md` |

## Instructions

### List Mode: `/customize-templates`

When invoked without arguments, show the override status of all templates.

1. Read the skill-to-template mapping table above
2. For each entry, check whether the custom override file exists at `Templates/Custom/<skill>-template.md`
3. Display a status table:

```markdown
| Skill | Default Template | Custom Override | Status |
|-------|-----------------|----------------|--------|
| adr | Templates/ADR.md | Templates/Custom/adr-template.md | default |
| meeting | Templates/Meeting.md | Templates/Custom/meeting-template.md | customised |
| daily | Templates/Daily.md | Templates/Custom/daily-template.md | default |
```

Use **customised** when the custom file exists, **default** when it does not.

4. Summarise: "X of Y templates have custom overrides. Use `/customize-templates <skill>` to create an override."

### Customise Mode: `/customize-templates <skill-name>`

Copy a default template to the custom override location.

1. Look up `<skill-name>` in the mapping table
2. If not found, report the error and list valid skill names
3. Check if a custom override already exists at `Templates/Custom/<skill>-template.md`
   - If it exists, inform the user: "Custom template already exists at `Templates/Custom/<skill>-template.md`. Edit it directly, or use `/customize-templates reset <skill>` to start fresh."
   - Stop
4. Read the default template from `Templates/<Type>.md`
5. Copy it to `Templates/Custom/<skill>-template.md`
6. Confirm to the user:

```
Copied default template to: Templates/Custom/<skill>-template.md

You can now edit this file to customise the template.
The original at Templates/<Type>.md remains unchanged.

Skills that support template loading will check for custom
templates first. See the "Template Loading" section below
for the pattern other skills should follow.
```

### Reset Mode: `/customize-templates reset <skill-name>`

Remove a custom template to revert to the default.

1. Look up `<skill-name>` in the mapping table
2. Check if `Templates/Custom/<skill>-template.md` exists
   - If it does not exist, inform the user: "No custom template found for `<skill>`. Already using the default."
   - Stop
3. Confirm with the user: "Remove custom template at `Templates/Custom/<skill>-template.md`? This will revert to the default template. (Y/n)"
4. If confirmed, delete the file
5. Confirm: "Removed custom template. `/<skill>` will now use the default at `Templates/<Type>.md`."

### Diff Mode: `/customize-templates diff <skill-name>`

Show differences between the custom and default templates.

1. Look up `<skill-name>` in the mapping table
2. Check if `Templates/Custom/<skill>-template.md` exists
   - If it does not exist, inform the user: "No custom template for `<skill>`. Nothing to diff."
   - Stop
3. Run a diff between the two files:
   ```bash
   diff -u "Templates/<Type>.md" "Templates/Custom/<skill>-template.md"
   ```
4. Display the diff output to the user
5. If the files are identical, report: "Custom template is identical to the default. No changes detected."

## Template Loading

**This is the pattern that other skills should adopt to support custom templates.**

When a skill creates a new note from a template, it should check for a custom override first:

1. Check for custom template at `Templates/Custom/{skill-name}-template.md`
2. If found, use it instead of the default template in `Templates/`
3. If not found, use the default template

### Example Implementation (for skill authors)

In a skill's SKILL.md instructions, add before the template-reading step:

```markdown
Check for a custom template override:
- If `Templates/Custom/<skill>-template.md` exists, read and use that template
- Otherwise, use the default `Templates/<Type>.md`
```

Skills are not required to adopt this pattern immediately. It is opt-in and backwards-compatible -- skills that do not check for custom templates will continue to work with their defaults.

## Notes

- Custom templates live in `Templates/Custom/` which is tracked by git, so overrides are version-controlled
- The naming convention `<skill>-template.md` avoids conflicts with the default templates
- Obsidian's Templater plugin will also pick up templates from `Templates/Custom/` if the folder is configured
- Only the templates listed in the mapping table above are supported; other templates in `Templates/` can be edited directly
