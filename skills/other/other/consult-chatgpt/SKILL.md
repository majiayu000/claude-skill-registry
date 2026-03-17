---
name: consult-chatgpt
description: Lightweight ChatGPT consultation for agents (cached, budgeted)
argument-hint: "<goal> | <context> | <evidence> | <tried> | <question>"
allowed-tools: [Read, Write, Bash, Glob]
---

# ChatGPT Consultation Broker

Consult ChatGPT for a second opinion on debugging, architecture, or best practices questions.
This skill implements caching to avoid redundant calls.

**Arguments format**: `$ARGUMENTS`

The arguments should contain your consultation context. Structure it roughly as:
- **Goal**: What you're trying to fix/understand (1-2 sentences)
- **Context**: Runtime, key libraries, constraints
- **Evidence**: Symptoms, snippets, observed vs expected behavior
- **Tried**: What you've already attempted and results
- **Question**: Specific questions you want answered

You can provide this as free-form text - the skill will format it appropriately.

---

## Process

### Step 1: Parse and Validate Input

Extract the following from the provided arguments:
- `goal`: One sentence describing what you're fixing/understanding
- `context`: Runtime versions, key libraries, constraints
- `evidence`: Symptom description, minimal code snippet (max 60 lines), observed vs expected
- `tried`: List of attempts and their results
- `question`: Specific questions (ideally 1-3)

If the input is too vague or missing critical components, ask for clarification before proceeding.

### Step 2: Format the Question

Create a question file at `/tmp/consult-chatgpt-question.md` with this structure:

```markdown
# Goal
[goal - one sentence]

# Context
- Runtime: [version info]
- Key libs: [relevant libraries and versions]
- Constraints: [any hard constraints]

# Evidence
- Symptom: [description]
- Minimal snippet:
```[language]
[code - max 60 lines]
```
- Observed: [what happens]
- Expected: [what should happen]

# Tried
- [attempt 1]: [result]
- [attempt 2]: [result]

# Question
1. [primary question]
2. [secondary question if relevant]
3. What's the fastest experiment to discriminate between possible causes?
```

**Validation checklist before proceeding:**
- [ ] Goal is a specific sentence (not vague)
- [ ] Code snippet is <= 60 lines
- [ ] No secrets, tokens, or PII included
- [ ] Total file size <= 4KB
- [ ] Questions are specific and answerable

### Step 3: Compute Fingerprint and Check Cache

Compute a fingerprint to check if we've already answered this question:

```bash
# Create cache directory if needed
mkdir -p ~/.cache/consult-chatgpt/answers

# Compute fingerprint from question content
FINGERPRINT=$(cat /tmp/consult-chatgpt-question.md | md5sum | cut -d' ' -f1)
CACHE_FILE=~/.cache/consult-chatgpt/answers/${FINGERPRINT}.md

# Check if cached answer exists
if [ -f "$CACHE_FILE" ]; then
    echo "CACHE_HIT: Found cached answer for fingerprint $FINGERPRINT"
    cat "$CACHE_FILE"
    exit 0
fi
```

If cache hit, read the cached answer file and skip to Step 5 (return the answer).

### Step 4: Call ChatGPT

If no cache hit, send the question to ChatGPT:

```bash
# Send to ChatGPT with 20-minute timeout
ask-question -f /tmp/consult-chatgpt-question.md \
             -o /tmp/consult-chatgpt-answer.md \
             -t 1200000

# Cache the answer
FINGERPRINT=$(cat /tmp/consult-chatgpt-question.md | md5sum | cut -d' ' -f1)
cp /tmp/consult-chatgpt-answer.md ~/.cache/consult-chatgpt/answers/${FINGERPRINT}.md
```

### Step 5: Parse and Return Structured Answer

Read the answer from `/tmp/consult-chatgpt-answer.md` (or cache file).

Extract and summarize:
1. **Top 3-5 likely causes** identified by ChatGPT
2. **Recommended discriminating tests** to narrow down the cause
3. **Suggested fix** if ChatGPT provided one
4. **Caveats/assumptions** in ChatGPT's reasoning

Present to the calling agent in this format:

```
## ChatGPT Consultation Result

**Fingerprint**: [hash]
**Source**: [CACHE_HIT or FRESH_CALL]

### Likely Causes (in order of probability)
1. [cause 1]
2. [cause 2]
3. [cause 3]

### Discriminating Tests
- [test 1]: If [result], then [cause X] is likely
- [test 2]: If [result], then [cause Y] is likely

### Suggested Approach
[ChatGPT's recommended fix or approach]

### Caveats
- [assumption 1]
- [caveat 1]

---

**IMPORTANT**: Treat this as a hypothesis, not truth.
1. Run the discriminating tests first
2. Verify locally before implementing
3. If the answer doesn't fit your evidence, something is wrong with the question
```

---

## Cache Management

The cache lives at `~/.cache/consult-chatgpt/`:
- `answers/[fingerprint].md` - cached answers

To clear cache (if needed):
```bash
rm -rf ~/.cache/consult-chatgpt/answers/*
```

To see cache stats:
```bash
echo "Cached answers: $(ls ~/.cache/consult-chatgpt/answers/ 2>/dev/null | wc -l)"
du -sh ~/.cache/consult-chatgpt/ 2>/dev/null || echo "Cache empty"
```

---

## Budget Reminder

This skill should only be invoked when:
- `consult_score >= 5` (per the consultation policy)
- At least one local experiment has been attempted
- You can articulate "what would change my mind"

**Budget**: Max 2 consultations per top-level task. Cooldown 15 minutes between calls.

If you're hitting budget limits, consider:
1. Asking another internal agent (Oracle, Librarian)
2. Running more local experiments
3. Breaking down the problem into smaller pieces
