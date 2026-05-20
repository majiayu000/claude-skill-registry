---
name: ppw:literature
description: >-
  Search academic literature via Semantic Scholar MCP, select papers interactively,
  and generate verified BibTeX entries. 文献检索与BibTeX生成，通过Semantic Scholar MCP。
triggers:
  primary_intent: search academic literature and generate BibTeX citations
  examples:
    - "Find papers about urban heat island"
    - "帮我找关于城市热岛的文献"
    - "Search literature for spatiotemporal analysis"
    - "生成这篇文章的BibTeX引用"
    - "Find relevant papers on deep learning for land use classification"
    - "帮我检索相关文献并生成引用格式"
tools:
  - External MCP
  - Structured Interaction
references:
  required: []
  leaf_hints: []
input_modes:
  - pasted_text
output_contract:
  - bibtex_entry
---

## Purpose

This Skill searches academic literature using the Semantic Scholar MCP, presents an interactive numbered result list (up to 10 papers), waits for the user to select a specific paper, then generates a verified BibTeX entry built exclusively from MCP-returned data. Before any workflow begins, a pre-flight probe confirms MCP availability — if unavailable, the Skill refuses immediately with setup instructions rather than proceeding with degraded capability. After the user selects a paper, a mandatory anti-hallucination verification prompt reminds the user to confirm the paper's actual relevance before committing the citation. This Skill does not write or rewrite paper content; it searches, selects, and generates citation entries only.

## Trigger

**Activates when the user asks to:**
- Search or find academic papers on a topic
- Generate BibTeX or citation entries for a reference
- 帮我找文献、检索相关论文、帮我生成引用格式

**Example invocations:**
- "Find papers about urban heat island" / "帮我找关于城市热岛的文献"
- "Search literature for spatiotemporal analysis" / "检索时空分析相关文献"
- "Generate BibTeX for a citation" / "帮我生成BibTeX引用格式"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-shot search → result list → user selects → BibTeX generated; no iteration |
| `batch` | | Not supported — each search requires user selection in session |

**Default mode:** `direct`. Search is single-shot: if results are unsatisfactory, user re-triggers the Skill with different keywords.

## References

### Required (always loaded)

None. This is a search task — no expression pattern files needed.

### Leaf Hints

None.

> No reference files loaded. All paper metadata sourced from Semantic Scholar MCP at runtime.

## Ask Strategy

The Skill collects search inputs conversationally. At most two questions:

1. **Search query** (required): the topic or keyword to search — ask only if not provided in the trigger message.
2. **Result count** (optional): how many results to display. Default: 5. Maximum: 10.

