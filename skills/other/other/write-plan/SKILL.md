---
name: write-plan
description: BEI-specific plan creation with questionnaire extraction, duplication audit, and /build workflow rules. Use when planning new features to ensure no duplication and proper workflow integration.
---

# /write-plan - BEI Planning Workflow

**Purpose:** Create implementation plans with built-in duplication prevention, questionnaire extraction, and /build workflow rules.

**Use when:** Planning any new feature, module, or significant enhancement for BEI ERP.

## Usage

```bash
/write-plan <feature-name> [--questionnaire <google-doc-url>] [--quick]

# Examples:
/write-plan inventory-management
/write-plan hr-benefits --questionnaire https://docs.google.com/document/d/...
/write-plan store-ordering --quick  # Skip interactive questions
```

## What This Does

This skill wraps `/ralph-specum:start` with BEI-specific enhancements to replicate the successful Finance & Accounting planning process that saved 2-3 weeks by avoiding 60% duplication.

### The 5-Phase Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 0: Questionnaire Extraction (if --questionnaire)     │
│  Extract Q&A → Save to scratchpad/                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Research (Ralph Specum research-analyst)          │
│  Domain research → Feasibility → Tech stack                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Duplication Audit (RLM - 3 parallel agents)       │
│  → DocTypes audit  → APIs audit  → Frontend routes audit   │
│  → Create audit report with EXTEND vs BUILD vs DELETE      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Requirements (Ralph Specum product-manager)       │
│  Map Q&A to requirements → Tag [EXTEND], [BUILD], [DELETE] │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: Design (Ralph Specum architect-reviewer)          │
│  Auto-add /build workflow rules → Cost/benefit analysis    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: Tasks (Ralph Specum task-planner)                 │
│  Enforce /local-frappe, /pr-deploy in all task steps       │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Parse Arguments

```python
# Extract from user command
feature_name = args[0]  # Required
questionnaire_url = None
quick_mode = False

if "--questionnaire" in args:
    idx = args.index("--questionnaire")
    questionnaire_url = args[idx + 1]

if "--quick" in args:
    quick_mode = True
```

---

### Step 2: Questionnaire Extraction (if provided)

**ONLY if `--questionnaire` URL is provided:**

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

