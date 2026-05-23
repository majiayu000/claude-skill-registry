---
name: context-optimizer
description: 上下文优化专家。专注于长对话中的上下文管理、token 效率和性能优化。解决 lost-in-middle、context poisoning 等问题，提升 AI 代理在复杂任务中的表现。
metadata:
  short-description: 上下文管理与优化
  keywords:
    - context-optimizer
    - 上下文优化
    - token 效率
    - 长对话
    - 压缩策略
    - 缓存机制
    - 性能优化
    - 上下文窗口
  category: 性能优化
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Context Optimizer - 上下文优化专家

## 核心理念

**上下文优化** 是长对话性能的关键：

```
┌─────────────────────────────────────────────────────────┐
│  识别问题 → 压缩历史 → 掩码加载 → 缓存重用 → 性能提升  │
└─────────────────────────────────────────────────────────┘
```

**核心问题**：
- ❌ **Lost-in-Middle**：关键信息被中间内容淹没
- ❌ **Context Poisoning**：冲突信息干扰判断
- ❌ **Distraction**：无关信息浪费 token
- ❌ **Context Clash**：多信息源冲突

---

## 何时使用本技能

在以下场景时激活：

- 长对话导致性能下降
- Context window 接近限制
- AI 遗忘之前的信息
- 提到"上下文"、"token 限制"、"效率"

---

## 上下文问题识别

### 问题 1：Lost-in-Middle

**表现**：
- AI 遗忘对话中间的关键信息
- 首尾信息记住，中间信息遗忘
- 需要重复提供相同信息

**检测**：
```python
def detect_lost_in_middle(conversation: list) -> bool:
    """检测是否出现 lost-in-middle 问题"""
    # 1. 检查对话长度
    if len(conversation) < 10:
        return False

    # 2. 检查是否有重复提问
    questions = [msg for msg in conversation if '?' in msg]
    unique_questions = set(questions)
    if len(questions) > len(unique_questions) * 1.5:
        return True  # 存在重复提问

    # 3. 检查中间内容是否被引用
    middle_start = len(conversation) // 3
    middle_end = len(conversation) * 2 // 3
    middle_content = conversation[middle_start:middle_end]

    # 检查后续对话是否引用中间内容
    later_refs = sum(
        1 for msg in conversation[middle_end:]
        if any(keyword in msg for keyword in extract_keywords(middle_content))
    )

    if later_refs < len(middle_content) * 0.1:
        return True  # 中间内容被遗忘

    return False
```

### 问题 2：Context Poisoning

**表现**：
- AI 产生矛盾的回答
- 错误信息影响判断
- 不同来源信息冲突

**检测**：
```python
def detect_context_poisoning(conversation: list) -> list:
    """检测上下文污染"""
    conflicts = []

    # 1. 提取所有事实陈述
    facts = extract_facts(conversation)

    # 2. 检测矛盾
    for fact1, fact2 in combinations(facts, 2):
        if are_contradictory(fact1, fact2):
            conflicts.append({
                'type': 'contradiction',
                'fact1': fact1,
                'fact2': fact2,
                'severity': 'high'
            })

    # 3. 检测信息源冲突
    sources = group_by_source(facts)
    for source, source_facts in sources.items():
        if has_internal_conflicts(source_facts):
            conflicts.append({
                'type': 'source_conflict',
                'source': source,
                'severity': 'medium'
            })

    return conflicts
```

---

## 优化策略

### 策略 1：压缩策略

#### 历史压缩

```python
class ContextCompressor:
    """上下文压缩器"""

    def compress_history(
        self,
        conversation: list,
        max_tokens: int,
        retention_priority: list[str] = None
    ) -> list:
        """
        压缩对话历史

        Args:
            conversation: 对话历史
            max_tokens: 最大 token 数
            retention_priority: 保留优先级 ["current_task", "decisions", "errors"]

        Returns:
            压缩后的对话
        """
        priority = retention_priority or ["current_task", "decisions", "errors"]

        # 1. 分类消息
        categorized = self._categorize_messages(conversation)

        # 2. 按优先级保留
        retained = []
        current_tokens = 0

        for category in priority:
            messages = categorized.get(category, [])

            for msg in messages:
                tokens = self._count_tokens(msg)
                if current_tokens + tokens > max_tokens:
                    # 尝试压缩
                    compressed = self._compress_message(msg)
                    if current_tokens + self._count_tokens(compressed) <= max_tokens:
                        retained.append(compressed)
                        current_tokens += self._count_tokens(compressed)
                else:
                    retained.append(msg)
                    current_tokens += tokens

        return retained

    def _categorize_messages(self, conversation: list) -> dict:
        """分类消息"""
        categories = {
            'current_task': [],
            'decisions': [],
            'errors': [],
            'context': []
        }

        for msg in conversation:
            if self._is_task_related(msg):
                categories['current_task'].append(msg)
            elif self._is_decision(msg):
                categories['decisions'].append(msg)
            elif self._is_error(msg):
                categories['errors'].append(msg)
            else:
                categories['context'].append(msg)

        return categories

    def _compress_message(self, message: str) -> str:
        """压缩单条消息"""
        # 提取关键信息
        key_points = extract_key_points(message)

        # 生成摘要
        summary = summarize(key_points)

        return f"[摘要] {summary}"

    def _count_tokens(self, text: str) -> int:
        """估算 token 数量"""
        return len(text.split()) * 1.3  # 粗略估计
```

#### 增量摘要

