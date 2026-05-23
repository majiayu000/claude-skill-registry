---
name: install
description: Use when the user asks to install, add, or set up a package, tool, CLI, or application
argument-hint: [package-name...]
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
  - Edit(home/dot_config/mise/config.toml)
  - Edit(home/.chezmoidata/packages.yaml)
  - Bash(mise registry:*)
  - Bash(mise ls-remote:*)
  - Bash(gh release view:*)
  - Bash(npm view:*)
  - Bash(pip index:*)
  - Bash(chezmoi diff:*)
---

# Package Installation Skill

## Arguments

`$ARGUMENTS`: Space-separated package names to install.

## Workflow

**When to escalate:** For complex backend decisions, version conflicts, or security concerns, consult the Package Manager subagent.

For each package in `$ARGUMENTS`:

### 1. Identify Package Type

Check in order:

1. **Mise registry:**
   ```bash
   mise registry | grep -i <package>
   ```

2. **Known GUI/system apps:** GUI applications → cask, system utilities → brew

**Package type mapping:**

| Package Type | Format |
|-------------|---------|
| Aqua registry | `"aqua:owner/repo" = "version"` |
| GitHub releases | `"github:owner/repo" = "version"` |
| Python CLI | `"pipx:package" = "version"` |
| Node.js CLI | `"npm:package" = "version"` |
| GUI app | Add to casks list |
| System utility | Add to brews list |

### 2. Discover Latest Version

**GitHub tools (aqua/github):**
```bash
gh release view --repo <owner>/<repo> --json tagName --jq .tagName
```

**npm:**
```bash
npm view <package> version
```

**PyPI:**
```bash
pip index versions <package> 2>/dev/null | head -1
```

**Native mise:**
```bash
mise ls-remote <tool> | tail -1
```

### 3. Add to Manifest

**Mise tools** → `home/dot_config/mise/config.toml`:
- Add under `[tools]` section
- Use backend prefix
- Pin exact version
- Follow comment organization (Runtimes, Aqua, GitHub, Python, Node)

**Homebrew** → `home/.chezmoidata/packages.yaml`:
- Add to `packages.darwin.brews` or `packages.darwin.casks`
- Follow alphabetical order

### 4. Verify

```bash
chezmoi diff
```

Expected: Only the intended manifest file changed. If unrelated changes appear, investigate.

### 5. Apply

**Requires user approval:**
```bash
chezmoi apply
```

**CRITICAL:** Always run `chezmoi apply` with no arguments. This triggers `run_onchange_00-install-mise-tools.sh.tmpl` which runs `mise install`. Targeted apply (`chezmoi apply <file>`) skips this script.

If the diff shows unrelated changes, ask the user how to proceed - do NOT attempt a partial apply.

### 6. Commit

```bash
git add <manifest-file>
git commit -m "feat: add <package-name>"
```

---

After all packages: Ask user "All packages installed and committed. Push to origin?"

## Rules

- Mise > Homebrew for dev tools; aqua > other mise backends
- Exact versions only (no `latest`, ranges, wildcards)
- One commit per package
- Edit source files in `home/` only

## Reference

See `docs/package-management.md` for complete backend documentation.
