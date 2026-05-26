---
name: agent-ops-article-verification
description: "Systematically deconstruct written content into verifiable claims, validate each using search/documentation, and facilitate informed discussion through structured interviewing."
license: MIT
compatibility: [opencode, claude, cursor]

metadata:
  category: analysis
  related: [agent-ops-interview, agent-ops-state]

---

# Article Verification Workflow

## Purpose

Help writers produce high-integrity content by identifying and validating every factual claim, opinion, and assertion in an article. Systematically deconstructs content into verifiable components, validates each claim, and facilitates informed discourse through structured interviewing.

## When to Use

- **Pre-publication review**: Verify content before publishing
- **Editor fact-checking**: Flag concerns before content goes public
- **AI output verification**: Validate LLM-generated text before use
- **Content audit**: Retrospective verification of published content
- **Quality assurance**: Automated claim extraction + selective human verification

## Input

- Raw article text (provided directly), OR
- File path to markdown/text file to analyze

## Output

- Verification report saved to `.agent/docs/verification-report-{timestamp}.md`
- Summary in `.agent/focus.md`

---

## Phase 1: Claim Extraction & Atomization

### Purpose

Break content into granular, verifiable units for systematic analysis.

### Process

1. **Read the entire text** for full context
2. **Extract claims** using the Claimify framework:
   - **Selection**: Filter out unverifiable content (pure opinion, conjecture, aesthetic judgments)
   - **Disambiguation**: Clarify ambiguous statements using context
   - **Decomposition**: Break complex statements into atomic claims

### Claim Categories

| Category | Description | Example |
|----------|-------------|---------|
| `FACTUAL` | Verifiable against objective evidence | "Python was released in 1991" |
| `EMPIRICAL` | Claims about measurable phenomena, scientific findings | "Studies show X increases Y by 30%" |
| `OPINION` | Author's interpretation or stance | "React is the best framework" |
| `EXPERT_CLAIM` | Requires domain expertise to verify | "This architecture prevents race conditions" |
| `LOGICAL` | Causal claims, conditional statements | "If X then Y because Z" |

### Extraction Output Format

For each claim, record:

```markdown
### Claim #{N}

**Original text:** "[exact quote from article]"
**Section:** [paragraph/heading reference]
**Category:** [FACTUAL/EMPIRICAL/OPINION/EXPERT_CLAIM/LOGICAL]
**Atomic statement:** [simplified, verifiable form]
```

---

## Phase 2: Verification & Investigation

### Purpose

Search for evidence to support, contradict, or contextualize each extracted claim.

### Process

For each claim:

1. **Search for evidence**
   - Use web search tools (MCP tools, Context7, etc.)
   - Check official documentation when applicable
   - Look for contradictory information
   - Document source credibility
   - Note gaps where information is unavailable

2. **Apply logical analysis**
   - Check internal consistency
   - Verify causal reasoning
   - Identify logical fallacies

3. **Assign verification status**

### Verification Statuses

| Status | Meaning |
|--------|---------|
| ✅ `VERIFIED` | Evidence strongly supports the claim |
| ⚠️ `PARTIALLY_VERIFIED` | Mixed evidence, context-dependent, or nuanced |
| ❌ `CONTRADICTED` | Evidence contradicts the claim |
| ❓ `UNVERIFIABLE` | Cannot find sufficient evidence either way |
| ⏳ `OUTDATED` | Information was once accurate but circumstances changed |
| 🚩 `SUSPICIOUS` | Extraordinary claim, low-credibility source, or logical inconsistency |

### Documentation Requirements

For each claim, record:

- **Source type**: academic, news, official docs, personal, AI-generated
- **Confidence level**: High / Medium / Low
- **Relevant citations**: URLs, document references
- **Caveats**: Context limitations, exceptions
- **Alternative viewpoints**: If applicable

### Special Handling Rules

**Opinion vs Fact:**
- Pure opinions (e.g., "This is important") → note but don't fact-check
- Grounded opinions with evidence claims → check the evidence
- Implicit factual claims within opinions → extract and verify separately

**Causal Claims:**
- Flag claims of causation (A causes B) as requiring higher evidence standards
- Distinguish between correlation and causation
- Note when multiple causal factors exist

**Outdated Information:**
- Flag information that was accurate at publication but has changed
- Provide updated data where available
- Note the publication date's relevance

**Conflicting Evidence:**
- Present both sides fairly
- Note expert consensus where it exists
- Identify areas of legitimate debate

---

## Phase 3: Report Generation

### Purpose

Produce structured markdown report documenting all findings.

### Report Template

```markdown
# Article Verification Report

*Article: [Title or description]*
*Analyzed: [Date]*
*Agent: agent-ops-article-verification*

---

## Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total claims extracted | {N} | 100% |
| ✅ Verified | {N} | {%} |
| ⚠️ Partially verified | {N} | {%} |
| ❌ Contradicted | {N} | {%} |
| ❓ Unverifiable | {N} | {%} |
| ⏳ Outdated | {N} | {%} |
| 🚩 Suspicious | {N} | {%} |

**Overall assessment:** [Brief credibility summary]

---

## Claim-by-Claim Analysis

### Claim #1: "[Exact text from article]"

**Category:** [FACTUAL/EMPIRICAL/OPINION/EXPERT_CLAIM/LOGICAL]
**Extracted from:** [Section/paragraph reference]

**Atomic statement:**
> [Simplified, verifiable form]

**Status:** [✅/⚠️/❌/❓/⏳/🚩] [STATUS_NAME]

**Findings:**
- Evidence supporting: [specific data points, citations]
- Evidence contradicting: [specific data points, citations]
- Source evaluation: [credibility assessment]
- Confidence level: [High/Medium/Low]

**References:**
1. [Source title](URL) — accessed [date]
2. [Source title](URL) — accessed [date]

**Author Notes:** [Space for clarifications added during interview]

---

### Claim #2: ...

[Repeat structure for each claim]

---

## Verification Statistics

- **Claim complexity distribution:** [simple/moderate/complex counts]
- **Primary evidence types used:** [news/academic/official records/other]
- **Major evidence gaps:** [list areas where verification was impossible]
- **Topics requiring expert review:** [if any]

---

## Interview Notes

[Added during Phase 4 — records of author clarifications and updates]

---

## Appendix: Methodology

This report was generated using the agent-ops-article-verification skill, which:
1. Extracts atomic claims from source text
2. Categorizes claims by verifiability type
3. Searches for supporting/contradicting evidence
4. Documents findings with source citations
5. Facilitates author interview for clarifications
```

