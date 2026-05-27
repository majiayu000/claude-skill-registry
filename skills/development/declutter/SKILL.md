---
name: declutter
description: Identify misplaced files and organize project structure following open-source best practices, while delegating refactoring to specialized skills
version: "1.0.0"
allowed-tools: "Bash, Read, Grep, Glob, Task, Skill"
license: "AGPL-3.0"
---

# Declutter Skill

**Purpose**: Create a clean, welcoming project structure where every file has its proper place, following open-source conventions and the project's established patterns.

**Philosophy**: A well-organized project should produce a hand-sized, predictable tree that immediately communicates what the project does and how it's structured. The root should be clean and inviting, not overwhelming.

---

## Core Principles

### 1. Clean Root, Clear Intent

The project root is the first impression. It should contain only:
- Essential entry files (README, LICENSE, main config)
- Standard directories that communicate purpose
- No orphaned files, experiments, or ambiguous content

### 2. Correlation Preservation

Files that belong together stay together:
- Module-related files remain in module context
- Development stage files stay with their stage
- App-specific files stay with their app
- Build artifacts stay with build configuration

### 3. Skill Delegation

Declutter **identifies and recommends** but does not refactor alone:
- For code restructuring → delegate to `refactor` skill
- For documentation moves → delegate to `technical-writer` agent
- For build pipeline changes → delegate to `devops` skill
- If skill doesn't exist → recommend installation/configuration

### 4. Query Before Move

When placement is ambiguous:
1. First, check for relevant specialized skills/agents
2. Consult with appropriate skill for research
3. Only ask user when no skill can help
4. Always explain the reasoning

---

## When to Use This Skill

**Trigger Phrases**:
- "Declutter this project"
- "Organize the file structure"
- "Clean up the root directory"
- "This project is messy, help me organize it"
- "Where should this file go?"

**Automatic Contexts**:
- After initial project setup
- Before open-sourcing a project
- When onboarding feels overwhelming
- After feature sprawl or rapid prototyping

---

## The Declutter Workflow

```
Phase 1: Assessment (Survey)
   ↓
Phase 2: Classification (Categorize)
   ↓
Phase 3: Research (Consult Skills)
   ↓
Phase 4: Proposal (Plan Moves)
   ↓
Phase 5: Execution (Delegate Actions)
```

---

## Phase 1: Assessment (Survey the Landscape)

**Goal**: Understand current state without judgment.

### Actions:

1. **Capture the current tree**:
   ```bash
   tree -L 2 -a --dirsfirst -I '.git|node_modules|target|__pycache__|.venv'
   ```

