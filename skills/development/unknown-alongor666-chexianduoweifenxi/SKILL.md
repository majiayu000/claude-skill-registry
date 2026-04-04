---
name: project-knowledge-base
description: 项目知识库管理器 - 将保险业务项目文档(数据分析、PPT报告、技术方案)转化为结构化、可迁移的知识资产。支持:(1)自动生成2类标准化模板(项目启动/技术方案);(2)从Markdown/代码仓库智能提取技术决策和可复用模式;(3)统一文档格式标准;(4)生成可跨项目复用的知识库。触发场景:用户要整理项目文档、创建知识库、生成项目模板、提取技术经验、标准化现有文档时使用。
---

# 项目知识库管理器

将散落在代码注释、聊天记录、Markdown文档中的项目知识，转化为结构化、可复用的知识资产。

## 快速开始

### 场景1: 启动新项目，创建标准化知识库

```bash
# 进入技能脚本目录（安装后路径）
cd /mnt/skills/user/project-knowledge-base/scripts
python init_project_kb.py "车险周报自动化" "/home/claude/my-projects"
```

生成结果:

- 标准目录结构（docs/decisions/patterns/reports）
- 2个文档模板（项目启动文档、技术方案文档）
- README索引文件

### 场景2: 从现有项目提取知识模式

```bash
python extract_patterns.py /path/to/source /home/claude/my-projects/knowledge-base
```

自动提取:

- 技术决策（@decision标记）
- 代码模式（函数签名+docstring）
- 配置模板（JSON/YAML结构）

### 场景3: 更新知识库索引

```bash
python generate_index.py /home/claude/my-projects/knowledge-base
```

## 核心工作流程

### 工作流A: 新项目启动

```
用户：我要开始一个新的车险数据分析项目

↓ Step 1: 初始化知识库
  调用 init_project_kb.py 创建目录和模板

↓ Step 2: 填写模板
  引导用户填写项目启动文档：
  - 项目背景与目标
  - 关键指标（保费、赔付率等）
  - 里程碑与时间表

↓ Step 3: 设计技术方案
  引导用户填写技术方案文档：
  - 技术选型（参考insurance-domain.md）
  - 架构设计
  - 关键决策点

↓ 输出
  可直接使用的知识库，包含标准化文档
```

### 工作流B: 从现有项目构建知识库

```
用户：我有一个车险周报项目，代码写了很多，想整理成知识库

↓ Step 1: 确认源代码路径
↓ Step 2: 运行 extract_patterns.py 扫描
↓ Step 3: 保存提取的知识资产到 decisions/ 和 patterns/
↓ Step 4: 运行 generate_index.py 更新README

↓ 输出
  结构化知识库，可复用到新项目
```

### 工作流C: 标准化零散文档

```
用户：我有一些项目笔记和聊天记录，想整理成规范文档

↓ Step 1: 创建目标知识库（init_project_kb.py）
↓ Step 2: 分析现有内容，映射到模板
↓ Step 3: 生成标准化文档保存到docs/目录
↓ Step 4: 更新索引（generate_index.py）
```

## 工作流程

### 完整知识库构建流程

```
1. 场景识别
   ↓
   ├─ 新项目 → 工作流A
   ├─ 现有项目 → 工作流B
   └─ 零散文档 → 工作流C

2. 初始化
   ↓
   运行 init_project_kb.py
   ├─ 创建标准目录结构
   │   ├─ docs/ (项目文档)
   │   ├─ decisions/ (技术决策记录)
   │   ├─ patterns/ (可复用模式)
   │   └─ reports/ (分析报告)
   ├─ 生成模板文件
   │   ├─ 项目启动文档
   │   └─ 技术方案文档
   └─ 创建 README 索引

3. 知识提取（如适用）
   ↓
   运行 extract_patterns.py
   ├─ 扫描源代码
   │   ├─ 提取 @decision 标记
   │   ├─ 识别设计模式
   │   └─ 收集配置模板
   ├─ 分析技术选型
   └─ 保存到对应目录

4. 内容填充
   ↓
   ├─ 手动填写模板（新项目）
   └─ 整理提取内容（现有项目）

5. 索引更新
   ↓
   运行 generate_index.py
   ├─ 扫描所有文档
   ├─ 生成分类索引
   └─ 更新 README

6. 输出交付
   ↓
   结构化知识库
   ├─ 可复用模板
   ├─ 技术决策文档
   ├─ 代码模式库
   └─ 完整索引
```

