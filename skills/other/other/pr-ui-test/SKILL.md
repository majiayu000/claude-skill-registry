---
name: pr-ui-test
description: >-
    Automated UI testing for pull requests using Playwright MCP and the gh CLI.
    ALWAYS invoke this skill when the user asks to test a PR's UI, run visual
    regression checks on a pull request, QA a frontend PR, verify UI changes,
    smoke-test a branch, or test edge cases for a PR. Also trigger when the user
    says "test this PR", "check the UI on this branch", "QA this", "run
    playwright on the PR", "review and test", or any variation of testing
    frontend/UI changes in a pull request context. Do NOT attempt to run
    Playwright or post PR comments directly — ALWAYS route through this skill
    first.
---

# PR UI Test

Automated UI testing for pull requests. Uses Playwright MCP to verify that UI
changes work correctly, generates and runs edge-case tests, then posts a
concise findings report as a PR comment via `gh`.

## Prerequisites

Before running, confirm the following are available:

1. **Playwright MCP** — connected and accessible (browser automation)
2. **`gh` CLI** — authenticated and available in PATH (`gh auth status`)
3. **Dev server** — the project must have a runnable dev server (e.g. `npm run dev`, `pnpm dev`, etc.)
4. **PR context** — either a PR number/URL or a branch name with an open PR

If any prerequisite is missing, inform the user clearly what's needed and stop.

---

## Workflow

Follow these steps in order. Do not skip steps or reorder them.

### Step 1: Gather PR context

Determine the PR number. If the user gave a URL, extract the number. If they
gave a branch name, resolve it:

```bash
gh pr view <branch-name> --json number,title,headRefName,baseRefName,url -q '.'
```

Then fetch the diff to understand what changed:

```bash
gh pr diff <pr-number> --name-only
```

For the full diff (needed to understand the nature of changes):

```bash
gh pr diff <pr-number>
```

Read the diff carefully. Identify:

- **Which components/pages changed** — these are your primary test targets
- **What kind of change** — new feature, bugfix, refactor, styling, layout
- **User-facing behavior changes** — form inputs, buttons, navigation, display logic
- **Conditional rendering or state changes** — these are edge-case goldmines

### Step 2: Prepare the environment

Check out the PR branch if not already checked out and start the dev server:

```bash
git checkout <head-branch>
npm install   # or pnpm install, yarn install — match the project
```

Start the dev server in the background. Detect the correct command from
`package.json` scripts (usually `dev`, `start`, or `serve`):

```bash
# Example — adapt to the actual project
npm run dev &
DEV_SERVER_PID=$!
```

Wait for the server to be ready before proceeding. Poll the expected port:

```bash
# Wait up to 30 seconds for the server to start
for i in $(seq 1 30); do
  curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|304" && break
  sleep 1
done
```

Note: The project might have separate frontend/backend servers. If so, ensure both are running and accessible, along with any needed auth emulators.

### Step 3: Plan tests

Based on the diff analysis from Step 1, create a test plan. Think about this
carefully — the test plan is the backbone of the entire run.

**Primary tests** verify the happy-path behavior of what changed:

- Does the new/modified UI render without errors?
- Do interactive elements (buttons, inputs, links, toggles) work?
- Does form submission/validation behave correctly?
- Do API-driven components display data properly?
- Does navigation work as expected?

**Edge-case tests** probe the boundaries. Generate 3–5 edge cases based on the
nature of the change. Think about what a thorough QA engineer would try:

- Empty states — what happens with no data?
- Overflow — very long text, many items, large numbers
- Rapid interaction — double-clicks, fast repeated submissions
- Invalid input — special characters, empty fields, boundary values
- State transitions — loading → error, loading → empty, back-button behavior
- Responsive behavior — narrow viewport widths if layout changed
- Keyboard navigation — tab order, enter/escape key handling
- Concurrent state — toggling things while requests are in-flight

Pick edge cases that are **relevant to the actual change**, not generic. A PR
that adds a search filter needs overflow and empty-result tests, not a
double-click test on an unrelated button.

### Step 4: Execute tests with Playwright MCP

Use the Playwright MCP to run each test. For every test:

1. **Navigate** to the relevant page
2. **Wait** for the page to be fully loaded (network idle or specific element visible)
3. **Take a screenshot** of the initial state for the report
4. **Perform the interaction** (click, type, submit, resize, etc.)
5. **Assert the result** — check for expected elements, text, state changes
6. **Take a screenshot** of the result state
7. **Record** pass/fail and any observations

Structure your Playwright MCP calls like this (adapt to actual MCP tool names):

```
Navigate to http://localhost:3000/relevant-page
Wait for the page to load completely
Take a screenshot — label it "{test-name}-before"

Perform the interaction:
  - Click the submit button / Type into the search field / etc.

Check the result:
  - Is the expected element visible?
  - Does the text content match expectations?
  - Are there any console errors?

Take a screenshot — label it "{test-name}-after"
```

**Important Playwright MCP patterns:**

