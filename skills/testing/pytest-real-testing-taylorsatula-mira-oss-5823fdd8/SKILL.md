---
name: Real Pytest - No Mocks, Real Tests
description: Write pytests that test real public interfaces with actual components, no mocking, and precise assertions. MIRA-specific patterns. Use when creating or reviewing tests.
---

# Real Testing Philosophy

## CRITICAL MINDSET SHIFT

**Tests that verify implementation are worse than no tests** - they provide false confidence while catching nothing.

**Your job is not to confirm the code works. Your job is to:**
1. **Think critically about the contract** - what SHOULD this module do?
2. **Surface design problems** - is this module papering over architectural failures?
3. **Write tests that enforce guarantees** - not tests that mirror implementation
4. **Prove tests can fail** - see them fail first, verify failure modes are correct

Tests that always pass are actively harmful. They waste time and provide false security.

### 🚨 NEVER SKIP TESTS

**ABSOLUTE RULE: Do NOT use `@pytest.mark.skip`, `@pytest.mark.skipif`, or `pytest.skip()`**

Tests either:
- ✅ **PASS** - the code works correctly
- ❌ **FAIL** - the code is broken and needs fixing

There is no third state. Skipped tests are:
- Technical debt pretending to be documentation
- Broken code that someone gave up on
- False confidence in test coverage metrics

**If a test can't run:**
- Fix the environment/dependencies so it can run
- Fix the code so the test passes
- Delete the test if it's testing something that doesn't exist

**NEVER commit a skipped test.** Either make it pass or delete it.

---

## PHASE 1: Contract-First Analysis (DO THIS FIRST)

**NEVER write tests by reading implementation.** That's how you write tests that mirror what code does instead of what it should do.

### Protocol: Analyze Contract Without Reading Implementation

**Step 1: Read ONLY the module's public interface**
```python
# Read THIS (public interface)
class ReminderTool:
    def run(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute reminder operations."""
        pass

# DO NOT read implementation details
# DO NOT look at internal methods
# DO NOT read how it's implemented
```

**Step 2: Document the contract**

Before writing any test, answer these questions in writing:

```
MODULE CONTRACT ANALYSIS
========================

1. What is this module's PURPOSE?
   - What problem does it solve?
   - Why does it exist?

2. What GUARANTEES does it provide?
   - What promises does the API make?
   - What invariants must hold?
   - What post-conditions are guaranteed?

3. What should SUCCEED?
   - Valid inputs
   - Happy path scenarios
   - Boundary cases that should work

4. What should FAIL?
   - Invalid inputs
   - Boundary conditions that should error
   - Security violations
   - Resource constraints

5. What are the DEPENDENCIES?
   - What does this module depend on?
   - Are there too many dependencies?
   - Could this be simpler?

6. ARCHITECTURAL CONCERNS:
   - Is this module doing too much?
   - Is it papering over design failures elsewhere?
   - Does the contract make sense or is it convoluted?
   - Should this module even exist?
```

**Step 3: Design test cases from contract**

Based on contract analysis (NOT implementation):
- List positive test cases (what should work)
- List negative test cases (what should fail)
- List boundary conditions
- List security concerns
- List performance concerns

**See "CANONICAL EXAMPLE" section below for complete contract analysis walkthrough.**

---

## PHASE 1.5: Contract Verification (VALIDATE YOUR ASSUMPTIONS)

**CRITICAL**: Do NOT read the implementation file yourself. Use the contract-extractor agent as an abstraction barrier.

### Why This Phase Exists

You've formed expectations about the contract from the interface. Now verify those expectations against actual implementation WITHOUT seeing the implementation yourself. The agent reads the code and reports ONLY contract facts (not implementation details).

### Protocol: Invoke Agent → Compare → Identify Gaps

**Step 1: Invoke the contract-extractor agent**

