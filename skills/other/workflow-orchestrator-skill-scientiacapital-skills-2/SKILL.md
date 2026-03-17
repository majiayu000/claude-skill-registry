---
name: "workflow-orchestrator"
description: "Project workflow system - cost tracking, parallel execution, security gates, agent orchestration. Use when: start day, begin session, status check, new feature, build, implement, end day, wrap up, debug, investigate, research, evaluate."
---

<objective>
Universal project workflow system providing cost tracking, parallel execution via git worktrees, security gates, and intelligent agent orchestration. Manages complete development lifecycle from session start to end-of-day with mandatory security sweeps and context preservation.
</objective>

<quick_start>
**Start session:**
```bash
pwd && git status && git log --oneline -5
cat PROJECT_CONTEXT.md 2>/dev/null
```

**End session:**
1. Run security sweep: `gitleaks detect --source .`
2. Update `PROJECT_CONTEXT.md` with completed/in-progress
3. Log costs to `costs/daily-YYYY-MM-DD.json`

**Feature development:** Plan → DB/Schema → Parallel implementation → Security gate → Ship
</quick_start>

<success_criteria>
Workflow is successful when:
- Context scan completed at session start (pwd, git status, PROJECT_CONTEXT.md)
- Security sweep passes before any commits (gitleaks, secrets check, audit)
- Cost tracking updated (daily.json, mtd.json)
- PROJECT_CONTEXT.md updated at session end
- Worktrees cleaned up after merge
- All security gates passed before shipping
</success_criteria>

<triggers>

- **Session Management:** "start day", "begin session", "what's the status", "end day", "wrap up", "done for today"
- **Feature Development:** "new feature", "build", "implement"  
- **Debugging:** "debug", "investigate", "why is this broken"
- **Research:** "research", "evaluate", "should we use"

---

## START DAY

### Pre-Flight Checks
```bash
# Git clean?
git status --short | head -5
# Deps installed?
[ -f package.json ] && [ ! -d node_modules ] && echo "⚠️ Run npm install"
[ -f requirements.txt ] && [ ! -d .venv ] && echo "⚠️ Run pip install"
# Env exists?
[ -f .env.example ] && [ ! -f .env ] && echo "⚠️ Copy .env.example to .env"
```

### Context Scan (Mandatory)
```bash
# Detect project
pwd
git status
git log --oneline -5

# Load context
cat PROJECT_CONTEXT.md 2>/dev/null || echo "No context file"
cat CLAUDE.md 2>/dev/null
cat TASK.md 2>/dev/null
cat PLANNING.md 2>/dev/null
```

### Worktree Status
```bash
cat ~/.claude/worktree-registry.json 2>/dev/null | jq '.worktrees[] | select(.project == "'$(basename $(pwd))'")'
git worktree list
```

### Cost Status
```bash
cat costs/daily-$(date +%Y-%m-%d).json 2>/dev/null || echo "No cost tracking today"
cat costs/mtd.json 2>/dev/null | jq '.total'
```

### Output Format
```markdown
## Session Start: [PROJECT_NAME]

### Completed (Last Session)
- [x] Task 1
- [x] Task 2

### In Progress
| Task | Branch/Worktree | Status |
|------|-----------------|--------|
| API endpoint | feature/api @ 8100 | 70% |

### Blockers
- [ ] Waiting on X

### Today's Priority Queue
1. [AGENT: research-skill] Evaluate framework options
2. [AGENT: langgraph-agents-skill] Build orchestration
3. [AGENT: debug-like-expert] Fix flaky test

### Cost Context
- Today: $0.00 | MTD: $12.34 | Budget: $100
- Avg cost/task: $0.45
```

**Deep dive:** See `reference/start-day-protocol.md`

---

## RESEARCH PHASE

**Trigger:** Before ANY feature development involving new frameworks, APIs, or architectural decisions.

### Scan Existing Solutions
```bash
# Check MCP cookbook first
ls /Users/tmk/Desktop/tk_projects/mcp-server-cookbook/ 2>/dev/null

# Check your repos
find ~/tk_projects -name "*.md" -exec grep -l "[search_term]" {} \; 2>/dev/null | head -20
```

