---
name: content-discovery
description: |
  Automated content discovery workflow for scanning multiple data sources
  (ArXiv, GitHub, HuggingFace), applying AI-powered semantic filtering and
  deduplication, analyzing content quality, downloading images, and publishing
  to multiple channels (Hexo blog, Telegram, Discord).

  Use this skill when:
  - Executing /discover command with task configurations
  - Scanning academic papers from ArXiv (via MCP or WebSearch)
  - Finding GitHub repositories or HuggingFace models
  - Applying semantic AI filtering to avoid duplicate content
  - Generating high-quality Chinese summaries and insights
  - Publishing structured content with metadata tracking

  This skill handles the complete end-to-end discovery pipeline including
  data source detection, content filtering, quality validation, image extraction,
  and multi-channel publishing.
---

# Content Discovery Skill

自动化内容发现工作流：扫描数据源 → 智能分析 → 发布内容 → 优化关键词

## 输入配置

每个发现任务需要以下配置：

1. **任务ID**: {task_id}
2. **任务配置文件**: config/tasks/{task_id}.md
3. **关键词文件**: config/keywords/{task_id}.json
4. **会话目录**: temp/sessions/{task_id}/{session_id}/
5. **输出目录**: posts/{task_id}/

## 工作流程（5个阶段）

### 阶段 1: 数据源检测和选择

1. **读取任务配置** (config/tasks/{task_id}.md)
   - 提取已启用的数据源
   - 读取过滤规则 (YAML 格式)
   - 读取发布配置

2. **检测可用工具**
   - 优先检测 MCP 服务 (mcp__hf-mcp-server__*)
   - Fallback 到 WebSearch
   - 记录选择的工具到会话日志

3. **读取关键词** (config/keywords/{task_id}.json)
   - 提取所有类别的关键词
   - 用于构建搜索查询

### 阶段 2: 内容搜索和过滤

1. **执行搜索**
   - 使用选定的工具 (MCP 或 WebSearch)
   - 应用关键词构建查询

2. **应用过滤规则**
   - 根据task_type应用相应过滤规则
   - GitHub: minimum_stars, has_readme, time_range
   - ArXiv: time_range, categories, author_email_domains
   - HuggingFace: min_downloads, min_likes, tags

