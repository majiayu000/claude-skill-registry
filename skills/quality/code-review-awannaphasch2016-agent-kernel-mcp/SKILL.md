---
name: code-review
description: Code review checklist covering security, performance, defensive programming, and testing anti-patterns. Use before merging PRs, after implementing features, or when reviewing code quality.
---

# Code Review Skill

**Tech Stack**: Python 3.11+, pytest, AWS Lambda, Aurora MySQL

**Source**: Extracted from CLAUDE.md code quality principles and testing patterns.

---

## When to Use This Skill

Use the code-review skill when:
- ✓ Reviewing pull requests
- ✓ After implementing significant features
- ✓ Before merging to main/dev
- ✓ Auditing legacy code for issues
- ✓ Post-incident code review

**DO NOT use this skill for:**
- ✗ Simple typo fixes (no review needed)
- ✗ Documentation-only changes
- ✗ Automated dependency updates (unless major version)

---

## Quick Review Decision Tree

```
What type of change?
├─ Security-sensitive? (auth, permissions, data access)
│  └─ Review SECURITY.md checklist
│
├─ Performance-critical? (Lambda, DB queries, API calls)
│  └─ Review PERFORMANCE.md checklist
│
├─ Distributed system? (Lambda, Aurora, S3, SQS, Step Functions)
│  └─ Review Boundary Verification section + execution-boundaries.md
│
├─ Error handling? (try/catch, validation, failures)
│  └─ Review DEFENSIVE.md checklist
│
├─ Tests added/modified?
│  └─ Check testing-workflow skill anti-patterns
│
└─ General code quality?
   └─ Review all sections
```

---

## Core Review Principles

### Principle 1: Fail Fast and Visibly

**From CLAUDE.md:**
> "Fail fast and visibly when something is wrong. Silent failures hide bugs."

**Review Checklist:**

```python
# ❌ REJECT: Silent failure
def store_report(symbol, data):
    try:
        result = db.execute(query, params)
        return True  # Always returns True!
    except Exception as e:
        logger.warning(f"DB error: {e}")  # Logged at WARNING
        return True  # ❌ Still returns True!

# ✅ APPROVE: Explicit failure
def store_report(symbol, data):
    rowcount = db.execute(query, params)
    if rowcount == 0:
        logger.error(f"INSERT affected 0 rows for {symbol}")
        return False  # ✅ Explicit failure signal
    return True
```

**Questions to Ask:**
- [ ] Does this function check operation outcomes (not just exceptions)?
- [ ] Are errors logged at ERROR level (not WARNING)?
- [ ] Does the function return explicit success/failure indicators?

### Principle 2: Validate Prerequisites

**From CLAUDE.md:**
> "Before executing a workflow node, validate that all prerequisite data exists and is non-empty."

**Review Checklist:**

```python
# ❌ REJECT: Assumes upstream succeeded
def analyze_technical(state: AgentState) -> AgentState:
    result = analyzer.calculate_indicators(state['ticker_data'])
    state['indicators'] = result  # Might be {} if ticker_data was empty!
    return state

# ✅ APPROVE: Validates prerequisites
def analyze_technical(state: AgentState) -> AgentState:
    # VALIDATION GATE
    if not state.get('ticker_data') or len(state['ticker_data']) == 0:
        logger.error(f"Cannot analyze: ticker_data is empty for {state['ticker']}")
        state['error'] = "Missing ticker data"
        return state

    # Safe to proceed
    result = analyzer.calculate_indicators(state['ticker_data'])
    state['indicators'] = result
    return state
```

**Questions to Ask:**
- [ ] Does this function validate inputs before processing?
- [ ] Does it check that prerequisite data exists AND is non-empty?
- [ ] Does it fail explicitly if prerequisites are missing?

### Principle 3: No Silent None Propagation

**From CLAUDE.md:**
> "Functions that return `None` on failure create cascading silent failures."

**Review Checklist:**

