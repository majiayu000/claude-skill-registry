---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation). NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.
metadata:
  short-description: 系统化调试与根因分析
  keywords:
    - systematic-debugging
    - 调试
    - Bug 修复
    - 根因分析
    - 问题诊断
    - 堆栈追踪
    - 生产环境调试
    - root cause
    - debugging
  category: 调试
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
  iron-law: |
    NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
---

# Systematic Debugging - 系统化调试

## 铁律

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**违反规则的信件就是违反规则的精神。**

**无例外**：
- 不跳过根因调查直接修复
- 不基于猜测进行修复
- 不尝试多个更改同时测试
- 不在不完全理解的情况下修复

---

## 常见合理化

| 借口 | 现实 |
|------|------|
| "快速修复现在，稍后调查" | 永不会有"稍后"。技术债积累 |
| "尝试改变 X，看是否有效" | 猜测不是调试。可能碰巧修复但未理解 |
| "添加多个更改，运行测试" | 无法确定哪个更改有效。浪费调试时间 |
| "可能大概差不多是 X" | 模糊理解导致错误修复 |
| "不完全理解但可能有效" | 理解不完全=修复不完整 |

---

## 红色标志 - 停止并重新开始

- "快速修复现在，稍后调查"
- "尝试改变 X，看是否有效"
- "添加多个更改，运行测试"
- "可能大概差不多是 X，让我修复"
- "不完全理解但可能有效"
- 基于猜测而非证据的修复

**所有这些意味着：停止修复。回到根因调查阶段。**

---

## 四阶段框架

### 阶段 1：根因调查

**任何修复前**：

1. **仔细阅读错误消息**
   - 不要跳过错误或警告
   - 它们通常包含确切解决方案

2. **一致复现**
   - 你能可靠触发吗？

3. **检查最近变更**
   - 什么变更可能导致此问题？

4. **多组件系统收集证据**
   ```bash
   # 对于每个组件边界：
   - 记录进入组件的数据
   - 记录退出组件的数据
   - 验证环境/配置传播
   - 检查每层状态
   运行一次以收集显示何处中断的证据
   然后分析证据以识别失败组件
   然后调查该特定组件
   ```

5. **追踪数据流**
   - 向后追踪到坏值起源

### 阶段 2：模式分析

1. **找到工作示例**
2. **与参考对比**
3. **识别差异**
4. **理解依赖**

### 阶段 3：假设与测试

1. **形成单一假设**："我认为 X 是根本原因，因为 Y"
2. **最小化测试**：进行最小可能更改
3. **验证后再继续**
4. **3+ 次修复失败时：质疑架构**

### 阶段 4：实现

1. **创建失败测试用例**
2. **实施单一修复**
3. **验证修复**
4. **如果 3+ 次修复失败：质疑架构**

---

## 核心理念

**系统化调试** 不是碰运气，而是方法化地解决问题的科学流程。

```
┌─────────────────────────────────────────────────────────┐
│  收集证据 → 形成假设 → 系统验证 → 定位根因 → 实施修复  │
└─────────────────────────────────────────────────────────┘
```

**核心原则**：
- **基于证据，而非猜测**
- **治疗根本原因，而非症状**
- **一次验证一个假设**
- **记录整个过程**

---

## 何时使用本技能

在以下场景时激活：

- 出现错误、异常、Bug
- 需要分析堆栈追踪（Stack Trace）
- 提到"调试"、"排查问题"、"定位根因"
- 生产环境问题分析
- 跨文件或跨模块的问题追踪
- 间歇性 Bug（时有时无）

---

## 调试工作流程

### 步骤 1：收集证据 📋

**信息收集清单**：

| 证据类型 | 收集方法 | 重要性 |
|---------|---------|--------|
| **完整堆栈追踪** | 复制完整错误信息 | ⭐⭐⭐⭐⭐ |
| **相关日志** | 查看应用日志 | ⭐⭐⭐⭐⭐ |
| **复现步骤** | 记录如何触发问题 | ⭐⭐⭐⭐ |
| **环境信息** | OS、版本、依赖 | ⭐⭐⭐ |
| **代码变更** | 最近的 Git 提交 | ⭐⭐⭐⭐ |
| **用户输入** | 触发问题的数据 | ⭐⭐⭐ |

**堆栈追踪分析示例**：

```python
# 示例错误
Traceback (most recent call last):
  File "app.py", line 45, in process_order
    result = payment_service.charge(amount)
  File "payment.py", line 78, in charge
    return api_client.post("/charge", data)
  File "api.py", line 23, in post
    response = self.session.request(method, url, **kwargs)
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**分析要点**：
1. **从下往上读**：最下面是根本原因
2. **追踪调用链**：app.py → payment.py → api.py
3. **识别错误类型**：SSL 证书验证失败
4. **定位失败点**：api.py 第 23 行

### 步骤 2：形成假设 💡

**假设生成规则**：

1. **基于证据**：不要凭空猜测
2. **优先考虑最近变更**
3. **从简单到复杂排序**
4. **一次只关注一个假设**

**假设模板**：

```
假设：[问题描述] 的原因是 [根本原因]
触发条件：[什么情况下会出现]
验证方法：[如何证明或否定]
```

**假设示例**：

```
假设：SSL 错误的原因是生产环境缺少证书文件
触发条件：部署到生产环境后首次调用 API
验证方法：检查 /etc/ssl/certs/ 目录是否存在证书
```

**常见根因分类**：

| 类别 | 典型原因 | 检查方法 |
|------|---------|---------|
| **配置问题** | 环境变量、配置文件错误 | 检查 .env、config |
| **依赖问题** | 版本冲突、缺失依赖 | 检查 requirements.txt |
| **数据问题** | 空值、格式错误、边界值 | 检查输入数据 |
| **并发问题** | 竞态条件、死锁 | 检查锁、线程安全 |
| **资源问题** | 内存泄漏、连接池耗尽 | 检查资源使用 |
| **逻辑错误** | 边界条件、空值处理 | 代码审查 |

### 步骤 3：系统验证 🔍

**验证原则**：

1. **一次验证一个假设**（控制变量）
2. **设计最小化验证实验**
3. **记录验证过程和结果**
4. **用排除法缩小范围**

**验证方法**：

```python
# 方法 1：添加日志
def process_order(order_id):
    logger.info(f"Processing order: {order_id}")
    order = get_order(order_id)
    logger.debug(f"Order data: {order}")
    # ...

