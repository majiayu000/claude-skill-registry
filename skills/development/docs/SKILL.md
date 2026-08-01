---
name: docs
description: A Claude Code skill for managing Architecture Decision Records (ADRs)
  using the git-adr CLI.
---

# git-adr Claude Code Skill

A Claude Code skill for managing Architecture Decision Records (ADRs) using the git-adr CLI.

## Why Use This Skill?

### Instant ADR Creation from Conversation

Turn natural language into properly formatted ADRs:

```
You: "We decided to use PostgreSQL because it has better JSON support than MySQL"

Claude: I'll create that ADR for you.
> git adr new "Use PostgreSQL for primary database" --template madr
Created ADR: 20251216-use-postgresql-for-primary-database
```

### Six Professional Formats, Zero Learning Curve

Claude automatically uses your project's configured format or helps you choose the right one:

| Format | Best For | Example Use |
|--------|----------|-------------|
| **MADR** | Option analysis with decision matrices | "Compare three caching solutions" |
| **Nygard** | Quick, minimal documentation | "Record that we picked Redis" |
| **Y-Statement** | Single-sentence decisions | "Capture our API versioning choice" |
| **Alexandrian** | Pattern-based thinking | "Document our authentication pattern" |
| **Business Case** | Stakeholder approval, ROI | "Justify the cloud migration budget" |
| **Planguage** | Measurable quality requirements | "Define our performance SLAs" |

### Git-Native Storage

ADRs are stored in git notes, not files:

- **Non-intrusive**: No `docs/adr/` folder cluttering your repo
- **Portable**: ADRs travel with git history (clone, fork, push, pull)
- **Linkable**: Associate decisions with the commits that implement them
- **Searchable**: Full-text search across all decisions

### Direct Command Execution

Claude doesn't just generate markdown - it runs the commands:

```bash
# Claude executes these directly
git adr init                    # Start tracking ADRs
git adr new "Use PostgreSQL"    # Create ADR
git adr link 20251216-... abc1234   # Link to implementation commit
git adr sync push               # Share with team
```

## Installation

### Method 1: Copy from Repository (Recommended)

```bash
# Clone git-adr if you haven't already
git clone https://github.com/zircote/git-adr.git
cd git-adr

# Copy skill to Claude Code skills directory
cp -r skills/git-adr ~/.claude/skills/
```

### Method 2: Download from Release

```bash
# Download the skill package from a release
curl -LO https://github.com/zircote/git-adr/releases/download/vX.Y.Z/git-adr-X.Y.Z.skill

# Extract to Claude Code skills directory
unzip git-adr-X.Y.Z.skill -d ~/.claude/skills/
```

### Method 3: Manual Download

1. Go to [Releases](https://github.com/zircote/git-adr/releases)
2. Download `git-adr-X.Y.Z.skill` from the latest release
3. Extract to `~/.claude/skills/`

### Verify Installation

```bash
ls ~/.claude/skills/git-adr/SKILL.md
# Should show the skill file
```

## Quick Start (30 Seconds)

After installing the skill, try these in Claude Code:

```
1. "Initialize ADR tracking in this repo"
   → Claude runs: git adr init

2. "Create an ADR about our decision to use TypeScript"
   → Claude creates a properly formatted ADR

3. "What ADRs do we have?"
   → Claude runs: git adr list

4. "Show me the TypeScript decision"
   → Claude runs: git adr show 20251216-...
```

## Feature Overview

### Creating ADRs

**From conversation:**
```
"We decided to containerize with Docker because our deployment
environments vary and we need consistency."
```

Claude will:
1. Check your project's configured template
2. Generate properly structured content
3. Create the ADR with `git adr new`

**With specific format:**
```
"Create a business case ADR for migrating to AWS"
```

Claude uses the business-case template for stakeholder-friendly documentation.

### Searching and Viewing

```
"Find all ADRs about authentication"
→ git adr search "authentication"

"Show me accepted decisions from last month"
→ git adr list --status accepted --after 2025-11-01

"What's the status of our database decisions?"
→ git adr list --tag database
```

### Linking to Implementation

```
"Link the PostgreSQL ADR to commit abc1234"
→ git adr link 20251216-use-postgresql abc1234

"Show which commits implement this decision"
→ git adr show 20251216-use-postgresql
```

### Team Collaboration

```
"Pull the latest ADRs from the team"
→ git adr sync pull

"Share my new ADR with the team"
→ git adr sync push
```

### Decision Lifecycle

```
"Supersede the MySQL decision with our PostgreSQL choice"
→ git adr supersede 20250101-use-mysql "Migrate to PostgreSQL"

"Mark the caching decision as deprecated"
→ git adr edit 20251201-... --status deprecated
```

## Skill Contents

```
skills/git-adr/
├── SKILL.md                    # Core instructions (269 lines)
└── references/
    ├── commands.md             # All git-adr commands
    ├── configuration.md        # Configuration options
    ├── best-practices.md       # ADR writing guidance
    ├── workflows.md            # Team workflow patterns
    └── formats/
        ├── madr.md             # MADR 4.0 template
        ├── nygard.md           # Original minimal format
        ├── y-statement.md      # Single-sentence format
        ├── alexandrian.md      # Pattern-language format
        ├── business-case.md    # Business justification
        └── planguage.md        # Quantified requirements
```

## Configuration

The skill respects your project's git-adr configuration:

```bash
# Set default template for new ADRs
git adr config adr.template madr

# View current configuration
git adr config list
```

Claude will automatically use your configured template when creating ADRs.

## Prerequisites

The skill requires git-adr CLI to be installed:

```bash
# Install via pip
pip install git-adr

# Or via Homebrew
brew tap zircote/git-adr && brew install git-adr

# Verify installation
git adr --version
```

## Further Reading

- [git-adr Documentation](https://github.com/zircote/git-adr)
- [MADR Format Specification](https://adr.github.io/madr/)
- [ADR Best Practices](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
