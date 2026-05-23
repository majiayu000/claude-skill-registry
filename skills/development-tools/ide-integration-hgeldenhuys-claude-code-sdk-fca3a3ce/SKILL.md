---
name: ide-integration
description: IDE integration tips for VS Code, JetBrains, and terminal workflows. Use when setting up Claude Code with your IDE, configuring keybindings, optimizing terminal workflows, or synchronizing file navigation. Covers extensions, split terminals, clipboard, and diff viewing.
version: 1.0.0
author: Claude Code SDK
tags: [ide, vscode, jetbrains, terminal]
---

# IDE Integration

Optimize your Claude Code workflow by integrating with VS Code, JetBrains IDEs, and terminal multiplexers. This skill covers setup, keybindings, and patterns for seamless development.

## Quick Reference

| IDE | Setup | Best Use |
|-----|-------|----------|
| VS Code | Integrated terminal, extensions | Full-featured editing + Claude |
| JetBrains | External terminal recommended | Heavy refactoring, debugging |
| Terminal-only | tmux/screen for sessions | SSH, server-side, minimal setups |
| Chrome | `claude --chrome` | Web app testing, browser automation |

## Chrome Integration (2.0.73+)

Connect Claude Code to Chrome for browser automation and live debugging.

```bash
# Start with Chrome enabled
claude --chrome

# Or enable in-session
/chrome
```

**Capabilities:**
- Live debugging (console errors, DOM state)
- Web app testing (forms, flows, regressions)
- Design verification (compare UI to mocks)
- Data extraction from websites
- Authenticated app access (uses your login state)

**Requirements:** Chrome browser, [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) v1.0.36+, Pro/Team/Enterprise plan.

See [chrome-integration](../chrome-integration/SKILL.md) skill for detailed workflows.

## UI Improvements (2.1.6+)

- **@ Autocomplete Icons** - Different suggestion types now have icons
- **Status Line Fields** - `context_window.used_percentage` and `remaining_percentage` available

## Core Integration Patterns

### Pattern 1: Split Terminal Workflow

Run Claude Code in one terminal pane, run commands in another.

```
+---------------------------+---------------------------+
|                           |                           |
|    IDE / Editor           |   Claude Code Terminal    |
|                           |                           |
|                           |---------------------------|
|                           |   Command Terminal        |
|                           |   (tests, builds, etc.)   |
+---------------------------+---------------------------+
```

### Pattern 2: IDE as Diff Viewer

Let Claude make changes, use IDE's diff tools to review:

1. Claude edits files
2. IDE shows git diff/file changes
3. Review changes in IDE's visual diff
4. Accept or request refinements from Claude

### Pattern 3: File Navigation Sync

Share current file context between IDE and Claude:

```bash
# Copy current file path to clipboard (macOS)
echo "/path/to/current/file.ts" | pbcopy

# Paste into Claude prompt
"Look at /path/to/current/file.ts and fix the error on line 42"
```

## Clipboard Integration

### macOS

```bash
# Copy to clipboard
echo "text" | pbcopy
cat file.txt | pbcopy

# Paste from clipboard
pbpaste
pbpaste > file.txt
```

### Linux (X11)

```bash
# Requires xclip or xsel
echo "text" | xclip -selection clipboard
xclip -selection clipboard -o
```

### WSL / Windows

```bash
# Copy
echo "text" | clip.exe

# Paste
powershell.exe Get-Clipboard
```

## Terminal Multiplexing

Split terminals efficiently for Claude Code workflows.

### tmux Quick Reference

```bash
# Start new session
tmux new -s claude

# Split horizontally (top/bottom)
Ctrl-b "

# Split vertically (left/right)
Ctrl-b %

# Navigate panes
Ctrl-b arrow-key

# Resize panes
Ctrl-b Ctrl-arrow-key

# Detach session
Ctrl-b d

# Reattach
tmux attach -t claude
```

### Recommended tmux Layout

```bash
# Create Claude Code development layout
tmux new-session -s dev -n main \; \
  split-window -h -p 40 \; \
  split-window -v -p 30 \; \
  select-pane -t 0
```

Layout result:
- Left pane (60%): Main editor / IDE
- Top-right (40% x 70%): Claude Code
- Bottom-right (40% x 30%): Command runner

## File Watching Patterns

### Watch for Claude's Changes

