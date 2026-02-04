---
name: treido-verify
description: "Treido QA/verification runner. Runs gates, sanity-checks rails, and selects the smallest relevant tests. Trigger: VERIFY"
---

# Treido Verify (QA)

Read-only: **do not patch files** and **do not edit** `TASKS.md` or `audit/*`. Return a report only.

You are the verification pass after implementation. Prefer **small, fast signals** before broader tests.

## Gates (Always)

```bash
pnpm -s typecheck
pnpm -s lint
pnpm -s styles:gate
```

## Audit / Plan Lint (Optional, Read-only)

Use these checks to validate that the merged audit + plan are internally consistent (heuristics; report issues to the orchestrator).

```bash
# audit ID lint (duplicates / format) — pass the audit file path explicitly
node -e "const fs=require('fs');const p=process.argv[1];const s=fs.readFileSync(p,'utf8');const ids=[...s.matchAll(/\\|\\s*([A-Z0-9]+-\\d{3})\\s*\\|/g)].map(m=>m[1]);const dup=[...new Set(ids.filter((id,i,a)=>a.indexOf(id)!==i))];const bad=[...new Set(ids.filter(id=>!/^[A-Z0-9]+-\\d{3}$/.test(id)))];console.log('IDs:',ids.length);if(dup.length)console.log('Duplicate IDs:',dup.join(', '));if(bad.length)console.log('Bad IDs:',bad.join(', '));if(!dup.length&&!bad.length)console.log('OK');" audit/YYYY-MM-DD_context.md

# TASKS.md lint (required fields per task) — heuristic: checks the next few lines after each task bullet
node -e "const fs=require('fs');const s=fs.readFileSync('TASKS.md','utf8');const lines=s.split(/\\r?\\n/);let bad=0;for(let i=0;i<lines.length;i++){if(!/^- \\[[ xX]\\] /.test(lines[i]))continue;let j=i+1,look=0,blk=[];for(;j<lines.length && look<14;j++,look++){if(/^- \\[[ xX]\\] /.test(lines[j])||/^###\\s+/.test(lines[j]))break;blk.push(lines[j]);}const t=blk.join('\\n');const miss=[];if(!/\\bOwner:\\b/.test(t))miss.push('Owner');if(!/\\bVerify:\\b/.test(t))miss.push('Verify');if(!/\\bFiles:\\b/.test(t))miss.push('Files');if(miss.length){bad++;console.log('Task missing',miss.join('/'),':',lines[i]);}}if(!bad)console.log('OK');"
```

## Rail Checks (Fast Heuristics)

```bash
# logging / PII risks
rg -n "\\b(console\\.log|console\\.debug|console\\.info)\\b" app components lib

# i18n drift (rough)
rg -n "\\b([A-Z][a-z]+ ){2,}" app components --glob '*.tsx'

# cached-server hazards
rg -n "'use cache'|\\b(cookies|headers)\\(" app lib --glob '*.ts' --glob '*.tsx'

# Supabase hot-path smell
rg -n "select\\(\\s*\\*\\s*\\)" app lib --glob '*.ts' --glob '*.tsx'
```

## Tests (Risk-based)

- UI-only: `pnpm -s test:unit`
- Auth/payments/checkout/webhooks: `REUSE_EXISTING_SERVER=true pnpm -s test:e2e:smoke`

## Output

- Report which gates/tests ran and their result.
- If you ran lint checks: report any duplicate/bad IDs and any task blocks missing required fields.
- If failures: point to the minimal file(s)/task ID(s) to fix next.
