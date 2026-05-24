---
name: research
description: Systematic investigation and root cause analysis. Use when debugging persistent issues, understanding complex systems, or before making architectural decisions.
---

# Research Skill

**Tech Stack**: AWS CLI, Git, ripgrep, jq, curl, browser DevTools

**Source**: Extracted from CLAUDE.md investigation principles and debugging patterns.

---

## When to Use This Skill

Use the research skill when:
- ✓ Same bug persists after 2+ fix attempts
- ✓ Need to understand unfamiliar codebase
- ✓ Investigating production incidents
- ✓ Making architectural decisions
- ✓ Debugging complex system interactions
- ✓ Learning new technology/library

**DO NOT use this skill for:**
- ✗ First fix attempt (try the obvious solution first)
- ✗ Well-understood problems (just fix it)
- ✗ Time-critical incidents (fix first, investigate later)

---

## Quick Research Decision Tree

```
What's the problem?
├─ First time seeing this issue?
│  ├─ YES → Try obvious fix (iteration)
│  └─ NO → Same bug after 2 attempts? → RESEARCH
│
├─ Production incident?
│  ├─ Affecting users NOW? → Rollback/hotfix first, research later
│  └─ Post-incident analysis? → Deep research
│
├─ Need to understand codebase?
│  ├─ Specific function/module? → Read code + tests
│  ├─ System architecture? → Trace request flow
│  └─ Historical context? → Git blame + commit history
│
├─ Technology decision?
│  ├─ Read official docs (not blog posts)
│  ├─ Compare alternatives (trade-offs)
│  ├─ Prototype with real use case
│  └─ Document decision (ADR)
│
└─ API/Library integration?
   ├─ Read type requirements (don't assume)
   ├─ Check version compatibility
   ├─ Test minimal example
   └─ Verify with actual data
```

---

## Loop Pattern: Meta-Loop → Initial-Sensitive