```bash
# macOS - watch for file changes
fswatch -o /path/to/project | xargs -n1 -I{} echo "File changed"

# Linux - inotifywait
inotifywait -m -r -e modify /path/to/project

# Cross-platform with node
npx chokidar '/path/**/*.ts' -c 'echo "Changed: {path}"'
```

### Auto-reload Integration

Many IDEs auto-reload files. If not:

| IDE | Enable Auto-reload |
|-----|-------------------|
| VS Code | Enabled by default |
| WebStorm | File > Settings > Appearance > Synchronize files on frame activation |
| IntelliJ | Same as WebStorm |
| Vim/Neovim | `:set autoread` |

## Diff Viewing

### Command Line Diffs

```bash
# Git diff of Claude's changes
git diff

# Diff specific file
git diff path/to/file.ts

# Diff with color (most terminals)
git diff --color

# Side-by-side diff
git diff --side-by-side  # requires diff-so-fancy or similar
```

### IDE Diff Tools

| IDE | How to View Diffs |
|-----|-------------------|
| VS Code | Source Control panel (Ctrl/Cmd+Shift+G) |
| JetBrains | Git tool window, Local Changes tab |
| Vim | `:Gdiff` (with fugitive plugin) |

### Delta (Enhanced Diffs)

```bash
# Install delta
brew install git-delta  # macOS
cargo install git-delta # Rust

# Configure git to use delta
git config --global core.pager delta
git config --global interactive.diffFilter 'delta --color-only'
```

## Environment Variables for Claude Code

```bash
# Add to ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="your-key"
export CLAUDE_CODE_EDITOR="code"  # or "webstorm", "vim", etc.

# For JetBrains IDEs, use the CLI launcher
export CLAUDE_CODE_EDITOR="webstorm"
export CLAUDE_CODE_EDITOR="idea"
export CLAUDE_CODE_EDITOR="pycharm"
```

## Quick Keybinding Reference

### Terminal Navigation

| Action | macOS | Linux |
|--------|-------|-------|
| New tab | Cmd+T | Ctrl+Shift+T |
| Split horizontal | Cmd+D (iTerm2) | Varies |
| Split vertical | Cmd+Shift+D (iTerm2) | Varies |
| Switch pane | Cmd+[ / Cmd+] | Varies |
| Clear terminal | Cmd+K | Ctrl+L |
| Cancel command | Ctrl+C | Ctrl+C |
| Search history | Ctrl+R | Ctrl+R |

### Copy/Paste in Terminal

| Action | macOS | Linux |
|--------|-------|-------|
| Copy | Cmd+C | Ctrl+Shift+C |
| Paste | Cmd+V | Ctrl+Shift+V |
| Select all | Cmd+A | Ctrl+Shift+A |

## Workflow: Initial Setup

### Prerequisites

- [ ] Claude Code installed and authenticated
- [ ] IDE installed and configured
- [ ] Terminal multiplexer (optional but recommended)

### Steps

1. **Configure terminal**
   - [ ] Set up split panes or tmux
   - [ ] Test clipboard integration

2. **Configure IDE**
   - [ ] Enable file auto-reload
   - [ ] Set up diff viewer shortcuts
   - [ ] Install recommended extensions

3. **Test integration**
   - [ ] Have Claude edit a file
   - [ ] Verify IDE shows changes
   - [ ] Test undo/redo flow

## Common Integration Issues

| Issue | Solution |
|-------|----------|
| IDE doesn't show Claude's changes | Enable auto-reload, check file watcher |
| Clipboard not working | Check pbcopy/xclip installation |
| tmux colors broken | Set `export TERM=xterm-256color` |
| SSH sessions disconnect | Use `tmux` to persist Claude sessions |
| Large file edits slow | Consider Claude's `Edit` tool vs full rewrites |

## Best Practices

1. **Use split terminals** - Keep Claude visible while working
2. **Review diffs before committing** - IDE diff tools are faster than reading
3. **Copy file paths liberally** - Saves Claude from searching
4. **Persist sessions** - Use tmux/screen for long-running work
5. **Configure shortcuts** - Quick terminal switching is essential

## Reference Files

| File | Contents |
|------|----------|
| [VSCODE.md](./VSCODE.md) | VS Code specific setup, extensions, keybindings |
| [JETBRAINS.md](./JETBRAINS.md) | IntelliJ, WebStorm, PyCharm integration |
| [TERMINAL.md](./TERMINAL.md) | Terminal integration, iTerm2, tmux patterns |
