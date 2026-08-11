---
name: 科研可视化工具
description: >-
  从数据剖析到出版级成图的完整可视化工具。先做数据剖析（列类型/样本量/分布/异常值/分组结构/相关性），
  再结合论证目标推荐图型，主动拦截科研画图经典错误，产出 Nature / Science / IEEE / Elsevier / PNAS /
  中文核心期刊级别的成图。覆盖数据 EDA、图表契约、选图决策、出版级绘制、程序自检 + AI 读图闭环、多格式
  导出和文件审计。数学建模场景额外支持三类图体系（原始数据/过程/结果）和子问题覆盖检查。
  当用户涉及论文配图、科研画图、数据可视化、选图、期刊投稿图、figure、出版级图表、matplotlib、seaborn、
  plotly、误差棒、显著性标注、色盲安全配色、矢量图导出、中文论文图表、多面板时使用。
---

# 科研可视化工具

> 从数据剖析到出版级成图 | Python + MATLAB | 自检 + AI 读图闭环

## 路径

- `SKILL_ROOT`：math-modeling-skill 仓库根目录（只读）。
- 本文件中所有 `tools/figure/...` 路径均相对于 `SKILL_ROOT`。
- CLI 命令使用 `"<SKILL_ROOT>/tools/figure/scripts/..."` 格式，确保从任何工作目录均可执行。
- Python import 使用 `sys.path.insert(0, os.path.join(SKILL_ROOT, 'tools', 'figure', 'scripts'))` 后导入。

## 概述

本工具融合 nature-figure 的图表契约/后端路由架构与 scipilot-figure-skill 的数据剖析/选图决策/自检闭环，
并扩展数学建模特有的三类图体系和子问题覆盖检查。**永远先思考再画**：

1. 先理解数据再选图——拿到数据先做 EDA，用事实驱动图型选择
2. 先想清楚"这张图要论证什么"——同样数据，不同论点 = 不同图
3. 主动拦截科研画图的经典错误，而不是顺从
4. 维度太多就建议拆图，不硬塞

**只覆盖纯数据图**：折线、柱状、散点、箱线/小提琴、热力图、误差棒、分布图、相关性矩阵、雷达图、
3D 曲面、多面板组合。**不做**示意图、流程图、架构图。

## 工作流

### 第 1 步：数据剖析

```bash
python "<SKILL_ROOT>/tools/figure/scripts/profile_data.py" data.csv --group group --group condition
```

输出：每列类型、样本量、缺失率、连续列描述统计 + 偏度 + 异常值、分组样本量分布、相关性矩阵、初步图型建议。
不会读报告？查 `tools/figure/references/guides/data_profiling.md`。

**重点核对**：列类型识别对不对？每组 n 是多少？是否高度偏态？是否需要对数轴？

**数学建模场景**：从题目分析报告提取全部子问题并规范为 `q1…qN`，按子问题核对行列、类型、缺失、
分组样本量、分布、异常值和单位。

### 第 2 步：图表契约

在选图之前，先填写五点契约（详见 `tools/figure/static/core/contract.md`）：

1. **核心结论**：一句话写出这张图必须捍卫的论点
2. **证据链**：每个面板对应论点的哪个证据环节
3. **版型**：quantitative grid / schematic-led composite / image plate + quant / asymmetric mixed-modality
4. **后端**：Python 或 MATLAB
5. **期刊/导出规范**：最终尺寸、可编辑文字、源数据、统计口径、导出格式

### 第 3 步：选图决策

**永远先选图型，再画图。** 图型选错，画得再好看也没用。

基于第 1、2 步的事实，查 `tools/figure/references/chart-types/chart_selection.md` 的决策框架：

- **按数据形态选图**：连续变量看分布→直方图/KDE/箱线，分类+连续看比较→箱线/柱状，两连续看关系→散点+回归，时间趋势→折线，多变量相关→热力图/pairplot
- **按论证意图选图**：同一批数据，不同论点→不同图（"整体差异"用箱线，"动态变化"用折线，"个体差异"用散点）
- **给出推荐 + 简短理由 + 1-2 个备选**
- 数据维度过多（分组组合 > 12）→ **明确建议拆图**
- 用户指定图型不适合数据 → **善意指出问题并说明更好的选择**（如 n<10 要画均值柱→建议箱线/stripplot）
- 数学建模场景：查 `chart_selection.md` 末尾的"数学建模场景速查"表
- **图型多样**：全文图型种类 ≥ 3 种，避免全部柱状或全部折线；每个面板回答唯一问题，不重复展示相同数据（详见 `design_theory.md` §11 反冗余清单）

