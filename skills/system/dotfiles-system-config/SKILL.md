---
name: dotfiles-system-config
description: Use when making system configuration changes - decides if changes belong in dotfiles and where
---

# System Configuration

When making system configuration changes:

1. **Should this go in dotfiles?** Persist across machines → dotfiles, not direct system changes

2. **Where in dotfiles?**
   | Config Type | Location |
   |-------------|----------|
   | Shell | `fish/` |
   | Git | `git/` |
   | Editor | `zed/`, `nvim/`, `vim/` |
   | Homebrew | `Brewfile` |
   | npm globals | `npm/global-packages.txt` |
   | macOS settings | `sync` script (defaults) |
   | New tools | subdirectory + `sync` updates |

3. **Update sync script** - New config directories need linking rules
