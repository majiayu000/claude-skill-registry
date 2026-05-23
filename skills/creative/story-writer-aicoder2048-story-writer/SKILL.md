---
name: story-writer
description: 通用短篇小说创作技能包。支持多种类型（武侠/科幻/童话/现言），执行大纲、人物、目录、章节的专业创作。根据类型参数加载对应的创作方法论和写作风格。
---

# 短篇小说创作 Skill（通用版）

[技能说明]
    通用的短篇小说创作技能包，支持多种小说类型。覆盖故事构思、人物塑造、章节规划、正文写作全流程。
    根据传入的类型参数（GENRE_TYPE），读取对应类型目录下的创作资源，生成符合该类型规范的小说内容。

    **支持的类型**：
    - wuxia（武侠）：金庸风格，典雅古风，侠义豪情
    - kehuan（科幻）：阿西莫夫+刘慈欣风格，冷峻理性，宇宙思考
    - tonghua（童话）：诗意优美，温暖治愈，纯真有趣
    - xianyan（现言）：口语化自然，情感细腻，节奏明快

[文件结构]
    .claude/skills/story-writer/
    ├── SKILL.md                        # 本文件（技能包核心配置）
    ├── templates/                      # 通用文档模板
    │   ├── outline-template.md
    │   ├── character-template.md
    │   ├── chapter-index-template.md
    │   └── chapter-template.md
    └── genres/                         # 类型专属配置
        ├── wuxia/                      # 武侠类型
        │   ├── genre-config.md         # 类型元数据和Q1-Q3
        │   ├── outline-method.md       # 大纲创作方法论
        │   ├── output-style.md         # 写作风格
        │   └── examples/               # 示例
        ├── kehuan/                     # 科幻类型
        │   └── ...
        ├── tonghua/                    # 童话类型
        │   └── ...
        └── xianyan/                    # 现言类型
            └── ...

[核心能力]
    - **类型识别**：根据传入的 GENRE_TYPE 参数加载对应类型配置
    - **创作阶段理解**：识别当前处于大纲、人物、目录还是章节创作阶段
    - **资源整合**：读取通用模板 + 类型专属方法论/风格/示例
    - **专业创作**：基于资源和上下文创作符合该类型规范的小说内容
    - **风格把控**：确保创作内容符合该类型的写作风格
    - **模板遵循**：严格按照模板格式生成文档结构
    - **上下文理解**：理解已有文档内容，确保创作连贯性

[参数]
    GENRE_TYPE: 小说类型标识（wuxia/kehuan/tonghua/xianyan）

    根据 GENRE_TYPE，确定资源路径：
    - 类型配置：genres/{GENRE_TYPE}/genre-config.md
    - 创作方法论：genres/{GENRE_TYPE}/outline-method.md
    - 写作风格：genres/{GENRE_TYPE}/output-style.md
    - 示例目录：genres/{GENRE_TYPE}/examples/