### Report Location

Save to: `.agent/docs/verification-report-{YYYYMMDD-HHMMSS}.md`

---

## Phase 4: Structured Interview

### Purpose

Facilitate informed discussion with the author about findings, allowing clarification, additional evidence, and consensus on revisions.

### Invocation

Use `agent-ops-interview` skill for structured one-question-at-a-time dialogue.

### Opening Statement

> "I've extracted and verified {N} claims from your content. Let's go through them systematically. For each claim, I'll show what I found, then ask about your sources or reasoning. You can clarify, provide additional context, or revise claims. Ready?"

### Interview Flow

For each claim with status ❌ CONTRADICTED, 🚩 SUSPICIOUS, or ⚠️ PARTIALLY_VERIFIED:

1. **Present the finding**:
   ```
   **Claim #{N}:** "[claim text]"
   **Status:** [status with explanation]
   **Evidence found:** [brief summary]
   ```

2. **Ask ONE clarifying question** (examples):
   - "What evidence informed this claim?"
   - "Did you consider [contradicting evidence]?"
   - "How certain are you about this statement?"
   - "Has anything changed since you wrote this?"
   - "Can you provide the source for this?"

3. **Record response** in the report's "Author Notes" section

4. **Update status if warranted** based on new information

5. **Proceed to next claim** only after current one is resolved

### Handling Responses

| Author says | Action |
|-------------|--------|
| Provides new source | Verify source, update findings, potentially upgrade status |
| Explains context | Add context to Author Notes, reassess if relevant |
| Agrees with contradiction | Mark for revision, note in report |
| Defends claim | Note defense, keep original status with author's reasoning |
| "Skip" | Mark as "Author declined to address", move on |
| "Stop" | End interview, save progress, note incomplete |

### Closing

After all claims reviewed:

1. **Present summary of changes needed**:
   ```
   ## Interview Summary
   
   Claims requiring revision: {N}
   - Claim #3: [brief issue]
   - Claim #7: [brief issue]
   
   Claims clarified (no revision needed): {N}
   
   Remaining unresolved: {N}
   ```

2. **Ask for confirmation**:
   > "Does this summary accurately capture our discussion? Any final clarifications?"

3. **Update report** with all interview notes

4. **Save final report**

---

## Completion Criteria

- [ ] All claims extracted from source content
- [ ] Each claim categorized appropriately
- [ ] Verification attempted for all verifiable claims
- [ ] Status assigned to each claim with supporting evidence
- [ ] Report generated and saved to `.agent/docs/`
- [ ] Interview conducted for disputed/unverified claims
- [ ] Author notes recorded in report
- [ ] Final report includes interview findings
- [ ] Focus.md updated with summary

---

## Anti-patterns (avoid)

- ❌ Skipping claims because they "seem obvious"
- ❌ Marking claims verified without actual evidence search
- ❌ Arguing for or against claims — remain neutral
- ❌ Batching multiple interview questions
- ❌ Proceeding without author response during interview
- ❌ Ignoring nuance — context matters
- ❌ Treating all sources as equally credible
- ❌ Failing to note confidence levels
- ❌ Not distinguishing correlation from causation

---

## Tool Integration

### Web Search

Use available MCP tools for evidence gathering:
- `mcp_context7_query-docs` — for library/framework documentation
- `mcp_microsoftdocs_microsoft_docs_search` — for Microsoft/Azure content
- `fetch_webpage` — for general web content
- `semantic_search` — for workspace context

### Interview

Invoke `agent-ops-interview` skill for Phase 4 structured dialogue.

### State

Update `.agent/focus.md` after each phase:

```markdown
## Just did
- Article verification Phase {N} for "{content title}"
  - Claims extracted: {N}
  - Status: {summary}

## Doing now
- Phase {N+1}: {description}

## Next
- {remaining phases}
```

---

## Example Invocation

**User input:**
> "Verify this article: Python is the most popular programming language in 2024, with over 50% market share. It was created by Guido van Rossum in 1989 and is used by 90% of data scientists."

**Phase 1 output:**
```markdown
### Claim #1
**Original:** "Python is the most popular programming language in 2024"
**Category:** EMPIRICAL
**Atomic:** Python ranks #1 in programming language popularity metrics for 2024

### Claim #2
**Original:** "with over 50% market share"
**Category:** EMPIRICAL
**Atomic:** Python has >50% market share among programming languages

### Claim #3
**Original:** "created by Guido van Rossum in 1989"
**Category:** FACTUAL
**Atomic:** Guido van Rossum created Python in 1989

### Claim #4
**Original:** "used by 90% of data scientists"
**Category:** EMPIRICAL
**Atomic:** 90% of data scientists use Python
```

**Phase 2 would then verify each claim with evidence search.**
