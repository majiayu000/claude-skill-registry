---
name: nlp-interface
description: 自然语言接口，理解用户意图并映射到对应的命令
trigger:
  - auto: true  # 自动拦截所有非斜杠开头的输入
priority: highest
version: 1.0
---

# NLP Interface Skill - 自然语言接口

智能自然语言接口，理解用户的日常语言并自动映射到对应的斜杠命令，让知识管理更自然、更高效。

## 功能概述

NLP Interface 是一个自动触发的智能接口层，位于用户和命令系统之间：

```
用户输入 → NLP Interface → 意图识别 → 命令映射 → 执行命令
   ↓              ↓              ↓          ↓
 "记笔记"      识别为添加      /kb-add    执行添加
```

**核心能力**：
1. **意图识别**：理解用户想要做什么（6大类意图）
2. **上下文管理**：记住对话历史，理解代词指代
3. **智能路由**：将自然语言映射到具体的斜杠命令
4. **参数提取**：从自然语言中提取命令参数
5. **澄清策略**：当意图不明确时，主动询问

## 工作流程

### Step 1: 输入检测

```python
检测用户输入:
IF 输入以 "/" 开头:
    → 不处理，交给原有命令系统
ELSE:
    → 进入意图识别流程
```

### Step 2: 意图识别

```python
意图分类（6大类）:

1. 添加知识意图
   关键词: "记", "添加", "学习", "了解", "保存", "记录"
   映射命令: /kb-add

2. 搜索查找意图
   关键词: "找", "搜索", "查", "看看", "有没有", "关于"
   映射命令: /kb-search

3. 编辑修改意图
   关键词: "修改", "更新", "编辑", "改", "补充", "添加内容"
   映射命令: /kb-edit

4. 学习复习意图
   关键词: "测试", "测验", "练习", "复习", "回顾", "教我", "讲解"
   映射命令: /kb-quiz, /kb-review, /kb-teach

5. 导入内容意图
   关键词: "保存这个网页", "抓取", "导入", "从URL", "从PDF"
   映射命令: /kb-from-url, /kb-from-pdf, /kb-from-image

6. 网络搜索意图
   关键词: "搜索资料", "网上找", "Google一下", "查资料", "找资料"
   映射命令: /kb-search-web
```

### Step 3: 置信度计算

```python
置信度评估:

高置信度 (>90%):
    → 直接执行命令

中置信度 (70-90%):
    → 显示确认信息
    → "我要执行: [命令]，确认吗？(回车确认 / n取消)"

低置信度 (<70%):
    → 询问澄清
    → 显示选项列表
    → "你想做什么？1. 搜索 2. 添加 3. 测试"
```

### Step 4: 参数提取

```python
从自然语言提取命令参数:

标题提取:
    - 从引号内提取: "标题: React Hooks"
    - 从冒号后提取: "学习: useState"
    - 核心名词短语: "React Hooks学习笔记"

标签提取:
    - "标签: xxx" → ["xxx"]
    - "带tag xxx" → ["xxx"]
    - "#xxx" → ["xxx"]
    - 从内容中识别关键词

分类提取:
    - "学习笔记" → learning-note
    - "代码" → code-snippet
    - "项目" → project-doc
    - "研究" → research-note

其他参数:
    - 时间: "最近", "这个月" → --after=DATE
    - 难度: "简单", "困难" → --difficulty=LEVEL
    - 数量: "5个", "前10" → --count=N
```

### Step 5: 上下文解析

```python
上下文管理（最近10轮对话）:

代词解析:
    "它" → 最近提到的主体
    "这个" → 最近操作的对象
    "那个" → 前一轮提到的对象
    "第一条" → 上次搜索结果的第1个

话题追踪:
    - 持续时间: 30分钟内视为同一话题
    - 主题延续: "再搜索XXX"（在当前话题内细化）
    - 话题切换: "现在搜索Python"（清空上下文）

参考解析:
    "修改它" → /kb-edit [last_id]
    "关联这个" → /kb-link [last_id] [current_id]
```

### Step 6: 执行命令

```python
构建完整命令并执行:

1. 构建命令字符串:
    intent = "kb-add"
    params = {"title": "React Hooks", "tags": ["react"]}
    command = f"/{intent} \"{params['title']}\" --tags={','.join(params['tags'])}"

2. 传递给命令系统:
    执行构建的命令

3. 返回结果给用户:
    显示命令输出
    保存到对话历史
```

