---
name: skssearch
description: 搜索 SkillsMP skill 库。当用户描述需求、询问某类 skill 是否存在、或明确搜索时触发。
---

# skssearch

## 关键词生成（最关键）

SkillsMP 只支持英文。关键词生成的核心原则：

> **像 skill 作者一样思考，而不是像用户一样搜索。**
> Skill 以「能力」命名，不以「需求」命名。

### 第一步：提取意图

从用户描述中识别：
- **核心动作**：用户想让 skill 做什么？（write / review / generate / analyze / test / format / search...）
- **目标对象**：作用在什么上？（readme / code / csv / api / image / pr / commit...）
- **领域/技术栈**（如有）：react / python / sql / docker / markdown...

### 第二步：生成关键词

用 1-2 个词，优先选：

| 策略 | 示例 |
|------|------|
| 动作名词（skill 最常见命名） | `reviewer`、`writer`、`generator`、`analyzer` |
| 领域词（单词）| `csv`、`testing`、`readme`、`documentation` |
| 动作+领域（精确时用） | `code review`、`readme writer` |

**不要用**：完整需求描述（`help me write project documentation`）、实现细节（`using langchain to process csv`）、中文词（无效）

### 第三步：选最优关键词

- 优先选覆盖面最广的词（`testing` > `pytest unit test`）
- 同一概念有多个英文词时，选 skill 作者最可能用的那个
- 不确定时，选最短的那个

### 示例

| 用户说的 | 思考过程 | 关键词 |
|---------|---------|--------|
| "帮我找个写 README 的" | 动作=write，对象=readme → skill 作者会叫它 readme writer | `readme writer` |
| "有没有代码审查的？" | 动作=review，对象=code → 常见名 | `code review` |
| "我需要处理 CSV 文件" | 对象=csv，动作=process → 领域词更精准 | `csv` |
| "找个能生成单元测试的" | 动作=generate，对象=test → 领域词 | `testing` |
| "有 React 相关的吗" | 技术栈=react → 直接用 | `react` |
| "想找个调试助手" | 动作=debug → 动作名词 | `debugging` |

## 执行

确定关键词后，**直接运行**，不要询问确认：

```bash
python3 "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/skssearch/search.py" "<KEYWORD>"
```