### 第 4 步：查期刊规范

确定目标期刊后查 `tools/figure/references/quality/journal_specs.md` 拿到：单/双栏宽（mm 与 inch）、字号、
推荐字体、DPI、矢量格式偏好。不知道目标期刊就问一句。

### 第 5 步：配环境

**Python**：

```python
import sys, os
sys.path.insert(0, os.path.join(SKILL_ROOT, 'tools', 'figure', 'scripts'))
from setup_style import setup_style
setup_style(journal='nature', lang='en')             # 英文 Nature
setup_style(journal='general', lang='zh', serif_for_zh=True)   # 中文宋体混排
```

`SciencePlots` 装了自动用，没装回退到内置预设。

**MATLAB**：将 `ROLE_ROOT/scripts/apply_publication_style.m` 复制到 `PROJECT_ROOT/utils/` 后调用。

### 第 6 步：绘制

按 `tools/figure/references/api-templates/plot_recipes.md` 对应章节的配方画。每节都有可直接复制的代码 + 常见坑。

**Python** 画图时强制做到：
- `figsize=(目标宽, 目标高)` 单位英寸——直接定最终尺寸
- 用 `seaborn.color_palette('colorblind')` 或 Okabe-Ito + 冗余编码（不同线型/marker）
- 误差棒/阴影要在图注交代是 SD / SEM / 95% CI + n

**MATLAB**：按 `references/roles/编程手/scripts/apply_publication_style.m` 的出版规范绘制，用 `export_publication_figure()` 导出。

数学建模场景（两种语言均适用）：按三类图体系生成（原始数据图 / 过程图 / 结果图），每类至少 3 张、合计至少 9 张，且每个子问题在三类中各至少 1 张。**每类内部图型要有变化**（如原始数据类至少含 1 张分布图 + 1 张关系图），全文图型种类 ≥ 3 种。

### 第 7 步：自检闭环（三层全过）

1. **语义层**：`tools/figure/references/design/viz_pitfalls.md` 18+ 条避坑清单——图型/配色/误差是否踩坑
2. **形式层**：`tools/figure/references/quality/publication_checklist.md` 形式合规（尺寸、DPI、字号、误差交代）
3. **视觉层**：
   - **Python**：`tools/figure/scripts/visual_qa.render_preview(fig, 'figs/_preview.png')` 渲预览，`tools/figure/scripts/visual_qa.audit_layout(fig)` 程序抓缺字/裁切/重叠
   - **MATLAB**：用 `export_publication_figure()` 导出 PNG 后人工检查
   - 用 Read 工具读 PNG，对照 `tools/figure/references/quality/visual_review.md` 的 8 项清单核对
   - 发现问题 → 回改 → 重渲 → 再读，最多 3 轮

### 第 8 步：导出

**Python**：

```python
import sys, os
sys.path.insert(0, os.path.join(SKILL_ROOT, 'tools', 'figure', 'scripts'))
from export_figure import export_figure
export_figure(
    fig, basename='figs/fig1',
    formats=['pdf', 'svg', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,
)
```

**MATLAB**：使用 `export_publication_figure(fig, 'figs/fig1', 'png', 300)` 或 `export_publication_figure(fig, 'figs/fig1', 'svg')`。

数学建模场景（两种语言均适用）：同时输出 SVG 与至少 300 DPI PNG。

### 第 9 步：文件审计

两个脚本职责不同，按顺序执行：

```bash
# 1. 编程手自检：文件格式/DPI/字体合规（每张图都过）
python "<SKILL_ROOT>/tools/figure/scripts/check_figure.py" "<PROJECT_ROOT>/figures" --strict

# 2. 数学建模 P2 门禁：三类图数量 + 子问题覆盖（终检时由质检 Subagent 执行）
python "<SKILL_ROOT>/references/roles/编程手/scripts/figure_audit.py" "<PROJECT_ROOT>/figures" --questions q1 q2 ... qN --strict
```

- `check_figure.py`：检查单张图的格式合规性（DPI、字体、尺寸、矢量格式），编程手每次导出后自检用。
- `figure_audit.py`：检查三类图数量是否达标、子问题是否全覆盖，P2 编程终检时由独立质检 Subagent 执行。

## 主动拦截（顾问职责）

发现用户需求触发以下错误时，**先说明再给替代方案，不要默默照做**。完整清单见
`tools/figure/references/design/viz_pitfalls.md`。

