---
name: code-stats
description: "Analyze codebase with tokei (fast line counts by language) and difft (semantic AST-aware diffs). Get quick project overview without manual counting. Triggers on: how big is codebase, count lines of code, what languages, show semantic diff, compare files, code statistics."
compatibility: "Requires tokei and difft CLI tools. Install: brew install tokei difft (macOS) or cargo install tokei difftastic (cross-platform)."
allowed-tools: "Bash"
---

# Code Statistics

Quickly analyze codebase size, composition, and changes.

## tokei - Line Counts

```bash
# Count all code
tokei

# Compact output sorted by code
tokei --compact --sort code

# Specific languages
tokei --type=TypeScript,JavaScript

# Exclude directories
tokei --exclude node_modules --exclude dist

# JSON output for scripting
tokei --output json | jq '.Total.code'
```

### Sample Output

```
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 TypeScript             45        12847         9823         1456         1568
 JavaScript             12         2341         1876          234          231
-------------------------------------------------------------------------------
 Total                  57        15188        11699         1690         1799
===============================================================================
```

## difft - Semantic Diffs

```bash
# Compare files
difft old.ts new.ts

# Inline mode
difft --display=inline old.ts new.ts

# With git
GIT_EXTERNAL_DIFF=difft git diff
GIT_EXTERNAL_DIFF=difft git show HEAD~1
```

### Why Semantic?

| Traditional diff | difft |
|-----------------|-------|
| Line-by-line | AST-aware |
| Shows moved as delete+add | Recognizes moves |
| Whitespace sensitive | Ignores formatting |

## Quick Reference

| Task | Command |
|------|---------|
| Count all code | `tokei` |
| Compact output | `tokei --compact` |
| Sort by code | `tokei --sort code` |
| TypeScript only | `tokei -t TypeScript` |
| JSON output | `tokei --output json` |
| Exclude dir | `tokei --exclude node_modules` |
| Semantic diff | `difft file1 file2` |
| Git diff | `GIT_EXTERNAL_DIFF=difft git diff` |

## When to Use

- Getting quick codebase overview
- Comparing code changes semantically
- Understanding project composition
- Reviewing refactoring impact
- Tracking codebase growth

## Additional Resources

For detailed patterns, load:
- `./references/tokei-advanced.md` - Filtering, output formats, CI integration
- `./references/difft-advanced.md` - Display modes, git integration, language support
