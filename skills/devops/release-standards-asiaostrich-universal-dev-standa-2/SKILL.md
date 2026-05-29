---
name: release
scope: universal
description: "[UDS] Guide release process and changelogs"
allowed-tools: Read, Write, Grep, Bash(git:*), Bash(npm version:*)
argument-hint: "[version]"
disable-model-invocation: true
---

# Release Assistant | 發布助手

Guide the release process following Semantic Versioning and changelog best practices.

引導遵循語義化版本和變更日誌最佳實踐的發布流程。

## Subcommands | 子命令

| Subcommand | Description | 說明 |
|------------|-------------|------|
| `start` | Start a release branch/process | 開始發布流程 |
| `finish` | Finalize release (tag, merge) | 完成發布（標籤、合併） |
| `changelog` | Generate or update CHANGELOG.md | 產生或更新變更日誌 |
| `check` | Run pre-release verification | 執行發布前檢查 |

## Version Types | 版本類型

| Type | Pattern | npm Tag | 用途 |
|------|---------|---------|------|
| Stable | `X.Y.Z` | `@latest` | Production release | 正式版 |
| Beta | `X.Y.Z-beta.N` | `@beta` | Public testing | 公開測試 |
| Alpha | `X.Y.Z-alpha.N` | `@alpha` | Internal testing | 內部測試 |
| RC | `X.Y.Z-rc.N` | `@rc` | Release candidate | 候選版本 |

## Workflow | 工作流程

1. **Determine version** - Decide version type based on changes (MAJOR/MINOR/PATCH)
2. **Update version files** - Update package.json and related version references
3. **Update CHANGELOG** - Move [Unreleased] entries to new version section
4. **Run pre-release checks** - Verify tests, lint, and standards compliance
5. **Create git tag** - Tag with `vX.Y.Z` format
6. **Commit and push** - Commit version bump and push tags

### Version Increment Rules | 版本遞增規則

| Change Type | Increment | Example |
|-------------|-----------|---------|
| Breaking changes | MAJOR | 1.9.5 → 2.0.0 |
| New features (backward-compatible) | MINOR | 2.3.5 → 2.4.0 |
| Bug fixes (backward-compatible) | PATCH | 3.1.2 → 3.1.3 |

## Usage | 使用方式

- `/release start 1.2.0` - Start release process for v1.2.0
- `/release changelog 1.2.0` - Update CHANGELOG for v1.2.0
- `/release finish 1.2.0` - Finalize and tag v1.2.0
- `/release check` - Run pre-release verification

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [versioning.md](../../core/versioning.md)