| 错误 | 后果 | 替代方案 |
|---|---|---|
| n<10/组 还想画均值柱 | 掩盖分布、掩盖 n | 箱线 + stripplot |
| 双 Y 轴显示无关变量 | 视觉假相关 | 拆成上下子图共享 x |
| 用饼图展示占比 | 人眼判角度差长度 3 倍 | 横向柱状（按值排序） |
| 3D 柱 / 3D 饼 | 视角扭曲数值 | 2D 柱、热力图 |
| 比例图 Y 轴不从 0 起 | 误导小差异 | 从 0 起或用 log |
| x 是分类却用折线连均值 | 暗示假连续 | 散点/点图/柱状 |
| rainbow / jet 色图 | 感知不均匀 | viridis / magma / RdBu_r |

尊重用户最终决定，但**留下明确的劝阻记录**。

## 参考文档

`tools/figure/references/` 下文档——**按需读，不要一次全读**：

### 选图与决策

| 文档 | 何时读 |
|---|---|
| `chart-types/chart_selection.md` | **每次选图必读**——决策框架、不同论点→不同图 |
| `guides/figure_contract.md` | 多面板图的契约工作流——核心结论→证据链→面板映射→审稿人风险 |

### 配方与模板

| 文档 | 何时读 |
|---|---|
| `api-templates/plot_recipes.md` | 各类图完整配方（含数学建模专用模式） |
| `guides/tutorials.md` | 端到端可运行教程——分组柱状/收敛曲线/热力图/森林图 |
| `api-templates/api.md` | 可复用辅助函数（make_grouped_bar/make_trend/make_heatmap 等） |
| `api-templates/template_catalog.md` | CSV 驱动模板——ROC/热力图/收敛曲线 |

### 自检与合规

| 文档 | 何时读 |
|---|---|
| `design/viz_pitfalls.md` | 自检前必读——18+ 条避坑清单 |
| `quality/qa_contract.md` | 交付前 QA 契约——统计图注最小模板 |
| `quality/publication_checklist.md` | 投稿前最后过形式合规清单 |
| `quality/visual_review.md` | 出图后视觉自检——AI 读图 8 项清单 |

### 设计与布局

| 文档 | 何时读 |
|---|---|
| `design/design_theory.md` | 配色/字体/布局/导出理论 |
| `guides/nature_2026_observations.md` | Nature 页面布局原型——示意图主导/非对称/密集分类 |
| `chart-types/chart_types.md` | 雷达/3D/散点等高级图型 |
| `design/common_patterns.md` | hero panel 等布局模式 |
| `guides/figure_legend_conventions.md` | 图注写作规范——结构/时态/自足/进阶 |

### 数据与工具

| 文档 | 何时读 |
|---|---|
| `guides/data_profiling.md` | 读不懂 `profile_data.py` 输出 |
| `quality/journal_specs.md` | 不确定目标期刊的栏宽/字号/DPI/字体 |
| `guides/asset_adaptation.md` | 复用模板时的数据映射规则 |

## 依赖

```
matplotlib>=3.7
seaborn>=0.13
plotly>=5.18
pandas>=2.0
numpy>=1.24
scipy>=1.10
Pillow>=10.0
SciencePlots>=2.1      # 可选
pypdf>=4.0             # 可选；字体嵌入检查
kaleido>=0.2.1         # 可选；plotly 导出
```

可选依赖缺失时优雅降级并提示。

## 核心原则

1. **按最终尺寸出图，不二次缩放**——figsize 直接设论文实际尺寸
2. **矢量优先**——折线/柱状/散点/热力/误差棒 → PDF/SVG，不用 JPEG
3. **配色对色盲友好**——默认 colorblind 色板 + 冗余编码 + 灰度预览
4. **字号可读**——正文标签和刻度数字 7-9 pt，最小 ≥ 6 pt
5. **误差必有交代**——图注必须写清误差类型、样本量 n、检验方法、显著性符号定义
6. **图型多样**——同一道题的全部图应覆盖 ≥ 3 种不同图型（如折线、柱状、散点、热力图、箱线、直方图、雷达图等），避免全部是柱状图或全部是折线图；每个面板必须回答一个唯一的问题，不得用不同图表形式重复展示相同数据（详见 `design_theory.md` §11 反冗余清单）

## 何时加载

| 情形 | 读取 |
|---|---|
| 画图 | 本文件 `tools/figure/SKILL.md` |
| 不确定用什么图 | `tools/figure/references/chart-types/chart_selection.md` |
| 需要图表函数 | `tools/figure/references/api-templates/plot_recipes.md` |
| 交付前 | `tools/figure/references/quality/publication_checklist.md` |
| MATLAB 出版绘图 | `references/roles/编程手/scripts/apply_publication_style.m` + `export_publication_figure.m` |
