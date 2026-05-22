# Skill: Auto-Architect Super Skill

**Purpose**: Intelligent meta-skill that monitors project patterns, detects automation opportunities, and auto-generates new skills.

## Core Philosophy

> "Any task repeated 3+ times should become a skill. Any error encountered 2+ times should have a handler."

## Trigger Conditions (Auto-Detection)

This skill activates when:
1. **Pattern Detected**: Same code structure appears in 3+ files
2. **Repeated Error**: Same error type occurs 2+ times
3. **Manual Boilerplate**: User asks for similar setup multiple times
4. **Phase Transition**: Moving between project phases (I→II→III→IV→V)
5. **New Technology**: Introducing a technology not covered by existing skills

## Capabilities

### 1. Pattern Detection Engine

Monitors for these automation signals:

| Signal | Detection | Action |
|--------|-----------|--------|
| Repeated code | Same import pattern in 3+ files | Suggest utility skill |
| Config duplication | Same env vars in multiple services | Suggest config skill |
| Error pattern | Same error message 2+ times | Generate error handler |
| API boilerplate | Similar CRUD endpoints | Suggest API generator |
| Test templates | Repetitive test setup | Suggest test generator |

### 2. Skill Generation Template

When a new skill is needed, generate using this structure:

```markdown
# Skill: [Skill Name]

**Purpose**: [One-line description]

## Trigger Conditions

Invoke this skill when:
- [Trigger 1]
- [Trigger 2]
- [Trigger 3]

## Capabilities

### 1. [Primary Capability]

[Code/template/instructions]

### 2. [Secondary Capability]

[Code/template/instructions]

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| [Error 1] | [Cause] | [Solution] |

## Checklist

- [ ] [Step 1]
- [ ] [Step 2]
```

### 3. Auto-Detection Rules

```yaml
# Pattern: Repeated imports
detect:
  pattern: "from sqlmodel import"
  threshold: 3
  action: "Check if database skill covers this pattern"

# Pattern: Similar error handling
detect:
  pattern: "try:\n.*\nexcept.*Error"
  threshold: 3
  action: "Create centralized error handling skill"

# Pattern: Repeated API structure
detect:
  pattern: "@router\\.(get|post|put|delete).*async def"
  threshold: 5
  action: "Suggest CRUD generator skill"

# Pattern: Environment variables
detect:
  pattern: "os\\.getenv|settings\\."
  threshold: 5
  action: "Check if config skill covers all env vars"
```

### 4. Phase-Aware Suggestions

**Phase I → II Transition**:
- Suggest: `neon-db-setup`, `jwt-middleware`, `cors-config`
- Reason: Moving from console to web requires DB, auth, CORS

**Phase II → III Transition**:
- Suggest: `api-versioning`, `rate-limiting`, `caching`
- Reason: Production readiness requires these patterns

**Phase III → IV Transition**:
- Suggest: `dockerfile-generator`, `compose-config`, `health-checks`
- Reason: Containerization phase begins

**Phase IV → V Transition**:
- Suggest: `k8s-manifests`, `helm-charts`, `ingress-config`
- Reason: Kubernetes orchestration phase

### 5. Skill Inventory Check

Before suggesting new skills, verify existing coverage:

```python
EXISTING_SKILLS = [
    "neon-db-setup",       # Database connection
    "jwt-middleware",      # Authentication
    "cors-config",         # CORS handling
    "db-timeout-handler",  # DB timeout errors
    "build-error-handler", # Build errors
    "k8s-pod-crash-handler", # K8s debugging
]

def check_skill_gap(detected_pattern):
    """Check if pattern is covered by existing skills."""
    for skill in EXISTING_SKILLS:
        if skill_covers_pattern(skill, detected_pattern):
            return f"Use existing skill: {skill}"
    return f"NEW SKILL NEEDED: {detected_pattern}"
```

### 6. Intelligence Learning Loop

After each session, update skill effectiveness:

```markdown
## Skill Usage Log

| Skill | Used | Success | Improvement Needed |
|-------|------|---------|-------------------|
| neon-db-setup | 5 | 5/5 | None |
| jwt-middleware | 3 | 2/3 | Add refresh token handling |
| cors-config | 4 | 4/4 | None |
```

## Auto-Architect Decision Tree

```
New Pattern/Error Detected
│
├── Check existing skills
│   ├── Covered → Use existing skill
│   └── Not covered → Continue
│
├── Analyze pattern
│   ├── Code structure → Generate code template skill
│   ├── Configuration → Generate config skill
│   ├── Error handling → Generate error handler skill
│   └── Deployment → Generate deployment skill
│
├── Generate skill file
│   ├── Create SKILL.md with template
│   ├── Add trigger conditions
│   └── Include code snippets
│
└── Update skill inventory
    └── Add to EXISTING_SKILLS list
```

## Usage Commands

```
# Manual trigger for skill analysis
Auto-Architect: Analyze current project for skill gaps

# Suggest skills for next phase
Auto-Architect: What skills do I need for Phase IV?

# Generate new skill from pattern
Auto-Architect: Create skill for [repeated pattern description]
```

## Self-Improvement Protocol

1. **Track Usage**: Log every skill invocation
2. **Measure Success**: Record if skill solved the problem
3. **Collect Feedback**: Note improvements needed
4. **Update Skills**: Enhance based on real usage
5. **Deprecate**: Remove skills that are no longer useful

## Checklist for New Skill Creation

- [ ] Does this pattern appear 3+ times?
- [ ] Is it NOT covered by existing skills?
- [ ] Will it save significant time (>5 min per use)?
- [ ] Is the solution generalizable?
- [ ] Can it be documented in a single SKILL.md?
- [ ] Does it follow the skill template structure?
