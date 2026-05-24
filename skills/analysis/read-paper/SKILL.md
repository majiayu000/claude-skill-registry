---
name: read_paper
description: Convert a research paper into structured Obsidian notes and link research projects
---

## 📄 Paper Reading Skill

Read a research paper and convert it into:
- one structured **paper note**
- one or more linked **research project notes**

This skill transforms reading into reusable research ideas.

---

## CRITICAL RULES (NON-NEGOTIABLE)
- Paper notes live **only** in `Reading/`
- Use `Templates/Paper Note.md` **exactly** - preserve ALL headings, emojis, and structure
- Project notes live **only** in `Projects/`
- Never create topic notes or concept-only notes
- Research ideas always live as **project notes**
- Paper notes must **never link to MOCs**
- Paper notes may link only to:
  - project notes (in `Projects/`)
  - other paper notes (in `Reading/`)
- **NO OTHER LINK TYPES ALLOWED** - no concepts, no methods, no techniques
- Bullet points only — no prose
- Aggressive `[[wiki linking]]` required **BUT ONLY** to projects/papers

---

## TEMPLATE COMPLIANCE (MANDATORY)

**BEFORE starting, read the template:**
1. Use the `view` tool to read `Templates/Paper Note.md`
2. Copy the EXACT structure including:
   - All emoji section headers (🧾, 🌍, ❓, 💡, etc.)
   - All subsection prompts (### questions)
   - All markdown formatting
3. Fill in content under each subsection prompt
4. Do NOT remove, rename, or flatten any sections

**Template location:** `Templates/Paper Note.md`

**Rules:**
- Keep ALL emojis exactly as shown in template
- Keep ALL section headings exactly as shown in template
- Keep ALL subsection prompts (### questions) exactly as shown
- Answer each subsection with bullet points below the prompt
- Do NOT remove or rename sections
- Do NOT flatten the structure
- Place project links ONLY in "Linked Research Projects" subsection
- Place paper links ONLY in "Connections to Other Work" subsections

---

## LINKING RULES (CRITICAL)

### ✅ ALLOWED Links in Paper Notes
1. `[[Project Name]]` - links to files in `Projects/`
2. `[[Paper Title]]` - links to influential papers
   - Link to papers even if they don't exist in vault yet (paper notes can be created later)
   - MUST use exact, full paper titles in Title Case
   - MUST format as wiki links with double brackets
   - Example: `[[Attention Is All You Need]]` not "Attention is all you need"
   - Example: `[[BERT: Pre-Training of Deep Bidirectional Transformers for Language Understanding]]`
   - Example of future paper link: `[[Representation Engineering - A Top-Down Approach to AI Transparency]]`

### ❌ FORBIDDEN Links in Paper Notes
- `[[Transformer Architecture]]` - this is a concept, NOT allowed
- `[[Attention Mechanism]]` - this is a technique, NOT allowed
- `[[Self-Supervised Learning]]` - this is a method, NOT allowed
- `[[BERT]]` - this is a model name, NOT allowed (unless it's a paper title)
- `[[Cross-Entropy Loss]]` - this is a concept, NOT allowed
- Any link that is not explicitly a project or paper

### How to Handle Technical Terms
**Do NOT link them.** Just write them as plain text.

Examples:
- ❌ "The paper uses `[[attention mechanisms]]`"
- ✅ "The paper uses attention mechanisms"
- ❌ "They employ `[[contrastive learning]]`"
- ✅ "They employ contrastive learning"

**Exception:** Only link if you're creating/referencing a PROJECT about that mechanism:
- ✅ "Uses attention mechanisms → `[[Scaling Laws for Attention Heads]]`" (project)

---

## Paper Access Rules

**When searching for papers online:**
1. **ALWAYS** try the arXiv HTML version first: `https://arxiv.org/html/[paper-id]`
2. If HTML is unavailable (404, missing, or incomplete), **download the TeX source**: `https://arxiv.org/src/[paper-id]`
   - The source is a `.tar.gz` archive — extract it and read the `.tex` files
   - Focus on the main `.tex` file (often `main.tex` or the largest `.tex` file)
   - Extract content from the TeX source as you would from HTML
3. **DO NOT** download PDFs — TeX source is always preferred over PDF
4. Only use PDFs as a last resort if neither HTML nor TeX source is available

---

## Workflow

### 0. Read the template FIRST
**MANDATORY FIRST STEP:**
```
Use view tool on: Templates/Paper Note.md
```
Study the structure before creating the paper note.

### 1. Create paper note
- File name: **exact paper title**
- if present in paper title, exchange `:` for `-`
- Location: `Reading/`
- **Copy template structure EXACTLY from `Templates/Paper Note.md`**
- Fill each section with bullet points under the subsection prompts
- **Do NOT remove subsection headings or prompts**
- **Link to existing projects immediately** in "Linked Research Projects"
- **Only propose new projects** - don't create them yet

### 2. Fill template sections
Answer each subsection prompt with bullet points:

**🌍 Background:** Answer both subsection prompts
**❓ Problem Statement:** Answer all three subsection prompts
**💡 Key Idea:** Answer all three subsection prompts
**🧭 High-Level Approach:** Describe method/framework
**🔬 Technical Details / Analysis:** Answer all three subsection prompts
**📊 Main Results / Observations:** List findings
**🧩 Interpretation:** Answer both subsection prompts
**⚠️ Limitations / Open Questions:** List items
**🔗 Connections to Other Work:** Fill three subsections with `[[Paper Title]]` wiki links
  - Link to ALL influential papers mentioned or referenced in the current paper
  - Link even if paper notes don't exist in vault yet (they will be added when those papers are read)
  - MUST use exact, full paper titles in Title Case
  - MUST format as wiki links: `[[Title]]` not plain text
  - Extract titles from paper references/citations when available
**🚀 Relevance for My Research:** Answer two prompts + add project links

**CRITICAL:** Write technical details as plain text. Do NOT create wiki links for concepts, methods, or techniques.

### 3. Identify existing projects and propose new ones

**Part A: Link to existing projects immediately**
- Search for existing projects in `Projects/` that relate to the paper
- Add links to these existing projects in the paper note under "Linked Research Projects"
- No user approval needed for linking to existing projects
- **Note:** Reciprocal links (project → paper) will be added in step 4

**Part B: Propose new projects (requires user approval)**

**CRITICAL: Ground proposals in the paper itself, not inferred extensions**

Extract ideas **directly from the paper's content**:
- Explicit open questions the paper identifies (e.g., "future work", "unclear", "remains to be seen")
- Limitations the authors acknowledge
- Unexplained observations or surprising results mentioned in the paper
- Assumptions stated but not tested
- Gaps the paper identifies in prior work
- Follow-up experiments the paper suggests

**DO NOT infer extensions beyond what the paper discusses.** If the paper doesn't mention it, don't propose it.

**Before creating ANY new project files:**
1. **Re-read the paper's "Limitations / Open Questions" section** you filled in step 2
2. For each open question or limitation that could be a standalone project:
   - Proposed project title (describes the idea, grounded in paper content)
   - Quote or paraphrase from the paper showing where this question/gap appears
   - 1-2 sentence description of what it would explore
   - Note if it's related to any existing project
3. **Use `AskUserQuestion` tool** to let the user select which projects to create:
   - Use `multiSelect: true` so the user can pick multiple projects
   - Each option: `label` = project title, `description` = 1-line summary of what it explores
   - Include a "None" option with description "Don't create any new projects"
   - Example:
     ```
     question: "Which projects should I create from this paper?"
     header: "Projects"
     multiSelect: true
     options:
       - label: "Project Title A", description: "Explores X based on paper's open question about Y"
       - label: "Project Title B", description: "Tests whether Z holds, motivated by limitation W"
       - label: "None", description: "Don't create any new projects"
     ```
4. Wait for user selection
5. Only create the selected projects (skip if "None" selected)

Project title examples:
- `Detecting Representation Drift During Fine-Tuning`
- `Preventing Emergent Misalignment via Gradient Monitoring`

For each approved new project:
- create a new file in `Projects/`
- use `Templates/Project.md` as template
- status: `seed`
- add **1–3 bullet points minimum**
- link the current paper under **Relevant Papers**

### 4. Create approved new projects and finalize bidirectional links

**After receiving user approval**, create the new project files:
- Create only the approved new projects in `Projects/`
- Use `Templates/Project.md` as template
- Fill with the descriptions you prepared
- Link the current paper under **Relevant Papers** in each project

**CRITICAL: Bidirectional linking for existing projects**

For **every project** linked from the paper note (both existing and newly created):
1. Open the project note in `Projects/`
2. Locate the **"Relevant Papers"** section
3. Add a wiki link to the paper note if it's not already there:
   - Format: `[[Paper Title]]` (the paper note file name)
   - Use Title Case with the exact paper title
   - Place it in the "Relevant Papers" section
4. Save the project note

This ensures the graph remains consistent: if paper → project link exists, then project → paper link must also exist.

Then update the paper note:
- Add newly created project links to **"Linked Research Projects"** (existing projects should already be linked from step 1)
- Ensure paper links in **"🔗 Connections to Other Work"** subsections are complete
- **CRITICAL:** Use exact paper title in Title Case when linking to papers
- **CRITICAL:** Format paper references as wiki links: `[[Paper Title]]` not plain text
- If you don't know the exact title, use a descriptive title in Title Case
- Examples:
  - ✅ `[[Sparse Autoencoders Find Highly Interpretable Features in Language Models]]`
  - ✅ `[[Concept Bottleneck Models]]`
  - ❌ "Bricken et al. 2023" (not a wiki link)
  - ❌ `[[sparse autoencoders]]` (not title case, too generic)

**VERIFY:** Every `[[link]]` in the paper note is either:
1. A file in `Projects/` (project note) - appears under "Linked Research Projects"
2. A paper title as wiki link - appears under "Connections to Other Work" as `[[Title Case Paper Title]]`
   - Paper notes may not exist in vault yet, but will be added when those papers are read
   - Use exact, full paper titles from references

### 5. Minimal quality check
Before finishing:
- **ALL template sections present with emojis**
- **ALL subsection prompts (### questions) present**
- Paper note contains **≥ 5 internal links** (ONLY to projects/papers)
- At least **one project note** created or reused
- No paragraph longer than 3 bullets
- **VERIFY: Every wiki link is to a file in `Projects/` or `Reading/`**
- No concept links (attention, transformers, etc.) - only plain text

### 6. Update maintenance counters
After completing the paper note (and any new projects):
1. Read `.claude/vault_maintanance.md`
2. Increment `papers_since_audit_links`, `papers_since_vault_index`, and `papers_since_validate_links` each by 1
3. If any **new** project files were created, increment `projects_since_audit_links` and `projects_since_vault_index` each by the number of new projects created
4. Write the updated values back to `.claude/vault_maintanance.md`

---

## Output Style
- bullet points only
- fragments preferred
- dense information
- no narrative text
- **preserve ALL template structure, emojis, and subsection prompts**
- **technical terms as plain text, NOT wiki links**
- links ONLY to projects (`Projects/`) or papers (`Reading/`)
- don't include `:` in file names. Exchange `:` always with `-`

---

## Goal
Convert reading into:
- explicit mechanisms
- reusable research ideas
- connected project graph
- long-term synthesis potential
- **properly structured notes following template exactly**

**Important workflow:**
- Link to existing projects immediately without asking
- Propose new projects and get user approval before creating them

A paper note without linked projects is considered incomplete.
A paper note that doesn't follow the template structure is considered invalid.

---

## Self-Check Before Completing

**Template structure:**
1. Did I read `Templates/Paper Note.md` first? ✅
2. Are ALL emoji section headers present? ✅
3. Are ALL subsection prompts (### questions) present? ✅
4. Did I answer each subsection separately? ✅

**Links:**
For EVERY `[[link]]` in the paper note:
1. Is this link pointing to a file in `Projects/`? ✅
2. Is this link pointing to a file in `Reading/`? ✅
3. Is this link a concept/method/technique? ❌ REMOVE
4. For paper links: Is it in Title Case with wiki link brackets? ✅
5. For paper links: Did I use the full paper title, not "Author et al."? ✅

**Bidirectional linking verification:**
1. For each project linked in the paper note:
   - Did I add/verify the reciprocal link from project → paper? ✅
   - Does the project's "Relevant Papers" section include this paper? ✅
2. All paper-project relationships are now bidirectional ✅

**If uncertain whether something should be a link:** Don't link it. Use plain text.

**Maintenance counters:**
1. Did I increment `papers_since_audit_links`, `papers_since_vault_index`, `papers_since_validate_links` in `.claude/vault_maintanance.md`? ✅
2. Did I increment `projects_since_audit_links` and `projects_since_vault_index` for each new project created? ✅
