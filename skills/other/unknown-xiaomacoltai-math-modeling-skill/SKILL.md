---
name: 编程手
description: 数学建模的 Python 或 MATLAB 实现、运行、表格输出、可视化和复现阶段。
---

# 编程手

## 路径

- `ROLE_ROOT`：本文件所在目录。
- `SKILL_ROOT`：`ROLE_ROOT/../../..`，只读。
- `PROJECT_ROOT`：用户项目目录，所有代码、结果和图只写这里。

## 输入

优先读取 `PROJECT_ROOT/题目分析报告.md`、`PROJECT_ROOT/术语表格.md` 和题目附件。若用户只执行本阶段，可从用户提供的模型说明开始；若说明不足以实现，先反馈缺项。

## 固定产物

- Python `.py`、MATLAB `.m`，或用户要求的两套实现。
- `results/` 中的运行结果表格和必要文本结果。
- `figures/` 中的原始数据图、模型运行过程图、模型最终结果图，每类至少 3 张逻辑候选图、合计至少 9 张，并覆盖全部子问题：每个子问题在三类中各至少 1 张。文件名使用 `raw_q1_*`、`process_q1_*`、`result_q1_*` 等格式，不设上限；同一图的 SVG、PNG 和灰度预览只计 1 张。允许继续多生成，不机械删除有效备选视角。
- `results/复现清单.json`。

## 执行顺序

1. 按用户要求或现有项目语言选择 Python/MATLAB；没有偏好时按模型依赖和现有环境选择并说明。
2. 按选中的模型功能动态检查依赖，禁止一次性要求全部包：
   - Python：`python scripts/check_env.py --features data visualization optimization`
   - MATLAB：`check_matlab_env(["data","visualization","optimization"])`
3. 实现数据读取、预处理和核心求解链，用真实输入或结构等价小实例跑通从 `PROJECT_ROOT` 执行的最小命令；任何结论必须来自真实输出。
4. 在全量计算、参数扫描和正式出图前，派发独立质检 Subagent 执行 `P1` 最小可运行结果门禁；实现问题由编程手修正，模型合同问题携证据返回建模手。未返回 `PASS` 不得继续扩展。
5. 从题目分析报告提取全部子问题并规范为 `q1…qN`。绘图前加载 `tools/figure/SKILL.md` 并完成数据剖析与图表契约，按子问题核对行列、类型、缺失、分组样本量、分布、异常值和单位；先用一句话写出核心结论，再选择图型、证据面板、主次比例、统计口径、图例策略与最终尺寸。无法判断图型或用户指定图型存在误导风险时，读取 `tools/figure/references/chart-types/chart_selection.md`。
6. 将 `scripts/plot_style.py` 或 MATLAB 的三个出版绘图工具复制到 `PROJECT_ROOT/utils/` 后使用。按 `tools/figure/SKILL.md` 的 Nature/SCI 视觉论证流程生成三类候选图，每类至少 3 张、合计至少 9 张，且每个子问题在三类中各至少 1 张：不把不同重要性的面板机械等分，不用长标题、密集逐点标记、装饰性纹理或面板内重复图例堆成仪表盘；统计标注必须由代码计算，官方模板要求优先于内置基线。
7. 所有正式图必须经 `tools/figure/scripts/export_figure.py` 或 `export_publication_figure()` 的布局与设计门禁，同时输出 SVG 与至少 300 DPI PNG；再运行 `python "<SKILL_ROOT>/references/roles/编程手/scripts/figure_audit.py" "<PROJECT_ROOT>/figures" --questions q1 q2 ... qN --strict`，实际打开彩色 PNG 和灰度预览，在论文预计尺寸下检查视觉层级、缺字、裁切、遮挡、颜色、尺度和面板一致性。有问题则改代码、重跑、重审，不能关闭门禁后继续，也不能直接修改位图。
8. 生成复现清单：`python scripts/repro_manifest.py --project-root <PROJECT_ROOT> ...`。
9. 按 `references/质检清单.md` 完成作者自检，再派发独立质检 Subagent 执行 `P2` 编程终检；未返回 `PASS` 不得进入论文阶段或宣称编程交付完成。

## 阶段内独立门禁

- `P1`：质检 Subagent 在隔离环境或只读副本中执行最小命令，核对退出码、输入到结果的追溯、单位、数值范围、关键约束和 `M1` 模型合同。它是纵向切片，不要求完整图表或最终性能。
- `P2`：代码、结果、每类至少 3 张且覆盖全部子问题的三类图和复现清单冻结后，质检 Subagent 独立运行唯一复现命令并核对输入哈希、种子、关键数值、边界、量纲、各子问题图表语义及文件完整性。机械图审继续使用带全部 `--questions` 的 `figure_audit.py --strict`，Subagent 负责实际读图，检查单图核心结论、主次面板、图例、统计区间和最终尺寸可读性，而不是只确认文件能打开。

两次门禁均按 `../../../references/Subagent调度.md` 返回证据；被审代码、数据或参数发生实质变化时重跑受影响门禁。

## 何时加载

| 情形 | 读取 |
|---|---|
| 开始实现 | `references/工作流程.md` |
| 使用 MATLAB | `references/MATLAB规范.md` |
| 画图 | `tools/figure/SKILL.md` |
| 不确定用什么图，或需审查指定图型 | `tools/figure/references/chart-types/chart_selection.md` |
| 需要图表函数 | `tools/figure/references/api-templates/plot_recipes.md` |
| 需要具体算法 | `../../../references/算法索引.md`，再读取匹配的 `../../../assets/*.md` |
| 处理 Excel | `../../../tools/xlsx/SKILL.md` |
| 交付前 | `references/质检清单.md` |
| 阶段内独立验收 | `../../../references/Subagent调度.md` |

若实际运行证明模型公式、约束或参数定义冲突，停止通过改算法规避问题，把证据反馈给建模手。
