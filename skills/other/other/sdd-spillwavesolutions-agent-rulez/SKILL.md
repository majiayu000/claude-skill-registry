---
name: sdd
description: This skill should be used when users want guidance on Spec-Driven Development methodology using GitHub's Spec-Kit. Guide users through executable specification workflows for both new projects (greenfield) and existing codebases (brownfield). After any SDD command generates artifacts, automatically provide structured 10-point summaries with feature status tracking, enabling natural language feature management and keeping users engaged throughout the process.
version: 2.1.0
triggers:
  - spec-driven development
  - spec kit
  - speckit
  - sdd
  - specify cli
  - specification driven
  - github spec-kit
  - /speckit
  - constitution
  - specify init
  - executable specifications
  - intent-driven development
  - brownfield
  - existing codebase
  - legacy code
  - legacy system
  - add features to existing
  - modernize
  - modernization
  - existing project
  - reverse engineer
  - codebase analysis
  - iterative enhancement
  - feature status
  - track features
  - add feature
  - move feature
  - reorder features
  - feature progress
  - feature dependencies
author: Based on GitHub Spec-Kit by Den Delimarsky and John Lam
license: MIT
tags:
  - development-methodology
  - ai-native-development
  - spec-driven
  - github
  - project-management
  - workflow
  - requirements
  - planning
---

# Spec-Driven Development (SDD) Skill

Guide users through GitHub's Spec-Kit for Spec-Driven Development - a methodology that flips traditional software development by making specifications executable and directly generating working implementations.

## Core Philosophy

Spec-Driven Development emphasizes:
- **Intent-driven development**: Define the "what" before the "how"
- **Rich specification creation**: Use guardrails and organizational principles
- **Multi-step refinement**: Not one-shot code generation
- **AI-native**: Heavy reliance on advanced AI capabilities

Remember: This is **AI-native development**. Specifications aren't just documentation - they're executable artifacts that directly drive implementation. The AI agent uses them to generate working code that matches the intent defined in the specs.

## Quick Decision Tree

### Is this a new project (greenfield)?
→ **See [Greenfield Workflow](references/greenfield.md)** for the complete 6-step process

### Is this an existing codebase (brownfield)?
→ **See [Brownfield Workflow](references/brownfield.md)** for reverse-engineering and integration guidance

### Need installation help?
→ **See [Installation Guide](references/sdd_install.md)** for setup and troubleshooting

## Installation Quick Start

**Recommended (Persistent):**
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**One-time Usage:**
```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

**Verify:**
```bash
specify check
```

For detailed installation options, troubleshooting, and environment variables, see [Installation Guide](references/sdd_install.md).

## Supported AI Agents

Works with:
- ✅ Claude Code
- ✅ GitHub Copilot
- ✅ Gemini CLI
- ✅ Cursor
- ✅ Qwen Code
- ✅ opencode
- ✅ Windsurf
- ✅ Kilo Code
- ✅ Auggie CLI
- ✅ CodeBuddy CLI
- ✅ Roo Code
- ✅ Codex CLI
- ✅ Amp
- ⚠️ Amazon Q Developer CLI (doesn't support custom arguments for slash commands)

## Artifact Summarization and Feedback Loop

**CRITICAL WORKFLOW**: After any SDD command generates or modifies artifacts, automatically follow this feedback loop to keep the user engaged:

### After Each Command Completes

1. **Detect Artifact Changes**
   - Identify which artifacts were created or modified:
     - `constitution.md` (project principles)
     - `spec.md` (requirements specification)
     - `plan.md` (technical implementation plan)
     - `tasks.md` (actionable task breakdown)
     - Analysis reports from brownfield workflows

2. **Read and Summarize**
   - Read the relevant artifact(s)
   - Extract key information:
     - **For constitution.md**: Core principles, coding standards, constraints
     - **For spec.md**: Main requirements, user stories, success criteria
     - **For plan.md**: Tech stack choices, architecture decisions, milestones
     - **For tasks.md**: Number of tasks, major task categories, dependencies
     - **For analysis reports**: Current patterns, tech debt, integration points

3. **Present Structured Summary** (Use 10-Point Template Below)
   - Show what was generated and why
   - Highlight the most important decisions with rationale
   - Include quality indicators and watch-outs
   - Keep summary focused and actionable
   - Use clear headings for each section

4. **Include Feature Status** (Hybrid Approach)
   - Brief status line in every summary
   - Detailed status on demand with `/speckit-status`
   - See "Feature Status Tracking" section below

5. **Offer Feedback Options**
   - **Option A**: "Looks good, proceed to next step"
   - **Option B**: "I'd like to modify [specific section]"
   - **Option C**: "Regenerate with these changes: [user input]"
   - **Option D**: "Explain why [specific decision] was made"

### 10-Point Summary Template

Use this structured format after ANY SDD command completes:

```
## ✅ [Command Name] Completed - Here's What Just Happened

