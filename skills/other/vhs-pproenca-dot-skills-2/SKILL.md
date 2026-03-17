---
name: vhs
description: VHS terminal recording best practices from Charmbracelet (formerly charmbracelet-vhs). This skill should be used when writing, reviewing, or editing VHS tape files to create professional terminal GIFs and videos. Triggers on tasks involving .tape files, VHS configuration, terminal recording, demo creation, or CLI documentation.
---

# Charmbracelet VHS Best Practices

Comprehensive best practices guide for VHS terminal recordings, maintained by Charmbracelet. Contains 47 rules across 8 categories, prioritized by impact to guide creation of professional, portable, and optimized terminal demos.

## When to Apply

Reference these guidelines when:
- Writing new VHS tape files
- Creating terminal demos for documentation
- Setting up CI/CD for automated GIF generation
- Optimizing recording file size and quality
- Troubleshooting tape file issues
- Reviewing tape files for best practices

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Configuration Structure | CRITICAL | `config-` |
| 2 | Dependency Management | CRITICAL | `deps-` |
| 3 | Command Syntax | HIGH | `cmd-` |
| 4 | Timing & Synchronization | HIGH | `timing-` |
| 5 | Output Optimization | MEDIUM-HIGH | `output-` |
| 6 | Visual Quality | MEDIUM | `visual-` |
| 7 | CI/Automation | MEDIUM | `ci-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Configuration Structure (CRITICAL)

- [`config-settings-order`](references/config-settings-order.md) - Place all settings before commands
- [`config-output-first`](references/config-output-first.md) - Declare output at file start
- [`config-shell-explicit`](references/config-shell-explicit.md) - Explicitly set shell type
- [`config-typing-speed-global`](references/config-typing-speed-global.md) - Set global TypingSpeed early
- [`config-dimensions-explicit`](references/config-dimensions-explicit.md) - Set explicit terminal dimensions
- [`config-comments-document`](references/config-comments-document.md) - Use comments to document tape structure

### 2. Dependency Management (CRITICAL)

- [`deps-require-early`](references/deps-require-early.md) - Use Require for dependency validation
- [`deps-require-order`](references/deps-require-order.md) - Place Require before settings
- [`deps-require-all`](references/deps-require-all.md) - Require all external commands
- [`deps-system-requirements`](references/deps-system-requirements.md) - Verify system dependencies

### 3. Command Syntax (HIGH)

- [`cmd-type-syntax`](references/cmd-type-syntax.md) - Use correct Type command syntax
- [`cmd-enter-explicit`](references/cmd-enter-explicit.md) - Always follow Type with Enter
- [`cmd-key-repeat`](references/cmd-key-repeat.md) - Use key repeat counts
- [`cmd-ctrl-combinations`](references/cmd-ctrl-combinations.md) - Use Ctrl combinations for terminal control
- [`cmd-hide-show`](references/cmd-hide-show.md) - Use Hide/Show for sensitive operations
- [`cmd-env-variables`](references/cmd-env-variables.md) - Use Env for environment variables
- [`cmd-screenshot`](references/cmd-screenshot.md) - Use Screenshot for static captures
- [`cmd-multiline-type`](references/cmd-multiline-type.md) - Handle multiline commands properly

### 4. Timing & Synchronization (HIGH)

- [`timing-sleep-after-enter`](references/timing-sleep-after-enter.md) - Add Sleep after commands for output
- [`timing-wait-pattern`](references/timing-wait-pattern.md) - Use Wait for dynamic command completion
- [`timing-type-speed-override`](references/timing-type-speed-override.md) - Override TypingSpeed for emphasis
- [`timing-sleep-units`](references/timing-sleep-units.md) - Use explicit time units
- [`timing-final-sleep`](references/timing-final-sleep.md) - End recordings with final Sleep
- [`timing-natural-pauses`](references/timing-natural-pauses.md) - Add natural pauses between actions
- [`timing-wait-timeout`](references/timing-wait-timeout.md) - Set appropriate Wait timeouts
- [`timing-playback-speed`](references/timing-playback-speed.md) - Use PlaybackSpeed for final adjustments

### 5. Output Optimization (MEDIUM-HIGH)

- [`output-format-selection`](references/output-format-selection.md) - Choose output format based on use case
- [`output-framerate`](references/output-framerate.md) - Optimize framerate for file size
- [`output-dimensions-optimize`](references/output-dimensions-optimize.md) - Right-size terminal dimensions
- [`output-loop-offset`](references/output-loop-offset.md) - Use LoopOffset for seamless loops
- [`output-multiple-formats`](references/output-multiple-formats.md) - Generate multiple output formats
- [`output-relative-paths`](references/output-relative-paths.md) - Use relative paths for portability

### 6. Visual Quality (MEDIUM)

- [`visual-font-readable`](references/visual-font-readable.md) - Choose readable font settings
- [`visual-theme-selection`](references/visual-theme-selection.md) - Select appropriate theme
- [`visual-window-decoration`](references/visual-window-decoration.md) - Add window decorations for polish
- [`visual-spacing`](references/visual-spacing.md) - Adjust letter and line spacing
- [`visual-padding-margin`](references/visual-padding-margin.md) - Use padding and margins effectively
- [`visual-cursor-visibility`](references/visual-cursor-visibility.md) - Ensure cursor visibility

### 7. CI/Automation (MEDIUM)

- [`ci-github-action`](references/ci-github-action.md) - Use official VHS GitHub Action
- [`ci-auto-commit`](references/ci-auto-commit.md) - Auto-commit generated assets
- [`ci-golden-files`](references/ci-golden-files.md) - Use golden files for integration testing
- [`ci-matrix-builds`](references/ci-matrix-builds.md) - Generate platform-specific demos
- [`ci-caching`](references/ci-caching.md) - Cache VHS dependencies in CI

### 8. Advanced Patterns (LOW)

- [`advanced-source-include`](references/advanced-source-include.md) - Use Source for reusable tape components
- [`advanced-clipboard`](references/advanced-clipboard.md) - Use Copy and Paste for complex input
- [`advanced-recording-live`](references/advanced-recording-live.md) - Record live sessions then edit
- [`advanced-server-mode`](references/advanced-server-mode.md) - Use server mode for remote access

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
