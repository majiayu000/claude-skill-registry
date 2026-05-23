---
name: skill-evolution
description: Skill 经验进化管理器。在对话结束时分析用户反馈，提取最佳实践和解决方案，持久化到 evolution.json 并缝合到 SKILL.md。支持三层架构（上游层、全局层、项目层）实现跨项目经验管理。当用户说"复盘"、"记录经验"、"保存这个技巧"、"evolve"时使用此工具。
---

# Skill Evolution Manager

Skill 系统的"进化中枢"。负责将对话中的经验教训持久化存储，并跨版本、跨项目保留。

## 核心价值

**问题**: Skill 更新时，用户积累的最佳实践会丢失；不同项目间的经验无法共享。

**解决方案**:
1. 将用户经验存储在独立的 `evolution.json` 文件中
2. 通过智能缝合将经验自动写入 SKILL.md
3. Skill 更新后，通过全量对齐恢复经验
4. **三层架构**：支持上游层、全局层、项目层的经验分离和合并

## 三层架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                          三层经验架构                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐                                               │
│  │   上游层 (Upstream)  │  skills-repo 原始仓库的经验                │
│  │   evolution.json     │  来自社区/原作者的最佳实践                 │
│  │   位置: skills-repo/skills/<skill>/evolution.json                │
│  └─────────┬────────┘                                               │
│            │ 继承                                                    │
│            ▼                                                         │
│  ┌──────────────────┐                                               │
│  │   全局层 (Global)    │  你个人的通用经验                          │
│  │   evolution.json     │  可选择性提交 PR 到上游                    │
│  │   位置: ~/.claude/evolutions/<skill>/evolution.json              │
│  └─────────┬────────┘                                               │
│            │ 继承                                                    │
│            ▼                                                         │
│  ┌──────────────────┐                                               │
│  │   项目层 (Project)   │  项目特定经验                              │
│  │   <skill>.json       │  不提交到版本控制                          │
│  │   位置: <project>/.claude/evolutions/<skill>.json                │
│  └──────────────────┘                                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 合并优先级

```
最终生效的经验 = merge(
    上游层,      # 最低优先级
    全局层,      # 中等优先级
    项目层       # 最高优先级
)
```

- **列表字段** (preferences, fixes, contexts): 追加去重
- **custom_prompts**: 项目层 > 全局层 > 上游层（覆盖）

## 核心功能

1. **复盘诊断**: 分析对话中的问题点和成功方案
2. **经验提取**: 将非结构化反馈转为结构化 JSON
3. **增量合并**: 去重合并新经验到 evolution.json
4. **智能缝合**: 将经验自动写入 SKILL.md 的专用章节
5. **跨版本对齐**: Skill 更新后重新缝合经验
6. **跨项目管理**: promote/pull 命令在层级间同步经验

## 使用场景

**触发方式**:
- `/skill-evolution` 或 `/evolve`
- "复盘一下刚才的对话"
- "记录一下这个经验"
- "把这个技巧保存到 Skill 里"
- "这个问题的解决方案要记住"

## 工作流程

### 步骤 1: 复盘诊断

Agent 分析当前对话，识别：
- **问题点**: 报错、参数错误、风格不对
- **成功方案**: 有效的解决方法、最佳实践
- **用户偏好**: 用户明确表达的喜好

### 步骤 2: 生成结构化 JSON

Agent 将提取的经验转换为 JSON 格式：

```json
{
  "preferences": [
    "用户希望下载时默认静音",
    "优先使用 mp4 格式"
  ],
  "fixes": [
    "Windows 下路径需要转义",
    "某些参数在 v2.0 后已弃用"
  ],
  "contexts": [
    "批量操作时需要添加 --batch 参数",
    "处理大文件时增加超时时间"
  ],
  "custom_prompts": "在执行前总是先打印预估耗时"
}
```

### 步骤 3: 选择保存层级

Agent 询问用户：
- **全局层**: 所有项目共享的通用经验
- **项目层**: 仅当前项目使用的特定经验

### 步骤 4: 增量合并

运行 `scripts/merge_evolution.py` 将经验合并：

```bash
# 传统模式（保存到 skill 目录）
python scripts/merge_evolution.py <skill_dir> '<json_string>'

# 分层模式（保存到全局层）
python scripts/merge_evolution.py <skill_name> '<json_string>' --layer global

# 分层模式（保存到项目层）
python scripts/merge_evolution.py <skill_name> '<json_string>' --layer project --project /path/to/project
```

