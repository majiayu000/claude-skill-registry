---
name: skill-factory
description: 自动化工厂，将 GitHub 仓库转换为标准化的 AI Skill。当用户提供 GitHub URL 并希望"打包"、"封装"或"创建 Skill"时使用此工具。支持自动获取仓库元数据、生成标准目录结构、注入生命周期管理所需的扩展元数据。
---

# Skill Factory

将任意 GitHub 仓库一键转换为标准化的 Claude Skill。

## 核心功能

1. **信息获取**: 通过 `git ls-remote` 获取 commit hash，通过 HTTP 获取 README
2. **目录生成**: 创建标准化的 Skill 目录结构（SKILL.md, scripts/, references/, assets/）
3. **元数据注入**: 自动填充扩展元数据字段（source_url, source_hash, version 等）
4. **占位脚本**: 生成 wrapper.py 模板，便于后续实现

## 使用场景

**触发方式**:
- `/skill-factory <github_url>`
- "将这个仓库打包成 Skill: <url>"
- "从 GitHub 创建 Skill: <url>"
- "封装这个工具: <url>"

## 工作流程

### 步骤 1: 获取仓库信息

运行 `scripts/fetch_github_info.py` 获取仓库元数据:

```bash
python scripts/fetch_github_info.py <github_url>
```

输出 JSON 格式:
```json
{
  "name": "repo-name",
  "owner": "owner",
  "url": "https://github.com/owner/repo",
  "latest_hash": "abc123...",
  "default_branch": "main",
  "description": "仓库描述",
  "readme": "README 内容..."
}
```

### 步骤 2: 分析 README

Agent 分析 README 内容，理解:
- 工具的主要功能
- 安装和使用方法
- CLI 参数或 API 接口
- 依赖要求

### 步骤 3: 创建 Skill 目录

运行 `scripts/create_skill.py` 生成目录结构:

```bash
python scripts/create_skill.py <json_file_or_string> <output_dir>
```

生成的目录结构:
```
skill-name/
├── SKILL.md              # 主 Skill 文件（含扩展元数据）
├── scripts/
│   └── wrapper.py        # 占位脚本
├── references/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

### 步骤 4: 完善 Skill

Agent 根据 README 分析结果:
1. 完善 SKILL.md 的描述和使用说明
2. 实现 wrapper.py 的实际逻辑
3. 添加必要的参考文档

### 步骤 5: 验证

确认:
- [ ] SKILL.md 的 frontmatter 格式正确
- [ ] source_hash 已正确记录
- [ ] description 包含触发条件
- [ ] wrapper.py 可执行（如已实现）

## 生成的元数据格式

每个由 skill-factory 创建的 Skill 必须包含以下扩展元数据:

```yaml
---
name: skill-name
description: 详细描述，包含触发条件

# 生命周期管理字段（必需）
source_url: https://github.com/owner/repo
source_hash: abc123def456...
version: 0.1.0
created_at: 2026-01-23
updated_at: 2026-01-23
evolution_enabled: true

# 可选字段
entry_point: scripts/wrapper.py
dependencies:
  - dependency1
  - dependency2
---
```

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `scripts/fetch_github_info.py` | 获取 GitHub 仓库元数据（轻量级，无需 clone） |
| `scripts/create_skill.py` | 创建标准化 Skill 目录结构 |
| `scripts/import_github_skill.py` | **完整导入** GitHub 仓库为本地 Skill（支持并行下载） |

### import_github_skill.py（推荐）

高效地从 GitHub 仓库下载所有文件并创建本地 Skill。

**特点：**
- 使用 GitHub API 获取目录结构（单次请求）
- 并行下载所有文件（10 线程）
- API 限流时自动切换到 git clone 备选方案
- 支持自定义 Skill 名称
- 支持移除源信息（`--no-source`）

**用法：**
```bash
# 基本用法
python scripts/import_github_skill.py <github_url> <output_dir>

# 自定义名称
python scripts/import_github_skill.py <github_url> <output_dir> --name my-skill

# 不保留源信息（作为全新本地 Skill）
python scripts/import_github_skill.py <github_url> <output_dir> --no-source

# 组合使用
python scripts/import_github_skill.py https://github.com/user/repo ./skills --name my-skill --no-source
```

**示例：**
```bash
# 导入并重命名
python scripts/import_github_skill.py https://github.com/PenglongHuang/chinese-novelist-skill ./skills --name chinese-novelist --no-source
```

## 最佳实践

1. **渐进式披露**: 不要将整个仓库内容塞入 Skill，只包含必要的封装代码
2. **依赖隔离**: 生成的 Skill 应明确声明依赖，建议使用 venv 或 uv 管理
3. **幂等性**: `source_hash` 字段允许 skill-manager 后续检查更新
4. **描述完整**: description 必须包含"做什么"和"何时使用"

## 示例

### 示例 1: 封装 yt-dlp

```
用户: /skill-factory https://github.com/yt-dlp/yt-dlp

Agent:
1. 运行 fetch_github_info.py 获取仓库信息
2. 分析 README，了解 yt-dlp 是视频下载工具
3. 运行 create_skill.py 创建目录
4. 完善 SKILL.md，添加常用命令示例
5. 实现 wrapper.py，封装下载功能
```

### 示例 2: 封装 ffmpeg-python

```
用户: 把 https://github.com/kkroening/ffmpeg-python 打包成 Skill

Agent:
1. 获取仓库信息
2. 分析 README，了解这是 FFmpeg 的 Python 绑定
3. 创建 Skill 目录
4. 完善文档，添加常用转换示例
5. 实现 wrapper.py，封装常用操作
```

## 与其他 Skill 的协作

- **skill-manager**: 使用 source_url 和 source_hash 检查更新
- **skill-evolution**: 使用 evolution_enabled 控制是否记录用户经验
- **skill-creator**: 遵循相同的目录结构和元数据规范
