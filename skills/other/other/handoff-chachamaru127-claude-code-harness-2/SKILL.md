---
name: handoff
description: "PMへの完了報告やエージェント間バトンタッチ。スムーズな引き継ぎを実現。Use when user mentions '/handoff', completion report, handoff to Cursor/OpenCode, auto-fix, or reporting to PM. Do NOT load for: casual completion statements, progress chat, informal status updates."
description-en: "Completion report to PM and agent handoff. Smooth transition achieved. Use when user mentions '/handoff', completion report, handoff to Cursor/OpenCode, auto-fix, or reporting to PM. Do NOT load for: casual completion statements, progress chat, informal status updates."
description-ja: "PMへの完了報告やエージェント間バトンタッチ。スムーズな引き継ぎを実現。Use when user mentions '/handoff', completion report, handoff to Cursor/OpenCode, auto-fix, or reporting to PM. Do NOT load for: casual completion statements, progress chat, informal status updates."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
argument-hint: "[cursor|opencode|auto-fix]"
---

# Handoff Skill

PM-実装役間のハンドオフとワークフロー遷移を管理するスキル。

## 機能詳細

| 機能 | 詳細 |
|------|------|
| **PM→実装役** | See [references/handoff-to-impl.md](references/handoff-to-impl.md) |
| **実装役→PM** | See [references/handoff-to-pm.md](references/handoff-to-pm.md) |
| **レビュー指摘自動修正** | See [references/auto-fixing.md](references/auto-fixing.md) |
| **コミット実行** | See [references/execute-commit.md](references/execute-commit.md) |

## Quick Reference

- "**Cursor に完了報告を書いて**" → `/handoff cursor`
- "**OpenCode にハンドオフ**" → `/handoff opencode`
- "**レビュー指摘を自動修正**" → `/handoff auto-fix`
- "**変更内容とテスト結果を含めて**" → Includes git diff and test results

## Prerequisites

> **This command should only run after harness-review APPROVE**

| Condition | Required | Check Method |
|-----------|----------|--------------|
| harness-review completed | Yes | Review result is APPROVE |
| No Critical/High issues | Yes | All fixed |
| Implementation complete | Yes | Plans.md tasks completed |

**Why handoff requires review approval:**
- PM receives unreviewed changes otherwise
- Quality not assured
- Breaks `/work` flow (implement → review → fix → OK → handoff)

## Usage

```bash
/handoff cursor     # Handoff to Cursor
/handoff opencode   # Handoff to OpenCode
```

---

## Execution Flow

### Step 1: Identify Completed Tasks

- Check Plans.md checkboxes
- Summarize work done

### Step 2: Update Plans.md

```markdown
# Before
- [ ] Task name `pm:依頼中`

# After
- [x] Task name `cc:完了` (YYYY-MM-DD)
```

### Step 3: Gather Changes

```bash
git status -sb
git diff --stat
```

### Step 4: Check CI/CD (if applicable)

```bash
gh run list --limit 3
```

### Step 4.5: Unified Memory Finalize（必須）

完了報告の前に、共通メモリへ最終状態を確定する:

```text
harness_mem_record_checkpoint(session_id, title, content, tags?, privacy_tags?)
harness_mem_finalize_session(session_id, summary_mode="standard")
```

これにより Claude Code / Codex / OpenCode のどこからでも同一セッションを再開できる。
`session_id` は `$CLAUDE_SESSION_ID` → `.claude/state/session.json` の `.session_id` の順で取得する。
`harness_mem_sessions_list(project, limit=1)` の先頭利用は read-only（resume確認）に限定し、handoff時の `record_checkpoint` / `finalize_session` では明示 `session_id` が無い場合に失敗扱いとする。
`harness_mem_finalize_session` が失敗している場合は handoff を確定しない。

### Step 5: Generate Report

## Output Format

```markdown
## Completion Report

### Summary
- (1-3 lines describing what was done)

### Completed Tasks
- **Task Name**: [Task description]

### Changed Files
| File | Changes |
|------|---------|
| `path/to/file1` | [Summary] |
| `path/to/file2` | [Summary] |

### Verification Results
- [x] Build success
- [x] Tests passed
- [x] Manual verification complete

### Risks / Notes
- (If any)

### Next Actions (for PM)
1. [ ] [What PM should do next]
2. [ ] [Optional items]
```

---

## /work Integration Flow

```
/work execution
    ↓
Phase 1: Parallel implementation
    ↓
Phase 2: harness-review loop
    ├── NG (Critical/High) → Fix → Re-review
    └── OK (APPROVE) → Phase 3
    ↓
Phase 3: Auto-commit (if configured)
    ↓
Phase 4: This skill runs ← First time handoff happens
```

> `/work` automatically calls this skill in Phase 4.
> When running manually, always do so after harness-review APPROVE.

---

## Target-Specific Notes

### Handoff to Cursor

- Plans.md markers use `cc:完了` (Japanese)
- Report format optimized for Cursor PM workflow
- Includes context for `/review-cc-work` command

### Handoff to OpenCode

- Similar format to Cursor
- Compatible with OpenCode's command structure
- Works with multi-LLM development workflow

## Related Skills

- `work` - Main implementation workflow
- `harness-review` - Code review
- `setup` - Project setup (includes 2-Agent workflow)