### 步骤 5: 智能缝合

运行 `scripts/smart_stitch.py` 将经验写入 SKILL.md：

```bash
# 单层模式
python scripts/smart_stitch.py <skill_dir>

# 分层模式（合并三层经验）
python scripts/smart_stitch.py <skill_dir> --layered --project /path/to/project
```

### 步骤 6: 跨版本对齐

当 `skill-manager` 更新 Skill 后，运行全量对齐恢复经验：

```bash
python scripts/align_all.py <skills_dir>
```

## 脚本说明

| 脚本 | 功能 | 参数 |
|------|------|------|
| `layered_merge.py` | 分层经验管理核心 | `<action> <skill_name> [options]` |
| `merge_evolution.py` | 增量合并经验 | `<skill_dir> <json> [--layer] [--project]` |
| `smart_stitch.py` | 缝合到 SKILL.md | `<skill_dir> [--layered] [--project]` |
| `align_all.py` | 全量对齐 | `<skills_dir> [--dry-run] [--backup]` |

### layered_merge.py 命令

```bash
# 查看经验状态
python scripts/layered_merge.py status <skill_name> [--project <path>]

# 合并三层经验（查看结果）
python scripts/layered_merge.py merge <skill_name> [--project <path>]

# 将项目经验提升到全局层
python scripts/layered_merge.py promote <skill_name> [--project <path>] [--fields f1,f2]

# 从全局层拉取经验到项目层
python scripts/layered_merge.py pull <skill_name> [--project <path>]

# 保存经验到指定层
python scripts/layered_merge.py save <skill_name> <layer> '<json>' [--project <path>]
```

## evolution.json 格式

```json
{
  "preferences": ["string"],
  "fixes": ["string"],
  "contexts": ["string"],
  "custom_prompts": "string",
  "last_updated": "ISO-8601 datetime",
  "last_evolved_hash": "commit hash"
}
```

| 字段 | 说明 |
|------|------|
| `preferences` | 用户偏好列表 |
| `fixes` | 已知问题修复方案 |
| `contexts` | 特定使用场景说明 |
| `custom_prompts` | 自定义指令注入 |
| `last_updated` | 最后更新时间 |
| `last_evolved_hash` | 最后进化时的 source_hash |

## 最佳实践

1. **通过 evolution.json 修改**: 不要直接编辑 SKILL.md 中的经验章节
2. **定期复盘**: 每次使用 Skill 遇到问题或发现技巧时，及时记录
3. **更新后对齐**: 每次 skill-manager 更新 Skill 后，运行 align_all.py
4. **备份重要经验**: 使用 `--backup` 选项保护重要的经验数据
5. **合理选择层级**:
   - 通用经验 → 全局层
   - 项目特定经验 → 项目层
   - 高质量经验 → 考虑 PR 到上游

## 示例

### 示例 1: 记录用户偏好到全局层

```
用户: 记录一下，我希望下载视频时默认不带字幕，这个是通用设置

Agent:
1. 识别这是一个用户偏好，且是通用设置
2. 生成 JSON: {"preferences": ["下载视频时默认不带字幕"]}
3. 运行 merge_evolution.py --layer global 合并到全局层
4. 运行 smart_stitch.py --layered 更新 SKILL.md
```

### 示例 2: 记录项目特定修复

```
用户: 这个项目的路径比较特殊，记住要用绝对路径

Agent:
1. 识别这是项目特定的修复方案
2. 生成 JSON: {"fixes": ["此项目必须使用绝对路径"]}
3. 运行 merge_evolution.py --layer project 合并到项目层
```

### 示例 3: 提升经验到全局

```
用户: 把这个项目里学到的经验提升到全局，其他项目也能用

Agent:
1. 运行 layered_merge.py promote <skill_name>
2. 项目层的经验被复制到全局层
3. 报告提升结果
```

### 示例 4: 新项目初始化

```
用户: 这是新项目，把全局经验拉下来

Agent:
1. 运行 layered_merge.py pull <skill_name>
2. 全局层的经验被复制到项目层
3. 可以在此基础上继续积累项目特定经验
```

## 与其他 Skill 的协作

- **skill-factory**: 创建的 Skills 自动启用 evolution（`evolution_enabled: true`）
- **skill-manager**: 更新 Skill 后应调用 align_all.py 恢复经验；提供 promote/pull 命令
- **skill-creator**: 遵循相同的经验章节格式
