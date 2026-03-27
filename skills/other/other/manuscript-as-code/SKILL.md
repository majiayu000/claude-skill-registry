---
name: manuscript-as-code
description: "Treat manuscripts as software: version control, reproducible builds, figure pipelines, CI, and structured repo layout. Helps teams avoid 'final_v7' chaos and ensures submission-ready artifacts."
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Manuscript as Code（论文工程化）

## 目标

把“写论文”升级成“交付可复现的出版工程”：
- 结构清晰：任何人进仓库都知道哪里改正文、哪里改图、哪里改引用
- 可复现：一条命令能构建 PDF/HTML；CI 自动验证
- 可审计：每张图/每个结果都有来源（代码/数据/参数）

适用：
- 多人协作写作（导师/合作者/跨机构）
- 反复投稿/返修（需要明确改动轨迹）
- 图表多、实验多、容易“找不到版本”的项目

---

## 推荐仓库结构（最小可行）

见 `templates/repo-structure.md`。核心思想：
- `manuscript/`：只放正文与引用（source-of-truth）
- `figures/`：每张图一个目录（source + out）
- `build/`：所有生成物（可删除，可再生）
- `submission/` 与 `revision/`：投稿与返修阶段产物

---

## 元规则（工程化的关键）

### 1) 生成物与源文件分离

- 源：`figures/fig-02/src/plot.py`
- 产物：`figures/fig-02/out/fig-02.pdf`
- 禁止把产物当源文件编辑（比如在 PDF 上涂改）

### 2) 每张图都要能“重生成”

最少要求：
- 一条命令 + 固定参数能导出最终图（PDF/TIFF）
- 记录依赖版本与随机种子（如果有）

### 3) 把“投稿约束”写成配置

推荐维护：
- `submission/submission-manifest.yml`（统一记录规格与完成度）

---

## 案例（推荐学习）

- Manubot：`manubot/rootstock`（论文的 CI/协作写作范式）
- Deep review：`greenelab/deep-review`（评审/返修视角）