### Evaluate Approach
Use `/research-skill` checklist:
- Framework selection criteria
- LLM selection (default: DeepSeek V3 for bulk, Claude Sonnet for reasoning)
- Infrastructure (Supabase/Neon/RunPod)

### Cost Projection
```python
# Estimate before building
estimated_costs = {
    "inference": tokens_estimate * model_cost_per_1k / 1000,
    "compute": hours_estimate * runpod_hourly,
    "storage": gb_estimate * supabase_monthly / 30
}
if sum(estimated_costs.values()) > threshold:
    flag_for_review()
```

### Output
Create `RESEARCH.md` → `FINDINGS.md` with:
- Substantive one-liner summary
- Confidence score (1-10)
- Dependencies list
- Open questions
- **GO/NO-GO recommendation**

### Gate
⛔ **Human checkpoint required before proceeding**

**Deep dive:** See `reference/research-workflow.md`

---

## FEATURE DEVELOPMENT

### Phase 0: PLAN
```markdown
1. Create BRIEF.md with scope
2. Map to agents (use workflow-enforcer-skill 70+ catalog)
3. Identify parallelization opportunities
4. Create TodoWrite todos
5. Cost estimate
```

### Phase 1: SETUP + DB
```bash
# Schema design
/database-design:schema-design

# Migrations
/supabase-sql-skill or /database-migrations:sql-migrations
```
⛔ **Gate: Schema review before Phase 2**

### Phase 2: PARALLEL IMPLEMENTATION

#### Port Allocation
```bash
# Reserve ports upfront (8100-8199 pool)
PORTS=$(cat ~/.claude/worktree-registry.json | jq '[.worktrees[].ports[]] | max // 8098' | xargs -I{} expr {} + 2)
echo "Next available: $PORTS, $(expr $PORTS + 1)"
```

#### Spawn Worktrees
```bash
# Worktree A: Backend
git worktree add -b feature/api-backend ~/tmp/worktrees/$(basename $(pwd))/api-backend
# Assign ports 8100, 8101

# Worktree B: Frontend  
git worktree add -b feature/ui ~/tmp/worktrees/$(basename $(pwd))/ui
# Assign ports 8102, 8103

# Worktree C: Tests
git worktree add -b feature/tests ~/tmp/worktrees/$(basename $(pwd))/tests
# Assign ports 8104, 8105
```

#### Monitor & Merge
```bash
# Check status
git worktree list

# After completion, merge
git checkout main
git merge feature/api-backend
git worktree remove ~/tmp/worktrees/my-project/api-backend
```

### Phase 3: SECURITY + INTEGRATION

Run parallel scans:
```bash
# SAST
semgrep --config auto . 

# Secrets
gitleaks detect --source .

# Dependencies
npm audit --audit-level=critical || pip-audit

# Tests
pytest --cov=src || npm test -- --coverage
```

⛔ **Gate: ALL must pass**
```python
gate = (
    sast_clean AND 
    secrets_found == 0 AND 
    critical_vulns == 0 AND 
    test_coverage >= 80
)
```

### Phase 4: SHIP
```bash
# Final review
git diff main...HEAD

# Update docs
# - TASK.md (mark complete)
# - PLANNING.md (update status)  
# - CLAUDE.md (add learnings)

# Commit
git add .
git commit -m "feat: [description]"
git push

# Log cost
echo '{"feature": "X", "cost": 1.23, "date": "'$(date -Iseconds)'"}' >> costs/by-feature.jsonl
```

**Deep dive:** See `reference/feature-development.md`

---

## DEBUG MODE

**Trigger:** When standard troubleshooting fails or issue is complex.

### Context Scan
```bash
# Detect project type
cat package.json 2>/dev/null && echo "Node.js project"
cat pyproject.toml 2>/dev/null && echo "Python project"
cat Cargo.toml 2>/dev/null && echo "Rust project"

# Load domain expertise
ls ~/.claude/skills/expertise/ 2>/dev/null
```

### Evidence Gathering (Mandatory)
Document before ANY fix attempt:
```markdown
## Issue
[Exact error message]

## Reproduction
1. Step 1
2. Step 2
3. Error occurs

## Expected vs Actual
- Expected: X
- Actual: Y

## Environment
- OS: 
- Runtime version:
- Dependencies:
```

