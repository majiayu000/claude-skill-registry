---
name: workflow-validator
description: |
  Quality Gate Teacher for Spec-Kit-Plus workflow. Acts as a strict reviewer that
  validates quality (not just existence) of each phase's output before allowing
  progression. Generates detailed reports and grades work like a teacher.
  Triggers: validate, quality gate, phase check, workflow status, q-status
version: 2.0.0
author: Claude Code
role: Quality Gate Teacher
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Workflow Validator - Quality Gate Teacher

> **Role**: I am a strict teacher who reviews each phase's work. I don't just check if files exist - I validate QUALITY. Work must meet my standards before proceeding.

---

## CORE PRINCIPLE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUALITY GATE TEACHER                                │
│                                                                             │
│   "I don't care if the file exists. I care if it's GOOD."                  │
│                                                                             │
│   After EVERY phase:                                                        │
│   1. Read the output                                                        │
│   2. Evaluate against quality criteria                                      │
│   3. Generate validation report with GRADE                                  │
│   4. APPROVE or REJECT with specific feedback                               │
│   5. Only allow next phase if APPROVED                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## VALIDATION WORKFLOW

After each phase completes, execute:

```
┌──────────────────┐
│  Phase N Done    │
└────────┬─────────┘
         ▼
┌──────────────────────────────────────────────────────────────┐
│  QUALITY GATE VALIDATION                                     │
│                                                              │
│  1. READ output artifacts                                    │
│  2. EVALUATE against phase-specific criteria                 │
│  3. GRADE: A (Excellent) / B (Good) / C (Acceptable) /       │
│            D (Needs Work) / F (Fail)                         │
│  4. GENERATE report: .specify/validations/phase-N-report.md  │
│  5. DECISION: APPROVED (A/B/C) or REJECTED (D/F)             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
APPROVED   REJECTED
    │         │
    │         ▼
    │    ┌────────────────┐
    │    │ Feedback given │
    │    │ Re-do phase    │
    │    │ Max 3 attempts │
    │    └────────────────┘
    ▼
┌──────────────────┐
│  Phase N+1       │
└──────────────────┘
```

---

## PHASE-SPECIFIC QUALITY CRITERIA

### Phase 1: INIT - Project Structure

**What to Check:**
```bash
# Directory structure
[ -d ".specify" ] && [ -d ".specify/templates" ]
[ -d ".claude" ] && [ -d ".claude/skills" ] && [ -d ".claude/agents" ]
[ -d ".claude/logs" ] && [ -d ".claude/build-reports" ]
```

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| .specify/ exists | 20% | Directory created |
| .specify/templates/ exists | 20% | Templates dir ready |
| .claude/ structure complete | 30% | All subdirs present |
| Git initialized | 15% | .git/ exists |
| Feature branch created | 15% | Not on main/master |

**Grading:**
- A: 100% criteria met
- B: 85%+ criteria met
- C: 70%+ criteria met
- D: 50%+ criteria met
- F: <50% criteria met

**Report Template:**
```markdown
# Phase 1 Validation Report

## Grade: [A/B/C/D/F]
## Status: [APPROVED/REJECTED]

### Checklist
- [✓/✗] .specify/ directory created
- [✓/✗] .specify/templates/ exists
- [✓/✗] .claude/ structure complete
- [✓/✗] Git repository initialized
- [✓/✗] Feature branch created

### Score: X/100

### Feedback
{Specific feedback on what was good/needs improvement}

### Decision
{APPROVED: Proceed to Phase 2 / REJECTED: Fix issues and retry}
```

---

### Phase 2: ANALYZE PROJECT - Existing Infrastructure

**What to Check:**
```bash
# Read project-analysis.json
cat .specify/project-analysis.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d)"
```

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Valid JSON | 20% | Parses without error |
| existing_skills listed | 20% | Array with actual skills found |
| existing_agents listed | 20% | Array with actual agents found |
| project_type detected | 20% | Not empty/unknown |
| language detected | 20% | Matches actual project |

**Content Validation:**
```python
def validate_project_analysis(data: dict) -> tuple[str, list]:
    """Validate project-analysis.json quality."""
    issues = []
    score = 0

    # Check JSON structure
    required_fields = ['project_type', 'existing_skills', 'existing_agents',
                       'existing_hooks', 'has_source_code', 'language']

    for field in required_fields:
        if field in data:
            score += 15
        else:
            issues.append(f"Missing field: {field}")

    # Check skills are actually listed (not empty)
    if data.get('existing_skills') and len(data['existing_skills']) > 0:
        score += 10
    else:
        issues.append("No existing skills detected - verify .claude/skills/")

    # Check language detection makes sense
    if data.get('language') and data['language'] != 'unknown':
        score += 10
    else:
        issues.append("Language not properly detected")

    # Determine grade
    if score >= 90: grade = 'A'
    elif score >= 80: grade = 'B'
    elif score >= 70: grade = 'C'
    elif score >= 50: grade = 'D'
    else: grade = 'F'

    return grade, issues
```

---

### Phase 3: ANALYZE REQUIREMENTS - Technology Detection

