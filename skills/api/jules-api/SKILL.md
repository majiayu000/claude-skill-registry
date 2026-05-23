---
name: jules-api
description: "Programmatic interface to Google's Jules API for asynchronous coding task delegation. Use when creating Jules sessions, monitoring async work, or integrating code reviews/refactoring/tests into workflows. Not for synchronous coding tasks or when immediate execution is required."
---

# Jules API Integration

<mission_control>
<objective>Delegate asynchronous coding tasks to Jules (Google's AI coding agent) for maximum efficiency. Claude creates sessions, monitors progress, and retrieves outputs while user continues other work.</objective>
<success_criteria>Jules session created with proper TDD prompt, session ID returned to user, async workflow established</success_criteria>
</mission_control>

<trigger>When user mentions code review, refactoring, adding tests, bug fixes, or when code is pushed to remote branch</trigger>

> **API Status**: Alpha (v1alpha) - specifications may stabilize

---

## Overview

Jules API enables asynchronous coding task delegation:

- Create sessions with prompts (repo-based or repoless)
- Monitor progress through state transitions
- Retrieve outputs (PRs, artifacts, files)
- Approve plans or provide feedback interactively

---

## Delegation Philosophy

**KEY PRINCIPLE**: Use Jules for async tasks to free Claude for strategic work.

### When to Delegate

Claude should proactively suggest Jules for:

| Task          | Example                                                  |
| ------------- | -------------------------------------------------------- |
| Code Reviews  | "Review authentication changes in feature/auth"          |
| Refactoring   | "Refactor parser to use Polars for 10x performance"      |
| Adding Tests  | "Add comprehensive tests for payment module"             |
| Bug Fixes     | "Fix timezone bug (commit abc123) with regression tests" |
| Documentation | "Update API docs for new endpoints"                      |
| Maintenance   | Weekly dependency updates, nightly linting               |

### Effective Delegation Patterns

**Pattern 1: Implement → Review**

1. Claude implements feature
2. Push branch to remote
3. Create Jules session: "Review and improve feature X"
4. Jules creates PR with improvements
5. Claude integrates feedback

**Pattern 2: Test Generation**

1. Claude implements feature
2. Create Jules session: "Add comprehensive tests for module X"
3. Jules generates test suite
4. Merge when tests pass

**Pattern 3: Bug Fix**

1. Investigate and identify root cause
2. Create Jules session with reproduction steps
3. Jules fixes and adds regression tests

**Pattern 4: Repoless Prototype**

1. Create session without sourceContext
2. Jules creates code in ephemeral environment
3. Download and integrate results

### Claude's Role in Delegation

When delegating to Jules, Claude should:

1. **Prepare the context** - Ensure branch is pushed and up-to-date
2. **Write clear prompts** - Specific, actionable instructions with TDD
3. **Create the session** - Use direct API calls
4. **Return session info** - Give user the session ID and URL
5. **Suggest next steps** - Explain what Jules will do and when to check back

**Example dialogue**:

```
User: "Can you review my authentication changes?"

Claude: "I'll create a Jules session to review your authentication code.
         Jules works asynchronously and will create a PR with feedback.

         Session ID: 123456789
         URL: https://jules.google.com/session/123456789

         Jules typically completes tasks in ~10 minutes.
         You can continue other work while Jules reviews."
```

---

## TDD Requirement (Critical)

**IMPORTANT**: Always instruct Jules to use Test-Driven Development.

### Why TDD with Jules

- Ensures correctness before implementation
- Creates behavior-relevant tests (not implementation tests)
- Prevents regressions and edge cases
- Provides clear acceptance criteria
- Makes code more maintainable and documented

### What Are Behavior-Relevant Tests

Behavior-relevant tests validate **what** the code does, not **how** it does it.

**Good behavior-relevant tests**:

- Test from user/caller perspective
- Validate actual business requirements
- Cover edge cases and error conditions
- Remain stable when implementation changes

**Bad implementation tests**:

- Test private methods directly
- Mock internal implementation details
- Break on refactoring
- Test "how" rather than "what"

### TDD Instruction Template

Include this in every Jules prompt:

```
Use Test-Driven Development (TDD) approach:
1. Write behavior-relevant tests first (expected behavior, edge cases, error conditions)
2. Run tests to confirm they fail (red phase)
3. Implement minimal code to make tests pass (green phase)
4. Refactor while keeping tests passing (refactor phase)
5. Ensure all tests have meaningful assertions that validate actual behavior
```

### Example Prompts with TDD

**Feature implementation**:

```
Add user authentication to the API.

Use TDD approach:
1. Write tests for: successful login, invalid credentials, token expiration, rate limiting
2. Implement authentication logic to pass tests
3. Refactor for security best practices

Tests should validate actual behavior, not implementation details.
```

**Refactoring**:

```
Refactor the parser to use Polars instead of Pandas.

Use TDD approach:
1. Write behavior tests that validate current parser output
2. Refactor to use Polars while keeping tests green
3. Add performance benchmarks as tests

Focus on behavior: input -> output validation, not internal implementation.
```

---

## Base Configuration

```
Base URL: https://jules.googleapis.com
API Version: v1alpha
Authentication: X-Goog-Api-Key header
```

### Session States

| State                    | Meaning                    |
| ------------------------ | -------------------------- |
| `QUEUED`                 | Awaiting processing        |
| `PLANNING`               | Agent developing strategy  |
| `AWAITING_PLAN_APPROVAL` | Requires user confirmation |
| `AWAITING_USER_FEEDBACK` | Needs additional input     |
| `IN_PROGRESS`            | Actively executing         |
| `COMPLETED`              | Successfully finished      |
| `FAILED`                 | Execution unsuccessful     |

**IMPORTANT**: Always use `"automationMode": "AUTO_CREATE_PR"` for automatic PR creation.

---

## Authentication

1. Get API key: https://jules.google.com/settings#api
2. Set environment variable:

```bash
export JULES_API_KEY="your-api-key-here"
```

**Security**: Never commit API keys to version control.

---

## Quick Start

**Create session (with repository)**:

```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for authentication module using TDD approach",
    "sourceContext": {
      "source": "sources/github/myorg/myrepo",
      "githubRepoContext": {"startingBranch": "main"}
    },
    "automationMode": "AUTO_CREATE_PR"
  }'
```

**Create session (repoless)**:

```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a Python CLI that fetches weather data",
    "title": "Weather CLI Prototype"
  }'
```

**Check status**:

```bash
curl https://jules.googleapis.com/v1alpha/sessions/SESSION_ID \
  -H "X-Goog-Api-Key: $JULES_API_KEY"
```

---

## Proactive Delegation Triggers

Claude should automatically suggest Jules delegation when:

- User pushes a branch and asks "what do you think?"
- User says "add tests", "improve tests", or "review"
- User mentions "refactor" or "optimize"
- Feature is complete and needs polish
- User reports a well-defined bug
- Documentation needs updating
- Recurring maintenance tasks mentioned

**Example proactive response**:

```
User: "Just pushed the new API endpoint to feature/api-v2"

Claude: "Great! Would you like me to create a Jules session to review it?
         Jules can check for edge cases, add tests, and optimize while you
         continue working on other features. Sessions typically complete
         in ~10 minutes."
```

---

## Best Practices

1. **Use Descriptive Prompts**: Specific, actionable instructions
2. **Monitor State**: Poll session status to track progress
3. **Enable Plan Approval**: Set `requirePlanApproval: true` for sensitive operations
4. **Handle States**: Respond to AWAITING_USER_FEEDBACK and AWAITING_PLAN_APPROVAL
5. **Check Outputs**: Review outputs array for PRs and artifacts
6. **Use Pagination**: Handle nextPageToken for large result sets
7. **Enable Environment Variables**: Set `environmentVariablesEnabled: true` for credentials
8. **Use Repoless for Prototypes**: Quick experiments don't need a repository

---

## Jules PR Comment Resume Feature

**IMPORTANT**: Jules monitors PRs and automatically resumes sessions when you comment!

**How it works**:

1. Jules creates PR #466
2. Session completes (state: `COMPLETED`)
3. You comment on PR: "Wrong SDK used (google.generativeai vs google.genai)"
4. **Jules AUTOMATICALLY resumes session**
5. State changes: `COMPLETED` → `AWAITING_PLAN_APPROVAL`
6. Jules generates new plan to address your feedback
7. You approve the plan
8. Jules fixes issues and updates PR

**Best practices**:

- **DO**: Comment on PRs with specific, actionable feedback
- **DO**: Check if session auto-resumed before creating duplicate
- **DO**: Approve Jules' new plan if it looks good
- **DO**: Use detailed comments - Jules understands context
- **DON'T**: Create new session if existing one can resume
- **DON'T**: Use vague comments like "fix this"

This creates a powerful iteration loop.

---

## Timing Considerations

**Jules session duration**:

- Typical: ~10 minutes
- Simple tasks: 5-10 minutes
- Complex tasks: 15-30 minutes
- Large refactors: 30+ minutes

**Workflow optimization**:

- Create Jules session immediately when delegation is appropriate
- Continue other work while Jules executes (don't wait synchronously)
- Check session status after ~10 minutes
- Use this time for strategic planning or other tasks

---

## Usage Philosophy

**IMPORTANT**: This skill prioritizes **direct API usage** via HTTP calls (curl, httpx, requests) rather than relying on custom Python scripts. This ensures:

- **Language-agnostic** (works with any language/environment)
- **Portable** (no dependency on jules_client.py)
- **Transparent** (clear what API calls are being made)
- **Maintainable** (follows API documentation directly)

**When using this skill**:

1. **Primary**: Use direct HTTP calls (curl in bash, httpx/requests in Python)
2. **Secondary**: Use jules_client.py only as a convenience for complex workflows

---

## Tools

### Feed Feedback (CI/Reviews)

This skill includes a script `feed_feedback.py` designed to run in a scheduled workflow. It enables Jules to receive feedback from CI failures and code reviews on its own Pull Requests.

**Purpose**: Closes the feedback loop by reporting CI errors and review comments back to the active Jules session so it can interactively fix issues.

**Usage**:

```bash
# Run locally (requires JULES_API_KEY and GITHUB_TOKEN)
python .claude/skills/jules-api/feed_feedback.py

# Run for a specific bot author (default: jules-bot)
python .claude/skills/jules-api/feed_feedback.py --author my-bot-name
```

**How it works**:

1. Scans for open PRs by `jules-bot`
2. Checks CI status (failed) and Reviews (changes requested)
3. Extracts the Jules Session ID from the branch name or PR body
4. Sends a prompt to the session with error logs and feedback
5. Posts a comment on the PR to prevent spamming the same feedback

---

## Navigation

**External Documentation**:

- Official API → https://developers.google.com/jules/api/reference/rest
- Changelog → https://jules.google.com/docs/changelog/
- Jules Blog → https://blog.google/technology/google-labs/jules-tools-jules-api/

**Local References**:

| If you need...                        | Read...                                             |
| ------------------------------------- | --------------------------------------------------- |
| Complete API documentation, endpoints | [api-reference.md](references/api-reference.md)     |
| Working Python/Bash code examples     | [code-examples.md](references/code-examples.md)     |
| Debugging stuck sessions              | [troubleshooting.md](references/troubleshooting.md) |

---

## Genetic Code (Portability Invariant)

This skill bundles its philosophy for zero-dependency operation:

- **TDD First**: Tests before implementation (ensures correctness)
- **Async Delegation**: Jules for tactical work, Claude for strategic
- **Direct API**: HTTP calls preferred over scripts (portability, transparency)
- **AUTO_CREATE_PR**: Always enable for automated workflows
- **PR Comment Resume**: Jules auto-resumes when you comment on PRs

These principles enable effective async delegation without requiring external rules or context.

---

## Critical Constraints

<critical_constraint>
MANDATORY: Always include TDD instructions in Jules prompts
MANDATORY: Use "automationMode": "AUTO_CREATE_PR" for all sessions
MANDATORY: Prefer direct API calls (curl/httpx) over jules_client.py
MANDATORY: Check session state after ~10 minutes for typical completion
MANDATORY: Provide specific, actionable feedback when responding to Jules
MANDATORY: Use behavior-relevant test descriptions (not implementation tests)
No exceptions. TDD ensures correctness; AUTO_CREATE_PR enables workflows; direct API calls ensure portability.
</critical_constraint>
