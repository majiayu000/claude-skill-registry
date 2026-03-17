---
name: knowledge-manager
description: 智能知识管理助手,自动分析、组织和优化知识库
trigger:
  - on_add: true
  - on_edit: true
  - explicit: "帮我整理知识" "优化知识库" "分析标签"
priority: high
---

# Knowledge Manager Skill

智能知识管理助手,自动分析和优化知识库结构。

## 功能概述

Knowledge Manager 是一个自动触发的智能助手,帮助用户:

1. **自动标签建议**: 基于内容智能推荐标签
2. **自动关联建议**: 识别相关条目并建议链接
3. **分类检测**: 自动判断条目应该属于哪个分类
4. **智能组织**: 识别重复、孤立和需要整合的条目
5. **质量评估**: 评估条目的完整性和质量

## 触发条件

### 自动触发

1. **添加知识后** (`on_add: true`)
   - 用户执行 `/kb-add` 后自动触发
   - 分析新添加的条目
   - 建议标签、分类和关联

2. **编辑知识后** (`on_edit: true`)
   - 用户执行 `/kb-edit` 后自动触发
   - 检查编辑后的内容
   - 更新建议和关联

### 手动触发

用户可以通过以下方式手动触发:
- "帮我整理知识"
- "优化知识库"
- "分析标签使用情况"
- "查找重复条目"
- "建议知识关联"

## 执行流程

### 1. 内容分析

```markdown
## 分析新添加的条目

当用户添加知识时:

1. **提取关键词**
   - 从标题中提取核心概念
   - 从正文中识别技术术语
   - 提取专有名词和缩写

2. **主题识别**
   - 判断讨论的主要主题
   - 识别技术栈和工具
   - 检测应用场景

3. **质量评估**
   - 检查内容完整性
   - 评估是否有代码示例
   - 判断是否需要补充信息
```

### 2. 标签建议

```markdown
## 智能标签推荐

基于内容分析推荐标签:

1. **现有标签匹配**
   - 查找 tags.json 中相似的标签
   - 推荐使用现有标签体系

2. **新标签建议**
   - 识别内容中的关键概念
   - 建议新的标签名称
   - 避免标签冗余

3. **标签层级**
   - 建议主标签和副标签
   - 保持标签体系的一致性

输出格式:
```
建议标签:
  主标签: react, hooks
  相关标签: frontend, javascript, useState

说明:
  - react: React 框架相关内容
  - hooks: React Hooks 特性
  - frontend: 前端开发通用
  - javascript: JavaScript 语言

是否应用这些标签? (yes/no/edit)
```
```

### 3. 分类建议

```markdown
## 分类推荐

分析内容并建议分类:

**code 分类特征**:
- 代码片段
- API 文档
- 技术实现细节

**projects 分类特征**:
- 项目文档
- 开发日志
- 技术决策记录

**learning 分类特征**:
- 学习笔记
- 概念解释
- 教程和指南

**personal 分类特征**:
- 个人思考
- 经验总结
- 反思和感悟

输出格式:
```
建议分类: learning

置信度: 高 (85%)

理由:
  - 包含概念解释
  - 有学习笔记特征
  - 包含理解过程

是否应用此分类? (yes/no)
```
```

### 4. 关联建议

```markdown
## 智能关联推荐

识别可能相关的知识条目:

1. **标题相似度**
   - 计算与现有条目标题的相似度
   - 识别同义词和相关词

2. **标签重叠度**
   - Jaccard 相似系数
   - 标签重叠越多,关联性越强

3. **内容引用**
   - 检测是否提及了其他条目的 ID
   - 识别标题或内容中提到的其他概念

4. **时间邻近性**
   - 近期创建的相关条目
   - 同一时期学习的内容

输出格式:
```
发现 3 个可能相关的条目:

1. [2025-01-03-102015] React 基础概念
   相关度: 95% (高)
   关联类型: references
   理由: 标题和内容都有 "React" 关键词