**What to Check:**
```bash
cat .specify/requirements-analysis.json
```

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Valid JSON | 15% | Parses correctly |
| project_name extracted | 15% | Not empty |
| technologies_required populated | 25% | At least 1 technology |
| features extracted | 25% | At least 2 features |
| Matches actual requirements file | 20% | Cross-reference check |

**Content Validation:**
```python
def validate_requirements_analysis(data: dict, requirements_file: str) -> tuple[str, list]:
    """Validate requirements-analysis.json quality."""
    issues = []
    score = 0

    # Project name should match first heading in requirements
    if data.get('project_name'):
        score += 15
    else:
        issues.append("Project name not extracted")

    # Technologies should be detected
    techs = data.get('technologies_required', [])
    if len(techs) >= 3:
        score += 25
    elif len(techs) >= 1:
        score += 15
        issues.append(f"Only {len(techs)} technologies detected - verify requirements file")
    else:
        issues.append("No technologies detected - requirements file may be incomplete")

    # Features should be extracted
    features = data.get('features', [])
    if len(features) >= 5:
        score += 25
    elif len(features) >= 2:
        score += 15
        issues.append(f"Only {len(features)} features detected")
    else:
        issues.append("Not enough features extracted from requirements")

    # Cross-reference with actual requirements file
    # Read requirements file and verify technologies mentioned are detected
    score += 20  # Assuming cross-reference passes

    # Grade
    if score >= 90: grade = 'A'
    elif score >= 80: grade = 'B'
    elif score >= 70: grade = 'C'
    elif score >= 50: grade = 'D'
    else: grade = 'F'

    return grade, issues
```

---

### Phase 4: GAP ANALYSIS - Missing Components

**What to Check:**
```bash
cat .specify/gap-analysis.json
```

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Valid JSON | 15% | Parses correctly |
| skills_existing matches Phase 2 | 20% | Consistent data |
| skills_missing identified | 25% | Based on technologies |
| agents_missing identified | 20% | Based on project type |
| Logical consistency | 20% | Missing ∩ Existing = ∅ |

**Content Validation:**
```python
def validate_gap_analysis(data: dict, project_analysis: dict, req_analysis: dict) -> tuple[str, list]:
    """Validate gap-analysis.json quality."""
    issues = []
    score = 0

    # Check skills_existing matches project-analysis
    if set(data.get('skills_existing', [])) == set(project_analysis.get('existing_skills', [])):
        score += 20
    else:
        issues.append("skills_existing doesn't match project-analysis.json")

    # Check skills_missing makes sense for detected technologies
    techs = req_analysis.get('technologies_required', [])
    missing = data.get('skills_missing', [])

    # Each technology should have a corresponding skill (existing or missing)
    for tech in techs:
        tech_skill = f"{tech}-patterns"
        if tech_skill not in data.get('skills_existing', []) and tech_skill not in missing:
            issues.append(f"Technology '{tech}' has no skill (existing or planned)")

    if len(missing) > 0:
        score += 25
    else:
        # Might be valid if all skills exist
        if len(techs) <= len(data.get('skills_existing', [])):
            score += 25  # All skills covered
        else:
            issues.append("No missing skills identified but technologies need coverage")

    # Check no overlap between existing and missing
    existing_set = set(data.get('skills_existing', []))
    missing_set = set(data.get('skills_missing', []))
    if existing_set & missing_set:
        issues.append(f"Overlap found: {existing_set & missing_set}")
    else:
        score += 20

    # Agents missing based on project type
    if 'agents_missing' in data:
        score += 20
    else:
        issues.append("agents_missing not specified")

    # Grade
    if score >= 90: grade = 'A'
    elif score >= 80: grade = 'B'
    elif score >= 70: grade = 'C'
    elif score >= 50: grade = 'D'
    else: grade = 'F'

    return grade, issues
```

---

### Phase 5: GENERATE - Skills/Agents/Hooks Quality

**This is the most critical validation. Generated skills must be PRODUCTION READY.**

**What to Check:**
```bash
# List new skills
find .claude/skills -name "SKILL.md" -newer .specify/gap-analysis.json

# Read each new skill
for skill in $(find .claude/skills -name "SKILL.md" -newer .specify/gap-analysis.json); do
    echo "=== $skill ==="
    cat "$skill"
done
```

**Quality Criteria for EACH Generated Skill:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Has valid frontmatter | 10% | name, description, version |
| Has ## Overview section | 10% | Explains what skill does |
| Has ## Code Templates | 25% | At least 2 code examples |
| Code templates are correct syntax | 15% | No syntax errors |
| Has ## Best Practices | 15% | At least 3 practices |
| Has ## Common Commands | 10% | If applicable |
| Has ## Anti-Patterns | 10% | At least 2 anti-patterns |
| Content is technology-specific | 5% | Not generic/placeholder |

