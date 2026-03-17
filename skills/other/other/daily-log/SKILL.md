---
name: daily-log
description: Generate structured daily operation logs following standardized format for memory persistence and progress tracking.
version: 1.1
---

# Daily Log Skill

Generate comprehensive daily operation logs to track work, decisions, and lessons learned.

## When to Use

Use this skill at the end of a work session or day to:
- Record completed tasks and their outcomes
- Track token usage and time spent
- Document key decisions and their rationale
- Capture lessons learned and mistakes
- Maintain continuity across sessions

---

## Log Format Templates

### Template A: Full Detail (Legacy)
Use for: Important milestones, detailed project records
See: [FULL_TEMPLATE](./FULL_TEMPLATE.md)

### Template B: Attention-Driven (Recommended)
Use for: Daily work logging, quick review
See below ⬇️

---

## Attention-Driven Log Format (v1.1)

```markdown
# YYYY-MM-DD 操作日志

## 📅 会话概览
- **日期**: YYYY-MM-DD
- **工作时段**: HH:MM - HH:MM (X小时X分钟)
- **核心成果**: [一句话总结当天最重要的产出]
- **关键决策**: [X] 个
- **经验教训**: [X] 个
- **Token 消耗**: ~XX,XXX

---

## ⏱️ 时间分布

| 时段 | 任务 | 时长 | 注意力权重 |
|------|------|------|-----------|
| HH:MM-HH:MM | [任务1] | X分钟 | 9/10 |
| HH:MM-HH:MM | [任务2] | X分钟 | 7/10 |
| ... | ... | ... | ... |

**时间分析**:
- 高注意力任务耗时: X% (主要集中在XX:XX-XX:XX)
- 中断/切换次数: X 次
- 效率峰值时段: XX:XX-XX:XX

---

## 🎯 高注意力任务 (权重 8-10)

### [任务名称] (权重: X/10, 时段: HH:MM-HH:MM, 耗时: X分钟)

**一句话总结**: [核心成果或决策]

**关键细节**:
- [具体数据/数字]
- [文件路径/名称]
- [决策原因]
- [验证结果]

**经验教训** (如适用):
- [学到的要点]

---

## 📋 中注意力任务 (权重 5-7)

| 任务 | 权重 | 时段 | 关键成果 |
|------|------|------|----------|
| [任务名] | 7/10 | HH:MM-HH:MM | [一句话描述] |
| [任务名] | 6/10 | HH:MM-HH:MM | [一句话描述] |

---

## 📝 低注意力任务 (权重 0-4)

- [HH:MM-HH:MM] [任务名] - [状态]
- [HH:MM-HH:MM] [任务名] - [状态]

---

## 📊 今日统计

| 项目 | 数值 |
|------|------|
| 高注意力任务 | X |
| 中注意力任务 | X |
| 低注意力任务 | X |
| 代码文件创建 | X |
| 代码文件修改 | X |
| Skill 创建/更新 | X |
| Token 消耗 | ~XX,XXX |
| Git 提交 | X |

---

## 💡 今日最大教训

**一句话总结**: [核心教训]

**背景**: [发生了什么]
**根本原因**: [为什么发生]
**改进措施**: [如何改进]

---

## 🔗 关键文件位置

### 高价值产出
- `path/to/key/file1` - [一句话描述]
- `path/to/key/file2` - [一句话描述]

---

*日志生成时间: YYYY-MM-DD HH:MM*  
*注意力评分: 高[X] 中[X] 低[X]*
```

---

## Attention Scoring System

### How to Score Task Attention (0-10)

| Factor | Weight | Indicator | Examples |
|--------|--------|-----------|----------|
| **关键决策** | +3 | 改变了方向或方案 | 选择方案B、批准实施、确认规范 |
| **教训/错误** | +3 | 发现问题并修复 | 违反规则、编译错误、逻辑bug |
| **里程碑** | +2 | 重要节点完成 | MVP完成、发布上线、功能验收 |
| **文件变更** | +1/个 | 创建/修改/删除文件 | 新建Skill、修改配置、重构代码 |
| **普通操作** | 0 | 常规查询或查看 | 查看状态、读取文件、检查日志 |

### Attention Level Guidelines

```
Score 8-10 (High): 
  → Full detail: summary + key details + lessons
  
Score 5-7 (Medium): 
  → Brief: one sentence summary + key outcomes
  
Score 0-4 (Low): 
  → Minimal: title + status only
```

### Examples

**Task: "设计 MissionSystem 架构方案"**
- 关键决策: +3 (选择了TK_SERIAL方案)
- 里程碑: +2 (设计完成)
- **Score: 8/10** → High attention

**Task: "修复编译错误"**
- 教训: +3 (学会了BinaryReader→TK转换)
- 文件变更: +8个文件修改 = +1 (max)
- **Score: 9/10** → High attention

**Task: "查看 git status"**
- 普通操作: 0
- **Score: 2/10** → Low attention

---

## Workflow

### Step 1: Review Session

At end of session/day:
1. List all tasks completed
2. Identify major decisions made
3. Note any mistakes or lessons
4. Check for milestones reached

### Step 2: Score Each Task

Apply attention scoring:
```
For each task:
  - Did it involve a key decision? (+3)
  - Was there a mistake/lesson? (+3)
  - Was it a milestone? (+2)
  - How many files changed? (+1 per, max 2)
  - Sum → Attention Score (0-10)
```

### Step 3: Categorize by Attention Level

- **High (8-10)**: Write detailed section
- **Medium (5-7)**: Add to table
- **Low (0-4)**: List as bullet points

### Step 4: Extract Key Information

For high-attention tasks, extract:
- One-sentence summary
- Key details (numbers, paths, outcomes)
- Lessons learned (if applicable)

### Step 5: Generate Log

Write to `memory/YYYY-MM-DD.md` using attention-driven template

### Step 6: Update Long-term Memory (Optional)

If significant decisions or patterns emerged, update MEMORY.md

---

## Best Practices

### ✅ Do
- **Score honestly** - Not every task is high attention
- **Focus on value** - What would you want to remember in a month?
- **Quantify** - Use numbers, file counts, token estimates
- **Link key files** - Only high-value outputs need paths
- **One lesson max** - Focus on the most important lesson of the day

### ❌ Don't
- Don't over-document low-attention tasks
- Don't skip lessons learned section
- Don't include full conversation transcripts
- Don't log routine checks (git status, etc.) unless relevant
- Don't wait too long (score while memory is fresh)

---

## Comparison: Full Detail vs Attention-Driven

### Scenario: MissionSystem MVP Implementation Day

**Full Detail Version**: ~500 lines, ~95,000 tokens to read
- Every task fully documented
- All file paths listed
- Complete error descriptions
- Full conversation context

**Attention-Driven Version**: ~150 lines, ~20,000 tokens to read
- 2-3 high-attention tasks detailed
- 3-4 medium tasks in table
- 5+ low tasks as bullets
- Key decisions and lessons highlighted

**Review Time**:
- Full Detail: 10-15 minutes to scan
- Attention-Driven: 2-3 minutes to understand

---

## Version History

- **v1.1** (2026-02-12) - Added Attention-Driven logging
  - Attention scoring system (0-10)
  - Three-level detail format
  - Focus on high-value information
  - Reduced log size by 60-70%

- **v1.0** (2026-02-10) - Initial release
  - Standardized log format
  - 7-section structure
  - Statistics tracking
  - Lessons learned framework
