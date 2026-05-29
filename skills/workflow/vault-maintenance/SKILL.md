---
name: vault_maintenance
description: Run all vault maintenance skills in sequence - audit_links, update_vault_index, validate_paper_links
---

## 🛠️ Vault Maintenance Skill

Run all three maintenance skills in sequence, collecting fixes and approvals as they arise.

---

## WORKFLOW

### 1. Check maintenance counters
Read `.claude/vault_maintanance.md` and report current counter values before starting.

### 2. Run skills in order

Execute each skill **fully** before moving to the next. Follow each skill's own SKILL.md exactly:

1. **`/audit_links`** — validate graph structure (orphans, broken bidirectional links, forbidden concept links)
2. **`/update_vault_index`** — sync vault_index.md with current vault state
3. **`/validate_paper_links`** — validate paper note links against actual paper references

Each skill:
- Does its own incremental scan (uses its own timestamp)
- Presents its own findings
- Gets its own user approval for fixes
- Updates its own counters and timestamps in `vault_maintanance.md`

### 3. Final summary

After all three skills complete, print a compact summary:

```
✅ audit_links — [N issues found, N fixed]
✅ update_vault_index — [N projects added/removed]
✅ validate_paper_links — [N links validated, N removed]
```

---

## RULES

- **Do not skip a skill** even if it reports nothing to do
- **Each skill runs independently** — failures or "nothing to do" in one skill do not block others
- **Never batch fixes across skills** — each skill presents and gets approval for its own fixes separately
- Follow each skill's CRITICAL RULES and OUTPUT RULES exactly
- All three `vault_maintanance.md` timestamps and counters are reset by the individual skills — do not reset them again after the fact

---

## SELF-CHECK

✅ Did I run all three skills in order (audit → index → validate)?
✅ Did each skill update its own timestamp and counters?
✅ Did I print the final summary?