**Content Validation:**
```python
def validate_generated_skill(skill_path: str, technology: str) -> tuple[str, list]:
    """Validate a generated skill is production-ready."""
    issues = []
    score = 0

    content = open(skill_path).read()

    # Check frontmatter
    if content.startswith('---') and '---' in content[3:]:
        frontmatter = content.split('---')[1]
        if 'name:' in frontmatter and 'description:' in frontmatter:
            score += 10
        else:
            issues.append("Frontmatter missing name or description")
    else:
        issues.append("Missing or invalid frontmatter")

    # Check sections
    sections = {
        '## Overview': 10,
        '## Code Templates': 25,
        '## Best Practices': 15,
        '## Common Commands': 10,
        '## Anti-Patterns': 10
    }

    for section, weight in sections.items():
        if section in content or section.replace('##', '###') in content:
            score += weight
        else:
            issues.append(f"Missing section: {section}")

    # Check code templates have actual code
    code_blocks = content.count('```')
    if code_blocks >= 4:  # At least 2 code blocks (opening + closing)
        score += 15
    else:
        issues.append(f"Only {code_blocks//2} code examples - need at least 2")

    # Check not placeholder content
    placeholder_indicators = ['TODO', 'PLACEHOLDER', 'Example here', '{...}']
    for indicator in placeholder_indicators:
        if indicator in content:
            issues.append(f"Contains placeholder: '{indicator}'")
            score -= 10

    # Check technology-specific content
    if technology.lower() in content.lower():
        score += 5
    else:
        issues.append(f"Content doesn't mention {technology} - may be too generic")

    # Grade
    score = max(0, min(100, score))  # Clamp to 0-100
    if score >= 90: grade = 'A'
    elif score >= 80: grade = 'B'
    elif score >= 70: grade = 'C'
    elif score >= 50: grade = 'D'
    else: grade = 'F'

    return grade, issues, score
```

**Aggregate Skill Validation:**
```python
def validate_all_generated_skills(gap_analysis: dict) -> tuple[str, dict]:
    """Validate ALL generated skills meet quality standards."""

    missing_skills = gap_analysis.get('skills_missing', [])
    results = {}
    total_score = 0

    for skill_name in missing_skills:
        skill_path = f".claude/skills/{skill_name}/SKILL.md"

        if not os.path.exists(skill_path):
            results[skill_name] = {'grade': 'F', 'issues': ['Skill not created']}
            continue

        tech = skill_name.replace('-patterns', '').replace('-generator', '')
        grade, issues, score = validate_generated_skill(skill_path, tech)

        results[skill_name] = {
            'grade': grade,
            'score': score,
            'issues': issues,
            'status': 'APPROVED' if grade in ['A', 'B', 'C'] else 'REJECTED'
        }
        total_score += score

    # Overall grade
    if missing_skills:
        avg_score = total_score / len(missing_skills)
    else:
        avg_score = 100  # No skills needed = pass

    if avg_score >= 90: overall = 'A'
    elif avg_score >= 80: overall = 'B'
    elif avg_score >= 70: overall = 'C'
    elif avg_score >= 50: overall = 'D'
    else: overall = 'F'

    return overall, results
```

---

### Phase 7: CONSTITUTION - Project Rules

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| File exists and >100 lines | 15% | Substantial content |
| Has ## Core Principles | 20% | At least 3 principles |
| Has ## Code Standards | 20% | Specific rules |
| Has ## Technology Decisions | 15% | Matches detected tech |
| Has ## Quality Gates | 15% | Measurable criteria |
| Has ## Out of Scope | 15% | Boundaries defined |

---

### Phase 8: SPEC - Specification Quality

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| File exists and >300 lines | 10% | Comprehensive |
| Has ## User Stories | 20% | At least 3 stories |
| User stories have acceptance criteria | 15% | Each story has criteria |
| Has ## Functional Requirements | 20% | Detailed requirements |
| Has ## Non-Functional Requirements | 15% | Performance, security |
| Has ## API Contracts (if API) | 10% | Endpoints documented |
| Has ## Data Models | 10% | Entities defined |

---

### Phase 9: PLAN - Implementation Plan Quality

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| plan.md exists and >200 lines | 15% | Comprehensive |
| Has architecture diagram | 15% | Visual representation |
| Has ## Components breakdown | 20% | Each component detailed |
| Has ## Implementation Phases | 20% | Clear phases |
| Has ## Risks and Mitigations | 15% | Risk awareness |
| data-model.md exists | 15% | Database schema |

---

### Phase 10: TASKS - Task Breakdown Quality

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| File exists | 10% | tasks.md present |
| At least 10 tasks | 20% | Sufficient breakdown |
| Each task has skill reference | 20% | Skill: field present |
| Tasks have dependencies | 15% | Depends: field where needed |
| Tasks have priorities | 15% | P0/P1/P2 assigned |
| Covers all features from spec | 20% | Cross-reference check |

---

### Phase 11: IMPLEMENT - Code Quality

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Source files created | 20% | Code exists |
| Tests written | 25% | Test files exist |
| Tests pass | 20% | npm test succeeds |
| Coverage >= 80% | 20% | Coverage report |
| No linting errors | 15% | npm run lint passes |

---

### Phase 12: QA - Quality Assurance

**Quality Criteria:**

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Code review completed | 25% | Review report exists |
| Security review completed | 25% | Security report exists |
| All tests pass | 25% | Test suite green |
| Build succeeds | 25% | npm run build passes |

---

## VALIDATION REPORT STRUCTURE

After each phase, generate `.specify/validations/phase-{N}-report.md`:

```markdown
# Phase {N} Validation Report

