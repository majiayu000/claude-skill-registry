---
name: ai-ad-code-verifier
version: "2.5"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-12-24
baseline:
  - MASTER.md v4.4
  - STATE_MACHINE.md v2.6
  - CODE_FACTORY_REFERENCE_PROJECTS.md v1.0
new_features_v2_5:
  - 歧义处理流程 (AH-05) - ambiguity_handling 章节
  - Phase 1 行为约束验证 (AH-04) - phase1_constraints 章节
  - 7 角色白名单更新 (MASTER.md v4.4 §2.4)
  - 禁止模式正则检测
new_features_v2_4:
  - Phase 1/2 边界检查（PhaseConfig）
  - AH-01~05 防幻觉检查（AntiHallucinationChecker）
  - SoT 动态加载器（SotLoader）
code_sources:
  - project: HallOumi
    github: https://github.com/vectara/hallucination-leaderboard
    license: Apache-2.0
    borrowed_concepts:
      - 幻觉检测理念
      - 事实验证方法论
  - project: tree-sitter
    github: https://github.com/tree-sitter/tree-sitter
    license: MIT
    borrowed_concepts:
      - AST 解析策略
      - 多语言支持架构
  - project: mypy
    github: https://github.com/python/mypy
    license: MIT
    borrowed_concepts:
      - 静态类型检查架构
      - 类型错误报告格式
  - project: ruff
    github: https://github.com/astral-sh/ruff
    license: MIT
    borrowed_concepts:
      - 快速 Linting 架构
      - 规则配置系统
      - 自动修复模式
  - project: Qodo Cover
    github: https://github.com/qodo-ai/qodo-cover
    license: AGPL-3.0
    borrowed_concepts:
      - 测试生成策略
      - 覆盖率分析方法
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-code-verifier</name>
  <version>2.0</version>
  <domain>AI_AD_SYSTEM / 代码工厂 / 代码验证</domain>
  <profile>Enhanced-Verifier / Anti-Hallucination / Auto-Fix</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 核心架构 (Architecture)
  ====================================================== -->
  <architecture>
    增强版验证器采用 8 层验证流水线 (v2.2 新增幻觉抑制最终确认层):

    ```
    ┌─────────────────────────────────────────────────────────┐
    │                  EnhancedCodeVerifier                    │
    │                    (主编排器)                            │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 0: ModuleBoundaryVerifier (优先级 5) [v2.1 新增]  │
    │  - 验证目标模块归属 (pitcher/finance/ad_account/project) │
    │  - 检查写入表是否在该模块可写范围内                        │
    │  - 阻止跨模块写入操作                                     │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 1: HallucinationDetector (优先级 10)              │
    │  - 检测 AI 幻觉: 不存在的 API/函数/模块                   │
    │  - 验证导入是否真实存在                                   │
    │  - 检查 API 端点是否在项目中定义                          │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 2: ASTVerifier (优先级 20)                        │
    │  - 语法正确性验证                                        │
    │  - 代码结构完整性                                        │
    │  - 括号/缩进匹配                                         │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 3: SpecComplianceVerifier (优先级 30)             │
    │  - SoT 合规验证 (状态/角色/字段/错误码)                   │
    │  - 日报 8 状态验证 (raw_submitted...final_locked)       │
    │  - 4 技术角色验证 (admin/finance/account_manager/media_buyer) - MASTER.md v4.6 │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 3.5: FinanceRulesVerifier (优先级 35) [v2.1 新增] │
    │  - Ledger 只 INSERT 验证 (禁止 UPDATE/DELETE)            │
    │  - CONFIRMED 门禁 (fx_status=LOCKED)                     │
    │  - 冲正链验证 (禁止冲正的冲正)                            │
    │  - 金额符号验证 (AMOUNT_SIGN_RULES)                      │
    │  - 期间锁检查 (period_locks)                             │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 4: IntegrationVerifier (优先级 40)                │
    │  - 导入路径验证                                          │
    │  - 依赖可用性检查                                        │
    │  - 循环导入检测                                          │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 5: TestVerifier (优先级 50)                       │
    │  - 测试文件存在性                                        │
    │  - 测试覆盖率检查                                        │
    │  - 测试质量验证                                          │
    └───────────────────────┬─────────────────────────────────┘
                            │
    ┌───────────────────────▼─────────────────────────────────┐
    │  Layer 6: HallucinationSuppressor (优先级 60) [v2.2 新增] │
    │  - 状态值来源追溯 → STATE_MACHINE.md                     │
    │  - 角色值来源追溯 → frozenset 白名单                     │
    │  - 字段值来源追溯 → DATA_SCHEMA.md                       │
    │  - 错误码来源追溯 → ERROR_CODES_SOT.md                   │
    │  - API 调用来源追溯 → 项目代码                           │
    │  - 生成 source_traceability_report                       │
    │  - 任何追溯失败 → BLOCKING                               │
    └─────────────────────────────────────────────────────────┘
    ```

    实现文件位置:
    - `agents/skills/verifiers/__init__.py` - 模块导出
    - `agents/skills/verifiers/base.py` - 基础类型和接口
    - `agents/skills/verifiers/module_boundary_verifier.py` - 模块边界验证 [v2.1 新增]
    - `agents/skills/verifiers/hallucination_detector.py` - 幻觉检测
    - `agents/skills/verifiers/ast_verifier.py` - AST 验证
    - `agents/skills/verifiers/spec_compliance_verifier.py` - SoT 合规
    - `agents/skills/verifiers/finance_rules_verifier.py` - 财务规则验证 [v2.1 新增]
    - `agents/skills/verifiers/integration_verifier.py` - 集成验证
    - `agents/skills/verifiers/test_verifier.py` - 测试验证
    - `agents/skills/verifiers/hallucination_suppressor.py` - 幻觉抑制最终确认 [v2.2 新增]
    - `agents/skills/verifiers/enhanced_verifier.py` - 主编排器
  </architecture>


  <!-- ======================================================
       1. 核心使命 (Mission)
  ====================================================== -->
  <mission>
    作为代码工厂的质量守门员，防止 AI 幻觉并确保代码质量。

    核心原则:
    - 🎯 防幻觉: 检测 AI 生成的虚假 API/函数/模块
    - ✅ 多维验证: 语法 + SoT 合规 + 集成 + 测试
    - 🔄 自动修复: 对可自动修复的问题直接修复
    - 📊 报告聚合: 统一格式的验证报告
    - 🔁 迭代修复: 支持最多 3 次自动修复迭代
  </mission>


  <!-- ======================================================
       2. 错误码体系 (Error Codes)
  ====================================================== -->
  <error_codes>
    幻觉检测 (HALL):
    - HALL-001: 导入不存在的模块
    - HALL-002: 导入不存在的名称
    - HALL-003: 调用不存在的第三方函数
    - HALL-004: 调用不存在的项目函数
    - HALL-005: 使用不存在的 API 端点
    - HALL-006: 引用不存在的项目模块
    - HALL-007: 导入不存在的项目对象

    语法验证 (SYN):
    - SYN-001: 语法错误
    - SYN-002: 意外的 EOF
    - SYN-003: 缩进错误
    - SYN-004: 括号不匹配
    - SYN-005: 引号不匹配
    - SYN-006: 混合缩进
    - SYN-007: 字符串多行未闭合
    - SYN-008: TypeScript 语法错误

    结构验证 (STR):
    - STR-001: 函数体为空
    - STR-002: 类体为空
    - STR-003: 缺少函数定义
    - STR-004: 缺少类定义
    - STR-005: 代码被截断
    - STR-006: 导入后无代码
    - STR-007: 缺少返回语句

    SoT 合规 (SOT):
    - SOT-001: 使用未定义的状态
    - SOT-002: 使用旧状态名 (如 raw_submitted)
    - SOT-003: 使用非法角色
    - SOT-004: 使用旧角色名 (如 media_buyer)
    - SOT-005: 使用未知字段
    - SOT-006: 使用非标准错误码
    - SOT-007: 使用未知错误前缀
    - SOT-008: 直接修改 balance
    - SOT-009: 跨模块写入 (违反模块边界)

    财务规则 (FIN) - DATA_SCHEMA.md v5.11 §3.4.4 + STATE_MACHINE.md v2.6:
    - FIN-001: UPDATE ledger 表 (禁止)
    - FIN-002: DELETE ledger 表 (禁止)
    - FIN-003: CONFIRMED 时缺少 fx_status=LOCKED 检查
    - FIN-004: 冲正链循环 (冲正的冲正)
    - FIN-005: 期间锁绕过 (未检查 period_locks)
    - FIN-006: 金额符号错误 (违反 AMOUNT_SIGN_RULES)
    - FIN-007: 缺少冲正原因 (reason < 10 字符)

    集成验证 (INT):
    - INT-001: 未识别的模块
    - INT-002: 相对导入路径不存在
    - INT-003: 第三方库未安装
    - INT-004: 项目模块不存在
    - INT-005: 潜在循环导入
    - INT-006: 导入分组缺少空行
    - INT-007: 使用 star import
    - INT-008: 代码位置不正确

    测试验证 (TST):
    - TST-001: 缺少测试文件
    - TST-002: 缺少测试覆盖
    - TST-003: 测试失败
    - TST-004: 测试缺少断言
    - TST-005: 空测试函数
    - TST-006: 测试名称不够描述性
    - TST-007: P0 功能缺少测试覆盖 [v2.3 新增]
    - TST-008: P0 功能测试覆盖率不足 [v2.3 新增]
    - TST-009: P0 功能缺少边界测试 [v2.3 新增]

    幻觉抑制 (SUP) - v2.2 新增:
    - SUP-001: 状态值无法追溯到 STATE_MACHINE.md
    - SUP-002: 角色值无法追溯到 frozenset 白名单
    - SUP-003: 字段值无法追溯到 DATA_SCHEMA.md
    - SUP-004: 错误码无法追溯到 ERROR_CODES_SOT.md
    - SUP-005: API 调用在项目中不存在
    - SUP-006: 导入的模块/函数在项目中不存在
    - SUP-007: 使用非标准来源标注格式 (应为 # SoT: {DOC}#{SECTION})
  </error_codes>


  <!-- ======================================================
       3. 输入契约 (Input Contract)
  ====================================================== -->
  <input_contract>
    必填:
    {
      assembled_files: AssembledFile[],  // 组装后的文件列表
      requirement: string                 // 原始需求描述
    }

    可选:
    {
      config: {
        enable_hallucination: boolean,   // 幻觉检测 (默认 true)
        enable_ast: boolean,             // AST 验证 (默认 true)
        enable_spec: boolean,            // SoT 合规 (默认 true)
        enable_integration: boolean,     // 集成验证 (默认 true)
        enable_test: boolean,            // 测试验证 (默认 false)
        enable_p0_test_check: boolean,   // P0 功能测试检查 (默认 true) [v2.3 新增]
        auto_fix: boolean,               // 自动修复 (默认 true)
        max_fix_iterations: number,      // 最大修复次数 (默认 3)
        strict_mode: boolean,            // 严格模式 (默认 false)
        run_tests: boolean,              // 运行测试 (默认 false)
        p0_coverage_threshold: number    // P0 功能最低覆盖率 (默认 90) [v2.3 新增]
      },
      context: {                         // 验证上下文
        valid_states: string[],          // 合法状态列表
        valid_roles: string[],           // 合法角色列表
        valid_error_codes: string[],     // 合法错误码列表
        existing_modules: string[],      // 项目现有模块
        existing_functions: string[],    // 项目现有函数
        existing_endpoints: string[]     // 项目现有 API 端点
      }
    }
  </input_contract>


  <!-- ======================================================
       4. 输出契约 (Output Contract)
  ====================================================== -->
  <output_contract>
    {
      success: boolean,
      data: {
        verified_files: [
          {
            path: string,
            original_content: string,
            verified_content: string,
            status: "passed" | "fixed" | "failed" | "skipped",
            issues: VerifyIssue[],
            fixes_applied: number
          }
        ],
        summary: {
          total_files: number,
          passed: number,
          fixed: number,
          failed: number,
          skipped: number
        },
        all_issues: VerifyIssue[]
      },
      error: string | null
    }

    VerifyIssue:
    {
      file_path: string,
      line: number,
      column: number,
      category: string,           // "hallucination" | "syntax" | ...
      severity: "error" | "warning" | "info",
      code: string,               // "HALL-001", "SOT-003", etc.
      message: string,
      suggestion: string,
      evidence: string | null,
      auto_fixable: boolean,
      fix_applied: boolean
    }
  </output_contract>


  <!-- ======================================================
       5. 使用示例 (Usage Examples)
  ====================================================== -->
  <usage>
    示例 1: Python 代码使用
    ```python
    from agents.skills.verifiers import (
        EnhancedCodeVerifier,
        VerifyContext,
        VerifierConfig,
    )
    from pathlib import Path

    # 创建上下文
    context = VerifyContext(
        project_root=Path("/path/to/project"),
        requirement="实现用户注册 API",
        valid_states={"pending", "active", "disabled"},
        valid_roles={"admin", "finance", "media_buyer"},
    )

    # 配置验证器
    config = VerifierConfig(
        enable_hallucination=True,
        enable_ast=True,
        enable_spec=True,
        enable_integration=True,
        enable_test=False,
        auto_fix=True,
    )

    # 创建验证器
    verifier = EnhancedCodeVerifier(context, config)

    # 验证文件
    result = verifier.verify_file("path/to/file.py", file_content)

    # 检查结果
    if result.status == "passed":
        print("验证通过!")
    elif result.status == "fixed":
        print(f"已自动修复 {result.fixes_applied} 个问题")
        print(result.verified_content)
    else:
        print("验证失败:")
        for issue in result.issues:
            print(f"  [{issue.code}] {issue.message}")
    ```

    示例 2: 快速验证
    ```python
    from agents.skills.verifiers import quick_verify

    result = quick_verify(
        file_path="backend/services/user_service.py",
        content=code_content,
        project_root="/path/to/project",
    )

    if result["passed"]:
        print("验证通过")
    else:
        for error in result["errors"]:
            print(f"错误: {error['message']}")
    ```

    示例 3: 批量验证并生成报告
    ```python
    from agents.skills.verifiers import create_verifier_from_project

    # 从项目自动加载 SoT 定义
    verifier = create_verifier_from_project(
        project_root="/path/to/project",
        requirement="重构用户模块",
    )

    # 批量验证
    files = [
        ("file1.py", content1),
        ("file2.py", content2),
    ]
    results = verifier.verify_files(files)

    # 生成 Markdown 报告
    report = verifier.generate_report(results, format="markdown")
    print(report)
    ```
  </usage>


  <!-- ======================================================
       6. SoT 合规验证详情
  ====================================================== -->
  <sot_compliance_details>
    <!-- 状态值白名单 (STATE_MACHINE.md v2.6 全局状态表) -->

    日报状态机 (STATE_MACHINE.md v2.6 + DATA_SCHEMA.md v5.2):
    ```python
    # 使用 frozenset 确保不可变 (对齐 backend/models/enums.py)
    REPORT_STATUS = frozenset([
        'raw_submitted',    # 投手提交原始粉数
        'trend_pending',    # 等待趋势风控检查
        'trend_ok',         # 趋势正常
        'trend_flagged',    # 趋势异常,需人工复核
        'trend_resolved',   # 运营确认异常已解决
        'final_pending',    # 等待最终粉数确认
        'final_confirmed',  # 最终粉数已确认
        'final_locked'      # 已进入计费,锁定(终态)
    ])

    # 已废弃状态 (会触发 SOT-002):
    # DRAFT, SUBMITTED, PLATFORM_MATCHED, DIFF_FLAGGED, CONFIRMED, REJECTED, REVISED
    # (这些是旧版 7 状态,已弃用)
    ```

    Ledger 状态机:
    ```python
    LEDGER_STATUS = frozenset([
        'PENDING',    # 待处理
        'APPROVED',   # 已审批
        'EXECUTED',   # 已执行
        'CONFIRMED',  # 已确认 (需 fx_status=LOCKED)
        'REJECTED'    # 已拒绝
    ])

    LEDGER_FX_STATUS = frozenset([
        'PENDING',    # 待锁定
        'ESTIMATED',  # 预估
        'LOCKED'      # 已锁定
    ])
    ```

    账户状态机:
    ```python
    ACCOUNT_STATUS = frozenset([
        'active',     # 活跃
        'idle',       # 闲置
        'suspended',  # 暂停
        'banned'      # 封禁
    ])
    ```

    项目状态机:
    ```python
    PROJECT_STATUS = frozenset([
        'active',     # 进行中
        'paused',     # 暂停
        'completed',  # 已完成
        'cancelled'   # 已取消
    ])
    ```

    充值状态机:
    ```python
    TOPUP_STATUS = frozenset([
        'pending',    # 待审批
        'approved',   # 已审批
        'rejected',   # 已拒绝
        'settled'     # 已结算
    ])
    ```

    合法角色 (6 业务层 + 4 技术层, 来源: PRD v5.1, MASTER.md v4.6):
    ```python
    # 业务层 6 角色 (PRD v5.1)
    BUSINESS_ROLES = frozenset([
        'ceo',              # 老板 - 资金安全、公司盈亏、最终决策
        'project_owner',    # 项目负责人 - 日报审核、项目盈亏、资金使用效率
        'finance',          # 财务 - 资金出入准确、数据真实、对账
        'pitcher',          # 投手 - CPL 达标、日报准确、执行投放
        'account_manager',  # 户管 - 账户分配、账户状态监控
        'admin'             # 管理员 - 系统配置（不参与业务）
    ])

    # 技术层 4 角色 (MASTER.md v4.6 §INV-007)
    TECHNICAL_ROLES = frozenset(['admin', 'finance', 'account_manager', 'media_buyer'])

    # 已废弃角色 (会触发 SOT-004):
    # supervisor → project_owner (PRD v5.1)
    # data_operator → project_owner/finance (PRD v5.1)
    # super_admin → admin
    # accountant → finance
    ```

    错误码前缀 (ERROR_CODES_SOT.md v2.1 + P2 补充):
    ```python
    VALID_ERROR_PREFIXES = frozenset([
        # 通用错误 (General)
        'VAL',   # 验证错误 - 输入参数校验失败
        'AUTH',  # 认证/授权错误 - 登录、权限、Token
        'BIZ',   # 业务逻辑错误 - 通用业务规则违反
        'DB',    # 数据库错误 - 连接、查询、事务
        'INT',   # 集成错误 - 外部服务调用失败
        'SYS',   # 系统错误 - 内部异常、配置错误

        # 模块专用错误 (Module-Specific)
        'FIN',   # 财务错误 - ledger/冲正/对账/期间锁
        'RPT',   # 日报错误 - 日报提交/确认/状态流转
        'ACC',   # 账户错误 - 广告账户/代理商/归属
        'PRJ',   # 项目错误 - 项目/客户/单价规则
        'PIT',   # 投手错误 - 投手信息/权限/分配
        'TOP',   # 充值错误 - 充值申请/审批/结算
        'IMP',   # 导入错误 - 数据导入/模板/格式
        'EXP',   # 导出错误 - 数据导出/Excel/PDF
        'REC',   # 对账错误 - 平台对账/差异处理
        'SET',   # 结算错误 - 结算单/付款/确认
    ])

    # 错误码格式: {PREFIX}-{NUMBER}
    # 示例: RPT-001, FIN-003, ACC-010
    # NUMBER 范围: 001-999
    ```
  </sot_compliance_details>


  <!-- ======================================================
       6.1 歧义处理流程 (Ambiguity Handling) [v2.5 新增]
       来源: MASTER.md v4.4 §7 AH-05
  ====================================================== -->
  <ambiguity_handling>
    **歧义处理流程 (AH-05)** - 遇到歧义必须停止并询问

    **Step 1: 检测到歧义** → 立即 BLOCKING
    歧义类型包括:
    - 状态值不在 8 状态机白名单中
    - 角色值不在 7 角色白名单中
    - 字段值不在 DATA_SCHEMA.md 中
    - 规则编号不在 BUSINESS_RULES.md 中
    - API 端点不在 API_SOT.md 中
    - 错误码前缀不在 16 前缀白名单中

    **Step 2: 停止当前操作**
    - 不继续生成代码
    - 不尝试自动猜测
    - 不假设默认值

    **Step 3: 生成歧义报告**
    ```json
    {
      "type": "STATE_AMBIGUITY | ROLE_AMBIGUITY | FIELD_AMBIGUITY | RULE_AMBIGUITY | API_AMBIGUITY | ERROR_AMBIGUITY",
      "content": "发现状态 'pending_review' 不在 8 状态机中",
      "options": [
        "使用 'trend_pending' (趋势待检查)",
        "使用 'final_pending' (最终待确认)",
        "新增状态到 STATE_MACHINE.md (需 RFC)"
      ],
      "sot_ref": "STATE_MACHINE.md v2.6 §2"
    }
    ```

    **Step 4: 等待用户确认**
    - 输出歧义报告给用户
    - 等待用户选择选项或提供新指示
    - 不自行做决定

    **Step 5: 继续执行**
    - 按用户确认的方案继续
    - 记录歧义解决过程

    **错误码**: AH-05-AMBIGUITY (BLOCKING)
  </ambiguity_handling>


  <!-- ======================================================
       6.2 Phase 1 行为约束验证 (Phase 1 Constraints) [v2.5 新增]
       来源: MASTER.md v4.4 §7 AH-04
  ====================================================== -->
  <phase1_constraints>
    **Phase 1 行为约束验证 (AH-04)** - 必须遵循 Phase 1 软性原则

    **允许的行为** ✅:
    | 行为 | 说明 | 代码模式示例 |
    |------|------|-------------|
    | 记录 | 记录事件到日志 | `logger.info("CPL 超标")` |
    | 提示 | 返回警告信息 | `warnings: ["CPL 超标 30%"]` |
    | 高亮 | 前端显示标记 | `trend_flag: true` |
    | 统计 | 数据汇总分析 | `abnormal_count: 5` |

    **禁止的行为** ❌ (会触发 AH-02 违规):
    | 行为 | 说明 | 检测模式 |
    |------|------|---------|
    | 阻断 | 拒绝请求 | `raise HTTPException(4xx, ...)` |
    | 拒绝 | 返回错误 | `auto_reject`, `deny_request` |
    | 暂停 | 暂停项目 | `.suspend()`, `status = 'suspended'` |
    | 冻结 | 冻结账户 | `.freeze()`, `.disable()` |
    | 自动拒绝 | 自动驳回 | `auto_reject = True` |
    | 自动批准 | 自动通过 | `auto_approve = True` |

    **检测正则模式**:
    ```python
    FORBIDDEN_PATTERNS = [
        r'raise\s+HTTPException\s*\(\s*4\d\d',  # HTTP 4xx 错误
        r'raise\s+.*Error.*reject',              # 拒绝错误
        r'\.suspend\s*\(\s*\)',                  # 暂停方法
        r'\.freeze\s*\(\s*\)',                   # 冻结方法
        r'\.disable\s*\(\s*\)',                  # 禁用方法
        r'auto_approve\s*=\s*True',              # 自动批准
        r'auto_reject\s*=\s*True',               # 自动拒绝
        r'status\s*=\s*[\'"]suspended[\'"]',     # 设置暂停状态
        r'status\s*=\s*[\'"]frozen[\'"]',        # 设置冻结状态
    ]
    ```

    **验证规则**:
    1. 扫描生成的代码，检测是否包含禁止模式
    2. 如检测到 → 触发 AH-02 违规 (BLOCKING)
    3. 建议修改为仅记录和提示的方式

    **错误码**: AH-02-PHASE1-VIOLATION (BLOCKING)

    **修复建议**:
    ```python
    # 错误做法 (会触发 AH-02)
    if over_budget:
        raise HTTPException(400, "超预算，拒绝操作")

    # 正确做法 (Phase 1 合规)
    if over_budget:
        logger.warning(f"超预算警告: {amount}")
        return {"status": "ok", "warnings": ["超预算警告，请确认"]}
    ```
  </phase1_constraints>


  <!-- ======================================================
       6.3 P0 功能测试覆盖要求 (P0 Test Coverage Requirements) [v2.3 新增]
  ====================================================== -->
  <p0_test_coverage>
    **核心原则**: P0 级别的功能必须有测试覆盖，否则代码不可合并。

    **P0 功能定义** (必须测试):
    ```yaml
    p0_features:
      # 状态机相关
      - 状态转换函数 (transition_*)
      - 状态验证函数 (validate_status)
      - 状态守卫函数 (guard_*)

      # 财务相关
      - Ledger 写入函数 (create_ledger_entry)
      - 冲正函数 (reverse_*, create_reversal)
      - 余额计算函数 (calculate_balance)
      - 期间锁检查函数 (check_period_lock, is_period_locked)

      # 权限相关
      - 角色验证函数 (check_role, require_role)
      - 模块边界检查函数 (check_module_boundary)
      - 数据隔离函数 (filter_by_owner)

      # 业务规则相关
      - BR-XXX 规则实现函数
      - 金额计算函数 (calculate_*)
      - 日期验证函数 (validate_date_*)
    ```

    **测试要求**:
    | 功能类型 | 最低覆盖率 | 测试类型 |
    |---------|-----------|---------|
    | 状态转换 | 100% 路径 | 单元测试 + 边界测试 |
    | 财务计算 | 100% 分支 | 单元测试 + 精度测试 |
    | 权限检查 | 100% 角色 | 单元测试 + 集成测试 |
    | 业务规则 | ≥90% 行 | 单元测试 + 场景测试 |

    **测试命名规范**:
    ```python
    # 正向测试
    def test_{function}_success_{scenario}():
        ...

    # 负向测试
    def test_{function}_fails_when_{condition}():
        ...

    # 边界测试
    def test_{function}_boundary_{edge_case}():
        ...

    # 示例
    def test_transition_to_confirmed_success_with_valid_status():
        ...

    def test_create_ledger_entry_fails_when_period_locked():
        ...

    def test_calculate_balance_boundary_with_zero_amount():
        ...
    ```

    **验证错误码**:
    - TST-007: P0 功能缺少测试覆盖
    - TST-008: P0 功能测试覆盖率不足
    - TST-009: P0 功能缺少边界测试
  </p0_test_coverage>


  <!-- ======================================================
       7. 禁止行为 (Forbidden Actions)
  ====================================================== -->
  <forbidden_actions>
    <forbidden id="VER-001">
      <action>忽略幻觉检测结果</action>
      <correct_action>必须修复所有 HALL-xxx 错误</correct_action>
    </forbidden>

    <forbidden id="VER-002">
      <action>使用已废弃的状态/角色</action>
      <correct_action>使用 SoT 定义的合法值</correct_action>
    </forbidden>

    <forbidden id="VER-003">
      <action>自动修复超过 3 次仍失败时继续</action>
      <correct_action>返回失败报告，需要人工介入</correct_action>
    </forbidden>

    <forbidden id="VER-004">
      <action>修改测试以通过验证</action>
      <correct_action>修复代码，而非修改测试</correct_action>
    </forbidden>

    <forbidden id="VER-005">
      <action>直接修改 balance 字段</action>
      <correct_action>通过 ledger_entries 记录</correct_action>
    </forbidden>
  </forbidden_actions>


  <!-- ======================================================
       8. 版本记录 (Version Notes)
  ====================================================== -->
  <VERSION_NOTES>
    ### v2.5 (2025-12-24) - 防幻觉规则集成版
    - 新增歧义处理流程 (ambiguity_handling) - AH-05
    - 新增 Phase 1 行为约束验证 (phase1_constraints) - AH-04
    - 更新角色白名单为 7 角色 (MASTER.md v4.4 §2.4)
    - 新增禁止模式正则检测 (FORBIDDEN_PATTERNS)
    - 新增错误码: AH-05-AMBIGUITY, AH-02-PHASE1-VIOLATION

    ### v2.3 (2025-12-22) - P2 优化版
    - 新增 P0 功能测试覆盖要求 (p0_test_coverage)
    - 新增 TST-007~009 错误码 (P0 测试覆盖)
    - 新增 SUP-007 错误码 (非标准来源标注)
    - 扩展错误码前缀 (16 个: 通用 6 + 模块 10)
    - 新增配置项: enable_p0_test_check, p0_coverage_threshold

    ### v2.2 (2025-12-22)
    - 新增 Layer 6: HallucinationSuppressor (幻觉抑制最终确认)
    - 新增 SUP-001~006 错误码
    - 8 层验证流水线完整实现

    ### v2.1 (2025-12-22)
    - 新增 Layer 0: ModuleBoundaryVerifier (模块边界验证)
    - 新增 Layer 3.5: FinanceRulesVerifier (财务规则验证)
    - 新增 FIN-001~007 错误码
    - 更新角色/状态白名单为 frozenset 格式

    ### v2.0 (2025-12-18)
    - 新增幻觉检测层 (HallucinationDetector)
      - 检测不存在的 API/函数/模块
      - 验证第三方库导入
      - 检查项目内部引用
    - 增强 AST 验证
      - 支持 Python 和 TypeScript
      - 结构完整性检查
      - 括号/缩进/引号匹配
    - 增强 SoT 合规检查
      - 日报 8 状态机验证
      - 充值/转账状态机验证
      - 角色/错误码验证
      - balance 直接修改检测
    - 新增集成验证层
      - 导入路径验证
      - 循环导入检测
      - 第三方依赖检查
    - 新增测试验证层
      - 测试文件存在性检查
      - 测试覆盖率分析
      - 测试质量检查
    - 统一错误码体系
    - 支持多种报告格式 (text/json/markdown)

    ### v1.0 (2025-12-17)
    - 初始版本
    - 四维验证: 类型/Lint/SoT合规/测试
    - 借鉴 mypy 的类型检查架构
    - 借鉴 ruff 的快速 Linting 和自动修复
    - 自研 SoT 合规检查器
    - 最多 3 次自动修复迭代
  </VERSION_NOTES>

</skill>
