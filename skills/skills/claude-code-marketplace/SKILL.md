---
name: claude-code-marketplace
description: 管理 claude-code-marketplace 插件商城的版本升级，包括更新版本号、编写更新日志和同步 CHANGELOG。在用户要求升级插件版本、更新插件商城、发布新版本或编写更新日志时使用。触发关键词：claude-code-marketplace、插件升级、版本更新、发布插件、更新日志。
metadata:
  version: "0.13.4"
---

# Claude Code 插件商城版本升级助手

本技能用于自动化处理 claude-code-marketplace 插件商城的版本升级流程，确保版本号一致性和更新日志的完整性。

## 使用场景

当遇到以下情况时使用本技能：

- 需要发布 claude-code-marketplace 的新版本
- 更新插件商城的版本号
- 编写或更新插件的 CHANGELOG
- 同步多个配置文件中的版本号

## 核心职责

1. **版本号管理**：确保所有相关文件中的版本号保持一致
2. **更新日志维护**：编写符合规范的版本更新说明
3. **文件同步**：自动更新所有必要的配置文件

## 相关文件目录

插件商城的核心文件位于以下目录：

- `.claude-plugin` - 插件商城根配置目录
- `claude-code-marketplace/common-tools` - 插件工具包目录

## 需要更新版本号的文件

执行版本升级时，**必须**同步更新以下文件中的版本号：

1. `.claude-plugin/marketplace.json` - 插件商城主配置文件
2. `claude-code-marketplace/common-tools/.claude-plugin/plugin.json` - 插件配置文件

### Skills 文档的 metadata.version 字段

除了上述配置文件外，每次版本升级时还**必须**同步更新所有 skills 文档的 `metadata.version` 字段。

**需要更新的 skills 文档列表**：

> **重要提示**：在执行更新前，必须先扫描 `claude-code-marketplace/common-tools/skills` 目录下的所有 `SKILL.md` 文件，确保没有遗漏任何技能。

通常包括（但不限于）：

- `claude-code-marketplace/common-tools/skills/openspec/SKILL.md`
- `claude-code-marketplace/common-tools/skills/init-prettier-git-hooks/SKILL.md`
- `claude-code-marketplace/common-tools/skills/init-claude-code-statusline/SKILL.md`
- `claude-code-marketplace/common-tools/skills/init-ai-md/SKILL.md`
- `claude-code-marketplace/common-tools/skills/nitro-api-development/SKILL.md`
- `claude-code-marketplace/common-tools/skills/git-commit/SKILL.md` (如有)

**metadata.version 字段格式**：

```yaml
---
name: skill-name
description: 技能描述
metadata:
  version: "X.Y.Z"
---
```

**更新规则**：

- **原则上独立管理**：每个 Skill 应当有自己独立的版本号，不强制与插件商城版本（marketplace version）保持一致，除非该 Skill 确实发生了变更。
- **按需更新**：仅当 Skill 的内容、功能或文档发生变更时，才更新其 `metadata.version`。
- **发布一致性（可选）**：如果本次发布是一次整体的大版本更新（Major update），或者是为了保持整齐划一（虽然不推荐），可以统一更新所有 Skills 的版本号，但这**不是强制要求**。
- **默认策略**：默认情况下，**只更新发生了实际变更的 Skill 的版本号**。

### 版本号格式

遵循语义化版本规范（Semantic Versioning）：

- `MAJOR.MINOR.PATCH` 格式（例如：`1.2.3`）
- MAJOR：不兼容的 API 修改
- MINOR：向下兼容的功能性新增
- PATCH：向下兼容的问题修正

## 更新日志文件

每次版本更新的内容**必须**记录在以下文件中：

- `claude-code-marketplace/common-tools/CHANGELOG.md`

### 更新日志格式规范

遵循 [Keep a Changelog](https://keepachangelog.com/) 规范：

```markdown
## [版本号] - YYYY-MM-DD

### Added

- 新增的功能

### Changed

- 变更的功能

### Deprecated

- 即将废弃的功能

### Removed

- 已移除的功能

### Fixed

- 修复的问题

### Security

- 安全相关的修复
```

## 升级流程步骤

执行插件版本升级时，请按照以下顺序操作：

1. **确定新版本号**
   - 根据变更类型确定版本号增量（MAJOR/MINOR/PATCH）
   - 确认新版本号符合语义化版本规范

2. **更新配置文件**
   - 更新 `.claude-plugin/marketplace.json` 中的 version 字段
   - 更新 `claude-code-marketplace/common-tools/.claude-plugin/plugin.json` 中的 version 字段

3. **更新 Skills 版本（按需）**
   - 检查哪些 Skill 发生了变更
   - 仅更新发生变更的 Skill 的 `metadata.version`
   - 如果是新增 Skill，确保其初始版本号设置正确（通常为 0.0.1 或 0.1.0）

4. **编写更新日志**
   - 在 `CHANGELOG.md` 文件顶部添加新版本条目
   - 使用标准的 changelog 分类（Added/Changed/Fixed 等）
   - 记录本次更新的所有变更内容
   - 添加发布日期

5. **验证一致性**
   - 检查所有配置文件中的版本号是否一致
   - 检查 CHANGELOG 格式是否符合规范
   - 确认所有变更都已记录

6. **提交变更**
   - 使用规范的 commit message
   - 推荐格式：`chore(plugin): release version X.Y.Z`

## 示例

### 示例 1：发布补丁版本（仅修复插件逻辑）

假设当前版本为 `1.2.3`，修复了一个 bug，需要发布 `1.2.4`，且没有 Skill 变更。

**步骤**：

1. 更新两个 JSON 配置文件中的 version 为 `"1.2.4"`
2. Skills 文档版本号**保持不变**
3. 在 CHANGELOG.md 添加：

   ```markdown
   ## [1.2.4] - 2025-01-05

   ### Fixed

   - 修复插件加载时的路径解析错误
   ```

4. 提交：`chore(plugin): release version 1.2.4`

### 示例 2：发布功能版本（新增/修改 Skill）

假设当前版本为 `1.2.4`，新增了一个 `git-commit` 技能，需要发布 `1.3.0`。

**步骤**：

1. 更新两个 JSON 配置文件中的 version 为 `"1.3.0"`
2. 设置 `skills/git-commit/SKILL.md` 的 `metadata.version` 为 `"0.0.1"` (或其他初始版本)
3. 其他 Skills 版本号**保持不变**
4. 在 CHANGELOG.md 添加：

   ```markdown
   ## [1.3.0] - 2025-01-05

   ### Added

   - 新增 `git-commit` 技能，用于规范化 git 提交
   ```

5. 提交：`chore(plugin): release version 1.3.0`

## 注意事项

1. **版本号一致性**：`marketplace.json` 和 `plugin.json` 的版本号必须一致。
2. **Skills 独立版本**：Skills 拥有独立的生命周期，不要盲目同步所有 Skills 的版本号。
3. **CHANGELOG 完整性**：每次发布都必须更新 CHANGELOG，不能遗漏。
4. **语义化版本**：严格遵循语义化版本规范，让用户清楚了解变更影响。
5. **日期格式**：使用 ISO 8601 格式（YYYY-MM-DD）。
6. **变更分类**：准确使用 changelog 分类，帮助用户快速定位关注的内容。

## 相关资源

- [语义化版本规范](https://semver.org/lang/zh-CN/)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/)
