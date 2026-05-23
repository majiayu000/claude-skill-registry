---
name: roadmap-updating
description: Use when updating product roadmap with new PRDs - sequences PRDs by timeline, manages roadmap.md structure, and maintains changelog
---

# Roadmap Updating

## Purpose

Update roadmap with newly validated PRDs:
- Sequence by timeline and status
- Organize by timeframe (Now/Next/Later)
- Maintain roadmap.md structure
- Create changelog snapshots

## When to Use

Activate when:
- User invokes `/project:update-roadmap`
- After product-planning generates PRDs
- After interactive PRD creation
- Manual roadmap review cycles

## Workflow

### 1. Load PRDs

**From:**
- `datasets/product/backlog.md` (latest PRD Intake section)
- `datasets/product/prds/{YYYY}/PRD_*.md` files

**Extract:**
- PRD titles
- Status (🚧 Drafting / 🏃 Actionable / 🔒 Closed / ❗ Abandoned)
- Timeline (milestones and expected delivery)

### 2. Sequence by Timeline

**Sort PRDs by:**
- Actionable PRDs first (ready for work)
- Then by expected delivery timeline
- Drafting PRDs listed separately (need completion)

**Timeframes:**
- Now: Actionable PRDs with near-term delivery (this quarter)
- Next: Actionable PRDs with mid-term delivery (next quarter)
- Later: Actionable PRDs with future delivery or Drafting status

### 3. Update Roadmap Structure

**roadmap.md format:**
```markdown
# Product Roadmap

**Last Updated**: YYYY-MM-DD

## Now (This Quarter)
- [ ] PRD 1 Title - 🏃 Actionable - {Expected Delivery}
- [ ] PRD 2 Title - 🏃 Actionable - {Expected Delivery}

## Next (Next Quarter)
- [ ] PRD 3 Title - 🏃 Actionable - {Expected Delivery}
- [ ] PRD 4 Title - 🏃 Actionable - {Expected Delivery}

## Later (Future / Drafting)
- [ ] PRD 5 Title - 🚧 Drafting - {Timeline TBD}
- [ ] PRD 6 Title - 🏃 Actionable - {Expected Delivery Q3+}

## Closed (Completed)
- [x] PRD 7 Title - 🔒 Closed - {Delivered Date}
```

### 4. Create Changelog Snapshot

**Before updating roadmap.md:**
```bash
cp datasets/product/roadmap.md datasets/product/snapshots/ROADMAP_{YYYY-MM-DD}.md
```

## Success Criteria

- PRDs sequenced by timeline
- Roadmap.md updated with correct structure
- Changelog snapshot created
- Last Updated timestamp current

## Related Skills

- `product-planning`: Generates PRDs for roadmap
- `prd-creation`: Creates individual PRDs
- `prd-validation`: Validates PRD quality
