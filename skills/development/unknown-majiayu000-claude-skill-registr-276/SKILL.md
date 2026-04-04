---
name: single-source-validator
description: ENFORCEMENT tool that detects when Skills automation is duplicated in agent definitions, lessons learned, or process docs. Prevents "single source of truth nightmare" by finding bash commands, step-by-step procedures, or process descriptions that replicate Skills. BLOCKING AUTHORITY - workflow cannot complete with violations.
---

# Single Source of Truth Validator Skill

**Purpose**: ENFORCE single source of truth for Skills - prevent duplication nightmare.

**When to Use**:
- After creating any new Skill
- Before Phase 5 finalization (MANDATORY)
- When updating agent definitions
- When updating lessons learned
- During periodic audits (monthly)

## 🚨 CRITICAL: ENFORCEMENT MECHANISM

**This skill has BLOCKING AUTHORITY.**

**If violations found:**
- ❌ Phase 5 validation FAILS
- ❌ Workflow CANNOT complete
- ❌ Changes MUST NOT be committed

**Why this matters:**
- Skills = ONLY source of automation
- All other docs REFERENCE skills, never duplicate
- Agents ignore guides when procedures are scattered
- User feedback: "SUPER CRITICAL" - duplication causes nightmare

---

## Single Source of Truth Architecture

```
SKILLS (/.claude/skills/*.md)
    Automation ONLY
    Executable bash scripts
    Zero duplication
         ↑
         |
    Referenced by
         |
         ↓
AGENT DEFINITIONS (/.claude/agents/*.md)
    Role + Tools + Skill References
    "Use skill X for Y"
    NEVER duplicate procedures

LESSONS LEARNED (/docs/lessons-learned/*.md)
    Problem → Solution → Example
    "See: /.claude/skills/X.md"
    NEVER duplicate procedures

PROCESS DOCS (/docs/standards-processes/*.md)
    Workflow + References
    "Automation: /.claude/skills/X.md"
    NEVER duplicate procedures
```

---

## What This Validates

This skill checks for **8 types** of single-source violations:

1. **Bash Command Duplication** - Exact bash commands from skills appearing in agent definitions, lessons learned, or process docs
2. **Step-by-Step Procedures** - Numbered or bulleted procedure steps duplicating skill automation
3. **Hardcoded Skill Paths** - Direct file path references (/.claude/skills/X.md) instead of skill name references
4. **Detailed Agent Skill Sections** - Agent definitions with When:/What:/Location: patterns (should be reference-only)
5. **Procedural Keyword Duplication** - Skill-specific procedures duplicated in other documents
6. **Missing Proper References** - Documents should say "Use X skill" or "See SKILLS-REGISTRY.md"
7. **Bash Scripts in Non-Skill Docs** - Bash code blocks in guides without skill references (NEW)
8. **Procedure Sections Without Skill References** - "How to", "Steps to", "Procedure" sections not referencing skills (NEW)

**Detection Levels:**
- ❌ **VIOLATIONS** (CRITICAL) - Exact duplications, blocks Phase 5
- ⚠️ **WARNINGS** - Potential issues, manual review recommended

---

## How to Use This Skill

### From Command Line

```bash
# Validate specific skill for duplication
bash .claude/skills/single-source-validator/execute.sh container-restart

# Validate with CRITICAL severity (default - blocks on warnings)
bash .claude/skills/single-source-validator/execute.sh staging-deploy CRITICAL

# Validate with WARNING severity (warnings don't block)
bash .claude/skills/single-source-validator/execute.sh phase-1-validator WARNING

# Show help and usage information
bash .claude/skills/single-source-validator/execute.sh --help
```

### From Claude Code

```
Use the single-source-validator skill to check if [skill-name] has any duplication violations
```

### Common Usage Patterns

**After creating new skill:**
```bash
bash .claude/skills/single-source-validator/execute.sh my-new-skill
```

**Before Phase 5 finalization (validate all skills):**
```bash
for skill_dir in .claude/skills/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        bash .claude/skills/single-source-validator/execute.sh "$skill_name"
    fi
done
```

**During periodic audit:**
```bash
bash .claude/skills/single-source-validator/execute.sh container-restart WARNING
```

---

## Proper Reference Format

### ❌ WRONG - Duplication

**Agent definition** (test-executor.md):
```markdown
## Before E2E Tests

Run these steps:
1. Stop containers: `docker-compose down`
2. Start with dev overlay: `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`
3. Wait 15 seconds
4. Check health: `curl http://localhost:5173`
```

**Why wrong**: Duplicates bash commands from restart-dev-containers skill

### ✅ CORRECT - Reference

**Agent definition** (test-executor.md):
```markdown
## Before E2E Tests

**MANDATORY**: Use restart-dev-containers skill to ensure environment is healthy.

**See**: `/.claude/skills/container-restart.md`

The skill automatically:
- Stops containers correctly
- Starts with dev overlay
- Checks compilation errors
- Verifies health endpoints
```

**Why correct**: References skill, provides context, no duplication

---

## Lessons Learned Format

### ❌ WRONG - Duplication

**Lesson** (test-executor-lessons-learned.md):
```markdown
## Problem: E2E Tests Fail