If the user provides the topic in the trigger message, skip question 1 and proceed immediately.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:literature` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:literature？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1: MCP Pre-flight Check

1. Call `mcp__semantic-scholar__papers-search-basic` with `{"query": "test", "limit": 1}`.
2. If the call succeeds: proceed to Step 2.
3. If the call fails or tool is unavailable: **refuse immediately** with:

   > "Semantic Scholar MCP is not available. To use this Skill:
   > 1. Open Claude Code Settings → MCP Servers
   > 2. Add the Semantic Scholar server (server key: `semanticscholar`)
   > 3. Restart Claude Code and retry"

   Do NOT proceed past this point if MCP is unavailable.

### Step 2: Collect Search Query

1. Extract the search topic from the trigger message if present.
2. If topic not provided, ask: "What topic or keywords should I search for?"
3. Confirm result count (default: 5).
- **Record workflow:** Append `{"skill": "ppw:literature", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 3: Execute Search and Build Result Cards

1. Call `mcp__semantic-scholar__papers-search-basic` with the user's query and result count.
2. For each returned paper: if the abstract field is empty in the search result, call `mcp__semantic-scholar__get-paper-abstract` to fetch an abstract excerpt.
3. Display numbered result cards in this exact format:

   ```
   **[1] Title of the Paper**
   Authors: Smith, J.; Lee, K. · Year: 2023 · Citations: 142
   > "One sentence from abstract describing the core contribution..."

   **[2] Another Relevant Paper**
   Authors: Zhang, W. · Year: 2022 · Citations: 89
   > "Abstract not available"
   ```

4. End the display with: "Please select a paper (enter number), or type 'none' to cancel."

### Step 4: User Selection

1. Wait for the user to enter a number or "none".
2. If "none": respond "Search cancelled." and end the session.
3. If out-of-range number: ask the user to re-enter a valid number from the displayed list.
4. If valid number: confirm the selection by restating the paper title.
5. Display the **mandatory verification prompt** (never omit):

   > "Please confirm that the selected paper actually supports the claim you are citing — do not rely solely on the title."

### Step 5: Generate BibTeX

1. Construct the BibTeX entry using **only fields returned by the MCP** for the selected paper.
2. Citation key format: `firstAuthorLastnameLowercaseYYYYfirstKeyword` (e.g., `smith2023urban`).
3. Use `@article` for journal papers, `@inproceedings` for conference papers, `@misc` for preprints — follow the paper type returned by MCP.
4. If any field (volume, pages, DOI) is not returned by MCP, **omit that field** — never fill from prior knowledge.
5. Display the BibTeX in a code fence:

   ````bibtex
   @article{smith2023urban,
     title     = {Full title from MCP},
     author    = {Last, First and Last2, First2},
     journal   = {Journal name from MCP},
     year      = {2023},
     volume    = {101},
     pages     = {101943},
     doi       = {10.1016/j.compenvurbsys.2023.101943}
   }
   ````

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `bibtex_entry` | BibTeX code block (`@article`, `@inproceedings`, or `@misc`) | After user selects a paper |

> All field values must come from the MCP-returned paper record. Never supply missing fields from prior knowledge — omit them instead.

**Example BibTeX (all fields from MCP data):**

```bibtex
@article{li2022spatiotemporal,
  title  = {Spatiotemporal Analysis of Urban Land Use Change},
  author = {Li, Wei and Wang, Fang},
  journal = {Computers, Environment and Urban Systems},
  year   = {2022},
  volume = {95},
  pages  = {101812},
  doi    = {10.1016/j.compenvurbsys.2022.101812}
}
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| MCP pre-flight fails | Refuse with exact setup instructions from Step 1; never proceed to search |
| Search returns zero results | "No papers found for '[query]'. Try broader keywords or re-trigger with different terms." |
| Abstract field missing for a result | Show "Abstract not available" in result card; do not skip the paper |
| User selects out-of-range number | Ask to re-enter a valid number from the displayed list |
| User types "none" | "Search cancelled." — end session |
| MCP returns non-article type | Use `@inproceedings` or `@misc` as appropriate; never force `@article` |
| DOI not returned by MCP | Omit `doi` field; add comment: `% DOI not available — please verify manually` |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Semantic Scholar MCP unavailable | Refuse immediately with setup guidance (Step 1 handles this); no partial fallback mode |
| `get-paper-abstract` call fails for one paper | Mark abstract as "Abstract not available"; continue displaying remaining results |
| Structured Interaction unavailable | Ask search query as plain-text question; proceed with numbered list in conversation |
| Basic search returns poor results | Inform user: "If results are poor, re-trigger the Skill with more specific keywords" (single-shot only) |

## Examples

**User:** "Find papers about urban heat island mitigation"

**Skill:** [Pre-flight check passes silently] → Calls `mcp__semantic-scholar__papers-search-basic` with `{"query": "urban heat island mitigation", "limit": 5}` → Displays results:

```
**[1] Urban Heat Island Mitigation through Green Infrastructure**
Authors: Smith, J.; Lee, K. · Year: 2023 · Citations: 142
> "This study evaluates green roof and tree-planting strategies for reducing UHI intensity in dense urban cores."

**[2] Cool Pavements and Their Effect on Urban Thermal Comfort**
Authors: Zhang, W.; Chen, L. · Year: 2022 · Citations: 89
> "A field experiment comparing reflective pavement materials across five climate zones."
```

Please select a paper (enter number), or type "none" to cancel.

**User:** "1"

**Skill:** "You selected: Urban Heat Island Mitigation through Green Infrastructure (Smith, J.; Lee, K., 2023)."

> "Please confirm that the selected paper actually supports the claim you are citing — do not rely solely on the title."

**Skill (after user confirms):**

```bibtex
@article{smith2023urban,
  title   = {Urban Heat Island Mitigation through Green Infrastructure},
  author  = {Smith, John and Lee, Kwang-Ho},
  journal = {Computers, Environment and Urban Systems},
  year    = {2023},
  volume  = {101},
  pages   = {101943},
  doi     = {10.1016/j.compenvurbsys.2023.101943}
}
```

---

*Skill: literature-skill*
*Conventions: references/skill-conventions.md*
