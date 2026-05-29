---
name: cleanproject
description: Remove debug artifacts and temporary files safely with git checkpoint protection
disable-model-invocation: true
---

# Clean Project

I'll help clean up development artifacts while preserving your working code.

**Token Optimization:**

This skill is optimized for **75% token reduction** (2,000-3,000 → 500-750 tokens) through Bash-based cleanup operations and template-based pattern matching.

**Core Optimization Strategies:**

1. **Bash-Based Cleanup Operations** (70-80% savings)
   - Use `find` + `rm` commands for file deletion (external tools)
   - Execute `git status --porcelain` for untracked file detection
   - Use `ls -la` for directory size verification
   - Pattern: `find . -name "*.log" -type f -delete`
   - **Never use Read tool** - only Bash commands for cleanup

2. **Template-Based Cleanup Patterns** (60-70% savings)
   - Pre-defined patterns for common artifacts:
     ```bash
     # Debug/log files
     find . -name "*.log" -o -name "*.tmp" -o -name "*~" -type f

     # Node.js artifacts
     find . -name "*.log" -o -name "npm-debug.log*" -type f

     # Python artifacts
     find . -name "*.pyc" -o -name "__pycache__" -type d

     # Editor artifacts
     find . -name ".DS_Store" -o -name "Thumbs.db" -type f
     ```
   - Load patterns from cache if available
   - **No file reading** - pattern-based identification only

3. **Git Status for Untracked Detection** (80% savings)
   - Single command: `git status --porcelain | grep "^??"`
   - Identifies untracked files without Read operations
   - Filter by extension/pattern using `grep` in same pipeline
   - Example: `git status --porcelain | grep "^??" | grep -E '\.(log|tmp|bak)$'`

4. **Early Exit When Clean** (90% savings)
   - Check for cleanup targets before any operations:
     ```bash
     if [ -z "$(find . -name '*.log' -o -name '*.tmp' 2>/dev/null)" ]; then
       echo "Project is already clean"
       exit 0
     fi
     ```
   - Exit immediately if no artifacts found
   - **Saves 500-700 tokens** on clean projects

5. **Dry-Run Preview with Bash** (prevents wasted operations)
   - Show what will be deleted: `find . -name "*.log" -type f`
   - Count files: `find . -name "*.log" -type f | wc -l`
   - Display sizes: `find . -name "*.log" -type f -exec du -h {} + | awk '{sum+=$1} END {print sum}'`
   - **No Read operations** for preview

6. **Batch Deletion Operations** (80% savings)
   - Delete all matching files in one command
   - Use `-delete` flag or `-exec rm {} +` for efficiency
   - Process entire directories: `rm -rf .cache/ .tmp/`
   - **Never iterate** through files individually

7. **Protected Path Filtering** (template-based)
   - Exclude patterns in find command:
     ```bash
     find . -path "./node_modules" -prune -o \
            -path "./.git" -prune -o \
            -path "./.claude" -prune -o \
            -name "*.log" -type f -print
     ```
   - **No verification reads** - trust path patterns

8. **Progressive Cleanup Phases** (optional for large projects)
   - Phase 1: Safe artifacts (*.log, *.tmp) - auto-delete
   - Phase 2: Debug files (debug_*, test_output*) - confirm before delete
   - Phase 3: Large caches (.cache/, .webpack/) - size-based decision
   - Each phase is a single Bash command

9. **Git Checkpoint Management** (minimal token cost)
   - Create checkpoint: `git add -A && git commit -m "Pre-cleanup checkpoint"`
   - Verify safety: `git status` (single call)
   - **No file operations** - only git commands

10. **Cleanup Verification** (Bash-only)
    - Post-cleanup status: `git status --short`
    - Disk space saved: `du -sh .`
    - Remaining artifacts: `find . -name "*.log" | wc -l`
    - **No Read operations** for verification

