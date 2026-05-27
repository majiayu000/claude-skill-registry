---
name: daily-ai-workflow-analyzer
description: AI深度分析语音记录，揭示行为模式、认知偏见和战略盲点。不只是数据汇总，而是直击本质的战略洞察和否定性指导。提取可沉淀的核心原则和工作偏好，构建个人工作模式知识库。
---

# DailyAIWorkflowAnalyzer Skill

## 核心价值

**从语音记录中提取深度战略洞察，揭示认知偏见和行为盲点**

不只是数据汇总，而是：
- 🔍 **识别行为模式** → 发现低效循环和回避策略
- 🧠 **诊断认知偏见** → 揭示系统性思维错误
- 🎯 **揭示战略盲点** → 指出用户自己意识不到的问题
- 💎 **沉淀核心知识** → 提炼值得长期保留的原则
- 🛑 **否定性指导** → 告诉你"停止做什么"比"开始做什么"更重要

## 何时使用

- 当你想从日常语音记录（微信、编程App、文档工具等）中提取有价值的模式
- 当你希望AI记住你的工作习惯、偏好和标准
- 当你想避免重复的沟通和低效的工作流
- 当你需要将经验转化为可复用的规则和配置

## 核心理念

**知识沉淀 > 数据堆积**

每次分析后：
- ✅ 得到可直接应用的规则
- ✅ 更新个人工作模式知识库
- ✅ 让AI越来越了解你的标准
- ❌ 不再是看完就忘的冗长报告

## 完整工作流（已优化）

### 一键分析所有应用

```bash
python3 /Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/analyze_voice_workflow.py --days 1 --all
```

### 分析特定应用

```bash
python3 /Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/analyze_voice_workflow.py --days 1 --app Antigravity
```

### 工作流程说明

**步骤1：提取语音记录**
- 从Typeless.app数据库提取最近N天的记录
- 按应用自动分组

**步骤2：AI深度分析**（核心改进）
- 识别重复出现的问题（≥2次）
- 提取新发现的原则和规则
- 生成可执行的行动清单
- 分析用户习惯和工作模式
- 根据App类型适配分析维度（聊天、编程、文档等）

**步骤3：自动导出到Obsidian**
- 生成结构化笔记到 `知识体系/个人工作模式/`
- 智能文件命名（根据App类型）：
  - 微信 → `微信聊天记录_YYYY-MM-DD.md`
  - 编程App → `Antigravity开发记录_YYYY-MM-DD.md`
  - 文档工具 → `Alma使用记录_YYYY-MM-DD.md`
- 自动更新知识库文件：
  - [[用户习惯清单]]
  - [[工作模式配置]]
  - [[偏好设置]]

### 输出示例

```
知识体系/个人工作模式/
├── 微信聊天记录_2026-01-12.md          ← 每日分析结果
├── Antigravity开发记录_2026-01-12.md   ← 编程App分析
├── Alma使用记录_2026-01-12.md          ← 文档工具分析
├── 用户习惯清单.md                      ← 自动积累
├── 工作模式配置.md                      ← 自动积累
└── 偏好设置.md                          ← 自动积累
```

### Phase 4: Visual Dashboard
Launch the interactive dashboard:
```bash
/Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/start_dashboard.sh
```
Then visit: http://localhost:8080

**Dashboard Features**:
- Overview statistics (total records, app count, time range, peak hours)
- App list with record counts and analysis status
- "AI Analyze" buttons to trigger deep analysis
- "View Report" buttons to display reports in-page (modal)
- Batch operations (analyze all, export all, refresh)
- Data visualization (app distribution, time distribution charts)

## Architecture

```
Static Framework (One-time creation)
├── analysis_dashboard.html (HTML structure, CSS, JS logic)
│   └── JavaScript: loadData() → fetch from API → renderDashboard()
└── Never regenerated, only data changes

Dynamic Service (Flask API)
├── analysis_server.py (lightweight backend)
│   ├── GET /api/data → Return all apps data
│   ├── POST /api/analyze → Trigger Python analysis
│   ├── GET /api/report/<app> → Return markdown report
│   └── GET /api/status → Real-time analysis status
└── Handles Python script execution and status polling

Data Processing (Python Scripts)
├── extract_voice_records.py (Query Typeless DB)
├── group_by_app.py (Group records by app)
├── generate_analysis_report.py (Generate structured reports)
└── analyze_voice_workflow.py (Master workflow controller)
```

## Key Configuration

### Paths
- **Typeless DB**: `~/Library/Application Support/Typeless/typeless.db`
- **Grouped Data**: `~/Library/Application Support/alma/workspaces/temp-voice-extraction/by_app/*.json`
- **Analysis Reports**: `~/Library/Application Support/alma/workspaces/temp-voice-extraction/analysis_reports/`
- **Dashboard Port**: 8080 (changed from 5000 to avoid conflicts)