2. **Identify technology stack**:
   - Check for `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.
   - Note frameworks (React, Astro, Django, etc.)
   - Identify build systems (webpack, vite, cargo, etc.)

3. **Count root-level items**:
   ```bash
   ls -la | wc -l
   ```

   **Healthy root**: 10-20 items (dirs + essential files)
   **Needs attention**: 20-30 items
   **Critical**: 30+ items

4. **Identify outliers**:
   - Files that don't match project type
   - Duplicate or similar-named files
   - Dated/versioned files (backup.old, file_v2.txt)
   - Orphaned configuration files

### Output:
- [ ] Tree captured
- [ ] Tech stack identified
- [ ] Root item count logged
- [ ] Outliers list created

---

## Phase 2: Classification (Categorize Everything)

**Goal**: Assign each item to a category for action.

### File Categories:

| Category | Examples | Action |
|----------|----------|--------|
| **Essential Root** | README, LICENSE, main config | Keep in root |
| **Documentation** | *.md guides, ADRs, specs | Move to `/docs` |
| **Configuration** | dotfiles, *.config.js | Consider `/config` or keep root |
| **Scripts** | Shell scripts, automation | Move to `/scripts` |
| **DevOps** | CI/CD, Docker, k8s | Move to `.github/`, `/deploy` |
| **Source Code** | Application code | Move to `/src`, `/lib`, `/app` |
| **Tests** | Test files | Move to `/tests` or colocate |
| **Build Artifacts** | Generated files | Add to `.gitignore` |
| **Experiments** | POCs, spikes | Move to `/sandbox` or delete |
| **Orphaned** | No clear purpose | Ask user or delete |

### Classification Rules:

**For Markdown Files**:
```
README.md, CONTRIBUTING.md, CHANGELOG.md → Root (OSS standard)
CODE_OF_CONDUCT.md, SECURITY.md → Root (GitHub special files)
*.md (other) → /docs
```

**For Configuration**:
```
Single dotfile → Root acceptable
Multiple similar configs → /config directory
Build tool config → Usually root (webpack.config.js, etc.)
Editor config → Root (.editorconfig, .prettierrc)
```

**For Scripts**:
```
1-2 scripts → /scripts or root acceptable
3+ scripts → Must move to /scripts
Shell scripts → /scripts
Build scripts → /scripts/build or npm scripts
```

### Output:
- [ ] Each file/directory categorized
- [ ] Action type assigned (keep/move/delete/ask)
- [ ] Ambiguous items flagged for consultation

---

## Phase 3: Research (Consult Specialized Skills)

**Goal**: Get expert guidance before making moves.

### Skill Consultation Matrix:

| Question Type | Consult |
|--------------|---------|
| "Where should docs go?" | `technical-writer` agent |
| "How to structure Rust project?" | `rust-cli-architect` agent |
| "Best practices for this framework?" | `Explore` agent with framework focus |
| "Is this safe to delete?" | `safety-pattern-auditor` skill |
| "How to reorganize build pipeline?" | `devops` skill (if exists) |
| "Cultural/locale files placement?" | `multicultural-holidays` skill |

### Consultation Protocol:

1. **Check if skill exists**:
   ```
   Glob: .claude/skills/*/SKILL.md
   ```

2. **Check if agent can help**:
   - Review Task tool agent descriptions
   - Match to categorization need

3. **If skill/agent available**:
   ```
   Task: [appropriate-agent]
   Prompt: "I'm decluttering this project and need guidance on
   [specific question]. What's the best practice for [specific situation]?"
   ```

4. **If skill/agent not available**:
   ```
   Report to user:
   "I'd like to consult a [skill-type] skill for [reason], but it's
   not installed. Would you like to:
   a) Configure/install the skill
   b) Proceed with my best judgment
   c) Skip this category for now"
   ```

### OSS Convention Research:

When framework-specific guidance isn't available, research:
- GitHub trending repos in same tech stack
- Official framework documentation
- Community-accepted patterns

Use the `Explore` agent:
```
Task: Explore
Prompt: "Find the standard directory structure for [technology] projects.
Focus on: root organization, docs placement, scripts location, config handling."
```

### Output:
- [ ] Skills/agents consulted
- [ ] Best practices documented
- [ ] User decisions recorded (if any)

---

## Phase 4: Proposal (Create the Move Plan)

**Goal**: Present a clear, actionable reorganization plan.

### Proposal Format:

```markdown
## Declutter Proposal - [Project Name]

### Current State
- Root items: 42 (Critical - needs attention)
- Tech stack: Rust CLI with Astro website
- Primary issues: Documentation scattered, scripts mixed

### Proposed Structure

```
project-root/
├── .claude/                 # Claude configuration (keep)
├── .github/                 # GitHub workflows (keep)
├── docs/                    # Documentation (create)
│   ├── architecture/        # ADRs and design docs
│   ├── guides/              # User guides
│   └── api/                 # API documentation
├── scripts/                 # Automation (organize)
│   ├── build/               # Build scripts
│   ├── dev/                 # Development helpers
│   └── release/             # Release automation
├── src/                     # Source code (keep)
├── tests/                   # Test files (keep)
├── website/                 # Astro site (keep)
├── Cargo.toml               # Main config (keep)
├── README.md                # Entry point (keep)
├── LICENSE                  # Legal (keep)
└── CHANGELOG.md             # History (keep)
```

### Proposed Moves

| File | From | To | Reason |
|------|------|-----|--------|
| ARCHITECTURE.md | / | /docs/architecture/ | Standard docs location |
| setup.sh | / | /scripts/ | OSS convention |
| dev-notes.md | / | /docs/guides/ | Internal documentation |

### Files to Delete
| File | Reason |
|------|--------|
| backup.old | Obsolete backup |
| test_experiment.rs | Superseded by /tests |

### Files Requiring Decision
| File | Options |
|------|---------|
| random_script.py | A) Delete B) Move to /scripts C) Keep |

### Skills to Engage

1. `technical-writer` - Restructure /docs hierarchy
2. `refactor` - Update import paths after moves (NOT AVAILABLE - recommend install)
```

### Output:
- [ ] Proposal document created
- [ ] All moves justified
- [ ] User decisions requested
- [ ] Skills identified for delegation

---

## Phase 5: Execution (Delegate and Move)

**Goal**: Execute the plan with proper delegation.

### Execution Rules:

1. **Never refactor code directly** - delegate to `refactor` skill
2. **Never update imports alone** - delegate to appropriate skill
3. **Document all moves** in commit message
4. **Preserve git history** where possible (git mv)

### Move Protocol:

```bash
# Always use git mv for tracked files
git mv old/path new/path

# Create directories first
mkdir -p new/directory

# Batch related moves
git mv docs/*.md docs/guides/
```

### Post-Move Validation:

1. **Check for broken links**:
   ```bash
   grep -rn "old/path" --include="*.md" --include="*.rs"
   ```

2. **Verify imports still work**:
   ```bash
   cargo check  # For Rust
   npm run build  # For JS
   ```

3. **Update any absolute references**

### Commit Strategy:

```bash
# Single logical commit for declutter
git add -A
git commit -m "$(cat <<'EOF'
refactor: Declutter project structure

Moves:
- ARCHITECTURE.md → docs/architecture/
- setup.sh → scripts/
- dev-notes.md → docs/guides/

Deletes:
- backup.old (obsolete)
- test_experiment.rs (superseded)

Created:
- docs/architecture/ directory
- scripts/build/ directory

Consulted: technical-writer agent, OSS conventions
EOF
)"
```

### Output:
- [ ] All moves executed
- [ ] Broken references fixed
- [ ] Commit created
- [ ] Post-move validation passed

---

## Mono-Repo Strategy

For mono-repos, declutter level by level:

### Level 1: Root
- Focus on top-level organization
- Ensure clear separation between projects
- Shared configs at root or `/config`

### Level 2: Individual Projects
- Apply same principles to each sub-project
- Respect sub-project conventions
- Don't cross-contaminate

### Level 3: Scripts/DevOps
- Centralize shared scripts
- Per-project scripts stay in project
- CI/CD in `.github/` or `/ci`

### Mono-Repo Structure Template:

```
monorepo/
├── .github/               # Shared CI/CD
├── docs/                  # Shared documentation
├── packages/              # Sub-projects
│   ├── app-a/
│   │   ├── src/
│   │   ├── tests/
│   │   └── package.json
│   └── app-b/
├── scripts/               # Shared automation
├── config/                # Shared configuration
├── package.json           # Root workspace
└── README.md
```

---

## Technology-Specific Conventions

### Rust Projects
```
project/
├── src/
│   ├── lib.rs             # Library entry
│   └── main.rs            # Binary entry
├── tests/                 # Integration tests
├── benches/               # Benchmarks
├── examples/              # Example usage
├── Cargo.toml
└── README.md
```

### JavaScript/Node Projects
```
project/
├── src/                   # Source code
├── dist/                  # Build output (gitignored)
├── tests/ or __tests__/   # Tests
├── scripts/               # Build/dev scripts
├── package.json
└── README.md
```

### Python Projects
```
project/
├── src/project_name/      # Package code
├── tests/                 # Tests
├── docs/                  # Documentation
├── scripts/               # Automation
├── pyproject.toml
└── README.md
```

See `references/oss-conventions.md` for comprehensive patterns.

---

## Quick Reference Checklist

```
┌─────────────────────────────────────────────────────────┐
│  DECLUTTER CHECKLIST                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Assessment:                                            │
│  ☐ Tree captured (depth 2)                             │
│  ☐ Tech stack identified                               │
│  ☐ Root item count: _____ (target: <20)               │
│  ☐ Outliers identified                                 │
│                                                         │
│  Classification:                                        │
│  ☐ Each item categorized                               │
│  ☐ Actions assigned (keep/move/delete/ask)            │
│                                                         │
│  Research:                                              │
│  ☐ Relevant skills consulted                           │
│  ☐ Missing skills reported                             │
│  ☐ OSS conventions checked                             │
│                                                         │
│  Proposal:                                              │
│  ☐ Target structure documented                         │
│  ☐ Move plan created                                   │
│  ☐ User decisions collected                            │
│                                                         │
│  Execution:                                             │
│  ☐ Moves delegated to skills where needed              │
│  ☐ git mv used for tracked files                       │
│  ☐ Broken references fixed                             │
│  ☐ Commit created with full context                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## What Declutter Does NOT Do

- **Does not refactor code** - delegates to `refactor` skill
- **Does not update imports** - delegates to appropriate skill
- **Does not delete without confirmation** - always asks
- **Does not override project conventions** - respects existing patterns
- **Does not move without explanation** - documents all decisions

---

## Skill Dependencies

### Required:
- None (can run standalone with manual moves)

### Recommended:
- `refactor` - For updating imports after moves
- `technical-writer` - For documentation restructuring
- `Explore` agent - For OSS convention research

### Optional:
- `devops` - For pipeline reorganization
- `validate-constitution` - For checking project rules

---

## Example Invocation

Using the Task tool:

```
Task: general-purpose
Prompt: "Run the declutter skill on this project.

Follow the workflow in .claude/skills/declutter/SKILL.md:
1. Assess the current structure
2. Classify all files/directories
3. Consult relevant skills for guidance
4. Create a proposal document
5. Present it for user approval before execution

Focus on making the root clean and welcoming.
Respect existing conventions and correlations.
Delegate refactoring to appropriate skills."
```

---

## Success Criteria

Declutter is complete when:

- ✅ Root contains ≤20 items
- ✅ All files are in logical locations
- ✅ Structure follows tech-stack conventions
- ✅ Orphaned files addressed
- ✅ Proposal approved by user
- ✅ All moves executed or delegated
- ✅ No broken references remain
- ✅ Commit documents all changes

---

*A decluttered project is a welcoming project. Every file in its place, every place with purpose.*