def extract_questionnaire(doc_url: str, feature_name: str):
    """Extract Q&A from Google Doc questionnaire."""

    # Extract document ID from URL
    doc_id = re.search(r'/document/d/([a-zA-Z0-9-_]+)', doc_url).group(1)

    # Authenticate with service account
    creds = service_account.Credentials.from_service_account_file(
        'credentials/task-manager-service.json',
        scopes=['https://www.googleapis.com/auth/documents.readonly']
    ).with_subject('sam@bebang.ph')

    docs = build('docs', 'v1', credentials=creds)

    # Get document content
    doc = docs.documents().get(documentId=doc_id).execute()

    # Extract text content
    content = doc.get('body', {}).get('content', [])
    text_content = []

    for element in content:
        if 'paragraph' in element:
            for text_run in element['paragraph'].get('elements', []):
                if 'textRun' in text_run:
                    text_content.append(text_run['textRun']['content'])

    full_text = ''.join(text_content)

    # Save to scratchpad
    with open(f'scratchpad/{feature_name}_questionnaire_raw.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"✅ Questionnaire extracted to scratchpad/{feature_name}_questionnaire_raw.txt")
    print(f"📝 Next: Manually structure Q&A into {feature_name}_answers_summary.md")

    return full_text
```

**Run extraction:**
```bash
python -c "
from write_plan_helpers import extract_questionnaire
extract_questionnaire('QUESTIONNAIRE_URL', 'FEATURE_NAME')
"
```

---

### Step 3: Start Ralph Specum with Research

**Invoke Ralph Specum:**

```bash
/ralph-specum:start <feature-name> "<goal-from-questionnaire>" --commit-spec
```

**What happens:**
- Creates `./specs/<feature-name>/` directory
- Spawns `research-analyst` agent
- Produces `research.md` with:
  - Domain analysis
  - Tech stack evaluation
  - Feasibility assessment
  - Implementation risks

**Wait for research.md to be created.**

---

### Step 4: Duplication Audit (CRITICAL - Don't Skip!)

**After research.md is created, BEFORE running `/ralph-specum:requirements`:**

**Invoke RLM with 3 parallel agents:**

```bash
/rlm "Audit the <feature-name> plan against existing my.bebang.ph features to avoid duplication.

Spawn 3 parallel agents:

Agent 1: Discover existing DocTypes
- Search hrms/hr/doctype/bei_* for similar DocTypes
- List DocType names, purposes, and key fields
- Identify which proposed features already exist

Agent 2: Discover existing API endpoints
- Search hrms/api/*.py for similar endpoints
- List endpoint names, purposes, and parameters
- Identify which proposed APIs already exist

Agent 3: Discover existing frontend routes
- Search bei-tasks/app/dashboard/** for similar pages
- List route paths, purposes, and components
- Identify which proposed pages already exist

Create comprehensive audit report at scratchpad/<feature-name>_plan_audit.md with:
- Section 1: Existing DocTypes Found
- Section 2: Existing API Endpoints Found
- Section 3: Existing Frontend Routes Found
- Section 4: Duplication Analysis (HIGH/MEDIUM/LOW risk)
- Section 5: Recommendations (EXTEND vs BUILD vs DELETE)
- Section 6: Cost Savings Estimate"
```

**RLM will:**
1. Spawn 3 agents in parallel
2. Each agent explores their domain
3. Consolidate findings into audit report
4. Save to `scratchpad/<feature-name>_plan_audit.md`

**Review the audit report and identify:**
- ✅ **[EXTEND]** - Features that already exist (add fields/logic)
- ✅ **[BUILD]** - Genuinely new features (no duplication)
- ❌ **[DELETE]** - Duplicate features (don't build)

---

### Step 5: Requirements Phase

**After reviewing audit report:**

```bash
/ralph-specum:requirements
```

**What to include in requirements approval:**
- ✅ Tag requirements based on audit: [EXTEND], [BUILD], [DELETE]
- ✅ Reference audit findings: "Per scratchpad/<feature>_plan_audit.md, BEI RFP duplicates BEI Payment Request"
- ✅ Include questionnaire business rules (if extracted)

**product-manager agent will:**
- Generate user stories
- Define acceptance criteria
- Map questionnaire answers to requirements

---

### Step 6: Design Phase (Auto-Enhanced)

```bash
/ralph-specum:design
```

**MANDATORY: Add this section to design.md after the header:**

```markdown
## Development Workflow (MANDATORY - /build Rules)

**This plan MUST be executed following `/build` workflow rules:**

### Phase 0: Setup (Before Starting Implementation)

1. **Create tasks** for all work items:
   ```bash
   /tasks add "Task 1 description"
   /tasks add "Task 2 description"
   ```

2. **Create feature branch** (optional, for isolation):
   ```bash
   /feature-branch <feature-name>
   ```

3. **Understand deployment polling** (CRITICAL for autonomous execution):
   - Skills will NEVER stop at "deployment gates"
   - Deployments are polled automatically using `scripts/wait_for_deployment.py`
   - If timeout occurs, verification task is created but work continues

### During Implementation (Every Task)

**For Python/API changes:**
1. ✅ **Use `/local-frappe`** to test changes BEFORE committing
   - Never commit untested Python code
   - Verify migrations work locally first
   - Test API endpoints with sample data

**For Frontend changes (bei-tasks repo):**
1. ✅ Test locally with `npm run dev`
2. ✅ Verify API integration works
3. ✅ Check responsive design

**For Commits:**
1. ❌ **NEVER use `git commit` directly**
2. ✅ **ALWAYS use `/pr-deploy`** (creates PR and triggers deployment)
3. ✅ Follow commit message conventions (feat/fix/refactor)
4. ✅ Include Co-Authored-By tag

**For Deployments (CRITICAL - Autonomous Execution):**

Deployments are async operations that historically caused work to stop for hours. The solution: **polling**.

**When backend changes require Frappe migration:**
```python
# 1. Commit changes that modify DocType JSON
# 2. Trigger migration via GitHub Actions
# 3. Poll for completion (DON'T STOP!)

from scripts.wait_for_deployment import wait_for_frappe_migration
import os

FRAPPE_API_KEY = os.popen('doppler secrets get FRAPPE_API_KEY --project bei-erp --config dev --plain').read().strip()
FRAPPE_API_SECRET = os.popen('doppler secrets get FRAPPE_API_SECRET --project bei-erp --config dev --plain').read().strip()

success = wait_for_frappe_migration(
    doctype="BEI Payment Request",
    field="new_field_name",
    api_key=FRAPPE_API_KEY,
    api_secret=FRAPPE_API_SECRET,
    max_wait_seconds=300,  # 5 minutes
    poll_interval=30        # Check every 30s
)

if not success:
    # Timeout - create verification task
    TaskCreate({
        "subject": "[VERIFY] Migration timeout - manual check needed",
        "description": "Migration did not complete within 5 minutes. Check GitHub Actions logs."
    })
    # Continue with other tests anyway
```

**When frontend changes deploy to Vercel:**
```python
# After git push to main (auto-triggers Vercel build)

from scripts.wait_for_deployment import wait_for_vercel_deployment

success = wait_for_vercel_deployment(
    url="https://my.bebang.ph/dashboard/feature",
    max_wait_seconds=120,  # 2 minutes
    poll_interval=15        # Check every 15s
)

if not success:
    # Timeout - create verification task
    TaskCreate({
        "subject": "[VERIFY] Vercel deployment timeout",
        "description": "Build did not go live within 2 minutes. Check Vercel dashboard."
    })
```

**Deployment Timeouts:**
| Type | Max Wait | Poll Interval | What Happens on Timeout |
|------|----------|---------------|-------------------------|
| Frappe Migration | 300s (5 min) | 30s | Create [VERIFY] task, continue |
| Vercel Build | 120s (2 min) | 15s | Create [VERIFY] task, continue |
| Docker Build | 600s (10 min) | 60s | Create [VERIFY] task, continue |

**MANDATORY RULES:**
1. ✅ **ALWAYS poll** - Never stop at "deployment gate"
2. ✅ **Continue on timeout** - Create verification task but keep going
3. ❌ **NEVER output "⏸️ PAUSED PENDING DEPLOYMENT"**
4. ❌ **NEVER wait for user to say "continue"**

**When Issues Found:**
1. ✅ **Create subtasks immediately** with `/tasks add "Fix [issue]"`
2. ✅ **Don't stop to ask** - operate autonomously
3. ✅ Fix issues inline, mark subtasks complete

### Phase Completion (After All Tasks Done)

1. **Run comprehensive E2E testing:**
   ```bash
   /test-full-cycle
   ```
   - Tests all 4 roles (Area Supervisor, Store Supervisor, Store Staff, HR User)
   - Audits all pages for UI/UX issues
   - Verifies RBAC (role-based access control)
   - Executes approval workflows

2. **Deploy to production:**
   ```bash
   /pr-deploy --auto-merge
   ```
   - Creates PR to production branch
   - Triggers GitHub Actions build
   - Auto-merges if CI passes

### Autonomous Operation Rules

**Core Principles:**
- ✅ **Never stop at deployment gates** - always poll until complete
- ✅ **Fix issues without stopping** - create subtasks for unexpected work
- ✅ **Use existing patterns** - don't reinvent (see audit findings)
- ✅ **Test before commit** - use `/local-frappe` for all Python changes
- ✅ **Deploy via PR** - never push to production directly
- ❌ **Don't duplicate** - extend existing features (per audit report)

**Forbidden Patterns:**
- ❌ "⏸️ PAUSED PENDING DEPLOYMENT" (use polling!)
- ❌ "I'll stop here and let you know..."
- ❌ "Would you like me to continue?"
- ❌ Waiting for user to say "continue"

**Deployment Polling is Mandatory:**
Every plan MUST use `scripts/wait_for_deployment.py` for all async operations. This is not optional - it's what makes autonomous execution work.

### Quick Reference Commands

| Task | Command |
|------|---------|
| Test Python locally | `/local-frappe` |
| Deploy changes | `/pr-deploy` or `/pr-deploy --auto-merge` |
| Create task | `/tasks add "Description"` |
| Mark task done | `/tasks done <id>` |
| Run E2E tests | `/test-full-cycle` |
| Check workflow | `/workflow` |
```

**Also add Cost/Benefit Analysis:**

```markdown
## Cost Savings Analysis

Based on duplication audit (`scratchpad/<feature>_plan_audit.md`):

| Metric | Without Audit | With Audit | Savings |
|--------|---------------|------------|---------|
| New DocTypes | X | Y | **Z DocTypes** |
| New APIs | X | Y | **Z endpoints** |
| New Pages | X | Y | **Z pages** |
| **Estimated Effort** | **X weeks** | **Y weeks** | **Z weeks** |
| **Duplication Risk** | **🔴 X%** | **🟢 0%** | **Eliminated** |

**Key Decisions:**
- ❌ **DELETE:** [List duplicate features removed]
- ✅ **EXTEND:** [List existing features being extended]
- ✅ **BUILD:** [List genuinely new features]
```

---

### Step 7: Tasks Phase (Enforced Workflow)

```bash
/ralph-specum:tasks
```

**task-planner agent will generate tasks.md.**

**VERIFY all task steps use /build commands:**
- ✅ Testing: `/local-frappe` (NOT `docker compose -f pwd.yml exec -T backend bench...`)
- ✅ Deployment: `/pr-deploy` (NOT `git commit && git push`)
- ✅ Task tracking: `/tasks add`, `/tasks done`

**If tasks don't follow workflow, manually update them.**

---

### Step 8: Implementation

```bash
/ralph-specum:implement --max-task-iterations 5
```

**spec-executor agent will:**
- Execute tasks one-by-one with fresh context
- Auto-commit after each task
- Update progress in `.progress.md`
- Stop on failure (max 5 retries per task)

---

## Output Files

After completion, you'll have:

```
./specs/<feature-name>/
├── .progress.md                              # Task completion tracking
├── research.md                               # Domain research + feasibility
├── requirements.md                           # User stories + acceptance criteria
├── design.md                                 # Architecture + /build workflow rules
└── tasks.md                                  # Implementation tasks

./scratchpad/
├── <feature>_questionnaire_raw.txt          # Raw Google Doc content
├── <feature>_answers_summary.md             # Structured Q&A (manual)
├── <feature>_key_findings.md                # Business rules (manual)
└── <feature>_plan_audit.md                  # Duplication audit report

./docs/plans/
└── YYYY-MM-DD-<feature-name>.md             # Final consolidated plan (optional)
```

---

## Key Success Factors

### ✅ What Made Finance & Accounting Plan Successful

1. **Questionnaire extraction** - Captured stakeholder requirements upfront
2. **Duplication audit** - Prevented 60% duplication (2-3 week savings)
3. **/build workflow rules** - Enforced `/local-frappe`, `/pr-deploy`, task tracking
4. **Cost/benefit analysis** - Quantified savings (DocTypes, APIs, pages, effort)
5. **EXTEND vs BUILD classification** - Clear decision framework

### ❌ Common Pitfalls to Avoid

1. **Skipping duplication audit** - Results in parallel systems, technical debt
2. **Using raw Docker/git commands** - Bypasses safety checks, breaks CI/CD
3. **Creating new DocTypes without checking existing** - Most common duplication source
4. **Not tagging requirements [EXTEND/BUILD/DELETE]** - Unclear scope

---

## Examples

### Example 1: With Questionnaire

```bash
/write-plan labor-scheduling --questionnaire https://docs.google.com/document/d/ABC123

# Workflow:
# 1. Extract Q&A from Google Doc
# 2. /ralph-specum:start labor-scheduling "Build labor scheduling from questionnaire"
# 3. Review research.md
# 4. /rlm duplication audit (3 agents)
# 5. Review audit report
# 6. /ralph-specum:requirements (tag with [EXTEND/BUILD])
# 7. /ralph-specum:design (add /build rules + cost analysis)
# 8. /ralph-specum:tasks (verify workflow commands)
# 9. /ralph-specum:implement
```

### Example 2: Without Questionnaire

```bash
/write-plan inventory-transfers

# Workflow:
# 1. /ralph-specum:start inventory-transfers "Build warehouse-to-store transfer workflow"
# 2. Review research.md
# 3. /rlm duplication audit (3 agents)
# 4. Review audit report
# 5. /ralph-specum:requirements (tag with [EXTEND/BUILD])
# 6. /ralph-specum:design (add /build rules + cost analysis)
# 7. /ralph-specum:tasks (verify workflow commands)
# 8. /ralph-specum:implement
```

### Example 3: Quick Mode (Minimal Interaction)

```bash
/write-plan payroll-import --quick

# Workflow:
# 1. Auto-generate all specs (research → requirements → design → tasks)
# 2. PAUSE before implement for duplication audit review
# 3. /ralph-specum:implement (after manual audit approval)
```

---

## Troubleshooting

### "Spec already exists"

```bash
/ralph-specum:status          # Check existing specs
/ralph-specum:switch <name>   # Switch to existing spec
# Or start fresh:
/ralph-specum:start <name> --fresh
```

### "Duplication audit found no duplicates, but I know they exist"

Audit agents search specific patterns. Manually check:
```bash
# DocTypes
ls hrms/hr/doctype/ | grep -i <keyword>

# APIs
grep -r "def.*<keyword>" hrms/api/

# Frontend
find bei-tasks/app -name "*<keyword>*"
```

### "Task failing repeatedly (5 times)"

```bash
# Fix manually, then resume:
/ralph-specum:implement

# Or cancel and restart:
/ralph-specum:cancel
/ralph-specum:implement
```

### "/build rules not applied to tasks"

Manually edit `./specs/<feature>/tasks.md`:
- Replace `docker compose -f pwd.yml exec -T backend bench...` → `/local-frappe`
- Replace `git commit` → `/pr-deploy`
- Add task tracking: `/tasks add`, `/tasks done`

---

## Checklist: Before Calling This Complete

- [ ] Questionnaire extracted (if URL provided)
- [ ] Research.md created and reviewed
- [ ] Duplication audit completed (3 agents: DocTypes, APIs, Routes)
- [ ] Audit report reviewed, features classified [EXTEND/BUILD/DELETE]
- [ ] Requirements.md tagged with classifications
- [ ] Design.md includes /build workflow rules section
- [ ] Design.md includes cost/benefit analysis table
- [ ] Tasks.md uses `/local-frappe` and `/pr-deploy` (NOT raw commands)
- [ ] Implementation started with `/ralph-specum:implement`

---

## Next Steps After Plan Creation

1. **Review final plan** - Check specs/<feature>/design.md
2. **Optionally consolidate** - Copy to docs/plans/YYYY-MM-DD-<feature>.md
3. **Execute** - Run `/ralph-specum:implement` for autonomous task execution
4. **Test** - Run `/test-full-cycle` after implementation
5. **Deploy** - Use `/pr-deploy --auto-merge` for production deployment

---

## Related Skills

- `/ralph-specum:start` - Base workflow (research → requirements → design → tasks)
- `/rlm` - Recursive Language Model for parallel exploration
- `/google` - Google Docs API for questionnaire extraction
- `/local-frappe` - Local testing before deployment
- `/pr-deploy` - Safe deployment via PR workflow
- `/test-full-cycle` - Comprehensive E2E testing

---

## Skill Metadata

**Created:** 2026-02-06
**Based on:** Finance & Accounting plan success (saved 2-3 weeks by avoiding 60% duplication)
**Replaces:** Manual planning process
**Requires:** Ralph Specum plugin, Google Docs API access, RLM capability
**Outputs:** Comprehensive plan with duplication prevention and /build workflow rules