```bash
# Use Task tool to invoke the agent
Task(
    subagent_type="contract-extractor",
    description="Extract contract from module",
    prompt="""Extract the contract from: path/to/module.py

Return:
- Public interface (methods, signatures, types)
- Actual return structures (dict keys, types)
- Exception contracts (what raises what, when)
- Edge cases handled
- Dependencies and architectural concerns"""
)
```

**Step 2: Compare your expectations against agent report**

Create a comparison:

```
EXPECTATION vs REALITY
======================

Expected return structure:
{
    "status": str,
    "results": list
}

Actual return structure (from agent):
{
    "status": str,
    "confidence": float,  # I MISSED THIS
    "results": list,
    "result_count": int   # I MISSED THIS
}

Expected exceptions:
- ValueError for empty query

Actual exceptions (from agent):
- ValueError for empty query ✓
- ValueError for negative max_results  # I MISSED THIS

Expected edge cases:
- Empty results returns []

Actual edge cases (from agent):
- Empty results returns status="low_confidence", confidence=0.0, results=[]
  # More nuanced than I expected
```

**Step 3: Identify discrepancies and their implications**

For each discrepancy, ask:
- Is the code **wrong** (doesn't match intended contract)?
- Is the contract **unclear** (missing documentation)?
- Did I **misunderstand** the requirements?
- Is this an **undocumented feature** (needs test)?

**Example Analysis**:
```
DISCREPANCY: Agent reports confidence field in return, I didn't expect it
IMPLICATION: This is part of the contract - add test to verify confidence in [0.0, 1.0]

DISCREPANCY: Agent reports ValueError for negative max_results, I didn't expect it
IMPLICATION: Good edge case handling - add negative test

DISCREPANCY: Agent reports 8 dependencies, I expected 3-4
IMPLICATION: ARCHITECTURAL CONCERN - too many deps, report to human
```

**Step 4: Update test plan based on verified contract**

Now you know:
- What the code actually returns (test these exact structures)
- What exceptions are actually raised (test these exact cases)
- What edge cases are actually handled (test these behaviors)
- What architectural problems exist (report these to human)

**Step 5: Design comprehensive test cases**

```python
# Based on VERIFIED contract (not assumptions):

# Positive tests
- test_search_returns_exact_structure  # Verify all keys agent reported
- test_search_confidence_in_valid_range  # Agent said 0.0-1.0
- test_search_respects_max_results  # Agent confirmed this guarantee

# Negative tests
- test_search_rejects_empty_query  # Agent confirmed ValueError
- test_search_rejects_negative_max_results  # Agent revealed this

# Edge cases
- test_search_empty_results_structure  # Agent showed exact structure
- test_search_with_no_user_data  # Based on RLS info from agent

# Architectural concerns
- Report to human: "Module has 8 dependencies - possible SRP violation"
```

**See "CANONICAL EXAMPLE" section below for complete agent invocation, comparison, and gap analysis walkthrough.**

### When to Read Implementation

**Only AFTER writing tests based on verified contract.** Then you can read implementation for context, debugging, or refactoring - but tests are already protecting the contract.

---

## PHASE 2: Fail-First Verification (PROVE TESTS CAN FAIL)

**A test that always passes proves nothing.** You must see it fail.

### Protocol: Write → Fail → Verify

**Step 1: Write test based on contract expectations**

Don't look at implementation. Write assertions based on what the contract says SHOULD happen.

```python
def test_search_returns_confidence_score(search_tool, authenticated_user):
    """Contract: search must return confidence score between 0.0 and 1.0"""
    user_id = authenticated_user["user_id"]
    set_current_user_id(user_id)

    # Based on contract, not implementation
    result = search_tool.run(
        operation="search",
        query="Python async patterns",
        max_results=5
    )

    # Contract expectations
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0
    assert "results" in result
    assert len(result["results"]) <= 5
```

**Step 2: Run the test - expect failure or question success**

```bash
pytest tests/test_search_tool.py::test_search_returns_confidence_score -v
```

**If test FAILS:**
- Is this the expected failure? (No data exists yet)
- Is the failure message clear?
- Is this exposing a bug in the code?
- Is this exposing a problem with the contract?

**If test PASSES immediately:**
- Is the code actually correct?
- Are my assertions too weak?
- Am I testing a trivial case?
- Did I set up test data somewhere I forgot about?

**Step 3: Verify the test can actually catch bugs**

Temporarily break the code and verify the test fails:
```python
# In the actual implementation, temporarily break it:
def run(self, operation, **kwargs):
    return {"confidence": 2.5}  # INTENTIONAL BUG: exceeds 1.0
```

Run test - it should fail. If it doesn't, your assertions are too weak.

**Step 4: Remove the intentional bug, test should pass**

Now you have confidence the test actually works.

---

## Common Testing Anti-Patterns

**When writing tests, surface design problems - don't paper over them.**

| Anti-Pattern | Why It's Wrong | What To Do Instead |
|--------------|----------------|-------------------|
| **Mocking** | Tests mocks, not code. Hides integration issues. | Use real services (sqlite_test_db, test_db). If hard to test, fix design. |
| **Reading implementation first** | Tests mirror HOW instead of WHAT. Confirms current behavior, doesn't catch regressions. | Analyze contract WITHOUT reading code. Use contract-extractor agent. |
| **Tests that mirror implementation** | Testing that method calls BM25 then embeddings (HOW) vs testing returns relevant results (WHAT). | Test observable contract behavior, not internal paths. |
| **Weak assertions** | `assert result is not None` says nothing. | Precise: `assert 0.0 <= result["confidence"] <= 1.0` |
| **Only happy paths** | Missing adversarial cases means bugs slip through. | Test failure cases: empty inputs, invalid values, boundary conditions. |
| **Missing negative tests** | Only testing what should succeed. | Test what should FAIL with pytest.raises and match= |
| **Testing private methods** | `tool._internal()` means public interface insufficient. | Report: "Public interface doesn't expose needed contract." |
| **Papering over design problems** | Mocking 8 dependencies instead of reporting. | Report: "Module has 8 dependencies - violates SRP." |
| **Complex test setup** | Need 5 fixtures for one test = tight coupling. | Report: "Module too coupled - consider interface segregation." |
| **Unclear contract** | Can't answer "what SHOULD this return?" | Report: "Contract doesn't specify behavior for None values." |
| **Module papering over upstream failures** | Tool validates/fixes data from another module. | Report: "Fix upstream module, don't compensate downstream." |

**When you find architectural red flags, report them:**

```
ARCHITECTURAL CONCERN: ToolName

PROBLEM: [Specific issue]
EVIDENCE: [What you observed]
IMPACT: [Why this matters]
RECOMMENDATION: [Specific fix]
```

---

## Core Principle: NEVER MOCK

MIRA's testing philosophy: **NEVER MOCK.** Use actual services, real databases, real APIs.

This is a hard rule because mocking is where I slip. The test will seem "hard" without mocks and I'll think "just this once..." DON'T.

### Why No Mocking?

**Mocks test mocks, not code:**
```python
# This tests nothing about real behavior:
@mock.patch('tool.database')
def test_reminder_tool(mock_db):
    mock_db.query.return_value = [{"id": 1, "title": "Test"}]
    result = tool.get_reminders()
    # You have NO IDEA if real code works
```

**Real tests catch real bugs:**
```python
# This will fail if database schema changes:
def test_reminder_tool(sqlite_test_db):
    tool = ReminderTool()
    tool.run("add_reminder", title="Test", date="2025-01-01")

    # Real database query
    rows = sqlite_test_db.execute("SELECT * FROM reminders WHERE title = ?", ("Test",))
    assert len(rows) == 1
```

**If it's hard to test without mocks, the design is wrong.** Fix the design, don't mock it away.

---

## MIRA Test Infrastructure

### 🚨 USE authenticated_user - IT'S FULLY SET UP

**The `authenticated_user` fixture gives you EVERYTHING you need:**

```python
def test_anything(authenticated_user):
    # These are ALL set up and ready:
    user_id = authenticated_user["user_id"]           # Test user ID
    continuum_id = authenticated_user["continuum_id"] # Test user's continuum (ALREADY EXISTS)
    email = authenticated_user["email"]               # test@example.com
    token = authenticated_user["access_token"]        # Valid session token

    # User context is ALREADY SET - just use user_id
    # Continuum ALREADY EXISTS - just add messages to it
    # Cleanup happens AUTOMATICALLY - no manual teardown needed
```

**What `authenticated_user` does for you:**
1. ✅ Creates test user (if doesn't exist)
2. ✅ Creates test user's continuum (if doesn't exist)
3. ✅ Sets user context for RLS
4. ✅ Creates valid session token
5. ✅ Cleans up all test data before/after each test
6. ✅ Preserves user record for reuse

**How to use it (SIMPLE):**

```python
# ✅ CORRECT - Just use the continuum_id that's already there
def test_add_messages(authenticated_user, test_db):
    user_id = authenticated_user["user_id"]
    continuum_id = authenticated_user["continuum_id"]  # Use this!
    set_current_user_id(user_id)  # Set context

    repo = get_continuum_repository()
    msg = Message(role="user", content="Test message")
    repo.save_message(msg, continuum_id, user_id)  # Just save directly

    # Message is in the database, ready to test

# ❌ WRONG - Don't create new continuums (test user already has one)
def test_add_messages_wrong(authenticated_user):
    user_id = authenticated_user["user_id"]
    repo = get_continuum_repository()
    continuum = repo.create_continuum(user_id)  # DON'T DO THIS!
    # This creates a SECOND continuum - user should only have ONE
```

**Common Patterns:**

```python
# Most common: Just add messages to test user's continuum
def test_tool(authenticated_user):
    user_id = authenticated_user["user_id"]
    continuum_id = authenticated_user["continuum_id"]
    set_current_user_id(user_id)

    # Add test data
    repo = get_continuum_repository()
    msg = Message(role="user", content="Test")
    repo.save_message(msg, continuum_id, user_id)

    # Test your code
    result = tool.run("search", query="Test")
    assert result["status"] == "success"

# API testing: authenticated_client has headers pre-set
def test_api(authenticated_client):
    response = authenticated_client.get("/v0/api/endpoint")
    assert response.status_code == 200
```

**Test User Constants (for reference):**
```python
TEST_USER_EMAIL = "test@example.com"
SECOND_TEST_USER_EMAIL = "test2@example.com"
# User IDs vary, always use authenticated_user["user_id"]
```

### 🔒 Using second_authenticated_user for RLS Testing

**The `second_authenticated_user` fixture provides a SECOND fully-configured test user:**

When you need to verify Row-Level Security (RLS) or multi-user scenarios, use both fixtures together:

```python
def test_user_isolation(authenticated_user, second_authenticated_user):
    """Verify RLS prevents cross-user data access."""
    user1_id = authenticated_user["user_id"]
    user1_continuum_id = authenticated_user["continuum_id"]

    user2_id = second_authenticated_user["user_id"]
    user2_continuum_id = second_authenticated_user["continuum_id"]

    # User 1 creates private data
    set_current_user_id(user1_id)
    repo = get_continuum_repository()
    msg1 = Message(role="user", content="User 1 secret data")
    repo.save_message(msg1, user1_continuum_id, user1_id)

    # User 2 tries to access User 1's data
    set_current_user_id(user2_id)
    result = search_tool.run("search", query="secret", max_results=10)

    # Verify User 2 cannot see User 1's data
    assert len(result["results"]) == 0, "RLS violation: User 2 can see User 1's data"
```

**Both fixtures provide identical structure:**
```python
authenticated_user = {
    "user_id": str,           # First test user ID
    "continuum_id": str,      # First test user's continuum
    "email": str,             # test@example.com
    "access_token": str       # Valid session token
}

second_authenticated_user = {
    "user_id": str,           # Second test user ID (different UUID)
    "continuum_id": str,      # Second test user's continuum (different UUID)
    "email": str,             # test2@example.com
    "access_token": str       # Valid session token
}
```

**When to use second_authenticated_user:**
- Testing RLS isolation between users
- Verifying user-specific queries filter correctly
- Testing collaborative features (if MIRA adds them)
- Confirming data leakage prevention
- Any scenario requiring multiple distinct users

**Cleanup is automatic for both users:**
- Both users' data cleaned before/after each test
- Both user records preserved for reuse
- No manual cleanup needed

**SQLite for Tool Testing:**
```python
@pytest.mark.schema_files(['tools/implementations/reminder_tool_schema.sql'])
def test_reminder_tool(sqlite_test_db):
    tool = ReminderTool()
    tool.run("add_reminder", title="Test", date="2025-01-01")

    rows = sqlite_test_db.execute("SELECT * FROM reminders WHERE title = ?", ("Test",))
    assert len(rows) == 1
```

**Automatic Cleanup:**
- `cleanup_test_user_data()` runs after each test (autouse)
- Deletes user's data, preserves user account for reuse
- No manual teardown needed

### Test Organization - Mirror the Codebase

Test files MUST mirror the codebase directory structure:

```
codebase:                          tests:
clients/                           tests/clients/
  llm_provider.py           →        test_llm_provider.py
cns/                               tests/cns/
  core/                              core/
    conversation.py         →          test_conversation.py
  services/                          services/
    orchestrator.py         →          test_orchestrator.py
tools/                             tests/tools/
  implementations/                   implementations/
    reminder_tool.py        →          test_reminder_tool.py
```

**Class-Based Organization:**
```python
class TestReminderToolBasics:
    """Core functionality - contract enforcement."""

    def test_add_reminder_creates_with_exact_fields(self):
        # Test contract: what fields are guaranteed
        pass

class TestReminderToolEdgeCases:
    """Boundary conditions and error cases."""

    def test_add_reminder_rejects_invalid_date(self):
        # Test contract: what should fail
        pass

class TestReminderToolSecurity:
    """User isolation and security guarantees."""

    def test_user_cannot_access_other_users_reminders(self):
        # Test contract: RLS isolation
        pass
```

---

## Assertion Patterns

### Database Assertions
```python
# Verify exact row exists with exact values
row = test_db.execute_single("SELECT * FROM reminders WHERE id = ?", (id,))
assert row["title"] == "Expected title"
assert row["user_id"] == test_user_id
assert row["created_at"] is not None

# Verify count of results
rows = test_db.execute("SELECT * FROM continuums WHERE user_id = ?", (user_id,))
assert len(rows) == 3
```

### API Response Assertions
```python
# Verify structure and exact values
assert result["status"] == "success"
assert result["data"]["id"] is not None
assert isinstance(result["data"]["id"], str)
assert result["message"] == "Created successfully"

# Verify arrays with exact properties
assert len(result["items"]) == 5
assert all(item["created_at"] is not None for item in result["items"])
assert all(isinstance(item["id"], str) for item in result["items"])
```

### Exception Assertions
```python
# Test error cases with exact messages
with pytest.raises(ValueError, match="Query cannot be empty"):
    search_tool.run(operation="search", query="")

with pytest.raises(ValueError, match="Priority must be 0 \\(normal\\), 1 \\(high\\), or 2 \\(urgent\\)"):
    tool.run("send_message", priority=5)
```

---

## Quick Checklist (Use Before Committing Tests)

**Contract Analysis:**
- [ ] Did I analyze the contract WITHOUT reading implementation?
- [ ] Have I documented: purpose, guarantees, success cases, failure cases?
- [ ] Did I identify any architectural red flags in my analysis?

**Contract Verification:**
- [ ] Did I invoke the contract-extractor agent (NOT read implementation myself)?
- [ ] Did I compare my contract expectations against the agent's report?
- [ ] Did I identify discrepancies (missing fields, unexpected exceptions, edge cases)?
- [ ] Did I update my test plan based on verified contract?
- [ ] Did I report any architectural concerns the agent identified?

**Fail-First Verification:**
- [ ] Did I write tests based on VERIFIED contract (from agent)?
- [ ] Did I run tests and verify they can fail?
- [ ] Did I temporarily break code to prove tests catch bugs?

**Test Quality:**
- [ ] Are assertions checking EXACT values, not just existence?
- [ ] Have I tested both success AND failure cases?
- [ ] Are error messages checked with `match=...`?
- [ ] Does this test enforce a contract guarantee?
- [ ] Did I test all exceptions the agent reported?
- [ ] Did I test all edge cases the agent revealed?

**MIRA Standards:**
- [ ] Am I using real services/database (NO MOCKS)?
- [ ] Did I use appropriate fixture (`test_db`, `sqlite_test_db`, etc)?
- [ ] Is user isolation correct (RLS context set)?
- [ ] Does test file mirror codebase directory structure?

**Final Question:**
- [ ] If this test passes, am I confident the contract is enforced?
- [ ] Will this test catch a regression if someone breaks the code?
- [ ] Did I read implementation ONLY AFTER writing tests?

**If you answer NO to any of these, the test is not ready.**

---

## CANONICAL EXAMPLE: Contract-First Testing

**This comprehensive example demonstrates the complete workflow from contract analysis through validation. Reference this example when applying any phase.**

### Step 1: Contract Analysis (No Implementation Reading)

```
MODULE: ConversationSearchTool
INTERFACE: run(operation: str, **kwargs) -> Dict[str, Any]

CONTRACT ANALYSIS:
==================

PURPOSE:
- Search user's conversation history semantically
- Return relevant messages with context
- Provide confidence scoring

GUARANTEES:
- User isolation (RLS): only searches current user's data
- Returns max_results items or fewer
- Confidence score in [0.0, 1.0]
- Results sorted by relevance (highest first)

SUCCESS CASES:
- Search with valid query → returns results or empty list
- Search with entities list → filters by entities
- Expand message with valid ID → returns message + context

FAILURE CASES:
- Empty query string → ValueError
- Invalid message_id format → ValueError
- Negative max_results → ValueError

ARCHITECTURAL NOTES:
- Clean separation from orchestrator
- No obvious design issues
- RLS handles user isolation at DB level (good)
```

### Step 2: Design Test Cases

```python
# Positive tests (from contract)
- test_search_returns_results_with_confidence_score
- test_search_respects_max_results_limit
- test_search_with_entities_filters_correctly
- test_search_returns_empty_when_no_matches
- test_expand_message_returns_context

# Negative tests (from contract)
- test_search_rejects_empty_query
- test_expand_rejects_invalid_message_id
- test_search_rejects_negative_max_results

# Security tests (from contract)
- test_search_respects_user_isolation
```

### Step 3: Write Fail-First Tests

```python
class TestConversationSearchContract:
    """Tests enforce ConversationSearchTool's contract guarantees."""

    def test_search_returns_confidence_in_valid_range(self, search_tool, authenticated_user):
        """CONTRACT: confidence must be float in [0.0, 1.0]"""
        user_id = authenticated_user["user_id"]
        set_current_user_id(user_id)

        result = search_tool.run("search", query="test query", max_results=5)

        # Contract guarantees
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
        assert 0.0 <= result["confidence"] <= 1.0

    def test_search_respects_max_results_limit(self, search_tool, authenticated_user):
        """CONTRACT: must return at most max_results items"""
        user_id = authenticated_user["user_id"]
        set_current_user_id(user_id)

        # Create 10 messages
        repo = get_continuum_repository()
        conv = repo.create_continuum(user_id)
        for i in range(10):
            conv.save_message(Message(content=f"Message {i}", role="user"))

        # Request only 3
        result = search_tool.run("search", query="Message", max_results=3)

        # Contract: must not exceed max_results
        assert len(result["results"]) <= 3

    def test_search_rejects_empty_query(self, search_tool, authenticated_user):
        """CONTRACT: empty query must raise ValueError"""
        user_id = authenticated_user["user_id"]
        set_current_user_id(user_id)

        with pytest.raises(ValueError, match="Query cannot be empty"):
            search_tool.run("search", query="", max_results=5)

    def test_search_isolates_users(self, search_tool, authenticated_user, second_authenticated_user):
        """CONTRACT: RLS ensures user isolation"""
        user1_id = authenticated_user["user_id"]
        user1_continuum_id = authenticated_user["continuum_id"]

        user2_id = second_authenticated_user["user_id"]

        # User 1 creates message
        set_current_user_id(user1_id)
        repo = get_continuum_repository()
        msg = Message(content="User 1 secret data", role="user")
        repo.save_message(msg, user1_continuum_id, user1_id)

        # User 2 searches (should not see User 1's data)
        set_current_user_id(user2_id)
        result = search_tool.run("search", query="secret", max_results=10)

        # Contract: User 2 cannot see User 1's data
        assert len(result["results"]) == 0, "RLS violation: User 2 can see User 1's data"
```

### Step 4: Run and Verify

```bash
# Run tests - verify they can fail
pytest tests/tools/test_conversation_search.py -v

# If any test passes unexpectedly, investigate:
# - Is the code actually correct?
# - Are my assertions too weak?
# - Did I misunderstand the contract?
```

---

## Final Reality Check

**A test that always passes is worse than no test** - it provides false confidence.

Good tests are:
- **Based on contracts** - test what SHOULD happen, not what DOES happen
- **Adversarial** - test failure cases, boundaries, security
- **Precise** - exact assertions on exact values
- **Real** - no mocks, use actual services
- **Design-aware** - surface architectural problems

**Before committing any test, ask:**
1. Did I analyze the contract first, without reading implementation?
2. Did I invoke the contract-extractor agent to verify my assumptions?
3. Did I write tests based on the verified contract (not implementation)?
4. Will this test fail if someone breaks the contract?
5. Did I see this test fail, then verify it passes correctly?
6. Does this test enforce a real guarantee?

If NO to any of these → the test is not ready.

---

# VALIDATION MODE: Complete Module Validation

## 🚨 CRITICAL: VALIDATION WORKFLOW RESTRICTIONS

**During validation, you may ONLY edit test files.**

**ALLOWED**:
- Read implementation file
- Edit test files to fix coverage/quality issues
- Add new tests
- Strengthen assertions
- Improve test organization

**FORBIDDEN**:
- Edit implementation file
- Fix bugs in module code
- Refactor implementation
- Modify module behavior

**If validation reveals bugs in implementation:**
1. Report them to the user
2. Note in validation output: "Implementation issue requires human review"
3. DO NOT fix implementation yourself
4. Validation tests the code AS-IS

---

## Two-Agent Validation System

After writing a module and tests, validate them using the two-agent validation system:

1. **contract-extractor**: Extracts contracts from module (read-only)
2. **test-validator**: Validates tests against contracts (reports only)

This provides binary verdict: **✓ VALIDATED** or **✗ BLOCKED** with specific issues.

---

## When to Use Validation Mode

**GUIDE MODE** (pre-tests):
- You have a module but no tests yet
- Use contract-extractor to understand what to test
- Write tests based on extracted contracts
- Then proceed to VALIDATION MODE

**VALIDATION MODE** (post-tests):
- Module and tests both exist
- Want to verify tests are complete and high quality
- Need production readiness confirmation
- Get binary go/no-go decision

---

## Validation Protocol

### Step 1: Extract Contracts

Invoke contract-extractor agent to analyze the module:

```python
# Use Task tool to invoke contract-extractor
contract_report = await Task(
    subagent_type="contract-extractor",
    description="Extract module contracts",
    prompt=f"""Extract the complete contract from module: {module_path}

Provide:
- Public interface (methods, signatures, types)
- Actual return structures (exact dict keys, types, constraints)
- Exception contracts (what raises what, when)
- Edge cases handled
- Dependencies and architectural concerns
- VALIDATION CHECKLIST with numbered requirements

Module path: {module_path}"""
)
```

**Review the contract report:**
- Verify it extracted all public methods
- Check the validation checklist
- Note any architectural concerns

### Step 2: Validate Tests

Invoke test-validator agent with contracts + test file:

```python
# Use Task tool to invoke test-validator
validation_report = await Task(
    subagent_type="test-validator",
    description="Validate tests against contracts",
    prompt=f"""Validate tests against extracted contracts:

MODULE: {module_path}
TESTS: {test_path}

CONTRACT REPORT:
{contract_report}

Verify:
1. Contract Coverage - do tests cover all requirements from checklist?
2. Test Quality - are assertions strong? negative tests present?
3. Architecture - are design concerns acceptable?

Provide binary verdict: ✓ VALIDATED or ✗ BLOCKED
List specific issues if blocked."""
)
```

**Review the validation report:**
- Check the verdict: VALIDATED or BLOCKED
- If BLOCKED: read the blocking issues list
- If VALIDATED: module is production-ready

### Step 3: Handle Results

**If ✓ VALIDATED:**
```python
print(f"✅ MODULE VALIDATED: {module_path}")
print("- All contracts tested")
print("- Test quality verified")
print("- Architecture sound")
print("- Ready for production")
```

**If ✗ BLOCKED:**
```python
print(f"❌ VALIDATION BLOCKED: {module_path}")
print("\nBLOCKING ISSUES:")
for issue in blocking_issues:
    print(f"  - {issue}")
print("\nACTION: Fix issues and re-validate")
```

**For complete validation example with checklist and report format, see test-validator.md output format section.**

---

## Validation Criteria

**See test-validator.md for complete VALIDATED/BLOCKED decision logic and thresholds.**

---

## Integration with Slash Command

Use `/validate-module` for easy invocation:

```bash
/validate-module tools/implementations/reminder_tool.py

# Agent orchestrates:
# 1. Extracts contracts
# 2. Validates tests
# 3. Reports verdict
# 4. Lists issues if blocked
```

---

## Validation Workflow Summary

```
┌─────────────────────────┐
│ Module + Tests Written  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  contract-extractor     │◄── Extracts contracts
│  Agent Invoked          │    Returns validation checklist
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  test-validator         │◄── Validates against checklist
│  Agent Invoked          │    Checks quality + architecture
└────────────┬────────────┘
             │
             ▼
        ┌────┴────┐
        │ Verdict │
        └────┬────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│VALIDATED │  │ BLOCKED  │
│    ✓     │  │    ✗     │
└────┬─────┘  └────┬─────┘
     │             │
     ▼             ▼
 Production    Fix Issues
  Ready        Re-validate
```

---

## Best Practices

**1. Run validation before committing**
- Catch issues early
- Ensure quality gate before merge

**2. Fix all blocking issues**
- Don't ignore validation failures
- Each issue weakens test suite

**3. Address warnings when feasible**
- Non-blocking but indicate areas for improvement
- Good tests → great tests

**4. Re-run after fixes**
- Verify fixes resolved issues
- Catch any new problems introduced

**5. Use validation as learning**
- Study what validator caught
- Improve future test-writing

---

## Validation Output Interpretation

**✓ VALIDATED = Production Ready**
- All contracts tested
- Test quality verified
- Architecture acceptable
- Module can be deployed with confidence

**✗ BLOCKED = Must Fix**
- Specific issues listed
- Each issue is actionable
- Re-validate after fixes

**⚠ WARNINGS = Should Address**
- Non-blocking concerns
- Areas for improvement
- Consider addressing before production

---

## End-to-End Confidence

The two-agent validation system provides confidence that:

1. **Tests are complete** - all contracts covered
2. **Tests are strong** - precise assertions, negative cases
3. **Architecture is sound** - reasonable dependencies, clear purpose
4. **Module is ready** - production deployment confidence

**Use this system to validate every module before considering it "done".**
