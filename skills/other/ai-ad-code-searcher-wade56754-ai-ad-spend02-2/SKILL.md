---
name: ai-ad-code-searcher
version: "1.0"
status: ready_for_production
layer: skill
owner: wade
last_reviewed: 2025-12-17
baseline:
  - MASTER.md v3.5
  - CODE_FACTORY_REFERENCE_PROJECTS.md v1.0
code_sources:
  - project: code-graph-rag
    github: https://github.com/vitali87/code-graph-rag
    license: MIT
    borrowed_concepts:
      - Tree-sitter AST 解析架构
      - UniXcoder 语义向量化
      - 知识图谱存储代码关系
  - project: code-rag
    github: https://github.com/rawveg/code-rag
    license: MIT
    borrowed_concepts:
      - RAG 检索架构
      - 自然语言代码搜索
  - project: Aider
    github: https://github.com/paul-gauthier/aider
    license: Apache-2.0
    borrowed_concepts:
      - Repo Map 项目结构索引
---

<skill>
──────────────────────────────────────────────
  <name>ai-ad-code-searcher</name>
  <version>1.0</version>
  <domain>AI_AD_SYSTEM / 代码工厂 / 代码搜索</domain>
  <profile>Code-Search / RAG / Multi-Source</profile>
──────────────────────────────────────────────


  <!-- ======================================================
       0. 代码来源说明 (Code Sources)
  ====================================================== -->
  <code_sources>
    本 Skill 的设计和实现借鉴了以下开源项目：

    1. **code-graph-rag** (MIT License)
       - GitHub: https://github.com/vitali87/code-graph-rag
       - 借鉴内容:
         - Tree-sitter AST 解析多语言代码
         - UniXcoder 语义向量化 (按功能描述搜索)
         - 知识图谱存储函数调用/类继承关系

    2. **code-rag** (MIT License)
       - GitHub: https://github.com/rawveg/code-rag
       - 借鉴内容:
         - RAG (Retrieval-Augmented Generation) 架构
         - 向量相似度搜索

    3. **Aider** (Apache-2.0 License)
       - GitHub: https://github.com/paul-gauthier/aider
       - 借鉴内容:
         - Repo Map 项目结构索引技术
         - 文件依赖关系分析

    技术实现参考:
    - 向量数据库: Chroma (本地) / FAISS (大规模)
    - AST 解析: Tree-sitter (Python/TypeScript/JavaScript)
    - 语义编码: UniXcoder / OpenAI Embeddings
  </code_sources>


  <!-- ======================================================
       1. 核心使命 (Mission)
  ====================================================== -->
  <mission>
    作为代码工厂的搜索引擎，负责从多个来源搜索与需求相关的参考代码。

    核心原则:
    - 🔍 多源搜索: 本项目 > 代码资料库 > GitHub
    - 🎯 语义匹配: 按功能描述搜索，非仅关键词匹配
    - 📊 相关度排序: 返回按相关度排序的候选列表
    - 🏷️ 来源标注: 每个结果都标注来源和适配提示
  </mission>


  <!-- ======================================================
       2. 输入契约 (Input Contract)
  ====================================================== -->
  <input_contract>
    必填:
    {
      requirement: string  // 需求描述 (中英文均可)
    }

    可选:
    {
      sources: {
        local_project: boolean,   // 搜索本项目 (默认 true)
        code_library: boolean,    // 搜索代码资料库 (默认 true)
        github: boolean           // 搜索 GitHub (默认 false, 需网络)
      },
      max_candidates: number,     // 最大候选数 (默认 5)
      tech_stack_filter: {        // 技术栈过滤
        language: "python" | "typescript" | "javascript",
        framework: "fastapi" | "nextjs" | "react"
      },
      search_mode: "keyword" | "semantic" | "hybrid"  // 搜索模式 (默认 hybrid)
    }
  </input_contract>


  <!-- ======================================================
       3. 输出契约 (Output Contract)
  ====================================================== -->
  <output_contract>
    {
      success: boolean,
      data: {
        candidates: [
          {
            id: string,                    // 唯一标识
            source: "local_project" | "code_library" | "github",
            path: string,                  // 文件路径或 URL
            relevance_score: number,       // 0-100 相关度
            snippet: string,               // 代码片段预览
            match_reason: string,          // 匹配原因说明
            tech_stack_match: number,      // 0-100 技术栈匹配度
            adaptation_hint: string | null // 适配提示
          }
        ],
        search_stats: {
          total_searched: number,
          local_matches: number,
          library_matches: number,
          github_matches: number,
          search_time_ms: number
        }
      },
      error: string | null
    }
  </output_contract>


  <!-- ======================================================
       4. 搜索策略 (Search Strategy)
  ====================================================== -->
  <search_strategy>
    <phase id="KEYWORD_EXTRACTION">
      从需求描述中提取关键词:
      - 中文关键词 → 英文映射 (导出→export, 分页→pagination)
      - 技术术语识别 (Excel, API, CRUD)
      - 业务领域词汇 (日报, 账本, 充值)
    </phase>

    <phase id="LOCAL_PROJECT_SEARCH">
      优先级: ⭐⭐⭐⭐⭐ (最高)

      搜索方式:
      1. 从 inventory YAML 中按 tags 匹配
      2. 使用 grep/glob 在代码中搜索关键词
      3. 解析 AST 查找相关函数/类

      输出: 本项目已有的类似功能
    </phase>

    <phase id="CODE_LIBRARY_SEARCH">
      优先级: ⭐⭐⭐⭐

      搜索方式:
      1. 从 references YAML 中按 feature 匹配
      2. 从 snippets 目录中搜索代码片段
      3. 从 templates 目录中搜索模板

      输出: 已验证的参考代码
    </phase>

    <phase id="GITHUB_SEARCH">
      优先级: ⭐⭐⭐ (需网络)

      搜索方式:
      1. GitHub Code Search API
      2. 按 stars/license 过滤
      3. 检查技术栈兼容性

      输出: 外部开源参考
    </phase>

    <phase id="RANKING">
      综合排序:
      - 来源权重: local_project (1.5x) > code_library (1.2x) > github (1.0x)
      - 相关度权重: relevance_score * 0.4
      - 技术栈匹配权重: tech_stack_match * 0.3
      - 代码质量权重: quality_score * 0.2
      - 适配成本权重: (100 - adaptation_cost) * 0.1
    </phase>
  </search_strategy>


  <!-- ======================================================
       5. 关键词映射表 (Keyword Mapping)
  ====================================================== -->
  <keyword_mapping>
    中文 → 英文关键词:

    | 中文     | 英文                          |
    |----------|-------------------------------|
    | 导出     | export, download              |
    | 导入     | import, upload                |
    | 分页     | pagination, page, paginate    |
    | 表格     | table, grid, list, data-table |
    | 表单     | form, input, field            |
    | 上传     | upload, file-upload           |
    | 下载     | download, export              |
    | 搜索     | search, query, filter         |
    | 筛选     | filter, select                |
    | 排序     | sort, order                   |
    | 图表     | chart, graph, visualization   |
    | 认证     | auth, login, jwt              |
    | 权限     | permission, rbac, role        |
    | 日报     | daily-report, report          |
    | 账本     | ledger, accounting            |
    | 充值     | topup, recharge, deposit      |
  </keyword_mapping>


  <!-- ======================================================
       6. 禁止行为 (Forbidden Actions)
  ====================================================== -->
  <forbidden_actions>
    <forbidden id="CS-001">
      <action>返回无关代码作为搜索结果</action>
      <correct_action>只返回相关度 > 40 的结果</correct_action>
    </forbidden>

    <forbidden id="CS-002">
      <action>不标注代码来源</action>
      <correct_action>每个结果必须包含 source 和 path</correct_action>
    </forbidden>

    <forbidden id="CS-003">
      <action>返回许可证不兼容的代码</action>
      <correct_action>只返回 MIT/Apache/BSD 等兼容许可证的代码</correct_action>
    </forbidden>

    <forbidden id="CS-004">
      <action>伪造搜索结果</action>
      <correct_action>只返回实际存在的代码</correct_action>
    </forbidden>
  </forbidden_actions>


  <!-- ======================================================
       7. 使用示例 (Usage Examples)
  ====================================================== -->
  <usage>
    示例 1: 搜索导出功能
    「
    使用 ai-ad-code-searcher，
    requirement = "添加日报批量导出 Excel 功能"
    」

    示例 2: 搜索前端组件
    「
    使用 ai-ad-code-searcher，
    requirement = "数据表格组件，支持分页和筛选"，
    tech_stack_filter = { language: "typescript", framework: "react" }
    」

    示例 3: 仅搜索本项目
    「
    使用 ai-ad-code-searcher，
    requirement = "状态机流转逻辑"，
    sources = { local_project: true, code_library: false, github: false }
    」
  </usage>


  <!-- ======================================================
       8. 版本记录 (Version Notes)
  ====================================================== -->
  <VERSION_NOTES>
    ### v1.0 (2025-12-17)
    - 初始版本
    - 支持多源搜索 (本项目/代码资料库/GitHub)
    - 支持关键词和语义混合搜索
    - 借鉴 code-graph-rag 的 Tree-sitter + UniXcoder 架构
    - 借鉴 Aider 的 Repo Map 概念
  </VERSION_NOTES>

</skill>
