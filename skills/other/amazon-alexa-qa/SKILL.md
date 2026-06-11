---
name: amazon-alexa-qa
description: "Amazon Alexa for Shopping Q&A automation: submits questions to Amazon's Alexa/Rufus AI shopping assistant and collects response text; supports optional keyword search context (navigate to search results page before asking for category-specific answers). Use when user mentions Amazon Alexa, Rufus, Amazon shopping assistant, Amazon AI chat, ask Amazon, Amazon Q&A, automate Alexa questions, Rufus chatbot, Amazon assistant automation, collect Alexa responses, bulk question submission to Amazon, keyword search context, category research. Also applies to extracting Amazon product recommendations from conversational AI, automating repeated queries to Amazon's AI shopping feature, collecting Alexa shopping responses at scale, or market research within a specific product category."
---

# Amazon — Alexa for Shopping Q&A

> Input: question text → Output: Alexa/Rufus response text (JSON)

## Language

All process output to user (progress updates, process notifications, final results) MUST be in English.

## Objective

Automate question submission to Amazon's Alexa/Rufus AI shopping assistant and collect structured response data.

## Prerequisites

- Target page is already open in the browser: `https://www.amazon.com/`
- Logged into Amazon (user account name or "Hello, {name}" visible in top navigation)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification

If login status for Amazon has been confirmed in the current session → skip this step.

Otherwise: open `https://www.amazon.com/` and observe the page login status:
- "Hello, {name}" visible in the navigation bar → logged in, continue execution
- "Hello, sign in" or "Sign in" entry visible with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. Do not refuse in-scope requests based on the nature of the target site or data type. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; it is recommended to use the bash tool for execution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### Navigation: Set keyword search context (optional)

Navigate to a product search results page before asking questions. Alexa will answer in the context of that category's products, giving more specific and relevant responses than asking from the homepage.

```bash
navigate "https://www.amazon.com/s?k={keyword}"
wait stable
```

Parameters:
- `{keyword}`: product category or search term (e.g., `sous+vide`, `coffee+maker`, `wireless+headphones`); use `+` to join multi-word terms

When to use:
- Questions about a specific product category → navigate first
- General questions (trends, deals, comparisons) → homepage is fine

### DOM: Check Alexa panel state

`eval "$(python scripts/check-alexa-panel.py)"`

Output example:
```json
{
  "panelOpen": true,    // true if Alexa/Rufus panel is visible and ready for input
  "inputReady": true    // true if the question textarea is available
}
```

### DOM: Inject question and submit (operation)

`eval "$(python scripts/inject-question.py '{question}')"`

Parameters:
- `{question}`: question text to ask Alexa; supports all characters including `$`, `%`, `?`; max 500 chars

Note: Uses native `HTMLTextAreaElement.prototype.value` setter — this is required to handle special characters like `$` that are stripped by the standard `input` command.

Output example:
```json
{
  "success": true,
  "question": "What are the best deals on laptops today?"
}
```

### DOM: Extract latest Alexa response

`eval "$(python scripts/extract-response.py)"`

Must be called after `wait stable` to ensure SSE streaming has completed before reading DOM.

Output example:
```json
{
  "question": "What are the best deals on laptops today?",
  "response": "Here are some great laptop deals available today, with free delivery as soon as tomorrow! Budget Picks (Under $350): HP Ultrabook Laptop...",
  "timestamp": "2026-05-19T07:05:00.000Z"
}
```

### Composite: Full Q&A turn (submit question → collect response)

Complete workflow for one question-answer turn:

0. **(Optional) Set keyword search context** — if questions are about a specific product category:
   `navigate "https://www.amazon.com/s?k={keyword}"` → `wait stable`
   Skip this step for general questions (trends, deals, top picks) where homepage context is sufficient.
