---
name: ai-ad-code-assembler
version: "1.0"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-12-17
baseline:
  - MASTER.md v3.5
  - CODE_FACTORY_REFERENCE_PROJECTS.md v1.0
code_sources:
  - project: Aider
    github: https://github.com/paul-gauthier/aider
    license: Apache-2.0
    borrowed_concepts:
      - Repo Map 项目结构概览技术
      - 多文件协同编辑模式
      - Diff 格式输出
      - 上下文管理策略
  - project: Continue
    github: https://github.com/continuedev/continue
    license: Apache-2.0
    borrowed_concepts:
      - Context Provider 系统
      - 工具调用机制
  - project: Copier
    github: https://github.com/copier-org/copier
    license: MIT
    borrowed_concepts:
      - 模板渲染系统
      - YAML 配置驱动
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-code-assembler</name>
  <version>1.0</version>
  <domain>AI_AD_SYSTEM / 代码工厂 / 代码组装</domain>
  <profile>Code-Assembler / Multi-File / Template-Based</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 代码来源说明 (Code Sources)
  ====================================================== -->
  <code_sources>
    本 Skill 的设计和实现借鉴了以下开源项目：

    1. **Aider** (Apache-2.0 License)
       - GitHub: https://github.com/paul-gauthier/aider
       - 借鉴内容:
         - Repo Map 项目结构概览技术
         - 多文件协同编辑模式
         - Diff 格式输出
         - 上下文管理策略

    2. **Continue** (Apache-2.0 License)
       - GitHub: https://github.com/continuedev/continue
       - 借鉴内容:
         - Context Provider 系统设计
         - 工具调用机制

    3. **Copier** (MIT License)
       - GitHub: https://github.com/copier-org/copier
       - 借鉴内容:
         - 模板渲染系统
         - YAML 配置驱动生成

    核心能力:
    - 多文件组装: 同时生成后端服务 + 路由 + 前端组件
    - 依赖管理: 自动处理文件间依赖关系
    - 模板驱动: 基于项目模板生成一致的代码结构
  </code_sources>


  <!-- ======================================================
       1. 核心使命 (Mission)
  ====================================================== -->
  <mission>
    作为代码工厂的组装器，负责将适配后的代码组装成完整的功能模块。

    核心原则:
    - 🧩 多文件组装: 同时处理后端和前端的多个文件
    - 📦 依赖完整: 自动生成所需的导入和依赖
    - 📋 模板驱动: 使用项目模板确保代码风格一致
    - 🔗 集成就绪: 输出可直接集成到项目的代码
  </mission>


  <!-- ======================================================
       2. 输入契约 (Input Contract)
  ====================================================== -->
  <input_contract>
    必填:
    {
      adapted_files: AdaptedFile[],   // 适配后的文件列表
      requirement: string              // 原始需求描述
    }

    可选:
    {
      scope: "backend" | "frontend" | "fullstack",  // 组装范围 (默认 fullstack)
      include_tests: boolean,          // 是否生成测试 (默认 true)
      include_types: boolean,          // 是否生成类型文件 (默认 true)
      output_format: "files" | "diff"  // 输出格式 (默认 files)
    }
  </input_contract>


  <!-- ======================================================
       3. 输出契约 (Output Contract)
  ====================================================== -->
  <output_contract>
    {
      success: boolean,
      data: {
        assembled_module: {
          name: string,                 // 模块名称
          files: [
            {
              path: string,             // 文件路径
              content: string,          // 文件内容
              action: "create" | "modify",
              dependencies: string[]    // 依赖的其他文件
            }
          ],
          entry_points: {               // 入口点
            backend_router: string,
            frontend_page: string
          }
        },
        repo_map: {                     // 项目结构图 (借鉴 Aider)
          affected_files: string[],
          new_files: string[],
          modified_files: string[]
        },
        integration_guide: {            // 集成指南
          steps: string[],
          imports_to_add: string[],
          config_changes: string[]
        }
      },
      error: string | null
    }
  </output_contract>


  <!-- ======================================================
       4. 组装模式 (Assembly Patterns)
  ====================================================== -->
  <assembly_patterns>
    <pattern id="BACKEND_MODULE">
      <name>后端模块组装</name>
      <structure>
        backend/
        ├── schemas/
        │   └── {feature}_schema.py     # Pydantic 模型
        ├── services/
        │   └── {feature}_service.py    # 业务逻辑
        ├── routers/
        │   └── {feature}_router.py     # API 路由
        └── tests/
            └── test_{feature}.py       # 单元测试
      </structure>
      <dependencies>
        schema → service → router → test
      </dependencies>
    </pattern>

    <pattern id="FRONTEND_MODULE">
      <name>前端模块组装</name>
      <structure>
        frontend/
        ├── types/
        │   └── {feature}.ts            # TypeScript 类型
        ├── api/
        │   └── {feature}Api.ts         # API 调用
        ├── hooks/
        │   └── use{Feature}.ts         # React Hooks
        ├── components/
        │   └── {Feature}/
        │       ├── index.tsx           # 主组件
        │       └── {Feature}.module.css
        └── pages/
            └── {feature}/
                └── page.tsx            # 页面组件
      </structure>
      <dependencies>
        types → api → hooks → components → page
      </dependencies>
    </pattern>

    <pattern id="FULLSTACK_MODULE">
      <name>全栈模块组装</name>
      <dependencies>
        backend_schema → backend_service → backend_router
        → frontend_types → frontend_api → frontend_hooks
        → frontend_components → frontend_page
      </dependencies>
    </pattern>
  </assembly_patterns>


  <!-- ======================================================
       5. Repo Map (借鉴 Aider)
  ====================================================== -->
  <repo_map>
    Repo Map 是项目结构的概览，帮助理解代码组织。

    生成方式:
    1. 扫描项目目录结构
    2. 提取关键文件和入口点
    3. 标识本次组装涉及的文件

    输出格式:
    ```
    AI_ad_spend02/
    ├── backend/
    │   ├── routers/
    │   │   ├── daily_reports.py       # 现有
    │   │   └── export.py              # [NEW] 本次新增
    │   └── services/
    │       ├── daily_report_service.py # 现有
    │       └── export_service.py       # [NEW] 本次新增
    └── frontend/
        └── components/
            └── ExportButton/           # [NEW] 本次新增
                └── index.tsx
    ```
  </repo_map>


  <!-- ======================================================
       6. 模板系统 (借鉴 Copier)
  ====================================================== -->
  <template_system>
    <template id="BACKEND_SERVICE">
      <file>backend/services/{feature}_service.py</file>
      <content>
        ```python
        """
        {feature_name} Service
        [ASSEMBLED] 由 ai-ad-code-assembler 组装生成
        """
        from typing import List, Optional
        from sqlalchemy.ext.asyncio import AsyncSession

        from backend.models import {Model}
        from backend.schemas.{feature}_schema import {Schema}Create, {Schema}Update


        class {ClassName}Service:
            """
            {feature_description}
            """

            def __init__(self, db: AsyncSession):
                self.db = db

            async def create(self, data: {Schema}Create) -> {Model}:
                """创建 {entity_name}"""
                # [ADAPTED] 来自参考代码
                {adapted_create_logic}

            async def get_list(
                self,
                skip: int = 0,
                limit: int = 100,
            ) -> List[{Model}]:
                """获取 {entity_name} 列表"""
                {adapted_list_logic}
        ```
      </content>
    </template>

    <template id="BACKEND_ROUTER">
      <file>backend/routers/{feature}_router.py</file>
      <content>
        ```python
        """
        {feature_name} Router
        [ASSEMBLED] 由 ai-ad-code-assembler 组装生成
        """
        from fastapi import APIRouter, Depends
        from sqlalchemy.ext.asyncio import AsyncSession

        from backend.core.deps import get_db
        from backend.services.{feature}_service import {ClassName}Service
        from backend.schemas.{feature}_schema import {Schema}Response

        router = APIRouter(prefix="/{feature}", tags=["{feature}"])


        @router.get("/", response_model=List[{Schema}Response])
        async def list_{feature}(
            skip: int = 0,
            limit: int = 100,
            db: AsyncSession = Depends(get_db),
        ):
            service = {ClassName}Service(db)
            return await service.get_list(skip=skip, limit=limit)
        ```
      </content>
    </template>
  </template_system>


  <!-- ======================================================
       7. 禁止行为 (Forbidden Actions)
  ====================================================== -->
  <forbidden_actions>
    <forbidden id="ASM-001">
      <action>生成不完整的模块</action>
      <correct_action>确保所有依赖文件都被生成</correct_action>
    </forbidden>

    <forbidden id="ASM-002">
      <action>破坏现有代码结构</action>
      <correct_action>新文件单独创建，现有文件标注修改点</correct_action>
    </forbidden>

    <forbidden id="ASM-003">
      <action>不提供集成指南</action>
      <correct_action>必须输出集成步骤和所需配置</correct_action>
    </forbidden>

    <forbidden id="ASM-004">
      <action>忽略文件间依赖</action>
      <correct_action>按依赖顺序组装，确保导入正确</correct_action>
    </forbidden>
  </forbidden_actions>


  <!-- ======================================================
       8. 使用示例 (Usage Examples)
  ====================================================== -->
  <usage>
    示例 1: 全栈模块组装
    「
    使用 ai-ad-code-assembler，
    adapted_files = [适配后的文件列表],
    requirement = "添加日报批量导出 Excel 功能"，
    scope = "fullstack"
    」

    示例 2: 仅后端组装
    「
    使用 ai-ad-code-assembler，
    adapted_files = [...],
    requirement = "...",
    scope = "backend",
    include_tests = true
    」

    示例 3: Diff 格式输出
    「
    使用 ai-ad-code-assembler，
    adapted_files = [...],
    requirement = "...",
    output_format = "diff"
    」
  </usage>


  <!-- ======================================================
       9. 版本记录 (Version Notes)
  ====================================================== -->
  <VERSION_NOTES>
    ### v1.0 (2025-12-17)
    - 初始版本
    - 多文件组装支持 (后端/前端/全栈)
    - 借鉴 Aider 的 Repo Map 技术
    - 借鉴 Copier 的模板系统
    - 集成指南自动生成
  </VERSION_NOTES>

</skill>
