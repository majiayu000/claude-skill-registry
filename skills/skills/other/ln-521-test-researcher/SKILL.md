---
name: ln-521-test-researcher
description: "Researches real-world problems, competitor solutions, and customer complaints before test planning. Posts findings as Linear comment for ln-522 and ln-523."
---

# Test Researcher

Researches real-world problems and edge cases before test planning to ensure tests cover actual user pain points, not just AC.

## Purpose & Scope
- Research common problems for the feature domain using Web Search, MCP Ref, Context7.
- Analyze how competitors solve the same problem.
- Find customer complaints and pain points from forums, StackOverflow, Reddit.
- Post structured findings as Linear comment for downstream skills (ln-522, ln-523).
- No test creation or status changes.

## When to Use

This skill should be used when:
- **Invoked by ln-520-test-planner** at start of test planning pipeline
- Story has non-trivial functionality (external APIs, file formats, authentication)
- Need to discover edge cases beyond AC

**Skip research when:**
- Story is trivial (simple CRUD, no external dependencies)
- Research comment already exists on Story
- User explicitly requests to skip

## Workflow

### Phase 1: Discovery

Auto-discover Team ID from `docs/tasks/kanban_board.md`.

**Input:** Story ID from orchestrator (ln-520)

### Phase 2: Extract Feature Domain

1) Fetch Story from Linear
2) Parse Story goal and AC to identify:
   - What technology/API/format is involved?
   - What is the user's goal? (e.g., "translate XLIFF files", "authenticate via OAuth")
3) Extract keywords for research queries

### Phase 3: Research Common Problems

Use available tools to find real-world problems:

1) **Web Search:**
   - "[feature] common problems"
   - "[format] edge cases"
   - "[API] gotchas"
   - "[technology] known issues"

2) **MCP Ref:**
   - `ref_search_documentation("[feature] error handling best practices")`
   - `ref_search_documentation("[format] validation rules")`

3) **Context7:**
   - Query relevant library docs for known issues
   - Check API documentation for limitations

### Phase 4: Research Competitor Solutions

1) **Web Search:**
   - "[competitor] [feature] how it works"
   - "[feature] comparison"
   - "[product type] best practices"

2) **Analysis:**
   - How do market leaders handle this functionality?
   - What UX patterns do they use?
   - What error handling approaches are common?

### Phase 5: Research Customer Complaints

1) **Web Search:**
   - "[feature] complaints"
   - "[product type] user problems"
   - "[format] issues reddit"
   - "[format] issues stackoverflow"

2) **Analysis:**
   - What do users actually struggle with?
   - What are common frustrations?
   - What gaps exist between user expectations and typical implementations?

### Phase 6: Compile and Post Findings

1) **Compile findings** into categories:
   - **Input validation issues** (malformed data, encoding, size limits)
   - **Edge cases** (empty input, special characters, Unicode)
   - **Error handling** (timeouts, rate limits, partial failures)
   - **Security concerns** (injection, authentication bypass)
   - **Competitor advantages** (features we should match or exceed)
   - **Customer pain points** (problems users actually complain about)

2) **Post Linear comment** on Story with research summary:

```markdown
## Test Research: {Feature}

### Sources Consulted
- [Source 1](url)
- [Source 2](url)

### Common Problems Found
1. **Problem 1:** Description + test case suggestion
2. **Problem 2:** Description + test case suggestion

### Competitor Analysis
- **Competitor A:** How they handle this + what we can learn
- **Competitor B:** Their approach + gaps we can exploit

### Customer Pain Points
- **Complaint 1:** What users struggle with + test to prevent
- **Complaint 2:** Common frustration + how to verify we solve it

### Recommended Test Coverage
- [ ] Test case for problem 1
- [ ] Test case for competitor parity
- [ ] Test case for customer pain point

---
_This research informs both manual tests (ln-522) and automated tests (ln-523)._
```

## Critical Rules

- **No test creation:** Only research and documentation.
- **No status changes:** Only Linear comment.
- **Source attribution:** Always include URLs for sources consulted.
- **Actionable findings:** Each problem should suggest a test case.
- **Skip trivial Stories:** Don't research "Add button to page".

## Definition of Done

- [ ] Feature domain extracted from Story (technology/API/format identified)
- [ ] Common problems researched (Web Search + MCP Ref + Context7)
- [ ] Competitor solutions analyzed (at least 1-2 competitors)
- [ ] Customer complaints found (forums, StackOverflow, Reddit)
- [ ] Findings compiled into categories
- [ ] Linear comment posted with "## Test Research: {Feature}" header
- [ ] At least 3 recommended test cases suggested

**Output:** Linear comment with research findings for ln-522 and ln-523 to use.

## Reference Files

- Research methodology: Web Search, MCP Ref, Context7 tools
- Comment format: Structured markdown with sources
- Downstream consumers: ln-522-manual-tester, ln-523-auto-test-planner

---

**Version:** 1.0.0
**Last Updated:** 2026-01-15
