# summarize-skill

**用途**: 总结执行结果，生成友好的摘要

**输入**: 执行日志、创建的文件列表

**输出**: 用户友好的摘要

---

## 核心能力

1. **提取关键信息** - 从日志中提取重要信息
2. **统计汇总** - 统计文件数量、类型等
3. **生成可读摘要** - 转换为用户易懂的语言
4. **提供下一步指引** - 告诉用户接下来做什么

---

## 输入格式

```yaml
input:
  created_files: array      # 创建的文件列表
  execution_logs: array     # 执行日志
  system_name: string       # 系统名称
  structure: object         # 系统结构
```

---

## 输出格式

```yaml
output:
  summary:
    success: boolean
    total_files: number
    breakdown:              # 文件分类统计
      agents: number
      skills: number
      workflows: number
      data_files: number
      docs: number
    
    created_at: string
    duration_seconds: number
  
  display_text: string      # 友好展示（用 emoji）
  next_steps: array         # 下一步建议
  links: array              # 重要文件的链接
```

---

## 执行逻辑

### 1. 统计文件

```python
def categorize_files(files):
    breakdown = {
        "agents": 0,
        "skills": 0,
        "workflows": 0,
        "data_files": 0,
        "docs": 0
    }
    
    for file in files:
        if "/agents/" in file:
            breakdown["agents"] += 1
        elif "/skills/" in file:
            breakdown["skills"] += 1
        elif "/workflows/" in file:
            breakdown["workflows"] += 1
        elif "/data/" in file:
            breakdown["data_files"] += 1
        elif file.endswith(".md"):
            breakdown["docs"] += 1
    
    return breakdown
```

### 2. 生成友好文本

```python
def format_summary(system_name, breakdown, next_steps):
    text = f"✅ {system_name} 创建完成！\n\n"
    text += f"📁 系统结构:\n"
    text += f"  - {breakdown['agents']} 个 Agent\n"
    text += f"  - {breakdown['skills']} 个 Skills\n"
    text += f"  - {breakdown['workflows']} 个 Workflows\n\n"
    text += f"🚀 下一步:\n"
    for i, step in enumerate(next_steps, 1):
        text += f"  {i}. {step}\n"
    
    return text
```

---

## 示例

**输入**:
```yaml
created_files:
  - "health-system/.claude/agents/health-advisor.md"
  - "health-system/.claude/skills/checkup-analysis/SKILL.md"
  - "health-system/.claude/workflows/daily-check.yaml"
  # ... 更多文件
  
system_name: health-system

structure:
  agents: 1
  skills: 8
  workflows: 3
```

**输出**:
```yaml
summary:
  success: true
  total_files: 25
  breakdown:
    agents: 1
    skills: 8
    workflows: 3
    data_files: 3
    docs: 2
  created_at: "2026-01-19T15:30:00Z"
  duration_seconds: 120

display_text: |
  ✅ health-system 创建完成！
  
  📁 系统结构:
    - 1 个 Agent（健康顾问）
    - 8 个 Skills（体检分析、指标追踪等）
    - 3 个 Workflows（每日检查、每周报告、体检分析）
  
  🚀 下一步:
    1. 填写 data/profile/profile.json（你的基本信息）
    2. 试用: "执行每日健康检查"
    3. 上传体检报告测试分析功能

next_steps:
  - "填写个人档案"
  - "记录今日数据"
  - "触发首次检查"

links:
  - path: "health-system/README.md"
    title: "使用说明"
  - path: "health-system/DESIGN.md"
    title: "设计文档"
```

---

## 评价标准

- 信息完整性（40%）
- 可读性（30%）
- 指引清晰度（20%）
- 友好度（10%）

通过条件：>= 7.0

---

## 版本历史

- v1.0.0 (2026-01-19): 初始版本
