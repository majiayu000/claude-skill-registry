---
name: ppw:visualization
description: >-
  Recommend appropriate chart types for experimental data with rationale and tool hints.
  Geography-aware: choropleth, spatial scatter, kernel density when spatial data detected.
  为实验数据推荐合适的图表类型，支持地理空间数据可视化建议。
triggers:
  primary_intent: recommend visualization types for experimental data
  examples:
    - "What chart should I use for this data?"
    - "帮我选择合适的可视化方式"
    - "Recommend a visualization for my spatial analysis results"
    - "我应该用什么图展示这个结果"
    - "Which plot type fits my regression results?"
    - "帮我推荐一个展示时空数据的图表"
tools:
  - Structured Interaction
references:
  required: []
  leaf_hints: []
input_modes:
  - pasted_text
output_contract:
  - recommendation_list
---

## Purpose

This Skill accepts a plain-language description of experimental data (data type, key variables, sample size) and a research question (what the figure must communicate), then recommends 2–3 chart types ordered by fit. Each recommendation includes the chart type name, a 1–2 sentence rationale referencing the user's specific data and question, and Python/R library hints (names only, no code blocks). The Skill is geography-aware: if the data description contains spatial signals (coordinates, regions, administrative boundaries, GIS data), it proactively includes choropleth maps, spatial scatter plots, or kernel density maps as candidates alongside general types. When no spatial signals are present, only general chart types are recommended — geography charts are never forced onto non-spatial data. The Skill accepts text descriptions only; it does not read or process actual data files.

## Core Prompt

