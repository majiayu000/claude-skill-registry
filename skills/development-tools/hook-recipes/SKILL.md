---
name: hook-recipes
description: >
  Ready-to-use hook recipes for common Claude Code automation: prettier on edit,
  tsc check, console.log warning, git push review, doc blocker. Use when the user
  wants a specific hook example, asks "how do I auto-format" or "block markdown creation",
  or needs a hook for a common development workflow.
---

# Hook Recipes

A collection of battle-tested hook configurations for Claude Code. Copy these directly into `~/.claude/settings.json` under the `hooks` key.

## When to Use
- User asks for a specific hook recipe or example
- User wants to auto-format code after edits
- User wants to block certain file types from being created
- User wants warnings about console.log, TODO, or debug statements
- User needs a git push review gate
- User asks "how do I set up hooks for X"

## Core Recipes

### Recipe 1: Prettier Auto-Format on Edit

Formats JavaScript, TypeScript, CSS, and JSON files after every edit or write:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(js|ts|jsx|tsx|css|scss|json|md)$'; then npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi",
        "description": "Prettier auto-format"
      }
    ]
  }
}
```

### Recipe 2: TypeScript Type-Check After Edit

Runs `tsc --noEmit` after editing TypeScript files to catch type errors immediately:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.tsx?$'; then npx tsc --noEmit --pretty 2>&1 | tail -20; fi",
  "description": "TypeScript type-check"
}
```

### Recipe 3: Console.log Warning

Warns when a file containing `console.log` is edited. Does not block, just informs:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(js|ts|jsx|tsx)$'; then MATCHES=$(grep -n 'console\\.log' \"$CLAUDE_FILE_PATH\" 2>/dev/null); if [ -n \"$MATCHES\" ]; then echo \"WARNING: console.log found in $CLAUDE_FILE_PATH:\"; echo \"$MATCHES\" | head -5; fi; fi",
  "description": "Warn about console.log in edited files"
}
```

### Recipe 4: Git Push Review Gate

Opens the diff for review before allowing a git push. Blocks the push so the user can inspect:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git push'; then echo '=== FILES TO BE PUSHED ===' && git diff --stat HEAD~1 && echo '' && echo 'Review the above changes. This hook will allow the push to proceed.'; fi",
        "description": "Show diff summary before git push"
      }
    ]
  }
}
```

To actually block and require confirmation:

```json
{
  "matcher": "Bash",
  "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'git push'; then echo 'BLOCKED: Git push requires explicit user approval.' && exit 1; fi",
  "description": "Block git push (user must approve)"
}
```

### Recipe 5: Doc File Blocker

Prevents creation of unnecessary documentation files (.md, .txt) unless in a docs directory:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(md|txt)$' && ! echo \"$CLAUDE_FILE_PATH\" | grep -q '/docs/'; then echo 'BLOCKED: Do not create .md or .txt files outside /docs/' && exit 1; fi",
        "description": "Block markdown/text file creation outside docs/"
      }
    ]
  }
}
```

### Recipe 6: ESLint Auto-Fix

Auto-fix lint issues and report remaining problems:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(js|ts|jsx|tsx)$'; then npx eslint --fix --no-warn-ignored \"$CLAUDE_FILE_PATH\" 2>&1 | head -20; fi",
  "description": "ESLint auto-fix after edit"
}
```

### Recipe 7: Secret Leak Prevention

Block file writes that contain potential secrets:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(env|key|pem|credentials)$'; then echo 'BLOCKED: Cannot write secret/credential files' && exit 1; fi",
        "description": "Block writing secret files"
      }
    ]
  }
}
```

### Recipe 8: Session-End Audit

Check all modified files for debug artifacts before the session ends:

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "MODIFIED=$(git diff --name-only 2>/dev/null); if [ -n \"$MODIFIED\" ]; then echo '=== Session End Audit ===' && echo \"$MODIFIED\" | xargs grep -ln 'console\\.log\\|debugger\\|TODO.*HACK\\|FIXME' 2>/dev/null | while read f; do echo \"WARNING: Debug artifact in $f\"; done; fi",
        "description": "Audit modified files for debug artifacts at session end"
      }
    ]
  }
}
```

### Recipe 9: Test Runner After Source Edit

Run the related test file whenever a source file is modified:

```json
{
  "matcher": "Edit|Write",
  "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.ts$' && ! echo \"$CLAUDE_FILE_PATH\" | grep -q '\\.test\\.'; then TEST=$(echo \"$CLAUDE_FILE_PATH\" | sed 's/\\.ts$/.test.ts/'); if [ -f \"$TEST\" ]; then npx vitest run \"$TEST\" --reporter=dot 2>&1 | tail -10; fi; fi",
  "description": "Run related test file after source edit"
}
```

## Combining Recipes

A complete settings.json with multiple hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(md|txt)$' && ! echo \"$CLAUDE_FILE_PATH\" | grep -q '/docs/'; then echo 'BLOCKED: No docs outside /docs/' && exit 1; fi",
        "description": "Doc blocker"
      },
      {
        "matcher": "Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(env|key|pem)$'; then echo 'BLOCKED: Secret file' && exit 1; fi",
        "description": "Secret blocker"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(ts|tsx)$'; then npx prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi",
        "description": "Prettier"
      },
      {
        "matcher": "Edit|Write",
        "command": "if echo \"$CLAUDE_FILE_PATH\" | grep -qE '\\.(ts|tsx)$'; then npx tsc --noEmit --pretty 2>&1 | tail -15; fi",
        "description": "TSC check"
      }
    ],
    "Stop": [
      {
        "command": "git diff --name-only 2>/dev/null | xargs grep -ln 'console\\.log' 2>/dev/null && echo 'WARNING: console.log in modified files'",
        "description": "Console.log audit"
      }
    ]
  }
}
```

## Anti-Patterns

- **Stacking too many PostToolUse hooks**: Each hook runs sequentially. Five hooks at 2 seconds each means 10 seconds of delay after every edit. Prioritize the most valuable checks.
- **Blocking reads or greps**: Never use PreToolUse to block non-destructive tools like Read, Grep, or Glob. These are essential for exploration.
- **Missing file extension filters**: A hook without `grep -qE '\\.ts$'` runs on every file type, including binaries and images. Always filter by extension.
- **Swallowing errors silently**: Redirect stderr to `/dev/null` only for known noise. Important errors should surface to the agent.
- **Using interactive commands**: Hooks cannot prompt for input. Commands like `git add -i` or `read -p` will hang.

## Quick Reference

| Recipe | Type | Blocks? | Target Files |
|--------|------|---------|-------------|
| Prettier | PostToolUse | No | .js/.ts/.css/.json |
| TSC check | PostToolUse | No | .ts/.tsx |
| Console.log warn | PostToolUse | No | .js/.ts/.jsx/.tsx |
| Git push review | PreToolUse | Optional | Bash (git push) |
| Doc blocker | PreToolUse | Yes | .md/.txt |
| Secret blocker | PreToolUse | Yes | .env/.key/.pem |
| ESLint fix | PostToolUse | No | .js/.ts/.jsx/.tsx |
| Session audit | Stop | No | All modified files |
| Test runner | PostToolUse | No | .ts (non-test) |