```python
# ❌ REJECT: Returns None hides failures
def fetch_ticker_data(ticker: str):
    hist = yf.download(ticker, period='1y')
    if hist is None or hist.empty:
        logger.warning(f"No data for {ticker}")
        return None  # ✗ Caller doesn't know WHY it failed

# ✅ APPROVE: Raises explicit exception
def fetch_ticker_data(ticker: str):
    hist = yf.download(ticker, period='1y')
    if hist is None or hist.empty:
        error_msg = f"No historical data for {ticker}"
        logger.error(error_msg)
        raise ValueError(error_msg)  # ✓ Explicit failure
```

**Questions to Ask:**
- [ ] Does this function return None on error?
- [ ] Would an exception be more appropriate?
- [ ] Does the caller know HOW to handle None?

---

## Review Checklists by Category

### Security Review

See [SECURITY.md](SECURITY.md) for:
- Authentication/authorization
- SQL injection prevention
- XSS prevention
- Secrets management
- Input validation

### Performance Review

See [PERFORMANCE.md](PERFORMANCE.md) for:
- Lambda cold start optimization
- Database query patterns
- Caching strategies
- External API efficiency

### Defensive Programming Review

See [DEFENSIVE.md](DEFENSIVE.md) for:
- Error handling patterns
- Validation gates
- Boundary type checking
- Silent failure detection

### Boundary Verification Review

**When**: Code changes affect distributed systems (Lambda, Aurora, S3, SQS, Step Functions)

**Checklist**:
- [ ] **WHERE**: Execution environment identified (Lambda, EC2, local)?
- [ ] **WHAT env**: Environment variables verified (Terraform/Doppler)?
- [ ] **WHAT services**: External systems identified (Aurora schema, S3 bucket)?
- [ ] **WHAT properties**: Entity configuration verified (timeout, memory, concurrency)?
- [ ] **WHAT intention**: Usage matches designed purpose (sync vs async)?
- [ ] **Contract verification**: Boundaries verified through ground truth (not just code inspection)

