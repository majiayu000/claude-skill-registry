---
name: localsetup-framework-compliance
description: "Pre-task workflow, certainty assessment, context load, document status, testing, Git checkpoints, document maintenance. Use for framework modifications, PRDs, or any task that must follow checklist and checkpoints."
metadata:
  version: "1.2"
---

# Framework compliance (pre-task, checkpoints, document maintenance)

## 0. MANDATORY PRE-TASK WORKFLOW (CRITICAL)

Before executing ANY task:

1. **IDENTIFY TASK TYPE**  - file_creation, code_modification, framework_modification, git_operation, etc.
2. **CHECK CORE RULES** (BLOCKS EXECUTION IF VIOLATED): Engine/user data separation; Git checkpoints after framework modifications; Markdown compatibility; Testing after changes; Backup management.
3. **ASSESS CERTAINTY**  - HIGH/MEDIUM/LOW/CRITICAL LOW; if &lt;70% lookup docs; if &lt;50% on core rules get user confirmation.
4. **PRE-EXECUTION CHECKLIST**  - Use `source lib/rule_enforcer_enhanced.sh && pre_execution_checklist "$task_type" "$task_description"` (when available).
5. **EXECUTE TASK** with rule compliance monitoring.
6. **POST-EXECUTION VERIFICATION**  - Use `post_execution_verification "$task_type" "$task_context"`; verify checkpoints and backups.

**Documentation lookup:** Check _localsetup/docs/, your platform's rules path (e.g. .cursor/rules/ on Cursor), _localsetup/config/rules_index.yaml. Never proceed with CRITICAL LOW certainty on core rules without user confirmation.

## 1. Context load and repo role

- **VERIFY:** Context is loaded. If unsure, ask user to run `./_localsetup/tools/verify_context`.
- **Repo role:** Framework lives in client repo at _localsetup/. Only modify local context (e.g. your platform's local rules, such as .cursor/rules/local-*.mdc on Cursor) or propose changes via PRD. See [REPO_AND_DATA_SEPARATION.md](../../docs/REPO_AND_DATA_SEPARATION.md).

## 6. Document status and testing

- **Document status:** Before referencing any document, check status (ACTIVE/PROPOSAL/DRAFT/DEPRECATED/ARCHIVED). If PROPOSAL, do not assume implemented. Use `check_document_status()` or _localsetup/docs/DOCUMENT_INDEX.yaml.
- **Testing:** Run _localsetup/tests/automated_test.sh after changes; maintain 100% test pass rate.

## 14. Git checkpoints (CRITICAL)

- **MANDATORY:** Create Git checkpoints IMMEDIATELY after framework modifications. Use `_localsetup/tools/verify_rules` to verify.
- **Checkpoint creation:** Stage and commit with messages like "Checkpoint: <operation> - <description>". Never commit user/repo-local data that should stay private.
- **Rollback:** `git reset --hard <commit-hash>` (with confirmation). List: `git log --oneline`.

## 16. Document maintenance after major task

- **Trigger:** After major task completion, user validation, and Git commit.
- **Workflow:** Document scrub first (update _localsetup/docs/ that reference the task), then create workflow docs if needed. Use `lib/document_maintenance.sh` when available.
- **Major task:** Framework modifications, new tools, new features, significant config changes. Not: simple bug fixes, test-only changes.
