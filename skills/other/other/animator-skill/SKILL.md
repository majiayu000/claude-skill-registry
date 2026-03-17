---
name: animator-skill
description: Use when converting static image sequences (sequence boards) into motion prompts for AI video generation platforms (Runway, Pika, SVD), or describing temporal movement for video synthesis
version: 1.0.0
allowed-tools: Read, Write
user-invocable: false
---

# Animator Skill

为 Animator 提供创建动态 motion prompts 的专业知识，优化用于 AI 视频生成工作流。

## 概述

此技能将静态 4 格序列转换为时间运动描述，支持：

- **主体运动** - 角色动作、表情、姿态
- **镜头运动** - Pan, Dolly, Crane, Orbit
- **自然运动** - 风、水、光影
- **平台优化** - Runway Gen-3, Pika Labs, SVD, AnimateDiff

## 核心原则

### 1. 简洁胜于复杂

**一个主要动作，而非多个同时动作**

❌ **过于复杂**:

```
角色跑forward, 跳过obstacle, 空中旋转, 拔剑, 落地战斗姿态
```

✅ **专注简洁**:

```
角色跑forward并跳过obstacle, 落地蹲姿。快速节奏。3秒。
```

### 2. 物理合理性

时长必须与动作匹配：

- **3 秒**: 转头、拿物体、走 2-3 步
- **5 秒**: 穿过房间、坐下/站起、开门走入
- **❌ 不现实**: "跑 100 米"在 3 秒、"完整战斗"在 5 秒

### 3. 运动优先，细节其次

简化静态描述，强调运动：

❌ **过度详细** (120+ 词):

```
A 25-year-old woman with waist-length silver hair, pale skin, violet eyes,
wearing black coat over white shirt and black pants, silver ring on right hand,
walks from left to right...
```

✅ **运动优先** (25 词):

```
A woman with silver hair in a black coat walks from left to right across platform.
Steady pace. 4 seconds.
```

### 4. 明确运动源

清楚指明什么在动：

- **主体运动**: "Character walks left to right. Camera static."
- **镜头运动**: "Flower static. Camera pans right slowly."
- **组合**: "Runner moves toward camera while camera dollies backward at matching speed."

## Motion Prompt 结构模板

```
[简化主体描述] [主要动作] [方向].
[镜头运动(如有)]. [速度描述]. [时长].
```

**示例**:

```
A woman with silver hair in a crimson coat walks from left to right along
a train platform, wind blowing her hair. Camera pans right to follow her.
Steady walking pace. 5 seconds.
```

## 快速开始

### 步骤 1: 分析 Sequence Board

确定 4 格序列中的关键运动：

- Frame 1 → Frame 2: 发生了什么变化？
- 主体移动了吗？镜头移动了吗？
- 环境有自然运动吗（风、水、光）？

### 步骤 2: 选择一个主要动作

不要试图描述所有变化，选择**最重要的一个**。

### 步骤 3: 指定方向

使用明确的方向性词汇：

- left to right / right to left
- toward camera / away from camera
- background to foreground
- clockwise / counterclockwise

### 步骤 4: 选择速度

参考 [MOTION_LIBRARY.md](MOTION_LIBRARY.md) 速度指导：

- **慢速** (4-5 秒): slowly, gradually, gently
- **中速** (3-4 秒): walks, moves, steady pace
- **快速** (2-3 秒): quickly, swiftly, rushes

### 步骤 5: 确定时长

根据平台和运动复杂度：

- Runway Gen-3: 3-5 秒
- Pika Labs: 3-4 秒
- SVD: 2-4 秒
- AnimateDiff: 1-3 秒

## 输出约束

**严格禁止**:

- ❌ Frontmatter 元数据
- ❌ 模板说明
- ❌ 超过 80 词的冗长描述
- ❌ 多个竞争性动作
- ❌ 物理上不可能的运动

**必须包含**:

- ✅ 40-80 词的简洁描述
- ✅ 一个清晰的主要动作
- ✅ 运动方向
- ✅ 速度/节奏
- ✅ 时长
- ✅ 主体 vs 镜头运动的区分

## 详细资源

### 方法论指南 📖

- [motion-prompt-methodology.md](motion-prompt-methodology.md) - Motion prompt 原则
  - 简洁性和专注性
  - 方向性和速度指定
  - 主体与镜头运动区分
  - 视频时长的物理合理性
  - 视频模型优化技术

### 运动类型库 📖

- [MOTION_LIBRARY.md](MOTION_LIBRARY.md) - 完整运动参考
  - 主体运动库（人物移动、动作、表情）
  - 镜头运动库（Pan、Dolly、Crane、Orbit）
  - 自然运动（风、水、光影）
  - 运动速度指导（慢/中/快）
  - 平台特性和优化（Runway, Pika, SVD, AnimateDiff）
  - 物理合理性检查
  - 常见运动组合示例

### 模板

- [templates/motion-prompt-template.md](templates/motion-prompt-template.md) - 输出格式

## 何时使用

**自动触发场景**:

- 用户请求"生成 motion prompts"
- 批准的 sequence board 需要转换为视频
- Director 反馈运动清晰度问题

**手动参考场景**:

- 选择合适的运动类型
- 确定运动速度
- 优化平台特定格式
- 检查物理合理性

## 平台快速选择

- **复杂运动** → Runway Gen-3
- **快速生成** → Pika Labs
- **本地部署** → Stable Video Diffusion
- **风格化动画** → AnimateDiff

## 常见错误与解决

### ❌ 错误: 过于冗长

```
(120+ words with excessive scene description)
```

✅ **解决**: 简化场景，强调运动 (~25 words)

### ❌ 错误: 多个动作

```
角色跑、跳、旋转、拔剑、落地
```

✅ **解决**: 选择一个主要动作

### ❌ 错误: 方向模糊

```
角色在房间里移动
```

✅ **解决**: 明确方向 "from background to foreground"

---

**用法**: Animator agent 自动引用此技能。方法论和库（标记 📖）采用渐进式披露，仅在需要时查阅。
