---
name: create_project
description: Create atomic research project notes with minimal overhead
---

## 📋 Create Project Skill

Create new research project notes in `Projects/` with proper linking and structure.

---

## CRITICAL RULES

- Project notes live **only** in `Projects/`
- Use `Templates/Project.md` **exactly**
- Status must be: `seed | idea | active | writing | finished`
- Every project **must link to at least one MOC**
- Projects must link back to papers in "Relevant Papers"
- No orphan projects

---

## WORKFLOW

### 1. Get project details
Ask user for:
- **Project title** (one-line idea)
- **Status** (seed/idea/active/writing/finished)
- **MOC to link** (research area)
- **Related papers** (if any exist in `Reading/`)

### 2. Read template
```
Read: Templates/Project.md
```
Study the exact structure before creating.

### 3. Create project file

**File name:** Exact project title
**Location:** `Projects/`
**Template:** `Templates/Project.md` (copy EXACTLY)

### 4. Fill minimal sections

**Mandatory fields:**
- Seed Idea: 1-2 bullets
- Status: seed | idea | active | writing | finished
- Research Question: 1 bullet (what are we asking?)
- Hypothesis/Claim: 1 bullet (what's the answer?)

**Links:**
- Add MOC link in appropriate section
- Add paper links to "Relevant Papers" if papers exist

### 5. Verify structure
- All template sections present
- Status field filled correctly
- MOC link present
- No orphan projects

### 6. Update maintenance counters
1. Read `.claude/vault_maintanance.md`
2. Increment `projects_since_audit_links` and `projects_since_vault_index` each by 1
3. Write the updated values back to `.claude/vault_maintanance.md`

---

## OUTPUT RULES

- Ultra-concise bullets only
- Fragments OK
- No prose
- Clarity > grammar
- >5 bullets → split section

---

## SELF-CHECK

✅ Did I read `Templates/Project.md` first?
✅ Are ALL template sections present?
✅ Is status valid (seed|idea|active|writing|finished)?
✅ Does project link to exactly one MOC?
✅ Are paper links in Title Case with `[[brackets]]`?
✅ No orphan projects created?
✅ Did I increment `projects_since_audit_links` and `projects_since_vault_index` in `.claude/vault_maintanance.md`?
