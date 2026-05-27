---
name: core
description: prd.json schema and task system - auto-loaded when prd.json exists
allowed-tools: Read, Write, Edit, TaskCreate, TaskUpdate, TaskList, Grep, Glob
model: opus
user-invocable: false
disable-model-invocation: true
---

# Hybrid Task System

## Sprint Summary
!`node -e "try{const p=require('./prd.json');const sp=p.sprints?p.sprints[p.sprints.length-1]:p;const s=Object.values(sp.stories||p.stories||{});const name=sp.id||sp.name||p.sprint||'unknown';const done=s.filter(x=>x.passes===true).length;const pending=s.filter(x=>x.passes===null||x.passes===false).length;const deferred=s.filter(x=>x.passes==='deferred').length;console.log('Sprint:',name,'| Done:',done,'| Pending:',pending,'| Deferred:',deferred,'| Total:',s.length)}catch(e){console.log('No prd.json')}"`

Do not read the full prd.json into context. Use `Grep` to find specific stories or `Read` with offset/limit for targeted sections.

## When to Sprint

- **5+ related tasks** — create a sprint in prd.json
- **< 5 tasks or single fixes** — work directly, no sprint or stories needed
- **Design/creative work** — iterate freely, skip planning overhead
- **Quick fixes** — just fix, verify, done

Sprints are for tracking, not for ceremony. If the work is small, skip the overhead.

## Two Layers

| Layer | Tool | Purpose |
|-------|------|---------|
| Long-term | prd.json | Sprint history, resolutions (Git-tracked) |
| Short-term | Native Tasks | Active work (session only) |

Work with native Tasks during session, batch-update prd.json at end.

## prd.json Story Schema

```json
{
  "id": "S26-001",
  "title": "Fix tooltip clipping",
  "priority": 1,
  "passes": null,
  "type": "fix",
  "category": "components",
  "notes": "",
  "resolution": ""
}
```

| Field | Values |
|-------|--------|
| `passes` | `null` (pending), `true` (done), `false` (failed), `"deferred"` |
| `type` | fix, feature, refactor, qa, perf |
| `priority` | 0=critical, 1=high, 2=medium, 3=low |
| `resolution` | HOW it was fixed (learning) |

## Resolution Learning

When completing bug fixes, document HOW:

```
[PATTERN]: [SPECIFIC FIX]
```

Examples:
- `null-check: Added optional chaining at line 45`
- `missing-import: Added import for DateRange`
- `type-mismatch: Changed Record<string, T> to Partial<Record<K, T>>`
- `overflow: Added max-h + overflow-auto`

## Context Optimization

| Action | Do This |
|--------|---------|
| Check status | Read prd.json header (30 lines) |
| Start task | Grep specific story |
| Track progress | Native TaskUpdate |
| Complete work | Batch edit prd.json at session end |

## Archive Trigger

When 4+ total sprints exist, or prd.json > 500 lines, or prd.json > 50KB:
- Suggest `archive` before starting work
- Archive keeps only last 3 sprints active
- Completed stories move to `.claude/archives/prd-archive-YYYY-MM.json`