**Solution**:
1. Run `docker-compose down`
2. Run `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`
3. Check logs for compilation errors
4. Verify health endpoints
```

**Why wrong**: Step-by-step procedure duplicates skill

### ✅ CORRECT - Reference

**Lesson** (test-executor-lessons-learned.md):
```markdown
## Problem: E2E Tests Fail with "Element Not Found"

**Root Cause**: Container shows "Up" but code has compilation errors inside.

**Solution**: Use `restart-dev-containers` skill before E2E tests.

The skill automatically checks for compilation errors and verifies health.

**See**: `/.claude/skills/container-restart.md`

**Example**:
```bash
# In test-executor workflow
bash .claude/skills/container-restart.md
# Then run E2E tests
npm run test:e2e
```
```

**Why correct**: Explains problem/solution, references skill, shows usage example

---

## Process Documentation Format

### ❌ WRONG - Duplication

**Process doc** (docker-operations-guide.md):
```markdown
## Container Restart Procedure

Steps:
1. Stop: `docker-compose -f docker-compose.yml -f docker-compose.dev.yml down`
2. Start: `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d`
3. Verify: Check container logs for errors
4. Health: Test all endpoints
```

**Why wrong**: Detailed procedure duplicates skill automation

### ✅ CORRECT - Reference

**Process doc** (docker-operations-guide.md):
```markdown
## Container Restart Procedure

**Automation**: `/.claude/skills/container-restart.md`

The skill provides automated container restart with:
- Correct docker-compose commands (dev overlay)
- Compilation error checking (critical for E2E tests)
- Health endpoint verification
- Database seed data validation

**When to use**: Before E2E tests, after code changes, when containers unhealthy

**Manual procedure**: See skill file for troubleshooting steps if automation fails
```

**Why correct**: References skill as automation, provides context, no duplication

---

## Integration with Phase 5 Validator

**Update to phase-5-validator.md**:

```bash
# Step: Check for single source of truth violations
echo "Checking single source of truth compliance..."

