---
name: lazygit-config
description: Configure lazygit TUI including config.yml setup, custom pagers (especially delta integration), themes, keybindings, and custom commands. Use when setting up lazygit, configuring git diff viewers, integrating delta, or customizing lazygit behavior. Keywords: lazygit, delta, git diff, pager, lazygit config, config.yml, git TUI, diff viewer
---

# Lazygit Configuration Expert

Expert guidance for configuring lazygit with delta integration, custom pagers, themes, and keybindings.

## Core Concepts

Lazygit is a terminal UI for git that prioritizes:
- **Minimal configuration**: Only override what you need
- **YAML-based config**: Clean, hierarchical settings
- **Custom pagers**: Enhanced diff viewing with tools like delta
- **Keybinding flexibility**: Adapt to any layout (Vim, Emacs, Colemak)
- **Repository-specific configs**: Override settings per repo

## Configuration File Locations

### Platform-Specific Paths

**Standard locations (current):**
- **macOS**: `~/Library/Application Support/lazygit/config.yml`
- **Linux**: `~/.config/lazygit/config.yml`
- **Windows**: `%LOCALAPPDATA%\lazygit\config.yml`

**Legacy locations (older installs):**
- **macOS**: `~/Library/Application Support/jesseduffield/lazygit/config.yml`
- **Linux**: `~/.config/jesseduffield/lazygit/config.yml`
- **Windows**: `%APPDATA%\jesseduffield\lazygit\config.yml`

### Repository-Specific Configs

**Project-level overrides:**
- `.lazygit.yml` in any parent directory (applies to child repos)
- `<repo>/.git/lazygit.yml` (repo-specific only)

**Precedence**: Repo configs override global configs

### Quick Access

Press `e` in lazygit's Status panel to edit config directly.

## Configuration Structure

Lazygit config uses YAML organized into major sections:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/jesseduffield/lazygit/master/schema/config.json

gui:
  # Visual appearance, themes, UI elements

git:
  # Git behavior, pagers, diffing, merging

os:
  # External commands (editor, opener, clipboard)

keybinding:
  # Universal and context-specific key mappings

customCommands:
  # User-defined git commands and workflows
```

**Best practice**: Only include settings you want to change from defaults.

## Delta Integration (Recommended)

Delta is a syntax-highlighting pager that dramatically improves diff readability.

### Quick Setup

**1. Install delta:**
```bash
# macOS (Homebrew)
brew install git-delta

# Nix
nix profile install nixpkgs#delta

# Add to your flake.nix
packages = [ pkgs.delta ];
```

**2. Configure lazygit:**

Add to `config.yml`:

```yaml
git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never
```

**3. Configure delta in ~/.gitconfig:**

```ini
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    line-numbers = true
    side-by-side = false
    syntax-theme = Monokai Extended
```

### Advanced Delta Setup

**Multiple pagers (cycle with `|` key):**

```yaml
git:
  paging:
    colorArg: always
    pager: delta --dark --paging=never --line-numbers
  pagers:
    - pager: delta --dark --paging=never --line-numbers
    - pager: delta --dark --paging=never --side-by-side
    - pager: diff-so-fancy
```

**Delta with hyperlinks (clickable line numbers):**

```yaml
git:
  paging:
    pager: delta --dark --paging=never --line-numbers --hyperlinks --hyperlinks-file-link-format="lazygit-edit://{path}:{line}"
```

**External diff tool (difftastic, difft):**

```yaml
git:
  pagers:
    - pager: delta --dark --paging=never
    - externalDiffCommand: difft --color=always
```

## Delta Configuration

Delta is configured via `~/.gitconfig`, not lazygit's config.yml.

### Basic Delta Settings

```ini
[delta]
    # Enable features
    navigate = true           # n/N to jump between files
    line-numbers = true       # Show line numbers
    hyperlinks = true         # Clickable file paths

    # Appearance
    dark = true              # Dark mode (or light = true)
    syntax-theme = Monokai Extended

    # Layout
    side-by-side = false     # Unified diff (true for split view)

    # Decorations
    file-style = bold yellow
    file-decoration-style = yellow ul
    hunk-header-style = file line-number syntax
```

### Popular Delta Themes

Available themes (check with `delta --list-syntax-themes`):
- **Dark**: `Monokai Extended`, `Nord`, `OneHalfDark`, `Dracula`
- **Light**: `GitHub`, `OneHalfLight`, `Solarized (light)`

**Set theme:**
```ini
[delta]
    syntax-theme = Nord
```

### Delta Features (Presets)

Delta supports feature presets:

```ini
[delta]
    features = decorations navigate

[delta "decorations"]
    file-style = bold yellow ul
    file-decoration-style = none
    hunk-header-decoration-style = blue box

[delta "navigate"]
    navigate = true
```

### Side-by-Side Mode

```ini
[delta]
    side-by-side = true
    line-numbers-left-format = ""
    line-numbers-right-format = "│ "
