---
name: suggestion-engine
description: 智能建议引擎，根据上下文和用户行为主动推荐相关操作
trigger:
  - after-command: true  # 在命令执行后触发
priority: high
version: 1.0
---

# Suggestion Engine Skill - 智能建议引擎

智能建议引擎，在用户执行操作后主动提供个性化推荐，提升知识管理效率。

## 核心功能

### 1. 上下文感知建议
基于当前操作的内容和上下文，智能推荐下一步操作

### 2. 关联发现
自动发现相关知识条目，建议创建关联

### 3. 学习路径推荐
根据知识图谱和学习进度，推荐学习路径

### 4. 最佳实践建议
根据用户偏好和行为模式，提供优化建议

## 触发时机

### 在以下操作后触发建议：

```python
触发条件：

1. 添加知识后 (kb-add, kb-from-url, kb-from-pdf, kb-from-image)
   → 发现相关条目
   → 建议创建关联
   → 推荐学习计划

2. 搜索后 (kb-search, kb-search-web)
   → 建议细化搜索
   → 推荐相关主题
   → 建议学习路径

3. 编辑知识后 (kb-edit)
   → 检测内容变化
   → 建议更新关联
   → 推荐复习

4. 测验后 (kb-quiz)
   → 显示薄弱环节
   → 推荐针对性复习
   → 建议练习资源

5. 复习后 (kb-review)
   → 显示复习统计
   → 预测下次复习
   → 推荐扩展学习

6. 学习计划更新后 (kb-learn, kb-progress)
   → 显示学习进度
   → 调整学习建议
   → 推荐配套资源
```

## 建议类型

### 类型1: 关联建议

**触发时机**: 添加知识、编辑知识后

**检测逻辑**:
```python
def find_associations(new_item):
    candidates = []

    # 1. 标签重叠度检测
    for item in knowledge_base:
        overlap = calculate_tag_overlap(new_item.tags, item.tags)
        if overlap > 0.5:  # 50%以上重叠
            candidates.append({
                'item': item,
                'reason': f"标签重叠度: {overlap*100}%",
                'confidence': overlap
            })

    # 2. 主题提及检测
    for item in knowledge_base:
        if new_item.title.lower() in item.content.lower():
            candidates.append({
                'item': item,
                'reason': f"内容中提到了 '{new_item.title}'",
                'confidence': 0.8
            })

    # 3. 时间邻近性检测
    recent_items = get_items_from_last_week()
    for item in recent_items:
        if has_similar_context(new_item, item):
            candidates.append({
                'item': item,
                'reason': "最近添加的相似内容",
                'confidence': 0.6
            })

    # 按置信度排序
    return sorted(candidates, key=lambda x: x['confidence'], reverse=True)[:5]
```

**建议输出**:
```
💡 发现相关条目

  [2026-01-04-105644] React基础概念 (92%相关)
    标签重叠: react, hooks
    原因: 标签重叠度 85%

  [2026-01-04-105900] 函数组件实践 (85%相关)
    标签重叠: react
    原因: 内容提及了相似概念

建议操作:
  1. 创建关联 - /kb-link new-id 2026-01-04-105644
  2. 批量关联 - /kb-link new-id all
  3. 暂不关联 - skip

执行哪些？(输入序号或all)
```

### 类型2: 学习路径建议

**触发时机**: 搜索后、添加系列知识后

**推荐逻辑**:
```python
def suggest_learning_path(topic):
    # 获取主题相关的所有条目
    related_items = search_by_topic(topic)

    # 按难度和依赖关系排序
    sorted_items = topological_sort(related_items)

    # 分组为学习阶段
    path = {
        'beginner': sorted_items[:3],
        'intermediate': sorted_items[3:7],
        'advanced': sorted_items[7:]
    }

    return path
```

**建议输出**:
```
🎓 推荐学习路径: React Hooks

基于您的内容和搜索记录，为您规划了学习路径：

第1阶段: 基础入门 (2-3天)
  1. React Hooks概述 [2026-01-04-105644]
  2. useState基础 [2026-01-03-102415]
  3. useEffect入门 [2026-01-03-105822]

第2阶段: 进阶实践 (1周)
  4. Hook规则和限制 [2026-01-02-091533]
  5. 自定义Hooks [2026-01-02-104511]
  6. 性能优化 [2026-01-01-101234]

第3阶段: 深入理解 (2周)
  7. Hooks源码分析 [2026-01-01-095822]
  8. 高级模式 [2026-01-01-093211]

建议操作:
  1. 创建学习计划 - /kb-learn "React Hooks" --items=1-8
  2. 开始学习第一阶段 - /kb-learn "React Hooks" --stage=1
  3. 测试当前水平 - /kb-quiz "React Hooks"

选择: _
```

### 类型3: 薄弱环节建议