# Get list of all skills
SKILLS=$(ls /.claude/skills/*.md 2>/dev/null | grep -v "README.md" || true)

for SKILL_FILE in $SKILLS; do
    SKILL_NAME=$(basename "$SKILL_FILE" .md)

    echo "Validating skill: $SKILL_NAME"

    # Run validator
    bash /.claude/skills/single-source-validator.md "$SKILL_NAME" CRITICAL

    if [ $? -ne 0 ]; then
        echo "❌ VIOLATION: Duplication detected for skill: $SKILL_NAME"
        echo "Phase 5 validation BLOCKED"
        exit 1
    fi
done

echo "✅ All skills maintain single source of truth"
```

---

## Validation Workflow

### For New Skills

```bash
# 1. Create new skill
vim /.claude/skills/my-new-skill.md

# 2. Validate immediately
bash /.claude/skills/single-source-validator.md my-new-skill

# 3. Fix any violations before committing
```

### For Existing Skills

```bash
# Run validator on specific skill
bash /.claude/skills/single-source-validator.md container-restart

# Or validate all skills
for skill in /.claude/skills/*.md; do
    name=$(basename "$skill" .md)
    if [ "$name" != "README" ]; then
        bash /.claude/skills/single-source-validator.md "$name"
    fi
done
```

### Before Phase 5 Completion

```bash
# MANDATORY: Validate all skills
# Integrated into phase-5-validator.md
# Blocks workflow if violations found
```

---

## Common Violations & Fixes

### Violation 1: Agent Definition Has Bash Commands

**Violation**:
```
❌ VIOLATION: Agent 'test-executor' duplicates bash command
   File: /.claude/agents/test-executor.md
   Command: docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

**Fix**:
```bash
# 1. Open agent file
vim /.claude/agents/test-executor.md

# 2. Remove bash command section

# 3. Replace with reference
# Before E2E Tests
# Use restart-dev-containers skill: /.claude/skills/container-restart.md

# 4. Validate
bash /.claude/skills/single-source-validator.md container-restart
```

### Violation 2: Lessons Learned Has Procedure Steps

**Violation**:
```
❌ VIOLATION: Lesson 'test-executor-lessons-learned' duplicates bash command
   File: /docs/lessons-learned/test-executor-lessons-learned.md
   Command: docker logs witchcity-web --tail 50 | grep -i error
```

**Fix**:
```bash
# 1. Open lesson file
vim /docs/lessons-learned/test-executor-lessons-learned.md

# 2. Remove step-by-step procedure

# 3. Replace with Problem→Solution→Example format
## Problem: Containers start but tests fail
**Root Cause**: Compilation errors inside container
**Solution**: Use restart-dev-containers skill (checks compilation)
**See**: /.claude/skills/container-restart.md

# 4. Validate
bash /.claude/skills/single-source-validator.md container-restart
```

### Violation 3: Process Doc Duplicates Automation

**Violation**:
```
❌ VIOLATION: Process doc 'staging-deployment-guide' duplicates bash command
   File: /docs/functional-areas/deployment/staging-deployment-guide.md
   Command: docker build -f apps/api/Dockerfile -t registry.digitalocean.com/...
```

**Fix**:
```bash
# 1. Open process doc
vim /docs/functional-areas/deployment/staging-deployment-guide.md

# 2. Remove bash script section

# 3. Replace with reference to automation
**Automation**: /.claude/skills/staging-deploy.md
The skill handles: build, registry push, deployment, health checks

**Manual procedure**: This guide covers context and troubleshooting

# 4. Validate
bash /.claude/skills/single-source-validator.md staging-deploy
```

---

## Severity Levels

### CRITICAL (Default)
- **Exact bash command matches**: Always blocked
- **Step-by-step procedures**: Always blocked
- **Warnings treated as failures**: Yes
- **Use for**: Phase 5 validation, skill creation

### WARNING
- **Exact bash command matches**: Blocked
- **Step-by-step procedures**: Blocked
- **Warnings treated as failures**: No (manual review)
- **Use for**: Periodic audits, exploratory checks

### INFO
- **Exact bash command matches**: Reported only
- **Step-by-step procedures**: Reported only
- **Warnings treated as failures**: No
- **Use for**: Documentation reviews, planning

---

## Agent Instructions

### All Agents (Mandatory)

**Before modifying agent definitions, lessons learned, or process docs:**

```bash
# Check if skill exists for this procedure
ls /.claude/skills/ | grep -i "relevant-keyword"

# If skill exists, REFERENCE it, don't duplicate
echo "See: /.claude/skills/[skill-name].md" >> file.md

# If no skill exists and procedure is complex, CREATE SKILL FIRST
vim /.claude/skills/new-procedure.md

# Then reference from other docs
```

### Orchestrator (Phase 5)

**MANDATORY validation before finalization:**

```bash
# Run validator on ALL skills
echo "Validating single source of truth..."

for skill in /.claude/skills/*.md; do
    name=$(basename "$skill" .md)
    if [ "$name" != "README" ] && [ "$name" != "single-source-validator" ]; then
        bash /.claude/skills/single-source-validator.md "$name" CRITICAL
        if [ $? -ne 0 ]; then
            echo "❌ Phase 5 validation BLOCKED due to violations in: $name"
            exit 1
        fi
    fi
done

echo "✅ Single source of truth maintained across all skills"
```

### Librarian (File Organization)

**When creating/moving documentation:**

```bash
# Before creating new procedure doc
# 1. Check if skill exists
bash /.claude/skills/single-source-validator.md [relevant-skill] INFO

# 2. If skill exists, reference it
# 3. If no skill, consider if automation needed
# 4. If automation needed, create skill FIRST
```

---

## Metrics & Monitoring

### Success Metrics

- **Zero violations** in Phase 5 validation (target: 100%)
- **Skills referenced** vs **procedures duplicated** ratio (target: >95%)
- **Agent compliance** - agents using skills vs. duplicating (target: 100%)

### Monitoring Commands

```bash
# Count total skills
SKILL_COUNT=$(ls /.claude/skills/*.md | wc -l)

# Count references to skills
REF_COUNT=$(grep -r "\.claude/skills/" /.claude/agents /docs/lessons-learned /docs/standards-processes | wc -l)

# Count violations (should be 0)
VIOLATION_COUNT=0
for skill in /.claude/skills/*.md; do
    name=$(basename "$skill" .md)
    if [ "$name" != "README" ] && [ "$name" != "single-source-validator" ]; then
        bash /.claude/skills/single-source-validator.md "$name" CRITICAL > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            ((VIOLATION_COUNT++))
        fi
    fi
done

echo "Skills: $SKILL_COUNT"
echo "References: $REF_COUNT"
echo "Violations: $VIOLATION_COUNT"
```

---

## Troubleshooting

### Issue: Validator reports false positive

**Cause**: Skill and doc have similar bash command for different purpose

**Solution**:
1. Review context around command in both files
2. If different purpose, add comment in doc: `# Different from skill: [explanation]`
3. Run validator with WARNING severity for manual review

### Issue: Too many warnings, hard to review

**Cause**: Keyword-based detection is overly broad

**Solution**:
1. Focus on VIOLATIONS first (exact bash commands)
2. Review warnings manually during periodic audits
3. Refine keyword extraction logic if needed

### Issue: Validator missed duplication

**Cause**: Procedure rewritten in different style (paraphrased)

**Solution**:
1. Manual code review remains important
2. Validator catches exact duplicates, not paraphrases
3. Educate agents on spirit of single source of truth

---

## Version History

- **2025-11-04**: Created as ENFORCEMENT mechanism for single source of truth
- Addresses user feedback: "SUPER CRITICAL" - agents ignore guides when procedures scattered
- Provides BLOCKING AUTHORITY - workflow cannot complete with violations
- Integrated with phase-5-validator for mandatory validation

---

**Remember**: This skill has blocking authority. Zero tolerance for duplication. Skills are the ONLY source of automation.
