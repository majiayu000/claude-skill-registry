---
name: clang-format Configuration
description: The model must invoke this skill when any trigger occurs - (1) user mentions "clang-format" or ".clang-format", (2) user requests analyzing code style/formatting patterns/conventions, (3) user requests creating/modifying/generating formatting configuration, (4) user troubleshoots formatting behavior or unexpected results, (5) user asks about brace styles/indentation/spacing/alignment/line breaking/pointer alignment, (6) user wants to preserve existing style/minimize whitespace changes/reduce formatting diffs/codify dominant conventions.
---

# clang-format Configuration

Configure the clang-format code formatting tool using ready-to-use templates, integration scripts, and comprehensive reference documentation.

## Purpose

This skill provides procedural workflows for clang-format configuration tasks:

- Create new .clang-format files from proven templates
- Analyze existing code style and generate matching configurations
- Set up editor and git integration with bundled scripts
- Troubleshoot formatting behavior using reference documentation

## Workflow Routing by Trigger Type

Once invoked, route to appropriate workflow based on which trigger fired:

**Trigger 1: Explicit clang-format mention** → If user asks about specific options: Consult references/01-09.md for relevant category → If user needs complete reference: Direct to references/complete/clang-format-style-options.md → If user asks about CLI usage: Reference references/cli-usage.md

**Trigger 2: Code style analysis request** → Follow "Analyzing Existing Code Style" workflow below → Examine code samples systematically (braces→indentation→spacing→breaking→alignment) → Map patterns to closest template in assets/configs/ → Generate initial configuration hypothesis as a temporary configuration file "/tmp/<repo*name>/hypothesis*<number>.clang-format" → VERIFY IMPACT: Run `clang-format --style="/tmp/<repo_name>/hypothesis_<number>.clang-format" file.cpp | diff - file.cpp` on 3-5 representative samples → MEASURE IMPACT using weighted scoring: • Metric 1: Line count changes (lines added/removed) - weight 10 • Metric 2: In-line whitespace changes (spacing within existing lines) - weight 1 • Impact Score = (line_count_changes × 10) + (whitespace_changes × 1) • Lower score = lower impact to rebasing conflicts, future git-diff analysis, and merge request change reviews = better configuration → ITERATE: Adjust config options targeting highest-impact settings, re-test, compare scores → REPEAT until reaching minimal achievable score while maintaining consistent style enforcement → REPORT TO USER: Present winning configuration with: • Final impact score and breakdown (line changes vs whitespace changes) • Comparison table showing all tested hypotheses and their scores • Example diff snippets showing what will change, with commands for the user to test it themselves against files of their choice. • Rationale for selected configuration → AWAIT USER APPROVAL before finalizing configuration → Only after approval: provide final configuration file

**Trigger 3: Configuration file operations** → If creating new: Follow "Creating New Configuration from Template" workflow → If modifying existing: Read current config, identify changes needed, consult relevant category guide → If generating from code: Use Trigger 2 workflow (code style analysis)

**Trigger 4: Formatting behavior investigation** → Follow "Troubleshooting Formatting Issues" workflow below → Verify config detection with --dump-config → Identify affected category, consult relevant references/0X.md guide → Test isolated options with minimal config

**Trigger 5: Style option inquiries** → Map question to category: braces→03, indentation→04, spacing→05, alignment→01, breaking→02 → Reference specific category guide in references/ → Provide examples from quick-reference.md if applicable

**Trigger 6: Minimal-disruption requests** → Use "Analyzing Existing Code Style" workflow to match current patterns → Emphasize starting from closest template to minimize changes → Test on representative samples before project-wide application → Document which patterns were preserved vs normalized

## Bundled Resources

### Configuration Templates (assets/configs/)

Seven ready-to-use `.clang-format` templates optimized for common scenarios:

- `google-cpp-modified.clang-format` - Google C++ style with 4-space indent, 120 column limit
- `linux-kernel.clang-format` - Linux kernel coding standards (tabs, K&R braces)
- `microsoft-visual-studio.clang-format` - Microsoft/Visual Studio conventions
- `modern-cpp17-20.clang-format` - Modern C++17/20 style with contemporary idioms
- `compact-dense.clang-format` - Compact style for space-constrained environments
- `readable-spacious.clang-format` - Spacious style prioritizing readability
- `multi-language.clang-format` - Multi-language configuration (C++, JavaScript, Java)

**When to use templates**: Start new projects, establish team standards, or quickly test formatting approaches.

### Integration Scripts (assets/integrations/)

Three editor and git integration scripts:

- `pre-commit` - Git hook script for automatic formatting of staged files (works with pre-commit or prek framework)
- `vimrc-clang-format.vim` - Vim configuration for format-on-save
- `emacs-clang-format.el` - Emacs configuration for clang-format integration

**When to use integrations**: Set up automatic formatting in development workflow.

**Note**: The pre-commit hook script works with both the pre-commit framework (Python) and prek (Rust alternative). Both frameworks use `.pre-commit-config.yaml` with identical syntax.

### Reference Documentation (references/)

Detailed documentation organized by category:

**Quick Navigation**:

- `index.md` - Overview and documentation hub
- `quick-reference.md` - Complete working configurations with explanations
- `cli-usage.md` - Command-line usage, editor setup, CI/CD integration

**Option Categories** (01-09.md):

