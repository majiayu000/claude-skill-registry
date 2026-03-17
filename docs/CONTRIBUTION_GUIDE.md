# Skill Registry 收录指南

本文档说明社区提交如何被审核和收录到 Claude Skills Registry。

## 实体类型

Registry 有两种实体：

| 类型 | 说明 | 收录方式 |
|------|------|----------|
| **Skill** | 单个 SKILL.md 文件 | 自动爬取 |
| **Collection** | 技能包（多个 skills + commands + hooks） | 手动审核 |

## Skill 收录流程

### 自动爬取（主要途径）

Registry 通过 GitHub Code Search 和预设仓库列表自动发现 SKILL.md 文件。

**被收录的条件：**
1. 仓库中存在标准的 `SKILL.md` 文件
2. SKILL.md 大于 50 字符
3. 有 YAML frontmatter（`name` 和 `description` 字段）

**爬取源：**
- `scripts/clone_and_import.py` 中的 `REPOS_TO_CLONE` 列表
- GitHub Code Search API 自动发现（`scripts/discover_by_topic.py`）
- 社区贡献的 awesome-list 仓库

**分类规则：**
1. 优先使用 SKILL.md frontmatter 中的 `category` 字段
2. 无 category 时根据关键词自动猜测（`guess_category()`）
3. 都没有时归入 `other`

### 手动提交

通过 [GitHub Issues](https://github.com/majiayu000/claude-skill-registry/issues) 提交。

如果提交的是单个 skill 且仓库中有标准 SKILL.md：
1. 将仓库 URL 加入 `REPOS_TO_CLONE`
2. 下一次爬取周期自动收录

## Collection 收录流程

Collection 是打包的技能套件，包含多个 skills、commands、hooks 等。

### 判断标准：何时用 Collection 而非多个 Skill

| 信号 | → 收录为 |
|------|----------|
| 仓库中有 1 个独立 SKILL.md | Skill |
| 仓库中有多个**无关联**的 SKILL.md | 多个独立 Skill |
| 仓库中有多个**内聚**的 SKILL.md，共享安装命令 | Collection |
| 提供 `npx` / 一键安装，捆绑 skills + commands + hooks | Collection |
| 同一个 skill 在仓库中存在多个副本（template/plugin/...） | Collection（避免重复） |

### 提交要求

通过 GitHub Issues 提交，需包含：
- 仓库 URL
- 安装命令
- 包含的 skills 列表
- 包含的 commands 列表（如有）
- 类别和标签

### 审核流程

1. **验证仓库**：clone 并确认 SKILL.md 文件存在且质量合格
2. **安全扫描**：通过 `scripts/security_scanner.py` 检查
3. **分类决策**：根据上方判断标准决定收录为 Skill 还是 Collection
4. **写入源文件**：手动添加到 `sources/collections.json`
5. **构建验证**：运行 `rebuild_registry.py` 和 `build_search_index.py` 确认输出正确
6. **关闭 Issue**：回复提交者收录结果

### 源文件格式

Collections 维护在 `sources/collections.json`：

```json
{
  "collections": [
    {
      "name": "collection-name",
      "description": "简短描述",
      "repo": "owner/repo",
      "category": "product",
      "tags": ["tag1", "tag2"],
      "install": "npx package-name@latest",
      "homepage": "https://...",
      "author": "github-username",
      "skills": ["skill-a", "skill-b"],
      "commands": ["/cmd:a", "/cmd:b"],
      "hooks": ["pre-tool-use"],
      "source_url": "https://github.com/owner/repo",
      "license": "MIT"
    }
  ]
}
```

Schema 定义：`schema/collection.schema.json`

## 去重策略

- Skill 级别：`repo:path` 作为唯一键去重
- Collection 级别：`name` 唯一，不与 skill 条目合并
- Collection 内的子 skill **不会**被拆解为独立 skill 条目（避免膨胀）

## 分类列表

`development` | `testing` | `data` | `design` | `documents` | `productivity` | `devops` | `security` | `marketing` | `product` | `communication` | `creative`