3. **AI 语义去重**
   - 列出已发布文件: posts/{task_id}/*.json
   - 提取文件名中的语义信息
   - 使用 AI 判断新内容与已有内容的语义相似度
   - 如果相似度 > 90%，判定为重复，跳过

### 阶段 3: 内容分析和评估

1. **提取元数据**
   - 标题、作者/创建者、发布日期、摘要等
   - 相关 URL（github_url, official_url, demo_url）

2. **数据来源追踪（重要）**
   必须添加 `metadata` 字段用于数据溯源和二次更新：
   ```json
   {
     "metadata": {
       "source_url": "<数据采集的原始URL>",
       "source_type": "<自动检测: github/huggingface/arxiv/web>",
       "collected_at": "<当前时间 ISO 8601>",
       "updated_at": "<当前时间 ISO 8601>",
       "task_id": "<当前任务ID>",
       "source_details": {
         // 根据 source_type 添加特定信息
         // GitHub: {"repo": "...", "branch": "main"}
         // HuggingFace: {"repo_type": "model", "repo_id": "..."}
         // ArXiv: {"arxiv_id": "...", "version": "v1"}
       }
     }
   }
   ```

   **自动类型检测规则**：
   - URL 包含 `github.com` → source_type: "github"
   - URL 包含 `huggingface.co` → source_type: "huggingface"
   - URL 包含 `arxiv.org` → source_type: "arxiv"
   - 其他 → source_type: "web"

3. **生成内容摘要与观点提炼**
   - **风格要求**: 高质量公众号/小红书/Twitter文章风格
   - **信息密度**: 高密度，无废话，直击要点
   - **内容结构**:
     * 核心观点：提炼1-2句精华观点（独特见解）
     * 技术亮点：3-5个关键技术点（带数据支撑）
     * 实用价值：实际应用场景和价值分析
   - **写作原则**:
     * 有态度：明确的技术判断和评价
     * 有深度：不仅介绍"是什么"，更分析"为什么"和"意味着什么"
     * 有对比：与同类方案对比，突出差异和优势
     * 有洞察：提供超越论文本身的思考
   - **语言风格**: 专业但不枯燥，准确但不晦涩
   - **长度控制**: 800-1500字（不是字符），信息密度优先
   - **必须包含**: 原文链接（arXiv/GitHub/官网）
   - **重要**: 所有内容必须为中文

4. **质量标准检查**（根据任务类型）

   **Foundation Models**:
   - ✅ 提取技术报告链接（优先 arxiv.org）
   - ✅ 确保 release_date 使用实际发布日期（非采集日期）
   - ✅ 内容长度 ≥ 1500 字符
   - ✅ 全部中文翻译
   - ✅ 保留 source_url

   **MCP Servers**:
   - ✅ 提取所有工具列表（tools_resources.tools）
   - ✅ 每个工具必须包含: name, description, parameters
   - ✅ **如果无法获取工具文档，直接跳过该内容**（不发布）
   - ✅ 提供配置示例（config_example）
   - ✅ 内容长度 ≥ 1500 字符
   - ✅ 全部中文翻译

   **Prompt Papers**:
   - ✅ 确保包含 arxiv_url
   - ✅ 内容长度 ≥ 1000 字符
   - ✅ 全部中文翻译

5. **评分与过滤**
   - 根据配置的 scoring_weights 评估
   - 过滤低于 minimum_score 的内容
   - **如果不符合质量标准，直接跳过**

**注意**：详见 `docs/DATA_SOURCE_TRACKING.md` 和 `docs/CONTENT_QUALITY_STANDARDS.md`

### 阶段 3.5: 图片提取和下载（AI Agent 主导）

**由 AI Agent 直接处理，无需独立脚本**

1. **图片发现（AI 分析）**
   - 使用 WebFetch/Read 工具获取内容页面（GitHub README、HF Model Card）
   - AI 分析页面内容，提取所有图片 URL
   - AI 智能识别图片类型：
     * Cover: 宽高比 16:9，尺寸较大，位于顶部，包含 "cover/banner/hero" 关键词
     * Screenshot: 包含 "screenshot/demo/preview" 关键词或上下文
     * Diagram: 包含 "arch/diagram/flow/structure" 关键词
     * Badge/Icon: 自动排除（尺寸 < 50x50px 或包含 badge/shield 关键词）

2. **智能选择（AI 决策）**
   - Cover: 选择 1 张最合适的（优先 16:9，尺寸 ≥ 800px）
   - Screenshots: 最多 3 张最重要的
   - Diagrams: 最多 3 张架构图/流程图
   - AI 评估图片的内容价值和相关性

3. **下载到本地（Bash 工具）**
   ```bash
   # Agent 调用 Bash 工具
   source .claude-plugin/scripts/discover/image_utils.sh

   # 创建目录
   IMAGE_DIR=$(create_image_dir "{task_id}" "{slug}")

   # 下载封面
   download_image "https://example.com/cover.png" \
                  "$IMAGE_DIR/cover.png"

   # 下载截图
   download_image "https://example.com/screenshot-1.png" \
                  "$IMAGE_DIR/screenshot-1.png"

   # 下载架构图
   download_image "https://example.com/architecture.svg" \
                  "$IMAGE_DIR/diagram-1.svg"

   # 获取图片尺寸
   SIZE=$(get_image_size "$IMAGE_DIR/cover.png")
   ```

4. **更新 JSON 数据（AI Agent）**
   - Agent 使用 Write 工具更新 JSON 文件
   - 添加完整的图片信息：
   ```json
   {
     "images": {
       "cover": {
         "original_url": "https://...",
         "local_path": "images/{task_id}/{slug}/cover.png",
         "alt": "AI生成的描述性文本",
         "width": 1200,
         "height": 630,
         "downloaded": true
       },
       "screenshots": [
         {
           "original_url": "https://...",
           "local_path": "images/{task_id}/{slug}/screenshot-1.png",
           "alt": "...",
           "caption": "AI生成的说明",
           "downloaded": true
         }
       ],
       "diagrams": [...]
     },
     "featured_image": "images/{task_id}/{slug}/cover.png"
   }
   ```

5. **错误处理**
   - 下载失败: 标记 `downloaded: false`，保留原始 URL
   - 超大文件（>5MB）: curl 自动拒绝
   - 网络超时: Agent 可选择重试
   - 图片无效: 使用 validate_image 检查，清理失败文件

**工具集**:
- `.claude-plugin/scripts/discover/image_utils.sh` - Bash 辅助函数
- Agent 的 WebFetch/Read - 页面内容获取
- Agent 的 Bash - 执行下载命令
- Agent 的 Write - 更新 JSON

**注意**: 详见 `docs/IMAGE_MANAGEMENT.md`

### 阶段 4: 发布

1. **保存原始数据**
   - 保存为 JSON 格式到 posts/{task_id}/
   - 文件命名: {date}_{topic}_{title-slug}.json
   - **必须包含 metadata 字段**（用于数据追溯和二次更新）
   - 确保 metadata.source_url 指向原始数据页面

2. **读取发布配置**
   - 从任务配置文件读取 hexo, telegram, discord 配置
   - 检查 enabled 字段

3. **发布到启用的渠道**

   **Hexo博客** (如果 hexo.enabled: true):
   - 读取 hexo.template 模板
   - 使用AI将JSON数据转换为高质量markdown
   - 理解并处理模板中的条件逻辑 ({{#if}})
   - 填充所有变量 ({{variable}})
   - **处理图片引用**:
     - 使用 `featured_image` 作为文章头图
     - 在正文中插入 screenshots 和 diagrams
     - 图片路径使用相对路径: `/images/{task_id}/{slug}/xxx.png`
     - 为所有图片添加 alt 文本
   - 保存到 ${HEXO_PATH}/{post_dir}/
   - 文件名: {actual_date}-{slug}.md
   - **重要**: 使用模型的实际发布日期作为文章日期，不是采集日期
   - **⚠️ 强制规则**: categories 字段必须使用小写（如 models, papers, engineering）
     - 原因：SEO最佳实践，避免大小写URL重复内容惩罚
     - 错误示例：categories: ["Models"] ❌
     - 正确示例：categories: ["models"] ✅

   **Telegram频道** (如果 telegram.enabled: true):
   - 使用 telegram.format 格式化内容
   - 发送到 telegram.channel_id

   **Discord频道** (如果 discord.enabled: true):
   - 使用 discord webhook 发送
   - 格式化为 Discord embed

4. **验证发布**
   - 确认所有启用的渠道都发布成功
   - 记录发布结果到会话日志

### 阶段 4.5: 质量验证（发布后检查）

1. **内容完整性检查**
   - JSON 文件包含所有必需字段
   - Markdown 文件格式正确
   - 图片文件成功下载

2. **质量标准验证**（根据任务类型）

   **Foundation Models**:
   ```bash
   # 检查必需字段
   - metadata.source_url 存在
   - release_date 不等于 collected_at
   - technical_report 字段（如果适用）
   - 内容为中文且 ≥ 1500 字符
   ```

   **MCP Servers**:
   ```bash
   # 检查工具文档
   - tools_resources.tools 非空数组
   - 每个 tool 包含 name, description
   - config_example 存在
   - 内容为中文且 ≥ 1500 字符
   ```

   **Prompt Papers**:
   ```bash
   # 检查论文链接
   - arxiv_url 存在且有效
   - 内容为中文且 ≥ 1000 字符
   ```

3. **失败处理**
   - 如果验证失败，删除已发布的 JSON 和 Markdown
   - 记录失败原因到会话日志
   - 不计入发布统计

4. **归档不合格内容**
   - 移动到 config/.archived/quality-failed-{date}/
   - 保留删除记录用于后续改进

### 阶段 5: 关键词优化

1. **分析新内容**
   - 从摘要和标题中提取技术术语

2. **关键词发现**
   - 计算新词的出现频率和置信度
   - 过滤置信度低于 0.85 的词

3. **更新关键词文件**
   - 更新 config/keywords/{task_id}.json

## 输出要求

每个任务完成后输出执行摘要:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 任务执行完成: {task_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

数据源: {使用的工具}
搜索结果: {总数}
过滤后: {数量}
去重后: {数量}
质量检查: {通过/失败}
发布成功: {数量}

质量统计:
  • 中文内容: {数量}/{总数} (100% required)
  • 符合长度要求: {数量}/{总数}
  • 包含必需字段: {数量}/{总数}

任务特定指标:
  • [Foundation Models] 有技术报告: {数量}/{总数}
  • [MCP Servers] 有工具文档: {数量}/{总数}
  • [Prompt Papers] 有arxiv链接: {数量}/{总数}

发布渠道:
  • JSON原始数据: {数量}个文件（含 metadata.source_url）
  • Hexo博客: {已发布/跳过/失败} (如果enabled)
  • Telegram: {已发送/跳过/失败} (如果enabled)
  • Discord: {已发送/跳过/失败} (如果enabled)

图片下载:
  • 封面: {数量}
  • 截图: {数量}
  • 架构图: {数量}

新发现关键词: {数量}

质量不合格（已跳过）:
  • 无工具文档: {数量}
  • 内容过短: {数量}
  • 非中文内容: {数量}
  • 缺少必需字段: {数量}

保存位置:
  • JSON: posts/{task_id}/
  • 图片: blog/source/images/{task_id}/
  • Hexo: {HEXO_PATH}/{post_dir}/ (如果enabled)
  • 归档: config/.archived/ (如果有不合格内容)
会话日志: temp/sessions/{task_id}/{session_id}/

💡 二次更新: 所有 JSON 包含 metadata.source_url，可用于未来更新
⚠️ 质量优先: 不符合标准的内容已被跳过或归档
```

## 错误处理

如果执行失败:
- 记录详细错误到 logs/{task_id}_{session_id}.log
- 保存中间结果到会话目录
- 返回错误摘要

## 工具和脚本

可用的辅助脚本：
- `.claude-plugin/scripts/discover/image_utils.sh` - 图片下载和处理
- `.claude-plugin/scripts/discover/update_index.sh` - 更新任务索引
- `.claude-plugin/scripts/discover/check.sh` - 前置环境检查
- `.claude-plugin/scripts/discover/parse_tasks.sh` - 任务解析

## 并行执行支持

此 Skill 支持并行处理多个任务。当同时执行多个任务时：
- 每个任务创建独立的会话目录
- 任务之间相互隔离，互不影响
- 所有任务完成后汇总统计信息
