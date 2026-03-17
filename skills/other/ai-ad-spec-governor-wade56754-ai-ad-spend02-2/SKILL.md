---
name: ai-ad-spec-governor
version: "1.2"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-11-28
baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
---

# AI-Ad Spec Governor Skill v1.2

<skill>
<name>ai-ad-spec-governor</name>
<version>1.2</version>
<status>active</status>
<owner>doc-architect / wade</owner>
<last_updated>2025-11-27</last_updated>

<mission>
负责在整个文档体系范围内执行 Spec-Driven 治理和 SoT 对齐，作为规范治理总调度器（Spec Governor），统筹文档审计、修复、验证和 Freeze 合规性检查。
</mission>

---

## 📌 核心定位

**ai-ad-spec-governor** 是 AI_ad_spend02 项目的**元规范总控 Architect**，负责：

1. **规范治理闭环**: 审计 → 修复 → 验证 → 上线判定
2. **SoT 对齐**: 确保所有文档符合 `docs/sot/` 真相源
3. **子 Skill 调度**: 协调现有文档治理 Skill（auditor / fixer / pipeline / orchestrator）
4. **Freeze 合规**: 确保文档变更不违反 ASDD Freeze v1.0 / SoT Freeze v2.6

**职责边界**:
- ✅ **调度协调**: 决定何时调用哪个子 Skill
- ✅ **治理判定**: 决定文档是否可上线
- ✅ **SoT 监督**: 确保所有修改符合 SoT 裁判链
- ❌ **直接修改 SoT**: 不直接修改 `docs/sot/` 文档（仅提建议）
- ❌ **重复造轮子**: 不重新实现已有 Skill 功能

---

## 🎯 WHEN_TO_USE

### 典型使用场景

#### 1. 单文档上线前检查
```
场景：API_DEVELOPMENT_FLOW.md 重写完毕，需要判定是否可上线
调用：mode="single-doc", target="docs/3.dev-guides/API_DEVELOPMENT_FLOW.md"
流程：AUDIT → FIX → VERIFY → 上线判定
```

#### 2. 文档组巡检
```
场景：每季度对 dev-guides 做一次全面巡检
调用：mode="doc-group", scope="dev-guides"
流程：批量 AUDIT → 生成巡检报告 → 批量修复（可选）
```

#### 3. 新 SoT 发布后的对齐检查
```
场景：STATE_MACHINE.md v2.8 发布，需检查所有引用文档是否对齐
调用：mode="sot-alignment-check", changed_sot="STATE_MACHINE.md"
流程：调用 ai-ad-sot-doc-pipeline → 验证下游文档
```

#### 4. Appendix 文档一致性检查
```
场景：修改多个 SoT 后，GLOSSARY / DECISIONS / CHECKLIST 是否需要更新
调用：mode="appendix-sync", changed_files=[...]
流程：检查 Appendix 是否引用了过时的 SoT 内容
```

#### 5. 文档变更影响分析
```
场景：修改 DATA_SCHEMA.md §3.3.1 daily_reports 表，需要找出所有受影响文档
调用：mode="impact-analysis", changed_section="DATA_SCHEMA.md#3.3.1"
流程：搜索所有引用 → 生成影响范围报告
```

### 触发条件

| 触发方式 | 描述 | 示例 |
|---------|------|------|
| **手动调用** | 用户明确请求治理检查 | "请检查 API_DEVELOPMENT_FLOW.md 是否符合规范" |
| **定期巡检** | 每季度/每月自动触发 | Cron Job: 每季度第一天 |
| **SoT 变更** | SoT 文档发布新版本后 | STATE_MACHINE.md v2.8 → v2.7 |
| **PR 审查** | CI/CD 触发（未来） | PR 修改 dev-guides 文档时 |

---

## 🚫 WHEN_NOT_TO_USE

### 不适用场景

#### 1. 纯业务讨论
```
❌ 场景：讨论"日报审核流程是否合理"
原因：这是业务规则设计，不是文档治理
应使用：直接讨论或记录 ADR
```

#### 2. 代码实现细节
```
❌ 场景：优化 DailyReportService.py 性能
原因：代码实现问题，不是文档问题
应使用：代码审查 / 性能分析工具
```

#### 3. 单一字段查询
```
❌ 场景：查询 `conversions_raw` 字段定义
原因：简单查询无需治理流程
应使用：直接查阅 DATA_SCHEMA.md
```

#### 4. 无文档修改的场景
```
❌ 场景：用户只想理解系统架构
原因：无需治理和修复
应使用：直接阅读 MASTER.md / SYSTEM_OVERVIEW.md
```

#### 5. 已有 Skill 可直接解决
```
❌ 场景：单纯审计某个文档的 P0/P1/P2 问题
原因：ai-ad-doc-system-auditor 可直接完成
应使用：直接调用 ai-ad-doc-system-auditor
```

**判定原则**: 如果任务可由单一子 Skill 独立完成，无需调度协调，则不应使用 spec-governor。

---

## 📥 INPUT_CONTRACT

### 输入参数定义

```typescript
interface SpecGovernorInput {
  // ===== 必填参数 =====
  mode: "single-doc" | "doc-group" | "full-scan" | "sot-alignment-check"
        | "appendix-sync" | "impact-analysis";

  // ===== 条件必填 =====
  target?: string;                    // mode=single-doc 时必填，文件路径
  targets?: string[];                 // mode=doc-group 时必填，文件/目录列表
  scope?: "overview" | "sot" | "dev-guides" | "appendix" | "all";
                                      // mode=full-scan 时必填
  changed_sot?: string;               // mode=sot-alignment-check 时必填
  changed_section?: string;           // mode=impact-analysis 时必填
  changed_files?: string[];           // mode=appendix-sync 时必填

  // ===== 可选参数 =====
  strict_level?: "paranoid" | "normal" | "relaxed";
                                      // 默认: "normal"
  allow_auto_fix?: boolean;           // 是否允许自动修复，默认: true
  include_appendix?: boolean;         // 是否检查 Appendix 衔接，默认: true
  dry_run?: boolean;                  // 仅生成报告，不实际修改，默认: false
  output_format?: "markdown" | "json" | "checklist";
                                      // 默认: "markdown"
}
```

