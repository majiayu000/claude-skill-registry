---
name: bugs-to-stories
description: "Convert bug reports into prd.json user stories for autonomous fixing. Use after running test-and-break skill. Triggers on: convert bugs to stories, fix these bugs, add bugs to prd, create fix stories."
---

# Bugs to Stories Converter

Takes bug reports from the test-and-break skill and converts them into properly formatted user stories that can be added to prd.json for Ralph to fix autonomously.

---

## The Job

1. Read the bug report from `tasks/bug-report-*.md`
2. Convert each bug into a user story
3. Add stories to prd.json (or create new one)
4. Ensure proper prioritization (critical bugs first)

---

## Conversion Rules

### Bug → User Story Mapping

| Bug Field | Story Field |
|-----------|-------------|
| BUG-XXX | id: "FIX-XXX" |
| Title | title: "Fix: [title]" |
| Steps to Reproduce | Goes into notes |
| Expected Behavior | Part of description |
| Actual Behavior | Part of description |
| Severity | Determines priority |

### Priority Mapping

| Bug Severity | Story Priority Range |
|--------------|---------------------|
| Critical | 1-3 (fix immediately) |
| High | 4-7 |
| Medium | 8-12 |
| Low | 13+ |

### Story Format

```json
{
  "id": "FIX-001",
  "title": "Fix: [Descriptive bug title]",
  "description": "As a user, I expect [expected behavior] but currently [actual behavior occurs].",
  "acceptanceCriteria": [
    "[Specific technical fix needed]",
    "[Another fix criterion if needed]",
    "Regression test: Following original bug steps no longer reproduces the issue",
    "Typecheck passes"
  ],
  "priority": 1,
  "passes": false,
  "notes": "Bug reproduction: [steps from bug report]"
}
```

---

## Process

### Step 1: Read Bug Report

```bash
# Find the latest bug report
ls -t tasks/bug-report-*.md | head -1
```

Read the bug report and parse each bug entry.

### Step 2: Check Existing prd.json

```bash
# Check if prd.json exists and get current state
if [ -f prd.json ]; then
  cat prd.json | jq '{
    project: .project,
    totalStories: (.userStories | length),
    maxPriority: ([.userStories[].priority] | max),
    incompleteStories: ([.userStories[] | select(.passes == false)] | length)
  }'
fi
```

### Step 3: Decide Integration Strategy

**Option A: Add to existing prd.json (recommended if original build incomplete)**
- Append bug fix stories after existing stories
- Set priorities to come after current highest priority
- Keep original project name and branchName

**Option B: Create bug-fix-only prd.json (if original build complete)**
- Create new prd.json with only bug fix stories
- Use branchName: `ralph/bugfix-[date]`
- Start priorities at 1

Ask user which approach if unclear.

### Step 4: Generate Stories

For each bug in the report:

```javascript
// Example conversion
const bugToStory = (bug, priorityOffset) => ({
  id: bug.id.replace('BUG', 'FIX'),
  title: `Fix: ${bug.title}`,
  description: `As a user, I expect ${bug.expected} but currently ${bug.actual}.`,
  acceptanceCriteria: [
    ...generateFixCriteria(bug),
    `Regression test: ${bug.steps.join(' → ')} no longer reproduces the issue`,
    "Typecheck passes"
  ],
  priority: severityToPriority(bug.severity) + priorityOffset,
  passes: false,
  notes: `Original bug steps: ${bug.steps.join('; ')}`
});
```

### Step 5: Update prd.json

**If adding to existing:**
```bash
# Backup first
cp prd.json prd.json.backup

# Add new stories (Claude does this programmatically)
```

**If creating new:**
```json
{
  "project": "[Original Project] - Bug Fixes",
  "branchName": "ralph/bugfix-2024-01-15",
  "description": "Bug fixes from automated testing",
  "userStories": [
    // converted bug stories here
  ]
}
```

### Step 6: Verify

```bash
# Verify the updated prd.json
cat prd.json | jq '{
  project: .project,
  totalStories: (.userStories | length),
  bugFixStories: ([.userStories[] | select(.id | startswith("FIX"))] | length),
  allPassesFalse: ([.userStories[] | select(.passes == false)] | length)
}'
```

---

## Example Conversion

**Input Bug:**
```markdown
## BUG-003: Form submits with empty required fields

**Severity:** High
**Type:** Functional

**Steps to Reproduce:**
1. Go to /signup
2. Leave all fields empty
3. Click "Create Account"

**Expected Behavior:**
Form should show validation errors and prevent submission

**Actual Behavior:**
Form submits and shows server error
```

**Output Story:**
```json
{
  "id": "FIX-003",
  "title": "Fix: Form submits with empty required fields",
  "description": "As a user, I expect the signup form to show validation errors when I leave required fields empty, but currently it submits and shows a server error.",
  "acceptanceCriteria": [
    "Add client-side validation for all required fields",
    "Show inline error messages for empty required fields",
    "Disable submit button until required fields are filled",
    "Regression test: Going to /signup → leaving fields empty → clicking Create Account shows validation errors instead of submitting",
    "Typecheck passes"
  ],
  "priority": 4,
  "passes": false,
  "notes": "Original bug steps: Go to /signup; Leave all fields empty; Click Create Account"
}
```

---

## After Conversion

Once bugs are converted to stories:

1. Tell the user how many bug fix stories were added
2. Show the priority distribution
3. Ask if they want to start Ralph to fix them:

> "I've added X bug fix stories to prd.json:
> - Critical fixes: X (priority 1-3)
> - High priority: X (priority 4-7)
> - Medium priority: X (priority 8-12)
> - Low priority: X (priority 13+)
>
> Ready to run Ralph to fix these bugs automatically?"

If yes, they can run `./ralph.sh` to start fixing.
