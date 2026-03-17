---
name: localsetup-public-repo-identity
description: "Public repo identity – use in README and published repos. For your identity, use local-identity (gitignored) or copy from framework template. Use when editing README*, CONTRIBUTING*."
metadata:
  version: "1.2"
---

# Public repo identity (stub)

Use a **local identity file** or the **framework template** so the framework repo stays generic (no PII).

- **This repo (machine):** Use your platform's rules path for a local identity file (e.g. `.cursor/rules/local-identity.mdc` on Cursor) with your real name and org. That file is gitignored; your platform loads it. Keep this stub so the rule is still referenced; the actual identity comes from the local-identity file.
- **Framework template:** Copy from `_localsetup/config/templates/public-repo-identity.template.mdc`, fill in placeholders, and save as local-identity.mdc or use in another repo.

Do not put real names, contact info, or org details in this file; they belong in local-identity.mdc (not committed).
