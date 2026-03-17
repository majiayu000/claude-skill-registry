---
name: ai-ad-flow-orchestrator
version: "1.1"
status: active
layer: skill
owner: wade
last_reviewed: 2025-12-07

sot_dependencies:
  required:
    - docs/sot/DEV_FLOW_SOT_v1.0.md  # v1.1 (7 Flow 架构)
    - docs/sot/STATE_MACHINE.md
    - docs/sot/DATA_SCHEMA.md
    - docs/sot/BUSINESS_RULES.md
    - docs/sot/API_SOT.md
  optional:
    - docs/sot/ERROR_CODES_SOT.md

sub_skills:
  - ai-ad-spec-governor    # /sot-check
  - ai-ad-be-gen           # /gen be
  - ai-ad-fe-gen           # /gen fe
  - ai-ad-test-gen         # /gen test
  - ai-master-architect    # /review
  - ai-doc-system-auditor  # /doc

enhancement:
  enabled: true
  superclaude_patterns:
    - task_breakdown       # 任务分解
    - step_implementation  # 步骤化执行
    - analysis_pattern     # 分析审计
  internal_workflow: true
  sot_priority: true

baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, DEV_FLOW_SOT_v1.1, SoT Freeze v2.6
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-flow-orchestrator</name>
  <version>1.1</version>
  <domain>AI_AD_SYSTEM / 开发流程编排</domain>
  <profile>Flow-Orchestrator / Multi-skill / Safe</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 核心使命（Mission）
  ====================================================== -->
  <mission>
    根据用户任务描述，自动识别适用的开发流程 (Flow)，
    输出完整的命令执行序列: /sot-check → /gen → /review → /doc

    目标：
    - 任务开始前必须进行 SoT 对齐检查
    - 代码生成必须受 SoT 约束
    - 生成的代码必须经过审查
    - 流程结束时必须更新相关文档

    SoT 基准: DEV_FLOW_SOT_v1.1 (7 大 Flow)
  </mission>


  <!-- ======================================================
       1. 输入契约（Input Contract）
  ====================================================== -->
  <input_contract>
    最小输入：
    {
      task: string,           // 任务描述，如 "实现充值审批功能"
    }

    可选输入：
    {
      flow_type?: "BE_DEV_FLOW" | "FE_DEV_FLOW" | "API_FIX_FLOW" | "TEST_HARDEN_FLOW" | "DOC_FREEZE_FLOW" | "REFACTOR_FLOW" | "FULL_FLOW",
      target_module?: string,  // 目标模块名，如 "topup", "reconciliation"
      skip_steps?: string[],   // 跳过的步骤，如 ["doc"]
    }

    命令映射 (DEV_FLOW_SOT §11):
    - /dev-flow be    → BE_DEV_FLOW
    - /dev-flow fe    → FE_DEV_FLOW
    - /dev-flow fix   → API_FIX_FLOW
    - /dev-flow test  → TEST_HARDEN_FLOW
    - /dev-flow doc   → DOC_FREEZE_FLOW
    - /dev-flow full  → FULL_FLOW
    - /dev-flow refactor → REFACTOR_FLOW

    若 task 缺失 → 输出 <halt>Missing: task description</halt> 并停止。
  </input_contract>


  <!-- ======================================================
       2. 输出契约（Output Contract）
  ====================================================== -->
  <output_contract>
    成功输出：
    {
      flow_type: string,           // 识别的流程类型
      flow_name: string,           // 流程中文名
      command: string,             // 对应的 /dev-flow 命令
      command_sequence: [          // 命令执行序列
        { step: number, command: string, purpose: string, expected_output: string }
      ],
      local_test_commands: string[], // 本地测试命令
      freeze_checklist: string[],    // 冻结检查项
    }

    失败输出：
    {
      error: string,
      suggestion: string,
    }
  </output_contract>


  <!-- ======================================================
       3. Flow 识别规则 (基于 DEV_FLOW_SOT §3)
  ====================================================== -->
  <flow_detection>
    基于任务描述自动识别 Flow 类型 (7 大 Flow):

    <!-- BE_DEV_FLOW 触发关键词 -->
    <flow id="BE_DEV_FLOW" command="/dev-flow be">
      <triggers>
        - 新增后端
        - 新增 API
        - 新增接口
        - 实现 service
        - 实现服务
        - 后端功能
        - 新增模块
        - 状态机流转
        - 账本分录
        - 后端开发
      </triggers>
      <complexity>高</complexity>
    </flow>

    <!-- FE_DEV_FLOW 触发关键词 -->
    <flow id="FE_DEV_FLOW" command="/dev-flow fe">
      <triggers>
        - 新增页面
        - 新增组件
        - 前端功能
        - UI 开发
        - React 组件
        - 表单页面
        - 列表页面
        - 前端开发
      </triggers>
      <complexity>中</complexity>
    </flow>

    <!-- API_FIX_FLOW 触发关键词 -->
    <flow id="API_FIX_FLOW" command="/dev-flow fix">
      <triggers>
        - 修复接口
        - 修复 API
        - Bug 修复
        - 接口问题
        - 返回值错误
        - 参数校验
        - 接口报错
        - fix bug
      </triggers>
      <complexity>低</complexity>
    </flow>

    <!-- TEST_HARDEN_FLOW 触发关键词 -->
    <flow id="TEST_HARDEN_FLOW" command="/dev-flow test">
      <triggers>
        - 补充测试
        - 测试覆盖
        - 回归测试
        - 边界测试
        - 测试加固
        - 单元测试
        - 测试补齐
      </triggers>
      <complexity>中</complexity>
    </flow>

    <!-- DOC_FREEZE_FLOW 触发关键词 -->
    <flow id="DOC_FREEZE_FLOW" command="/dev-flow doc">
      <triggers>
        - 文档审计
        - 文档冻结
        - 文档治理
        - 更新文档
        - SoT 更新
        - 文档检查
      </triggers>
      <complexity>低</complexity>
    </flow>

    <!-- REFACTOR_FLOW 触发关键词 -->
    <flow id="REFACTOR_FLOW" command="/dev-flow refactor">
      <triggers>
        - 代码重构
        - 重构代码
        - 优化代码
        - 代码优化
        - 去重复
        - 提取公共
        - 性能优化
        - 技术债
        - refactor
      </triggers>
      <complexity>中</complexity>
      <constraints>
        - 不得改变业务行为
        - 不得修改 SoT 定义
        - 输入/输出契约保持不变
      </constraints>
    </flow>

    <!-- FULL_FLOW 触发关键词 -->
    <flow id="FULL_FLOW" command="/dev-flow full">
      <triggers>
        - 完整功能
        - 端到端
        - 全栈开发
        - 前后端
        - MVP
        - 新模块开发
        - 完整模块
      </triggers>
      <complexity>高</complexity>
      <composition>BE_DEV_FLOW → FE_DEV_FLOW → TEST_HARDEN_FLOW → DOC_FREEZE_FLOW</composition>
    </flow>

    若无法识别 → 默认 BE_DEV_FLOW 并提示用户确认。
  </flow_detection>


  <!-- ======================================================
       4. 命令序列模板 (基于 DEV_FLOW_SOT §4-10)
  ====================================================== -->
  <command_templates>

    <!-- BE_DEV_FLOW 命令序列 (DEV_FLOW_SOT §4) -->
    <template flow="BE_DEV_FLOW">
      <step n="1">
        <command>/sot-check docs/sot/</command>
        <purpose>SoT 对齐 - 确认相关规则</purpose>
        <expected>SoT 规则清单 + 依赖关系</expected>
      </step>
      <step n="2">
        <command>/gen be "生成 {module} 的 Pydantic Schema"</command>
        <purpose>Schema 层生成</purpose>
        <expected>backend/schemas/{module}.py</expected>
      </step>
      <step n="3">
        <command>/gen be "实现 {module} 的 Service 层"</command>
        <purpose>Service 层生成</purpose>
        <expected>backend/services/{module}_service.py</expected>
      </step>
      <step n="4">
        <command>/gen be "实现 {module} 的 Router 层"</command>
        <purpose>Router 层生成</purpose>
        <expected>backend/routers/{module}.py</expected>
      </step>
      <step n="5">
        <command>/gen test "为 {module} 生成状态机测试 + API 测试"</command>
        <purpose>测试生成</purpose>
        <expected>backend/tests/services/test_{module}_service.py, backend/tests/api/test_{module}_api.py</expected>
      </step>
      <step n="6">
        <command>/review backend/services/{module}_service.py</command>
        <purpose>代码审查 (Service 层)</purpose>
        <expected>审查报告 + 修复建议</expected>
      </step>
      <local_test>
        pytest backend/tests/services/test_{module}_service.py -v
        pytest backend/tests/api/test_{module}_api.py -v
        mypy backend/services/{module}_service.py
      </local_test>
    </template>

    <!-- FE_DEV_FLOW 命令序列 (DEV_FLOW_SOT §5) -->
    <template flow="FE_DEV_FLOW">
      <step n="1">
        <command>/sot-check docs/sot/API_SOT.md</command>
        <purpose>API 契约确认</purpose>
        <expected>相关 API 端点列表 + 数据结构</expected>
      </step>
      <step n="2">
        <command>/gen fe "生成 {module} 的 API Client"</command>
        <purpose>API Client 生成</purpose>
        <expected>frontend/src/lib/api/{module}.ts</expected>
      </step>
      <step n="3">
        <command>/gen fe "创建 {component} 页面/组件"</command>
        <purpose>组件/页面生成</purpose>
        <expected>frontend/src/modules/{module}/</expected>
      </step>
      <step n="4">
        <command>/gen test "为 {component} 生成前端测试"</command>
        <purpose>测试生成</purpose>
        <expected>frontend/tests/{module}/</expected>
      </step>
      <step n="5">
        <command>/review frontend/src/modules/{module}/</command>
        <purpose>组件审查</purpose>
        <expected>审查报告</expected>
      </step>
      <local_test>
        cd frontend && npm run type-check
        npm run lint
        npm run test -- --testPathPattern={module}
      </local_test>
    </template>

    <!-- API_FIX_FLOW 命令序列 (DEV_FLOW_SOT §6) -->
    <template flow="API_FIX_FLOW">
      <step n="1">
        <command>/sot-check {target_file}</command>
        <purpose>问题定位 - 对比 API_SOT.md 识别偏差点</purpose>
        <expected>问题清单 + SoT 规则引用</expected>
      </step>
      <step n="2">
        <command>/gen be "修复 {issue_description}"</command>
        <purpose>修复生成</purpose>
        <expected>修改后的 Router/Service 代码</expected>
      </step>
      <step n="3">
        <command>/gen test "为 {target_file} 生成回归测试"</command>
        <purpose>回归测试</purpose>
        <expected>回归测试用例</expected>
      </step>
      <step n="4">
        <command>/review {target_file}</command>
        <purpose>验证审查</purpose>
        <expected>审查报告</expected>
      </step>
      <local_test>
        pytest backend/tests/api/test_{module}_api.py::{test_case} -v
      </local_test>
    </template>

    <!-- TEST_HARDEN_FLOW 命令序列 (DEV_FLOW_SOT §7) -->
    <template flow="TEST_HARDEN_FLOW">
      <step n="1">
        <command>/sot-check backend/tests/</command>
        <purpose>覆盖分析</purpose>
        <expected>测试缺口清单</expected>
      </step>
      <step n="2">
        <command>/gen test "补齐 {entity} 状态机测试"</command>
        <purpose>状态机测试</purpose>
        <expected>状态机测试用例</expected>
      </step>
      <step n="3">
        <command>/gen test "补齐 {module} 边界条件测试"</command>
        <purpose>边界测试</purpose>
        <expected>边界测试用例</expected>
      </step>
      <step n="4">
        <command>/review backend/tests/</command>
        <purpose>覆盖验证</purpose>
        <expected>测试审查报告</expected>
      </step>
      <local_test>
        pytest backend/tests/ -v
        pytest backend/tests/ --cov=backend --cov-report=html
      </local_test>
    </template>

    <!-- DOC_FREEZE_FLOW 命令序列 (DEV_FLOW_SOT §8) -->
    <template flow="DOC_FREEZE_FLOW">
      <step n="1">
        <command>/doc docs/</command>
        <purpose>文档审计</purpose>
        <expected>P0/P1/P2 问题清单</expected>
      </step>
      <step n="2">
        <command>/sot-check docs/sot/</command>
        <purpose>SoT 一致性检查</purpose>
        <expected>SoT 一致性报告</expected>
      </step>
      <step n="3">
        <command>/doc --freeze {module}</command>
        <purpose>Freeze 报告生成</purpose>
        <expected>docs/reports/{module}_FREEZE_REPORT.md</expected>
      </step>
      <local_test>
        # 无代码测试，人工确认文档准确性
      </local_test>
    </template>

    <!-- REFACTOR_FLOW 命令序列 (DEV_FLOW_SOT §9) -->
    <template flow="REFACTOR_FLOW">
      <constraints>
        ⚠️ 不得改变业务行为
        ⚠️ 不得修改 SoT 定义
        ⚠️ 输入/输出契约保持不变
      </constraints>
      <entry_conditions>
        - 测试覆盖率 >= 80%
        - CI 通过
        - SoT 文档 frozen
        - 无 P0 级 Bug
      </entry_conditions>
      <step n="1">
        <command>pytest backend/tests/ --tb=short > refactor_baseline.txt</command>
        <purpose>快照基线</purpose>
        <expected>测试快照 + API 响应样本</expected>
      </step>
      <step n="2">
        <command>/sot-check {target_files}</command>
        <purpose>SoT 对齐检查</purpose>
        <expected>SoT 合规报告 + 技术债清单</expected>
      </step>
      <step n="3">
        <command>/review {target_files}</command>
        <purpose>代码分析</purpose>
        <expected>重构建议清单</expected>
      </step>
      <step n="4">
        <command>/gen be "重构 {module} 的 {重构目标}"</command>
        <purpose>重构实施</purpose>
        <expected>重构后的代码</expected>
      </step>
      <step n="5">
        <command>/sot-check {target_files}</command>
        <purpose>等价验证</purpose>
        <expected>SoT 合规 + 测试通过</expected>
      </step>
      <local_test>
        pytest backend/tests/ -v > refactor_after.txt
        diff refactor_baseline.txt refactor_after.txt
      </local_test>
      <exit_conditions>
        - 所有现有测试通过
        - 行为等价 (diff 无差异)
        - /sot-check 无新增 P0/P1
      </exit_conditions>
    </template>

    <!-- FULL_FLOW 命令序列 (DEV_FLOW_SOT §10) -->
    <template flow="FULL_FLOW">
      <composition>
        Phase 1: BE_DEV_FLOW (完整 6 步)
        Phase 2: FE_DEV_FLOW (完整 5 步)
        Phase 3: TEST_HARDEN_FLOW (完整 4 步)
        Phase 4: DOC_FREEZE_FLOW (完整 3 步)
      </composition>
      <step n="1" phase="backend">
        <command>执行 BE_DEV_FLOW 完整流程</command>
        <purpose>后端开发</purpose>
        <expected>Schema + Service + Router + 后端测试</expected>
      </step>
      <step n="2" phase="frontend">
        <command>执行 FE_DEV_FLOW 完整流程</command>
        <purpose>前端开发</purpose>
        <expected>API Client + 页面/组件 + 前端测试</expected>
      </step>
      <step n="3" phase="test">
        <command>执行 TEST_HARDEN_FLOW 完整流程</command>
        <purpose>测试加固</purpose>
        <expected>状态机测试 + 边界测试 + 覆盖率报告</expected>
      </step>
      <step n="4" phase="doc">
        <command>执行 DOC_FREEZE_FLOW 完整流程</command>
        <purpose>文档冻结</purpose>
        <expected>文档审计报告 + Freeze 报告</expected>
      </step>
      <local_test>
        # 后端测试
        pytest backend/tests/ -v

        # 前端测试
        cd frontend && npm run test

        # 覆盖率
        pytest backend/tests/ --cov=backend --cov-report=html
      </local_test>
    </template>

  </command_templates>


  <!-- ======================================================
       5. 执行流程
  ====================================================== -->
  <execution_workflow>
    Phase 1: 任务分析
    ─────────────────
    1. 接收用户任务描述
    2. 提取关键词，匹配 Flow 类型 (7 大 Flow)
    3. 若用户指定 flow_type，使用指定值
    4. 输出 Flow 类型确认 + 对应 /dev-flow 命令

    Phase 2: 命令序列生成
    ─────────────────────
    1. 加载对应 Flow 模板 (参考 DEV_FLOW_SOT)
    2. 替换 {module}, {component} 等占位符
    3. 若用户指定 skip_steps，移除对应步骤
    4. 输出完整命令序列

    Phase 3: 执行指导
    ─────────────────
    1. 输出命令执行顺序
    2. 提示每步的预期产出
    3. 提供本地测试命令
    4. 输出冻结检查清单
  </execution_workflow>


  <!-- ======================================================
       6. 输出格式
  ====================================================== -->
  <output_format>
    ## Flow Orchestration Report

    ### 任务识别
    - **任务**: {task}
    - **Flow 类型**: {flow_type}
    - **Flow 名称**: {flow_name}
    - **命令**: {command}
    - **复杂度**: {complexity}
    - **SoT 基准**: DEV_FLOW_SOT v1.1

    ### 命令执行序列

    | Step | 命令 | 目的 | 预期产出 |
    |------|------|------|----------|
    | 1    | ...  | ...  | ...      |

    ### 执行提示

    ```
    ⚠️ 命令不支持管道串联，请逐条执行：

    Step 1: /sot-check ...
    → 确认 SoT 规则后继续

    Step 2: /gen be ...
    → 检查生成代码后继续

    ...
    ```

    ### 本地测试

    ```bash
    # 代码测试
    pytest backend/tests/ -v

    # 类型检查
    mypy backend/services/{module}_service.py
    ```

    ### 冻结检查清单

    - [ ] 所有 SoT 规则已遵循
    - [ ] 代码审查通过
    - [ ] 本地测试通过
    - [ ] 相关文档已更新
  </output_format>


  <!-- ======================================================
       7. 错误处理
  ====================================================== -->
  <error_handling>
    <error code="FLOW_UNKNOWN">
      <condition>无法识别 Flow 类型</condition>
      <action>默认 BE_DEV_FLOW，提示用户确认</action>
    </error>
    <error code="MODULE_MISSING">
      <condition>任务未指明目标模块</condition>
      <action>询问用户补充模块名</action>
    </error>
    <error code="SOT_VIOLATION">
      <condition>/sot-check 发现 P0 违规</condition>
      <action>中断流程，输出违规详情，等待修复</action>
    </error>
    <error code="REFACTOR_BEHAVIOR_CHANGE">
      <condition>REFACTOR_FLOW 检测到业务行为变化</condition>
      <action>中断流程，提示用户确认是否改为 BE_DEV_FLOW</action>
    </error>
  </error_handling>


  <!-- ======================================================
       8. 调用示例
  ====================================================== -->
  <examples>
    <example name="后端新功能">
      <input>
        task: "实现充值审批功能"
      </input>
      <output>
        flow_type: BE_DEV_FLOW
        command: /dev-flow be 实现充值审批功能
        command_sequence:
          1. /sot-check docs/sot/
          2. /gen be "生成 topup_approval 的 Pydantic Schema"
          3. /gen be "实现 topup_approval 的 Service 层"
          4. /gen be "实现 topup_approval 的 Router 层"
          5. /gen test "为 topup_approval 生成状态机测试 + API 测试"
          6. /review backend/services/topup_approval_service.py
      </output>
    </example>

    <example name="接口修复">
      <input>
        task: "修复日报导出接口返回空数据问题"
      </input>
      <output>
        flow_type: API_FIX_FLOW
        command: /dev-flow fix 修复日报导出接口返回空数据问题
        command_sequence:
          1. /sot-check backend/routers/daily_report.py
          2. /gen be "修复日报导出接口返回空数据问题"
          3. /gen test "为日报导出接口生成回归测试"
          4. /review backend/routers/daily_report.py
      </output>
    </example>

    <example name="代码重构">
      <input>
        task: "重构 topup_service.py 的审批逻辑"
      </input>
      <output>
        flow_type: REFACTOR_FLOW
        command: /dev-flow refactor 重构 topup_service.py 的审批逻辑
        constraints:
          - 不得改变业务行为
          - 不得修改 SoT 定义
        command_sequence:
          1. pytest backend/tests/ --tb=short > refactor_baseline.txt
          2. /sot-check backend/services/topup_service.py
          3. /review backend/services/topup_service.py
          4. /gen be "重构 topup_service.py 的审批逻辑"
          5. /sot-check backend/services/topup_service.py
          6. pytest + diff 验证
      </output>
    </example>

    <example name="完整功能开发">
      <input>
        task: "实现对账模块"
      </input>
      <output>
        flow_type: FULL_FLOW
        command: /dev-flow full 实现对账模块
        phases:
          Phase 1: BE_DEV_FLOW (后端)
          Phase 2: FE_DEV_FLOW (前端)
          Phase 3: TEST_HARDEN_FLOW (测试加固)
          Phase 4: DOC_FREEZE_FLOW (文档冻结)
      </output>
    </example>
  </examples>

</skill>
