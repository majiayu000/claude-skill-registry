---
name: Leavn Commit Machine
description: Create clean, descriptive git commits for Leavn app following emoji prefix convention with comprehensive change summaries
allowed-tools: Bash, Read
---

# Leavn Commit Machine

## Instructions

Create commits following Leavn's emoji convention:

1. **Check what changed**:
   ```bash
   git status
   git diff --stat
   git diff
   ```

2. **Choose emoji prefix**:
   - 🔧 `:wrench:` - Bug fixes, corrections
   - 🚀 `:rocket:` - New features, major improvements
   - 🧹 `:broom:` - Code cleanup, deletions
   - ⚡️ `:zap:` - Performance improvements
   - 🛡️ `:shield:` - Security, error handling
   - 🔀 `:twisted_rightwards_arrows:` - Merge, consolidation
   - 🐛 `:bug:` - Bug fixes (visual/functional)
   - 🎨 `:art:` - UI/UX improvements
   - 🎵 `:musical_note:` - Audio features
   - 📝 `:memo:` - Documentation

3. **Write commit message**:
   ```
   {emoji} Brief summary (50 chars)

   - Bullet point details
   - File counts, line changes
   - Impact statement

   🤖 Generated with Claude Code
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

4. **Commit**:
   ```bash
   git add -A
   git commit -m "$(cat <<'EOF'
   Message here
   EOF
   )"
   ```

Use this skill when: Ready to commit changes, multiple files modified, need good commit message