### 🎯 Key Decisions Made (Top 3)
1. [Decision] - **Rationale:** [Why this was chosen]
2. [Decision] - **Rationale:** [Why this was chosen]
3. [Decision] - **Rationale:** [Why this was chosen]

### 📋 What Was Generated
- [Artifact 1]: [Brief description of content]
- [Artifact 2]: [Brief description of content]

### 🔍 Important Items to Review (Top 3)
1. [Critical item to check and why it matters]
2. [Important detail to verify and potential impact]
3. [Edge case to consider and how it affects the design]

### ⚠️ Watch Out For (Top 2)
- [Potential issue or gotcha] - **How to avoid:** [Guidance]
- [Common mistake] - **How to avoid:** [Guidance]

### 🔄 What This Enables Next (2 Options)
- **Option 1:** [Next step] - Best if: [Condition]
- **Option 2:** [Alternative step] - Best if: [Condition]

📊 **Feature Status:** [Current Feature Name] ([Stage]) → Next: [Next Feature]
   Progress: [●●●○○] [X]% | Completed: [N] of [Total] features | Dependencies: [Status]

**Your options:** [A] Proceed [B] Modify [C] Explain more [D] Show full status
```

### Example: Enhanced Summarization After \`/speckit-specify\`

\`\`\`
## ✅ Specify Completed - Here's What Just Happened

### 🎯 Key Decisions Made
1. **Authentication: JWT tokens** - Rationale: Stateless architecture, horizontally scalable, industry standard
2. **Password requirements: 12+ characters with complexity** - Rationale: Balances security (NIST guidelines) with usability
3. **Session timeout: 24 hours** - Rationale: Standard for web apps, balances security vs user convenience

### 📋 What Was Generated
- \`.speckit/features/user-auth/specify.md\`: Complete requirements with 5 user stories, 8 success criteria, 3 edge cases

### 🔍 Important Items to Review
1. **Password reset flow** - Verify email requirements match your infrastructure (SMTP server, templates)
2. **Multi-factor authentication** - Currently marked as "future enhancement"; may need to be in MVP
3. **Rate limiting** - Set at 5 login attempts per 15 min; consider if this fits your security policy

### ⚠️ Watch Out For
- **Email service dependency not specified** - How to avoid: Add email service to plan.md dependencies
- **GDPR compliance for user data** - How to avoid: Review data retention and user deletion requirements

### 🔄 What This Enables Next
- **Option 1:** Run \`/speckit-plan\` to design technical implementation - Best if: Requirements look good
- **Option 2:** Modify specify.md - Best if: You need to adjust requirements or add features

📊 **Feature Status:** user-authentication (Specified) → Next: profile-management
   Progress: [●●○○○] 40% | Completed: 1 of 5 features | Dependencies: database-setup ✅

**Your options:** [A] Proceed to planning [B] Modify requirements [C] Explain JWT choice [D] Show full status
\`\`\`

### When to Skip Summarization

Only skip the summarization step when:
- User explicitly requests "skip summaries" or "run all steps automatically"
- Re-running a command without artifact changes
- Command fails or produces errors (troubleshoot instead)

### Benefits of This Workflow

- **Eliminates "black box" feeling**: Clear explanations of what was generated and why
- **Enables early feedback**: Catch misunderstandings before implementation
- **Maintains agility**: Quick review with structured format, not lengthy approval processes
- **Builds trust**: User sees the AI's reasoning and decisions with rationale
- **Provides context**: Feature status keeps users oriented in the overall project

## Feature Status Tracking

### Hybrid Approach

After every SDD command, include a **brief feature status line** in the summary. Provide **detailed status on demand** with `/speckit-status`.

### Brief Status Line Format

Include this at the end of every summary:

```
📊 **Feature Status:** [Current Feature Name] ([Stage]) → Next: [Next Feature Name]
   Progress: [●●●○○] [X]% | Completed: [N] of [Total] features | Dependencies: [Dep] ✅/⏸️
