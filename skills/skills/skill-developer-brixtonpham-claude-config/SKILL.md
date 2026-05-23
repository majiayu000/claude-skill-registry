---
name: skill-developer
description: Skill system infrastructure manager. Create/modify skills, configure skill-rules.json, design trigger patterns, debug activation, implement hooks (UserPromptSubmit/PreToolUse). Scope: meta-level operations only - NOT domain content (UI/backend/workflows). Covers: YAML frontmatter, keyword/intent patterns, enforcement levels, progressive disclosure, 500-line rule, Anthropic best practices.
---

# Skill Developer Guide

## Purpose

Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.

## When to Use This Skill

Automatically activates when you mention:
- Creating or adding skills
- Improving, enhancing, or optimizing skills
- Refactoring or upgrading skills
- Modifying skill triggers or rules
- Understanding how skill activation works
- Debugging skill activation issues
- Working with skill-rules.json
- Hook system mechanics
- Claude Code best practices
- Progressive disclosure
- YAML frontmatter
- 500-line rule

## Context Awareness: What This Skill Covers

### ✅ This Skill is FOR (Meta-Level)

**Skill System Management:**
- Creating/modifying `.claude/skills/` directory contents
- Editing `skill-rules.json` configuration
- Writing/updating `SKILL.md` files
- Designing trigger patterns (keywords, intent patterns)
- Understanding hook mechanisms (UserPromptSubmit, PreToolUse)
- Skill activation and debugging
- Progressive disclosure patterns
- Anthropic best practices (500-line rule, etc.)

**Keywords That Trigger This Skill:**
- "skill triggers", "skill activation", "skill keywords"
- "intent patterns", "promptTriggers", "enforcement levels"
- "skill-rules.json", "SKILL.md", "skill frontmatter"
- "UserPromptSubmit", "PreToolUse", "hook system"
- "progressive disclosure", "500-line rule"
- "skill metadata", "trigger conditions"

### ❌ This Skill is NOT FOR (Domain-Specific Content)

**UI/Frontend Development:**
- Use `ui-design-system` skill for: TailwindCSS, Radix UI, shadcn/ui, design tokens, OKLCH colors, component libraries

**Backend Development:**
- Use other skills for: API design, database patterns, server architecture

**Documentation Discovery:**
- Use `docs-seeker` skill for: Finding llms.txt, searching documentation, library references

**Git Workflows:**
- Use `git-workflow` skill for: Commits, branches, atomic commits, PR creation

**Other Domain Skills:**
- Each domain skill covers its specific topic (Docker, PostgreSQL, Cloudflare, etc.)

### 🎯 Clear Distinction Examples

| User Query | Correct Skill | Why |
|------------|---------------|-----|
| "How do skill triggers work?" | ✅ skill-developer | Meta-level: about skill system |
| "Add keywords to ui-design-system" | ✅ skill-developer | Modifying skill configuration |
| "What are design tokens?" | ❌ ui-design-system | Domain content, not skill system |
| "How to use OKLCH colors?" | ❌ ui-design-system | UI/frontend topic |
| "Create a new skill for Docker" | ✅ skill-developer | Creating skill infrastructure |
| "How to containerize app?" | ❌ docker skill | Domain content |
| "Update skill-rules.json keywords" | ✅ skill-developer | Skill system configuration |
| "What are naming conventions for design tokens?" | ❌ ui-design-system | UI design content |

### 🔍 Context-Aware Trigger Strategy

**Trigger When:**
- User explicitly mentions "skill" + system terms (triggers, keywords, rules, activation)
- User is working on `.claude/skills/` directory
- User asks about hook mechanisms or skill architecture
- User wants to create/modify/debug skills