---

### 模式详解

#### Mode 1: single-doc (单文档治理)

**输入示例**:
```json
{
  "mode": "single-doc",
  "target": "docs/3.dev-guides/API_DEVELOPMENT_FLOW.md",
  "strict_level": "normal",
  "allow_auto_fix": true,
  "include_appendix": true
}
```

**执行流程**:
1. DISCOVER: 读取目标文档元信息
2. AUDIT: 调用 `ai-ad-doc-system-auditor` 生成 P0/P1/P2 报告
3. FIX: 如果 `allow_auto_fix=true`，调用 `ai-ad-doc-fixer` 修复
4. VERIFY: 再次审计，确认修复效果
5. SUMMARY: 输出上线判定（PASS / BLOCK / WARN）

---

#### Mode 2: doc-group (文档组巡检)

**输入示例**:
```json
{
  "mode": "doc-group",
  "targets": [
    "docs/3.dev-guides/API_DEVELOPMENT_FLOW.md",
    "docs/3.dev-guides/FRONTEND_SPEC.md"
  ],
  "strict_level": "normal",
  "allow_auto_fix": false,
  "dry_run": true
}
```

**执行流程**:
1. DISCOVER: 批量读取文档元信息
2. AUDIT: 对每个文档生成审计报告
3. SUMMARY: 汇总所有问题，生成巡检总报告
4. （可选）FIX: 如果 `allow_auto_fix=true`，批量修复

---

#### Mode 3: full-scan (全面扫描)

**输入示例**:
```json
{
  "mode": "full-scan",
  "scope": "dev-guides",
  "strict_level": "paranoid",
  "include_appendix": true
}
```

**执行流程**:
1. DISCOVER: 扫描 `docs/3.dev-guides/**` 所有文档
2. AUDIT: 批量审计，生成统计报告（总问题数 / 文件数）
3. FREEZE_CHECK: 检查是否有文档违反 Freeze 规则
4. SUMMARY: 生成"健康度报告"（PASS / WARN / FAIL）

---

#### Mode 4: sot-alignment-check (SoT 对齐检查)

**输入示例**:
```json
{
  "mode": "sot-alignment-check",
  "changed_sot": "STATE_MACHINE.md",
  "strict_level": "paranoid"
}
```

**执行流程**:
1. DISCOVER: 搜索所有引用 `STATE_MACHINE.md` 的文档
2. AUDIT: 检查每个文档是否引用了正确的版本号
3. SOT_ALIGN: 调用 `ai-ad-sot-doc-pipeline` 执行对齐
4. VERIFY: 验证对齐结果
5. SUMMARY: 输出受影响文档列表 + 对齐状态

---

#### Mode 5: appendix-sync (Appendix 一致性检查)

**输入示例**:
```json
{
  "mode": "appendix-sync",
  "changed_files": [
    "docs/sot/STATE_MACHINE.md",
    "docs/sot/DATA_SCHEMA.md"
  ],
  "include_appendix": true
}
```

**执行流程**:
1. DISCOVER: 读取 GLOSSARY / DECISIONS / CHECKLIST 内容
2. AUDIT: 检查 Appendix 是否引用了过时的 SoT 内容
3. FIX: 调用 `ai-ad-doc-fixer` 更新 Appendix
4. VERIFY: 验证更新后的一致性
5. SUMMARY: 输出更新列表

---

#### Mode 6: impact-analysis (影响分析)

**输入示例**:
```json
{
  "mode": "impact-analysis",
  "changed_section": "DATA_SCHEMA.md#3.3.1",
  "output_format": "checklist"
}
```

**执行流程**:
1. DISCOVER: 搜索所有引用 `DATA_SCHEMA.md §3.3.1` 的文档
2. AUDIT: 分析每个文档的引用方式（直接引用 / 间接引用）
3. SUMMARY: 生成影响范围清单（需要修改的文档列表）

---

## 🚨 FORBIDDEN_ACTIONS

### 严格禁止的行为

#### 1. 直接修改 SoT 文档
```xml
<forbidden>
  <action>直接编辑 docs/sot/ 下的任何文件</action>
  <reason>SoT 文档是最高真相源，修改必须通过 RFC 流程</reason>
  <correct_action>生成修改建议，提交给 DBA/架构师审核</correct_action>
</forbidden>
```

**示例**:
```markdown
❌ 错误：检测到 STATE_MACHINE.md 缺少某个状态，直接添加
✅ 正确：输出报告："建议在 STATE_MACHINE.md §8 添加状态 XYZ，需 RFC 审批"
```

---

#### 2. 未经审计直接重写文档
```xml
<forbidden>
  <action>在未调用 ai-ad-doc-system-auditor 的情况下直接重写大量文档</action>
  <reason>可能引入新的不一致性，破坏现有正确内容</reason>
  <correct_action>必须先 AUDIT → 生成问题清单 → 有针对性地修复</correct_action>
</forbidden>
```

**示例**:
```markdown
❌ 错误：发现 API_DEVELOPMENT_FLOW.md 过时，直接调用 fixer 全文重写
✅ 正确：先调用 auditor 生成 P0/P1/P2 报告 → 根据报告针对性修复
```

---

#### 3. 发明新的字段/状态/错误码
```xml
<forbidden>
  <action>在没有 SoT 依据的情况下"发明"新的字段/状态/错误码并写入文档</action>
  <reason>违反 AP-AI-002 反模式规则，破坏 SoT 唯一性</reason>
  <correct_action>检查 SoT 是否已定义 → 如不存在，提出 RFC</correct_action>
</forbidden>
```

**示例**:
```markdown
❌ 错误：发现 daily_reports 需要新字段 `quality_score`，直接写入 dev-guide
✅ 正确：检查 DATA_SCHEMA.md → 如不存在，输出"建议添加新字段，需 DBA 审核"
```

---

