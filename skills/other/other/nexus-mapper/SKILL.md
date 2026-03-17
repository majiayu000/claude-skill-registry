---
name: nexus-mapper
description: "Generate a persistent .nexus-map/ knowledge base that lets any AI session instantly understand a codebase's architecture, systems, dependencies, and change hotspots. Use when starting work on an unfamiliar repository, onboarding with AI-assisted context, preparing for a major refactoring initiative, or enabling reliable cold-start AI sessions across a team. Produces INDEX.md, systems.md, concept_model.json, git_forensics.md and more. Requires shell execution and Python 3.10+. For ad-hoc file queries or instant impact analysis during active development, use nexus-query instead."
---

# nexus-mapper — AI 项目探测协议

本 Skill 指导 AI Agent 使用 **PROBE 五阶段协议**，对任意本地 Git 仓库执行系统性探测，产出 `.nexus-map/` 分层知识库。

---

## 何时调用 / 何时不调用

| 场景                                                                | 调用  |
| ------------------------------------------------------------------- | :---: |
| 用户提供本地 repo 路径，希望 AI 理解其架构                          |  是   |
| 需要生成 `.nexus-map/INDEX.md` 供后续 AI 会话冷启动                 |  是   |
| 用户说「帮我分析项目」「建立项目知识库」「让 AI 了解这个仓库」      |  是   |
| 运行环境无 shell 执行能力（纯 API 调用模式，无 `run_command` 工具） |  否   |
| 宿主机无本地 Python 3.10+                                           |  否   |
| 目标仓库无任何已知语言源文件（`.py/.ts/.java/.go/.rs/.cpp` 等均无） |  否   |
| 用户只想查询某个特定文件/函数 → 直接用 `view_file` / `grep_search`  |  否   |

---

## 前提检查

缺失项要显式告知用户；需要降级等时及时提醒用户，经过同意才能继续。

| 前提              | 检查方式                                |
| ----------------- | --------------------------------------- |
| 目标路径存在      | `$repo_path` 可访问                     |
| Python 3.10+      | `python --version` >= 3.10              |
| 脚本依赖已安装    | `python -c "import tree_sitter"` 无报错 |
| 有 shell 执行能力 | Agent 环境支持 `run_command` 工具调用   |

`git` 历史是加分项，不是硬阻塞项。没有 `.git` 或历史过少时，跳过热点分析，并在输出中明确记录这是一次降级探测。

---

## 输入契约

```
repo_path: 目标仓库的本地绝对路径（必填）
```

**语言支持**：自动按文件扩展名 dispatch，语言配置（扩展名映射 + Tree-sitter 查询）存储在 `scripts/languages.json`。当前已接入 Python/JavaScript/TypeScript/TSX/Bash/Java/Go/Rust/C#/C/C++/Kotlin/Ruby/Swift/Scala/PHP/Lua/Elixir/GDScript/Dart/Haskell/Clojure/SQL/Proto/Solidity/Vue/Svelte/R/Perl 等 30+ 语言。

**非标准语言**：若仓库含有内置未支持的语言，通过命令行参数动态补充（详见 `references/05-language-customization.md`）：
- `--add-extension .templ=templ` 添加新文件扩展名映射
- `--add-query templ struct "(component_declaration ...)"` 添加结构查询
- `--language-config <JSON_FILE>` 复杂配置时使用 JSON 文件

---

## 输出格式

执行完成后，目标仓库根目录下将产出：

```text
.nexus-map/
├── INDEX.md                    ← AI 冷启动主入口（< 2000 tokens）
├── arch/
│   ├── systems.md              ← 系统边界 + 代码位置
│   ├── dependencies.md         ← Mermaid 依赖图 + 时序图
│   └── test_coverage.md        ← 静态测试面：测试文件、覆盖到的核心模块、证据缺口
├── concepts/
│   ├── concept_model.json      ← Schema V1 机器可读图谱
│   └── domains.md              ← 核心领域概念说明
├── hotspots/
│   └── git_forensics.md        ← Git 热点 + 耦合对分析
└── raw/
    ├── ast_nodes.json          ← Tree-sitter 解析原始数据
    ├── git_stats.json          ← Git 热点与耦合数据
    └── file_tree.txt           ← 过滤后的文件树
```

所有生成的 Markdown 文件必须带一个简短头部，至少包含：`generated_by`、`verified_at`、`provenance`。

`concept_model.json` 的人类可读名称字段统一使用 `label`，不要添加 `title`。

如果 PROFILE 阶段发现语言覆盖降级或人工推断，`provenance` 必须明确标注。

---

## PROBE 阶段门控

> [!IMPORTANT]
> **进入每个阶段前必须先读对应 reference，不得跳过。**
> 各阶段详细步骤、完成检查清单与边界场景处理均在 reference 中定义。