```

**Stage values:**
- `Specifying` (20% complete)
- `Planning` (40% complete)
- `Tasking` (60% complete)
- `In Progress` (80% complete)
- `Complete` (100% complete)

**Progress indicator:**
- Use filled circles (●) for completed stages
- Use empty circles (○) for pending stages
- Calculate percentage based on stage

### Detailed Status Dashboard

When user requests full status (option D) or runs `/speckit-status`, show:

```
📊 Project Feature Status Dashboard

🎯 CURRENT FEATURE
├─ [feature-name] ([Stage] - [X]% complete)
│  ├─ ✅ Requirements specified
│  ├─ 🔄 Implementation plan in progress
│  ├─ ⏸️  Tasks not started
│  └─ ⏸️  Implementation not started
│  Blockers: [None | Description]
│  Dependencies: [feature-name] ✅

✅ COMPLETED FEATURES ([N])
├─ [feature-1] (100% complete)
└─ [feature-2] (100% complete)

📋 UPCOMING FEATURES ([N])
├─ [feature-3] (depends on: [current-feature])
└─ [feature-4] (depends on: [feature-3])

⚠️  BLOCKED FEATURES ([N])
[List any features that are blocked with reasons]
```

### Natural Language Feature Management

Claude should automatically detect and handle natural language feature management requests:

**User says:** "Move feature XYZ before ABC"
**Claude does:**
1. Reads current feature list from `.speckit/features/`
2. Shows current order with numbers
3. Proposes new order
4. Asks for confirmation
5. Updates feature priority/order in constitution or plan
6. Shows updated status dashboard

**User says:** "Add a new feature for email notifications"
**Claude does:**
1. Detects new feature request
2. Asks clarifying questions (priority, dependencies, description)
3. Generates feature spec outline
4. Inserts into feature list at appropriate position
5. Shows updated status dashboard

**User says:** "Let's do profile-management first"
**Claude does:**
1. Identifies current feature order
2. Proposes moving profile-management to top priority
3. Adjusts dependencies if needed
4. Updates artifacts
5. Shows updated status

**Detection patterns:**
- "Move [feature] before/after [other]" → Reorder
- "Add [feature]" → New feature
- "Let's do [feature] first" → Move to top priority
- "Skip [feature] for now" → Mark as deferred
- "We finished [feature]" → Update status to complete
- "What features depend on [feature]?" → Show dependency tree
- "Show feature status" → Display full dashboard

### Quick Feature Operations

Guide users through these operations when requested:

**Add Feature:**
```
User: "Add a feature for admin dashboard"
Claude:
1. What's the priority? (High/Medium/Low)
2. What features does this depend on? (user-auth, profile-management, etc.)
3. Brief description?
[Creates outline, shows updated status]
```

**Reorder Features:**
```
User: "Reorder features"
Claude:
Current order:
1. user-authentication
2. profile-management
3. admin-dashboard
4. email-notifications
5. reporting

How would you like to reorder? (provide new numbers or describe changes)
[Updates order, shows new status]
```

**Remove Feature:**
```
User: "Remove the reporting feature"
Claude:
⚠️  Warning: This will remove 'reporting' feature.
Dependencies affected: None
Are you sure? (yes/no)
[If yes: removes, updates status]
```

### Progress Calculation

Automatically calculate progress based on SDD workflow completion:

| Stage | Progress | Indicators |
|-------|----------|------------|
| **Specified** | 20% | `specify.md` exists |
| **Planned** | 40% | `plan.md` exists |
| **Tasked** | 60% | `tasks.md` exists |
| **In Progress** | 80% | Implementation started (code files modified) |
| **Complete** | 100% | Implementation complete, tests pass |

### Dependency Tracking

Track and visualize dependencies:

**Show dependencies:**
```
user-authentication
├─ Depends on: database-setup ✅
└─ Blocks: profile-management ⏸️, admin-dashboard ⏸️
```

**Check if ready:**
```
📊 Can we start profile-management?
   Checking dependencies...
   ✅ user-authentication (complete)
   ✅ database-setup (complete)

   All dependencies satisfied! Ready to proceed.
```

**Detect circular dependencies:**
```
⚠️  Warning: Circular dependency detected
   feature-A depends on feature-B
   feature-B depends on feature-C
   feature-C depends on feature-A

   Please resolve this before proceeding.