### Hypothesis Formation
List 3+ hypotheses with evidence:
```markdown
### Hypotheses
1. **[Most likely]** Database connection timeout
   - Evidence: Error mentions "connection refused"
   - Test: Check DB status
   
2. **[Possible]** Race condition in async code
   - Evidence: Intermittent failure
   - Test: Add logging around suspect area
   
3. **[Less likely]** Dependency version mismatch
   - Evidence: Works on other machine
   - Test: Compare package-lock.json
```

### Critical Rules
- ❌ NO DRIVE-BY FIXES - if you can't explain WHY, don't commit
- ❌ NO GUESSING - verify everything
- ✅ Use all tools: MCP servers, web search, extended thinking
- ✅ Think out loud
- ✅ One variable at a time

**Deep dive:** See `reference/debug-methodology.md`

---

## END DAY

### Security Sweep (Mandatory - Blocks Commits)
```bash
# Parallel scans
gitleaks detect --source . --verbose
git log -p | grep -E "(password|secret|api.?key|token)" || echo "Clean"
npm audit --audit-level=critical 2>/dev/null || pip-audit 2>/dev/null || echo "No package manager"
grep -r "API_KEY\|SECRET" --include="*.env*" . && echo "⚠️ Check env files"
```

⛔ **Gate: ALL must pass before any commits**

### Context Preservation
Update `PROJECT_CONTEXT.md`:
```markdown
## Last Updated: [DATE]

### Completed This Session
- [x] Built API endpoint
- [x] Fixed auth bug

### In Progress
- [ ] Frontend integration (70%)

### Blockers
- Waiting on design review

### Decisions Made
- Chose Supabase over Firebase (cost: $0 vs $25/mo)
- Using DeepSeek V3 for embeddings (90% cheaper)

### Tomorrow's Priorities
1. Complete frontend integration
2. Write tests
3. Deploy to staging
```

### Cost Tracking
```bash
# Log today's costs
cat >> costs/daily-$(date +%Y-%m-%d).json << EOF
{
  "inference": {"claude": 0.45, "deepseek": 0.02},
  "compute": {"runpod": 0.00},
  "total": 0.47
}
EOF

# Update MTD
jq '.total += 0.47' costs/mtd.json > tmp && mv tmp costs/mtd.json
```

### Portfolio Metrics Capture
```bash
# Lines shipped today
git diff --stat $(git log --since="today 00:00" --format="%H" | tail -1)..HEAD 2>/dev/null

# Session summary
echo '{"date":"'$(date +%Y-%m-%d)'","commits":'$(git log --since="today 00:00" --oneline | wc -l | tr -d ' ')',"files_changed":'$(git diff --stat $(git log --since="today 00:00" --format="%H" | tail -1)..HEAD 2>/dev/null | tail -1 | grep -oE '[0-9]+ file' | grep -oE '[0-9]+' || echo 0)'}' >> ~/.claude/portfolio/daily-metrics.jsonl
```

### Learning Capture
Add to PROJECT_CONTEXT.md or CLAUDE.md:
- Patterns discovered (reusable approaches)
- Mistakes made (avoid next time)
- Tools discovered (new MCP servers, agents, commands)

### Worktree Cleanup
```bash
# Check for orphans
git worktree list --porcelain | grep -E "^worktree"

# Merge completed work
for wt in $(git worktree list | grep -v "bare\|main" | awk '{print $1}'); do
  # Check if PR merged, then cleanup
done

# Remove merged worktrees
git worktree prune
```

**Deep dive:** See `reference/end-day-protocol.md`

---

## COST TRACKING

### Model Costs Reference
```python
MODEL_COSTS = {
    # Per 1K tokens
    "claude-sonnet": 0.003,      # Complex reasoning
    "deepseek-v3": 0.00014,      # 95% cheaper - bulk processing
    "qwen-72b": 0.0002,          # 93% cheaper - alternatives
    "voyage-embed": 0.0001,      # Embeddings
    "ollama-local": 0.0,         # Free - local dev
}

BUDGETS = {
    "daily": 5.00,
    "monthly": 100.00,
    "alert_threshold": 0.8,  # Alert at 80%
}
```