- Always wait for network idle or a specific selector before interacting —
  don't race the page load
- Use `waitForSelector` or equivalent before clicking elements
- Check the browser console for errors after each major interaction
- If a test requires authentication, handle login first as a prerequisite step
- If the app uses client-side routing, wait for route transitions to complete

### Step 5: Compile findings

Organize results into three categories:

| Category       | Meaning                                                               |
| -------------- | --------------------------------------------------------------------- |
| ✅ **Pass**    | Behaves as expected, no issues found                                  |
| ⚠️ **Warning** | Works but has a minor concern (accessibility, performance, edge case) |
| ❌ **Fail**    | Broken behavior, visual regression, or error                          |

For each test, record:

- **Test name** — concise, descriptive (e.g., "Search filter with empty query")
- **Result** — Pass / Warning / Fail
- **Details** — What was tested, what happened, what was expected (1–2 sentences)
- **Screenshot reference** — if a screenshot was captured

### Step 6: Post PR comment

Format the findings and post them using `gh`. Use the script at
`scripts/format-comment.sh` if available, or format inline.

The comment must follow this exact structure:

```markdown
## 🧪 Automated UI Test Results

**PR:** #<number> | **Branch:** `<branch>` | **Tested:** <timestamp>

### Summary

- ✅ **X passed** | ⚠️ **Y warnings** | ❌ **Z failed**

### Results

#### Primary Tests

| Test        | Result | Details          |
| ----------- | ------ | ---------------- |
| <test-name> | ✅     | <1-line summary> |

#### Edge Case Tests

| Test        | Result | Details          |
| ----------- | ------ | ---------------- |
| <test-name> | ⚠️     | <1-line summary> |

### Details

<Only include this section if there are warnings or failures.
For each warning/failure, provide:>

#### ⚠️/❌ <Test Name>

**Expected:** <what should happen>
**Actual:** <what happened>
**Suggestion:** <how to fix, if applicable>

---

<sub>Automated UI testing via pr-ui-test skill using Playwright</sub>
```

Post the comment:

```bash
gh pr comment <pr-number> --body "$(cat /tmp/pr-ui-test-comment.md)"
```

If a previous automated comment exists from this skill (search for the
"Automated UI testing via pr-ui-test" footer), consider editing it instead of
creating a duplicate:

```bash
# Find existing comment ID
EXISTING=$(gh api repos/{owner}/{repo}/issues/<pr-number>/comments \
  --jq '.[] | select(.body | contains("Automated UI testing via pr-ui-test")) | .id' \
  | tail -1)

if [ -n "$EXISTING" ]; then
  gh api repos/{owner}/{repo}/issues/comments/$EXISTING \
    -X PATCH -f body="$(cat /tmp/pr-ui-test-comment.md)"
else
  gh pr comment <pr-number> --body "$(cat /tmp/pr-ui-test-comment.md)"
fi
```

### Step 7: Clean up

Stop the dev server.

```bash
kill $DEV_SERVER_PID 2>/dev/null
```

Report the summary to the user in the conversation as well.

---

## Guiding Principles

**Be concise in the PR comment.** Developers skim PR comments. The table
format exists so they can see pass/fail at a glance. Only expand into detail
paragraphs for warnings and failures. Never dump raw logs or full stack traces
into the comment.

**Edge cases should be relevant, not exhaustive.** 3–5 targeted edge cases
based on the actual diff are worth more than 15 generic ones. Quality over
quantity — each edge case should test something that could plausibly break
given the specific changes in the PR.

**Fail gracefully.** If the dev server won't start, if Playwright can't reach
a page, if a selector doesn't exist — record it as a failure with a clear
error message rather than crashing the entire run. Complete what you can and
report what you couldn't.

**Don't test unchanged code.** Focus exclusively on pages and components
touched by the PR diff. Testing unrelated parts of the app wastes time and
creates noise. The one exception: if the PR modifies a shared component (like
a Button or Modal), test a representative consumer of that component.

**Explain the "why" for failures.** A failing test that says "button not
found" is useless. A failure that says "The submit button with selector
`#checkout-submit` was not found — the PR renamed it to `.btn-checkout` but
the form's click handler still references the old ID" is actionable.

---

## Failed Approaches (Read This)

These patterns have been tried and produce poor results:

- **Testing every page in the app** — wastes time, creates noise, almost
  never catches real issues outside the changed code. Stick to the diff.
- **Screenshot-diffing without Playwright assertions** — pixel-level diffs
  produce enormous false-positive rates from anti-aliasing, font rendering,
  and animation timing. Use DOM assertions instead.
- **Posting screenshots as image uploads in PR comments** — GitHub comment
  images require hosting or base64 embedding, both of which are unreliable
  from CI-like contexts. Describe findings in text; keep screenshots local
  for reference only.
- **Running tests without waiting for the dev server** — race condition city.
  Always poll the port before starting tests.
- **Giant monolithic PR comments** — reviewers stop reading after 3 screens.
  Keep the table tight and only expand for problems.