### Analysis Framework
Located at: `templates/analysis_framework.json`

**Dimensions**（根据App类型自动适配）：
- Scene Recognition:
  - 编程App: 功能需求, 交互设计, 界面反馈, 问题反馈, 优化建议, 协作沟通
  - 聊天App: 日常对话, 工作沟通, 信息分享, 问题讨论, 协作安排
  - 文档工具: 知识整理, 信息记录, 搜索查询, 内容编辑
- Workflow Stages:
  - 编程App: 需求阶段, 设计阶段, 实现阶段, 测试阶段, 修复阶段
  - 聊天App: 发起话题, 信息交流, 问题讨论, 达成共识
  - 文档工具: 信息收集, 整理归纳, 查询使用
- Collaboration Patterns:
  - 编程App: 指令型, 建议型, 质疑型, 授权型, 期望型
  - 聊天App: 信息型, 询问型, 分享型, 确认型
  - 文档工具: 查询型, 记录型, 整理型

## Resources

### scripts/
- `extract_voice_records.py`: Extract voice records from Typeless SQLite DB
- `group_by_app.py`: Group records by focused_app_name into separate JSON files
- `generate_analysis_report.py`: Generate structured analysis reports (markdown)
- `analyze_voice_workflow.py`: Master workflow controller (orchestrates extraction, grouping, reporting)
- `analysis_server.py`: Flask API server for dashboard
- `start_dashboard.sh`: One-click startup script for dashboard

### templates/
- `analysis_report_template.md`: Standardized template for analysis reports
- `analysis_framework.json`: Configuration for scene/stage/pattern recognition

### references/
- `typeless_db_schema.md`: Complete schema of Typeless.app SQLite database
- `obsidian_organization_guidelines.md`: Guidelines for structuring Obsidian notes (future integration)

## Usage Examples

### Automated Analysis (Recommended)

When you ask AI to "analyze voice records" or "generate analysis report", it will:

1. **Auto-start server** (if not running)
2. **Run complete analysis workflow**
3. **Display reports directly in conversation**

**Example commands**:
- "分析今天的语音记录"
- "分析微信最近两天的聊天记录"
- "生成语音记录分析报告"
- "分析 Antigravity 的语音记录"

**What AI does automatically**:
```bash
# Check and start Flask server (background)
# Execute full analysis
python3 auto_analyze.py --all
# Read and display report content
```

**You see**:
- Analysis progress (✓ steps complete)
- Report summaries directly in chat
- No manual steps required

---

### Manual Analysis (Advanced)

If you want to use the visual dashboard:

1. Launch dashboard: `start_dashboard.sh`
2. Visit: http://localhost:8080
3. Review: Check app statistics and patterns
4. Decide: Click "AI Analyze" for apps with valuable insights
5. View: Click "View Report" to see detailed analysis in-page
6. Iterate: Use insights to improve workflows, then repeat

---

### Command-Line Analysis

**Analyze all apps**:
```bash
python3 /Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/auto_analyze.py --all
```

**Analyze specific app**:
```bash
python3 /Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/auto_analyze.py --app Antigravity
```

**Start dashboard only**:
```bash
/Users/douba/.claude/skills/daily-ai-workflow-analyzer/scripts/start_dashboard.sh
```

## Analysis Report Structure (v2.0 - 深度洞察版)

### 报告类型
- **App名称** + "深度洞察分析报告" + 日期
  - 微信 → "微信深度洞察分析报告"
  - 编程App → "App名称开发深度洞察分析报告"
  - 文档工具 → "App名称使用深度洞察分析报告"

### 核心理念
**不只是数据汇总，而是深度战略洞察**

报告采用"直面本质"的分析框架，旨在：
- 识别用户自己意识不到的行为模式
- 诊断认知偏见和思维惯性
- 揭示战略盲点和潜在风险
- 提供包含否定性指导的行动建议
- 提炼真正值得长期保留的知识

### 核心章节结构

#### 1. ⚡ 执行摘要
- 核心发现：一句话概括最重要的洞察
- 关键问题：必须立即解决的1-2个问题
- 战略建议：优先级最高的行动方向

#### 2. 🎯 行为模式识别
- **重复循环模式**：识别"测试→修复→再测试"等低效循环
- **回避策略**：指出用技术细节回避战略思考的行为
- **低效决策**：对比实际决策和更优选择

#### 3. 🧠 认知偏见诊断
- 识别已表现出的认知偏见（如：确认偏见、沉没成本谬误）
- 说明偏见的表现和后果
- 提供打破偏见的具体方法

#### 4. 🔍 战略盲点揭示
- 揭示用户自己意识不到的核心问题
- 说明"为什么它是盲点"
- 分析潜在风险和解决方向

