---
name: iso-24495-text-audit
description: Audit user-selected Markdown or text files for deterministic plain-language findings. Use only when the user explicitly invokes this skill.
disable-model-invocation: true
argument-hint: "[file-or-directory]"
metadata:
  version: "0.5.0"
---

# ISO 24495 Text Audit

Audit only the path the user selects. Report mechanical findings so the user can decide whether the text suits its readers and purpose.

## Workflow

1. Read the path from `$ARGUMENTS`. Ask for a path when none was supplied.
2. Resolve the audit script relative to this `SKILL.md` file.
3. State the selected file or directory before running the script.
4. Treat an explicitly supplied directory as approval to read that directory.
5. Ask before expanding the audit beyond the supplied path.
6. Run the script with Bun:

```text
bun <skill-directory>/scripts/audit-text-cli.ts <file-or-directory> --project-dir <project-directory>
```

7. Report every finding with its file, line, rule, and explanation.
8. Report skipped or unreadable entries. Never treat an incomplete audit as clean.
9. Explain that findings are mechanical proxies, not an ISO judgement.
10. Leave the final decision and any rewriting request to the user.

## Boundaries

- Read `.md`, `.markdown`, and `.txt` files only.
- Do not follow a selected or nested symbolic link or directory junction. Report each one as skipped.
- Do not alter the selected text unless the user separately requests changes.
- Do not create a report file unless the user requests one and names its location.
- Do not describe zero findings as proof that text is valid, compliant, or suitable.
- Use the relevant sector skill when interpreting findings in legal, technical, scientific, or designed documents.