[执行流程]
    第零步：加载类型配置
        读取 genres/{GENRE_TYPE}/genre-config.md
        获取该类型的：
        - 类型名称和描述
        - 写作风格关键词
        - 世界观元素
        - 封面设计氛围

    第一步：理解创作需求
        识别当前创作阶段：
        - 如果在讨论故事大纲或outline.md不存在 → 大纲创作阶段
        - 如果在讨论人物或刚执行/character → 人物创作阶段
        - 如果在讨论章节规划或刚执行/catalog → 目录创作阶段
        - 如果在创作章节正文或刚执行/write → 章节创作阶段

    第二步：读取创作资源
        **大纲创作阶段**：
            1. 读取 templates/outline-template.md（通用文档格式模板）
            2. 读取 genres/{GENRE_TYPE}/outline-method.md（该类型大纲创作方法论）
            3. 读取 genres/{GENRE_TYPE}/output-style.md（该类型写作风格）
            4. 读取 genres/{GENRE_TYPE}/examples/outline-example.md（该类型大纲示例）
            5. 从对话历史获取用户回答的Q1-Q3

        **人物创作阶段**：
            1. 读取 outline.md（了解故事背景和设定）
            2. 读取 templates/character-template.md（通用文档格式模板）
            3. 读取 genres/{GENRE_TYPE}/outline-method.md（人物塑造指导部分）
            4. 读取 genres/{GENRE_TYPE}/output-style.md（该类型写作风格）
            5. 读取 genres/{GENRE_TYPE}/examples/character-example.md（该类型人物示例）

        **目录创作阶段**：
            1. 读取 outline.md 和 character.md（了解故事和人物）
            2. 读取 templates/chapter-index-template.md（通用文档格式模板）
            3. 读取 genres/{GENRE_TYPE}/outline-method.md（章节规划方法）
            4. 读取 genres/{GENRE_TYPE}/output-style.md（该类型写作风格）

        **章节创作阶段**：
            1. 读取 outline.md、character.md、chapter_index.md（全部上下文）
            2. 读取 templates/chapter-template.md（通用文档格式模板）
            3. 读取 genres/{GENRE_TYPE}/output-style.md（该类型写作风格和章节创作方法，最重要）
            4. 读取 genres/{GENRE_TYPE}/examples/chapter-example.md（该类型章节示例）
            5. 从chapter_index.md获取当前章节的规划内容

    第三步：执行专业创作
        **大纲创作**：
            基于用户提供的信息（核心创意、核心冲突、故事调性）和读取的资源：
            - 严格按照 templates/outline-template.md 的格式结构
            - 遵循 genres/{GENRE_TYPE}/outline-method.md 的创作方法论
            - 应用 genres/{GENRE_TYPE}/output-style.md 的写作风格
            - 参考 genres/{GENRE_TYPE}/examples/outline-example.md 的示例
            - 生成包含以下内容的完整大纲：
                • 小说信息（书名、类型、故事调性）
                • 核心梗概（一句话）
                • 导语（150-200字）
                • 故事大纲（采用起承转合结构，2000-3000字）
                • 主要人物（简要列出3-5个核心人物）

        **人物创作**：
            基于outline.md的故事设定和读取的资源：
            - 严格按照 templates/character-template.md 的格式结构
            - 遵循 genres/{GENRE_TYPE}/outline-method.md 中的人物塑造指导
            - 应用 genres/{GENRE_TYPE}/output-style.md 的写作风格
            - 参考 genres/{GENRE_TYPE}/examples/character-example.md 的示例
            - 生成包含以下内容的人物小传：
                • 主要角色（3-5个，详细描述）
                • 反派/对立角色（如有）
                • 重要配角（如有）
                • 其他角色（如有）
            - 确保人物形象鲜明，具有该类型特质

        **目录创作**：
            基于outline.md和character.md的设定和读取的资源：
            - 严格按照 templates/chapter-index-template.md 的格式结构
            - 遵循 genres/{GENRE_TYPE}/outline-method.md 的章节规划方法
            - 应用 genres/{GENRE_TYPE}/output-style.md 的写作风格
            - 生成固定5章的章节目录，与大纲的起承转合结构对应
            - 每章包含：章节标题 + 一句话剧情简介
            - 确保起承转合布局合理，故事节奏流畅

        **章节创作**：
            基于全部上下文文档和读取的资源：
            - 严格按照 templates/chapter-template.md 的格式结构
            - 严格遵循 genres/{GENRE_TYPE}/output-style.md 的写作风格和章节创作方法（最重要）
            - 参考 genres/{GENRE_TYPE}/examples/chapter-example.md 的示例
            - 基于 chapter_index.md 中该章节的规划进行创作
            - 生成2000-3000字的章节正文

    第四步：返回创作成果
        返回符合对应模板格式的完整内容

[创作原则]
    - **模板遵循原则**：
        • 创作的所有文档必须严格遵循templates/中定义的格式
        • 不能遗漏模板中的必要标题和段落
        • 不能改变模板定义的层级结构
        • 可以根据实际需要调整内容的详略

    - **风格一致性原则**：
        • 所有创作必须保持该类型的写作风格统一
        • 严格遵循genres/{GENRE_TYPE}/output-style.md中定义的写作风格
        • 参考genres/{GENRE_TYPE}/examples/中的示例风格
        • 确保大纲、人物、章节的风格协调

    - **上下文连贯性原则**：
        • character创作必须基于outline
        • catalog创作必须基于outline + character
        • chapter创作必须基于outline + character + catalog
        • 确保前后内容不矛盾，逻辑连贯

    - **质量标准原则**：
        • 大纲：类型元素丰富，主题清晰，故事结构完整，固定起承转合结构，2000-3000字
        • 人物：形象鲜明，具有该类型特质，与故事匹配
        • 目录：固定5章，与大纲的起承转合结构对应，布局合理，节奏流畅
        • 章节：2000-3000字，风格统一，推进剧情

[注意事项]
    - 必须先获取 GENRE_TYPE 参数才能开始创作
    - 确保每个阶段的必需资源都已读取完整
    - 不仅读取文档内容，还要深入理解其含义
    - output-style.md中的风格要求是强约束，必须严格遵守
    - templates/中的格式是必须遵循的，任何偏离都可能导致问题
    - 短篇小说固定为5章结构，采用起承转合布局
    - 创作内容必须完整、连贯、符合该类型特点
    - 始终使用中文创作

[扩展新类型]
    要添加新的小说类型，只需：
    1. 在 genres/ 下创建新的类型目录（如 genres/xuanhuan/）
    2. 创建以下文件：
       - genre-config.md（类型元数据、Q1-Q3问题模板）
       - outline-method.md（创作方法论）
       - output-style.md（写作风格）
       - examples/（示例文件）
    3. 无需修改本 SKILL.md 或任何 command 文件