### 决策逻辑

- **场景识别**：根据用户需求自动选择工作流
- **内容提取**：智能识别代码中的知识模式
- **标准化**：统一文档格式，便于跨项目复用
- **索引生成**：自动维护知识库导航

## 脚本使用指南

### 脚本1: init_project_kb.py

**功能**: 初始化项目知识库

```bash
python init_project_kb.py <项目名称> [知识库路径]

# 示例
python init_project_kb.py "车险周报自动化"
python init_project_kb.py "数据分析平台" "/home/claude/projects/kb"
```

**输出**:

- 目录结构: docs/, decisions/, patterns/, reports/
- 文档模板: 项目启动文档.md, 技术方案文档.md
- README.md

### 脚本2: extract_patterns.py

**功能**: 从代码和文档中提取知识模式

```bash
python extract_patterns.py <源代码目录> <知识库目录>

# 示例
python extract_patterns.py /mnt/skills/user/insurance-weekly-report /home/claude/kb
```

**提取规则**:

- `# @decision: xxx` → 技术决策记录
- `def func(): """docstring"""` → 代码模式
- `.json` 文件 → 配置模板

### 脚本3: generate_index.py

**功能**: 扫描知识库并生成README索引

```bash
python generate_index.py <知识库目录>
```

## 领域知识参考

在以下情况查阅 `references/insurance-domain.md`:

1. **填写车险业务相关模板时** - 了解术语（保费、赔付率、成本率）和分析维度
2. **设计技术方案时** - 参考麦肯锡风格报告规范、图表类型选择
3. **提取代码模式时** - 理解业务逻辑和数据格式要求

## 模板说明

### 模板1: 项目启动文档

**适用场景**: 新项目启动、明确范围和目标、干系人对齐

**核心章节**:

1. 项目背景与目标（业务痛点、KPI）
2. 项目范围（功能、数据、分析维度）
3. 干系人与角色
4. 关键里程碑与时间表
5. 风险与应对
6. 成功标准

### 模板2: 技术方案文档

**适用场景**: 技术选型与架构设计、关键决策记录

**核心章节**:

1. 技术选型（语言、框架、依赖库）
2. 系统架构设计（整体架构、模块设计、数据流）
3. 关键技术决策（使用@decision标记便于后续提取）
4. 技术风险与应对
5. 可扩展性设计
6. 测试策略与部署方案

## 最佳实践

### 技术决策编写

```python
# @decision: 选择python-pptx而非ReportLab
# 理由: python-pptx支持精确布局控制，满足麦肯锡风格要求
# 权衡: 性能略低但12-13页规模可接受
```

### 知识库组织（多项目）

```
knowledge-base/
├── project-A/
│   ├── docs/
│   ├── decisions/
│   └── patterns/
├── project-B/
└── shared/
    ├── templates/
    └── references/
```

### 跨项目复用流程

1. 从旧项目提取模式（extract_patterns.py）
2. 查看 patterns/ 目录找到可复用的代码/配置
3. 在新项目中参考或直接复制
4. 更新新项目的技术方案文档，记录复用的模式

## 故障排查

| 问题              | 可能原因           | 解决方案                        |
| ----------------- | ------------------ | ------------------------------- |
| 脚本运行失败      | Python版本/依赖    | 确保Python>=3.8，安装pandas     |
| 提取不到@decision | 格式不对           | 使用 `# @decision: 内容` 格式   |
| README缺少内容    | 无YAML frontmatter | 文档开头添加 `---` 包围的元数据 |

---

**技能版本**: v1.0.0 (MVP)
**适用场景**: 华安保险车险业务项目知识管理
