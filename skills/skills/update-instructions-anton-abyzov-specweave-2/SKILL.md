---
description: Smart merge for CLAUDE.md and AGENTS.md instruction files that preserves user customizations while updating SpecWeave sections. Use after plugin refresh, version upgrade, or when instruction files need sync. Parses SW-managed sections and preserves user content.
user-invocable: false
---

# Update Instructions Skill

Smart merge for CLAUDE.md and AGENTS.md instruction files.

## What It Does

1. **Reads existing instruction files** (if present)
2. **Parses SW-managed sections** (marked with `<!-- SW:SECTION:X -->`)
3. **Preserves user content** (anything between or after SW sections)
4. **Updates SW sections** with latest template content
5. **Writes merged result** back to file

## When to Use

- After running `specweave refresh-marketplace`
- After upgrading SpecWeave version (`npm update -g specweave`)
- When CLAUDE.md or AGENTS.md seem outdated
- To sync instruction files with latest framework features

## Usage

```
/sw:update-instructions
```

Or via CLI:
```bash
npx specweave update-instructions
```

## How Merge Works

### Fresh Install (no existing file)
Creates new file with all SW sections + meta header

### Legacy File (no SW markers)
Prepends new SW content, preserves original below separator

### Marked File (has SW markers)
Updates SW sections in-place, preserves user content between sections

## Section Format

Template sections (in `.template` files):
```markdown
<!-- SECTION:rules required -->
## Rules
Content here...
<!-- /SECTION -->
```

Generated sections (in output files):
```markdown
<!-- SW:META template="claude" version="1.0.0" sections="header,rules,..." -->

<!-- SW:SECTION:header version="1.0.0" -->
Content...
<!-- SW:END:header -->
```

## User Customization

Add custom content **between** SW sections or **after** the last section:
```markdown
<!-- SW:END:docs -->

## My Custom Section

This will be preserved during updates!
```

## Files Affected

- `CLAUDE.md` - Claude Code instruction file
- `AGENTS.md` - Generic AI tool instruction file


