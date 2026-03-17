---
name: changelog
description: Read and parse CHANGELOG.md for version info and release notes. Use when user asks about latest version, version history, release notes, or changelog content. Triggers on "latest version", "changelog", "release notes", "version log".
---

# Changelog 工具

解析 CHANGELOG.md 获取版本号和版本日志。

## Dart 脚本（需要 dart 环境）

### 获取最新版本号

```bash
dart run <skill_path>/scripts/latest_version.dart [changelog_path]
```

### 获取特定版本日志

```bash
dart run <skill_path>/scripts/version_log.dart [version] [changelog_path]
```

不指定版本时默认输出最新版本的日志。

## Shell 脚本（适用于 CI，无需 dart）

### 获取最新版本号

```bash
<skill_path>/scripts/latest_version.sh [changelog_path]
```

### 获取特定版本日志

```bash
<skill_path>/scripts/version_log.sh [version] [changelog_path]
```

## 参数说明

- `changelog_path`（可选）：CHANGELOG.md 路径，默认为 CHANGELOG.md
- `version`（可选）：版本号（如 `0.3.0`），不指定则使用最新版本