2. [2025-01-02-084530] 函数组件
   相关度: 82% (中高)
   关联类型: builds-on
   理由: Hooks 是在函数组件基础上构建的

3. [2025-01-01-120000] JavaScript 闭包
   相关度: 45% (低)
   关联类型: related
   理由: 都涉及前端开发

是否创建这些关联? (all/select/none)
```
```

### 5. 知识组织分析

```markdown
## 组织结构分析

定期分析知识库的组织状况:

1. **重复检测**
   - 查找标题或内容相似的条目
   - 建议合并或建立关联

2. **孤立条目检测**
   - 没有链接的条目
   - 没有反向链接的条目
   - 建议创建关联

3. **标签分析**
   - 统计标签使用频率
   - 识别过度使用或很少使用的标签
   - 建议标签优化

4. **分类分布**
   - 分析各分类的条目数量
   - 识别不平衡的分类

输出格式:
```
知识库组织分析报告:

📊 总体统计
  总条目: 45 个
  总标签: 32 个
  总链接: 23 个

🔍 重复检测
  发现 2 对相似条目:
  - [2025-01-01-100000] React Hooks
    [2025-01-03-150000] React Hooks 详解
    相似度: 78%
    建议: 建立关联或合并

🏝️  孤立条目
  5 个条目没有链接:
  - [2025-01-02-120000] CSS Grid
  - [2025-01-04-090000] TypeScript 基础
  ...

🏷️  标签分析
  最常用标签:
  1. react (12 次)
  2. javascript (8 次)
  3. hooks (6 次)

  很少使用的标签:
  - debugging (1 次)
  - optimization (1 次)

📁 分类分布
  code: 15 个 (33%)
  learning: 18 个 (40%)
  projects: 8 个 (18%)
  personal: 4 个 (9%)

💡 优化建议
  1. 为孤立条目创建关联
  2. 合并相似的 React Hooks 条目
  3. 考虑合并 debugging 和 optimization 标签
```
```

## 智能建议示例

### 场景 1: 用户添加 React Hooks 笔记

```markdown
用户执行: /kb-add --type=learning-note
标题: React Hooks 学习笔记

[用户输入内容后]

Knowledge Manager 自动触发:

✨ 内容分析完成!

建议标签:
  主标签: react, hooks
  相关标签: frontend, functional-components
  理由: 内容主要讨论 React Hooks 和函数组件

建议分类: learning
置信度: 高 (92%)
理由: 学习笔记格式,包含概念解释

发现相关条目:
  1. [2025-01-03-102015] React 基础概念 (相关度: 88%)
     建议: references - 引用了 React 基础概念

  2. [2025-01-02-084530] 函数组件 (相关度: 75%)
     建议: builds-on - 在函数组件基础上讨论

是否应用这些建议?
输入选项:
  - apply all: 应用所有建议
  - select: 选择性应用
  - skip: 跳过,稍后手动处理

用户选择: apply all

✅ 已应用所有建议!
标签已更新: react, hooks, frontend, functional-components
分类已更新: learning
关联已创建:
  → references: 2025-01-03-102015
  → builds-on: 2025-01-02-084530
```

### 场景 2: 用户请求知识库分析

