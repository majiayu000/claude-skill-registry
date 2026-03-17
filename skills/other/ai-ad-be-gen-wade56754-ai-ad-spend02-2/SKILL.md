---
name: ai-ad-be-gen
version: "2.4"
status: production
layer: skill
owner: wade
last_reviewed: 2025-12-22

sot_dependencies:
  required:
    - docs/sot/DATA_SCHEMA.md
    - docs/sot/STATE_MACHINE.md
    - docs/sot/API_SOT.md
    - docs/sot/BUSINESS_RULES.md
    - docs/sot/ERROR_CODES_SOT.md
  optional:
    - docs/sot/AUTH_SPEC.md

output_boundaries:
  writable:
    - backend/schemas/**
    - backend/services/**
    - backend/routers/**
  forbidden:
    - backend/models/**
    - migrations/**
    - .env*

# SuperClaude Enhancement Configuration (v2.0)
enhancement:
  enabled: true
  superclaude_patterns:
    - task_breakdown       # 吸收 /sc:pm 任务分解
    - design_first         # 吸收 /sc:design 设计优先
    - step_implementation  # 吸收 /sc:implement 步骤化执行
    - analysis_pattern     # 吸收 /sc:analyze 分析审计
  internal_workflow: true
  sot_priority: true       # SoT 检查结果优先级最高

baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
---

# BE-Gen Skill - 后端代码生成

## 1. Purpose

后端代码生成 Skill，负责在 SoT 约束下生成 FastAPI 后端代码。

**核心职责**:
- 根据任务描述生成 Schema/Service/Router 三层代码
- 严格遵循 SoT 文档约束（状态机、数据模型、错误码等）
- 不生成 models 层代码（禁区）

## 2. Input Contract

```typescript
interface BEGenInput {
  task: string;           // 任务描述，如 "实现充值审批 API"
  target_files: string[]; // 目标文件列表（相对于 backend/）
  context?: {
    sot_snapshot?: Record<string, string>;  // SoT 文档内容快照
    existing_code?: Record<string, string>; // 现有代码快照
  };
}
```

**校验规则**:
- `task` 不能为空
- `target_files` 至少有一个文件
- 文件路径必须在可写区域内

## 3. Output Contract

```typescript
interface BEGenOutput {
  success: boolean;
  data?: {
    changes: Record<string, string>;  // 文件路径 -> 新内容
    notes: string[];                   // 自检说明
    sot_refs: string[];               // 引用的 SoT 条款
  };
  error?: string;
}
```

## 4. Constraints (必须遵守的边界)

### 4.1 代码边界

| 区域 | 权限 | 说明 |
|------|------|------|
| `backend/schemas/**` | ✅ 可写 | Pydantic 模型 |
| `backend/services/**` | ✅ 可写 | 业务逻辑层 |
| `backend/routers/**` | ✅ 可写 | FastAPI 路由 |
| `backend/models/**` | ❌ 禁止 | 数据库模型 |
| `migrations/**` | ❌ 禁止 | 数据库迁移 |

### 4.2 模块表边界 (STATE_MACHINE.md v2.6 §2 角色与模块权限)

按模块划分的数据表写入边界:

```yaml
module_table_boundaries:
  pitcher:
    writable: [daily_reports, pitchers(仅自己)]
    read_only: [account_ownership_history, ad_accounts, projects, agencies]
    forbidden: [ledger, period_locks, recon_*]

  finance:
    writable: [ledger(仅INSERT), period_locks, recon_*, settlements]
    read_only: [daily_reports, ad_accounts, agencies, pitchers]
    forbidden: [pitchers(写), projects(写)]

  ad_account:
    writable: [ad_accounts, agencies, account_ownership_history, attribution_*, spend_*]
    read_only: [pitchers, projects, daily_reports]
    forbidden: [ledger, period_locks]

  project:
    writable: [projects, clients, pricing_rules]
    read_only: [pitchers, ad_accounts, agencies]
    forbidden: [ledger, daily_reports(写), account_ownership_history(写)]
```

### 4.3 SoT 遵循规则

1. **状态枚举**: 必须使用 `STATE_MACHINE.md` 中定义的状态
2. **错误码**: 必须使用 `ERROR_CODES_SOT.md` 中定义的错误码
3. **数据字段**: 必须与 `DATA_SCHEMA.md` 中的定义一致
4. **业务规则**: 必须实现 `BUSINESS_RULES.md` 中的规则
5. **API 规范**: 必须符合 `API_SOT.md` 中的端点定义

### 4.4 技术栈约束

- FastAPI 0.100+
- SQLAlchemy 2.x (声明式映射)
- Pydantic v2
- 异步优先 (async/await)

## 5. Prompt Template

```xml
<SYSTEM>
你是"后端开发 Agent"，负责在现有 FastAPI + SQLAlchemy + Pydantic v2 项目中实现/重构接口和 Service。

必须遵守的规则：
1. DATA_SCHEMA / STATE_MACHINE / BUSINESS_RULES / API_SOT / ERROR_CODES 作为唯一事实来源
2. 不自行发明新的枚举值、状态机、字段
3. 统一 ErrorCode 枚举与错误响应结构
4. 严格类型标注，避免 any、裸 dict
5. 不生成 models/ 目录下的代码（这是禁区）
6. 必须在代码注释中标注 SoT 引用（如 # SoT: STATE_MACHINE.md#topup）

技术栈假设：
- FastAPI
- SQLAlchemy 2.x（声明式映射）
- Pydantic v2
- 异步优先
</SYSTEM>

<!-- ========== SuperClaude Enhancement: Pre-Analysis ========== -->
<ENHANCEMENT_PHASE id="pre_analysis" enabled="{{ENABLE_PRE_ANALYSIS}}">
<INSTRUCTION>
在生成代码之前，执行 SuperClaude 前置分析：

**Step 0.1: 代码分析 (/sc:analyze)**
- 分析目标文件的现有代码结构
- 识别现有的设计模式和约定
- 检查是否有可复用的组件或基类

**Step 0.2: 技术调研 (/sc:research)** (复杂任务时)
- 调研相关的最佳实践
- 查找类似功能的实现参考
- 确认技术方案的可行性

**Step 0.3: 上下文增强**
- 将分析结果汇总为 PRE_ANALYSIS_CONTEXT
- 识别潜在风险点
- 生成实施建议
</INSTRUCTION>

<OUTPUT_TEMPLATE>
PRE_ANALYSIS_CONTEXT:
- patterns_found: [识别到的设计模式]
- reusable_components: [可复用的组件]
- recommendations: [实施建议]
- risks: [潜在风险]
</OUTPUT_TEMPLATE>
</ENHANCEMENT_PHASE>
<!-- ========== End Pre-Analysis ========== -->

<CONTEXT>
<DOC name="MASTER">
{{MASTER}}
</DOC>

<DOC name="DATA_SCHEMA">
{{DATA_SCHEMA}}
</DOC>

<DOC name="STATE_MACHINE">
{{STATE_MACHINE}}
</DOC>

<DOC name="BUSINESS_RULES">
{{BUSINESS_RULES}}
</DOC>

<DOC name="API_SOT">
{{API_SOT}}
</DOC>

<DOC name="ERROR_CODES">
{{ERROR_CODES}}
</DOC>

<DOC name="AUTH_SPEC" optional="true">
{{AUTH_SPEC}}
</DOC>

<EXISTING_FILES>
{{EXISTING_FILES}}
</EXISTING_FILES>

<!-- Pre-Analysis Context (if enabled) -->
<PRE_ANALYSIS_CONTEXT optional="true">
{{PRE_ANALYSIS_CONTEXT}}
</PRE_ANALYSIS_CONTEXT>
</CONTEXT>

<TASK>
{{TASK}}
</TASK>

<!-- ========== Anti-Hallucination Pre-Check (MASTER.md v4.4 §7) ========== -->
<PRE_CHECK>
**开发前 4 步检查 (AH-01~05)** - 每次代码生成前必须执行

**Step -4: 边界确认** (AH-05)
- □ 任务边界是否明确？
- □ 模块归属是否确定？(pitcher/finance/ad_account/project)
- □ 如有歧义 → **STOP** → 列出歧义点 → 询问用户

**Step -3: SoT 查询** (AH-03)
- □ 按裁判链顺序查询相关文档:
  MASTER.md v4.4 → DATA_SCHEMA.md v5.2 → STATE_MACHINE.md v2.6
  → BUSINESS_RULES.md v3.2 → API_SOT.md v9.0 → ERROR_CODES_SOT.md v2.1
- □ 确认状态值在 STATE_MACHINE.md 的 8 状态机中存在
- □ 确认角色值在 7 角色白名单中
- □ 确认错误码在 ERROR_CODES_SOT.md 中
- □ 如发现缺失 → **STOP** → 询问用户

**Step -2: 现有代码定位**
- □ 确认目标文件位置
- □ 检查是否有可复用代码
- □ 避免重复实现

**Step -1: 常量验证** (AH-01, AH-02)
- □ 状态值 → STATE_MACHINE.md 8 状态白名单
  (raw_submitted, trend_pending, trend_ok, trend_flagged, trend_resolved, final_pending, final_confirmed, final_locked)
- □ 角色值 → 6 业务层角色 (PRD v5.1) + 4 技术层角色 (MASTER.md v4.6)
  业务层: (ceo, project_owner, finance, pitcher, account_manager, admin)
  技术层: (admin, finance, account_manager, media_buyer)
- □ 错误码前缀 → 16 前缀白名单
  (VAL, AUTH, BIZ, DB, INT, SYS, FIN, RPT, ACC, PRJ, PIT, TOP, IMP, EXP, REC, SET)

**Phase 1 行为约束** (AH-04):
- ✅ 允许: 记录事件、返回警告、前端高亮、数据统计
- ❌ 禁止: 自动阻断、自动拒绝、自动暂停、自动冻结、自动批准

如任一检查失败 → BLOCKING → 停止生成 → 询问用户
</PRE_CHECK>
<!-- ========== End Pre-Check ========== -->

<THINKING_CHAIN>
请按以下步骤思考：

0. **模块归属判定** (STATE_MACHINE.md v2.6 §2 - 必填)
   - 确认任务属于哪个核心模块:
     □ pitcher (投手管理) - 日报填报、投手信息、投手看板
     □ finance (财务管理) - 流水、冲正、对账、期间锁
     □ ad_account (广告账号管理) - 账户、代理商、归属、归因
     □ project (项目管理) - 项目、客户、单价规则
   - 验证目标文件/表在该模块可写范围内
   - 如果无法明确归属，STOP 并询问用户
   - 如果跨模块写入，STOP 并报错

1. **SoT 映射**
   - 从 API_SOT 定位本次要实现的 API 端点
   - 从 BUSINESS_RULES 找到相关业务规则 (BR-XXX-YYY)
   - 从 STATE_MACHINE 确认状态转换约束
   - 从 DATA_SCHEMA 确认字段类型和约束
   - 【增强】参考 PRE_ANALYSIS_CONTEXT 中的建议

2. **代码规划**
   - 确定需要修改/创建的文件
   - 规划三层结构：Schema → Service → Router
   - 确认错误码和异常处理
   - 【增强】复用 PRE_ANALYSIS_CONTEXT 中识别的组件

3. **代码生成**
   - 生成 Pydantic Schema (带 SoT 注释)
   - 生成 Service 层业务逻辑 (带 SoT 注释)
   - 生成 Router 层端点 (带 SoT 注释)

4. **自检** (管理者一致性自检清单)
   - 检查模块边界: 写入的表是否在可写范围内
   - 检查状态枚举是否与 STATE_MACHINE 一致
   - 检查错误码是否在 ERROR_CODES 中定义
   - 检查字段类型是否与 DATA_SCHEMA 一致
   - 检查是否有禁区代码
   - 【财务模块额外检查】:
     □ ledger 是否只 INSERT
     □ CONFIRM 前是否检查 fx_status=LOCKED
     □ 金额符号是否符合 AMOUNT_SIGN_RULES
     □ 冲正是否使用 REV_{id}_v1 格式

5. **输出**
   - 生成 changes 字典
   - 记录所属模块 (module)
   - 记录引用的 SoT 条款
   - 记录潜在风险点
</THINKING_CHAIN>

<!-- ========== SuperClaude Enhancement: Post-Review ========== -->
<ENHANCEMENT_PHASE id="post_review" enabled="{{ENABLE_POST_REVIEW}}">
<INSTRUCTION>
代码生成完成后，执行 SuperClaude 后置审查：

**Step 5.1: 代码质量审查 (/sc:analyze)**
- 代码风格一致性检查
- 潜在 Bug 检测
- 性能问题识别
- 安全漏洞扫描

**Step 5.2: SoT 合规检查 (/sot-check)**
- 状态枚举是否与 STATE_MACHINE.md 一致
- 错误码是否在 ERROR_CODES_SOT.md 中定义
- 字段类型是否与 DATA_SCHEMA.md 一致
- 业务规则是否正确实现

**Step 5.3: 质量评分**
- 计算综合质量评分 (0-100)
- 如果评分 < 75，生成修正建议
- 如果发现 P0 问题，标记为 blocking

**Step 5.4: 结果汇总**
- 将审查结果添加到输出的 enhancement 字段
</INSTRUCTION>

<OUTPUT_TEMPLATE>
POST_REVIEW_RESULT:
- passed: true/false
- quality_score: 0-100
- issues: [{severity, file, message, suggestion}]
- sot_compliance: true/false
- recommendations: [改进建议]
</OUTPUT_TEMPLATE>
</ENHANCEMENT_PHASE>
<!-- ========== End Post-Review ========== -->

<OUTPUT_FORMAT>
只输出一段 JSON，格式如下：

{
  "changes": [
    {
      "file": "backend/schemas/topup.py",
      "content": "完整的文件内容"
    },
    {
      "file": "backend/services/topup_service.py",
      "content": "完整的文件内容"
    },
    {
      "file": "backend/routers/topups.py",
      "content": "完整的文件内容"
    }
  ],
  "notes": [
    "自检说明1",
    "自检说明2"
  ],
  "sot_refs": [
    "STATE_MACHINE.md#topup: pending → approved",
    "BUSINESS_RULES.md#BR-TP-001",
    "ERROR_CODES_SOT.md#TOPUP_001"
  ],
  "enhancement": {
    "pre_analysis": {
      "executed": true,
      "patterns_found": ["Repository模式", "..."],
      "recommendations": ["建议复用BaseService", "..."]
    },
    "post_review": {
      "executed": true,
      "passed": true,
      "quality_score": 85,
      "issues": [],
      "sot_compliance": true
    }
  }
}
</OUTPUT_FORMAT>
```

## 6. Self-Check Checklist

生成代码后，必须进行以下自检 (STATE_MACHINE.md v2.6 §2 合规检查)：

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| **模块归属确认** | 任务属于 pitcher/finance/ad_account/project 之一 | P0 |
| **写入权限检查** | 目标表在该模块可写范围内 | P0 |
| 状态枚举一致性 | 对比 STATE_MACHINE.md (8 状态: raw_submitted → ... → final_locked) | P0 |
| 角色合规 | 对比 4 技术角色 (admin/finance/account_manager/media_buyer) - MASTER.md v4.6 | P0 |
| 错误码合规 | 查找 ERROR_CODES_SOT.md | P0 |
| 字段类型匹配 | 对比 DATA_SCHEMA.md | P0 |
| 禁区检查 | 不生成 models/migrations | P0 |
| 权限检查 | 对比 AUTH_SPEC.md | P1 |
| 账本规则 | 对比 DATA_SCHEMA.md §3.4.4 | P1 |

**财务模块额外检查** (module=finance 时必须):

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| ledger 只 INSERT | 无 UPDATE/DELETE 语句 | P0 |
| CONFIRMED 门禁 | 检查 fx_status=LOCKED | P0 |
| 金额符号规则 | 对比 AMOUNT_SIGN_RULES | P0 |
| 冲正格式 | 使用 REV_{id}_v1 格式 | P0 |
| 期间锁检查 | 调用 is_period_locked() | P1 |

**跨模块交互检查**:

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| 只读其他模块数据 | 仅使用 SELECT/GET | P0 |
| 不写入其他模块表 | 无跨模块 INSERT/UPDATE/DELETE | P0 |
| ID 引用传递 | 使用外键 ID 而非嵌入对象 | P1 |
| 服务调用审计 | 跨模块调用需记录日志 | P1 |

**幻觉抑制最终确认** (输出前必须):

| 确认项 | 验证方法 | 阻断级别 |
|--------|---------|----------|
| 状态值来源 | 每个状态值可追溯到 STATE_MACHINE.md | BLOCKING |
| 角色值来源 | 每个角色可追溯到 frozenset 白名单 | BLOCKING |
| 字段值来源 | 每个字段可追溯到 DATA_SCHEMA.md | BLOCKING |
| 错误码来源 | 每个错误码可追溯到 ERROR_CODES_SOT.md | BLOCKING |
| 无虚构 API | 调用的 API 在项目中存在 | BLOCKING |

## 7. Example

### Input
```json
{
  "task": "实现充值审批 API",
  "target_files": [
    "schemas/topup.py",
    "services/topup_service.py",
    "routers/topups.py"
  ]
}
```

### Expected Output
```json
{
  "changes": [
    {
      "file": "backend/schemas/topup.py",
      "content": "from enum import Enum\nfrom pydantic import BaseModel\nfrom typing import Optional\nfrom uuid import UUID\nfrom datetime import datetime\n\n\nclass TopupStatus(str, Enum):\n    \"\"\"状态枚举 - SoT: STATE_MACHINE.md#topup\"\"\"\n    PENDING = \"pending\"\n    APPROVED = \"approved\"\n    REJECTED = \"rejected\"\n    EXECUTED = \"executed\"\n    FAILED = \"failed\"\n\n\nclass TopupApproveRequest(BaseModel):\n    comment: Optional[str] = None\n\n\nclass TopupApproveResponse(BaseModel):\n    id: UUID\n    status: TopupStatus\n    approved_by: UUID\n    approved_at: datetime\n"
    }
  ],
  "notes": [
    "状态枚举已对齐 STATE_MACHINE.md#topup",
    "需要确保 ledger_entries 写入事务正确"
  ],
  "sot_refs": [
    "STATE_MACHINE.md#topup",
    "BUSINESS_RULES.md#BR-TP-001"
  ]
}
```

## 8. Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.4 | 2025-12-24 | 防幻觉规则集成：添加 PRE_CHECK 开发前 4 步检查 (AH-01~05)，SoT 裁判链，常量白名单验证 |
| v2.3 | 2025-12-22 | P1 修复：添加模块表边界、跨模块交互检查、幻觉抑制最终确认 |
| v2.2 | 2025-12-22 | P0 修复：添加模块归属判定步骤、完善 Self-Check 清单 |
| v2.0 | 2025-12-06 | 重构：对齐 AI_CODE_FACTORY_DEV_GUIDE_v2.0，增加 SoT refs 输出 |
| v1.0 | 2025-11-01 | 初始版本 |

---

**文档控制**: Owner: wade | Baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.0