## 意图识别规则

### 1. 添加知识

**触发模式**：
```
"记一条笔记"
"添加知识"
"学习XXX"
"了解XXX"
"记录XXX"
"保存笔记"
```

**示例对话**：
```
用户: "记一条React Hooks学习笔记"
系统:
  意图: kb-add
  提取:
    - 标题: "React Hooks学习笔记"
    - 类型: learning-note
    - 标签: [react, hooks] (智能推荐)

  执行: /kb-add "React Hooks学习笔记" --type=learning-note --tags=react,hooks
```

### 2. 搜索查找

**触发模式**：
```
"找XXX"
"搜索XXX"
"查XXX"
"看看XXX"
"有没有XXX"
"关于XXX的笔记"
```

**示例对话**：
```
用户: "找useState相关内容"
系统:
  意图: kb-search
  提取:
    - 查询词: "useState"
    - 过滤: 无

  执行: /kb-search useState
```

### 3. 编辑修改

**触发模式**：
```
"修改XXX"
"更新XXX"
"编辑XXX"
"改XXX"
"给XXX补充"
"修改第一条"
"更新刚才那个"
```

**示例对话**：
```
用户: "修改刚才那条笔记"
系统:
  意图: kb-edit
  上下文:
    - 上次操作: 搜索结果
    - 最近ID: 2026-01-04-105815

  执行: /kb-edit 2026-01-04-105815
```

### 4. 学习复习

**触发模式**：
```
"测试XXX"
"测验XXX"
"练习XXX"
"复习今天"
"回顾最近"
"教我XXX"
"讲解XXX"
```

**示例对话**：
```
用户: "测试React部分"
系统:
  意图: kb-quiz
  提取:
    - 主题: "React"
    - 难度: medium (默认)

  执行: /kb-quiz "React" --difficulty=medium
```

### 5. 导入内容

**触发模式**：
```
"保存这个网页: URL"
"导入PDF"
"抓取URL"
"从URL导入"
"从PDF提取"
```

**示例对话**：
```
用户: "保存https://react.dev这篇文章"
系统:
  意图: kb-from-url
  提取:
    - URL: "https://react.dev"

  执行: /kb-from-url https://react.dev
```

### 6. 网络搜索

**触发模式**：
```
"搜索XXX资料"
"网上找XXX"
"Google一下XXX"
"查XXX的资料"
"找XXX的学习资源"
```

**示例对话**：
```
用户: "搜索React性能优化最新资料"
系统:
  意图: kb-search-web
  提取:
    - 查询: "React性能优化"
    - 约束: ["最新"]

  执行: /kb-search-web "React性能优化" --time=recent
```

## 上下文管理

### 对话历史结构

```json
{
  "sessionId": "2026-01-04-session-001",
  "startTime": "2026-01-04T14:30:00Z",
  "lastActivity": "2026-01-04T14:35:22Z",
  "turnCount": 5,
  "currentTopic": "React Hooks",

  "recentContext": {
    "lastCommand": "kb-search",
    "lastQuery": "useState",
    "lastIds": ["2026-01-04-105815", "2026-01-04-105644"],
    "lastResult": "3个结果"
  },

  "turns": [
    {
      "turnId": 1,
      "timestamp": "2026-01-04T14:30:05Z",
      "userInput": "找React笔记",
      "intent": "kb-search",
      "confidence": 0.92,
      "executedCommand": "/kb-search React"
    },
    ...
  ]
}
```

### 上下文解析策略

```python
代词解析规则:

"它" → 指向最近操作的主体
  例: "修改它" → 修改上次搜索/编辑的条目

"这个" → 指向当前讨论的对象
  例: "这个不错" → 当前查看的条目

"那个" → 指向前一轮的对象
  例: "那个呢？" → 前一轮提到的另一个对象

"第一条" → 指向列表中的第1个
  例: "修改第一条" → 上次搜索结果的第1条

"刚才那个" → 指向上一次操作的对象
  例: "再搜索刚才那个" → 继续细化搜索
```

## 澄清策略

### 模糊输入处理