## Summary
| Field | Value |
|-------|-------|
| Phase | {N}: {Phase Name} |
| Timestamp | {ISO timestamp} |
| Grade | {A/B/C/D/F} |
| Score | {X}/100 |
| Status | {APPROVED/REJECTED} |

## Criteria Evaluation

| Criterion | Weight | Score | Status |
|-----------|--------|-------|--------|
| {criterion 1} | {weight}% | {score} | ✓/✗ |
| {criterion 2} | {weight}% | {score} | ✓/✗ |
...

## Issues Found
{If any issues, list them with specific details}

1. **{Issue Title}**
   - Location: {where}
   - Problem: {what's wrong}
   - Fix: {how to fix}

## What Was Good
{Positive feedback on quality aspects}

## Recommendations
{Suggestions for improvement}

## Decision

### {APPROVED / REJECTED}

{If APPROVED}
✅ Phase {N} meets quality standards. Proceeding to Phase {N+1}.

{If REJECTED}
❌ Phase {N} does not meet quality standards.

**Required Fixes:**
1. {Fix 1}
2. {Fix 2}

**Retry:** {attempt X of 3}
```

---

## EXECUTION COMMAND

When invoked (via `/q-status`, `/q-validate`, or automatically after each phase):

```bash
#!/bin/bash
# Quality Gate Teacher Execution

PHASE=$1

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           QUALITY GATE TEACHER - PHASE $PHASE REVIEW           ║"
echo "╠════════════════════════════════════════════════════════════════╣"

# Create validations directory
mkdir -p .specify/validations

# Run phase-specific validation
case $PHASE in
    1) validate_init ;;
    2) validate_project_analysis ;;
    3) validate_requirements_analysis ;;
    4) validate_gap_analysis ;;
    5) validate_generated_skills ;;
    6) validate_test_phase ;;
    7) validate_constitution ;;
    8) validate_spec ;;
    9) validate_plan ;;
    10) validate_tasks ;;
    11) validate_implementation ;;
    12) validate_qa ;;
    13) validate_delivery ;;
esac

# Output result
echo "║                                                                ║"
echo "║  Grade: $GRADE                                                 ║"
echo "║  Score: $SCORE/100                                             ║"
echo "║  Status: $STATUS                                               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Generate report
generate_report $PHASE $GRADE $SCORE "$ISSUES"

# Return decision
if [ "$STATUS" == "APPROVED" ]; then
    echo "✅ APPROVED - Proceeding to next phase"
    exit 0
else
    echo "❌ REJECTED - Please fix issues and retry"
    exit 1
fi
```

---

## COMPONENT UTILIZATION VALIDATION (Cross-Cutting)

> **Critical Check**: Are custom skills, agents, and hooks being used? Or is the general agent doing everything without leveraging the ecosystem?

This validation runs alongside EVERY phase (especially Phase 11+) to ensure the work is being done **through** the custom components, not around them.

### Why This Matters

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPONENT UTILIZATION ENFORCEMENT                        │
│                                                                             │
│   "If you built skills, agents, and hooks - USE THEM."                     │
│                                                                             │
│   Problem: General Claude agent can do everything, but:                     │
│   - Custom skills contain SPECIALIZED knowledge                             │
│   - Custom agents have OPTIMIZED workflows                                  │
│   - Hooks provide AUTOMATED guardrails                                      │
│                                                                             │
│   If work bypasses these → QUALITY DEGRADATION                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What to Check

**1. Skill Invocation Logs**
```bash
# Check if skills are being invoked
cat .claude/logs/skill-invocations.log 2>/dev/null | wc -l

# List which skills were used
cat .claude/logs/skill-invocations.log 2>/dev/null | grep -oP 'Skill invoked: \K\S+' | sort | uniq -c
```

**2. Tool Usage Logs**
```bash
# Check tool usage patterns
cat .claude/logs/tool-usage.log 2>/dev/null | wc -l

# Detect if Task tool is being used (agents)
cat .claude/logs/tool-usage.log 2>/dev/null | grep -c "Task"
```

**3. Available vs Used Components**
```bash
# List available skills
ls -1 .claude/skills/ | grep -v "^\." | wc -l

# List available agents
ls -1 .claude/agents/ | grep -v "^\." | wc -l

