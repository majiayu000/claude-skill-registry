---
name: claude-code-tool-patterns
description: "Use when writing large files (>1000 lines), editing after many operations, or configuring hooks in Claude Code."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Claude Code Tool Patterns & Gotchas

**Extracted:** 2026-02-09 (consolidated 2026-02-10)
**Context:** Claude Code のツール使用時に発生しがちな問題とその回避策

---

## 1. Large File Write Performance

### Problem

Very large files (>3000 lines) in a single Write tool call become extremely slow and may appear to hang.

**Symptoms:**
- Write operation takes >60 seconds
- User interrupts thinking it's stuck
- No feedback on progress

### Solution

**Split large files into modular components:**

1. Identify logical boundaries (chapters, sections, domains)
2. Create multiple focused files (200-800 lines each)
3. Add navigation file (README/index) to tie them together
4. Write files in parallel when possible

```
# BAD: Single monolithic file
/docs/architecture.md (4000 lines) → 90+ seconds

# GOOD: Modular files
/docs/architecture/
├── README.md (200 lines)
├── 00-overview.md (600 lines)
├── 01-adr-backend.md (500 lines)
└── ...
→ Each write completes in ~5-10 seconds
```

---

## 2. File Edit Refresh Pattern

### Problem

Edit tool fails with "File has been modified since read" when file state has changed since last Read.

### Solution

**Always Read immediately before Edit:**

```
# BAD: Edit without recent Read
- Earlier: Read file.py
- (Multiple other operations)
- Later: Edit file.py  # May fail

# GOOD: Read immediately before Edit
- Earlier: Read file.py
- (Multiple other operations)
- Later: Read file.py   # Refresh state
- Then: Edit file.py    # Safe to edit
```

### When to Apply

- Before every Edit call in sessions with multiple file operations
- After file state might have changed through other tools
- In long-running sessions (context near limits)
- When you see "File has been modified" errors

---

## 3. Hook Command JSON Escape Trap

### Problem

settings.json の hooks にシェルコマンドを直接書くと、`\"`, `$`, `\n` などの
特殊文字が JSON パースエラー（"Bad control character in string literal"）を引き起こす。

### Solution

**外部スクリプトファイルに切り出す:**

```bash
# ~/.claude/hooks/my-hook.sh
#!/bin/bash
file=$(jq -r '.tool_input.file_path // empty')
if [ -n "$file" ] && echo "$file" | grep -q '\.py$'; then
  ruff format "$file" 2>/dev/null
fi
exit 0
```

```json
// settings.json — シンプルなコマンドだけを記述
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "bash ~/.claude/hooks/my-hook.sh"
      }]
    }]
  }
}
```

### When to Apply

- Hook コマンドに引用符、変数展開、パイプ、条件分岐が含まれる場合
- settings.json の JSON validation エラーが出た場合

---

## When to Use

- Planning to write a file >1000 lines
- Editing files after many intervening tool calls
- In complex multi-step workflows with frequent file operations
- Hook に複雑なシェルコマンドを設定する場合