```markdown
用户输入: 帮我分析知识库的组织情况

Knowledge Manager 执行:

📊 知识库组织分析报告

=== 总体概况 ===
  总条目数: 45 个
  总标签数: 32 个
  总链接数: 23 个
  平均每个条目链接数: 0.51 个

=== 重复检测 ===
  发现 3 对可能重复的条目:

  1. React Hooks 相关 (相似度: 82%)
     [2025-01-01-100000] React Hooks 入门
     [2025-01-03-150000] React Hooks 详解
     建议: 建立关联 (builds-on)

  2. JavaScript 异步 (相似度: 75%)
     [2025-01-02-110000] Promise 和 async/await
     [2025-01-04-120000] JavaScript 异步编程
     建议: 合并为一个条目

  3. CSS Flexbox (相似度: 68%)
     [2025-01-05-090000] Flexbox 布局
     [2025-01-06-100000] Flexbox 完整指南
     建议: 保留较新的版本

=== 孤立条目 ===
  8 个条目没有任何链接:

  1. [2025-01-02-120000] CSS Grid 布局
     建议关联: [2025-01-05-090000] Flexbox 布局 (related)

  2. [2025-01-04-090000] TypeScript 基础
     建议关联: [2025-01-01-100000] React Hooks (related)

  ... (其余 6 个)

=== 标签分析 ===
  使用频率分布:
    高频 (>10次): react (12), javascript (8)
    中频 (5-10次): hooks (6), async (5)
    低频 (<5次): 其余 28 个标签

  标签优化建议:
    1. 合并相似标签:
       - js → javascript
       - ts → typescript

    2. 拆分宽泛标签:
       - frontend → react, vue, angular

=== 分类分布 ===
  code: 15 个 (33%) ⚖️  平衡
  learning: 18 个 (40%) ⚖️  平衡
  projects: 8 个 (18%) ⚖️  偏低
  personal: 4 个 (9%) ⚠️  过低

  建议: 增加项目和反思类内容的记录

=== 质量评估 ===
  高质量条目 (>500字): 12 个 (27%)
  中等质量 (200-500字): 23 个 (51%)
  低质量条目 (<200字): 10 个 (22%)

  建议: 丰富低质量条目的内容

💡 行动建议:
  1. 立即处理: 合并重复的 JavaScript 异步条目
  2. 本周完成: 为孤立条目创建关联
  3. 持续优化: 增加项目和反思类内容
  4. 标签整理: 统一 js 和 javascript 标签

是否需要我帮你执行这些建议?
```

## 技术实现

### 1. 相似度计算

```javascript
// Jaccard 相似系数 (标签重叠度)
function jaccardSimilarity(tags1, tags2) {
  const intersection = tags1.filter(tag => tags2.includes(tag));
  const union = [...new Set([...tags1, ...tags2])];
  return intersection.length / union.length;
}

// 文本相似度 (简单的词频统计)
function textSimilarity(text1, text2) {
  const words1 = tokenize(text1);
  const words2 = tokenize(text2);
  const common = words1.filter(word => words2.includes(word));
  return common.length / Math.max(words1.length, words2.length);
}
```

### 2. 标签推荐算法

```
1. 提取内容中的关键词
2. 与 tags.json 中的现有标签匹配
3. 计算每个相关标签的权重
4. 推荐权重最高的 3-5 个标签
```

### 3. 分类判断

```
1. 统计内容中的特征词
2. 每个分类有对应的特征词列表
3. 计算内容与每个分类的匹配度
4. 选择匹配度最高的分类
```

## 配置选项

### 自动应用阈值

```json
{
  "autoApply": {
    "tags": {
      "confidence": 0.9,
      "minMatches": 2
    },
    "category": {
      "confidence": 0.85
    },
    "links": {
      "minSimilarity": 0.8
    }
  }
}
```

### 分析频率

```json
{
  "analysis": {
    "onAdd": true,
    "onEdit": true,
    "scheduled": "weekly"
  }
}
```

## 注意事项

1. **用户控制**: 所有建议都需要用户确认,不自动修改
2. **性能优化**: 大量条目时使用缓存和增量分析
3. **隐私保护**: 分析过程仅在本地进行,不上传数据
4. **可配置性**: 允许用户自定义分析规则和阈值

## 未来扩展

1. **语义分析**: 使用 NLP 技术进行更深入的语义理解
2. **自动摘要**: 为长内容生成简洁的摘要
3. **知识图谱**: 可视化知识网络
4. **智能问答**: 基于知识库内容回答问题
5. **学习路径**: 自动推荐学习顺序和关联内容