#### 4. 绕过 SoT Pipeline
```xml
<forbidden>
  <action>隐式绕过 ai-ad-sot-doc-pipeline 对 SoT 进行"侧写式篡改"</action>
  <reason>破坏 Freeze 保护机制，导致版本混乱</reason>
  <correct_action>必须通过 ai-ad-sot-doc-pipeline 进行 SoT 相关操作</correct_action>
</forbidden>
```

**示例**:
```markdown
❌ 错误：发现 STATE_MACHINE.md 版本号过时，直接更新下游引用
✅ 正确：调用 ai-ad-sot-doc-pipeline → 执行统一的版本对齐流程
```

---

#### 5. 跨层级修改
```xml
<forbidden>
  <action>修改非目标层级的文档（如巡检 dev-guides 时顺便修改 overview）</action>
  <reason>超出授权范围，可能引入意外变更</reason>
  <correct_action>仅修改输入参数指定范围内的文档</correct_action>
</forbidden>
```

---

#### 6. 忽略 Freeze 规则
```xml
<forbidden>
  <action>在 SoT Freeze v2.6 保护下直接修改 STATE_MACHINE.md / DATA_SCHEMA.md 等</action>
  <reason>违反 Freeze 规则，破坏版本稳定性</reason>
  <correct_action>输出"此文档处于 Freeze 状态，需架构委员会审批"</correct_action>
</forbidden>
```

---

## 🔄 WORKFLOW_OVERVIEW

### 高层流程架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI-Ad Spec Governor v1.0                     │
│                     (Orchestration Layer)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 1: DISCOVER (文档发现与分类)      │
         │  - 读取目标文档/扫描目录                  │
         │  - 识别文档类型（SoT / dev-guide / etc）│
         │  - 提取元信息（版本/状态/依赖）          │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 2: AUDIT (规范审计)               │
         │  ┌────────────────────────────────────┐  │
         │  │ 调用: ai-ad-doc-system-auditor     │  │
         │  │ 输出: P0/P1/P2 问题报告            │  │
         │  └────────────────────────────────────┘  │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 3: FIX (自动修复)                 │
         │  ┌────────────────────────────────────┐  │
         │  │ 调用: ai-ad-doc-fixer              │  │
         │  │ 条件: allow_auto_fix=true          │  │
         │  │       + 非 SoT 文档                │  │
         │  └────────────────────────────────────┘  │
         │  ┌────────────────────────────────────┐  │
         │  │ SoT 场景:                          │  │
         │  │ 调用: ai-ad-sot-doc-pipeline       │  │
         │  └────────────────────────────────────┘  │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 4: VERIFY (验证修复效果)          │
         │  ┌────────────────────────────────────┐  │
         │  │ 再次调用: auditor                  │  │
         │  │ 对比前后差异                       │  │
         │  └────────────────────────────────────┘  │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 5: FREEZE_CHECK (Freeze 合规检查) │
         │  - 检查是否违反 SoT Freeze v2.6          │
         │  - 检查是否违反 ASDD Freeze v1.0         │
         │  - 输出 Freeze 冲突报告                  │
         └──────────────────────────────────────────┘
                              │
                              ▼
         ┌──────────────────────────────────────────┐
         │  Phase 6: SUMMARY (总结与判定)           │
         │  - 生成治理报告                          │
         │  - 上线判定: PASS / BLOCK / WARN         │
         │  - 输出修复建议（如有）                  │
         └──────────────────────────────────────────┘
```

---

### 子 Skill 调度矩阵

| Phase | 主要调用的子 Skill | 调用条件 |
|-------|-------------------|---------|
| **DISCOVER** | - | 内置逻辑（Glob/Grep/Read） |
| **AUDIT** | `ai-ad-doc-system-auditor` | 所有文档 |
| **FIX** | `ai-ad-doc-fixer` | 非 SoT 文档 + `allow_auto_fix=true` |
| **FIX** (SoT) | `ai-ad-sot-doc-pipeline` | SoT 文档或 SoT 对齐场景 |
| **VERIFY** | `ai-ad-doc-system-auditor` | 修复后的文档 |
| **COMPLEX_FLOW** | `ai-ad-doc-orchestrator` | 多文档复杂依赖场景 |
| **FREEZE_CHECK** | - | 内置逻辑（检查 SoT 版本号） |
| **SUMMARY** | - | 内置逻辑（汇总报告） |

---

## 📋 PHASE DEFINITIONS

---

### Phase 1: DISCOVER (文档发现与分类)

```xml
<phase id="DISCOVER">
  <goal>
    发现目标文档，提取元信息，识别文档类型和层级，确定治理策略
  </goal>

  <inputs>
    <input name="mode" required="true">运行模式</input>
    <input name="target/targets/scope" required="conditional">目标文档路径</input>
  </inputs>

  <outputs>
    <output name="discovered_docs">文档清单（路径、类型、元信息）</output>
    <output name="doc_classification">文档分类（SoT / dev-guide / appendix）</output>
    <output name="dependency_map">文档依赖关系图</output>
  </outputs>

  <steps>
    <step order="1">
      <description>根据 mode 参数确定搜索策略</description>
      <logic>
        - mode=single-doc: 直接读取 target 文件
        - mode=doc-group: 遍历 targets 列表
        - mode=full-scan: 扫描 scope 目录下所有 .md 文件
        - mode=sot-alignment-check: 搜索所有引用 changed_sot 的文档
        - mode=impact-analysis: 搜索所有引用 changed_section 的文档
      </logic>
    </step>

    <step order="2">
      <description>提取文档元信息</description>
      <logic>
        使用 Read 工具读取文档前 50 行，提取：
        - 文档版本 (> **文档版本**: vX.Y)
        - 文档状态 (> **文档状态**: Active / Draft / Deprecated)
        - 文档类型 (> **文档类型**: SoT / 开发指南 / 附录)
        - 维护团队
        - 最后审查日期
      </logic>
    </step>

    <step order="3">
      <description>文档分类与层级识别</description>
      <logic>
        根据文件路径确定层级（ASDD 6-Layer Architecture）：
        - docs/1.overview/ → Tier 1 (Overview)
        - docs/sot/ → Tier 2 (SoT) [最高优先级]
        - docs/3.dev-guides/ → Tier 3 (Dev Guides)
        - docs/4.architecture/ → Tier 4 (Architecture)
        - docs/5.infrastructure/ → Tier 5 (Infrastructure)
        - docs/6.agent-layer/ → Tier 6 (Agent Layer)

        特殊标记：
        - 如果文件名包含 "_SOT.md"，标记为 SoT 文档
        - 如果元信息标注 Freeze，标记为 Freeze 保护
      </logic>
    </step>

    <step order="4">
      <description>构建依赖关系图</description>
      <logic>
        使用 Grep 工具搜索文档内的引用：
        - 搜索模式: "引用"、"**引用**:"、"参考"
        - 提取被引用的文档名和版本号
        - 构建有向图: 当前文档 → 依赖的 SoT 文档
      </logic>
    </step>

    <step order="5">
      <description>输出发现报告</description>
      <output_format>
        {
          "total_docs": 5,
          "doc_list": [
            {
              "path": "docs/3.dev-guides/API_DEVELOPMENT_FLOW.md",
              "tier": "dev-guides",
              "version": "v7.0",
              "status": "Draft",
              "is_sot": false,
              "is_frozen": false,
              "dependencies": [
                "DATA_SCHEMA.md v5.6",
                "STATE_MACHINE.md v2.8"
              ]
            }
          ],
          "dependency_graph": "..."
        }
      </output_format>
    </step>
  </steps>

  <error_handling>
    <error code="DISCOVER_001">目标文档不存在</error>
    <error code="DISCOVER_002">无法提取元信息（文档缺少必填字段）</error>
    <error code="DISCOVER_003">循环依赖检测（A → B → A）</error>
  </error_handling>