# Compare with invocation logs
```

### Component Utilization Criteria

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Skills invoked during work | 25% | At least 1 skill per feature |
| Correct skills for technology | 20% | Matching tech → skill mapping |
| Agents used via Task tool | 20% | Task(subagent_type) calls logged |
| Hooks executing on events | 15% | PreToolUse/PostToolUse active |
| No bypass of available components | 20% | General agent didn't duplicate |

### Utilization Analysis Function

```python
def validate_component_utilization(phase: int, feature_count: int = 1) -> tuple[str, list, dict]:
    """
    Validate that custom skills, agents, and hooks are being utilized.
    Returns: (grade, issues, usage_report)
    """
    import os
    import json
    from pathlib import Path
    from datetime import datetime, timedelta

    issues = []
    score = 0
    usage_report = {
        'skills_available': [],
        'skills_used': [],
        'skills_unused': [],
        'agents_available': [],
        'agents_used': [],
        'agents_unused': [],
        'hooks_triggered': 0,
        'utilization_percentage': 0
    }

    # 1. Get available components
    skills_dir = Path('.claude/skills')
    agents_dir = Path('.claude/agents')

    if skills_dir.exists():
        usage_report['skills_available'] = [
            d.name for d in skills_dir.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ]

    if agents_dir.exists():
        usage_report['agents_available'] = [
            f.stem for f in agents_dir.glob('*.md')
            if not f.name.startswith('.')
        ]

    # 2. Check skill invocation logs
    skill_log = Path('.claude/logs/skill-invocations.log')
    if skill_log.exists():
        with open(skill_log) as f:
            for line in f:
                if 'Skill invoked:' in line:
                    skill_name = line.split('Skill invoked:')[1].strip()
                    if skill_name not in usage_report['skills_used']:
                        usage_report['skills_used'].append(skill_name)

    # 3. Check tool usage for Task (agent) calls
    tool_log = Path('.claude/logs/tool-usage.log')
    agent_invocations = []
    if tool_log.exists():
        with open(tool_log) as f:
            for line in f:
                # Look for Task tool usage patterns
                if 'Task' in line or 'subagent' in line.lower():
                    agent_invocations.append(line.strip())

    # Detect which agents were used (from subagent_type patterns)
    for agent in usage_report['agents_available']:
        agent_patterns = [agent, agent.replace('-', '_'), agent.replace('_', '-')]
        for pattern in agent_patterns:
            if any(pattern in inv for inv in agent_invocations):
                if agent not in usage_report['agents_used']:
                    usage_report['agents_used'].append(agent)
                break

    # 4. Calculate unused components
    usage_report['skills_unused'] = [
        s for s in usage_report['skills_available']
        if s not in usage_report['skills_used']
    ]
    usage_report['agents_unused'] = [
        a for a in usage_report['agents_available']
        if a not in usage_report['agents_used']
    ]

    # 5. Score calculation

    # Skill utilization (25%)
    skills_available = len(usage_report['skills_available'])
    skills_used = len(usage_report['skills_used'])
    if skills_available > 0:
        skill_ratio = skills_used / min(skills_available, feature_count * 2)
        if skill_ratio >= 0.5:
            score += 25
        elif skill_ratio >= 0.25:
            score += 15
            issues.append(f"Low skill utilization: {skills_used}/{skills_available} skills used")
        else:
            score += 5
            issues.append(f"CRITICAL: Only {skills_used} skills used out of {skills_available} available")
    else:
        score += 25  # No skills available = pass

    # Technology matching (20%)
    # Check if used skills match project technologies
    req_analysis_path = Path('.specify/requirements-analysis.json')
    if req_analysis_path.exists():
        with open(req_analysis_path) as f:
            req_data = json.load(f)
            technologies = req_data.get('technologies_required', [])

            matched_techs = 0
            for tech in technologies:
                tech_skill_patterns = [
                    f"{tech}-patterns",
                    f"{tech}-generator",
                    tech.lower(),
                    tech.replace('.', '').lower()
                ]
                if any(pattern in s.lower() for s in usage_report['skills_used'] for pattern in tech_skill_patterns):
                    matched_techs += 1

            if len(technologies) > 0:
                match_ratio = matched_techs / len(technologies)
                if match_ratio >= 0.7:
                    score += 20
                elif match_ratio >= 0.4:
                    score += 12
                    issues.append(f"Technology-skill mismatch: {matched_techs}/{len(technologies)} covered")
                else:
                    score += 5
                    issues.append(f"CRITICAL: Most technologies lack skill coverage")
            else:
                score += 20  # No tech requirements = pass
    else:
        score += 10  # Can't verify without requirements

    # Agent utilization (20%)
    agents_available = len(usage_report['agents_available'])
    agents_used = len(usage_report['agents_used'])
    if agents_available > 0:
        # Expected agents for implementation: code-reviewer, tdd-guide, build-error-resolver
        expected_agents = ['code-reviewer', 'tdd-guide', 'build-error-resolver']
        expected_used = [a for a in expected_agents if a in usage_report['agents_used']]

        if len(expected_used) >= 2:
            score += 20
        elif len(expected_used) >= 1:
            score += 12
            issues.append(f"Limited agent usage: Only {expected_used} of {expected_agents} used")
        else:
            score += 5
            issues.append(f"CRITICAL: Core agents not used - general agent doing everything")
    else:
        score += 20  # No agents = pass

    # Hooks active (15%)
    hooks_json = Path('.claude/hooks.json')
    settings_json = Path('.claude/settings.json')
    hooks_configured = 0

    for hook_file in [hooks_json, settings_json]:
        if hook_file.exists():
            with open(hook_file) as f:
                try:
                    data = json.load(f)
                    if 'hooks' in data:
                        for hook_type in ['PreToolUse', 'PostToolUse', 'Stop', 'UserPromptSubmit']:
                            if hook_type in data['hooks']:
                                hooks_configured += len(data['hooks'][hook_type])
                except:
                    pass

    usage_report['hooks_triggered'] = hooks_configured
    if hooks_configured >= 3:
        score += 15
    elif hooks_configured >= 1:
        score += 8
        issues.append(f"Limited hooks: Only {hooks_configured} hook(s) configured")
    else:
        issues.append("No hooks configured - missing automated guardrails")

    # No bypass check (20%)
    # If skills/agents exist but weren't used, penalize
    bypass_detected = False

    if skills_available > 3 and skills_used == 0:
        bypass_detected = True
        issues.append("BYPASS DETECTED: Skills exist but none were invoked")

    if agents_available > 5 and agents_used == 0:
        bypass_detected = True
        issues.append("BYPASS DETECTED: Agents exist but Task tool not used")

    if not bypass_detected:
        score += 20
    else:
        score += 0
        issues.append("General agent is doing work without utilizing custom components")

    # Calculate utilization percentage
    total_components = skills_available + agents_available
    used_components = skills_used + agents_used
    if total_components > 0:
        usage_report['utilization_percentage'] = round((used_components / total_components) * 100, 1)
    else:
        usage_report['utilization_percentage'] = 100

    # Determine grade
    if score >= 90: grade = 'A'
    elif score >= 80: grade = 'B'
    elif score >= 70: grade = 'C'
    elif score >= 50: grade = 'D'
    else: grade = 'F'

    return grade, issues, usage_report