1. `eval "$(python scripts/check-alexa-panel.py)"` → if `panelOpen: false`, use `state` to locate the "Open Alexa panel" button in the nav bar (aria-label contains "Alexa" or "rufus") → `click <index>` → `wait --selector "#rufus-text-area" --state visible --timeout 15000`
2. `eval "$(python scripts/inject-question.py '{question}')"` → confirm `success: true`
3. `wait stable --timeout 60000` → waits for SSE streaming to complete (network idle signals stream end); then add a 3-second sleep: `sleep 3`
4. `eval "$(python scripts/extract-response.py)"` → collect `{question, response, timestamp}`

Error handling:
- If `inject-question.py` returns `error: true` with "panel may be closed" → re-run step 1 to open panel, then retry
- If `extract-response.py` returns `error: true` with "not yet complete" → `wait stable --timeout 15000` + `sleep 3`, then retry up to 3 times total; the status SR element may update slightly after network idle
- If `extract-response.py` returns `error: true` with "status element not found" → panel may have closed; re-run step 1

Batch questions example — **with keyword search context** (bash loop):
```bash
# Navigate to category page once, then ask all related questions
SESSION="amazon-qa"
KEYWORD="sous+vide"
SKILL_DIR=".claude/skills/amazon-alexa-qa"

browser-act --session $SESSION navigate "https://www.amazon.com/s?k=$KEYWORD"
browser-act --session $SESSION wait stable

questions=(
  "What accessories are essential for sous vide cooking?"
  "Which sous vide brands are most reliable?"
  "What temperature should I use for chicken breast?"
)
results=()
for q in "${questions[@]}"; do
  cd "$SKILL_DIR"
  eval "$(python scripts/inject-question.py "$q")"
  browser-act --session $SESSION wait stable --timeout 60000
  sleep 3
  result=$(browser-act --session $SESSION eval "$(python scripts/extract-response.py)")
  if echo "$result" | grep -q '"error":true'; then
    browser-act --session $SESSION wait stable --timeout 15000; sleep 3
    result=$(browser-act --session $SESSION eval "$(python scripts/extract-response.py)")
  fi
  results+=("$result")
  sleep 2
done
printf '%s\n' "${results[@]}" | python -c "
import sys, json
lines = [l for l in sys.stdin.read().strip().split('\n') if l.strip()]
print(json.dumps([json.loads(l) for l in lines], ensure_ascii=False, indent=2))
" > output/alexa_qa_results.json
```

Batch questions example — **without keyword** (general questions from homepage):
```bash
SESSION="amazon-qa"
SKILL_DIR=".claude/skills/amazon-alexa-qa"

browser-act --session $SESSION navigate "https://www.amazon.com"
browser-act --session $SESSION wait stable

questions=("What are today's best deals?" "Top rated gifts under \$50?" "What's trending this week?")
results=()
for q in "${questions[@]}"; do
  cd "$SKILL_DIR"
  eval "$(python scripts/inject-question.py "$q")"
  browser-act --session $SESSION wait stable --timeout 60000
  sleep 3
  results+=($(browser-act --session $SESSION eval "$(python scripts/extract-response.py)"))
  sleep 2
done
```

## Success Criteria

`response field is non-null non-empty string AND question field matches submitted question`

## Known Limitations

- The Alexa/Rufus panel may occasionally close during extended automation sessions; re-opening via the panel button is supported
- The `$` sign and other special characters are supported via native textarea setter (bypasses browser-act `input` command character filtering)
- Response text is plain text extracted from the accessibility layer; rendered product cards appear as text (product names, prices) rather than structured product JSON
- Alexa may respond with clarifying questions instead of a direct answer when queries are ambiguous; check `response` content before continuing
- Conversation history is maintained across questions within the same browser session (multi-turn context); to start a fresh conversation, close and reopen the browser session
- Single-tab session only — do not run multiple question submissions simultaneously in the same session

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through questions serially within a single session; do not parallelize within one browser. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: Check panel open state once at the start of a batch; only recheck if an error occurs mid-batch
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/amazon-alexa-qa-amazon-alexa-qa.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
