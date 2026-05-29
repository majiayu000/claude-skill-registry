---
description: Show complete reference for all agentic-loop commands (slash commands, Ralph CLI, vibe CLI).
---

# Vibe & Thrive - Complete Reference

Print this complete reference for the user. Do not add any commentary.

---

## Slash Commands (in Claude Code)

| Command | Description |
|---------|-------------|
| `/idea [feature]` | Brainstorm in plan mode, generate PRD for Ralph |
| `/sign` | Add a learned pattern for Ralph to remember |
| `/my-dna` | Set up your personal style preferences |
| `/vibe-check` | Audit code quality before shipping |
| `/review` | Code review with OWASP security checks |
| `/explain` | Explain code line by line |
| `/styleguide` | Generate UI component design system |
| `/tour` | Interactive walkthrough of agentic-loop |
| `/vibe-help` | Quick reference cheatsheet |
| `/vibe-list` | This complete reference |

---

## Ralph CLI (in terminal)

### Setup & Status
| Command | Description |
|---------|-------------|
| `npx ralph init` | Initialize `.ralph/` in current directory |
| `npx ralph status` | Show feature, stories, pass/fail counts |
| `npx ralph progress` | Show last 50 lines of progress log |
| `npx ralph version` | Show version info |
| `npx ralph help` | Show built-in help |

### PRD Generation
| Command | Description |
|---------|-------------|
| `npx ralph prd "notes"` | Generate PRD interactively from description |
| `npx ralph prd --file spec.md` | Generate PRD from a file |
| `npx ralph prd --accept` | Save generated PRD to `.ralph/prd.json` |

### Autonomous Loop
| Command | Description |
|---------|-------------|
| `npx ralph run` | Run loop until all stories pass |
| `npx ralph run --max 10` | Limit to N iterations (default: 20) |
| `npx ralph run --story TASK-001` | Run for specific task only |
| `npx ralph stop` | Stop after current story completes |

### Verification
| Command | Description |
|---------|-------------|
| `npx ralph check` | Run all configured checks |
| `npx ralph verify TASK-001` | Verify a specific task |

### Signs (Learned Patterns)
| Command | Description |
|---------|-------------|
| `npx ralph signs` | List all learned patterns |
| `npx ralph sign "pattern" [cat]` | Add pattern with optional category |
| `npx ralph unsign <id or text>` | Remove a sign by ID or text match |

---

## Vibe CLI (in terminal)

| Command | Description |
|---------|-------------|
| `vibe help` | Show terminal quick reference |

---

## The Loop

```
/idea [feature]          Brainstorm → PRD
npx ralph run            Autonomous coding
npx ralph status         Check progress
npx ralph stop           Stop after current story
```

---

## Slash Command Details

### /idea [feature description]
Brainstorm in plan mode, explore codebase, ask clarifying questions.
- Writes idea to `docs/ideas/{feature}.md`
- On approval, splits into PRD stories
- Writes to `.ralph/prd.json`

### /review [file or selection]
Code review with security focus (OWASP Top 10):
- **Quick review** - Critical/high issues only
- **Full review** - Everything
- **Security review** - Deep dive on vulnerabilities
- **Performance review** - Focus on speed

### /explain [file or code]
Line-by-line explanation:
- High-level overview
- Walk through each section
- Highlight key concepts
- Summarize takeaways

### /styleguide
Generate design system page at `/styleguide`:
- Discovers your tech stack
- Asks about vibe (minimal, bold, dark, etc.)
- Asks about colors, border radius, components
- Generates tokens, buttons, forms, cards, feedback

### /vibe-check
Audit code for AI-introduced patterns:
- Debug statements
- TODO/FIXME comments
- Empty catch blocks
- Hardcoded URLs
- Potential secrets
- DRY violations

### /my-dna
Interactive wizard to set up your personal style:
- Core values (simplicity, speed, correctness, etc.)
- Communication preferences (brief vs detailed, tone)
- Working style (ask first vs try solutions)
- Learning preferences (show alternatives, explain why)

Creates `~/.claude/DNA.md` - applies to all your projects.

---

## Signs Examples

```bash
# Add patterns Ralph should follow
npx ralph sign "Always use camelCase in WebSocket responses" frontend
npx ralph sign "Run migrations before seeding" backend
npx ralph sign "Check for null before accessing nested props" general

# List learned patterns
npx ralph signs

# Remove a sign
npx ralph unsign sign-001
npx ralph unsign "camelCase"
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RALPH_DIR` | `.ralph` | Override ralph directory |
| `PROMPT_FILE` | `PROMPT.md` | Override prompt file |

---

## Config (.ralph/config.json)

```json
{
  "checks": {
    "lint": "npm run lint",
    "test": "npm test",
    "build": "npm run build"
  },
  "testUrlBase": "http://localhost:3000",
  "maxSessionSeconds": 600
}
```

---

## File Structure

```
# Project files
.ralph/
├── config.json      # Verification checks, settings
├── prd.json         # Current feature PRD
├── signs.json       # Learned patterns
├── progress.txt     # Activity log
├── archive/         # Completed PRDs
└── screenshots/     # Browser verification captures

CLAUDE.md            # Project standards (shared with team)
PROMPT.md            # Base prompt for Ralph sessions
docs/ideas/          # Brainstorm outputs from /idea

# Global files (your home directory)
~/.claude/
└── DNA.md           # Your DNA - personal preferences (from /my-dna)
```

---

*https://github.com/allierays/agentic-loop*
