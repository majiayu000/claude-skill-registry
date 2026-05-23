---
name: "workflow-orchestrator"
description: "Project workflow system - cost tracking, parallel execution, security gates, agent orchestration. Use when: start day, begin session, status check, new feature, build, implement, end day, wrap up, debug, investigate, research, evaluate."
---

# Workflow Orchestrator Skill v2.0

Universal project workflow system with cost tracking, parallel execution, security gates, and intelligent agent orchestration.

## Triggers

- **Session Management:** "start day", "begin session", "what's the status", "end day", "wrap up", "done for today"
- **Feature Development:** "new feature", "build", "implement"  
- **Debugging:** "debug", "investigate", "why is this broken"
- **Research:** "research", "evaluate", "should we use"

---

## START DAY

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
ls /Users/tmkipper/Desktop/tk_projects/mcp-server-cookbook/ 2>/dev/null

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
2. Map to agents (use workflow-enforcer 70+ catalog)
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

## GTME PERSPECTIVE

This workflow system demonstrates core Go-To-Market Engineer capabilities:

1. **Systematization** - Converting ad-hoc processes into repeatable, documented workflows
2. **Cost Awareness** - Unit economics thinking (cost-per-task, cost-per-lead mindset)
3. **Parallelization** - Orchestrating complex multi-agent systems efficiently
4. **Documentation Discipline** - Audit trails that prove capability
5. **Tool Integration** - Connecting sales, engineering, and ops tooling

**Portfolio Value:** This skill itself is a GTME portfolio piece showing technical depth + process thinking + cost optimization - directly relevant for roles combining GTM strategy with technical implementation.