```python
class IncrementalSummarizer:
    """增量摘要器"""

    def __init__(self, summary_interval: int = 10):
        self.summary_interval = summary_interval
        self.summaries = []

    def add_messages(self, messages: list) -> str:
        """添加消息并生成摘要"""
        # 每隔 N 条消息生成一次摘要
        if len(messages) % self.summary_interval == 0:
            summary = self._generate_summary(messages[-self.summary_interval:])
            self.summaries.append(summary)

        # 返回完整的摘要历史
        return "\n\n".join(self.summaries)

    def _generate_summary(self, messages: list) -> str:
        """生成消息摘要"""
        # 提取关键信息
        key_info = {
            'tasks': self._extract_tasks(messages),
            'decisions': self._extract_decisions(messages),
            'errors': self._extract_errors(messages),
            'outcomes': self._extract_outcomes(messages)
        }

        # 格式化摘要
        summary_parts = []
        if key_info['tasks']:
            summary_parts.append(f"任务: {', '.join(key_info['tasks'])}")
        if key_info['decisions']:
            summary_parts.append(f"决策: {', '.join(key_info['decisions'])}")
        if key_info['errors']:
            summary_parts.append(f"错误: {', '.join(key_info['errors'])}")
        if key_info['outcomes']:
            summary_parts.append(f"结果: {', '.join(key_info['outcomes'])}")

        return " | ".join(summary_parts)
```

### 策略 2：掩码策略

#### 按需加载

```python
class LazyContextLoader:
    """懒加载上下文"""

    def __init__(self):
        self.loaded_references = {}
        self.reference_metadata = {}

    def load_reference(
        self,
        ref_name: str,
        force: bool = False
    ) -> str | None:
        """
        按需加载参考文档

        Args:
            ref_name: 参考文档名称
            force: 是否强制重新加载
        """
        # 已加载且不强制
        if ref_name in self.loaded_references and not force:
            return self.loaded_references[ref_name]

        # 检查元数据
        metadata = self.reference_metadata.get(ref_name)
        if not metadata:
            return None

        # 按需决策
        if self._should_load(metadata):
            content = self._load_from_disk(ref_name)
            self.loaded_references[ref_name] = content
            return content

        return None

    def _should_load(self, metadata: dict) -> bool:
        """判断是否应该加载"""
        # 判断逻辑：
        # 1. 是否被明确请求
        # 2. 相关性分数
        # 3. 当前 token 使用率

        relevance = metadata.get('relevance', 0)
        token_usage = metadata.get('token_usage', 0)

        return relevance > 0.7 or token_usage < 0.8
```

### 策略 3：缓存策略

#### 智能缓存

```python
class SmartCache:
    """智能缓存系统"""

    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}

    def get(self, key: str) -> any:
        """获取缓存"""
        if key in self.cache:
            # 更新访问计数
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None

    def set(self, key: str, value: any, priority: int = 1):
        """设置缓存"""
        # 缓存已满，清理低优先级项
        if len(self.cache) >= self.max_size:
            self._evict_low_priority()

        self.cache[key] = value
        self.access_count[key] = 0

    def _evict_low_priority(self):
        """淘汰低优先级缓存"""
        # 按 (访问次数 * 优先级) 排序
        items = list(self.cache.items())
        items.sort(key=lambda x: self.access_count.get(x[0], 0) * x[1].get('priority', 1))

        # 移除最低分项
        if items:
            key_to_remove = items[0][0]
            del self.cache[key_to_remove]
            del self.access_count[key_to_remove]

# 使用示例
cache = SmartCache()

# 缓存解析结果
code_structure = parse_code('main.py')
cache.set('code:main.py', code_structure, priority=2)

# 获取缓存
cached = cache.get('code:main.py')
if cached:
    use_cached_structure(cached)
```

---

## 优化检查清单

### 问题诊断

- [ ] 对话长度是否合理
- [ ] 是否有重复提问
- [ ] 中间信息是否被遗忘
- [ ] 是否存在信息冲突

### 压缩策略

- [ ] 历史对话已摘要
- [ ] 关键决策已保留
- [ ] 错误信息已保留
- [ ] 无关信息已过滤

### 掩码策略

- [ ] 参考文档按需加载
- [ ] 详细信息延迟加载
- [ ] 避免一次性加载所有内容

### 缓存策略

- [ ] 解析结果已缓存
- [ ] 频繁访问内容已缓存
- [ ] 缓存有淘汰机制

---

## 最佳实践

### 1. 分阶段处理

```python
# ❌ 一次性处理所有信息
def process_large_file(filename):
    content = read_file(filename)  # 可能很大
    result = analyze(content)
    return result

# ✅ 分阶段处理
def process_large_file(filename):
    # 第一阶段：获取结构
    structure = get_file_structure(filename)

    # 第二阶段：按需加载
    for section in structure.sections:
        content = load_section(filename, section)
        result = analyze_section(content)

    return aggregate_results(results)
```

### 2. 渐进式信息披露

```python
# ❌ 一次性提供所有信息
def provide_context():
    return """
    这是项目的完整文档，包括架构、API、配置等...
    （可能 10000+ tokens）
    """

# ✅ 渐进式披露
def provide_context():
    return """
    项目概述：这是一个 Web 应用

    需要详细信息时，可查阅：
    - [架构设计](docs/architecture.md)
    - [API 文档](docs/api.md)
    - [配置指南](docs/config.md)

    （约 100 tokens）
    """
```

---

## 相关参考

- [上下文优化策略](../references/context-optimization.md)
- [多代理协调模式](../multi-agent-coordinator/SKILL.md)