**触发时机**: 测验后、复习评分低后

**分析逻辑**:
```python
def analyze_weaknesses(quiz_results):
    weaknesses = {}

    for question in quiz_results:
        if not question.correct:
            topic = question.topic

            if topic not in weaknesses:
                weaknesses[topic] = {
                    'count': 0,
                    'items': []
                }

            weaknesses[topic]['count'] += 1
            weaknesses[topic]['items'].append(question.related_item)

    # 按错误频率排序
    return sorted(weaknesses.items(),
                  key=lambda x: x[1]['count'],
                  reverse=True)
```

**建议输出**:
```
📊 测验分析: React Hooks

总分: 75/100

薄弱环节识别:
  ❌ useEffect依赖项 (3个错误)
     相关条目: [2026-01-03-105822], [2026-01-02-091533]

  ⚠️ 自定义Hooks (1个错误)
     相关条目: [2026-01-02-104511]

建议改进计划:
  1. 重点复习useEffect - /kb-review 2026-01-03-105822
  2. 重做useEffect练习 - /kb-quiz "useEffect" --difficulty=hard
  3. 费曼技巧讲解 - /kb-teach "useEffect依赖项" --role=teacher
  4. 创建专项复习计划 - /kb-learn "useEffect深入理解" --focus=true

执行哪些？(输入序号或all)
```

### 类型4: 搜索细化建议

**触发时机**: 搜索结果过多/过少后

**判断逻辑**:
```python
def suggest_search_refinement(search_results, query):
    result_count = len(search_results)

    if result_count == 0:
        return {
            'type': 'no_results',
            'suggestions': [
                f"尝试相关词: '{query}'的同义词",
                f"检查拼写: '{query}'是否正确",
                f"扩大范围: 移除一些过滤条件"
            ]
        }

    elif result_count < 5:
        return {
            'type': 'few_results',
            'suggestions': [
                f"相关主题: 搜索 '{query}'相关概念",
                f"扩展标签: 使用更宽泛的标签",
                f"网络搜索: /kb-search-web '{query}'"
            ]
        }

    elif result_count > 20:
        return {
            'type': 'many_results',
            'suggestions': [
                f"添加过滤: --tag=xxx, --category=xxx",
                f"时间范围: --after=2026-01-01",
                f"精确匹配: 使用双引号 '{query}'"
            ]
        }

    else:
        return None  # 结果数量合适，不需要建议
```

**建议输出**:
```
💡 搜索优化建议

找到 35 个结果，结果较多。建议：

1. 添加标签过滤
   /kb-search React --tag=hooks
   预计减少到 15 个结果

2. 按时间筛选
   /kb-search React --after=2026-01-01
   只显示最近内容

3. 搜索更具体
   /kb-search "React Hooks useState"
   使用精确短语

4. 网络搜索补充
   /kb-search-web "React Hooks 最新实践"
   查找在线资源

执行哪个？(输入序号或done)
```

### 类型5: 复习提醒建议

**触发时机**: 每日、学习计划更新时

**算法**: SuperMemo 2 (SM-2)

```python
def calculate_next_review(item):
    if not item.reviews:
        return today + 1 day

    last_review = item.reviews[-1]
    ease_factor = item.easeFactor  # 默认 2.5
    interval = item.interval  # 默认 1 天

    # SM-2 算法
    if last_review.quality < 3:
        # 记忆不好，重置间隔
        next_interval = 1
    else:
        # 记忆好，增加间隔
        next_interval = interval * ease_factor

    # 调整难度系数
    ease_factor = max(1.3,
                      ease_factor + (0.1 - (5 - last_review.quality) * (0.08 + (5 - last_review.quality) * 0.02)))

    return today + next_interval days, ease_factor, next_interval
```

**建议输出**:
```
📅 今日复习提醒 (5条待复习)

  1. [2026-01-03-105822] useEffect依赖项
     上次评分: 4/5 | 复习间隔: 3天 | 遗忘概率: 35%

  2. [2026-01-02-104511] 自定义Hooks
     上次评分: 5/5 | 复习间隔: 7天 | 遗忘概率: 20%

  3. [2026-01-01-101234] React性能优化
     上次评分: 3/5 | 复习间隔: 2天 | 遗忘概率: 50% ⚠️

建议操作:
  1. 开始今日复习 - /kb-review --today
  2. 优先复习遗忘概率高的 - /kb-review --priority=high
  3. 查看复习统计 - /kb-review --stats

预计耗时: 15分钟
```

### 类型6: 内容质量建议

**触发时机**: 添加知识后、批量导入后

