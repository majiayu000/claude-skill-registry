---
name: build-plans
description: 当你已经有了多步任务的规格说明或需求,但在动手写代码之前,请使用此技能编写实施计划.
---

# 编写计划 (Writing Plans)

## 概述 (Overview)

编写一份详尽的实施计划. 假设负责执行的工程师对我们的代码库完全不了解,且审美和习惯尚待磨合. 文档中需包含他们需要知道的一切信息: 每个任务涉及哪些文件、代码实现思路、测试方案、需要查看的文档以及如何进行验证. 将整个计划分解为易于消化的小型任务 (Bite-sized tasks). 遵循原则: DRY (Don't Repeat Yourself), YAGNI (You Ain't Gonna Need It), TDD (Test-Driven Development) 以及频繁提交 (Frequent commits).

假设开发者技术娴熟,但对我们的工具集或问题领域几乎一无所知. 假设他们不太擅长良好的测试设计.

**启动声明:** "我正使用 writing-plans 技能来创建实施计划."

**上下文:** 此计划应在专门的工作区执行 (通过 brainstorming 技能创建).

**计划保存路径:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小型任务粒度 (Bite-Sized Task Granularity)

**每一步应为一个独立的动作 (2-5 分钟):**

- "编写失败的测试" —— 步骤
- "运行测试以确保其失败" —— 步骤
- "实现最简代码使测试通过" —— 步骤
- "运行测试并确保其通过" —— 步骤
- "提交代码 (Commit)" —— 步骤

## 计划文档头部 (Plan Document Header)

**每份计划必须以上述头部开始:**

```markdown
# [功能名称] 实施计划

> **致代理:** 必需子技能: 使用 superpowers:executing-plans 按任务逐个实施此计划.

**目标:** [用一句话描述此功能构建的内容]

**架构:** [用 2-3 句话描述实现方法]

**技术栈:** [关键技术/库]

---
```

## 任务结构 (Task Structure)

````markdown
### 任务 N: [组件名称]

**涉及文件:**

- 新建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

**步骤 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2: 运行测试并验证失败**

运行: `pytest tests/path/test.py::test_name -v`
预期结果: 失败 (FAIL), 提示 "function not defined"

**步骤 3: 编写最简实现**

```python
def function(input):
    return expected
```

**步骤 4: 运行测试并验证通过**

运行: `pytest tests/path/test.py::test_name -v`
预期结果: 通过 (PASS)

**步骤 5: 提交 (Commit)**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 注意事项 (Remember)

- 始终使用精确的文件路径.
- 计划中提供完整的代码 (不要只写 "添加验证").
- 提供精确的命令及预期输出.
- 使用 @ 语法引用相关技能.
- 坚持 DRY, YAGNI, TDD, 频繁提交.

## 执行交付 (Execution Handoff)

保存计划后,提供执行选项:

**"计划已完成并保存至 `docs/plans/<filename>.md`. 有两种执行方案可选:**

**1. 子代理驱动 (此会话)** —— 我将为每个任务指派新的子代理,任务间进行评审,迭代迅速.

**2. 并行会话 (独立)** —— 使用 executing-plans 开启新会话,带检查点的批量执行.

**请问选择哪种方式?"**

**如果选择子代理驱动:**

- **必需子技能:** 使用 superpowers:subagent-driven-development
- 留在当前会话.
- 每个任务指派新的子代理 + 代码评审.

**如果选择并行会话:**

- 引导用户在工作区开启新会话.
- **必需子技能:** 新会话使用 superpowers:executing-plans