</phase>
```

---

### Phase 2: AUDIT (规范审计)

```xml
<phase id="AUDIT">
  <goal>
    调用 ai-ad-doc-system-auditor 对目标文档进行全面审计，生成 P0/P1/P2 问题报告
  </goal>

  <inputs>
    <input name="discovered_docs" source="DISCOVER">文档清单</input>
    <input name="strict_level" source="user_input">审计严格程度</input>
  </inputs>

  <outputs>
    <output name="audit_reports">每个文档的审计报告（P0/P1/P2 问题清单）</output>
    <output name="severity_summary">问题严重程度统计</output>
    <output name="priority_actions">优先修复建议</output>
  </outputs>

  <steps>
    <step order="1">
      <description>准备审计参数</description>
      <logic>
        根据 strict_level 确定审计范围：
        - paranoid: 启用所有检查项（包括 P2 细节问题）
        - normal: 重点检查 P0/P1 问题
        - relaxed: 仅检查 P0 问题
      </logic>
    </step>

    <step order="2">
      <description>批量调用 ai-ad-doc-system-auditor</description>
      <logic>
        对每个文档执行：
        1. 读取文档完整内容
        2. 调用 auditor 技能（通过 Skill 工具或直接执行 auditor 逻辑）
        3. 生成审计报告（P0/P1/P2 问题清单）
        4. 存储报告到内存

        并行处理优化：
        - 如果文档数 > 5，显示进度条
        - 如果某文档审计失败，继续处理其他文档
      </logic>
    </step>

    <step order="3">
      <description>问题分类与优先级排序</description>
      <logic>
        按严重程度分类：
        - P0 (Blocker): 必须立即修复（如 SoT 冲突、错误的状态定义）
        - P1 (High): 影响可用性（如缺少版本号、引用错误）
        - P2 (Medium): 优化改进（如格式问题、表达不清）

        生成优先级清单：
        1. 先修复 P0 问题
        2. 按文档重要性（SoT > dev-guides > appendix）排序
      </logic>
    </step>

    <step order="4">
      <description>生成审计摘要</description>
      <output_format>
        ## 审计报告摘要

        **总文档数**: 5
        **总问题数**: 23 (P0: 3, P1: 12, P2: 8)

        ### P0 问题 (Blocker)
        1. [API_DEVELOPMENT_FLOW.md] 引用的 STATE_MACHINE.md 版本错误 (v2.3 → 应为 v2.6)
        2. [FRONTEND_SPEC.md] 使用了未定义的错误码 CUSTOM_001
        3. [UI_DESIGN_SYSTEM.md] 重复定义了状态枚举（违反 SoT 唯一性）

        ### P1 问题 (High)
        ...

        ### 修复建议
        - 优先修复 P0 问题（3 项）
        - 调用 ai-ad-doc-fixer 批量修复格式问题
        - 调用 ai-ad-sot-doc-pipeline 对齐 SoT 版本引用
      </output_format>
    </step>
  </steps>

  <error_handling>
    <error code="AUDIT_001">ai-ad-doc-system-auditor 调用失败</error>
    <error code="AUDIT_002">文档内容无法解析（格式错误）</error>
  </error_handling>

  <chain_of_thought>
    我是 ai-ad-spec-governor，正在执行 AUDIT Phase：

    1. 收到 DISCOVER Phase 输出的 5 个文档清单
    2. 设置 strict_level=normal（重点检查 P0/P1）
    3. 开始批量审计...
       - [1/5] API_DEVELOPMENT_FLOW.md: 发现 3 个 P0, 5 个 P1, 2 个 P2
       - [2/5] FRONTEND_SPEC.md: 发现 0 个 P0, 3 个 P1, 1 个 P2
       ...
    4. 汇总问题：P0 共 3 个，P1 共 12 个，P2 共 8 个
    5. 生成优先级清单：优先修复 P0 问题（SoT 冲突最严重）
    6. 输出审计报告，准备进入 FIX Phase
  </chain_of_thought>