**Don't Trigger When:**
- User asks domain-specific questions (even if they're about design systems, tokens, etc.)
- Generic terms like "naming conventions" without "skill" context
- Backend/frontend development questions
- General coding questions

**Key Principle:** This skill is **meta-level** (about skills themselves), not **domain-level** (about UI, backend, etc.)

---

## System Overview

### Two-Hook Architecture

**1. UserPromptSubmit Hook** (Proactive Suggestions)
- **File**: `.claude/hooks/skill-activation-prompt.ts`
- **Trigger**: BEFORE Claude sees user's prompt
- **Purpose**: Suggest relevant skills based on keywords + intent patterns
- **Method**: Injects formatted reminder as context (stdout → Claude's input)
- **Use Cases**: Topic-based skills, implicit work detection

**2. Stop Hook - Error Handling Reminder** (Gentle Reminders)
- **File**: `.claude/hooks/error-handling-reminder.ts`
- **Trigger**: AFTER Claude finishes responding
- **Purpose**: Gentle reminder to self-assess error handling in code written
- **Method**: Analyzes edited files for risky patterns, displays reminder if needed
- **Use Cases**: Error handling awareness without blocking friction

**Philosophy Change (2025-10-27):** We moved away from blocking PreToolUse for Sentry/error handling. Instead, use gentle post-response reminders that don't block workflow but maintain code quality awareness.

### Configuration File

**Location**: `.claude/skills/skill-rules.json`

Defines:
- All skills and their trigger conditions
- Enforcement levels (block, suggest, warn)
- File path patterns (glob)
- Content detection patterns (regex)
- Skip conditions (session tracking, file markers, env vars)

---

## Skill Types

### 1. Guardrail Skills

**Purpose:** Enforce critical best practices that prevent errors

**Characteristics:**
- Type: `"guardrail"`
- Enforcement: `"block"`
- Priority: `"critical"` or `"high"`
- Block file edits until skill used
- Prevent common mistakes (column names, critical errors)
- Session-aware (don't repeat nag in same session)

**Examples:**
- `database-verification` - Verify table/column names before Prisma queries
- `frontend-dev-guidelines` - Enforce React/TypeScript patterns

**When to Use:**
- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues

### 2. Domain Skills

**Purpose:** Provide comprehensive guidance for specific areas

**Characteristics:**
- Type: `"domain"`
- Enforcement: `"suggest"`
- Priority: `"high"` or `"medium"`
- Advisory, not mandatory
- Topic or domain-specific
- Comprehensive documentation

**Examples:**
- `backend-dev-guidelines` - Node.js/Express/TypeScript patterns
- `frontend-dev-guidelines` - React/TypeScript best practices
- `error-tracking` - Sentry integration guidance

**When to Use:**
- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns
- How-to guides

---

## Quick Start: Creating a New Skill

### Step 1: Create Skill File

**Location:** `.claude/skills/{skill-name}/SKILL.md`

**Template:**
```markdown
---
name: my-new-skill
description: Brief description including keywords that trigger this skill. Mention topics, file types, and use cases. Be explicit about trigger terms.
---

# My New Skill

## Purpose
What this skill helps with

## When to Use
Specific scenarios and conditions

## Key Information
The actual guidance, documentation, patterns, examples
```

**Best Practices:**
- ✅ **Name**: Lowercase, hyphens, gerund form (verb + -ing) preferred
- ✅ **Description**: Include ALL trigger keywords/phrases (max 1024 chars)
- ✅ **Content**: Under 500 lines - use reference files for details
- ✅ **Examples**: Real code examples
- ✅ **Structure**: Clear headings, lists, code blocks

### Step 2: Add to skill-rules.json

See [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md) for complete schema.

**Basic Template:**
```json
{
  "my-new-skill": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?something"]
    }
  }
}
```

### Step 3: Test Triggers

**Test UserPromptSubmit:**
```bash
echo '{"session_id":"test","prompt":"your test prompt"}' | \
  npx tsx .claude/hooks/skill-activation-prompt.ts
```

**Test PreToolUse:**
```bash
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"session_id":"test","tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

### Step 4: Refine Patterns

Based on testing:
- Add missing keywords
- Refine intent patterns to reduce false positives
- Adjust file path patterns
- Test content patterns against actual files

### Step 5: Follow Anthropic Best Practices

✅ Keep SKILL.md under 500 lines
✅ Use progressive disclosure with reference files
✅ Add table of contents to reference files > 100 lines
✅ Write detailed description with trigger keywords
✅ Test with 3+ real scenarios before documenting
✅ Iterate based on actual usage

---

## Enforcement Levels

### BLOCK (Critical Guardrails)

- Physically prevents Edit/Write tool execution
- Exit code 2 from hook, stderr → Claude
- Claude sees message and must use skill to proceed
- **Use For**: Critical mistakes, data integrity, security issues

**Example:** Database column name verification

### SUGGEST (Recommended)

- Reminder injected before Claude sees prompt
- Claude is aware of relevant skills
- Not enforced, just advisory
- **Use For**: Domain guidance, best practices, how-to guides

**Example:** Frontend development guidelines

### WARN (Optional)

- Low priority suggestions
- Advisory only, minimal enforcement
- **Use For**: Nice-to-have suggestions, informational reminders

**Rarely used** - most skills are either BLOCK or SUGGEST.

---

## Skip Conditions & User Control

### 1. Session Tracking

**Purpose:** Don't nag repeatedly in same session

**How it works:**
- First edit → Hook blocks, updates session state
- Second edit (same session) → Hook allows
- Different session → Blocks again

**State File:** `.claude/hooks/state/skills-used-{session_id}.json`

### 2. File Markers

**Purpose:** Permanent skip for verified files

**Marker:** `// @skip-validation`

**Usage:**
```typescript
// @skip-validation
import { PrismaService } from './prisma';
// This file has been manually verified
```

**NOTE:** Use sparingly - defeats the purpose if overused

### 3. Environment Variables

**Purpose:** Emergency disable, temporary override

**Global disable:**
```bash
export SKIP_SKILL_GUARDRAILS=true  # Disables ALL PreToolUse blocks
```

**Skill-specific:**
```bash
export SKIP_DB_VERIFICATION=true
export SKIP_ERROR_REMINDER=true
```

---

## Enhancing Existing Skills

### When to Enhance Skills

Enhance skills when they have:
- Verbose content (SKILL.md >500 lines or >5k words)
- Poor structure or unclear organization
- Second-person voice ("you should/can/will")
- Missing or vague examples
- Unused files or duplicated content
- Vague metadata or descriptions
- Quality issues affecting effectiveness

### Enhancement Principles

1. **Conciseness**: Move details to reference files
2. **Direct Voice**: Use imperative/infinitive (NOT second person)
3. **Clear Structure**: Apply consistent patterns
4. **XML Integration**: Use tags for constraints/requirements
5. **Resource Optimization**: Organize scripts/references/assets properly

### Enhancement Process

**Step 1: Analysis**
- Read complete skill (SKILL.md + all resources)
- Identify quality issues across all dimensions
- Note structural problems and verbosity

**Step 2: Metadata Enhancement**
- Ensure kebab-case naming
- Write comprehensive description (30-60 words, third-person voice)
- Include specific trigger keywords and scenarios

**Step 3: Voice Correction**
- Eliminate "you should/can/will" phrases
- Convert to imperative: "Use X to...", "Process files by..."
- Remove filler words: "simply", "just", "basically"
- Use active voice throughout

**Step 4: Structural Optimization**
Apply appropriate pattern:
- **Workflow-based**: Sequential processes
- **Task-based**: Multiple discrete operations
- **Reference-based**: Standards and specifications
- **Capabilities-based**: Integrated feature systems

**Step 5: Content Refinement**
- Add concrete before/after examples
- Use XML tags for constraints, requirements, format
- Keep main instructions in natural language
- Reference bundled resources with usage instructions

**Step 6: Resource Organization**
- `scripts/` - Executable automation code
- `references/` - Detailed documentation
- `assets/` - Templates and boilerplate
- Delete unused example files
- Eliminate duplication

**Step 7: Size Reduction**
- Move comprehensive docs to references/
- Add grep patterns for finding content
- Implement progressive disclosure
- Target <500 lines in SKILL.md

### Enhancement Examples

**Voice Correction:**
```markdown
# Before
You should use this function when you need to process files.

# After
Process files using this function.
```

**Structure with XML:**
```markdown
# Before
This helps with data analysis.

# After
Analyze datasets to identify key insights and patterns.

<requirements>
- Highlight statistically significant findings
- Identify temporal trends and correlations
- Note anomalies or outliers
</requirements>
```

**Progressive Disclosure:**
```markdown
# Before (all in SKILL.md)
## Complete API Reference
[2000 words of documentation...]

# After (SKILL.md references external file)
## Resources
See [API_REFERENCE.md](references/api_reference.md) for complete API documentation.

To find specific endpoints:
grep -i "endpoint_name" references/api_reference.md
```

### Enhancement Checklist

**Metadata:**
- [ ] Kebab-case naming
- [ ] Comprehensive description (30-60 words)
- [ ] Third-person voice
- [ ] Specific triggers

**Content:**
- [ ] SKILL.md <500 lines
- [ ] Imperative/infinitive voice
- [ ] No second-person phrases
- [ ] Concrete examples
- [ ] XML tags for structure

**Resources:**
- [ ] Organized by type (scripts/references/assets)
- [ ] No duplication with SKILL.md
- [ ] Unused files deleted

**Quality:**
- [ ] Clear and actionable
- [ ] No TODOs remaining
- [ ] Ready for use

---

## Testing Checklist

When creating a new skill, verify:

- [ ] Skill file created in `.claude/skills/{name}/SKILL.md`
- [ ] Proper frontmatter with name and description
- [ ] Entry added to `skill-rules.json`
- [ ] Keywords tested with real prompts
- [ ] Intent patterns tested with variations
- [ ] File path patterns tested with actual files
- [ ] Content patterns tested against file contents
- [ ] Block message is clear and actionable (if guardrail)
- [ ] Skip conditions configured appropriately
- [ ] Priority level matches importance
- [ ] No false positives in testing
- [ ] No false negatives in testing
- [ ] Performance is acceptable (<100ms or <200ms)
- [ ] JSON syntax validated: `jq . skill-rules.json`
- [ ] **SKILL.md under 500 lines** ⭐
- [ ] Reference files created if needed
- [ ] Table of contents added to files > 100 lines

---

## Reference Files

For detailed information on specific topics, see:

### [TRIGGER_TYPES.md](TRIGGER_TYPES.md)
Complete guide to all trigger types:
- Keyword triggers (explicit topic matching)
- Intent patterns (implicit action detection)
- File path triggers (glob patterns)
- Content patterns (regex in files)
- Best practices and examples for each
- Common pitfalls and testing strategies

### [SKILL_RULES_REFERENCE.md](SKILL_RULES_REFERENCE.md)
Complete skill-rules.json schema:
- Full TypeScript interface definitions
- Field-by-field explanations
- Complete guardrail skill example
- Complete domain skill example
- Validation guide and common errors

### [HOOK_MECHANISMS.md](HOOK_MECHANISMS.md)
Deep dive into hook internals:
- UserPromptSubmit flow (detailed)
- PreToolUse flow (detailed)
- Exit code behavior table (CRITICAL)
- Session state management
- Performance considerations

### [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
Comprehensive debugging guide:
- Skill not triggering (UserPromptSubmit)
- PreToolUse not blocking
- False positives (too many triggers)
- Hook not executing at all
- Performance issues

### [PATTERNS_LIBRARY.md](PATTERNS_LIBRARY.md)
Ready-to-use pattern collection:
- Intent pattern library (regex)
- File path pattern library (glob)
- Content pattern library (regex)
- Organized by use case
- Copy-paste ready

### [ADVANCED.md](ADVANCED.md)
Future enhancements and ideas:
- Dynamic rule updates
- Skill dependencies
- Conditional enforcement
- Skill analytics
- Skill versioning

---

## Quick Reference Summary

### Create New Skill (5 Steps)

1. Create `.claude/skills/{name}/SKILL.md` with frontmatter
2. Add entry to `.claude/skills/skill-rules.json`
3. Test with `npx tsx` commands
4. Refine patterns based on testing
5. Keep SKILL.md under 500 lines

### Trigger Types

- **Keywords**: Explicit topic mentions
- **Intent**: Implicit action detection
- **File Paths**: Location-based activation
- **Content**: Technology-specific detection

See [TRIGGER_TYPES.md](TRIGGER_TYPES.md) for complete details.

### Enforcement

- **BLOCK**: Exit code 2, critical only
- **SUGGEST**: Inject context, most common
- **WARN**: Advisory, rarely used

### Skip Conditions

- **Session tracking**: Automatic (prevents repeated nags)
- **File markers**: `// @skip-validation` (permanent skip)
- **Env vars**: `SKIP_SKILL_GUARDRAILS` (emergency disable)

### Anthropic Best Practices

✅ **500-line rule**: Keep SKILL.md under 500 lines
✅ **Progressive disclosure**: Use reference files for details
✅ **Table of contents**: Add to reference files > 100 lines
✅ **One level deep**: Don't nest references deeply
✅ **Rich descriptions**: Include all trigger keywords (max 1024 chars)
✅ **Test first**: Build 3+ evaluations before extensive documentation
✅ **Gerund naming**: Prefer verb + -ing (e.g., "processing-pdfs")

### Troubleshoot

Test hooks manually:
```bash
# UserPromptSubmit
echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for complete debugging guide.

---

## Related Files

**Configuration:**
- `.claude/skills/skill-rules.json` - Master configuration
- `.claude/hooks/state/` - Session tracking
- `.claude/settings.json` - Hook registration

**Hooks:**
- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Stop event (gentle reminders)

**All Skills:**
- `.claude/skills/*/SKILL.md` - Skill content files

---

**Skill Status**: COMPLETE - Restructured following Anthropic best practices ✅
**Line Count**: < 500 (following 500-line rule) ✅
**Progressive Disclosure**: Reference files for detailed information ✅

**Next**: Create more skills, refine patterns based on usage
