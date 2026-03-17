---
name: update_moc
description: Manage research area hubs (MOCs) with lean, project-focused organization
---

## 🗺️ Update MOC Skill

Maintain research area MOCs (`MOCs/`) by adding/removing project links and canonical papers.

---

## CRITICAL RULES

- MOC notes live **only** in `MOCs/`
- MOCs organize **projects** (primary content)
- MOCs may link to **canonical/survey papers ONLY**
- **NO paper dumping** - exhaustive lists forbidden
- Papers appear in MOC only if:
  - Foundational/canonical for the field
  - Survey or taxonomy paper
  - Motivated multiple projects
- If paper is relevant through only ONE project → do not add to MOC

---

## WORKFLOW

### 1. Get MOC details
Ask user for:
- **MOC name** (research area to update)
- **Action:** Add projects? Add canonical papers? Remove items?
- **Items to add/remove** (project or paper names)

### 2. Identify target MOC file
**Location:** `MOCs/[MOC Name].md`
**Find by:** Search vault index or grep for MOC name

### 3. Validate before changes

For **projects to add:**
- Verify project exists in `Projects/`
- Verify project is NOT already in MOC
- Verify project links to this MOC (bidirectional)

For **papers to add:**
- Verify paper is foundational/canonical/survey
- Verify paper is NOT already in MOC
- Verify paper motivated multiple projects (or is canonical)

### 4. Update MOC
- Add project links in Projects section: `[[Project Name]]`
- Add paper links in Papers section (if canonical): `[[Paper Title]]`
- Maintain alphabetical or logical order
- Remove deprecated projects/papers

### 5. Verify bidirectional links
For **each added project:**
- Open project file in `Projects/`
- Verify project links to this MOC
- If missing → notify user to add MOC link to project

For **each added paper:**
- Verify paper does NOT link directly to MOC (forbidden)
- Paper links only to projects

---

## OUTPUT RULES

- Bullet points only
- Fragments preferred
- No prose
- Clear structure
- Each section ≤5 bullets

---

## SELF-CHECK

✅ Did I verify all items exist before adding?
✅ Are project links properly formatted: `[[Project Name]]`?
✅ Are paper links in Title Case: `[[Paper Title]]`?
✅ Did I check bidirectional project linking?
✅ Did I verify no forbidden paper→MOC links?
✅ Did I verify no paper dumping (only canonical papers)?
✅ MOC structure remains lean?
