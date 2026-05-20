---
description: Send specific files to OpenAI Codex CLI for an independent audit/review
allowed-tools: Bash(git:*), Bash(codex:*), Bash(cat:*), Bash(wc:*)
---

# Codex Direct File Audit

## Your Task

The user wants to audit specific files (not a git diff). They will provide file paths, or you should identify the relevant files from context.

1. Identify the files to audit. If the user provided paths, use those. Otherwise, determine the most relevant files from the conversation context.

2. Prepare a brief summary of what each file does and why it's being audited.

3. Run the following command, replacing `<FILE_PATHS>` with the space-separated list of files, and `<FILE_SUMMARY>` with a concise description of each file's purpose:

```
codex exec -m "gpt-5.4" -c 'model_reasoning_effort="xhigh"' -c 'service_tier="fast"' --dangerously-bypass-approvals-and-sandbox -C "$(pwd)" "You are a READ-ONLY code reviewer. Read and review the following files: <FILE_PATHS>. Review them for: bugs, security issues, performance problems, logic errors, and style concerns. Be specific about file names and line numbers. You may read other files in the repo and run tests to verify your findings. SAFETY RULES: Do NOT delete files, edit existing files, change branches, checkout, reset, revert, amend, or undo commits. Do NOT run git push, git checkout, git reset, git clean, rm, or any destructive command. You may create temporary files if needed for debugging. Your job is strictly to READ and REPORT. Do a deep audit and think from first principles. Leave no question unanswered. Here is context about the files: <FILE_SUMMARY>"
```

4. **Validate every finding before presenting it.** The auditor (Codex) operates with limited context. It does not know the project's vision, strategic goals, or architectural rationale. It will often invent critical issues that are misunderstandings, or overstate the severity of things that are intentional design choices. For each finding Codex returns, you MUST:
   - Check the actual source code to confirm the issue is real, not a hallucination or misread.
   - Check any local strategic/planning documents (e.g. `agents.md`, `README.md`, `CLAUDE.md`, `current_*.md`, or similar docs in the repo or in a /doc/ folder `DEV_JOURNAL.md` etc) to see if the finding conflicts with the stated project intent.
   - Ask yourself: "Is this a real bug, or is Codex misunderstanding the context?" and "Even if real, is this meaningful or is it trivial/stylistic noise?"
   - If there are findings that are not both real AND meaningful, share them with the user but clearly label them and with your reasons why.

5. Present the validated findings to the user. For each one, briefly note why you believe it's legitimate. If Codex gave the all-clear, or if all findings failed validation, say so.

6. Ask the user if they'd like to address any of the validated feedback.