1. `01-alignment.md` - Vertical alignment of declarations, assignments, operators
2. `02-breaking.md` - Line breaking and wrapping rules
3. `03-braces.md` - Brace placement styles (K&R, Allman, GNU, etc.)
4. `04-indentation.md` - Indentation rules and special cases
5. `05-spacing.md` - Whitespace control around operators, keywords
6. `06-includes.md` - Include/import organization and sorting
7. `07-languages.md` - Language-specific options for C++, Java, JavaScript
8. `08-comments.md` - Comment formatting and reflow
9. `09-advanced.md` - Penalty system, raw string formatting, experimental features

**Complete Reference** (complete/):

- `clang-format-cli.md` - Full command-line interface documentation
- `clang-format-style-options.md` - All 194 style options with examples

## Common Workflows

### Creating New Configuration from Template

To create a new `.clang-format` file:

1. Identify requirements (style guide, team preferences, language)
2. Select closest template from `assets/configs/`
3. Copy template to project root as `.clang-format`
4. Test formatting: `clang-format --dry-run file.cpp`
5. Customize specific options using references/01-09.md as needed
6. Verify changes: `clang-format file.cpp | diff - file.cpp`

Example:

```bash
# Copy Google C++ template
cp assets/configs/google-cpp-modified.clang-format /path/to/project/.clang-format

# Test on sample file
clang-format --dry-run /path/to/project/src/main.cpp

# Apply if satisfied
clang-format -i /path/to/project/src/*.cpp
```

### Analyzing Existing Code Style

To generate configuration matching existing code:

1. Examine code samples for formatting patterns
2. Identify key characteristics:
   - Brace placement → consult `references/03-braces.md`
   - Indentation (spaces/tabs, width) → consult `references/04-indentation.md`
   - Spacing (operators, keywords) → consult `references/05-spacing.md`
   - Line breaking (column limit, wrapping) → consult `references/02-breaking.md`
   - Alignment patterns → consult `references/01-alignment.md`
3. Map patterns to closest base style in `references/quick-reference.md`
4. Start with that template from `assets/configs/`
5. Override specific options to match observed patterns
6. Test on representative code samples
7. Iterate until formatting matches existing style

This workflow minimizes whitespace-only changes when introducing clang-format to existing projects.

### Setting Up Editor Integration

To enable format-on-save in editors:

**Vim**:

1. Copy `assets/integrations/vimrc-clang-format.vim` content to `.vimrc`
2. Restart Vim or source configuration
3. Save any C/C++/Java file to trigger formatting

**Emacs**:

1. Copy `assets/integrations/emacs-clang-format.el` to Emacs config
2. Restart Emacs or evaluate configuration
3. Save any supported file to trigger formatting

**Other editors**: Consult `references/cli-usage.md` for VS Code, CLion, and other editor setup instructions.

### Setting Up Git Hook for Formatting

**Option 1: Using pre-commit/prek framework (Recommended)**:

Configure in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-clang-format
    rev: v19.1.7
    hooks:
      - id: clang-format
```

Then install: `pre-commit install` or `prek install`

**Option 2: Manual git hook**:

1. Copy `assets/integrations/pre-commit` to `.git/hooks/pre-commit`
2. Make executable: `chmod +x .git/hooks/pre-commit`
3. Test by staging and committing changes

The hook formats only staged files, preserving unstaged changes.

### Troubleshooting Formatting Issues

When formatting produces unexpected results:

1. Verify configuration detection: `clang-format --dump-config file.cpp`
2. Check command options in `references/cli-usage.md`
3. Identify affected formatting category (braces, spacing, breaking, etc.)
4. Consult relevant category guide in references/01-09.md
5. Test isolated options: create minimal config with suspect option
6. For comprehensive option details, check `references/complete/clang-format-style-options.md`

### Setting Up CI/CD Formatting Checks

To enforce formatting in continuous integration:

1. Review CI examples in `references/cli-usage.md`
2. Add clang-format check to pipeline:
   ```bash
   # Check formatting without modifying files
   clang-format --dry-run --Werror src/**/*.{cpp,h}
   ```
3. Configure to fail build on formatting violations
4. Document formatting requirements for contributors

## Key Concepts

**Base Styles**: Predefined configurations (LLVM, Google, Chromium, Mozilla, WebKit, Microsoft, GNU) provide starting points. Set with `BasedOnStyle: Google` then override specific options.

**Multi-Language Support**: Configure different languages separately in single file using `Language:` key. See `assets/configs/multi-language.clang-format` for example.

**Penalty System**: clang-format uses penalties to choose between formatting alternatives. Higher penalty values discourage specific choices. See `references/09-advanced.md` for details.

**Progressive Refinement**: Start with template closest to requirements, then customize incrementally. Test frequently on representative code samples.

## Testing Configurations

```bash
# Preview changes without modifying file
clang-format --dry-run file.cpp

# Show diff of proposed changes
clang-format file.cpp | diff - file.cpp

# Apply formatting to file
clang-format -i file.cpp

# Format entire project
find src include -name '*.cpp' -o -name '*.h' | xargs clang-format -i

# Check formatting in CI (fail on violations)
clang-format --dry-run --Werror src/**/*.{cpp,h}
```

## Navigation Strategy

For most tasks, follow this progression:

1. **Start with templates**: Browse `assets/configs/` for ready-to-use configurations
2. **Quick reference**: Check `references/quick-reference.md` for complete configurations with explanations
3. **Category guides**: Consult `references/01-09.md` for specific option categories
4. **CLI usage**: Reference `references/cli-usage.md` for command-line and integration details
5. **Complete reference**: Use `references/complete/` for exhaustive option documentation

When analyzing code or troubleshooting, identify the formatting aspect (braces, spacing, alignment, etc.) and jump directly to the relevant category guide in references/.
