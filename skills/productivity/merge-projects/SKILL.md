---
name: merge_projects
description: Identify overlapping projects and merge them into consolidated notes
---

## 🔀 Merge Projects Skill

Detect overlapping or closely related projects and merge them into a single consolidated project note.

---

## CRITICAL RULES

- **Never merge automatically** — always present candidates and get user approval
- **Never delete source projects** until merged project is verified
- Merged project inherits the **highest status** of its sources (seed < idea < active < writing < finished)
- All paper links from source projects **must be preserved** in merged project
- All MOC links from source projects **must be preserved** in merged project
- Bidirectional links must be updated: papers that linked to old projects must link to merged project
- Vault index must be updated after merge

---

## WORKFLOW

### 1. Choose mode
Ask user:
- **Scan for candidates?** (analyze all projects for overlap)
- **Merge specific projects?** (user names 2-3 projects to merge)

---

### 2a. Scan mode — Identify merge candidates

**Read vault index** to get all projects and their descriptions.

**For each project pair, assess overlap signals:**
- Similar research questions or hypotheses
- Shared relevant papers (≥2 papers in common)
- Overlapping MOC links
- Complementary seed ideas (one project's approach is another's variant)
- Same phenomenon studied from slightly different angles

**Score overlap:**
- 🔴 High overlap (likely should merge): same core question, ≥3 shared papers, nearly identical hypotheses
- 🟡 Moderate overlap (consider merging): related questions, 2 shared papers, one could be a variant of the other
- 🟢 Low overlap (keep separate): distinct questions, ≤1 shared paper, different mechanisms

**Present candidates grouped by overlap score.**
For each candidate pair/group:
- List the projects
- Explain WHY they overlap (shared papers, similar questions, etc.)
- Suggest which project should be the "primary" (the more developed one)
- Suggest a merged title if current titles are too narrow

**Get user approval** before proceeding to merge.

---

### 2b. Direct merge mode — User specifies projects

- Read all specified project files in full
- Confirm overlap is real
- Ask user which should be primary (or suggest based on development level)
- Proceed to merge

---

### 3. Execute merge

**Create merged project:**
- Use the primary project as base
- Integrate content from secondary project(s) section by section:

| Section | Merge strategy |
|---|---|
| Current Focus | Keep primary's; note secondary's angle if distinct |
| Seed Idea | Combine triggers from all sources |
| Current Working Idea | Synthesize into broader framing |
| Research Question | Merge into unified question; keep sub-questions if distinct |
| Hypothesis / Claim | Keep primary; add secondary as alternative hypothesis if different |
| Context & Motivation | Union of all motivations |
| Possible Approaches | Union of all approaches (deduplicate) |
| Research Ideas & Variants | Secondary project's main direction becomes a variant |
| Related Work | Union (deduplicate) |
| Relationship to Prior Work | Union (deduplicate) |
| Possible Experiments | Union (deduplicate) |
| Open Questions & Risks | Union (deduplicate) |
| Next Actions | Union; remove completed/redundant |
| Relevant Papers | Union of ALL paper links (no paper lost) |

**Decide on merged title:**
- If primary title is broad enough → keep it
- If both titles are narrow → create new title capturing combined scope
- Title must be concise and descriptive

**Set merged status:**
- Use highest status among source projects
- If any source is `active` or higher → merged project inherits that status

---

### 4. Update all references

**Papers linking to absorbed projects:**
- Find all papers in `Reading/` that link to secondary (absorbed) project(s)
- Replace `[[Old Project Name]]` with `[[Merged Project Name]]` in their "Linked Research Projects" section

**MOCs containing absorbed projects:**
- Find MOCs listing secondary project(s)
- Replace with merged project link (avoid duplicates if primary already listed)

**Projects referencing absorbed projects:**
- Check if any other projects reference the absorbed ones in Related Work
- Update those references

---

### 5. Remove absorbed projects

**Only after verification:**
- Confirm merged project file exists and is complete
- Confirm all paper links updated
- Confirm all MOC links updated
- Confirm no remaining references to old project names

**Then delete** secondary (absorbed) project files.

---

### 6. Update vault index

- Run update_vault_index logic or notify user to run `/update_vault_index`

---

## TOKEN EFFICIENCY

**Optimizations:**
- In scan mode: read only vault index + project frontmatter + Relevant Papers sections first
- Only read full project files for confirmed merge candidates
- Use grep to find references to absorbed project names across vault
- Batch reference updates per file

**Avoid:**
- Reading all project files in full during scan phase
- Reading paper files unless needed for reference updates
- Multiple passes over same files

---

## OUTPUT RULES

- Scan results: table of candidate pairs with overlap score + rationale
- Merge summary: before/after comparison (projects consolidated, papers preserved, links updated)
- Bullets only, no prose
- Confirm paper count preserved: "X papers linked before → X papers linked after"

---

## SELF-CHECK

✅ Did I get user approval before merging?
✅ Are ALL paper links from source projects preserved in merged project?
✅ Are ALL MOC links preserved?
✅ Did I update paper notes that linked to absorbed projects?
✅ Did I update MOCs that listed absorbed projects?
✅ Did I check for references to absorbed projects in other project files?
✅ Is the merged project status correct (highest of sources)?
✅ Did I delete absorbed project files only after full verification?
✅ Is the vault index updated or user notified to update?
✅ No orphan references remain to deleted project names?
