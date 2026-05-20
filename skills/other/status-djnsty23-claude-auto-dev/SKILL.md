---
name: status
description: Shows sprint progress and task status. Use 'progress' (not 'status' - that's a built-in).
triggers:
  - progress
allowed-tools: Read, TaskList
model: opus
user-invocable: true
---

# Status

Show current progress with minimal token usage.

## Sprint Data
!`node -e "try{const p=require('./prd.json');const sp=p.sprints?p.sprints[p.sprints.length-1]:p;const s=Object.values(sp.stories||p.stories||{});const name=sp.id||sp.name||p.sprint||'unknown';console.log('Project:',p.project||p.projectName||'unknown','| Sprint:',name);console.log('Done:',s.filter(x=>x.passes===true).length,'| Pending:',s.filter(x=>x.passes===null||x.passes===false).length,'| Deferred:',s.filter(x=>x.passes==='deferred').length)}catch(e){console.log('No prd.json found')}"`

## Process

1. Call `TaskList` to get all native tasks
2. Read `prd.json` header (first 20 lines) if exists
3. Display:

```
[projectName] | Sprint: [sprint]
═══════════════════════════════
Progress: [N]/[N] complete
In Progress: [N] | Ready: [N] | Blocked: [N]

Active:
  → [id] [subject] (in_progress)

Next:
  [id] [subject] (pending)
  [id] [subject] (pending)
```

## Rules
- Use TaskList for native tasks (primary)
- Read only prd.json header for context (not full file)

- If no prd.json, just show TaskList results
