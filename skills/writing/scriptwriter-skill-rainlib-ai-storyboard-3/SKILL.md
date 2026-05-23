---
name: scriptwriter-skill
description: Use when creating episodic scripts, ensuring series continuity, adapting story concepts into visual narratives, or preparing scripts with sufficient beats for storyboarding
version: 1.0.0
allowed-tools: Read, Write, Bash(ls:*)
user-invocable: false
---

# Scriptwriter Skill

为 Scriptwriter 提供创作高质量、结构化剧本的专业知识，支持系列连续性和基于前作的续集创作。

## 概述

此技能支持创作：

- **结构完整的剧本** - 三幕结构，包含 9+ 个关键叙事时刻
- **系列连续剧集** - 保持角色、设定、风格一致性
- **视觉化场景** - 便于分镜转换的详细描述

## 核心原则

### 1. 视觉优先

剧本必须便于分镜转换。避免抽象心理描写，使用具体视觉化描述。

❌ **抽象**: Emma 感到困惑和恐惧。
✅ **视觉化**: Emma 的眼睛瞪大，手指颤抖着翻动页面。汗珠从额头滑落。

### 2. 角色一致性

- 建立规范外观描述（首次出场）
- 后续剧集保持关键识别符一致
- 性格发展合理渐进

### 3. 结构清晰

**三幕结构**:

- 第一幕 (~25%): Setup - 建立世界、触发事件
- 第二幕 (~50%): Confrontation - 上升动作、中点转折、低谷
- 第三幕 (~25%): Resolution - 高潮、决议、新平衡

### 4. Beats 充足

确保剧本包含**至少 9 个**清晰的视觉化转折点，分布在三幕中。

## 快速开始

### 创作新剧集的流程

**步骤 1: 查看系列历史**

```bash
# 查看已有剧集
ls script/

# 阅读前作了解角色和情节发展
```

**步骤 2: 基于用户输入设想故事**

用户可能提供：

- 主题关键词（如"背叛"、"发现真相"）
- 情节方向（如"角色 A 发现秘密"）
- 情感基调（如"悬疑"、"温馨"）

**步骤 3: 规划结构**

- 承接前作世界观和角色状态
- 设计 9+ 个关键叙事时刻
- 安排三幕结构

**步骤 4: 创作剧本**

使用标准场景格式，确保：

- 场景头: `## 场景 {X} - {INT./EXT.} {地点} - {时间}`
- 首次出场角色有完整外观描述
- 动作使用现在时、视觉化
- 足够的 beats 候选（≥9 个）

**步骤 5: 输出**

```
文件命名: script/ep{XX}-{title}.md
示例: script/ep03-betrayal.md
```

## 系列连续性检查清单

创作新剧集前：

- [ ] 已阅读所有之前的剧集
- [ ] 角色外观描述与前作一致
- [ ] 角色关系状态符合前作结尾
- [ ] 未解决情节线被考虑或推进
- [ ] 世界观设定无矛盾
- [ ] 视觉风格和氛围保持一致

## 输出约束

**严格禁止**:

- ❌ Frontmatter 元数据
- ❌ 模板说明
- ❌ 过于抽象的心理描写
- ❌ 缺少视觉细节的场景

**必须包含**:

- ✅ 场景编号、位置、时间
- ✅ 首次出场角色的外观描述
- ✅ 视觉化场景和动作
- ✅ 足够的关键时刻（≥9 个 beats 候选）
- ✅ 三幕结构完整

## 详细资源

### 方法论指南 📖

- [screenplay-methodology.md](screenplay-methodology.md) - 剧本创作方法论
  - 三幕结构和故事弧线
  - 角色发展原则
  - 场景构建技巧
  - 视觉化描述方法
  - 系列连续性管理

### 写作指导 📖

- [GUIDELINES.md](GUIDELINES.md) - 详细写作规范
  - 场景格式规范（场景头、时间标注）
  - 角色首次出场规则
  - 动作描述最佳实践
  - Beats 分布指导（9 beats 在三幕中的分配）
  - 对话写作技巧
  - 输出检查清单

### 模板

- [templates/episode-template.md](templates/episode-template.md) - Episode 剧本标准格式
- [templates/series-continuity-guide.md](templates/series-continuity-guide.md) - 系列连续性检查清单

## 何时使用

**自动触发场景**:

- 用户请求"创作新剧集"
- 用户提供故事概念需要转为剧本
- 需要为 Storyboard Artist 准备素材

**手动参考场景**:

- 不确定场景格式
- 处理系列连续性问题
- 规划 beats 分布
- 解决角色一致性问题

## 示例场景格式

```markdown
## 场景 5 - INT. 地铁车厢内 - 夜晚

车厢内昏暗，白色荧光灯忽明忽暗。空荡的座椅上散落着几张废弃报纸。

EMMA（25 岁，银色长发，穿深红色大衣）坐在靠窗位置，翻开古旧的皮质笔记本。
里面密密麻麻的手写符号和发光的六芒星图案映照在她脸上。

突然，所有灯光熄灭。
```

---

**用法**: Scriptwriter agent 自动引用此技能。方法论和指南（标记 📖）采用渐进式披露，仅在需要时查阅。