### Cost-Optimized Routing
| Task Type | Model | Why |
|-----------|-------|-----|
| Complex reasoning | Claude Sonnet | Quality critical |
| Bulk processing | DeepSeek V3 | 90% savings |
| Code generation | Claude Sonnet | Accuracy matters |
| Embeddings | Voyage | Cost + quality balance |
| Local dev/testing | Ollama | Free |

**Deep dive:** See `reference/cost-tracking.md`

---

## ROLLBACK / RECOVERY

### When to Rollback
- Tests failing after "fix"
- Security scan finds new issues
- Performance degradation
- Unexpected behavior

### Recovery Workflow
```bash
# 1. Stash current work
git stash

# 2. Find last known good
git log --oneline -20

# 3. Selective rollback
git checkout [commit] -- [specific_file]

# OR full revert
git revert [commit]

# 4. Verify
pytest  # or npm test

# 5. Investigate root cause using debug-like-expert
```

**Deep dive:** See `reference/rollback-recovery.md`

---

## AGENT QUICK REFERENCE

| Need | Agent/Skill |
|------|-------------|
| Market/tech research | `/research-skill` |
| Project planning | `/planning-prompts` |
| Multi-agent systems | `/langgraph-agents-skill` |
| Complex debugging | `/debug-like-expert` |
| Parallel development | `/worktree-manager` |
| Session context | `/project-context-skill` |
| CRM integration | `/crm-integration-skill` |
| Data analysis | `/data-analysis-skill` |
| Voice AI | `/voice-ai-skill` |
| Trading signals | `/trading-signals-skill` |
| SQL migrations | `/supabase-sql-skill` |
| GPU deployment | `/runpod-deployment-skill` |
| Sales/revenue | `/sales-revenue-skill` |
| Fast inference | `/groq-inference-skill` |

**Deep dive:** See `reference/agent-routing.md` for complete 70+ agent catalog

---

## PROJECT STRUCTURE

```
project/
├── CLAUDE.md              # Project rules + learnings
├── PLANNING.md            # Roadmap + phases
├── TASK.md                # Current sprint
├── Backlog.md             # Future work
├── PROJECT_CONTEXT.md     # Auto-generated session context
├── .taskmaster/
│   └── docs/
│       └── prd.txt        # Product requirements
├── .prompts/              # Meta-prompts
│   ├── research/
│   ├── plan/
│   ├── do/
│   └── refine/
├── costs/                 # Cost tracking
│   ├── daily-YYYY-MM-DD.json
│   ├── by-feature.jsonl
│   └── mtd.json
└── src/
```

---

## COST GATE

### Pre-Flight Budget Check

Run before ANY resource-intensive workflow (feature builds, research sprints, parallel agents):

```bash
# Read or initialize daily cost tracker
COST_FILE=~/.claude/daily-cost.json
if [ ! -f "$COST_FILE" ]; then
  echo '{"date":"'$(date +%Y-%m-%d)'","spent":0,"budget_monthly":100}' > "$COST_FILE"
fi

# Check budget status
SPENT=$(jq '.spent' "$COST_FILE")
BUDGET=$(jq '.budget_monthly' "$COST_FILE")
PCT=$(echo "scale=0; $SPENT * 100 / $BUDGET" | bc)
echo "MTD: \$$SPENT / \$$BUDGET ($PCT%)"
```

### Threshold Actions

| % of Budget | Action |
|-------------|--------|
| < 50% | Proceed normally |
| 50-80% | Display cost warning, suggest model downgrade |
| 80-95% | **WARN** — Ask user before proceeding |
| > 95% | **BLOCK** — Require explicit override |

### Model Cost Reference

| Model | Input/1M | Output/1M | Use When |
|-------|----------|-----------|----------|
| Claude Opus | $15.00 | $75.00 | Complex architecture decisions |
| Claude Sonnet | $3.00 | $15.00 | Code generation, reasoning |
| Claude Haiku | $0.25 | $1.25 | Search, classification, simple tasks |
| DeepSeek V3 | $0.27 | $1.10 | Bulk processing, 90% savings |

### Cost Tracking Per Operation