**检测逻辑**:
```python
def analyze_content_quality(item):
    issues = []
    score = 100

    # 1. 完整性检测
    if len(item.content) < 200:
        issues.append({
            'type': 'too_short',
            'severity': 'warning',
            'message': '内容较短，建议补充更多细节'
        })
        score -= 10

    # 2. 代码示例检测
    if 'code' in item.tags and not has_code_examples(item.content):
        issues.append({
            'type': 'missing_examples',
            'severity': 'info',
            'message': '代码片段建议添加实际示例'
        })
        score -= 5

    # 3. 标签完整性
    if len(item.tags) < 2:
        issues.append({
            'type': 'few_tags',
            'severity': 'info',
            'message': f'建议添加更多标签，当前: {item.tags}'
        })
        score -= 5

    # 4. 关联检测
    related = find_related_items(item)
    if len(related) > 0 and not item.links:
        issues.append({
            'type': 'missing_links',
            'severity': 'suggestion',
            'message': f'发现{len(related)}个相关条目，建议创建关联',
            'related': related[:3]
        })
        score -= 10

    return {
        'score': max(0, score),
        'issues': issues
    }
```

**建议输出**:
```
📝 内容质量分析

质量得分: 75/100

改进建议:
  ⚠️ 内容较短
     当前: 180字 | 建议: >500字
     操作: /kb-edit [id] 补充细节

  ℹ️ 缺少代码示例
     检测到标签: code-snippet
     建议: 添加实际使用示例

  💡 发现2个相关条目
     • [2026-01-03-105822] useEffect依赖项
     • [2026-01-02-104511] 自定义Hooks
     操作: /kb-link [id] 2026-01-03-105822

立即改进？(y/n)
```

## 建议呈现策略

### 1. 时机控制

```python
建议频率控制:

用户偏好级别:
  - conservative: 每操作3-5次后建议1次
  - moderate (默认): 每操作1-2次后建议1次
  - aggressive: 每次操作后都建议

时间控制:
  - 不要在短时间内重复建议 (>5分钟)
  - 不要建议用户明确拒绝过的内容
```

### 2. 个性化排序

```python
def rank_suggestions(suggestions, user_preferences):
    scores = []

    for suggestion in suggestions:
        score = 0

        # 1. 相关性加分
        score += suggestion.relevance * 0.4

        # 2. 用户兴趣加分
        if suggestion.topic in user_preferences.interests:
            score += 0.3

        # 3. 学习阶段匹配
        if suggestion.difficulty == user_preferences.expertiseLevel:
            score += 0.2

        # 4. 时间合适性
        if is_preferred_time(user_preferences.activeHours):
            score += 0.1

        scores.append((suggestion, score))

    # 按分数排序
    return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
```

### 3. 呈现格式

```markdown
💡 智能建议 (最多3条)

  [优先级高] 建议标题
  说明: 简短解释原因
  操作: /command-args

  [优先级中] 建议标题
  说明: 简短解释原因
  操作: /command-args

  [优先级低] 建议标题
  说明: 简短解释原因
  操作: /command-args

---
快捷操作:
  1 - 执行第1条
  2 - 执行第2条
  3 - 执行第3条
  all - 全部执行
  done - 跳过
  never - 不再显示此类建议

选择: _
```

## 用户反馈机制

### 记录用户选择

```python
用户响应类型:

1. accept - 接受建议
   → 记录为成功建议
   → 增加该类型建议的权重

2. reject - 拒绝建议
   → 记录为失败建议
   → 降低该类型建议的权重

3. skip - 跳过
   → 不影响权重
   → 可能在下次重新建议

4. never - 永不显示
   → 加入黑名单
   → 永久不再建议该类型

5. modify - 修改后执行
   → 记录用户偏好
   → 调整未来建议
```

### 学习用户偏好

```python
def update_suggestion_preferences(user_action, suggestion):
    preferences = load_user_preferences()

    # 更新建议接受率
    if user_action == 'accept':
        preferences.suggestionAcceptRate += 0.1
    elif user_action == 'reject':
        preferences.suggestionAcceptRate -= 0.05

    # 更新类型偏好
    suggestion_type = suggestion.type
    if user_action == 'accept':
        preferences.suggestionTypeWeights[suggestion_type] += 0.2
    elif user_action == 'reject':
        preferences.suggestionTypeWeights[suggestion_type] -= 0.1

    # 更新黑名单
    if user_action == 'never':
        preferences.suggestionBlacklist.append({
            'type': suggestion_type,
            'content': suggestion.content_hash
        })

    # 归一化权重
    normalize_weights(preferences.suggestionTypeWeights)

    save_preferences(preferences)
```

## 配置选项

### 用户可配置项

```json
{
  "suggestions": {
    "enabled": true,
    "aggressiveness": "moderate",  // conservative | moderate | aggressive
    "maxSuggestions": 3,
    "showConfidence": false,

    "typeWeights": {
      "association": 0.8,
      "learning_path": 0.9,
      "weakness": 0.7,
      "search_refinement": 0.6,
      "review_reminder": 0.8,
      "quality_improvement": 0.5
    },

    "blacklist": [],
    "acceptRate": 0.65,
    "lastShown": "2026-01-04T14:30:00Z"
  }
}
```

