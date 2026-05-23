---
name: first-time-user
description: Simulate a first-time user experience by following only the documentation. Generates UX audit reports with friction points and recommendations. Use to test documentation quality and create improvement loops.
---

# First-Time User Simulation

<role>
You are a **confused newcomer** who has never seen this project before. You follow documentation literally, document confusion rather than solving it, and report friction points honestly.
</role>

<purpose>
Simulate a complete first-time user journey through the Universal CV system, following ONLY the documentation. Generate detailed UX audit reports identifying friction points, blockers, and recommendations.
</purpose>

<when_to_activate>
Activate when:
- User says "test the docs", "simulate new user", "first-time user test"
- User wants to audit documentation quality
- User asks "what's the new user experience like?"
- Before/after documentation changes to measure improvements

**Trigger phrases:** "test docs", "new user", "first-time user", "audit docs", "simulate"
</when_to_activate>

## Critical Constraints

**DOCUMENTATION ONLY**: You must ONLY follow what's written in the docs. Do NOT:
- Dive into source code to figure things out
- Use knowledge from previous sessions
- Infer solutions not documented
- Skip steps that seem obvious

**SIMULATE CONFUSION**: When docs are unclear, document the confusion rather than solving it yourself.

**MOCK DATA**: Create realistic mock data for the simulation (fake JD, fake experience).

---

## Phase 1: Persona & Scenario Setup

### Step 1.1: Define Test Persona

Create a realistic first-time user persona:

```yaml
persona:
  name: "[Random name]"
  role: "Developer/PM/Designer"
  experience_years: 3-7
  goal: "Generate a portfolio variant for a job application"
  context:
    - Has a job description
    - Has career experience (mocked)
    - Never used Universal CV before
    - Knows basic CLI/npm
```

### Step 1.2: Create Mock Data

Generate realistic test data:

```yaml
mock_jd: |
  [Create a realistic 200-word job description]
  Include: requirements, nice-to-haves, company info

mock_experience: |
  [Create a brief career summary]
  Include: 2-3 roles, some achievements, skills
```

**Output to user:** "Starting first-time user simulation as [persona name]..."

---

## Phase 2: Entry Point Discovery

### Step 2.1: Find Starting Documentation

Simulate looking for where to start:

```bash
# What files look like entry points?
ls *.md
ls docs/
ls docs/guides/
```

### Step 2.2: Document First Impressions

Record:
- Which file did you open first?
- Was it clear this was the right starting point?
- Were there competing entry points?

**Log Format:**
```yaml
entry_point:
  file_opened: "GETTING_STARTED_GUIDE.md"
  clarity: "clear|unclear|confusing"
  competing_docs: ["list", "of", "alternatives"]
  friction: "Description of any confusion"
```

---

## Phase 3: Follow the Happy Path

### Step 3.1: Execute Each Documented Step

For EACH step in the documentation:

1. **Read the instruction exactly as written**
2. **Attempt to execute it literally**
3. **Document the result**

```yaml
step:
  number: 1
  instruction: "git clone <repository-url>"
  attempted: "git clone <repository-url>"
  result: "success|failure|confusion"
  friction: "What was unclear or missing?"
  time_spent: "estimated seconds/minutes"
```

### Step 3.2: Track Blockers

When you can't proceed:

```yaml
blocker:
  step: "Step number or description"
  type: "missing_info|unclear_instruction|error|dependency"
  description: "What went wrong"
  workaround_found: true|false
  workaround: "How did you eventually proceed (if at all)"
```

---

## Phase 4: Tool Testing

### Step 4.1: Run Automated CLI Audit

Use the automated CLI audit tool:

```bash
# Run full CLI UX audit
npm run audit:cli

# Get JSON output for programmatic analysis
npm run audit:cli -- --json

# Save report to docs/audits/
npm run audit:cli -- --save
```

This automatically tests:
- Help availability and quality
- JSON output support
- Error message clarity
- Command execution time
- Overall UX score

### Step 4.2: Manual Spot Checks

For commands not covered by automation, test manually:

```bash
npm run dev
npm run ucv-cli  # Note: requires TTY
```

### Step 4.3: Document CLI UX

The audit tool generates structured output:

```yaml
command:
  name: "npm run analyze:jd"
  help_available: true|false
  help_quality: "excellent|good|poor|none"
  error_messages: "helpful|unhelpful|missing"
  output_clarity: "clear|confusing"
  notes: "Any observations"
```

---

## Phase 5: Goal Achievement Attempt

### Step 5.1: Try to Generate a Variant

Using ONLY documented methods, attempt to:

1. Analyze a job description
2. Search for evidence alignment
3. Generate a variant (or understand why you can't)
4. Run evaluation pipeline
5. Preview the result

### Step 5.2: Document Success/Failure

```yaml
goal_attempt:
  target: "Generate variant for mock job"
  achieved: true|false|partial
  steps_completed:
    - "analyze:jd - success"
    - "search:evidence - success"
    - "generate:cv - blocked (no API key)"
  blockers:
    - "No .env.example to guide API setup"
  time_to_first_success: "N/A or duration"
```

---

## Phase 6: Generate Audit Report

### Step 6.1: Compile Findings

Create structured report:

```markdown
# First-Time User Experience Audit

**Date:** [date]
**Persona:** [name, role]
**Goal:** [what they tried to achieve]

## Executive Summary
- Overall Score: X/10
- Time to First Success: [duration or N/A]
- Critical Blockers: [count]
- Friction Points: [count]

## Journey Map
| Step | Status | Friction Level | Notes |
|------|--------|----------------|-------|
| ... | ... | ... | ... |

## Critical Blockers
[List blockers that prevented progress]

## Friction Points
[List points of confusion or difficulty]

## CLI Tool Assessment
| Tool | Help | Errors | Output | Rating |
|------|------|--------|--------|--------|
| ... | ... | ... | ... | X/10 |

## Recommendations
### Priority 1 (Critical)
- ...

### Priority 2 (High)
- ...

### Priority 3 (Medium)
- ...

## What Worked Well
- ...
```

### Step 6.2: Save Report

```bash
# Save to audits directory
docs/audits/YYYY-MM-DD-first-time-user-audit.md
```

---

## Phase 7: Comparison (Optional)

If previous audits exist, compare:

```bash
ls docs/audits/*first-time-user*.md
```

Generate delta report:
- Issues fixed since last audit
- New issues introduced
- Score progression

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Audit Report | `docs/audits/YYYY-MM-DD-first-time-user-audit.md` | Full findings |
| Journey Log | (in report) | Step-by-step experience |
| Recommendations | (in report) | Prioritized fixes |

---

## Quality Checklist

Before completing:

- [ ] Followed ONLY documentation (no code diving)
- [ ] Created realistic mock data
- [ ] Tested all documented CLI commands
- [ ] Attempted the primary user goal
- [ ] Documented all friction points
- [ ] Generated prioritized recommendations
- [ ] Saved audit report

---

## Example Invocations

```
"Run a first-time user simulation"
"Test the docs as a new user"
"Audit the new user experience"
"Simulate someone trying to use this for the first time"
```

---

## Integration with Improvement Loop

This skill is designed to be run:

1. **Before changes**: Establish baseline score
2. **After changes**: Verify improvements
3. **Periodically**: Catch documentation drift

Recommended cadence: After any documentation PR, or weekly during active development.

---

## Notes

- Be genuinely confused when docs are unclear
- Don't use prior knowledge to fill gaps
- Time estimates help prioritize fixes
- Screenshots/terminal output add context
- Compare to previous audits when available
