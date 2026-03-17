---
name: zls-integration
description: "zls-integration skill"
  Zig Language Server (ZLS) integration for IDE features - autocomplete, goto definition,
  diagnostics, hover docs, and build-on-save. Use when setting up ZLS, debugging LSP issues,
  or optimizing Zig development workflows. Pairs with zig-programming skill.
version: 1.0.0
trit: 0
---

# ZLS Integration Skill

Zig Language Server (ZLS) provides IDE features for Zig development. This skill covers installation, configuration, build-on-save diagnostics, and troubleshooting.

## Quick Reference

| Feature | ZLS Support | Notes |
|---------|-------------|-------|
| Autocomplete | ✓ Full | Includes comptime-aware completion |
| Goto Definition | ✓ Full | Cross-file navigation |
| Find References | ✓ Full | All usages in workspace |
| Hover Documentation | ✓ Full | Inline docs from source |
| Diagnostics | ⚡ Parser-level | Semantic via build-on-save |
| Rename Symbol | ✓ Full | Safe refactoring |
| Code Actions | ✓ Partial | Fix imports, remove unused |
| Formatting | ✓ Full | Uses `zig fmt` |

## Installation

### Via Package Manager (Recommended)

```bash
# macOS (Homebrew)
brew install zls

# Nix/Flox
flox install zls

# Arch Linux
pacman -S zls

# From source (any platform)
git clone https://github.com/zigtools/zls
cd zls
zig build -Doptimize=ReleaseSafe
```

### Version Compatibility

| Zig Version | ZLS Version | Notes |
|-------------|-------------|-------|
| 0.15.x | 0.15.x | Current stable |
| 0.14.x | 0.14.x | Previous stable |
| 0.13.x | 0.13.x | Legacy |
| master | master | Build from source |

**Always match ZLS version to Zig version.**

## Configuration

### zls.json Location

```
~/.config/zls.json           # Linux/macOS
%APPDATA%\zls.json           # Windows
<project>/.zls.json          # Project-specific
```

### Essential Configuration

```json
{
  "zig_exe_path": "/path/to/zig",
  "enable_autofix": true,
  "enable_import_access": true,
  "highlight_global_var_declarations": true,
  "warn_style": true,
  "enable_build_on_save": true,
  "build_on_save_step": "check"
}
```

## Build-On-Save Diagnostics

ZLS can run your build script on save to catch semantic errors (type mismatches, wrong argument counts) that parser-level analysis misses.

### Step 1: Add Check Step to build.zig

```zig
// build.zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(exe);

    // ZLS check step - runs on save
    const check = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    
    const check_step = b.step("check", "Check compilation (for ZLS)");
    check_step.dependOn(&check.step);
}
```

### Step 2: Configure ZLS

```json
{
  "enable_build_on_save": true,
  "build_on_save_step": "check"
}
```

### Step 3: Editor Setup

**VS Code (zls extension):**
```json
// settings.json
{
  "zig.zls.path": "/path/to/zls",
  "zig.zls.enableBuildOnSave": true
}
```

**Neovim (nvim-lspconfig):**
```lua
require('lspconfig').zls.setup({
  settings = {
    zls = {
      enable_build_on_save = true,
      build_on_save_step = "check"
    }
  }
})
```

**Emacs (lsp-mode):**
```elisp
(setq lsp-zig-zls-executable "/path/to/zls")
(setq lsp-zig-enable-build-on-save t)
```

## Troubleshooting

### No Diagnostics Appearing

1. Verify ZLS is running: `pgrep -l zls`
2. Check ZLS log: `~/.cache/zls/zls.log`
3. Ensure Zig version matches: `zig version` vs `zls --version`
4. Test build manually: `zig build check`

### Slow Completions

```json
{
  "skip_std_references": true,
  "prefer_ast_check_as_child_process": true
}
```

### Import Resolution Failures

```json
{
  "enable_import_access": true,
  "additional_module_paths": ["deps/", "vendor/"]
}
```

### Build-On-Save Not Working

1. Verify `check` step exists in build.zig
2. Run `zig build check` manually
3. Check ZLS config: `enable_build_on_save: true`
4. Restart language server

## GF(3) Integration

ZLS diagnostics map to triadic workflow:

| Diagnostic Type | Trit | Action |
|-----------------|------|--------|
| Error (red) | -1 | Must fix before build |
| Warning (yellow) | 0 | Review, may ignore |
| Hint (blue) | +1 | Optimization opportunity |

Conservation: `errors + warnings + hints → 0` as code improves.

## Editor Integration Matrix

| Editor | Plugin | Config Path |
|--------|--------|-------------|
| VS Code | zls (extension) | `.vscode/settings.json` |
| Neovim | nvim-lspconfig | `init.lua` or `lsp.lua` |
| Helix | Built-in | `languages.toml` |
| Emacs | lsp-mode + lsp-zig | `init.el` |
| Sublime | LSP-zig | `*.sublime-settings` |
| Vim | vim-lsp or coc.nvim | `.vimrc` or `coc-settings.json` |

## Related Skills

- `zig-programming` - Core Zig language and stdlib
- `zig-async-io` - Async/concurrent patterns (0.16.0+)
- `tree-sitter` - AST-based code analysis

## Resources

- [ZLS GitHub](https://github.com/zigtools/zls)
- [ZLS Configuration Guide](https://zigtools.org/zls/configure/)
- [Build-On-Save Guide](https://zigtools.org/zls/guides/build-on-save/)
- [Zig BBQ Cookbook](https://cookbook.ziglang.cc/)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
zls-integration (−) + SDF.Ch4 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch6: Layering
- Ch2: Domain-Specific Languages

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.