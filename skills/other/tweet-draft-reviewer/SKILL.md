---
name: tweet-draft-reviewer
description: Review tweet drafts in Claude Code against 8 voice rules. Scores 1-10, breaks down every rule, and rewrites anything that scores below 7.
---

# Tweet Draft Reviewer

Paste a tweet draft and get a score out of 10, a rule-by-rule breakdown, and a rewrite if the score is below 7. Takes 30 seconds. Saves you from posting something that sounds like a chatbot wrote it.

Built on 8 voice rules distilled from real content analysis — what separates high-engagement tweets from the ones that get skimmed.

---

## How to Use

**Single draft:**
```
Review this tweet draft: [paste tweet here]
```

**Batch scan:**
```
Review all tweet drafts in my content/tweet-drafts/ folder.
```

---

## Skill Instructions (for Claude Code)

When this skill is invoked, follow these phases exactly.

---

### PHASE 1: INTAKE

Determine input mode:

**Mode A — Direct paste:** User provided draft text inline. Proceed to PHASE 2 with that text.

**Mode B — Folder scan:** User asked to review drafts folder. Run:

```bash
VAULT="${VAULT_PATH:-$(pwd)}"
find "$VAULT/content/tweet-drafts" -name "*.md" 2>/dev/null | while read f; do
  if ! grep -q 'reviewed: true' "$f" 2>/dev/null; then
    echo "UNREVIEWED:$f"
  fi
done
```

If no vault path was given and no `content/tweet-drafts/` exists in the current directory, ask:
```
Where is your tweet drafts folder? (full path, e.g. /root/obsidian-vault/content/tweet-drafts)
```

**Mode C — Ambiguous:** No draft provided and no folder context. Ask:
```
Paste your tweet draft here, or tell me the path to your tweet-drafts folder and I'll scan it.
```

---

### PHASE 2: ANALYZE

Apply all 8 rules to the draft. For each rule, record ✅ PASS or ❌ FAIL with a one-line reason.

---

#### The 8 Rules

**Rule 1: No "I" opener**
- FAIL: First word is exactly `I` (standalone — not "In", "It", "If")
- PASS: Anything else

**Rule 2: Strong opener**
- FAIL: First sentence ends with `?` OR starts with "Have you", "Do you", "Are you", "What if", "What would"
- PASS: Declarative statement, specific number/fact, named scenario, or emotional setup

**Rule 3: No AI tells**
- FAIL: Contains any of: `delve`, `certainly`, `game-changing`, `game changer`, `it's worth noting`, `invaluable`, `unleash`, `revolutionize`, `transformative`
- PASS: None of those words detected

**Rule 4: No generic closers**
- FAIL: Ends with (or contains near the end): `what do you think`, `drop a comment`, `thoughts?`, `let me know in the comments`, `agree?`, `sound familiar?`
- PASS: Ends with a statement, directive, punchline, or thread hook

**Rule 5: Corey Test (specificity)**
- FAIL: Uses vague language without specifics — "it changed how I work", "massive results", "so much better" — no numbers, names, or concrete outcomes
- PASS: Contains at least one specific: a number, timeframe, named tool, or concrete result

**Rule 6: Character count**
- PASS: 280 characters or fewer
- THREAD PASS: Over 280 chars BUT sections are numbered (1/, 2/, 3/) or clearly separated with line breaks — count as PASS
- FAIL: Over 280 chars with no thread formatting

**Rule 7: Single point**
- FAIL: Makes 3+ distinct unrelated claims with no clear through-line
- PASS: One core idea, even if supported by 2–3 details

**Rule 8: Punchy rhythm**
- FAIL: Any sentence over 20 words OR preamble like "I've been thinking a lot about..." / "Something I've noticed recently is..."
- PASS: Short sentences, no preamble, gets to the point by line 2 at latest

---

### PHASE 3: OUTPUT

Print this exact format:

```
TWEET REVIEW
────────────

Score: X/10

Rule-by-Rule:
1. ✅/❌ No "I" opener — [reason]
2. ✅/❌ Strong opener — [reason]
3. ✅/❌ No AI tells — [reason]
4. ✅/❌ No generic closers — [reason]
5. ✅/❌ Corey Test — [reason]
6. ✅/❌ Character count — [reason + actual count]
7. ✅/❌ Single point — [reason]
8. ✅/❌ Punchy rhythm — [reason]

────────────
```

**Scoring table (passes → score):**

| Passes | Score |
|--------|-------|
| 8 | 10/10 |
| 7 | 9/10 |
| 6 | 8/10 |
| 5 | 6/10 |
| 4 | 5/10 |
| 3 | 4/10 |
| 2 | 3/10 |
| 1 | 1/10 |
| 0 | 0/10 |

**If score ≥ 7:**
```
→ Ready to post. Use Typefully or your scheduler to queue it.
```

**If score < 7 — add a rewrite:**
```
Suggested Rewrite:

[rewritten tweet that fixes all failing rules]
```

---

### PHASE 4: SELF-CRITIQUE

Before delivering the output, check:

1. **All 8 rules evaluated** — Count the rule lines in your output. There must be exactly 8. If any are missing, add them.
2. **Score matches pass count** — Count the ✅ marks. Verify the score matches the table above. Correct it if not.
3. **Rewrite quality** — If a rewrite was provided, check it against all 8 rules mentally. Does it pass the ones the original failed? If the rewrite would score below 7 itself, rewrite it again.
4. **Reason quality** — Each rule result must have a specific reason, not a generic one. "Too vague" is not enough — say what specifically is vague.

Fix anything that fails before delivering.

---

## Example Review

**Input:**
```
I've been thinking a lot about how AI is really changing the way founders 
approach content creation and productivity, and I think it's worth noting 
that the teams who figure out async AI workflows are going to have a 
massive advantage. What do you think about this?
```

**Output:**
```
TWEET REVIEW
────────────

Score: 2/10

Rule-by-Rule:
1. ❌ No "I" opener — Starts with "I've"
2. ❌ Strong opener — Slow setup, no hook, no specific fact
3. ❌ No AI tells — Contains "it's worth noting"
4. ❌ No generic closers — Ends with "What do you think about this?"
5. ❌ Corey Test — "massive advantage" is vague, no numbers or concrete outcome
6. ✅ Character count — 248 chars
7. ✅ Single point — Focused on async AI workflows
8. ❌ Punchy rhythm — Run-on sentence, preamble opener

────────────

Suggested Rewrite:

The founders winning right now aren't working harder.

They have agents running at 2am. Content drafted. Research done.
Queue processed.

By 7am they're reviewing output, not creating it.

Async AI ops is the new early morning routine.
```

---

## Batch Mode Output

When scanning a folder, output one review block per file:

```
📄 content/tweet-drafts/linkedin-ai-post.md
[full review block]

📄 content/tweet-drafts/founder-ops.md
[full review block]

────────────
BATCH SUMMARY
Reviewed: 4 drafts
Ready to post (≥7): 2
Need rewrite (<7): 2
```

---

## Requirements

- Claude Code with bash tool access (for folder scan mode)
- No external APIs — pure LLM reasoning for the review
- Tweet drafts folder at `content/tweet-drafts/` (optional — direct paste always works)
- Files in the drafts folder are marked `reviewed: true` to skip them in future scans