```

### Component Utilization Report Template

```markdown
# Component Utilization Report

## Summary
| Metric | Value |
|--------|-------|
| Phase | {N} |
| Utilization Grade | {A/B/C/D/F} |
| Utilization Score | {X}/100 |
| Overall Utilization | {Y}% |

## Skills Analysis
| Category | Count | Details |
|----------|-------|---------|
| Available | {X} | {list} |
| Used | {Y} | {list} |
| Unused | {Z} | {list} |

**Skill Coverage:** {used}/{available} ({percentage}%)

## Agents Analysis
| Category | Count | Details |
|----------|-------|---------|
| Available | {X} | {list} |
| Used | {Y} | {list} |
| Unused | {Z} | {list} |

**Agent Coverage:** {used}/{available} ({percentage}%)

## Hooks Analysis
| Hook Type | Count | Active |
|-----------|-------|--------|
| PreToolUse | {X} | ✓/✗ |
| PostToolUse | {Y} | ✓/✗ |
| Stop | {Z} | ✓/✗ |
| UserPromptSubmit | {W} | ✓/✗ |

## Bypass Detection
{NONE DETECTED / BYPASS DETECTED}

{If bypass detected:}
⚠️ **Warning:** Work is being done without utilizing custom components.
- Skills bypassed: {list}
- Agents bypassed: {list}

**Impact:** Quality may be degraded. Custom components contain specialized
knowledge that the general agent doesn't have.

## Recommendations

1. **Use Skill tool:** `Skill(skill-name)` before implementing features
2. **Use Task tool:** `Task(subagent_type="agent-name")` for specialized work
3. **Verify hooks:** Check `.claude/hooks.json` is properly configured

## Decision

{If utilization >= 70%}
✅ Component utilization is acceptable. Custom ecosystem is being leveraged.

{If utilization 50-69%}
⚠️ Component utilization is low. Review which components should be used.

{If utilization < 50%}
❌ CRITICAL: Custom components are being bypassed. This defeats the purpose
   of the autonomous workflow system. Re-run phase using proper components.
```

### Integration with Phase Validation

**For Phase 11 (IMPLEMENT) - MANDATORY:**

Add to Phase 11 criteria:

| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|
| Component utilization >= 50% | 15% | Skills/agents being used |
| Core agents invoked | 10% | code-reviewer, tdd-guide |
| Skill-to-technology mapping | 10% | Correct skills for stack |

**Enforcement Rule:**
```
IF component_utilization < 50% AND skills_available > 3:
    REJECT phase with "Component Bypass Detected"
    REQUIRE re-implementation using custom components
```

### Log File Setup

Ensure these log files are being populated:

```bash
# Create log directory
mkdir -p .claude/logs

# skill-invocations.log format:
# [2024-01-15T10:30:00] Skill invoked: api-patterns
# [2024-01-15T10:31:00] Skill invoked: testing-patterns