</phase>
```

---

### Phase 3: FIX (自动修复)

```xml
<phase id="FIX">
  <goal>
    根据审计报告，调用 ai-ad-doc-fixer 或 ai-ad-sot-doc-pipeline 自动修复问题
  </goal>

  <inputs>
    <input name="audit_reports" source="AUDIT">审计报告</input>
    <input name="allow_auto_fix" source="user_input">是否允许自动修复</input>
    <input name="dry_run" source="user_input">是否仅模拟（不实际修改）</input>
  </inputs>

  <outputs>
    <output name="fix_actions">修复操作清单（已执行的修改）</output>
    <output name="fixed_docs">已修复的文档列表</output>
    <output name="blocked_issues">无法自动修复的问题（需人工处理）</output>
  </outputs>

  <steps>
    <step order="1">
      <description>检查修复前提条件</description>
      <logic>
        if (allow_auto_fix === false) {
          输出: "跳过自动修复，仅生成修复建议"
          return;
        }

        if (dry_run === true) {
          输出: "模拟模式：不实际修改文件，仅输出修复预览"
        }
      </logic>
    </step>

    <step order="2">
      <description>分类问题并确定修复策略</description>
      <logic>
        对 P0/P1 问题进行分类：

        1. **可自动修复** (调用 ai-ad-doc-fixer):
           - 格式问题（Markdown 语法错误）
           - 元信息缺失（补充版本号、状态）
           - 表格/列表格式不规范
           - 术语不一致（对比 GLOSSARY.md 自动替换）

        2. **需 SoT Pipeline** (调用 ai-ad-sot-doc-pipeline):
           - SoT 版本引用错误
           - SoT 对齐问题
           - Freeze 冲突

        3. **无法自动修复** (需人工处理):
           - 业务逻辑错误（如流程描述不清）
           - 重复定义状态/错误码（需删除或合并）
           - 缺少整章节内容
      </logic>
    </step>

    <step order="3">
      <description>执行自动修复（非 SoT 文档）</description>
      <logic>
        对每个可自动修复的问题：
        1. 读取目标文档内容
        2. 调用 ai-ad-doc-fixer，传入：
           - target_file: 文档路径
           - issues: 该文档的 P0/P1 问题清单
           - fix_mode: "targeted" (针对性修复，不全文重写)
        3. 记录修复操作：
           - 修复前内容（diff 对比）
           - 修复后内容
           - 修复的问题编号
        4. 如果 dry_run=false，写入文件
      </logic>
    </step>

    <step order="4">
      <description>执行 SoT 对齐（SoT 相关问题）</description>
      <logic>
        对涉及 SoT 的问题：
        1. 调用 ai-ad-sot-doc-pipeline，传入：
           - mode: "alignment-fix"
           - changed_sot: 涉及的 SoT 文档名
           - target_docs: 需要对齐的下游文档列表
        2. Pipeline 会自动：
           - 更新 SoT 版本引用
           - 检查 Freeze 冲突
           - 生成对齐报告
      </logic>
    </step>

    <step order="5">
      <description>输出修复报告</description>
      <output_format>
        ## 修复报告

        **修复统计**:
        - 已修复问题: 18 / 23
        - 已修复文档: 4 / 5
        - 无法自动修复: 5 (需人工处理)

        ### 已执行的修复操作

        #### [API_DEVELOPMENT_FLOW.md]
        1. ✅ 修复 P0-001: 更新 STATE_MACHINE.md 引用版本 (v2.3 → v2.6)
        2. ✅ 修复 P1-003: 补充元信息缺失的"最后审查"字段
        3. ✅ 修复 P1-007: 修正表格格式（缺少闭合 `|`）

        #### [FRONTEND_SPEC.md]
        1. ✅ 修复 P0-002: 删除自定义错误码 CUSTOM_001，引用 ERROR_CODES_SOT.md
        2. ✅ 修复 P1-009: 术语统一（"用户角色" → "role"）

        ### 无法自动修复的问题（需人工处理）

        1. ❌ [UI_DESIGN_SYSTEM.md] P0-003: 重复定义状态枚举
           - 原因: 需要判断保留哪个定义，需人工决策
           - 建议: 删除本地定义，引用 STATE_MACHINE.md

        2. ❌ [API_DEVELOPMENT_FLOW.md] P1-011: 缺少"错误处理"章节
           - 原因: 需要补充完整内容，超出自动修复范围
           - 建议: 参考 API_SOT.md §4 补充错误处理章节
      </output_format>
    </step>
  </steps>

  <error_handling>
    <error code="FIX_001">ai-ad-doc-fixer 调用失败</error>
    <error code="FIX_002">文件写入失败（权限不足）</error>
    <error code="FIX_003">SoT 文档修复被拒绝（Freeze 保护）</error>
  </error_handling>

  <forbidden_actions_check>
    在执行任何修复前，检查：
    1. 目标文档是否在 docs/sot/ 下？
       - 是 → 拒绝修复，输出："此文档为 SoT，禁止直接修改"
       - 否 → 继续

    2. 修复操作是否会新增未定义的字段/状态/错误码？
       - 是 → 拒绝修复，输出："违反 AP-AI-002 反模式"
       - 否 → 继续

    3. 修复操作是否涉及 Freeze 文档？
       - 是 → 输出警告："此文档处于 Freeze 状态，需架构审批"
       - 否 → 继续
  </forbidden_actions_check>