**Escalation Trigger**:
- `/reflect` reveals: "I've tried 3 fixes, all failed with same error"
- `/trace` output identical across attempts
- **Pattern**: Stuck in retrying loop (execution changes, outcome doesn't)
- **Action**: Use `/hypothesis` to question assumptions (switch to initial-sensitive)

**Tools Used**:
- `/observe` - Notice system behavior (what's failing)
- `/hypothesis` - Generate alternative explanations (why might it fail differently than I think?)
- `/research` - Test hypotheses systematically
- `/validate` - Check if new understanding correct
- `/reflect` - Synthesize learnings after investigation

**Why This Works**: Research skill naturally fits initial-sensitive loop—you're questioning assumptions, not just fixing execution.

See [Thinking Process Architecture - Feedback Loops](../../.claude/diagrams/thinking-process-architecture.md#11-feedback-loop-types-self-healing-properties) for structural overview.

---

## Core Research Principles

### Principle 1: Research Before Iteration

**From CLAUDE.md:**
> "When same bug persists after 2 fix attempts, STOP iterating and START researching. Invest 30-60 minutes understanding root cause instead of deploying more guesses."

**Why This Matters:**
- ❌ Iteration: Fast feedback, but wasteful after 2+ failed attempts
- ✅ Research: Upfront cost, prevents 3+ failed deployment cycles

**Pattern:**

```
Attempt 1: Hypothesis + Deploy (8 minutes)
  ↓ Failed
Attempt 2: Different hypothesis + Deploy (8 minutes)
  ↓ Failed
Attempt 3: ❌ STOP - Don't deploy another guess

SWITCH TO RESEARCH MODE:
  - Read specs/docs (15 minutes)
  - Inspect real data (10 minutes)
  - Reproduce locally (20 minutes)
  - Identify root cause (15 minutes)
  ↓ Total: 60 minutes research

Attempt 3 (with root cause): Deploy fix (8 minutes)
  ✅ Success

Total time: 76 minutes (vs 120+ minutes with blind iteration)
```

### Principle 2: Read Primary Sources

**Hierarchy of Information Quality:**

| Source Type | Reliability | When to Use |
|-------------|-------------|-------------|
| **Official Docs** | Highest | First stop for API behavior, type requirements |
| **Source Code** | Very High | When docs are unclear or incomplete |
| **GitHub Issues** | High | For known bugs, edge cases, workarounds |
| **Stack Overflow** | Medium | For common problems, after reading docs |
| **Blog Posts** | Low | For general concepts, not implementation details |
| **ChatGPT/AI** | Lowest | Starting point only, always verify |

**Example: Type System Integration**

```bash
# ❌ DON'T: Ask ChatGPT "Does PyMySQL accept dicts for JSON columns?"
# ChatGPT might hallucinate or give outdated answer

# ✅ DO: Read PyMySQL documentation
open https://pymysql.readthedocs.io/en/latest/

# ✅ DO: Test with minimal example
python3 << 'EOF'
import pymysql
import json

# Test: Does PyMySQL accept dict for JSON column?
data = {'key': 'value'}

try:
    cursor.execute("INSERT INTO test (json_col) VALUES (%s)", (data,))
    print("✅ Dict accepted")
except TypeError as e:
    print(f"❌ Dict rejected: {e}")
    # Try JSON string instead
    cursor.execute("INSERT INTO test (json_col) VALUES (%s)", (json.dumps(data),))
    print("✅ JSON string accepted")
EOF
```

### Principle 3: Reproduce Locally

**Before deploying fixes, reproduce the issue locally.**

**Benefits:**
- ✅ Fast iteration (seconds vs minutes)
- ✅ Can debug with breakpoints
- ✅ No cloud costs
- ✅ Can test edge cases easily

**Pattern:**

```bash
# Step 1: Extract minimal failing case
# Instead of testing entire Lambda function...

# ❌ BAD: Deploy to AWS, check logs, repeat
aws lambda invoke --function-name worker --payload '{}' /tmp/response.json
# Wait 30 seconds for CloudWatch logs...

# ✅ GOOD: Reproduce locally
python3 << 'EOF'
from src.data.news_fetcher import NewsFetcher

# Exact same code as Lambda
fetcher = NewsFetcher()
result = fetcher.fetch_news('NVDA19')
print(result)  # Immediate feedback
EOF
```

### Principle 4: Inspect Real Data

**Don't assume data shape—verify with actual examples.**

**Common Mistakes:**
- Assuming API returns dict (might return list)
- Assuming field exists (might be null/missing)
- Assuming type (might be string not int)

**Pattern:**

```bash
# ❌ DON'T: Assume
# "The API returns a list of tickers"

# ✅ DO: Verify
curl -s https://api.example.com/tickers | jq . > sample_response.json
cat sample_response.json

# Inspect structure:
# - Is it a list or dict?
# - What fields are present?
# - What types are they?
# - Any null values?
# - Any nested structures?
```

**Example: Aurora Schema Investigation**

```bash
# Connect to Aurora via SSM tunnel
aws ssm start-session \
  --target i-1234567890abcdef0 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["aurora-endpoint"],"portNumber":["3306"],"localPortNumber":["3307"]}'

# Inspect actual schema (don't assume)
mysql -h 127.0.0.1 -P 3307 -u admin -p << 'SQL'
DESCRIBE precomputed_reports;

-- Check actual data types
SELECT
  symbol,
  report_json,
  typeof(report_json) as json_type
FROM precomputed_reports
LIMIT 1 \G

-- Check for null values
SELECT COUNT(*) as total,
       SUM(CASE WHEN report_json IS NULL THEN 1 ELSE 0 END) as null_count
FROM precomputed_reports;
SQL
```

---

## Research Workflow

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step research process.

---

## Investigation Checklist

See [INVESTIGATION-CHECKLIST.md](INVESTIGATION-CHECKLIST.md) for systematic debugging checklist.

---

## Boundary Verification

**When**: Investigating distributed systems (Lambda, Aurora, S3, SQS, Step Functions)

**Problem**: Code looks correct but fails in production due to unverified execution boundaries

**Critical questions**:
- WHERE does this code run? (Lambda, EC2, local?)
- WHAT environment does it require? (env vars, network, permissions?)
- WHAT external systems does it call? (Aurora schema, S3 bucket, API format?)
- WHAT are entity properties? (Lambda timeout/memory, Aurora connection limits, intended usage)
- HOW do I verify the contract? (Terraform config, SHOW COLUMNS, test access?)

**Five layers of correctness**:
1. **Syntactic**: Code compiles (Python syntax valid)
2. **Semantic**: Code does what it claims (logic correct)
3. **Boundary**: Code can reach what it needs (network, permissions)
4. **Configuration**: Entity config matches code requirements (timeout, memory)
5. **Intentional**: Usage matches designed purpose (sync Lambda not for async work)

**When to apply**:
- "Code looks correct but doesn't work" bugs
- Multi-service workflows (Lambda → Aurora → S3)
- After 2 failed deployment attempts (infrastructure issues)
- Before concluding "code is correct" (verify execution context)

**Verification workflow**:
```
1. Identify execution boundaries (code → runtime, code → database, service → service)
2. Identify physical entities (WHICH Lambda, WHICH Aurora, WHICH S3 bucket)
3. Verify configuration matches requirements (timeout, memory, concurrency)
4. Verify intention matches usage (async Lambda not for sync API)
5. Progress through evidence layers (code → config → runtime → ground truth)
```

**Integration with research workflow**:
- **Phase 1 (Observe)**: Notice boundary-related failure (timeout, permission denied, schema mismatch)
- **Phase 2 (Hypothesize)**: Identify which boundary might be violated
- **Phase 3 (Research)**: Apply boundary verification checklist systematically
- **Phase 4 (Validate)**: Verify contract through ground truth (test actual execution)

**See**: [Execution Boundary Checklist](../../checklists/execution-boundaries.md) for comprehensive verification workflow

**Related principles**:
- Principle #20 (Execution Boundary Discipline) - CLAUDE.md
- Principle #2 (Progressive Evidence Strengthening) - Verify through all layers
- Principle #15 (Infrastructure-Application Contract) - Sync code and infrastructure

---

## Architectural Investigations

**When**: Choosing between technologies, patterns, or architectural approaches

**Problem**: "X vs Y" comparisons get vague "it depends" answers without structured analysis

**Solution**: Apply OWL-based relationship analysis framework for systematic comparison

**Steps**:
1. **Define concepts being compared**
   - What is X? (definition, location, purpose, examples)
   - What is Y? (definition, location, purpose, examples)

2. **Apply 4 relationship types**:
   - **Part-Whole**: Is one part of the other, or are they peers?
   - **Complement**: Do they handle non-overlapping concerns that work together?
   - **Substitution**: Can one replace the other? Under what conditions?
   - **Composition**: Can they be layered/composed into a multi-tier system?

3. **Document with concrete examples**
   - Provide real scenarios, not abstract theory
   - Include trade-off analysis (what you gain vs lose)

4. **Make recommendation based on analysis**
   - Grounded in relationship analysis, not intuition
   - Include anti-patterns to avoid

**See**: [Relationship Analysis Guide](docs/RELATIONSHIP_ANALYSIS.md) for comprehensive methodology

**Example Use Cases**:
- "Should I use Redis or DynamoDB for caching?" → Apply substitution & composition analysis
- "How do CDN and application caching relate?" → Apply complement & composition analysis
- "Microservices vs Monolith?" → Apply part-whole & trade-off analysis

---

## Common Research Scenarios

### Scenario 1: Type System Mismatch

**Symptom:** Same error after 2 attempts, silent failure

**Research Steps:**

1. **Read Target System Documentation**
   ```bash
   # PyMySQL docs
   open https://pymysql.readthedocs.io/en/latest/modules/cursors.html

   # Look for: What types does execute() accept?
   ```

2. **Test Minimal Example**
   ```python
   import pymysql
   import json

   # Test hypothesis: Dict vs JSON string
   data = {'key': 'value'}

   # Test 1: Dict
   try:
       cursor.execute("INSERT INTO test (json_col) VALUES (%s)", (data,))
   except TypeError as e:
       print(f"Dict failed: {e}")

   # Test 2: JSON string
   cursor.execute("INSERT INTO test (json_col) VALUES (%s)", (json.dumps(data),))
   print("JSON string succeeded")
   ```

3. **Apply Fix with Confidence**
   ```python
   # Now we KNOW json.dumps() is required
   def store_report(symbol: str, report_json: dict):
       cursor.execute(
           "INSERT INTO reports (symbol, report_json) VALUES (%s, %s)",
           (symbol, json.dumps(report_json))  # Convert to string
       )
   ```

### Scenario 2: Production Incident

**Symptom:** Users reporting errors, dashboard shows spike

**Research Steps:**

1. **Triage (< 5 minutes)**
   ```bash
   # Check error count
   aws logs filter-log-events \
     --log-group-name /aws/lambda/worker \
     --start-time $(($(date +%s) - 600))000 \
     --filter-pattern "ERROR" \
     --query 'length(events)'

   # Check when it started
   aws cloudwatch get-metric-statistics \
     --namespace AWS/Lambda \
     --metric-name Errors \
     --dimensions Name=FunctionName,Value=worker \
     --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
     --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
     --period 60 \
     --statistics Sum
   ```

2. **Immediate Mitigation (< 10 minutes)**
   ```bash
   # Rollback to previous version
   CURRENT=$(aws lambda get-alias --function-name worker --name live \
     --query 'FunctionVersion' --output text)

   PREVIOUS=$((CURRENT - 1))

   aws lambda update-alias \
     --function-name worker \
     --name live \
     --function-version $PREVIOUS

   echo "Rolled back from v$CURRENT to v$PREVIOUS"
   ```

3. **Post-Incident Analysis (30-60 minutes)**
   ```bash
   # Collect evidence
   mkdir incident-$(date +%Y%m%d-%H%M%S)
   cd incident-*

   # Export error logs
   aws logs filter-log-events \
     --log-group-name /aws/lambda/worker \
     --start-time $INCIDENT_START \
     --end-time $INCIDENT_END \
     --filter-pattern "ERROR" > errors.json

   # Export metrics
   aws cloudwatch get-metric-statistics ... > metrics.json

   # Get deployment diff
   git diff v$PREVIOUS v$CURRENT > deployment.diff

   # Analyze (root cause analysis)
   # - What changed?
   # - What failed?
   # - Why did it fail?
   # - How to prevent?
   ```

### Scenario 3: Unfamiliar Codebase

**Task:** Add feature to module you've never seen

**Research Steps:**

1. **Find Entry Point**
   ```bash
   # Search for main function
   rg "def main" --type py

   # Search for Lambda handler
   rg "def lambda_handler" --type py

   # Search for CLI entry point
   rg "click.command" --type py
   ```

2. **Trace Request Flow**
   ```bash
   # Example: How does a ticker report get generated?

   # Step 1: Find API endpoint
   rg "\/api\/reports" src/
   # Found: src/telegram/api/routes/reports.py

   # Step 2: Read route handler
   cat src/telegram/api/routes/reports.py
   # Calls: ReportService.generate_report()

   # Step 3: Find service
   rg "class ReportService" src/
   # Found: src/telegram/services/report_service.py

   # Step 4: Read service
   cat src/telegram/services/report_service.py
   # Calls: workflow.run() with AgentState

   # Step 5: Find workflow
   rg "def run" src/workflow/
   # Found: src/workflow/graph.py
   ```

3. **Read Tests for Examples**
   ```bash
   # Tests show how to use the code
   rg "test.*generate_report" tests/ --type py

   cat tests/telegram/services/test_report_service.py
   # Shows:
   # - How to mock dependencies
   # - Expected input format
   # - Expected output structure
   ```

4. **Check Git History for Context**
   ```bash
   # Why was this code written?
   git log --oneline src/telegram/services/report_service.py

   # Read relevant commits
   git show abc123

   # Find related PRs
   gh pr list --search "report service" --state closed
   ```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Iteration Without Research

```bash
# ❌ BAD: Blind iteration
git commit -m "Try fix 1"
git push
# Wait 8 minutes...
# Failed

git commit -m "Try fix 2"
git push
# Wait 8 minutes...
# Failed

git commit -m "Try fix 3"
git push
# Wait 8 minutes...
# Failed

# Total: 24+ minutes wasted
```

**Solution:** After 2 attempts, research the root cause.

### Anti-Pattern 2: Trusting Secondary Sources

```bash
# ❌ BAD: Trust blog post
# Blog: "PyMySQL accepts dicts for JSON columns"
cursor.execute("INSERT INTO tbl (json_col) VALUES (%s)", ({'key': 'val'},))
# TypeError: not all arguments converted

# ✅ GOOD: Read official docs
open https://pymysql.readthedocs.io/
# Docs: "Parameters are passed as tuples"
# Must convert dict to JSON string first
cursor.execute("INSERT INTO tbl (json_col) VALUES (%s)", (json.dumps({'key': 'val'}),))
```

### Anti-Pattern 3: Assuming Instead of Verifying

```bash
# ❌ BAD: Assume
# "The API probably returns a list of dicts"
for ticker in response:  # Crashes if response is dict, not list
    process(ticker)

# ✅ GOOD: Verify
curl -s https://api.example.com/tickers | jq . > sample.json
cat sample.json
# Oh, it's actually a dict with a 'tickers' key!

for ticker in response['tickers']:  # Correct
    process(ticker)
```

---

## Quick Reference

### Research Triggers

| Situation | Action |
|-----------|--------|
| First attempt failed | Try one more fix |
| Second attempt failed | **START RESEARCH** |
| Production incident | Mitigate first, research later |
| Unfamiliar codebase | Trace request flow, read tests |
| API integration | Read official docs, test minimal example |
| Type mismatch | Inspect real data, verify assumptions |

### Time Investment

| Research Type | Time Budget | Expected Outcome |
|---------------|-------------|------------------|
| **Quick lookup** | 5-10 minutes | Confirm type, read docs |
| **Root cause analysis** | 30-60 minutes | Understand why bug persists |
| **Codebase exploration** | 1-2 hours | Understand module/system |
| **Technology evaluation** | 4-8 hours | Compare alternatives, prototype |

---

## File Organization

```
.claude/skills/research/
├── SKILL.md                    # This file (entry point)
├── WORKFLOW.md                 # Step-by-step research process
└── INVESTIGATION-CHECKLIST.md  # Systematic debugging checklist
```

---

## Next Steps

- **For research workflow**: See [WORKFLOW.md](WORKFLOW.md)
- **For debugging checklist**: See [INVESTIGATION-CHECKLIST.md](INVESTIGATION-CHECKLIST.md)

---

## References

- [How to Debug](https://blog.regehr.org/archives/199) - Systematic debugging by John Regehr
- [The Scientific Method of Debugging](https://www.brendangregg.com/blog/2016-02-08/linux-load-averages.html) - Brendan Gregg
- [Debugging: The 9 Indispensable Rules](https://debuggingrules.com/)
- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) - Investigation methodologies
