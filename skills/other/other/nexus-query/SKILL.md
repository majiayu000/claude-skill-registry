---
name: nexus-query
description: "Precise, instant code structure queries for active development — answer 'who depends on this interface before I refactor it', 'how many modules break if I change this', 'what is the real impact radius of this feature change', 'which module is the true high-coupling hotspot in this legacy codebase'. Essential before any interface change, continuous refactoring task, sprint work estimation, or when navigating unfamiliar or large legacy codebases. Requires Python 3.10+ and shell. Use nexus-mapper instead when building a full .nexus-map/ knowledge base."
---

# nexus-query — 代码结构精准查询


## 何时调用

| 场景 | 调用 |
|------|:----:|
| 「这个文件有哪些类/方法，依赖什么」 | 是 |
| 「改这个接口/模块，哪些文件受影响」 | 是 |
| 「这个改动的影响半径是多大」 | 是 |
| 「项目里谁是真正的核心依赖节点」 | 是 |
| 「整个项目大概分哪几块」 | 是 |
| 用户希望生成完整的 `.nexus-map/` 知识库 | 否 → 改用 nexus-mapper |
| 运行环境无 shell 执行能力 | 否 |
| 宿主机无本地 Python 3.10+ | 否 |

---

## 前提：确保 ast_nodes.json 可用

```
进入查询前 → 检查是否有 ast_nodes.json
├── 有（.nexus-map/raw/ast_nodes.json 或用户指定路径）→ 直接查询
└── 没有 → 运行 extract_ast.py 生成 → 再查询
```

```bash
# 默认路径（和 nexus-mapper 的 .nexus-map/ 兼容，可互通）
AST_JSON="$repo_path/.nexus-map/raw/ast_nodes.json"
GIT_JSON="$repo_path/.nexus-map/raw/git_stats.json"    # 可选

# 若 ast_nodes.json 不存在，先创建目录再生成（约数秒）
mkdir -p "$repo_path/.nexus-map/raw"
python $SKILL_DIR/scripts/extract_ast.py $repo_path > $AST_JSON

# 若需要 git 风险数据（可选，仅在存在 .git 时）
python $SKILL_DIR/scripts/git_detective.py $repo_path --days 90 > $GIT_JSON
```

> `$SKILL_DIR` 为本 Skill 的安装路径（`.agent/skills/nexus-query` 或独立 repo 路径）。

**依赖安装（首次使用）**：
```bash
pip install -r $SKILL_DIR/scripts/requirements.txt
```

---

## 五个查询模式

```bash
# 文件骨架：类、方法、行号、import 清单
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --file <path>
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --file <path> --git-stats $GIT_JSON

# 反向依赖：谁 import 了这个模块（区分源码文件和测试文件）
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --who-imports <module_or_path>

# 影响半径：上游依赖 + 下游被依赖（X upstream, Y downstream）
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --impact <path>
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --impact <path> --git-stats $GIT_JSON

# 全仓库核心节点：按扇入（被引用最多）和扇出（引用最多）排序
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --hub-analysis [--top N]

# 按顶层目录聚合结构摘要
python $SKILL_DIR/scripts/query_graph.py $AST_JSON --summary
```

### 各模式核心价值

| 模式 | 一句话价值 | 典型触发时机 |
|------|-----------|------------|
| `--file` | 不读源码也能掌握文件骨架，精确到行号 | 接手大型模块前；Bug 调查缩小读取区间 |
| `--who-imports` | 改接口前的"炸弹清单"——列出所有调用方 | 删函数/改签名/重命名类之前，必须跑 |
| `--impact` | `0 upstream, 24 downstream` 一眼看清改动范围 | Sprint 估时；评估修改是局部手术还是全局手术 |
| `--hub-analysis` | 找出真正的高耦合核心，不靠目录名猜 | 架构评审；技术债优先级排序 |
| `--summary` | 5 秒建立全局分层认知，比 README 更客观 | 初次接触项目；识别循环依赖风险区域 |

---

## 场景速查

| 你此刻的问题 | 用哪个 |
|-------------|--------|
| 这个文件有哪些类/方法，各在哪几行 | `--file` |
| 改这个接口/删函数，哪些文件跟着改 | `--who-imports` |
| 这个改动最终影响多少模块 | `--impact` |
| 这个改动风险有多高（加 git 热度） | `--impact --git-stats` |
| 项目里谁是真正的高耦合中心 | `--hub-analysis` |
| 整个项目的模块分布和层级 | `--summary` |
| 连续重构，改完一处要看影响链 | `--who-imports` → `--impact` |
| 估算技术债改造的工作量 | `--hub-analysis` → `--impact` |

---

## 执行守则

**守则1: 先骨架再查询**
使用 `--impact` 或 `--who-imports` 分析某个模块前，建议先用 `--file` 读取其骨架，理解职责和现有 import，避免对查询结果产生误判。

**守则2: git-stats 是加分项，不是硬阻塞**
没有 `.git` 或 git 历史不足时，跳过 `git_detective.py`，只用 AST 数据查询。

**守则3: 路径匹配灵活但要验证**
支持路径片段匹配（如 `vision.py` 可匹配 `src/core/vision.py`）。结果返回 `[NOT FOUND]` 时，先用 `--summary` 确认仓库中存在的模块路径格式，再重新查询。

**守则4: 结果直接呈现，让数字说话**
`--impact` 返回的 `X upstream, Y downstream` 是客观数字，直接告知用户，不用「可能影响较大」这类模糊词替代。