</phase>
```

---

### Phase 4: VERIFY (验证修复效果)

```xml
<phase id="VERIFY">
  <goal>
    再次调用 ai-ad-doc-system-auditor 验证修复效果，确认问题已解决
  </goal>

  <inputs>
    <input name="fixed_docs" source="FIX">已修复的文档列表</input>
    <input name="original_audit_reports" source="AUDIT">修复前的审计报告</input>
  </inputs>

  <outputs>
    <output name="verification_reports">修复后的审计报告</output>
    <output name="resolved_issues">已解决的问题清单</output>
    <output name="remaining_issues">未解决的问题清单</output>
    <output name="regression_issues">新引入的问题（回归）</output>
  </outputs>

  <steps>
    <step order="1">
      <description>再次审计已修复的文档</description>
      <logic>
        对每个已修复的文档：
        1. 调用 ai-ad-doc-system-auditor
        2. 生成修复后的审计报告
        3. 对比修复前后的问题清单
      </logic>
    </step>

    <step order="2">
      <description>对比修复前后差异</description>
      <logic>
        对每个文档生成 diff 报告：

        resolved_issues = 修复前问题 - 修复后问题
        remaining_issues = 修复前问题 ∩ 修复后问题
        regression_issues = 修复后问题 - 修复前问题

        计算修复率:
        fix_rate = resolved_issues.length / original_issues.length * 100%
      </logic>
    </step>

    <step order="3">
      <description>生成验证报告</description>
      <output_format>
        ## 验证报告

        **修复效果统计**:
        - 已解决: 18 / 23 (78%)
        - 未解决: 5 / 23 (22%)
        - 回归问题: 0 (良好)

        ### 已解决的问题

        #### [API_DEVELOPMENT_FLOW.md]
        - ✅ P0-001: SoT 版本引用错误 → 已修复
        - ✅ P1-003: 元信息缺失 → 已修复
        - ✅ P1-007: 表格格式错误 → 已修复

        ### 未解决的问题（需人工处理）

        #### [UI_DESIGN_SYSTEM.md]
        - ❌ P0-003: 重复定义状态枚举 → 需人工删除

        ### 回归问题（新引入）

        - 无回归问题（修复质量良好）
      </output_format>
    </step>

    <step order="4">
      <description>判定修复是否合格</description>
      <logic>
        判定标准:
        - PASS: P0 问题全部解决 + 修复率 >= 80%
        - WARN: P0 问题全部解决 + 修复率 60-80%
        - BLOCK: 存在未解决的 P0 问题

        输出判定结果，传递给 SUMMARY Phase
      </logic>
    </step>
  </steps>

  <error_handling>
    <error code="VERIFY_001">修复后审计失败</error>
    <error code="VERIFY_002">发现严重回归问题（新增 P0）</error>
  </error_handling>
</phase>
```

---

### Phase 5: FREEZE_CHECK (Freeze 合规检查)

```xml
<phase id="FREEZE_CHECK">
  <goal>
    检查文档修改是否违反 SoT Freeze v2.6 / ASDD Freeze v1.0 规则
  </goal>

  <inputs>
    <input name="fixed_docs" source="FIX">已修复的文档列表</input>
    <input name="discovered_docs" source="DISCOVER">文档清单（含 Freeze 标记）</input>
  </inputs>

  <outputs>
    <output name="freeze_violations">Freeze 冲突清单</output>
    <output name="freeze_compliance">Freeze 合规状态（PASS / WARN / BLOCK）</output>
  </outputs>

  <steps>
    <step order="1">
      <description>识别 Freeze 保护的文档</description>
      <logic>
        Freeze 保护文档列表（SoT Freeze v2.6）:
        - MASTER.md v4.6 (ASDD Freeze v1.0)
        - STATE_MACHINE.md v2.8
        - DATA_SCHEMA.md v5.6
        - API_SOT.md v9.0
        - ERROR_CODES_SOT.md v2.1
        - BUSINESS_RULES.md v3.1
        - AUTH_SPEC.md v2.0
        - DATA_SCHEMA.md v5.11 §3.4.4
        - DAILY_REPORT_SOT.md v4.1
        - RECONCILIATION_SOT.md v2.1
        - TRANSFER_SOT.md v1.0
      </logic>
    </step>

    <step order="2">
      <description>检查是否有 Freeze 文档被修改</description>
      <logic>
        对每个已修复的文档：
        1. 检查是否在 Freeze 保护列表中
        2. 如果是，标记为 Freeze 冲突
        3. 生成冲突报告：
           - 文档路径
           - Freeze 版本号
           - 修改操作描述
           - 需要的审批流程（RFC / 架构委员会）
      </logic>
    </step>

    <step order="3">
      <description>检查下游文档的 SoT 引用</description>
      <logic>
        对非 Freeze 文档（dev-guides / appendix）：
        1. 提取所有 SoT 引用（如 "引用: STATE_MACHINE.md v2.8"）
        2. 检查引用的版本号是否正确
        3. 如果引用了错误版本，标记为 Freeze 冲突
      </logic>
    </step>

    <step order="4">
      <description>生成 Freeze 合规报告</description>
      <output_format>
        ## Freeze 合规检查报告

        **合规状态**: WARN (存在 1 个冲突)

        ### Freeze 冲突

        1. ❌ [STATE_MACHINE.md] 被修改
           - Freeze 版本: v2.6 (SoT Freeze v2.6)
           - 修改操作: 添加新状态 `trend_flagged_resolved`
           - **处理建议**: 此文档处于 Freeze 保护，需提交 RFC 并经架构委员会审批
           - **审批流程**: RFC → 2 名架构师审批 → 版本升级 (v2.6 → v2.7)

        ### Freeze 合规文档

        - ✅ [API_DEVELOPMENT_FLOW.md] 引用 STATE_MACHINE.md v2.8 (正确)
        - ✅ [FRONTEND_SPEC.md] 引用 DATA_SCHEMA.md v5.6 (正确)
      </output_format>
    </step>
  </steps>

  <error_handling>
    <error code="FREEZE_001">检测到 Freeze 文档被直接修改（严重违规）</error>
    <error code="FREEZE_002">下游文档引用了不存在的 SoT 版本</error>
  </error_handling>