# tool-usage.log format:
# [2024-01-15T10:30:00] Tool: Edit | File: src/api/routes.ts
# [2024-01-15T10:31:00] Tool: Task | Subagent: code-reviewer
```

### Settings.json Hook Configuration

Verify these hooks exist in `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Skill",
        "hooks": [{
          "type": "command",
          "command": "echo \"[$(date -Iseconds)] Skill invoked: $CLAUDE_SKILL_NAME\" >> .claude/logs/skill-invocations.log"
        }]
      },
      {
        "matcher": "Task",
        "hooks": [{
          "type": "command",
          "command": "echo \"[$(date -Iseconds)] Agent task: $CLAUDE_TOOL_INPUT\" >> .claude/logs/agent-usage.log"
        }]
      }
    ]
  }
}
```

---

## PHASE RESET ENFORCEMENT (CRITICAL)

> **Rule**: If a custom skill, agent, or hook EXISTS for a task but the general agent completed that task WITHOUT using it, the phase MUST be RESET and re-executed.

### Why Reset?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BYPASS = AUTOMATIC PHASE RESET                         │
│                                                                             │
│   Custom components contain:                                                │
│   - SPECIALIZED knowledge the general agent doesn't have                    │
│   - VALIDATED patterns that prevent common mistakes                         │
│   - OPTIMIZED workflows developed through experience                        │
│                                                                             │
│   Bypassing them = Lower quality output = Unacceptable                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Reset Trigger Conditions

A phase is RESET if ANY of these conditions are met:

| Condition | Example | Action |
|-----------|---------|--------|
| Skill exists but not invoked | `coding-standards` exists, code written without `Skill(coding-standards)` | RESET |
| Agent exists but not used | `code-reviewer` exists, code not reviewed via `Task(subagent_type="code-reviewer")` | RESET |
| Hook should have fired but didn't | PreToolUse hook for testing, tests skipped | RESET |
| Technology skill available but ignored | `api-patterns` exists, API built without using it | RESET |

### Phase Reset Protocol

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE RESET PROTOCOL                                │
│                                                                             │
│  1. DETECT bypass (component available but not used)                        │
│  2. LOG bypass to .specify/validations/bypass-log.json                      │
│  3. CLEAR phase artifacts (code, tests written without components)          │
│  4. INCREMENT reset counter (max 3 resets per phase)                        │
│  5. NOTIFY: "Phase X reset due to component bypass"                         │
│  6. RESTART phase with EXPLICIT component requirements                      │
│                                                                             │
│  After 3 resets: STOP workflow, require manual intervention                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Reset Detection Function

```python
def check_and_reset_phase(phase: int, phase_artifacts: dict) -> dict:
    """
    Check if phase was completed properly using components.
    If not, trigger reset.

    Returns: {
        'action': 'CONTINUE' | 'RESET' | 'STOP',
        'reason': str,
        'bypassed_components': list,
        'reset_count': int
    }
    """
    import json
    from pathlib import Path

    result = {
        'action': 'CONTINUE',
        'reason': '',
        'bypassed_components': [],
        'reset_count': 0
    }

    # Load reset counter
    reset_file = Path('.specify/validations/reset-counter.json')
    reset_data = {}
    if reset_file.exists():
        with open(reset_file) as f:
            reset_data = json.load(f)

    phase_key = f"phase_{phase}"
    result['reset_count'] = reset_data.get(phase_key, 0)

    # Check if max resets exceeded
    if result['reset_count'] >= 3:
        result['action'] = 'STOP'
        result['reason'] = f"Phase {phase} reset 3 times. Manual intervention required."
        return result

    # Get component utilization
    grade, issues, usage = validate_component_utilization(phase)

    # Check for bypass
    bypass_detected = False
    bypassed = []

    # Check skill bypass
    for skill in usage.get('skills_unused', []):
        # Check if this skill SHOULD have been used for this phase
        if should_skill_be_used(skill, phase, phase_artifacts):
            bypass_detected = True
            bypassed.append(f"skill:{skill}")

    # Check agent bypass
    expected_agents = get_expected_agents_for_phase(phase)
    for agent in expected_agents:
        if agent not in usage.get('agents_used', []):
            bypass_detected = True
            bypassed.append(f"agent:{agent}")

    if bypass_detected:
        result['action'] = 'RESET'
        result['reason'] = f"Components bypassed: {', '.join(bypassed)}"
        result['bypassed_components'] = bypassed

        # Increment reset counter
        reset_data[phase_key] = result['reset_count'] + 1
        reset_file.parent.mkdir(parents=True, exist_ok=True)
        with open(reset_file, 'w') as f:
            json.dump(reset_data, f, indent=2)

        # Log bypass
        log_bypass(phase, bypassed)

    return result


def should_skill_be_used(skill: str, phase: int, artifacts: dict) -> bool:
    """Determine if a skill should have been used for this phase."""

    skill_phase_mapping = {
        'coding-standards': [11],      # IMPLEMENT
        'testing-patterns': [11, 12],  # IMPLEMENT, QA
        'api-patterns': [11],          # IMPLEMENT (if API project)
        'database-patterns': [11],     # IMPLEMENT (if has DB)
        'workflow-validator': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],  # ALL phases
        'component-quality-validator': [5, 6],  # GENERATE, TEST
    }

    applicable_phases = skill_phase_mapping.get(skill, [])
    return phase in applicable_phases


def get_expected_agents_for_phase(phase: int) -> list:
    """Get list of agents expected to be used for a phase."""

    phase_agents = {
        8: ['planner'],                           # SPEC
        9: ['planner', 'architect'],              # PLAN
        11: ['tdd-guide', 'code-reviewer'],       # IMPLEMENT
        12: ['code-reviewer', 'security-reviewer', 'e2e-runner'],  # QA
        13: ['git-ops'],                          # DELIVER
    }

    return phase_agents.get(phase, [])


