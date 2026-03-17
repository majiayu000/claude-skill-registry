---
name: Evolve-Skill
description: 核心进化技能。在开发结束时调用，自动分析对话历史，将“项目进化资产”沉淀到 EVOLVE.md，并将平台特有的 AI 行为教训写入 CLAUDE.md / GEMINI.md / AGENTS.md / CURSOR.md，实现可审计、可复用的持续进化。触发词："总结经验"、"进化"、"evolve"、"复盘"、"summarize lessons"、"retrospective"、"postmortem"。不适用于仅完成简单查询、单文件小改动或未产生可沉淀资产的场景。
---

# Evolve-Skill

此 Skill 面向**本地项目开发**的长期积累：在任务结束后复盘，把隐性经验固化为“可执行的规则 + 可检索的事件记录 + 可维护的运行手册片段”，并对不同 AI 平台做最小必要的行为矫正。

## 产出文件结构

```
<project-root>/
├── EVOLVE.md                          # 进化主文档（唯一真理源）
├── EVOLVE.local.md                    # 本地私密文件（gitignore，可选）
├── CLAUDE.md / GEMINI.md / AGENTS.md  # 平台配置文件（仅平台特有教训）
└── evolve/
    ├── audit.csv                      # 审计数据（经验指标追踪）
    ├── history/                       # 事件记录（分文件）
    │   └── YYYY-MM-DD-<topic>.md
    ├── runbooks/                      # 操作手册（分文件）
    │   └── YYYY-MM-DD-<topic>.md
    ├── rules/                         # 规则详细内容（分文件，主沉淀对象）
    │   └── <RULE_ID>.md
    ├── archived-rules.md              # 已归档规则（用户确认过时后迁入）
    └── changelog-archive.md           # Changelog 归档（超 30 条时迁移）
```


## 目标产物（单一真理源）

### 1) EVOLVE.md（进化主文档：唯一真理源）
EVOLVE.md 承载三类内容（强烈建议按固定结构维护）：
1. **TL;DR（常用入口）**：最常用命令/常见排障/关键注意事项（不含敏感值）
2. **Runbooks（按任务的操作手册）**：部署/升级/迁移/排障等可执行流程
3. **Rules（宪法级规则）**：短而硬、可执行、可验收
4. **History（事件记录索引）**：只保留摘要与链接，避免 EVOLVE.md 无限制膨胀
5. **Changelog（变更注记）**：记录每次进化新增/修改了哪些规则/手册条目


### 2) 平台配置文件（仅平台特有）
- Claude：`CLAUDE.md`
- Gemini：`GEMINI.md`
- Codex：`AGENTS.md`
- Cursor：`CURSOR.md`
- 其他平台：`<PLATFORM>.md`

这些文件只写入**平台特有**的偏好/坑位/限制，不写通用规则（通用只在 EVOLVE.md）。
平台文件中的自动同步内容由 `audit_sync.py sync` / `sync_platform` 维护，使用 `<!-- EVOLVE_SKILL:AUTO_SYNC:BEGIN ... -->` 标记块更新，不覆盖手写内容。

---

## 工作流程

### Step 1：读取上下文（扫描文件）
在工作区根目录读取（如存在）：
- `EVOLVE.md`（主目标文件）
- `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` / `CURSOR.md` / 其他（按照平台身份选择）
- （可选参考）`README.md`（仅用于了解项目介绍与目录结构，不写入）
- （可选参考）`evolve/runbooks/*`、`evolve/history/*`、`evolve/rules/*`

**首次初始化**：若 `EVOLVE.md` 不存在，请参阅 [references/project-init.md](references/project-init.md) 完成项目进化资产的完整初始化。

### Step 2：经验审计与打分（执行 audit_sync.py）
在提取新经验前，必须先对已有经验进行审计打分，这有助于了解当前已有哪些规则，避免重复提取：
1. 运行 `scopes` 查看可用领域。
2. 运行 `filter` 筛选与本次任务相关的条目；若本次要复盘平台教训（S-xxx），必须加 `--platform <platform-name>`（如 `claude|gemini|codex|cursor`，也可自定义）以避免跨平台污染。
3. 运行 `score` 对本次复盘中遵守或违反的已有规则进行打分（+hit/+vio/+err）；若使用了平台过滤，`score` 也必须带同样的 `--platform`。
4. 运行 `report` 查看审计结果与带编号的 `EVOLVE SUGGESTIONS`。
5. Agent 基于审计结果决定最终写入条目，并运行 `select` 回写 `evolve_slot`（如：`python <skill-root>/scripts/audit_sync.py select "1,3" --project-root .`）。
详细命令参考 [references/audit-system.md](references/audit-system.md)。