# 方法 2：断点调试
import pdb; pdb.set_trace()

# 方法 3：简化输入
def test():
    # 用最小输入验证
    process_order({"id": 1, "amount": 0})
```

**验证记录模板**：

```markdown
## 假设验证记录

### 假设 1：证书文件缺失
- **验证方法**：检查文件是否存在
- **验证结果**：❌ 文件存在
- **结论**：假设不成立，排除

### 假设 2：证书过期
- **验证方法**：检查证书有效期
- **验证结果**：✅ 证书已于 3 天前过期
- **结论**：假设成立，定位根因
```

### 步骤 4：定位根因 🎯

**区分症状与根因**：

使用**五问法**（5 Whys）深入挖掘：

```
问题：订单处理失败

Why 1: 为什么失败？
→ API 调用返回 500 错误

Why 2: 为什么 API 返回 500？
→ 数据库查询超时

Why 3: 为什么查询超时？
→ 缺少索引导致全表扫描

Why 4: 为什么缺少索引？
→ 新增字段时未同步添加索引

Why 5: 为什么未添加索引？
→ 没有 Code Review 流程

根因：缺少 Code Review 机制（而非"API 返回 500"）
```

**根因特征**：
- ✅ **可操作**：可以采取措施
- ✅ **可预防**：可以防止再次发生
- ✅ **系统级**：不是个人失误

### 步骤 5：实施修复 🔧

**修复原则**：

1. **最小化修复范围**
2. **添加回归测试**
3. **修复后验证**
4. **更新文档**

**修复清单**：

```markdown
## 修复计划

### 代码修复
- [ ] 修改代码：[具体位置]
- [ ] 添加测试：[测试用例]
- [ ] 运行测试确认通过

### 预防措施
- [ ] 添加检查机制
- [ ] 更新文档
- [ ] 团队分享经验

### 验证
- [ ] 本地验证
- [ ] 测试环境验证
- [ ] 生产环境验证
```

---

## 调试技巧库

### 技巧 1：二分法调试

当问题可能出现在多个位置时：

```python
# 在中间点添加日志
def complex_function(data):
    logger.info("Step 1: Start")
    result1 = step1(data)
    logger.info(f"Step 1 result: {result1}")

    logger.info("Step 2: Start")
    result2 = step2(result1)
    logger.info(f"Step 2 result: {result2}")

    logger.info("Step 3: Start")
    result3 = step3(result2)
    logger.info(f"Step 3 result: {result3}")

    return result3
```

### 技巧 2：最小化复现

```python
# 从复杂场景中提取最小复现用例
def test_minimal_reproduction():
    # 不需要完整的订单数据
    order = {"amount": 100}  # 最小输入
    result = process_payment(order)
    assert result.success
```

### 技巧 3：对比法调试

```python
# 对比工作版本和失败版本
def test_working_vs_broken():
    # 工作版本
    result_working = old_api_call(data)

    # 失败版本
    try:
        result_broken = new_api_call(data)
    except Exception as e:
        print(f"Broken: {e}")

    # 对比差异
    compare_results(result_working, result_broken)
```

### 技巧 4：环境隔离

```bash
# 使用 Docker 隔离环境
docker run -it python:3.11 bash

# 或使用虚拟环境
python -m venv debug_env
source debug_env/bin/activate
```

---

## 常见问题模式

### 模式 1：时序问题

**症状**：间歇性失败，时好时坏

**根因**：竞态条件、异步操作未正确等待

**调试方法**：
```python
# 添加重试和延迟
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def flaky_operation():
    # 可能失败的操作
    pass
```

### 模式 2：内存问题

**症状**：性能逐渐下降，最终崩溃

**根因**：内存泄漏

**调试方法**：
```python
import tracemalloc

tracemalloc.start()
# ... 运行代码 ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### 模式 3：状态污染

**症状**：测试单独通过，批量运行失败

**根因**：测试间共享状态

**调试方法**：
```python
@pytest.fixture(autouse=True)
def reset_state():
    # 每个测试前重置状态
    reset_database()
    reset_cache()
    yield
    cleanup()
```

---

## 验证清单

修复完成后，检查：

- [ ] 根本原因已识别（非症状）
- [ ] 修复方案最小化
- [ ] 添加回归测试
- [ ] 本地验证通过
- [ ] 文档已更新（如需要）
- [ ] 团队已分享经验
- [ ] 预防措施已实施

---

## 相关参考

- [系统化调试指南](../references/debugging-systematic.md)
- [根因追踪](root-cause-tracing.md)