**Common boundary failures to catch**:
- ❌ Missing env var (code expects, Terraform doesn't provide)
- ❌ Schema mismatch (code INSERT vs Aurora columns)
- ❌ Permission denied (IAM role vs resource policy)
- ❌ Timeout mismatch (code needs 120s, Lambda configured 30s)
- ❌ Intention violation (sync Lambda for async workload)

**Quick checks**:
```bash
# Verify Lambda configuration matches code requirements
aws lambda get-function-configuration \
  --function-name <name> \
  --query '{Timeout:Timeout, Memory:MemorySize}'

# Verify Aurora schema matches code
mysql> SHOW COLUMNS FROM table_name;

# Verify IAM permissions
aws iam get-role-policy --role-name <role> --policy-name <policy>
```

**See**: [Execution Boundary Checklist](../../checklists/execution-boundaries.md) for comprehensive verification

**Related**: Principle #20 (CLAUDE.md) - Execution Boundary Discipline

---

## Common Code Smells

### Smell 1: God Object

**Symptom:** Single class/module with >500 lines doing many things.

```python
# ❌ BAD: God object
class ReportService:
    """1200 lines - does everything!"""

    def fetch_data(self): pass
    def analyze_technical(self): pass
    def analyze_fundamental(self): pass
    def fetch_news(self): pass
    def generate_report(self): pass
    def score_report(self): pass
    def send_to_user(self): pass
    def log_to_analytics(self): pass
    # ... 20 more methods

# ✅ GOOD: Separated concerns
class DataFetcher:
    def fetch_ticker_data(self): pass

class TechnicalAnalyzer:
    def analyze(self): pass

class ReportGenerator:
    def generate(self): pass
```

**Review Action:** Request refactoring if class > 500 LOC or > 10 methods.

### Smell 2: Magic Numbers

```python
# ❌ BAD: Magic numbers
if rsi > 70:  # What does 70 mean?
    return "Overbought"

if len(price_history) < 30:  # Why 30?
    raise ValueError("Insufficient data")

# ✅ GOOD: Named constants
RSI_OVERBOUGHT_THRESHOLD = 70
MIN_PRICE_HISTORY_DAYS = 30

if rsi > RSI_OVERBOUGHT_THRESHOLD:
    return "Overbought"

if len(price_history) < MIN_PRICE_HISTORY_DAYS:
    raise ValueError(f"Need {MIN_PRICE_HISTORY_DAYS} days of data")
```

### Smell 3: Long Parameter List

```python
# ❌ BAD: 7 parameters
def generate_report(ticker, price, sma20, sma50, rsi, macd, volume):
    pass

# ✅ GOOD: Parameter object
from dataclasses import dataclass

@dataclass
class MarketData:
    ticker: str
    price: float
    sma20: float
    sma50: float
    rsi: float
    macd: dict
    volume: int

def generate_report(data: MarketData):
    pass
```

**Review Action:** Request refactoring if function has > 4 parameters.

---

## Testing Review

### Anti-Pattern 1: The Liar (Can't Fail)

```python
# ❌ REJECT: Test that can't fail
def test_store_report(self):
    mock_client = MagicMock()
    service.store_report('NVDA19', 'report')
    mock_client.execute.assert_called()  # Only checks "was it called?"

# ✅ APPROVE: Test that can actually fail
def test_store_report_detects_failure(self):
    mock_client = MagicMock()
    mock_client.execute.return_value = 0  # Simulate failure
    result = service.store_report('NVDA19', 'report')
    assert result is False
```

**Review Question:** "If I break the code, does this test fail?"

### Anti-Pattern 2: Happy Path Only

```python
# ❌ REJECT: Only success tested
def test_fetch_ticker(self):
    mock_yf.download.return_value = sample_dataframe
    result = service.fetch('NVDA')
    assert result is not None

# ✅ APPROVE: Both success AND failure
def test_fetch_ticker_success(self):
    mock_yf.download.return_value = sample_dataframe
    result = service.fetch('NVDA')
    assert len(result) > 0

def test_fetch_ticker_handles_empty(self):
    mock_yf.download.return_value = pd.DataFrame()
    with pytest.raises(ValueError):
        service.fetch('INVALID')
```

**Review Question:** "Are failure paths tested?"

---

## PR Review Process

### Step 1: High-Level Review (5 minutes)

```bash
# Check PR description
# - What problem does this solve?
# - Why this approach?
# - Any breaking changes?

# Check files changed
gh pr diff 123

# Size check
LINES_CHANGED=$(gh pr diff 123 --stat | tail -1)
# If > 500 lines, ask to split PR
```

**Questions:**
- [ ] Is PR description clear?
- [ ] Are changes focused (not mixing features)?
- [ ] Is PR size reasonable (< 500 lines)?

### Step 2: Security Review (10 minutes)

See [SECURITY.md](SECURITY.md) for detailed checklist.

**Quick checks:**
- [ ] No secrets hardcoded?
- [ ] Input validation present?
- [ ] SQL injection safe?
- [ ] XSS prevention?

### Step 3: Logic Review (20 minutes)

```python
# Read the code, ask:

# 1. Does it handle errors?
try:
    result = risky_operation()
except SpecificException as e:  # ✅ Specific exception
    logger.error(f"Failed: {e}")
    raise  # ✅ Re-raise or return False

# 2. Does it validate inputs?
if not ticker or len(ticker) > 10:
    raise ValueError("Invalid ticker")

# 3. Does it check outcomes?
rowcount = db.execute(query)
if rowcount == 0:
    return False  # Explicit failure
```

### Step 4: Test Review (10 minutes)

```bash
# Run tests locally
gh pr checkout 123
pytest

# Check test coverage
pytest --cov=src/module tests/test_module.py

# Review test quality (not just quantity)
```

**Questions:**
- [ ] Are new features tested?
- [ ] Are edge cases covered?
- [ ] Do tests follow patterns (see testing-workflow skill)?

### Step 5: Performance Review (5 minutes)

See [PERFORMANCE.md](PERFORMANCE.md) for detailed checklist.

**Quick checks:**
- [ ] N+1 query pattern avoided?
- [ ] Caching appropriate?
- [ ] Lambda timeout reasonable?

### Step 6: Boundary Verification (If distributed system changes)

**When to apply**: PR modifies Lambda, Aurora, S3, SQS, Step Functions, or cross-service integrations

**Quick assessment**:
```bash
# Check if PR touches distributed system boundaries
git diff main...PR-branch | grep -E "lambda|aurora|s3|sqs|stepfunctions"
```

**If YES, verify boundaries**:
- [ ] **Execution environment**: WHERE does modified code run?
- [ ] **Environment variables**: Code expectations vs Terraform reality?
- [ ] **External services**: Schema/format contracts verified?
- [ ] **Entity configuration**: Timeout/memory match code requirements?
- [ ] **Usage intention**: Sync/async pattern matches entity design?

**Example checks**:
```bash
# Lambda timeout matches code execution time?
aws lambda get-function-configuration --function-name <name> \
  --query 'Timeout'
# Compare with code's longest execution path

# Aurora schema matches INSERT queries?
mysql> SHOW COLUMNS FROM table_name;
# Compare with code's INSERT/UPDATE queries

# IAM permissions allow code's operations?
aws iam get-role-policy --role-name <role> --policy-name <policy>
# Compare with code's aws sdk calls
```

**See**: [Execution Boundary Checklist](../../checklists/execution-boundaries.md) for comprehensive verification

**Skip if**: PR only touches frontend, documentation, or single-process logic

---

## Approval Checklist

Before approving PR, verify ALL of these:

### Correctness
- [ ] Logic is sound
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] Tests pass