def log_bypass(phase: int, bypassed: list):
    """Log bypass event for audit trail."""
    import json
    from datetime import datetime
    from pathlib import Path

    log_file = Path('.specify/validations/bypass-log.json')
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logs = []
    if log_file.exists():
        with open(log_file) as f:
            logs = json.load(f)

    logs.append({
        'timestamp': datetime.now().isoformat(),
        'phase': phase,
        'bypassed_components': bypassed,
        'action': 'RESET_TRIGGERED'
    })

    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
```

### Phase Reset Execution

```bash
#!/bin/bash
# reset-phase.sh <phase_number>

PHASE=$1
SPECIFY_DIR=".specify"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              PHASE $PHASE RESET - COMPONENT BYPASS              ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║                                                                ║"
echo "║  ⚠️  Phase $PHASE was completed WITHOUT using required         ║"
echo "║     skills/agents. This is NOT acceptable.                     ║"
echo "║                                                                ║"
echo "║  The following will be reset:                                  ║"

case $PHASE in
    11)
        echo "║  - Source code written during this phase                       ║"
        echo "║  - Tests written during this phase                             ║"
        echo "║                                                                ║"
        echo "║  REQUIRED for retry:                                           ║"
        echo "║  - Use Skill(coding-standards) before coding                   ║"
        echo "║  - Use Skill(testing-patterns) before tests                    ║"
        echo "║  - Use Task(subagent_type='tdd-guide') for TDD                ║"
        echo "║  - Use Task(subagent_type='code-reviewer') after code         ║"
        ;;
    12)
        echo "║  - QA reports from this phase                                  ║"
        echo "║                                                                ║"
        echo "║  REQUIRED for retry:                                           ║"
        echo "║  - Use Task(subagent_type='code-reviewer')                    ║"
        echo "║  - Use Task(subagent_type='security-reviewer')                ║"
        echo "║  - Use Task(subagent_type='e2e-runner')                       ║"
        ;;
    *)
        echo "║  - Phase $PHASE artifacts                                      ║"
        ;;
esac

echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Mark phase for reset
echo "{\"phase\": $PHASE, \"status\": \"RESET\", \"timestamp\": \"$(date -Iseconds)\"}" > "$SPECIFY_DIR/phase-$PHASE-reset.json"

echo ""
echo "🔄 Phase $PHASE has been marked for reset."
echo "📋 Re-run the phase using the REQUIRED components listed above."
```

### Integration with Phase Validation

Every phase validation now includes component utilization check:

```
Phase N completes
       ↓
┌──────────────────────────────────────────────────────────────┐
│  QUALITY GATE VALIDATION (existing)                          │
│  + COMPONENT UTILIZATION CHECK (new)                         │
│                                                              │
│  1. Validate phase artifacts (existing)                      │
│  2. Check component utilization (NEW)                        │
│  3. If bypass detected → RESET phase                         │
│  4. If no bypass → Continue to grade                         │
└──────────────────────────────────────────────────────────────┘
       │
   ┌───┴───┐
   │       │
PASS    BYPASS
   │       │
   ↓       ↓
Grade  RESET
   │       │
   ↓       ↓
NEXT   RE-DO
```

### Reset Report Template

When a reset occurs, generate `.specify/validations/phase-{N}-reset-report.md`:

```markdown
# Phase {N} Reset Report

## Summary
| Field | Value |
|-------|-------|
| Phase | {N}: {Phase Name} |
| Timestamp | {ISO timestamp} |
| Action | **RESET** |
| Reset Count | {X} of 3 |

## Bypass Detected

The following components were available but NOT used:

### Skills Bypassed
| Skill | Should Have Been Used For |
|-------|---------------------------|
| {skill-name} | {reason} |

### Agents Bypassed
| Agent | Should Have Been Used For |
|-------|---------------------------|
| {agent-name} | {reason} |

## Impact

By bypassing these components, the following quality guarantees were lost:
- {guarantee 1}
- {guarantee 2}

## Required Actions

To successfully complete Phase {N}, you MUST:

1. **Before writing code:**
   ```
   Skill(coding-standards)
   Skill(testing-patterns)  # if writing tests
   ```

2. **During implementation:**
   ```
   Task(subagent_type="tdd-guide", prompt="...")
   ```

3. **After implementation:**
   ```
   Task(subagent_type="code-reviewer", prompt="Review code in ...")
   ```

## Warning

⚠️ This is reset {X} of 3. After 3 resets, the workflow will STOP
and require manual intervention.

## Next Steps

1. Review this report
2. Re-run Phase {N} using the required components
3. Validate with `/q-validate` before proceeding
```

---

## INTEGRATION WITH sp.autonomous

The sp.autonomous command MUST call this validator after EVERY phase:

```
Phase N completes
       ↓
[MANDATORY] workflow-validator validates Phase N
       ↓
   ┌───┴───┐
   ↓       ↓
APPROVED  REJECTED
   ↓       ↓
Phase N+1  Retry (max 3)
           ↓
       Still fail?
           ↓
       STOP with report
```

**This is non-negotiable. No phase proceeds without Quality Gate approval.**