```python
当意图不明确时:

示例1: 单词输入
用户: "React"
系统:
  "你想要对React做什么？
   1. 搜索相关笔记
   2. 添加新笔记
   3. 测试相关知识
   4. 学习React

   请回复数字或详细描述。"

示例2: 多种可能
用户: "Hooks"
系统:
  "我找到了几种可能:
   1. 搜索: React Hooks相关笔记
   2. 添加: 添加Hooks学习笔记
   3. 测试: Hooks知识测验

   请告诉我具体需求。"
```

## 偏好学习

### 自动学习用户习惯

```python
学习维度:

1. 标签偏好
   观察: 最近10次添加笔记，8次使用"frontend"
   学习: 默认建议标签包含"frontend"

2. 分类偏好
   观察: 70%的笔记在"learning"分类
   学习: 默认分类设为"learning"

3. 格式偏好
   观察: 用户经常使用详细格式查看搜索结果
   学习: 默认使用 --format=detailed

4. 时间偏好
   观察: 用户多在下午2-5点学习新知识
   学习: 下午主动建议学习资源
```

### 偏好应用

```python
应用偏好到命令:

用户: "记一条笔记"
系统应用:
  - 默认分类: learning (从偏好中获取)
  - 推荐标签: [react, hooks] (基于上下文)
  - 默认模板: learning-note

  输出: "我要添加一条学习笔记
          建议标签: react, hooks (基于最近话题)
          要修改吗？(回车确认 / 输入新标签)"
```

## 智能建议

### 操作后建议

```python
在命令执行完成后触发建议:

添加知识后:
  - 发现相关条目 (相似度>80%)
  - 建议创建关联
  - 建议开始学习计划

搜索后:
  - 建议细化搜索
  - 建议学习路径
  - 推荐相关主题

测验后:
  - 显示薄弱环节
  - 建议针对性复习
  - 推荐练习资源
```

## 配置选项

```json
{
  "nlp": {
    "enabled": true,
    "confirmThreshold": 0.7,
    "contextWindow": 10,
    "sessionTimeout": 1800,
    "maxHistory": 100
  },
  "preferences": {
    "autoLearn": true,
    "suggestAfterCommand": true,
    "showConfidence": false
  }
}
```

## 使用示例

### 完整对话流程

```
# 对话开始

用户: "找React笔记"
系统: [执行 /kb-search React]
      找到 3 个相关条目...

用户: "修改第一条"
系统: [从上下文解析 ID: 2026-01-04-105815]
      [执行 /kb-edit 2026-01-04-105815]

用户: "补充useEffect的内容"
系统: [识别为编辑操作，保持当前ID]
      请输入要补充的内容...

用户: "测试一下React"
系统: [执行 /kb-quiz "React" --difficulty=medium]

# 30分钟后，新会话开始

用户: "搜索useState"
系统: [新会话，清空上下文]
      [执行 /kb-search useState]
```

## 性能优化

```python
优化策略:

1. 意图识别缓存
   - 常见输入模式缓存
   - 避免重复计算

2. 对话历史压缩
   - 只保留关键信息
   - 定期清理过期会话

3. 异步处理
   - 偏好学习异步执行
   - 不阻塞主流程
```

## 错误处理

```python
错误处理策略:

1. 意图识别失败
   → 询问用户具体需求
   → 提供命令列表

2. 参数提取失败
   → 使用默认值
   → 询问用户确认

3. 命令执行失败
   → 显示原始错误
   → 建议正确的命令格式

4. 上下文丢失
   → 提示用户重新指定
   → 提供历史记录
```

## 调试模式

```python
调试模式输出:

当 showConfidence=true 时:

用户: "记笔记"
系统: [DEBUG]
      意图: kb-add
      置信度: 0.85
      提取参数: {title: null, tags: []}
      构建命令: /kb-add
      状态: 需要澄清

      请提供标题和内容...
```

## 与其他组件配合

```python
协作组件:

1. Knowledge Manager
   - 添加知识后触发
   - 接收标签和关联建议

2. Suggestion Engine
   - 接收操作上下文
   - 返回智能建议

3. Search Assistant
   - 网络搜索触发
   - 返回整理结果

4. User Preferences
   - 读取用户偏好
   - 更新使用统计
```

## 版本历史

- v1.0 (2026-01-04): 初始版本
  - 实现6大意图识别
  - 上下文管理
  - 参数提取
  - 澄清策略
