---
name: neovim
description: Neovim text editor installation and LazyVim setup configuration.
---

# Neovim — Setup Guide

**Install on Windows**

```powershell
winget install Neovim.Neovim
```

**LazyVim Setup**

```powershell
Move-Item $env:LOCALAPPDATA\nvim $env:LOCALAPPDATA\nvim.bak
git clone https://github.com/LazyVim/starter $env:LOCALAPPDATA\nvim
Remove-Item $env:LOCALAPPDATA\nvim\.git -Recurse -Force
nvim
```

🔗 [LazyVim Extras](https://www.lazyvim.org/extras) | [Java Setup Guide](https://github.com/nvim-java/nvim-java/wiki/Lazyvim)