```
[Skill 激活时]     → read references/probe-protocol.md  （阶段步骤蓝图，含边界场景与三维度质疑框架）
[EMIT 前]          → read references/output-schema.md    （Schema 校验规范）
[非标准语言时]     → read references/language-customization.md（按需，非门控）
```

---

## 执行守则

### 守则1: OBJECT 拒绝形式主义

OBJECT 的存在意义是打破 REASON 的幸存者偏差。大量工程事实隐藏在目录命名和 git 热点背后，第一直觉几乎总是错的。

不合格质疑（禁止提交）：
```
Q1: 我对系统结构的把握还不够扎实
Q2: xxx 目录的职责暂时没有直接证据
```
问题不在措辞，而在于没有证据线索，也无法在 BENCHMARK 阶段验证。

合格质疑格式：
```
Q1: git_stats 显示 tasks/analysis_tasks.py 变更 21 次（high risk），
    但 HYPOTHESIS 认为编排入口是 evolution/detective_loop.py。
    矛盾：若 detective_loop 是入口，为何 analysis_tasks 热度更高？
    证据线索: git_stats.json hotspots[0].path
    验证计划: view tasks/analysis_tasks.py 的 class 定义 + import 树
```

---

### 守则2: implemented 节点必须有真实 code_path

> [!IMPORTANT]
> 写入 `concept_model.json` 前，必须先区分节点是 `implemented`、`planned` 还是 `inferred`。
> 只有 `implemented` 节点允许写入 `code_path`，且必须亲手验证存在。

```bash
# BENCHMARK 阶段验证方式
ls $repo_path/src/nexus/application/weaving/   # 目录存在 → 节点有效
ls $repo_path/src/nexus/application/nonexist/  # [!ERROR] → 修正或删除此节点
```

对于 `planned` 或 `inferred` 节点，使用：

```json
{
  "implementation_status": "planned",
  "code_path": null,
  "evidence_path": "docs/architecture.md",
  "evidence_gap": "仓库中未发现 src/agents/monarch/，仅在设计文档中出现"
}
```

禁止：用勉强相关的文件冒充 `code_path`、把状态塞进路径字段（如 `code_path: "PLANNED"`）。

---

### 守则3: EMIT 原子性

先全部写入 `.nexus-map/.tmp/`，全部成功后整体移动到正式目录，删除 `.tmp/`。
目的：中途失败不留半成品。下次执行检测到 `.tmp/` 存在 → 清理后重新生成。

幂等性规则：

| 状态                                 | 处理方式                                   |
| ------------------------------------ | ------------------------------------------ |
| `.nexus-map/` 不存在                 | 直接继续                                   |
| `.nexus-map/` 存在且 `INDEX.md` 有效 | 询问用户：「是否覆盖？[y/n]」              |
| `.nexus-map/` 存在但文件不完整       | 「检测到未完成分析，将重新生成」，直接继续 |

---

### 守则4: INDEX.md 的角色——冷启动路由器，而非静态字典

`INDEX.md` 的读者是**从未见过这个仓库的 AI**。两个硬约束：
- **< 2000 tokens** — 超过就重写，不是截断
- **结论必须具体** — 证据不足时明确写出 `evidence gap` 或 `unknown`，并说明缺了什么证据

写完后执行 token 估算：行数 × 平均 30 tokens/行 = 粗估值。

**INDEX.md 必须包含的强制路由块（Hard-Trigger Block）**——生成时把这段结构写入文件末尾：

```markdown
## [操作指南] 强制执行步骤

> 本节是对所有读取本文件的 AI 发出的硬性操作指令，不是建议。

### 步骤1 — 必须先读完以下所有文件（顺序不限）

读完本文件后，在执行任何任务之前，必须依次 read 以下文件完整内容：

- `.nexus-map/arch/systems.md` — 系统边界与代码位置
- `.nexus-map/arch/dependencies.md` — 系统间依赖关系与 Mermaid 图
- `.nexus-map/arch/test_coverage.md` — 测试面与证据缺口
- `.nexus-map/hotspots/git_forensics.md` — Git 热点与耦合风险
- `.nexus-map/concepts/domains.md` — 核心领域概念

> 这些文件均为高密度摘要，总量通常 < 5000 tokens，是必要的上下文成本。
> 不得以"任务简单"或"只改一个文件"为由跳过。

### 步骤2 — 按任务类型追加操作（步骤1 完成后执行）

- 若任务涉及**接口修改、新增跨模块调用、删除/重命名公共函数**：
  → 必须运行 `query_graph.py --impact <目标文件>` 确认影响半径后再写代码。
- 若任务需要**判断某文件被谁引用**：
  → 运行 `query_graph.py --who-imports <模块名>`。
- 若仓库结构已发生重大变化（新增系统、重构模块边界）：
  → 任务完成后评估是否需要重新运行 nexus-mapper 更新知识库。
```

