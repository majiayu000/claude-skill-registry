---
name: ai-ad-code-adapter
version: "1.0"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-12-17
baseline:
  - MASTER.md v3.5
  - CODE_FACTORY_REFERENCE_PROJECTS.md v1.0
code_sources:
  - project: astx
    github: https://github.com/codemodsquad/astx
    license: MIT
    borrowed_concepts:
      - 结构化搜索替换模式
      - 通配符匹配语法
      - AST 级别代码转换
  - project: refactor (Python)
    github: https://github.com/isidentical/refactor
    license: MIT
    borrowed_concepts:
      - Python AST 重构框架
      - 契约式转换 (assert-based)
      - 规则化转换动作
  - project: ts-morph
    github: https://github.com/dsherret/ts-morph
    license: MIT
    borrowed_concepts:
      - TypeScript AST 操作模式
      - 代码重构辅助方法
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-code-adapter</name>
  <version>1.0</version>
  <domain>AI_AD_SYSTEM / 代码工厂 / 代码适配</domain>
  <profile>Code-Adapter / AST-Transform / Rule-Based</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 代码来源说明 (Code Sources)
  ====================================================== -->
  <code_sources>
    本 Skill 的设计和实现借鉴了以下开源项目：

    1. **astx** (MIT License)
       - GitHub: https://github.com/codemodsquad/astx
       - 借鉴内容:
         - 结构化搜索替换模式 (pattern → replacement)
         - 通配符匹配语法 ($identifier 占位符)
         - AST 级别代码转换

    2. **refactor** (MIT License)
       - GitHub: https://github.com/isidentical/refactor
       - 借鉴内容:
         - Python AST 重构框架
         - 契约式转换 (assert-based matching)
         - 规则化转换动作 (Rule + Replace)

    3. **ts-morph** (MIT License)
       - GitHub: https://github.com/dsherret/ts-morph
       - 借鉴内容:
         - TypeScript AST 操作模式
         - 代码重构辅助方法

    实现策略:
    - 简单转换: 使用正则表达式模式匹配
    - 复杂转换: 使用 LLM 辅助适配
    - 验证: 适配后进行语法检查
  </code_sources>


  <!-- ======================================================
       1. 核心使命 (Mission)
  ====================================================== -->
  <mission>
    作为代码工厂的适配器，负责将参考代码适配为符合项目规范的代码。

    核心原则:
    - 🔧 保留结构: 保留参考代码的整体结构，只做必要修改
    - 📏 规则驱动: 使用预定义规则进行技术栈适配
    - 📝 标注改动: 所有改动点都添加注释标注
    - ✅ 来源追溯: 保留代码来源信息
  </mission>


  <!-- ======================================================
       2. 输入契约 (Input Contract)
  ====================================================== -->
  <input_contract>
    必填:
    {
      reference: SearchCandidate,   // 选中的参考代码
      requirement: string,          // 原始需求描述
      adaptation_plan: AdaptationPlan  // 适配方案
    }

    可选:
    {
      custom_rules: {               // 自定义适配规则
        [pattern]: replacement
      },
      preserve_comments: boolean,   // 保留原注释 (默认 true)
      add_type_hints: boolean,      // 添加类型提示 (默认 true)
      target_path: string           // 目标文件路径
    }
  </input_contract>


  <!-- ======================================================
       3. 输出契约 (Output Contract)
  ====================================================== -->
  <output_contract>
    {
      success: boolean,
      data: {
        adapted_files: [
          {
            file_path: string,        // 目标文件路径
            content: string,          // 适配后的完整代码
            adaptations: [            // 适配记录
              {
                line: number,
                type: string,         // 适配类型
                original: string,
                adapted: string,
                reason: string
              }
            ],
            source_attribution: {     // 来源标注
              reference: string,
              source: string,
              adaptation_rate: string
            }
          }
        ],
        summary: {
          total_adaptations: number,
          by_type: {
            tech_stack: number,
            project_standard: number,
            sot_compliance: number,
            custom: number
          }
        }
      },
      error: string | null
    }
  </output_contract>


  <!-- ======================================================
       4. 适配层次 (Adaptation Layers)
  ====================================================== -->
  <adaptation_layers>
    <layer id="L1_TECH_STACK" priority="1">
      <name>技术栈适配</name>
      <description>将参考代码适配到项目的技术栈版本</description>

      <rules>
        <!-- Pydantic v1 → v2 -->
        <rule id="PYDANTIC_CONFIG">
          <pattern>class Config:</pattern>
          <replacement>model_config = ConfigDict(</replacement>
          <context>Pydantic v2 使用 model_config 替代 class Config</context>
        </rule>

        <rule id="PYDANTIC_VALIDATOR">
          <pattern>@validator\(([^)]+)\)</pattern>
          <replacement>@field_validator($1)</replacement>
          <context>Pydantic v2 使用 @field_validator 替代 @validator</context>
        </rule>

        <rule id="PYDANTIC_ROOT_VALIDATOR">
          <pattern>@root_validator</pattern>
          <replacement>@model_validator(mode='after')</replacement>
          <context>Pydantic v2 使用 @model_validator 替代 @root_validator</context>
        </rule>

        <!-- SQLAlchemy 1 → 2 -->
        <rule id="SQLALCHEMY_QUERY">
          <pattern>session\.query\((\w+)\)</pattern>
          <replacement>session.execute(select($1))</replacement>
          <context>SQLAlchemy 2.x 推荐使用 select() 语法</context>
        </rule>

        <rule id="SQLALCHEMY_COLUMN">
          <pattern>Column\(</pattern>
          <replacement>mapped_column(</replacement>
          <context>SQLAlchemy 2.x 使用 mapped_column</context>
        </rule>
      </rules>
    </layer>

    <layer id="L2_PROJECT_STANDARD" priority="2">
      <name>项目规范适配</name>
      <description>适配项目的响应格式、错误码、命名等规范</description>

      <rules>
        <rule id="RESPONSE_FORMAT">
          <pattern>return \{[^}]*\}</pattern>
          <replacement>return StandardResponse(data=..., message=...)</replacement>
          <context>使用项目标准响应格式</context>
        </rule>

        <rule id="ERROR_CODE">
          <pattern>raise HTTPException\(status_code=(\d+), detail="([^"]+)"\)</pattern>
          <replacement>raise AppException(code=ErrorCode.XXX, message="$2")</replacement>
          <context>使用项目标准错误码</context>
        </rule>

        <rule id="IMPORT_STANDARD">
          <description>添加项目标准导入</description>
          <imports>
            - from backend.core.response import StandardResponse
            - from backend.core.error_codes import ErrorCode, AppException
          </imports>
        </rule>
      </rules>
    </layer>

    <layer id="L3_SOT_COMPLIANCE" priority="3">
      <name>SoT 合规适配</name>
      <description>确保代码符合 SoT 文档定义</description>

      <checks>
        - 字段名是否在 DATA_SCHEMA 中定义
        - 状态值是否在 STATE_MACHINE 中定义
        - 错误码是否在 ERROR_CODES_SOT 中定义
        - 业务规则是否符合 BUSINESS_RULES
      </checks>

      <actions>
        - 替换不存在的字段为正确字段
        - 替换不存在的状态为正确状态
        - 添加遗漏的业务规则检查
      </actions>
    </layer>

    <layer id="L4_CUSTOM" priority="4">
      <name>功能定制</name>
      <description>根据需求进行功能定制 (使用 LLM)</description>

      <prompt_template>
        你是代码适配器。基于以下参考代码，根据需求进行定制。

        ## 参考代码
        {reference_code}

        ## 需求
        {requirement}

        ## 适配指南
        {adaptation_hint}

        ## 规则
        1. 保留参考代码的整体结构
        2. 只做满足需求的必要修改
        3. 用注释标注所有改动点: # [ADAPTED] 原因: xxx
        4. 不要发明新的状态/字段/错误码

        ## 输出格式
        只输出适配后的完整代码，包含改动标注注释。
      </prompt_template>
    </layer>
  </adaptation_layers>


  <!-- ======================================================
       5. 来源标注格式 (Source Attribution)
  ====================================================== -->
  <source_attribution>
    在每个适配后的文件头部添加来源标注:

    ```python
    """
    [ADAPTED FROM] {source}: {reference_path}
    [ADAPTATION]   基于参考代码适配，非从零生成
    [CHANGES]      技术栈适配 x 处，项目规范适配 x 处，SoT 合规 x 处，功能定制 x 处
    """
    ```

    在每个改动点添加行内标注:

    ```python
    # [ADAPTED] 原因: Pydantic v2 语法 | 原: class Config:
    model_config = ConfigDict(...)
    ```
  </source_attribution>


  <!-- ======================================================
       6. 禁止行为 (Forbidden Actions)
  ====================================================== -->
  <forbidden_actions>
    <forbidden id="ADP-001">
      <action>完全重写参考代码</action>
      <correct_action>只做必要的适配修改，保留原结构</correct_action>
    </forbidden>

    <forbidden id="ADP-002">
      <action>不标注来源和改动</action>
      <correct_action>必须添加来源标注和改动注释</correct_action>
    </forbidden>

    <forbidden id="ADP-003">
      <action>发明 SoT 中不存在的字段/状态/错误码</action>
      <correct_action>只使用 SoT 中已定义的</correct_action>
    </forbidden>

    <forbidden id="ADP-004">
      <action>删除参考代码的有效逻辑</action>
      <correct_action>只修改，不随意删除</correct_action>
    </forbidden>
  </forbidden_actions>


  <!-- ======================================================
       7. 使用示例 (Usage Examples)
  ====================================================== -->
  <usage>
    示例 1: 基础适配
    「
    使用 ai-ad-code-adapter，
    reference = [选中的参考代码],
    requirement = "添加日报批量导出 Excel 功能"，
    adaptation_plan = [选型阶段生成的适配方案]
    」

    示例 2: 自定义规则
    「
    使用 ai-ad-code-adapter，
    reference = [...],
    requirement = "...",
    adaptation_plan = [...],
    custom_rules = {
      "old_function_name": "new_function_name",
      "OldClassName": "NewClassName"
    }
    」
  </usage>


  <!-- ======================================================
       8. 版本记录 (Version Notes)
  ====================================================== -->
  <VERSION_NOTES>
    ### v1.0 (2025-12-17)
    - 初始版本
    - 四层适配架构 (技术栈/项目规范/SoT合规/功能定制)
    - 借鉴 astx 的结构化替换模式
    - 借鉴 refactor 的规则化转换框架
    - 来源标注和改动追踪
  </VERSION_NOTES>

</skill>