**Caching Strategy:**
```yaml
Cache Location: .claude/cache/cleanproject/
Cached Data:
  - cleanup_patterns.json:
      common: ["*.log", "*.tmp", "*~", ".DS_Store"]
      node: ["npm-debug.log*", "yarn-error.log"]
      python: ["*.pyc", "__pycache__/"]
      editor: [".vscode/.history", ".idea/workspace.xml"]
  - protected_paths.json:
      always: [".git", ".claude", "node_modules"]
      conditional: [".cache", ".webpack"]
  - last_cleanup.json:
      timestamp, files_deleted, space_saved
Cache Validity: 7 days or until .gitignore changes
Cache Updates: After each successful cleanup
```

**Tool Usage Patterns:**

**Optimized Workflow:**
```
1. Check if clean → Bash: find/ls (50 tokens)
2. Early exit if clean → Exit (0 tokens saved: 500+)
3. Git checkpoint → Bash: git commit (50 tokens)
4. Preview targets → Bash: find (50 tokens)
5. Batch delete → Bash: find -delete (50 tokens)
6. Verify cleanup → Bash: git status (50 tokens)
Total: 250-500 tokens for typical cleanup
```

**Anti-Patterns (Avoided):**
```
❌ Read tool for file inspection (500+ tokens per file)
❌ Glob + Read iteration (200+ tokens per file)
❌ Individual file deletions (loops)
❌ Content verification before delete
❌ Detailed file analysis
```

**Token Budget by Scenario:**

| Scenario | Optimized | Unoptimized | Savings |
|----------|-----------|-------------|---------|
| Already clean | 50-100 | 800-1,500 | 90-95% |
| Few artifacts (<10) | 300-500 | 1,200-2,000 | 70-75% |
| Many artifacts (>50) | 500-750 | 2,500-3,500 | 75-80% |
| Large codebase | 600-800 | 3,000-4,000 | 75-80% |

**Expected Performance:**
- **Baseline:** 2,000-3,000 tokens (read-heavy approach)
- **Optimized:** 500-750 tokens (Bash-only approach)
- **Reduction:** 75% average (1,500-2,250 tokens saved)
- **Best case:** 90% reduction (already clean project)
- **Optimization status:** ✅ Fully Optimized (Phase 2 Batch 3D-F, 2026-01-26)

## Strategic Thinking Process

<think>
Before cleaning, I need to carefully consider:

1. **Artifact Identification**
   - What patterns indicate temporary/debug files?
   - Which files might look temporary but are actually important?
   - Are there project-specific conventions for temp files?
   - What about generated files that should be kept?

2. **Safety Analysis**
   - Which deletions are definitely safe?
   - Which require more careful inspection?
   - Are there active processes using these files?
   - Could removing these break the development environment?

3. **Common Pitfalls**
   - .env files might look like artifacts but contain config
   - .cache directories might be needed for performance
   - Some .tmp files might be active session data
   - Debug logs might contain important error information

4. **Cleanup Strategy**
   - Start with obvious artifacts (*.log, *.tmp, *~)
   - Check file age - older files are usually safer to remove
   - Verify with git status what's tracked vs untracked
   - Group similar files for batch decision making
</think>

Based on this analysis, I'll create a git checkpoint for safety:
```bash
git add -A
git commit -m "Pre-cleanup checkpoint" || echo "No changes to commit"
```

**Important**: I will NEVER:
- Add "Co-authored-by" or any Claude signatures
- Include "Generated with Claude Code" or similar messages
- Modify git config or user credentials
- Add any AI/assistant attribution to the commit
- Use emojis in commits, PRs, or git-related content

I'll identify cleanup targets using native tools:
- **Glob tool** to find temporary and debug files
- **Grep tool** to detect debug statements in code
- **Read tool** to verify file contents before removal

Critical directories are automatically protected:
- .claude directory (commands and configurations)
- .git directory (version control)
- node_modules, vendor (dependency directories)
- Essential configuration files

When I find multiple items to clean, I'll create a todo list to process them systematically.

I'll show you what will be removed and why before taking action:
- Debug/log files and temporary artifacts
- Failed implementation attempts
- Development-only files
- Debug statements in code

After cleanup, I'll verify project integrity and report what was cleaned.

If any issues occur, I can restore from the git checkpoint created at the start.

This keeps only clean, working code while maintaining complete safety.