---

### 守则5: 最小执行面与敏感信息保护

> [!IMPORTANT]
> 默认只运行本 Skill 自带脚本和必要的只读检查。不要因为"想更懂仓库"就执行目标仓库里的构建脚本、测试脚本或自定义命令。

- 默认允许：`extract_ast.py`、`git_detective.py`、目录遍历、文本搜索、只读文件查看
- 默认禁止：执行目标仓库的 `npm install`、`pnpm dev`、`python main.py`、`docker compose up` 等，除非用户明确要求
- 遇到 `.env`、密钥文件、凭据配置时：只记录其存在和用途，不抄出具体值

---

### 守则6: 降级与人工推断必须显式可见

> [!IMPORTANT]
> 如果 AST 覆盖不完整，或者某部分来自人工阅读而非脚本产出，必须在最终文件中显式标注 provenance。

- `dependencies.md` 中凡是非 AST 直接支持的依赖关系，必须标注 `inferred from file tree/manual inspection`
- `domains.md`、`systems.md`、`INDEX.md` 如果涉及未支持语言区域，必须说明 `unsupported language downgrade`
- 若写入进度快照、Sprint 状态，必须附 `verified_at`，避免过期信息伪装成当前事实

---

## 不确定性表达规范

避免只写：待确认 · 可能是 · 疑似 · 也许 · 待定 · 暂不清楚 · pending · maybe · possibly · TBD

如果证据不足，按以下格式写：
- `unknown: 未发现直接证据表明 api/ 是主入口，当前仅能确认 cli.py 被 README 引用`
- `evidence gap: 仓库没有 git 历史，因此 hotspots 部分跳过`

允许诚实地写不确定，但必须解释不确定来自哪一条缺失证据。

---

## 脚本工具链

```bash
# 设置 SKILL_DIR（根据实际安装路径）
# 场景 A: 作为 .agent/skills 安装
SKILL_DIR=".agent/skills/nexus-mapper"
# 场景 B: 独立 repo（开发/调试时）
SKILL_DIR="/path/to/nexus-mapper"

# PROFILE 阶段 — 基础用法
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --file-tree-out <repo_path>/.nexus-map/raw/file_tree.txt \
  > <repo_path>/.nexus-map/raw/ast_nodes.json

# 补充非标准语言支持
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --add-extension .templ=templ \
  --add-query templ struct "(component_declaration name: (identifier) @class.name) @class.def" \
  > <repo_path>/.nexus-map/raw/ast_nodes.json

# 复杂配置：使用 JSON 配置文件
python $SKILL_DIR/scripts/extract_ast.py <repo_path> [--max-nodes 500] \
  --language-config /custom/path/to/language-config.json \
  > <repo_path>/.nexus-map/raw/ast_nodes.json
```

**依赖安装（首次使用）**：
```bash
pip install -r $SKILL_DIR/scripts/requirements.txt
```

---

## 持久化记忆规则（写入宿主 AGENTS.md）

建议把以下规则写入仓库的 `AGENTS.md`、`CLAUDE.md` 或同类持久记忆文件，使知识库在长期对话中保持活跃：

```md
如果仓库中存在 .nexus-map/INDEX.md，先阅读它，然后在执行任务前读完其路由块中列出的所有文件。

如果 .nexus-map/ 不存在，且当前任务涉及跨模块修改或接口变更，先向用户提议运行 nexus-mapper；若用户需立即开始，至少先运行 query_graph.py --summary 建立结构感知。

当任务改变了项目的结构认知（系统边界、入口、依赖关系），在交付前评估是否需要更新 .nexus-map。
```

---

## 按需查询工具（PROBE 辅助）

`scripts/query_graph.py` 读取 `raw/ast_nodes.json`，零额外依赖（纯 Python 标准库）。

```bash
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --file <path>         # 文件骨架
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --who-imports <mod>   # 反向依赖
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --impact <path>       # 影响半径
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --impact <path> --git-stats <git_stats.json>
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --hub-analysis        # 核心节点
python $SKILL_DIR/scripts/query_graph.py <ast_nodes.json> --summary             # 目录聚合
```

| 阶段   | 推荐查询               | 用途                                         |
| ------ | ---------------------- | -------------------------------------------- |
| REASON | `--hub-analysis`       | 数据验证核心系统假说，不靠目录名猜测         |
| OBJECT | `--impact --git-stats` | 验证边界假设，查看真实上下游依赖             |
| EMIT   | `--summary`, `--file`  | 生成 systems.md / dependencies.md 的数据支撑 |

各查询模式的核心价值：`--hub-analysis` 用于 REASON 期验证架构假说；`--impact --git-stats` 用于 OBJECT 期量化边界风险；`--summary` 与 `--file` 用于 EMIT 期生成精确数据支撑。