```

## Common Lazygit Configurations

### Git Settings

```yaml
git:
  # Paging (covered above)
  paging:
    colorArg: always
    pager: delta --dark --paging=never

  # Main branches
  mainBranches:
    - master
    - main

  # Auto-refresh
  autoFetch: true
  autoRefresh: true
  fetchInterval: 60  # seconds

  # Commit behavior
  commit:
    signOff: false
    autoWrapCommitMessage: true
    autoWrapWidth: 72

  # Merging
  merging:
    manualCommit: false
    args: ""

  # Log
  log:
    order: topo-order  # or date-order
    showGraph: always
    showWholeGraph: false

  # Diffing
  diff:
    pager: ""  # Uses git.paging.pager if empty
```

### GUI Settings

```yaml
gui:
  # Theme
  theme:
    activeBorderColor:
      - green
      - bold
    inactiveBorderColor:
      - default
    selectedLineBgColor:
      - blue
    selectedRangeBgColor:
      - blue

  # Window management
  windowSize: normal  # normal, half, full
  sidePanelWidth: 0.3333
  expandFocusedSidePanel: false
  mainPanelSplitMode: flexible  # flexible or horizontal

  # Display
  showFileTree: true
  showListFooter: true
  showRandomTip: false
  showCommandLog: true
  showBottomLine: true
  showBranchCommitHash: false

  # Scroll behavior
  scrollHeight: 2
  scrollPastBottom: true
  scrollOffMargin: 2
  scrollOffBehavior: margin  # margin or jump

  # Mouse support
  mouse: true

  # Commit length
  commitLength:
    show: true

  # Skip hooks
  skipDiscardChangeWarning: false
  skipStashWarning: false
  skipNoStagedFilesWarning: false
  skipRewordInEditorWarning: false
```

### OS Settings

```yaml
os:
  # Editor (uses $GIT_EDITOR, $VISUAL, $EDITOR in that order if not set)
  edit: "nvim {{filename}}"
  editAtLine: "nvim +{{line}} {{filename}}"
  editAtLineAndWait: "nvim +{{line}} {{filename}}"

  # Open command
  open: "open {{filename}}"
  openLink: "open {{link}}"

  # Clipboard
  copyToClipboardCmd: ""  # Auto-detected if empty
```

### Keybindings

**Universal keybindings:**

```yaml
keybinding:
  universal:
    quit: 'q'
    quit-alt1: '<c-c>'
    return: '<esc>'
    quitWithoutChangingDirectory: 'Q'
    togglePanel: '<tab>'
    prevItem: '<up>'
    nextItem: '<down>'
    prevItem-alt: 'k'
    nextItem-alt: 'j'
    prevPage: ','
    nextPage: '.'
    scrollLeft: 'H'
    scrollRight: 'L'
    gotoTop: '<'
    gotoBottom: '>'
    prevBlock: '<left>'
    nextBlock: '<right>'
    prevBlock-alt: 'h'
    nextBlock-alt: 'l'
    nextMatch: 'n'
    prevMatch: 'N'
    startSearch: '/'
    optionMenu: 'x'
    optionMenu-alt1: '?'
    select: '<space>'
    goInto: '<enter>'
    remove: 'd'
    new: 'n'
    edit: 'e'
    openFile: 'o'
    scrollUpMain: '<pgup>'
    scrollDownMain: '<pgdown>'
    scrollUpMain-alt1: 'K'
    scrollDownMain-alt1: 'J'
    scrollUpMain-alt2: '<c-u>'
    scrollDownMain-alt2: '<c-d>'
    executeCustomCommand: ':'
    createRebaseOptionsMenu: 'm'
    pushFiles: 'P'
    pullFiles: 'p'
    refresh: 'R'
    createPatchOptionsMenu: '<c-p>'
    nextTab: ']'
    prevTab: '['
    nextScreenMode: '+'
    prevScreenMode: '_'
    undo: 'z'
    redo: '<c-z>'
    filteringMenu: '<c-s>'
    diffingMenu: 'W'
    diffingMenu-alt: '<c-e>'
    copyToClipboard: '<c-o>'
```

**Context-specific keybindings:**

```yaml
keybinding:
  files:
    commitChanges: 'c'
    commitChangesWithoutHook: 'w'
    amendLastCommit: 'A'
    commitChangesWithEditor: 'C'
    findBaseCommitForFixup: '<c-f>'
    confirmDiscard: 'x'
    ignoreFile: 'i'
    refreshFiles: 'r'
    stashAllChanges: 's'
    viewStashOptions: 'S'
    toggleStagedAll: 'a'
    viewResetOptions: 'D'
    fetch: 'f'
    toggleTreeView: '`'
    openMergeTool: 'M'
    openStatusFilter: '<c-b>'

  branches:
    createPullRequest: 'o'
    viewPullRequestOptions: 'O'
    copyPullRequestURL: '<c-y>'
    checkoutBranchByName: 'c'
    forceCheckoutBranch: 'F'
    rebaseBranch: 'r'
    renameBranch: 'R'
    mergeIntoCurrentBranch: 'M'
    viewGitFlowOptions: 'i'
    fastForward: 'f'
    createTag: 'T'
    pushTag: 'P'
    setUpstream: 'u'
    fetchRemote: 'f'