```

### Integration with Workflows

**For Greenfield Projects:**
- After `/speckit-specify`, ask if there are multiple features
- If yes, list them and track progress through each
- Show status after each command

**For Brownfield Projects:**
- After `/speckit-reverse-engineer`, create feature list from discovered functionality
- Track new features separately from existing documented features
- Show integration impact on status

For complete feature management guidance, see [Feature Management Guide](references/feature_management.md).

## How to Use This Skill

### When User Asks About SDD

1. Explain core philosophy: Executable specifications, intent-driven, AI-native
2. Verify prerequisites: \`uv\`, Python 3.11+, Git, AI agent
3. Determine project type: New (greenfield) vs existing (brownfield)
4. Guide to appropriate workflow:
   - Greenfield → [Greenfield Workflow](references/greenfield.md)
   - Brownfield → [Brownfield Workflow](references/brownfield.md)

### When User Wants to Start a New Project

1. Guide installation → [Installation Guide](references/sdd_install.md)
2. Initialize project:
   \`\`\`bash
   specify init my-project --ai claude
   \`\`\`
3. Follow greenfield workflow → [Greenfield Workflow](references/greenfield.md)
4. **After each step**: Summarize artifacts and get user feedback

### When User Has an Existing Codebase

1. Check for \`.speckit/\` directory
2. **If missing** → Guide through [Brownfield Workflow](references/brownfield.md):
   - Analyze existing code
   - Generate constitution from existing patterns
   - Choose artifact generation strategy
   - Add new features with SDD
3. **If present** → Determine next step based on current progress
4. **After each step**: Summarize artifacts and get user feedback

### When User Wants to Add a Feature

**To greenfield project:**
1. Navigate to [Greenfield Workflow](references/greenfield.md)
2. Follow steps 3-6 (specify → plan → tasks → implement)
3. Summarize each artifact before proceeding

**To brownfield/existing project:**
1. Navigate to [Brownfield Workflow](references/brownfield.md)
2. Follow steps 6-7 (specify → integration planning → tasks → implement)
3. Summarize each artifact before proceeding

### When User Encounters Issues

1. **Installation issues** → [Installation Guide](references/sdd_install.md) troubleshooting section
2. **Workflow issues** → Check appropriate workflow guide:
   - [Greenfield troubleshooting](references/greenfield.md)
   - [Brownfield troubleshooting](references/brownfield.md)
3. **Feature detection** → Set \`SPECIFY_FEATURE\` environment variable (see [Installation Guide](references/sdd_install.md))

## Workflow Overview

### Greenfield (New Projects)

\`\`\`
specify init → /speckit-constitution → [SUMMARIZE] →
/speckit-specify → [SUMMARIZE] → /speckit-plan → [SUMMARIZE] →
/speckit-tasks → [SUMMARIZE] → /speckit-implement
\`\`\`

**Full details:** [Greenfield Workflow](references/greenfield.md)

### Brownfield (Existing Projects)

\`\`\`
specify init --here → /speckit-brownfield → [SUMMARIZE] →
/speckit-analyze-codebase → [SUMMARIZE] →
/speckit-reverse-engineer → [SUMMARIZE] → /speckit-specify → [SUMMARIZE] →
/speckit-integration-plan → [SUMMARIZE] → /speckit-tasks → [SUMMARIZE] →
/speckit-implement
\`\`\`

**Full details:** [Brownfield Workflow](references/brownfield.md)

## Development Phases Supported

### 0-to-1 Development ("Greenfield")
Start with high-level requirements, generate specifications from scratch, plan implementation steps, build production-ready applications.

**→ [Greenfield Workflow](references/greenfield.md)**

### Iterative Enhancement ("Brownfield")
Add features iteratively to existing codebases, modernize legacy systems, adapt processes for evolving requirements, reverse-engineer existing code into SDD format.

**→ [Brownfield Workflow](references/brownfield.md)**

### Creative Exploration
Explore diverse solutions in parallel, support multiple technology stacks & architectures, experiment with UX patterns.

**→ [Greenfield Workflow](references/greenfield.md) - Multi-Stack Exploration section**

## Key Commands Reference

### Installation & Setup
\`\`\`bash
specify init <project>              # New project
specify init --here --force         # Existing project
specify check                       # Verify installation
\`\`\`

### Greenfield Workflow
\`\`\`
/speckit-constitution               # Project principles → SUMMARIZE
/speckit-specify                    # Define requirements → SUMMARIZE
/speckit-plan                       # Technical planning → SUMMARIZE
/speckit-tasks                      # Break down tasks → SUMMARIZE
/speckit-implement                  # Execute
\`\`\`

### Brownfield Workflow
\`\`\`
/speckit-brownfield                 # Analyze existing code → SUMMARIZE
/speckit-analyze-codebase          # Deep analysis & constitution → SUMMARIZE
/speckit-reverse-engineer          # Document existing features → SUMMARIZE
/speckit-integration-plan          # Plan new feature integration → SUMMARIZE
\`\`\`

### Optional Enhancement Commands
\`\`\`
/speckit-clarify                   # Clarify ambiguous requirements
/speckit-analyze                   # Cross-artifact consistency check
/speckit-checklist                 # Generate quality checklists
\`\`\`

## Analysis Scripts

The SDD skill includes analysis scripts for deep quality validation and progress tracking:

### \`scripts/phase_summary.sh\`
Generates a comprehensive progress report across all phases in a tasks.md file:
- Shows completion percentage for each phase
- Lists pending tasks per phase
- Highlights simplified/modified tasks
- Provides overall progress statistics
- Supports any SDD feature's tasks.md file

**Usage:**
\`\`\`bash
~/.claude/skills/sdd/scripts/phase_summary.sh specs/003-keyboard-shortcuts/tasks.md
\`\`\`

**Output:** Markdown-formatted phase-by-phase progress report with:
- Phase-by-phase completion percentages
- Pending task lists (up to 5 per phase)
- Simplified task warnings
- Overall feature progress summary

**When to Use:**
- Check progress on any SDD feature
- Get quick overview of what's complete vs pending
- Identify phases that need attention
- Generate status reports for stakeholders

### \`scripts/analyze-requirements.py\`
Analyzes requirement coverage across spec.md and tasks.md:
- Maps functional requirements (FR-001, FR-002, etc.) to implementation tasks
- Identifies uncovered requirements (gaps in task coverage)
- Flags vague requirements lacking measurable criteria
- Calculates coverage percentage

**Usage:**
\`\`\`bash
python3 ~/.claude/skills/sdd/scripts/analyze-requirements.py
\`\`\`

**Output:** JSON with coverage metrics, uncovered requirements, vague requirements

### \`scripts/analyze-success-criteria.py\`
Analyzes success criteria verification coverage:
- Maps success criteria (SC-001, SC-002, etc.) to verification tasks
- Validates measurability of each criterion
- Identifies criteria without verification tasks
- Groups by metric type (performance, accessibility, usability)

**Usage:**
\`\`\`bash
python3 ~/.claude/skills/sdd/scripts/analyze-success-criteria.py
\`\`\`

**Output:** JSON with coverage summary, verification task mapping

### \`scripts/analyze-edge-cases.py\`
Analyzes edge case coverage across specifications:
- Maps edge cases to explicit task coverage
- Identifies implicitly covered cases (handled by general logic)
- Flags uncovered edge cases requiring attention
- Categorizes coverage type (EXPLICIT, IMPLICIT, UNCOVERED)

**Usage:**
\`\`\`bash
python3 ~/.claude/skills/sdd/scripts/analyze-edge-cases.py
\`\`\`

**Output:** JSON with coverage breakdown, uncovered edge case details

**When to Use:**
These scripts are automatically invoked during \`/speckit-analyze\` to provide deep consistency validation. They help identify:
- Requirements without task coverage
- Success criteria without verification
- Edge cases that need test coverage
- Ambiguous requirements needing clarification

### Validation Commands (Brownfield)
\`\`\`
/speckit-validate-reverse-engineering  # Verify spec accuracy
/speckit-coverage-check                # Check documentation coverage
/speckit-validate-constitution         # Verify constitution consistency
/speckit-trace [feature]               # Map specs to code
\`\`\`

## Detailed Documentation

- **[Installation Guide](references/sdd_install.md)**: Installation methods, troubleshooting, environment variables
- **[Greenfield Workflow](references/greenfield.md)**: Complete 6-step workflow for new projects
- **[Brownfield Workflow](references/brownfield.md)**: Complete 7-step workflow for existing codebases

## Integration with Other Skills

This skill works well with:
- **project-memory**: Document SDD decisions and patterns
- **design-doc-mermaid**: Visualize architecture from plan.md
- **github-workflows**: Automate SDD artifact validation
- **code-quality-reviewer**: Review generated implementation

## Resources

- GitHub Spec-Kit Repository: https://github.com/github/spec-kit
- Issues/Support: https://github.com/github/spec-kit/issues
- License: MIT

## Maintainers

- Den Delimarsky (@localden)
- John Lam (@jflam)
