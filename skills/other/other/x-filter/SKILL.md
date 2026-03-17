---
name: x-filter
description: Score and filter topics for X content creation using weighted criteria. Use when user wants to evaluate collected materials, filter topics by score, or mentions "filter topics", "score materials", "x-filter", "选题筛选". Applies 10-point scoring system with customizable weights.
---

# X Filter

Score and filter collected materials for X content creation. Topics scoring ≥7 points enter the creation pool.

## Scoring System (满分10分)

| Criteria | Weight | Description |
|----------|--------|-------------|
| **热度/趋势** | 4分 | Current popularity and trend momentum |
| **争议性** | 2分 | Discussion potential and debate value |
| **高价值** | 3分 | Information density and actionable insights |
| **账号定位相关** | 1分 | Alignment with account positioning |

**Threshold**: ≥7分 enters creation pool

## Prerequisites

- Materials from x-collect (or manual input)
- User profile from x-create/references/user-profile.md (for relevance scoring)

## Workflow

### Input

Accept materials from:
1. **x-collect output** - Structured material report
2. **Manual list** - User-provided topics/URLs
3. **Raw text** - Unstructured content to evaluate

### Scoring Process

For each material/topic:

**1. 热度/趋势 (Trending Score: 0-4)**
```
4分: 当前热门话题，大量讨论
3分: 近期热点，关注度上升
2分: 稳定话题，持续有人讨论
1分: 小众话题，关注度有限
0分: 过时话题，几乎无人讨论
```

**2. 争议性 (Controversy Score: 0-2)**
```
2分: 明显争议，多方观点对立
1分: 存在不同看法，可引发讨论
0分: 共识性话题，难以引发讨论
```

**3. 高价值 (Value Score: 0-3)**
```
3分: 硬核干货，可直接指导行动
2分: 有价值信息，提供新视角
1分: 一般信息，了解即可
0分: 低价值，无实质内容
```

**4. 账号定位相关 (Relevance Score: 0-1)**
```
1分: 与账号定位高度相关
0分: 与账号定位关联较弱
```

Check user profile at: `~/.claude/skills/x-create/references/user-profile.md`
If not found, assume domains: [AI/科技, 创业, 个人成长]

### Output Format

```markdown
# 选题筛选报告

## 筛选时间
{timestamp}

## 用户定位
- 领域: {domains}
- 人设: {persona_style}

## 筛选结果

### 入选创作池 (≥7分)

#### 1. {Topic Title} - **{total_score}分**
| 热度 | 争议性 | 高价值 | 相关性 |
|------|--------|--------|--------|
| {trending}/4 | {controversy}/2 | {value}/3 | {relevance}/1 |

- **推荐类型**: [短推文/Thread/评论回复]
- **推荐风格**: [高价值干货/犀利观点/热点评论/故事洞察/技术解析]
- **创作角度**: 建议的切入点
- **核心观点**: 可提炼的关键论点

#### 2. ...

### 待定 (5-6分)
- {Topic} - {score}分 - {原因}

### 淘汰 (<5分)
- {Topic} - {score}分 - {原因}

## 创作建议

入选 {n} 个选题，建议优先级：
1. {最高分选题} - 理由
2. {次高分选题} - 理由

下一步：运行 `/x-create {选题}` 开始创作
```

## Execution Steps

1. **Load materials** from x-collect or user input
2. **Read user profile** for relevance scoring
3. **Score each material** on 4 criteria
4. **Calculate totals** and sort by score
5. **Categorize**: ≥7 (入选), 5-6 (待定), <5 (淘汰)
6. **Generate recommendations** for top topics
7. **Output report** with next steps

## Example

Input from x-collect:
```
素材1: Claude 4.5 Opus发布
素材2: AI编程助手对比评测
素材3: OpenAI最新裁员新闻
```

Scoring:
```
Claude 4.5 Opus发布:
- 热度: 4/4 (刚发布，热门话题)
- 争议性: 1/2 (性能vs价格讨论)
- 高价值: 3/3 (新能力详解)
- 相关性: 1/1 (AI/科技相关)
- 总分: 9/10 ✓ 入选

AI编程助手对比评测:
- 热度: 2/4 (持续话题)
- 争议性: 2/2 (Cursor vs Copilot争论)
- 高价值: 3/3 (实用对比)
- 相关性: 1/1 (科技相关)
- 总分: 8/10 ✓ 入选

OpenAI最新裁员新闻:
- 热度: 3/4 (近期热点)
- 争议性: 1/2 (有讨论)
- 高价值: 1/3 (信息价值有限)
- 相关性: 0/1 (非核心领域)
- 总分: 5/10 × 待定
```

## Customization

Users can customize weights in user-profile.md:
```yaml
scoring:
  trending: 4      # 热度权重
  controversy: 2   # 争议性权重
  value: 3         # 高价值权重
  relevance: 1     # 相关性权重
  threshold: 7     # 入选阈值
```

## Integration

After filtering, suggest:
```
筛选完成！{n} 个选题入选创作池。

推荐优先创作：{top_topic}（{score}分）

下一步：运行 /x-create {top_topic} 开始创作
```