</phase>
```

---

### Phase 6: SUMMARY (总结与判定)

```xml
<phase id="SUMMARY">
  <goal>
    生成最终治理报告，输出上线判定（PASS / BLOCK / WARN），提供修复建议
  </goal>

  <inputs>
    <input name="audit_reports" source="AUDIT">审计报告</input>
    <input name="fix_actions" source="FIX">修复操作清单</input>
    <input name="verification_reports" source="VERIFY">验证报告</input>
    <input name="freeze_compliance" source="FREEZE_CHECK">Freeze 合规状态</input>
  </inputs>

  <outputs>
    <output name="governance_report">完整的治理报告（Markdown 格式）</output>
    <output name="deployment_verdict">上线判定（PASS / BLOCK / WARN）</output>
    <output name="action_items">后续行动清单</output>
  </outputs>

  <steps>
    <step order="1">
      <description>汇总所有 Phase 的输出</description>
      <logic>
        整合以下数据：
        - DISCOVER: 文档清单、依赖关系
        - AUDIT: 问题统计（P0/P1/P2）
        - FIX: 修复统计、无法自动修复的问题
        - VERIFY: 修复效果、回归问题
        - FREEZE_CHECK: Freeze 冲突
      </logic>
    </step>

    <step order="2">
      <description>计算综合评分</description>
      <logic>
        评分维度:
        1. 问题解决率: resolved / total * 100%
        2. P0 问题: 0 个 P0 → 100 分，1 个 P0 → 0 分
        3. Freeze 合规: 无冲突 → 100 分，有冲突 → 0 分
        4. 回归问题: 0 个回归 → 100 分，1+ 个回归 → 50 分

        综合得分 = (问题解决率 * 0.3) + (P0 分数 * 0.4)
                   + (Freeze 分数 * 0.2) + (回归分数 * 0.1)
      </logic>
    </step>

    <step order="3">
      <description>生成上线判定</description>
      <logic>
        判定规则:

        BLOCK (禁止上线):
        - 存在未解决的 P0 问题
        - OR 存在 Freeze 冲突且未获得审批
        - OR 存在严重回归问题（新增 P0）

        WARN (警告，需审查):
        - P0 全部解决 BUT 修复率 < 80%
        - OR 存在 5+ 个未解决的 P1 问题
        - OR Freeze 冲突已提交 RFC 但未审批

        PASS (可上线):
        - P0 全部解决
        - 修复率 >= 80%
        - 无 Freeze 冲突
        - 无严重回归
      </logic>
    </step>

    <step order="4">
      <description>生成后续行动清单</description>
      <logic>
        根据判定结果生成 Action Items:

        如果 BLOCK:
        - [ ] 修复所有 P0 问题（必须）
        - [ ] 解决 Freeze 冲突（提交 RFC 或撤销修改）
        - [ ] 修复回归问题

        如果 WARN:
        - [ ] 修复剩余 P1 问题（建议）
        - [ ] 提高修复率至 80% 以上
        - [ ] 等待 RFC 审批结果

        如果 PASS:
        - [ ] 更新 GLOSSARY / DECISIONS / CHECKLIST（如有新术语/决策）
        - [ ] 通知相关团队文档已更新
        - [ ] 记录本次治理操作到 DECISIONS.md
      </logic>
    </step>

    <step order="5">
      <description>输出最终治理报告</description>
      <output_format>
        # Spec Governor 治理报告

        **生成时间**: 2025-11-26 14:30:00 UTC
        **运行模式**: single-doc
        **目标文档**: docs/3.dev-guides/API_DEVELOPMENT_FLOW.md

        ---

        ## 📊 治理统计

        | 指标 | 数值 |
        |------|------|
        | 文档总数 | 1 |
        | 问题总数 | 23 (P0: 3, P1: 12, P2: 8) |
        | 已解决 | 18 / 23 (78%) |
        | 未解决 | 5 / 23 (22%) |
        | 回归问题 | 0 |
        | Freeze 冲突 | 0 |
        | **综合得分** | **85/100** |

        ---

        ## 🎯 上线判定

        **判定结果**: ✅ **PASS** (可上线)

        **理由**:
        - ✅ P0 问题全部解决（3/3）
        - ✅ 修复率达标（78% > 80% 阈值略低，但 P0 清零）
        - ✅ 无 Freeze 冲突
        - ✅ 无回归问题

        ---

        ## 📋 详细报告

        ### Phase 1: DISCOVER
        - 发现文档: 1 个
        - 文档层级: dev-guides (Tier 3)
        - 依赖 SoT: STATE_MACHINE.md v2.8, DATA_SCHEMA.md v5.6

        ### Phase 2: AUDIT
        - P0 问题: 3 个
          1. SoT 版本引用错误
          2. 自定义错误码
          3. 重复定义状态枚举
        - P1 问题: 12 个（元信息缺失、格式问题等）
        - P2 问题: 8 个（优化建议）

        ### Phase 3: FIX
        - 已修复: 18 / 23
        - 调用 ai-ad-doc-fixer: 3 次
        - 调用 ai-ad-sot-doc-pipeline: 1 次
        - 无法自动修复: 5 个（需人工处理）

        ### Phase 4: VERIFY
        - 修复效果: 良好（78% 解决率）
        - 回归问题: 0 个

        ### Phase 5: FREEZE_CHECK
        - Freeze 合规: ✅ PASS
        - 无 Freeze 冲突

        ---

        ## ✅ 后续行动清单

        ### 必须完成（上线前）
        - 无（所有阻塞项已解决）

        ### 建议完成（上线后）
        - [ ] 修复剩余 5 个 P1 问题（提高修复率至 90%）
        - [ ] 补充"错误处理"章节（参考 API_SOT.md §4）
        - [ ] 更新 GLOSSARY.md（如有新术语）

        ---

        ## 📝 治理记录

        - **执行人**: Claude / SuperClaude (ai-ad-spec-governor v1.0)
        - **治理耗时**: 约 5 分钟
        - **修改文件**: 1 个（API_DEVELOPMENT_FLOW.md）
        - **是否记录 ADR**: 建议记录（重大文档修复）
      </output_format>
    </step>
  </steps>

  <error_handling>
    <error code="SUMMARY_001">无法生成综合评分（数据不完整）</error>
    <error code="SUMMARY_002">判定逻辑异常（多个冲突条件）</error>
  </error_handling>
</phase>
```

---

## 📤 OUTPUT_FORMAT

### 标准输出格式

```markdown
# Spec Governor 治理报告

**生成时间**: {timestamp}
**运行模式**: {mode}
**目标文档**: {target}
**综合得分**: {score}/100

---

## 🎯 上线判定

**判定结果**: {PASS | BLOCK | WARN}

**理由**: ...

---

## 📊 治理统计

| 指标 | 数值 |
|------|------|
| 文档总数 | {total_docs} |
| 问题总数 | {total_issues} |
| 已解决 | {resolved} / {total} ({rate}%) |
| 未解决 | {remaining} / {total} |
| 回归问题 | {regressions} |
| Freeze 冲突 | {freeze_conflicts} |

---

## 📋 详细报告

{各 Phase 输出汇总}

---

## ✅ 后续行动清单

### 必须完成（上线前）
- [ ] ...

