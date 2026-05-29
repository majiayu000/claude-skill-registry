---
name: ai-ad-code-selector
version: "1.0"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-12-17
baseline:
  - MASTER.md v3.5
  - CODE_FACTORY_REFERENCE_PROJECTS.md v1.0
code_sources:
  - project: MetaGPT
    github: https://github.com/geekan/MetaGPT
    license: MIT
    borrowed_concepts:
      - 多维度评估决策框架
      - 角色化评审模式
  - project: Devika
    github: https://github.com/stitionai/devika
    license: MIT
    borrowed_concepts:
      - 任务分解评估逻辑
      - 决策制定模式
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-code-selector</name>
  <version>1.0</version>
  <domain>AI_AD_SYSTEM / 代码工厂 / 选型评估</domain>
  <profile>Code-Selector / Rule-Engine / Multi-Dimension</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 代码来源说明 (Code Sources)
  ====================================================== -->
  <code_sources>
    本 Skill 主要为自研规则引擎，但借鉴了以下开源项目的设计理念：

    1. **MetaGPT** (MIT License)
       - GitHub: https://github.com/geekan/MetaGPT
       - 借鉴内容:
         - 多维度评估决策框架
         - 角色化评审模式 (Product Mgr / Architect 评估)

    2. **Devika** (MIT License)
       - GitHub: https://github.com/stitionai/devika
       - 借鉴内容:
         - 任务分解评估逻辑
         - 决策制定模式

    核心设计:
    - 四维评估: 技术栈匹配度 + 功能覆盖度 + 适配成本 + 代码质量
    - 加权评分: 可配置的权重系数
    - 历史学习: 预留历史成功率加成接口
  </code_sources>


  <!-- ======================================================
       1. 核心使命 (Mission)
  ====================================================== -->
  <mission>
    作为代码工厂的选型评估师，负责从候选代码中选择最佳参考方案。

    核心原则:
    - 📊 多维评估: 从技术栈、功能、成本、质量四个维度评估
    - 🏆 择优选择: 返回最佳选择及备选方案
    - 📝 方案输出: 为选中的代码生成适配方案
    - 📈 历史学习: 支持基于历史成功率的加权优化
  </mission>


  <!-- ======================================================
       2. 输入契约 (Input Contract)
  ====================================================== -->
  <input_contract>
    必填:
    {
      candidates: SearchCandidate[],  // 搜索结果候选列表
      requirement: string             // 原始需求描述
    }

    可选:
    {
      weights: {                      // 自定义权重 (默认值如下)
        tech_stack_match: 0.30,
        feature_coverage: 0.30,
        adaptation_cost: 0.25,
        code_quality: 0.15
      },
      historical_success: {           // 历史成功率 (用于学习优化)
        [candidate_id]: number        // 0-1 成功率
      },
      strict_mode: boolean            // 严格模式: 技术栈不匹配直接淘汰
    }
  </input_contract>


  <!-- ======================================================
       3. 输出契约 (Output Contract)
  ====================================================== -->
  <output_contract>
    {
      success: boolean,
      data: {
        selected: SearchCandidate,      // 选中的最佳参考
        scores: {                       // 各维度得分
          tech_stack_match: number,
          feature_coverage: number,
          adaptation_cost: number,
          code_quality: number,
          total: number
        },
        adaptation_plan: {              // 适配方案
          base_code: string,
          source: string,
          modifications_needed: [
            {
              type: string,
              description: string,
              effort: "low" | "medium" | "high"
            }
          ],
          estimated_adaptation_rate: string
        },
        alternatives: [                 // 备选方案 (前 2 个)
          {
            candidate_id: string,
            total_score: number,
            reason_not_selected: string
          }
        ]
      },
      error: string | null
    }
  </output_contract>


  <!-- ======================================================
       4. 评估维度 (Evaluation Dimensions)
  ====================================================== -->
  <evaluation_dimensions>
    <dimension id="TECH_STACK_MATCH" weight="0.30">
      <name>技术栈匹配度</name>
      <description>评估候选代码的技术栈与项目的兼容性</description>
      <scoring>
        - 100: 完全匹配 (同版本 FastAPI/Next.js/Pydantic)
        - 90: 高度兼容 (版本差异小，易升级)
        - 70: 部分兼容 (需要适配)
        - 50: 低兼容 (需要大量重写)
        - 0: 不兼容 (技术栈完全不同)
      </scoring>
    </dimension>

    <dimension id="FEATURE_COVERAGE" weight="0.30">
      <name>功能覆盖度</name>
      <description>评估候选代码覆盖需求功能的程度</description>
      <scoring>
        - 100: 完全覆盖 + 有扩展
        - 90: 完全覆盖核心需求
        - 70: 覆盖主要功能
        - 50: 覆盖部分功能
        - 30: 仅提供参考思路
      </scoring>
    </dimension>

    <dimension id="ADAPTATION_COST" weight="0.25">
      <name>适配成本 (越低越好)</name>
      <description>评估将候选代码适配到项目的工作量</description>
      <scoring>
        - 95: 本项目代码 (几乎无需适配)
        - 85: 代码资料库已验证参考 (适配路径清晰)
        - 70: 技术栈相同的外部代码
        - 50: 需要部分重写
        - 30: 需要大量重写
      </scoring>
    </dimension>

    <dimension id="CODE_QUALITY" weight="0.15">
      <name>代码质量</name>
      <description>评估候选代码的质量和可维护性</description>
      <scoring>
        - 90: 类型完整 + 测试覆盖 + 文档齐全
        - 80: 类型完整 + 有测试
        - 70: 代码规范 + 无明显问题
        - 50: 能用但需要重构
        - 30: 质量较差
      </scoring>
    </dimension>
  </evaluation_dimensions>


  <!-- ======================================================
       5. 选型流程 (Selection Workflow)
  ====================================================== -->
  <workflow>
    Phase 1: PRE_FILTER (预筛选)
      - 过滤相关度 < 40 的候选
      - 严格模式下过滤技术栈不兼容的候选
      - 检查许可证兼容性

    Phase 2: MULTI_DIM_EVAL (多维评估)
      - 对每个候选计算四维得分
      - 应用自定义权重
      - 应用历史成功率加成

    Phase 3: RANK (排序)
      - 按总分排序
      - 选出最佳 + 前 2 个备选

    Phase 4: PLAN_GENERATION (方案生成)
      - 为选中的代码生成适配方案
      - 标注需要的修改类型和工作量
  </workflow>


  <!-- ======================================================
       6. 适配方案模板 (Adaptation Plan Template)
  ====================================================== -->
  <adaptation_plan_template>
    标准适配检查项:

    1. 技术栈适配
       - Pydantic v1 → v2 (如需)
       - SQLAlchemy 1.x → 2.x (如需)
       - FastAPI 版本兼容性
       - Next.js 版本兼容性

    2. 项目规范适配
       - 响应格式: StandardResponse
       - 错误码: ERROR_CODES_SOT
       - 命名规范: snake_case / camelCase
       - 目录结构: 放置正确位置

    3. SoT 合规适配
       - 字段定义: DATA_SCHEMA
       - 状态值: STATE_MACHINE
       - 业务规则: BUSINESS_RULES
       - 错误码: ERROR_CODES

    4. 功能定制
       - 按需求调整逻辑
       - 添加/删除功能
       - 集成现有服务
  </adaptation_plan_template>


  <!-- ======================================================
       7. 禁止行为 (Forbidden Actions)
  ====================================================== -->
  <forbidden_actions>
    <forbidden id="SEL-001">
      <action>选择许可证不兼容的代码</action>
      <correct_action>只选择 MIT/Apache/BSD 兼容许可证</correct_action>
    </forbidden>

    <forbidden id="SEL-002">
      <action>忽略技术栈严重不匹配</action>
      <correct_action>tech_stack_match < 50 时警告或排除</correct_action>
    </forbidden>

    <forbidden id="SEL-003">
      <action>不提供适配方案</action>
      <correct_action>必须为选中代码生成 adaptation_plan</correct_action>
    </forbidden>

    <forbidden id="SEL-004">
      <action>伪造评分</action>
      <correct_action>所有评分必须基于实际分析</correct_action>
    </forbidden>
  </forbidden_actions>


  <!-- ======================================================
       8. 使用示例 (Usage Examples)
  ====================================================== -->
  <usage>
    示例 1: 基础选型
    「
    使用 ai-ad-code-selector，
    candidates = [搜索结果列表],
    requirement = "添加日报批量导出 Excel 功能"
    」

    示例 2: 自定义权重
    「
    使用 ai-ad-code-selector，
    candidates = [...],
    requirement = "...",
    weights = {
      tech_stack_match: 0.40,  // 更重视技术栈匹配
      feature_coverage: 0.30,
      adaptation_cost: 0.20,
      code_quality: 0.10
    }
    」

    示例 3: 严格模式
    「
    使用 ai-ad-code-selector，
    candidates = [...],
    requirement = "...",
    strict_mode = true  // 技术栈不匹配直接淘汰
    」
  </usage>


  <!-- ======================================================
       9. 版本记录 (Version Notes)
  ====================================================== -->
  <VERSION_NOTES>
    ### v1.0 (2025-12-17)
    - 初始版本
    - 四维评估框架 (技术栈/功能/成本/质量)
    - 适配方案自动生成
    - 借鉴 MetaGPT 的多维度决策框架
    - 借鉴 Devika 的任务评估逻辑
  </VERSION_NOTES>

</skill>