### Step 3：深度回顾与分析（双向复盘）
回顾整个对话，提取两类信息：

#### A. 项目进化资产（写入 EVOLVE.md）
提取“未来能复用、能减少返工、能降低风险”的内容，包括但不限于：
- 关键决策与权衡（为什么 A 而不是 B）
- 可复用的操作流程（Runbook）
- 高价值的排障套路（Runbook/Checklist）
- 新增或加固的项目规则（Rules，注意不要与 Step 2 中已有的规则重复）
- 需要纳入“常用入口（TL;DR）”的高频命令/检查点

#### B. AI 行为教训（写入平台配置文件）
仅记录“当前平台/模型/工具链”特有的：
- 工具偏好（例如更可靠的命令/参数用法）
- 已知局限（例如某模型容易误解某类指令）
- 工作方式约束（例如必须先读 EVOLVE.md 再行动）
- 防止重复失误的自我约束（Self rules）

### Step 4：安全与脱敏（强制执行）
在写入任何文档前，执行以下约束：

1) **禁止写入敏感信息到可提交文件**
- 包括：明文 IP、用户名、端口、secret/token、订阅链接、私钥路径、OAuth 凭据等。
- 若对话里出现上述信息，只能写成“占位符 + 指引”，例如：
  - `SSH_HOST=<YOUR_HOST>`、`CLASH_SECRET=<REDACTED>`
  - “真实值请放入 `EVOLVE.local.md`（gitignore）”

2) **建议拆分本地私密文件（不由本 Skill 自动创建也可）**
- `EVOLVE.local.md` / `secrets.local.md`（应加入 .gitignore）
- EVOLVE.md 只保留模板与流程，不保留真实凭据。

### Step 5：执行文档更新与同步
1. **新增内容**：使用 Edit 工具遵循“非破坏性追加”更新 `EVOLVE.md` 及其他文件（保留原文，只在对应章节末尾追加或在索引处更新链接）。
   - *注意：在编写具体内容时，请务必查阅 [references/writing-specs.md](references/writing-specs.md) 获取模板和规范。*
2. **核心同步**：运行 `python <skill-root>/scripts/audit_sync.py sync --project-root .`，一次完成：
   - 审计指标同步到 `EVOLVE.md`（TL;DR + Rules 内联标签）
   - 依据 `evolve_slot` 在 `EVOLVE.md` 的 `## Rules` 下生成/更新 `RULE_SELECTION`
   - 同步 `evolve/rules/*.md` 详细规则内容与 Traceability（history/runbook 链接）
   - 平台文件自动同步（已知平台 + audit.csv 中新增平台 + 配置映射平台）
3. **可选控制**：
   - 仅同步单个平台：`python <skill-root>/scripts/audit_sync.py sync --project-root . --platform <name>`
   - 限制 EVOLVE 同步目标：`python <skill-root>/scripts/audit_sync.py sync --project-root . --evolve-platform <name>`
   - 仅同步平台文件：`python <skill-root>/scripts/audit_sync.py sync_platform --project-root . [--platform <name>]`
   - 临时跳过平台同步：`python <skill-root>/scripts/audit_sync.py sync --project-root . --no-platform-sync`
4. **可选映射配置**：在 `evolve/platform_targets.json` 指定平台到文件路径映射（例如将某个平台映射到自定义文件名/子目录）。
5. **收尾健康检查（建议执行）**：运行 `python <skill-root>/scripts/health_check.py --project-root .`，若存在 FAIL/WARN，在汇报中说明风险与后续处理建议。

---

## 执行原则（硬规则）

1. **Single Source of Truth**：通用规则与沉淀只维护在 EVOLVE.md。
2. **精准分类**：通用 → EVOLVE.md；平台特有 → 对应平台文件。
3. **可审计**：每次进化必须在 EVOLVE.md 的 Changelog 追加一条"变更注记"。
4. **非破坏性编辑**：不重写历史，不大改原文，只追加/合并去重。
5. **安全第一**：敏感信息脱敏；真实凭据只能进入 *.local（gitignore）文件。

---

## 结束反馈（向用户汇报）

完成更新后，简报必须包含：

* 本次已更新的文件列表（例如：EVOLVE.md、evolve/audit.csv、CLAUDE.md）
* EVOLVE.md 新增了哪些内容（Runbook/Rules/History/Changelog）
* 平台文件新增了哪些"Self 教训"（如有）
* 审计指标变更摘要（哪些规则 +hit/+vio/+err，哪些标记为待审查）
* TL;DR 是否因审计数据发生了变更（新增强调/移除淡化）
* 是否有晋升建议（如有，列出待确认的条目）
* 是否发现并避免写入敏感信息（如有，说明已做脱敏/占位符）
