---
name: using-skills
description: "Auto-loaded at session start via SessionStart hook. Teaches skill invocation protocol, tool selection rules (look-at for media, skills for workflows), agent delegation patterns, and enforcement mechanisms. NOT user-triggered - provides foundational skill usage discipline for all sessions."
user-invocable: false
disable-model-invocation: true
---

# Using Skills

**Invoke relevant skills BEFORE any response or action.**

This is non-negotiable. Even a 1% chance a skill applies requires checking.

## CRITICAL: Skill Already Loaded - DO NOT RE-INVOKE

<EXTREMELY-IMPORTANT>
**If you see a skill name in the current conversation turn (e.g., `<command-name>/dev</command-name>`), the skill is ALREADY LOADED.**

**DO NOT:**
- ❌ Use the Skill tool to invoke it again
- ❌ Say "I need to invoke the skill"
- ❌ Call `Skill(skill="dev")` or similar

**DO INSTEAD:**
- ✅ The skill instructions follow immediately in the next message
- ✅ Just proceed to the next step
- ✅ Follow the loaded skill's instructions directly

**If you catch yourself about to invoke a skill that's already loaded, STOP. Just go to the next step.**
</EXTREMELY-IMPORTANT>

## The Rule

```
User message arrives
    ↓
Is user explicitly invoking a skill (e.g., "use /dev")?
    ↓
YES → SKILL IS ALREADY LOADED
      ↓
      DO NOT invoke again with Skill tool
      ↓
      Proceed to next step (follow skill instructions)
NO  → Check: Does this match any skill trigger?
    ↓
YES → Invoke skill FIRST, then follow its protocol
NO  → Proceed normally
```

## Workflow Commands

Each workflow has two entry points — start fresh or re-enter mid-workflow:

| Start Fresh | Mid-Workflow | Purpose |
|-------------|-------------|---------|
| `/dev` | `/dev-debug` | Feature development (7 phases) / debug, fix, re-test |
| `/ds` | `/ds-fix` | Data analysis (5 phases) / wrong results, notebook errors, revisions |
| `/writing` | `/writing-revise` | Writing projects / apply review fixes, polish |

## Skill Triggers (Can Auto-Invoke)

| User Intent | Command | Trigger Words |
|-------------|---------|---------------|
| Bug/fix | `/dev-debug` | bug, broken, fix, doesn't work, crash, error, fails |
| Wrong results | `/ds-fix` | results wrong, notebook error, reviewer feedback, data changed |
| Writing | `/writing` | write, draft, document, essay, paper |
| **Media analysis** | **look-at** | describe image, analyze PDF, what's in this, screenshot, diagram |
| Create/edit skill | `workflows:skill-creator` | create skill, improve skill, edit skill, add enforcement, audit skill, SKILL.md |
| Create/edit workflow | `workflows:workflow-creator` | create workflow, design workflow, edit workflow, audit workflow, improve workflow |
| Create/edit plugin | `workflows:plugin-creator` | create plugin, scaffold plugin, new plugin, plugin structure, edit plugin |

## Red Flags - You're Skipping the Skill Check

If you think any of these, STOP:

| Thought | Reality |
|---------|---------|
| **"I need to invoke the skill properly"** | **If user said "use /dev", it's ALREADY LOADED. Just proceed.** |
| **"Let me invoke the skill first"** | **Check for `<command-name>` tag - it's already loaded if present** |
| **"I should use Skill tool for /dev"** | **NO. User invocation = already loaded = proceed to next step** |
| "This is just a simple question" | Simple questions don't involve reading code |
| "I'll gather information first" | That IS investigation - use the skill |
| "I know exactly what to do" | The skill provides structure you'll miss |
| "It's just one file" | Scope doesn't exempt you from process |
| "Let me quickly check..." | "Quickly" means skipping the workflow |
| **"I can read this image directly"** | **Use look-at to save context tokens** |

## Bug Reports - Mandatory Response

When user mentions a bug:

```
DO NOT:
1. Read code files
2. Investigate independently
3. "Take a look" without structure

INSTEAD:
1. Start ralph loop:
   ralph-loop: Start Ralph Loop in current session with bug debugging
   Skill(skill="ralph-loop:ralph-loop", args="Debug: [symptom] --max-iterations 15 --completion-promise FIXED")
2. Inside loop, follow /dev-debug protocol
```

**Any code reading before starting the workflow is a violation.**

## Skill Priority

When multiple skills could apply:

1. **Process skills first** - debugging, brainstorming determine approach
2. **Then implementation** - dev, ds, writing execute the approach

## How to Invoke

Use the Skill tool to invoke skills:

```bash
# dev-debug: Midpoint entry for dev workflow - debug, fix, re-test
Skill(skill="dev-debug")

# dev: Feature development workflow with 7 phases and TDD enforcement
Skill(skill="dev")

# ds: Data analysis workflow with 5 phases and output-first verification
Skill(skill="ds")
```

Or start ralph loop first for implementation/debug phases:

```bash
# ralph-loop: Per-task ralph loop pattern for implementation and debugging
Skill(skill="ralph-loop:ralph-loop", args="Task description --max-iterations 15")
```

## IRON LAW: Multimodal File Analysis

**NO READING IMAGES/PDFS WITH Read TOOL. USE look-at INSTEAD.**

### The Rule

```
User asks about image/PDF/media content
    ↓
Is it a media file requiring interpretation?
    ↓
YES → Use look-at skill (bash call to look_at.py)
NO  → Use Read tool for source code/text
```

### When to Use look-at

**ALWAYS use look-at for:**
- `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.heic` - Images
- `.pdf` - PDFs requiring content extraction
- `.mp4`, `.mov`, `.avi`, `.webm` - Videos
- `.mp3`, `.wav`, `.aac`, `.ogg` - Audio
- Any file where you need to UNDERSTAND content, not just see raw bytes

**Pattern:**
```bash
# look-at: Extract information from media file with specific goal
LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "/absolute/path/to/file" \
    --goal "What specific information to extract"
```

### When NOT to Use look-at

**Use Read tool instead for:**
- Source code files (`.py`, `.js`, `.rs`, etc.) - need exact formatting for editing
- Plain text files (`.txt`, `.md`, `.json`, etc.) - preserve exact content
- Config files requiring exact formatting preservation
- Any file that needs editing after reading

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can read images directly" | Read tool shows you the image, but wastes context tokens | Use look-at to extract ONLY what's needed |
| "It's just one small image" | Still uses 1000+ tokens in conversation context | look-at returns 50-200 tokens of extracted info |
| "I need to see the whole thing" | You can see it, user can't see what you see | Use look-at with specific goal |
| "look-at might miss details" | You can always fall back to Read if needed | Start with look-at, escalate if insufficient |
| "The user didn't ask for look-at" | look-at is FOR YOU, not the user | Use the right tool for the job |

### Red Flags - STOP If You Catch Yourself:

- **"Let me read this image..."** → NO. Use look-at.
- **"I'll use Read to see what's in the PDF..."** → NO. Use look-at.
- **"Just quickly checking this screenshot..."** → NO. Use look-at.
- **Passing image path to Read tool** → STOP. Use look-at instead.

### Cost & Context Benefits

- **Read tool on image:** ~1,000-5,000 context tokens
- **look-at extraction:** ~50-200 output tokens
- **Savings:** 95%+ token reduction
- **Speed:** Faster responses, less context bloat

### Example Usage

```bash
# look-at: Extract specific information from image file
LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "$HOME/Downloads/screenshot.png" \
    --goal "List all buttons and their labels"

# look-at: Analyze diagram to understand data flow
LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "$HOME/Documents/architecture.png" \
    --goal "Explain the data flow between components"

# look-at: Extract information from PDF document
LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "$HOME/Downloads/report.pdf" \
    --goal "Extract the executive summary section"
```

### Enforcement

**Using Read on images/PDFs when look-at should be used results in:**
1. Wasting context tokens unnecessarily
2. Making conversations slower
3. Ignoring available optimization tools
4. Violating the tool selection protocol

**Validate before calling Read:** Ask "Is this a media file?" If yes, invoke look-at instead.

## IRON LAW: Following Skill Instructions

**WHEN A SKILL LOADS, YOU MUST FOLLOW ITS EXACT INSTRUCTIONS.**

Skills contain specific patterns, required parameters, and enforcement rules. Skipping these requirements defeats the purpose of loading the skill.

### The Rule

```
Skill loads successfully
    ↓
Read the skill's requirements carefully
    ↓
Follow ALL instructions, including:
    - Required tool parameters (descriptions, timeouts, etc.)
    - Specific command patterns
    - Enforcement patterns (Iron Laws, Red Flags)
    - Step sequences
    ↓
Execute using the skill's exact patterns
```

### Common Violations

**Bash Description Parameter:**

When a skill requires `description` parameter on Bash calls (like look-at), you MUST include it:

```bash
# ❌ WRONG: No description parameter
LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "/path/to/file.pdf" \
    --goal "Extract title"

# ✅ CORRECT: With description parameter as skill requires
Bash(
    command='LOOK_AT=$(${CLAUDE_PLUGIN_ROOT}/skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" --file "/path/to/file.pdf" --goal "Extract title"',
    description="look-at: Extract title"
)
```

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The skill is just guidance" | Skills contain tested, required patterns | Follow the skill's exact instructions |
| "I know a better way" | Your way skips enforcement or optimization | Use the skill's pattern - it exists for a reason |
| "Description parameter is optional" | When skill says REQUIRED, it's required | Add the description parameter as instructed |
| "I'll add it if it fails" | You'll clutter the conversation with messy output first | Follow the pattern from the start |
| "It's just cosmetic" | Clean descriptions improve UX and debugging | Professional output requires following the pattern |

### Red Flags - STOP If You Catch Yourself:

- **About to call Bash without description when skill requires it** → STOP. Add the description parameter.
- **Thinking "I'll skip this requirement"** → STOP. Skills don't have optional requirements.
- **"The skill says to do X but I'll do Y"** → STOP. Follow the skill or don't load it.
- **Modifying the skill's pattern "to be simpler"** → STOP. The pattern exists for a reason.

### Why This Matters

**Skills encode:**
1. **Tested patterns** - Proven to work in production
2. **Optimization** - Context/token savings, clean output
3. **Enforcement** - Prevent common mistakes
4. **UX standards** - Consistent, professional output

**When you skip skill instructions:**
- ❌ You waste the effort of loading the skill
- ❌ You create messy, unprofessional output
- ❌ You miss optimizations (context savings, speed)
- ❌ You violate user expectations
- ❌ You make debugging harder

**The skill loaded for a reason - follow it completely.**

## IRON LAW: Creator Activity Routing

**NO CREATING OR SUBSTANTIALLY EDITING SKILLS, PLUGINS, OR WORKFLOWS WITHOUT THE WORKFLOWS WRAPPER.**

The workflows plugin provides wrapper skills that add two layers on top of built-in creator tools:
1. **Behavioral enforcement** — superpowers patterns (Iron Laws, rationalization tables, red flags, enforcement checklist audit)
2. **Mechanical enforcement** — PostToolUse hooks (`plugin-validate.py`, `validate-skill-paths.py`) that fire on every Write/Edit

Using built-in creators directly bypasses both layers. This applies globally — any project, not just the workflows plugin.

"Substantial" means: adding/removing sections, changing enforcement patterns, altering process flow, adding/modifying hooks. Typo fixes, version bumps, and single-line clarifications are exempt.

### The Rule

```
About to create or substantially edit a skill/plugin/workflow
    ↓
What type of creator activity?
    ↓
    +---> Skill creation/editing ------> Invoke workflows:skill-creator
    |
    +---> Workflow creation/editing ----> Invoke workflows:workflow-creator
    |
    +---> Plugin creation/editing ------> Invoke workflows:plugin-creator
    ↓
Follow the wrapper skill's full process
    ↓
DO NOT invoke built-in creators directly (skill-creator:skill-creator,
plugin-dev:skill-development, plugin-dev:plugin-structure, etc.)
```

### Creator Routing Table

| Activity | Route To | Wraps |
|----------|----------|-------|
| Create/edit a skill | `workflows:skill-creator` | `skill-creator:skill-creator` |
| Create/edit a workflow | `workflows:workflow-creator` | (standalone meta-tool) |
| Create/edit a plugin | `workflows:plugin-creator` | `plugin-dev:create-plugin` |

Trigger words: see Skill Triggers table above.

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I'll use the built-in creator directly / I know the patterns" | Built-in has no PostToolUse hooks — path errors and structural issues go uncaught. Knowing is not doing; hooks fire automatically, your memory does not | Invoke the workflows wrapper |
| "This is a simple/quick edit" | If changing process flow, hooks, or enforcement sections, it's substantial | Use the wrapper |
| "I'm not in the workflows project" | Wrappers apply globally — enforcement patterns matter everywhere | Invoke the workflows wrapper from any project |

### Red Flags - STOP If You Catch Yourself:

- **About to invoke a built-in creator directly** (`skill-creator:skill-creator`, `plugin-dev:*`, etc.) → STOP. Use the workflows wrapper.
- **Editing enforcement patterns without the wrapper** → STOP. This is exactly when the audit matters most.

## Advanced Agent Harnessing Patterns

**For detailed oh-my-opencode production patterns including:**
- Background + parallel execution (3x speedup)
- Tool restrictions for focused agents
- Structured delegation templates
- Failure recovery protocol
- Environment context injection
- Cost classification system
- Metadata-driven prompts

**See:** `references/agent-harnessing.md`

Quick reference:
- Tool restrictions: `references/tool-restrictions.md`
- Delegation template: `references/delegation-template.md`
- Metadata infrastructure: `references/skill-metadata.py`

Based on: [obra/superpowers](https://github.com/obra/superpowers) and oh-my-opencode production patterns.
