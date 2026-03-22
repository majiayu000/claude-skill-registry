---
name: managing-starship-fork
description: Sync, build, and install the custom starship fork with jj support. Use when updating starship, rebuilding the binary, syncing with upstream, or modifying the jj_status module.
---

# Starship Fork Management

Manage the custom starship fork at `~/Projects/starship` (origin: `TrevorS/starship`, upstream: `starship/starship`). The fork adds a `jj_status` module for Jujutsu VCS support on branch `claude/add-jujutsu-support-JuqjU`.

## Repo Layout

- **Origin:** `TrevorS/starship` (the fork)
- **Upstream:** `starship/starship`
- **Feature branch:** `claude/add-jujutsu-support-JuqjU`
- **Binary install path:** `~/.local/bin/starship`
- **Config:** `~/.config/starship.toml` (stowed from `~/.claude/dotfiles/starship/`)

## Sync with Upstream and Rebuild

```bash
cd ~/Projects/starship

# Sync master
git fetch upstream
git checkout master
git merge upstream/master --ff-only
git push origin master

# Rebase feature branch
git checkout claude/add-jujutsu-support-JuqjU
git rebase master

# Build and install
cargo build --release
cp target/release/starship ~/.local/bin/starship

# Push rebased branch
git push origin claude/add-jujutsu-support-JuqjU --force-with-lease
```

## Quick Rebuild (No Sync)

When you've made local changes and just want to rebuild:

```bash
cd ~/Projects/starship
cargo build --release
cp target/release/starship ~/.local/bin/starship
```

## Verify

```bash
starship --version        # Should show branch name in output
starship module jj_status # Test in a jj repo — should print change ID
```

## The jj_status Module

Source files in the fork:

- `src/modules/jj_status.rs` — module implementation (change ID, bookmarks, conflict/divergent/hidden flags)
- `src/configs/jj_status.rs` — config struct and defaults
- `src/modules/vcs.rs` — VCS discovery (detects `.jj/` directory)
- `docs/config/README.md` — user-facing documentation

Config in `starship.toml`:

```toml
[jj_status]
disabled = false           # Module is disabled by default
truncation_length = 12     # Change ID display length
style = "bold purple"
symbol = "jj "
conflicted = "x"           # Shown when working copy has conflicts
divergent = "?"            # Shown when change is divergent
hidden = "o"               # Shown when change is hidden
ignore_working_copy = true # Skip auto-snapshot for faster prompts
```

## Running Tests

```bash
cd ~/Projects/starship
cargo test jj              # Run jj-related tests only
cargo test                 # Run full test suite (slow)
```

## Notes

- Do NOT open PRs against upstream without explicit approval
- The fork's master should always be a clean fast-forward of upstream
- All custom work lives on the feature branch
- Build takes ~90s on first compile, incremental builds are much faster