### Security
- [ ] No hardcoded secrets
- [ ] Input validated
- [ ] SQL injection safe
- [ ] XSS safe

### Performance
- [ ] No obvious bottlenecks
- [ ] Caching used appropriately
- [ ] DB queries optimized

### Code Quality
- [ ] Follows project style
- [ ] Functions < 50 LOC
- [ ] Classes < 500 LOC
- [ ] Clear naming

### Testing
- [ ] New code tested
- [ ] Both success and failure paths
- [ ] No test anti-patterns

### Documentation
- [ ] Docstrings present
- [ ] Complex logic commented
- [ ] README updated if needed

### Boundary Verification (Distributed Systems)
- [ ] Execution boundaries identified (WHERE code runs)
- [ ] Environment variables verified (Terraform/Doppler match code)
- [ ] External service contracts verified (Aurora schema, S3 format, API payload)
- [ ] Entity configuration verified (timeout, memory, concurrency)
- [ ] Usage intention verified (sync/async pattern matches design)
- [ ] Progressive evidence applied (verified through ground truth, not just code)

---

## Quick Reference

### Review Time Budget

| PR Size | Review Time | Focus Areas |
|---------|-------------|-------------|
| **< 50 lines** | 10 min | Logic, tests |
| **50-200 lines** | 30 min | All checklists |
| **200-500 lines** | 60 min | Deep review |
| **> 500 lines** | Request split | Too large |

### Common Rejection Reasons

| Issue | Severity | Action |
|-------|----------|--------|
| **Hardcoded secrets** | Critical | Reject immediately |
| **No error handling** | High | Request changes |
| **No tests** | High | Request tests |
| **Silent failures** | High | Request explicit failures |
| **Magic numbers** | Medium | Request refactoring |
| **Missing docstrings** | Low | Request docs |

---

## File Organization

```
.claude/skills/code-review/
├── SKILL.md          # This file (entry point)
├── SECURITY.md       # Security review checklist
├── PERFORMANCE.md    # Performance review patterns
└── DEFENSIVE.md      # Defensive programming review
```

---

## Next Steps

- **For security review**: See [SECURITY.md](SECURITY.md)
- **For performance review**: See [PERFORMANCE.md](PERFORMANCE.md)
- **For defensive review**: See [DEFENSIVE.md](DEFENSIVE.md)
- **For test patterns**: See testing-workflow skill

---

## References

- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [The Art of Readable Code](https://www.oreilly.com/library/view/the-art-of/9781449318482/)
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Code Review Best Practices](https://stackoverflow.blog/2019/09/30/how-to-make-good-code-reviews-better/)
