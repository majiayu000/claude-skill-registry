---
name: ask_paper
description: Answer questions about a paper in the vault, using note first and arXiv HTML as fallback
---

## ❓ Ask Paper Skill

Answer a question about a specific paper in the vault.

**Input format:** `/ask_paper <partial paper title or keyword> | <question>`

If no `|` separator is present, treat the entire argument as combined input and infer the paper title and question from context.

---

## CRITICAL RULES

- **Read the paper note first** — always attempt to answer from the note
- **Only fetch arXiv HTML if the note is insufficient** — avoid unnecessary web requests
- **Never hallucinate** — if the answer isn't in the note or the paper, say so
- **Single paper scope** — answer questions about one paper at a time
- **Project context allowed** — may reference linked projects from the note to give research-relevant answers
- **Update the note** when arXiv HTML provides significant new information relevant to the question

---

## WORKFLOW

### 1. Resolve paper identity

**Fuzzy matching:**
- Search `Reading/` directory for files matching the provided title/keyword
- Use glob pattern: `Reading/*<keyword>*.md`
- If multiple matches, pick the closest match or ask user to disambiguate
- If no match, inform user the paper is not in the vault

**Validation:**
- Confirm the matched file exists in `Reading/`
- Extract paper title from file name

### 2. Read the paper note

- Read the full paper note from `Reading/<paper title>.md`
- Extract all sections and content
- Extract the `url` field from YAML frontmatter (needed for fallback)
- Extract linked projects from "Linked Research Projects" section

### 3. Attempt to answer from the note

**Evaluate confidence:**
- Can the question be fully answered using information in the note?
- Is the answer specific enough, or would it benefit from more detail?

**Confidence levels:**
- **HIGH**: Answer is clearly and specifically covered in the note → answer directly, skip arXiv fetch
- **MEDIUM**: Answer is partially covered but lacks detail → answer from note, then fetch arXiv for enrichment
- **LOW**: Answer is not covered in the note at all → must fetch arXiv HTML

**If HIGH confidence:** Answer the question using note content. Done.

**If MEDIUM or LOW:** Proceed to step 4.

### 4. Fetch arXiv HTML (fallback)

**Get the URL:**
- Use the `url` field from the paper note's YAML frontmatter
- The URL should be an arXiv HTML link (e.g., `https://arxiv.org/html/[paper-id]`)
- If URL is missing or `none`, inform user and attempt to find it via paper title search

**Fetch with targeted prompt:**
- Use WebFetch with a prompt specifically targeting the user's question
- Do NOT extract the entire paper — focus the prompt on the relevant section
- Example prompt: "Find information about [specific topic from question] in this paper. Look in methods, results, and discussion sections."

**Token efficiency:**
- Craft the WebFetch prompt to extract only the information needed to answer the question
- Avoid generic "extract everything" prompts
- If the question is about methods → target methods section
- If the question is about results → target results/experiments section
- If the question is about a specific concept → target the relevant section + definitions

### 5. Answer the question

**Format:**
- Bullet points preferred (consistent with vault style)
- Cite specific sections/figures/tables when possible
- If project context is relevant, mention which linked projects the answer connects to
- Be concise — answer the question, don't summarize the whole paper

**Source attribution:**
- If answered from note only: no attribution needed
- If answered from arXiv HTML: note that this information was fetched from the paper directly

### 6. Update the paper note (when arXiv HTML was fetched)

**When to update:**
- Only when arXiv HTML provided information NOT already in the note
- Only when the new information is significant (not trivial details)
- Only add information relevant to the question and the note's existing structure

**How to update:**
- Identify the most appropriate existing section in the note for the new information
- Add bullet points under the relevant subsection
- Do NOT restructure or rewrite existing content
- Do NOT add new sections — use existing template sections only
- Keep additions concise (1-3 bullets max)

**What to add:**
- Specific technical details that enrich an existing section
- Key results or numbers not captured in the note
- Method details that clarify the approach
- Important caveats or nuances

**What NOT to add:**
- Information already in the note (even if phrased differently)
- Tangential details not related to the question
- Full section rewrites

**After updating:**
- Briefly inform the user what was added to the note and where

---

## HANDLING EDGE CASES

### Paper not in vault
- Inform user: "Paper not found in Reading/. Would you like me to read it first using /read_paper?"

### No arXiv URL in frontmatter
- Check if `url` field is `none` or missing
- Inform user the URL is not available
- Suggest adding the URL to the frontmatter

### Question requires cross-referencing
- If the question implicitly compares to another paper, answer only for the target paper
- Mention: "For comparison with [other paper], you could run /ask_paper on that paper as well."

### Question about linked projects
- Read the linked project files if needed to provide project-relevant context
- Only read projects listed in the "Linked Research Projects" section
- Keep project context brief — focus on the paper question

---

## TOKEN EFFICIENCY

**Optimizations:**
- Always try note first (zero web cost)
- Targeted WebFetch prompts (skip irrelevant paper sections)
- Read only the specific project files if project context is needed
- Single WebFetch call in most cases

**Expected cost:**
- Note-only answer: ~50 tokens (just file read)
- ArXiv fallback: ~100-200 tokens (one targeted WebFetch)

---

## OUTPUT RULES

- Bullet points preferred
- Concise, direct answers
- Cite sections/figures/tables when referencing arXiv content
- Mention source (note vs arXiv) only when arXiv was fetched
- If note was updated, report what was added and where
- No essays — answer the question and stop

---

## SELF-CHECK

✅ Did I search Reading/ for the paper using fuzzy matching?
✅ Did I read the full paper note before attempting to answer?
✅ Did I evaluate confidence before fetching arXiv HTML?
✅ Did I use a targeted WebFetch prompt (not generic)?
✅ Did I answer concisely with bullet points?
✅ If I fetched arXiv: did I update the note with significant new information?
✅ If I updated the note: did I inform the user what was added?
✅ Did I reference linked projects when relevant to the question?