### 建议完成（上线后）
- [ ] ...
```

---

## 🔗 CHAIN_OF_THOUGHT

### 推理模板

```markdown
我是 ai-ad-spec-governor v1.0，正在执行规范治理任务：

**任务分析**:
- 模式: {mode}
- 目标: {target}
- 严格程度: {strict_level}
- 允许自动修复: {allow_auto_fix}

**执行流程**:
1. [DISCOVER] 发现 {N} 个文档，识别为 {tier} 层级
2. [AUDIT] 调用 ai-ad-doc-system-auditor，发现 {P0/P1/P2} 问题
3. [FIX] 修复 {N} 个问题，无法自动修复 {M} 个
4. [VERIFY] 验证修复效果，修复率 {rate}%
5. [FREEZE_CHECK] 检查 Freeze 合规，发现 {N} 个冲突
6. [SUMMARY] 综合判定: {PASS | BLOCK | WARN}

**关键决策**:
- 是否调用 ai-ad-doc-fixer: {是/否，原因}
- 是否调用 ai-ad-sot-doc-pipeline: {是/否，原因}
- 是否触发 Freeze 警告: {是/否，原因}

**输出**:
- 治理报告已生成
- 上线判定: {判定结果}
- 后续行动: {N} 项必须完成，{M} 项建议完成
```

---

## 🧪 EXAMPLE_USAGE

### 示例 1: 单文档上线前检查

**用户请求**:
```
请检查 API_DEVELOPMENT_FLOW.md 是否可以上线
```

**Spec Governor 响应**:
```markdown
收到治理请求，执行参数：
- mode: single-doc
- target: docs/3.dev-guides/API_DEVELOPMENT_FLOW.md
- strict_level: normal
- allow_auto_fix: true

开始执行...

[Phase 1: DISCOVER] ✅ 完成
- 发现文档: 1 个
- 文档层级: dev-guides (Tier 3)
- 依赖 SoT: STATE_MACHINE.md v2.8, DATA_SCHEMA.md v5.6

[Phase 2: AUDIT] ✅ 完成
- 调用 ai-ad-doc-system-auditor
- 发现问题: 23 个 (P0: 3, P1: 12, P2: 8)

[Phase 3: FIX] ✅ 完成
- 调用 ai-ad-doc-fixer (3 次)
- 调用 ai-ad-sot-doc-pipeline (1 次)
- 已修复: 18 / 23

[Phase 4: VERIFY] ✅ 完成
- 修复率: 78%
- 回归问题: 0

[Phase 5: FREEZE_CHECK] ✅ 完成
- Freeze 合规: PASS

[Phase 6: SUMMARY] ✅ 完成
- 综合得分: 85/100
- **上线判定: ✅ PASS (可上线)**

{完整治理报告}
```

---

### 示例 2: 批量巡检

**用户请求**:
```
对 dev-guides 目录做一次全面巡检
```

**Spec Governor 响应**:
```markdown
收到治理请求，执行参数：
- mode: full-scan
- scope: dev-guides
- strict_level: normal
- allow_auto_fix: false (仅巡检，不修复)

开始执行...

[Phase 1: DISCOVER] ✅ 完成
- 扫描目录: docs/3.dev-guides/
- 发现文档: 12 个

[Phase 2: AUDIT] ✅ 完成
- 批量审计: 12 个文档
- 总问题数: 87 (P0: 8, P1: 35, P2: 44)

[Phase 5: FREEZE_CHECK] ✅ 完成
- Freeze 合规: WARN (3 个文档引用过时 SoT 版本)

[Phase 6: SUMMARY] ✅ 完成
- **巡检判定: ⚠️ WARN (存在 8 个 P0 问题)**

## 巡检摘要

### 健康度评分
- 总分: 68/100 (需改进)
- P0 问题: 8 个（需立即修复）
- P1 问题: 35 个（建议修复）

### 最严重的问题
1. [API_DEVELOPMENT_FLOW.md] P0: SoT 版本引用错误
2. [FRONTEND_SPEC.md] P0: 自定义错误码
3. [UI_DESIGN_SYSTEM.md] P0: 重复定义状态枚举
...

### 后续建议
- 建议批量修复（设置 allow_auto_fix=true 重新运行）
- 建议更新 3 个文档的 SoT 引用
```

---

## 📚 RELATED_SKILLS

### 子 Skill 依赖

| 子 Skill | 版本 | 调用场景 |
|---------|------|---------|
| `ai-ad-doc-system-auditor` | v1.4 | AUDIT Phase / VERIFY Phase |
| `ai-ad-doc-fixer` | latest | FIX Phase (非 SoT 文档) |
| `ai-ad-sot-doc-pipeline` | latest | FIX Phase (SoT 对齐场景) |
| `ai-ad-doc-orchestrator` | v5.2 | COMPLEX_FLOW (多文档复杂依赖) |

---

## 🔄 VERSION_HISTORY

### v1.1 (2025-11-27)
- ✅ 添加 YAML frontmatter 符合 Skill Freeze 标准
- ✅ 更新 Tier 定义至 ASDD 6-Layer Architecture
- ✅ 更新 SoT Freeze v1.0 → v2.6
- ✅ 更新 MASTER.md v4.6 → v3.5
- ✅ 扩展 Freeze 保护文档列表（新增 DAILY_REPORT_SOT/RECONCILIATION_SOT/TRANSFER_SOT）
- ✅ 对齐 baseline: MASTER.md v4.6, SoT Freeze v2.6

### v1.0 (2025-11-26)
- ✅ 初始版本发布
- ✅ 定义 6 个 Phase（DISCOVER / AUDIT / FIX / VERIFY / FREEZE_CHECK / SUMMARY）
- ✅ 支持 6 种运行模式（single-doc / doc-group / full-scan / sot-alignment-check / appendix-sync / impact-analysis）
- ✅ 集成 4 个子 Skill 调度逻辑
- ✅ 实现 Freeze 合规检查
- ✅ 实现上线判定逻辑（PASS / BLOCK / WARN）

---

## 📧 MAINTAINER

**Owner**: doc-architect / wade
**Team**: AI Architecture Team
**Contact**: GitHub Issue / 内部文档系统

---

</skill>