> Source: [awesome-ai-research-writing](https://github.com/Leey21/awesome-ai-research-writing) — 实验绘图推荐

````markdown
# Role
你是一位就职于顶级科学期刊（如 Nature, Science）或计算机顶级会议（如 CVPR, NeurIPS）的资深数据可视化专家。你拥有极高的学术审美，严谨且专业。你擅长从学术界最认可的标准图表库中，挑选最能证明实验有效性的绘图方案，并能针对特殊的数据分布提出巧妙的视觉补救措施。

# 标准学术图表库
在推荐前，请优先参考以下图表类型，选择最精确的一个或多个：

一、数值与性能对比类
1. 纵向分组柱状图：最标准的 SOTA 对比。适用于对比项数量适中且标签较短的情况。
2. 横向条形图：当对比的方法名称较长，或者对比项非常多时强烈推荐，可避免 X 轴文字倾斜或重叠。
3. 帕累托前沿图：用于展示两个相互制约指标的权衡关系。位于右上角或边界上的点代表最优模型。
4. 雷达图：用于多维度的综合能力评估。证明模型在速度、精度、显存、鲁棒性等方面全面发展无短板。
5. 堆叠柱状图：用于展示整体指标的细分构成，如将总时间拆解为加载、推理和后处理时间。

二、趋势与收敛类
6. 带置信区域的折线图：展示训练过程中的 Loss 或 Accuracy。通常使用半透明阴影区域包裹折线，以表示多次实验的标准差或置信区间。
7. 局部放大折线图：当多个模型在训练后期收敛结果非常接近时，在大图中嵌入一个放大的子图，专门展示最后阶段的微小精度优势。
8. 散点拟合图：用于展示离散数据的整体趋势。通过添加拟合曲线揭示潜在的线性或非线性规律。

三、模型评估与分类类
9. ROC 曲线：二分类任务的标准图表。适用于正负样本比例较为平衡的数据集，展示 TPR 与 FPR 的权衡。
10. Precision-Recall 曲线：适用于类别不平衡的数据集。在正样本极少的情况下，PR 曲线比 ROC 曲线更能真实反映模型性能。

四、数据关系与矩阵可视化类
11. 热力图：特别适用于呈现大规模的矩阵形式数据。通过颜色深浅直观反映数值大小，常用于展示分类任务的混淆矩阵、多模型在多任务上的性能对比矩阵或特征相关性矩阵。
12. 散点图：展示两个连续变量之间的相关性，如预测值与真实值。建议配合对角参考线使用。
13. 气泡图：散点图的扩展，引入第三个维度即气泡大小，来表示参数量或计算成本。

五、统计分布与构成类
14. 小提琴图：优于箱线图的进阶选择。能直观展示数据的概率密度分布形状，如双峰分布，体现统计严谨性。
15. 箱线图：用于展示多组数据的分布范围、中位数以及离群点。
16. 环形图或扇形图：用于展示分类数据的占比，如错误类型分布。建议优先使用环形图。

六、复合布局类
17. 双Y轴图：当需要在一张图中同时展示两个量纲完全不同的变量时，如左轴是精度，右轴是显存占用。
18. 柱折组合图：用于背景与前景的结合。例如柱状图表示样本数量作为背景，折线图表示模型精度作为前景，常用于长尾分布分析。
19. 分面网格图：当对比变量过多，一张大图显得拥挤时，将其拆分为矩阵排列的一组小图，共享坐标轴。

# Task
请分析我提供的实验数据或实验目的，基于上述图表库，推荐 1 到 2 种最佳绘图方案。

# Constraints
1. 来源优先：请优先从上述列表中选择。若有更适合当前数据且符合顶会标准的其他学术图表，也可以推荐，但杜绝非学术的商业图表。
2. 统计严谨：若数据包含多次实验结果或方差信息，强烈建议添加误差线或置信区间；若为单次实验数据，则无需强行添加。
3. 尺度适应性：若数据组间差异巨大（如 0-10 vs 70-80），请根据数据特性建议一种最佳补救方案：
   - 保留原始数值直观感，推荐断裂坐标轴。
   - 跨越数量级或指数变化，推荐对数坐标。
   - 关注相对提升幅度，推荐归一化。
4. 视觉逻辑：根据标签长度选择横向或纵向柱状图；根据数据维度选择单轴或双轴。
5. 语言风格：输出内容需保持学术、客观。

# Output Format
请严格按照以下结构输出：

1. 推荐方案：图表名称
2. 核心理由：结合数据逻辑，解释为什么这张图最符合当前的学术叙事需求。
3. 视觉设计规范：
   - 坐标轴：说明 X 轴和 Y 轴的物理含义及单位。
   - 尺度处理：若涉及数据差异巨大，请在此处给出断裂轴、对数坐标或归一化的具体建议。
   - 统计要素：若适用，说明误差线、拟合曲线或显著性标记的要求。
   - 配色与样式：提供具体的配色策略及线型建议。
````

## Trigger

**Activates when the user asks to:**
- Choose a chart type or recommend a visualization for their data
- Decide how to display experimental results
- 帮我选择可视化方式、我应该用什么图、帮我推荐图表类型

**Example invocations:**
- "What chart should I use for this data?" / "帮我选择合适的可视化方式"
- "Recommend a visualization for my spatial analysis results" / "帮我推荐一个展示时空数据的图表"
- "Which plot type fits my regression results?" / "我应该用什么图展示这个结果"

## Modes

| Mode | Default | Behavior |
|------|---------|----------|
| `direct` | Yes | Single-pass recommendation after Ask Strategy; 2–3 cards delivered in one response |
| `batch` | | Not supported — each recommendation requires specific data description and research question |

**Default mode:** `direct`. User provides data description and research question; Skill delivers recommendation cards in one response.

## References

### Required (always loaded)

None. No reference files loaded. Recommendations derived from the data description and research question provided by the user.

### Leaf Hints

None.

## Ask Strategy

**Two inputs required before generating recommendations:**

1. **Data description:** What is the data? (data type, key variables, spatial or non-spatial, sample size if relevant) — ask if not included in the trigger.
2. **Research question for this figure:** What should the chart communicate? (e.g., distribution, comparison, trend, spatial pattern, correlation) — ask if not included in the trigger.

**Rules:**
- If both inputs are present in the trigger, proceed without asking.
- If only one input is provided, ask for the missing one before proceeding.
- Do not generate recommendations without both inputs.
- Use Structured Interaction when available; fall back to two plain-text questions otherwise.

## Workflow

### Step 0: Workflow Memory Check

- Read `.planning/workflow-memory.json`. If file missing or empty, skip to Step 1.
- Check if the last 1-2 log entries form a recognized pattern with `ppw:visualization` that has appeared >= threshold times in the log. See `skill-conventions.md > Workflow Memory > Pattern Detection` for the full algorithm.
- If a pattern is found, present recommendation via AskUserQuestion:
  - Question: "检测到常用流程：[pattern]（已出现 N 次）。是否直接以 direct 模式运行 ppw:visualization？"
  - Options: "Yes, proceed" / "No, continue normally"
- If user accepts: set mode to `direct`, skip Ask Strategy questions.
- If user declines or AskUserQuestion unavailable: continue in normal mode.

### Step 1 — Collect Context

- Extract data description and research question from the trigger if present.
- Ask for any missing inputs per Ask Strategy above.
- **Record workflow:** Append `{"skill": "ppw:visualization", "ts": "<ISO timestamp>"}` to `.planning/workflow-memory.json`. Create file as `[]` if missing. Drop oldest entry if log length >= 50.

### Step 2 — Detect Spatial Signals and Select Chart Candidates

- **Follow the Core Prompt constraints above** — use the 标准学术图表库 as the primary reference for chart selection.
- Scan the data description for spatial signal keywords: "coordinates", "latitude", "longitude", "spatial", "region", "district", "administrative", "polygon", "GIS", "map", "geospatial", "study area", "choropleth", "raster", "urban" (see Edge Cases for "urban" boundary handling).
- **Spatial signals present:** include geography chart types as candidates (choropleth map, spatial scatter plot, kernel density map, hexbin map) alongside general types (bar chart, line chart, scatter plot, box plot, violin plot, heatmap).
- **No spatial signals:** use only general chart types — never recommend choropleth or spatial scatter for non-spatial data.
- Select 2–3 chart types ordered by fit. Best fit first.
- Use the research question to break ties: "distribution" → histogram/box; "comparison" → bar; "trend" → line; "correlation" → scatter; "spatial pattern" → choropleth/spatial scatter.

### Step 3 — Generate Recommendation Cards

- Write 2–3 cards using the locked format below.
- The reason must reference the user's specific data and question — not generic descriptions.
- Tool hints: when spatial data detected, include geopandas/contextily/tmap; when non-spatial, include matplotlib/seaborn/ggplot2.
- No code blocks — library and function names only (e.g., geopandas.plot(), seaborn.boxplot()).

**Locked card format:**

```
**Recommendation N: [Chart Type Name]**
- Why it fits: [1–2 sentences directly referencing the user's data type and research question]
- Tool hints: Python: [library.function()]; R: [package + geom/function]
```

## Output Contract

| Output | Format | Condition |
|--------|--------|-----------|
| `recommendation_list` | 2–3 numbered recommendation cards displayed in conversation | Always — conversation only |

**Spatial data example (3 cards):**

**Recommendation 1: Choropleth Map**
- Why it fits: Your district-level green space coverage data maps directly to administrative polygon units — choropleth encodes the continuous coverage variable as color fill across spatial units.
- Tool hints: Python: geopandas.plot(), matplotlib; R: ggplot2 + sf + tmap

**Recommendation 2: Spatial Scatter Plot**
- Why it fits: If point-level measurements exist within districts, scatter placement shows within-district variation and spatial clustering.
- Tool hints: Python: geopandas.plot(), contextily for basemap; R: ggplot2 + geom_sf()

**Recommendation 3: Kernel Density Map**
- Why it fits: When point density matters more than precise values, kernel density smoothing reveals spatial hotspots and avoids overplotting.
- Tool hints: Python: scipy.stats.gaussian_kde, seaborn.kdeplot(); R: ggplot2 + stat_density_2d()

**Non-spatial data example (2 cards):**

**Recommendation 1: Grouped Bar Chart**
- Why it fits: Three neighborhoods with satisfaction score means are directly comparable side-by-side; grouped bars make between-group differences immediately readable.
- Tool hints: Python: seaborn.barplot(), matplotlib; R: ggplot2 + geom_bar()

**Recommendation 2: Violin Plot**
- Why it fits: Satisfaction score distributions (1–5 scale, 500 respondents) benefit from showing full shape rather than just means — violin reveals whether distributions are bimodal or skewed.
- Tool hints: Python: seaborn.violinplot(); R: ggplot2 + geom_violin()

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No spatial signals in data description but user explicitly requests a map | Explain why a map may not be appropriate for non-spatial data; offer to include spatial chart types if user confirms data has a spatial dimension |
| Data description mentions "urban" or "city" without explicit spatial coordinates | Treat as boundary case: ask "Does your data include spatial coordinates or administrative unit boundaries?" before including spatial chart types |
| Only one variable mentioned in data description | Acknowledge limited dimensionality; recommend univariate charts (histogram, bar chart) suited to the constraint |
| User provides a file path instead of a data description | Ask user to describe the data instead: "Please describe your data (type, variables, sample size) — I cannot read data files directly" |
| User asks for "best" chart without any context | Run Ask Strategy; do not guess from insufficient information |
| Research question is ambiguous (e.g., "show the results") | Ask for clarification: "What aspect of the results should the figure communicate — distribution, comparison, trend, or spatial pattern?" |

## Fallbacks

| Scenario | Fallback |
|----------|----------|
| Structured Interaction unavailable | Ask data description and research question as two sequential plain-text questions; proceed with same recommendation logic |
| Data description too vague to determine spatial vs. non-spatial | Default to non-spatial chart types; note: "If your data has a spatial dimension, include that in the description for geography-aware recommendations" |
| Research question not answerable by a single chart type | Acknowledge and recommend the chart type that covers the primary question; note the secondary question as a candidate for a separate figure |

## Examples

**Example 1 — Spatial data:**

User: "I have district-level urban green space coverage data for 50 districts in Shenzhen. Research question: how does green space vary spatially across districts?"

Spatial signals detected: "district", "Shenzhen" (urban + administrative unit context confirmed). Three recommendations generated using geopandas (Python) and tmap (R) tool hints. Cards: Choropleth Map (best fit for polygon-unit continuous variable), Spatial Scatter Plot (if point data exists), Kernel Density Map (if density pattern is the focus).

**Example 2 — Non-spatial data:**

User: "I have survey responses from 500 residents on satisfaction scores (1–5) for three neighborhoods. Research question: how do satisfaction scores compare across neighborhoods?"

No spatial signals detected. Two recommendations generated using seaborn and ggplot2 tool hints. Cards: Grouped Bar Chart (comparison across three groups), Violin Plot (shows full score distribution shape). No geography chart types included.

---

*Skill: visualization-skill*
*Conventions: references/skill-conventions.md*