```

## Custom Commands

Add custom git workflows:

```yaml
customCommands:
  - key: 'C'
    command: 'git cz'
    description: 'commit with commitizen'
    context: 'files'
    loadingText: 'opening commitizen commit tool'
    subprocess: true

  - key: 'p'
    command: 'git push --force-with-lease'
    description: 'push with lease'
    context: 'global'
    loadingText: 'pushing...'

  - key: 'T'
    prompts:
      - type: 'input'
        title: 'Tag name'
        key: 'TagName'
      - type: 'input'
        title: 'Tag message'
        key: 'TagMessage'
    command: 'git tag -a {{.Form.TagName}} -m "{{.Form.TagMessage}}"'
    description: 'Create annotated tag'
    context: 'commits'
```

## Common Workflows

### Setup Lazygit from Scratch

**1. Check current config location:**
```bash
# macOS
ls -la ~/Library/Application\ Support/lazygit/
# Linux
ls -la ~/.config/lazygit/
```

**2. Create config file:**
Use Write tool to create config at appropriate path.

**3. Install delta:**
Add to your `flake.nix` or install via package manager.

**4. Configure delta in ~/.gitconfig:**
Use Edit tool to add delta settings.

**5. Test:**
```bash
lazygit
# Press 'e' in status panel to verify config
# Use '|' to cycle between pagers if multiple configured
```

### Migrate Existing Config

**1. Read current config:**
```bash
# Find config location
lazygit --print-config-dir

# macOS example
cat ~/Library/Application\ Support/lazygit/config.yml
```

**2. Add delta integration:**
Merge delta pager settings into existing config.

**3. Backup before changes:**
```bash
cp ~/Library/Application\ Support/lazygit/config.yml \
   ~/Library/Application\ Support/lazygit/config.yml.backup
```

### Repository-Specific Overrides

**Use case**: Different pager for work vs personal repos

**Create `.lazygit.yml` in parent directory:**

```yaml
# ~/Code/work/.lazygit.yml
git:
  paging:
    pager: delta --light --paging=never --side-by-side
```

All repos under `~/Code/work/` inherit these settings.

## Troubleshooting

### Delta Not Working

**Check installation:**
```bash
which delta
delta --version
```

**Verify git config:**
```bash
git config --global core.pager
git config --global interactive.diffFilter
```

**Test delta directly:**
```bash
git diff | delta
```

**Check lazygit pager setting:**
```bash
lazygit --print-config-dir
cat "$(lazygit --print-config-dir)/config.yml" | grep -A 5 paging
```

### Colors Not Showing

**Ensure `colorArg: always`:**
```yaml
git:
  paging:
    colorArg: always
```

**Check terminal color support:**
```bash
echo $TERM  # Should be xterm-256color or similar
```

### Config Not Loading

**Check file location:**
```bash
lazygit --print-config-dir
```

**Validate YAML syntax:**
```bash
# Use yq or Python to validate
yq eval . config.yml
# or
python3 -c "import yaml; yaml.safe_load(open('config.yml'))"
```

**Check for schema errors:**
Add schema directive at top of config.yml:
```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/jesseduffield/lazygit/master/schema/config.json
```

IDE will highlight errors if schema is loaded.

## Output Instructions

When helping with lazygit configuration:

### 1. Determine User's Platform
```bash
uname  # Darwin (macOS), Linux, Windows
```

Set correct config path based on platform.

### 2. Check Existing Config
```bash
lazygit --print-config-dir
# Read current config if it exists
```

Use Read tool to check existing settings before making changes.

### 3. Delta Integration Priority
- Always suggest delta as the default pager (best experience)
- Provide gitconfig delta setup alongside lazygit config
- Include side-by-side option for users who prefer it

### 4. Use Appropriate Tools
- **Read**: Check existing configs (lazygit and gitconfig)
- **Write**: Create new config files
- **Edit**: Modify existing configs (safer than overwriting)
- **Bash**: Test delta, verify installation, check config location

### 5. Provide Complete Configs
- Include schema directive for IDE support
- Only include changed settings (don't copy entire default config)
- Add comments explaining non-obvious settings
- Test configs are valid YAML

### 6. Consider Project Context
- Check if delta is in `flake.nix` packages
- Verify git is configured properly
- Respect existing editor settings (nvim, vim, etc.)
- Follow dotfiles structure (config/ directory, symlinks)

### 7. Validation Steps
After making config changes:
1. Validate YAML syntax
2. Test delta works standalone: `git diff | delta`
3. Launch lazygit and verify pager works
4. Test pager cycling with `|` if multiple pagers configured

## Related Tools

**Other pagers to consider:**
- **diff-so-fancy**: Colorful diffs with good defaults
- **difftastic**: Structural diff tool (compares syntax trees)
- **delta alternatives**: bat (syntax highlighting), colordiff

**Complementary tools:**
- **commitizen**: Structured commit messages
- **git-absorb**: Automatic fixup commits
- **git-branchless**: Advanced rebasing workflows

## Reference Documentation

- Lazygit config docs: https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md
- Custom pagers: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Pagers.md
- Delta configuration: https://dandavison.github.io/delta/configuration.html
- Delta GitHub: https://github.com/dandavison/delta