#### 5. ❓ 真相检验问题
- 直击本质的开放性问题（无标准答案）
- 分为产品/项目、工作方式、个人成长三个层面
- 目的是引发深度思考，而非提供答案

#### 6. 🛑 立即停止做（否定性指导）
- **今日立即停止**：1-2个需要马上停止的行为
- **本周停止**：需要调整的习惯或模式
- 每个停止项都附带"为什么"的说明

#### 7. ✅ 立即开始做（正向行动）
- **今日/明日**：1-2个紧急行动
- **本周**：2-3个短期改进
- **本月**：1-2个长期目标

#### 8. ❓ 需要确认的问题
- 在继续工作前需要用户回答的关键问题
- 用于澄清意图、明确方向、消除歧义

#### 9. 💎 可沉淀的核心知识
- **值得长期保留的原则**：从具体场景中抽象出的通用原则
- **需要固化的工作偏好**：用户明确表达过的工作方式和偏好
- 包含来源场景、适用范围、示例

#### 10. 📊 数据快照（简化版）
- 只保留最关键的3-5个指标
- 详细数据放在附录，避免干扰核心洞察

#### 11. 附录
- 采样记录与模式映射
- 报告反馈问卷

### 与v1.0版本的区别

| 对比维度 | v1.0 (旧版本) | v2.0 (深度洞察版) |
|----------|--------------|------------------|
| **核心目标** | 数据汇总和行为描述 | 深度洞察和战略指导 |
| **分析深度** | 表面模式识别 | 认知偏见和战略盲点 |
| **行动指导** | 只有正向建议 | 包含否定性指导 |
| **价值产出** | SOP和规则清单 | 原则和偏好固化 |
| **问题导向** | "用户做了什么" | "用户为什么这么做" |
| **反馈机制** | 简单评分 | 多维度评估和反馈闭环 |

### 报告质量控制标准

生成报告时必须满足：
- ✅ 至少识别1-2个重复循环模式或低效决策
- ✅ 至少揭示1个用户自己意识不到的盲点
- ✅ 至少提供1个"立即停止做"的否定性指导
- ✅ 至少提出3个直击本质的真相检验问题
- ✅ 至少提炼1-2个值得长期保留的核心原则
- ❌ 不提供泛泛而谈的建议（如"多学习新技术"）
- ❌ 不堆砌用户自己就能看到的数据统计

## Feedback Mechanism

Each report includes a feedback section:
1. Overall value rating (1-5)
2. Most valuable part
3. Most in need of improvement

This feedback is collected to iteratively refine the analysis framework and report structure.

## Integration with Obsidian (Future)

The generated analysis reports can be synced to Obsidian vault:
- Daily analysis reports → Daily Notes
- App-specific reports → Project pages
- Extracted SOPs/Principles → Knowledge base

Currently in MVP phase—focus on report quality and value extraction before automation.

## Notes

- **Port Conflict**: Dashboard uses port 8080 (5000 was occupied)
- **Analysis Status**: Polling every 3 seconds for real-time updates
- **Report Formats**: Attempts multiple filename patterns (Final/standard)
- **MVP Approach**: Start with manual review in dashboard, automate sync later
- **Value-First**: Prioritize extracting actionable insights over storing raw data

## 迭代路线图

### 当前状态 (v2.0 - 深度洞察版)
- ✅ 数据提取和分组
- ✅ 深度战略洞察框架（行为模式、认知偏见、战略盲点）
- ✅ 否定性指导机制（"停止做什么"）
- ✅ 真相检验问题库（直击本质的开放性问题）
- ✅ 可沉淀知识提取（原则和偏好固化）
- ✅ 可视化仪表板和实时状态更新
- ⏳ AI驱动的深度分析（需要模型集成）
- ⏳ 与Obsidian的自动化同步
- ⏳ 跨时间段的趋势分析

### v2.1 计划（增强AI分析能力）
1. **集成Claude API**：用模型自动生成深度洞察，而非手工填写
2. **认知偏见库扩展**：建立更全面的偏见识别框架
3. **真相检验问题生成**：根据用户行为模式自动生成定制化问题
4. **行动建议优化**：基于历史数据优化建议的准确性和可执行性

### v2.2 计划（知识库集成）
1. **Obsidian同步**：自动将分析报告和提取的知识同步到Obsidian
2. **用户画像持续更新**：建立跨时间的用户行为模式档案
3. **原则库管理**：自动去重、版本化、更新核心原则
4. **工作偏好配置**：将固化的偏好转换为可应用的配置文件

### v2.3 计划（趋势分析和预测）
1. **跨报告对比**：对比不同时间段的分析结果，识别改进趋势
2. **偏见追踪**：追踪特定认知偏见的出现频率和演变
3. **模式演化分析**：识别用户行为模式的系统性变化
4. **预测性洞察**：基于历史数据预测潜在问题和风险
4. **Feedback Loop**: Collect user ratings to refine analysis framework
