---
name: bulletproof-skill
description: Harden skills against rationalization and bypass behaviors
usage: /bulletproof-skill [skill-path] [--check loopholes|rationalizations|red-flags] [--interactive] [--report]
modules: [loophole-patterns, rationalization-guide]
---

# Bulletproof Skill Command

Systematically hardens skills against rationalization and bypass behaviors.

## When To Use

Use this command when you need to:
- Hardening skills against rationalization and bypass behaviors
- Identifying loopholes in skill language
- Generating rationalization tables
- Creating red flags lists
- Preparing skills for production

## When NOT To Use

Avoid this command if:
- Testing skill functionality - use /test-skill instead
- Evaluating skill quality - use /skills-eval instead
- Creating new skills - use /create-skill instead

## Usage

```bash
# Analyze skill for loopholes and rationalizations
/bulletproof-skill skills/my-skill

# Generate full bulletproofing report
/bulletproof-skill skills/my-skill --report

# Apply suggested fixes automatically (interactive)
/bulletproof-skill skills/my-skill --interactive

# Check specific aspects only
/bulletproof-skill skills/my-skill --check loopholes
/bulletproof-skill skills/my-skill --check rationalizations
/bulletproof-skill skills/my-skill --check red-flags
```

## What is Bulletproofing?

**Problem**: LLMs rationalize around constraints through:
- Vague language interpretation ("usually", "try to", "generally")
- "Spirit vs letter" compliance
- Perceived simplicity exemptions
- Memory-based shortcuts

**Solution**: Makes implicit requirements explicit, adds rationalization counters, closes loopholes.

## Workflow

### Step 1: Loophole Analysis
Scans skill content for weakness patterns:
- **Vague Language**: "usually", "try to", "generally", "should"
- **Missing Exceptions**: Undefined terms like "complex", "important"
- **Ambiguous Conditions**: Subjective criteria allowing bypass
- **Escape Hatches**: "Skip if not needed" without criteria

### Step 2: Rationalization Detection
Identifies common bypass patterns:
- Simplicity Bypass: "This is just a simple task"
- Memory Shortcut: "I remember what the skill says"
- Overkill Excuse: "The skill is overkill for this"
- Deferral: "Let me do this one thing first"
- Spirit vs Letter: "Technically following the approach"

### Step 3: Generate Rationalization Table
Creates comprehensive mapping of rationalizations → counters.

### Step 4: Create Red Flags List
Builds self-check questions to catch bypass attempts.

### Step 5: Suggest Counters
Provides explicit anti-rationalization language.

## Severity Levels

- **Critical**: Allows complete skill bypass (MUST fix)
- **High**: Enables significant deviation (SHOULD fix)
- **Medium**: Potential for selective application (CONSIDER fixing)
- **Low**: Minor wording improvements (OPTIONAL)

## Output

### Summary Report
```
LOOPHOLE ANALYSIS
Skill: skills/my-skill v0.2.0

VAGUE LANGUAGE (4 instances)
- Line 23: "Usually follow..." → "ALWAYS follow..."
- Line 47: "Try to establish..." → "MUST establish..."

Total Issues: 10 (Critical: 2, High: 5, Medium: 1, Low: 1)
Recommendation: Address all CRITICAL and HIGH before production
```

### Rationalization Table
```
| Thought | Reality | Counter |
|---------|---------|---------|
| "This is just simple" | Skills prevent scope creep | Apply EVERY time |
| "I remember the skill" | Memory drifts | Read CURRENT version |
```

### Red Flags List
```
## Red Flags - STOP and Check Skill
- "This is just a simple..."
- "I remember what it says..."
- "This doesn't need the full..."
```

## Detailed Guides

For comprehensive patterns and examples, see the bulletproof-skill source code and the abstract methodology framework.

## Best Practices

**When to Bulletproof**:
- Before skill goes to production
- After discovering bypass instances
- When skill compliance is critical
- During skill refactoring

**What Makes Good Bulletproofing**:
- Specific, measurable counters
- Complete rationalization coverage
- Clear red flags
- Actionable fixes

**Common Mistakes**:
- Over-bulletproofing simple skills
- Missing common rationalizations
- Vague counters that invite new rationalizations
- Not testing bulletproofed version

## Integration

```bash
# Typical workflow
/create-skill my-skill          # Create skill
/test-skill my-skill            # Test functionality
/bulletproof-skill my-skill     # Harden against bypass
/skills-eval my-skill           # Final validation
```

## See Also

- **/create-skill**: Create new skills
- **/test-skill**: Test skill functionality
- **/skills-eval**: Evaluate skill quality
- **abstract:methodology-curator**: Browse anti-rationalization frameworks