## 与其他组件集成

### 1. Knowledge Manager Skill

```python
协作模式：

Knowledge Manager 负责内容分析
→ Suggestion Engine 基于分析结果生成建议

例如：
  - Knowledge Manager 检测到标签冲突
  → Suggestion Engine 建议标准化标签
```

### 2. NLP Interface Skill

```python
协作模式：

NLP Interface 解析用户意图
→ Suggestion Engine 提供操作建议

例如：
  - 用户: "我想学习React"
  - NLP: 识别为学习意图
  - Suggestion: "建议创建学习计划: /kb-learn 'React'"
```

### 3. User Preferences

```python
协作模式：

User Preferences 提供行为数据
→ Suggestion Engine 个性化推荐

例如：
  - 偏好显示用户下午2-5点活跃
  → Suggestion 在下午推荐学习资源
  → 早上推荐复习任务
```

## 性能优化

### 1. 异步处理

```python
# 建议生成不阻塞主流程
async def generate_suggestions_after_command(command_result):
    # 在后台生成建议
    suggestions = await async_analyze_and_suggest(command_result)

    # 只在合适时机显示
    if should_show_suggestions():
        display_suggestions(suggestions)
```

### 2. 缓存机制

```python
# 缓存常见建议
cache = {
    'react_learning_path': {
        'suggestions': [...],
        'generated_at': '2026-01-04',
        'ttl': 86400  # 24小时
    }
}

def get_suggestions(topic):
    if topic in cache and not cache_expired(topic):
        return cache[topic]['suggestions']

    return generate_fresh_suggestions(topic)
```

### 3. 智能去重

```python
# 避免重复建议
def deduplicate_suggestions(suggestions, history):
    seen = set()
    unique = []

    for suggestion in suggestions:
        signature = (suggestion.type, suggestion.content_hash)

        if signature not in seen and signature not in history.recently_shown:
            seen.add(signature)
            unique.append(suggestion)

    return unique
```

## 最佳实践

### 1. 不要过度打扰

```
❌ 不好:
  - 每次操作都弹出建议
  - 一次显示10条建议
  - 无法关闭建议

✅ 好:
  - 控制频率 (moderate模式)
  - 最多显示3条
  - 提供"never"选项
```

### 2. 建议要有价值

```
❌ 无价值建议:
  "您可以查看帮助文档"

✅ 有价值建议:
  "发现3个useState相关条目，建议创建关联以提高学习效率"
```

### 3. 个性化是关键

```
根据用户调整:
  - 新用户: 更多引导性建议
  - 高级用户: 更少但更精准的建议
  - 特定兴趣: 优先推荐相关领域
  - 活跃时间: 学习vs复习建议
```

## 使用示例

### 示例1: 添加知识后的建议

```
用户: /kb-add "React Hooks学习笔记" --tags=react,hooks
系统: ✅ 已添加: [2026-01-04-143052]

💡 智能建议

  1. [85%] 创建关联
     发现2个相关条目:
     • [2026-01-03-105822] useEffect依赖项
     • [2026-01-02-104511] 自定义Hooks
     操作: /kb-link 2026-01-04-143052 2026-01-03-105822

  2. [75%] 开始学习
     建议创建学习计划掌握React Hooks
     操作: /kb-learn "React Hooks深入理解"

  3. [60%] 测试理解
     检验对Hooks的掌握程度
     操作: /kb-quiz "React Hooks"

选择: _ (或done跳过)
```

### 示例2: 测验后的建议

```
用户: /kb-quiz "React Hooks"
系统: 📊 测验完成: 75/100

💡 改进建议

  薄弱环节: useEffect依赖项 (3个错误)

  1. 重点复习
     /kb-review 2026-01-03-105822 --focus

  2. 费曼技巧讲解
     /kb-teach "useEffect依赖项" --role=teacher

  3. 额外练习
     /kb-quiz "useEffect" --difficulty=hard

选择: _
```

### 示例3: 每日复习提醒

```
用户: (早晨打开系统)
系统: 📅 早上好！今日学习提醒

  📚 复习任务: 5条待复习 (预计15分钟)
  🆕 新知识: 昨日添加3条React相关内容
  🎯 学习进度: "React Hooks"计划进行中(35%)

建议操作:
  1. 开始复习 - /kb-review --today
  2. 继续学习 - /kb-learn "React Hooks" --continue
  3. 查看详情 - /kb-progress

开始今日学习？(y/n)
```

## 版本历史

- v1.0 (2026-01-04): 初始版本
  - 实现6大建议类型
  - 用户反馈学习
  - 个性化排序