After each workflow phase, log:
```bash
echo '{"phase":"feature-build","model":"sonnet","est_tokens":50000,"est_cost":0.15,"ts":"'$(date -Iseconds)'"}' >> ~/.claude/cost-log.jsonl
```

---

## PROGRESS RENDERING

### Native Progress (TaskCreate/TaskUpdate) — Preferred

Use TaskCreate with `activeForm` for live UI spinners during execution. This renders native checkmarks and progress indicators in Claude Code's UI:

```javascript
// Create tasks for each workflow phase
TaskCreate({ subject: "Plan architecture", activeForm: "Planning architecture" })
TaskCreate({ subject: "Build components", activeForm: "Building components" })
TaskCreate({ subject: "Run security sweep", activeForm: "Running security sweep" })

// Set dependencies for sequential phases
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })  // Build waits for Plan
TaskUpdate({ taskId: "3", addBlockedBy: ["2"] })  // Security waits for Build

// Track progress transitions
TaskUpdate({ taskId: "1", status: "in_progress" })  // → live spinner
TaskUpdate({ taskId: "1", status: "completed" })     // → checkmark
```

**Key fields:**
- `subject` — imperative title ("Run tests", "Build API")
- `activeForm` — present continuous for spinner display ("Running tests", "Building API")
- `addBlockedBy` — task IDs that must complete first (creates phase sequencing)

### Markdown Fallback (for summary output)

For session overviews and sprint reviews, use markdown tables:

```markdown
| Phase | Status | Duration | Notes |
|-------|--------|----------|-------|
| Plan | Done | 2m | Architecture approved |
| Build | In Progress | 8m | 2/3 components done |
| Test | Blocked | — | Blocked on build |
```

### Status Block (for quick checks)
```
Cost: $2.40 today | $38.20 MTD | Budget: $100/mo
Active: 2 worktrees | 1 agent running
Completed: 3/5 phases | 12 files changed
```

Use TaskCreate for live progress during execution. Use markdown tables for summaries. Use status blocks for quick checks.

---

## AGENT SELECTION

### Decision Logic

When routing a task to an agent:

1. **Identify task type** — debug, review, build, explore, research
2. **Check capability matrix** — see `/agent-capability-matrix-skill`
3. **Select model tier** — haiku for search/classify, sonnet for code, opus for architecture
4. **Check budget** — run cost gate before expensive operations

### Quick Selection Table

| Task Type | Primary Agent | Fallback | Model |
|-----------|--------------|----------|-------|
| Debug | debug-like-expert | general-purpose | sonnet |
| Code Review | code-reviewer | feature-dev:code-reviewer | haiku |
| Architecture | Plan agent | code-architect | opus |
| Security | security-skill | general-purpose | sonnet |
| Testing | testing-skill | general-purpose | sonnet |
| Explore | Explore agent | Grep/Glob direct | haiku |
| Research | research-skill | WebSearch | sonnet |
| Parallel Build | agent-teams | worktree-manager | sonnet |

### Failure Recovery

If an agent fails or returns poor results:
1. Try the fallback agent from the table above
2. If fallback fails, escalate to a higher model tier
3. If still failing, checkpoint current state and ask user

---

## CLAUDE CODE COMMANDS

| Command | Workflow |
|---------|----------|
| `/start-day` | Start Day protocol — context scan, cost status |
| `/build-feature <name>` | Feature Development — plan → build → test → ship |
| `/end-day` | End Day protocol — security sweep, context save |
| `/quick-fix <issue>` | Targeted debug flow — evidence → hypothesis → fix |
| `/cost-check` | Display daily/MTD spend and budget status |

---

## GTME PERSPECTIVE

This workflow system demonstrates core Go-To-Market Engineer capabilities:

1. **Systematization** - Converting ad-hoc processes into repeatable, documented workflows
2. **Cost Awareness** - Unit economics thinking (cost-per-task, cost-per-lead mindset)
3. **Parallelization** - Orchestrating complex multi-agent systems efficiently
4. **Documentation Discipline** - Audit trails that prove capability
5. **Tool Integration** - Connecting sales, engineering, and ops tooling

**Portfolio Value:** This skill itself is a GTME portfolio piece showing technical depth + process thinking + cost optimization - directly relevant for roles combining GTM strategy with technical implementation.