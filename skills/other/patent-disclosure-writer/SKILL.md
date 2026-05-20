---
name: patent-disclosure-writer
description: 自动化生成符合中国专利标准的专利申请技术交底书。用户只需提供创新想法，技能自动完成专利检索、技术分析、附图生成和文档撰写。支持发明专利和实用新型专利，输出 Markdown 和 DOCX 格式。可选5人专家团队审核，提供专业质量保证。
license: MIT
metadata:
  version: 2.2.0
  timelessness-score: 8/10
  last-updated: 2025-01-16
---

# 专利交底书自动生成技能

## 技能概述

本技能自动化分析、搜索、调研并编写《专利申请技术交底书》。用户只需提供基本的创新想法和思路，技能会自动搜索相关资料、分析现有技术、识别创新点，并生成完整的技术交底书。

**核心能力**：
- 自动专利检索和技术调研
- 智能分析创新点和技术方案
- 自动生成专业附图（Mermaid 格式）
- 支持断点续传和选择性重新生成
- 输出符合 IP-JL-027 标准的交底书

## 快速开始

### 1. 确保已配置 MCP 服务

本技能依赖以下 MCP 服务：
- web-search-prime（网络搜索）
- web-reader（网页内容提取）
- google-patents-mcp（专利检索）
- exa（技术文档搜索）

详细配置方法见 [references/configuration.md](references/configuration.md)

### 2. 运行生成命令

```bash
/patent
```

按提示输入：
- 创新想法
- 所属技术领域
- 关键词（可选）
- 专利类型（发明专利/实用新型专利）

### 3. 转换为 DOCX（可选）

```bash
/patent-md-2-docx
```

## 何时使用此技能

当用户需要以下操作时，应该使用此技能：
- "写专利交底书"
- "生成专利文档"
- "专利申请"
- "技术交底书"
- "申请发明专利"

## 斜杠命令

| 命令 | 功能 | 说明 |
|------|------|------|
| `/patent` | 智能生成交底书 | 支持断点续传、选择性重新生成 |
| `/patent-update-diagrams` | 智能补充附图 | 扫描章节并补充缺失的附图 |
| `/patent-export-figures` | 导出黑白附图 | 将 Mermaid 附图导出为黑白 PNG 图片 |
| `/patent-md-2-docx` | Markdown 转 DOCX | 将 Markdown 交底书转换为正式格式 |

## 执行流程

```
用户输入创新想法
       ↓
1. 发明名称生成 → 01_发明名称.md
2. 技术领域分析 → 02_技术领域.md
3. 背景技术调研 → 03_背景技术.md
4. 技术问题分析 → 04_技术问题.md
5. 技术方案设计 → 05_技术方案.md
6. 有益效果分析 → 06_有益效果.md
7. 实施方式编写 → 07_具体实施方式.md
8. 保护点提炼 → 08_专利保护点.md
9. 参考资料收集 → 09_参考资料.md
10. 文档整合 → 专利申请技术交底书_[发明名称].md
```

## 子代理列表

| 子代理 | 对应章节 | 输出文件 |
|--------|----------|----------|
| title-generator | 1.发明创造名称 | 01_发明名称.md |
| field-analyzer | 2.所属技术领域 | 02_技术领域.md |
| background-researcher | 3.相关的背景技术 | 03_背景技术.md |
| problem-analyzer | 4.(1)解决的技术问题 | 04_技术问题.md |
| solution-designer | 4.(2)技术方案 | 05_技术方案.md |
| benefit-analyzer | 4.(3)有益效果 | 06_有益效果.md |
| implementation-writer | 5.具体实施方式 | 07_具体实施方式.md |
| protection-extractor | 6.关键点和欲保护点 | 08_专利保护点.md |
| reference-collector | 7.其他参考资料 | 09_参考资料.md |
| document-integrator | 文档整合 | 专利申请技术交底书_[发明名称].md |
| diagram-exporter | 附图导出 | 黑白 PNG 图片 |

详细说明见 [references/agents.md](references/agents.md)

## 审核团队系统（新增）

本技能支持可选的专家团队审核功能，提供专业的专利质量保证。

### 审核模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **完整审核模式** | 5人专家团队，4阶段审核 | 重要专利申请 |
| **快速模式** | 跳过审核，直接生成 | 快速草稿、内部参考 |

### 审核流程

```
01-02章节 → [预审] → 03-05章节 → [中期审核1] →
06-07章节 → [中期审核2] → 08-09章节 → [最终审核] → 整合
```

### 审核代理

| 代理 | 角色 | 权重 |
|------|------|------|
| review-coordinator | 审核协调器 | - |
| expert-sr-tech | 资深技术专家 | 2票 |
| expert-tech | 技术专家 | 1票 |
| expert-legal | 法律专家 | 1票 |
| expert-sr-agent | 资深专利代理人 | 2票 |
| expert-agent | 专利代理人 | 1票 |

### 审核输出

- 阶段审核报告（4个）
- 审核汇总报告（1个）
- 修改建议清单
- 争议报告（如有）

## 专利类型

| 类型 | 创新要求 | 审查周期 | 保护期限 |
|------|---------|---------|----------|
| **发明专利** | 突出的实质性特点和显著的进步 | 2-3年 | 20年 |
| **实用新型专利** | 实质性特点和进步 | 6-12个月 | 10年 |

## MCP 工具依赖

| MCP 服务 | 用途 |
|---------|------|
| web-search-prime | 网络搜索 |
| web-reader | 网页内容提取 |
| google-patents-mcp | 专利检索 |
| exa | 技术文档搜索 |

## 输出文件

- 各章节独立 Markdown 文件（便于审核和修改）
- 完整的交底书文档：`专利申请技术交底书_[发明名称].md`
- 附图以 Mermaid 代码块形式嵌入

## 详细文档

- [完整配置指南](references/configuration.md) - MCP 服务配置详细步骤
- [子代理详解](references/agents.md) - 每个子代理的详细说明
- [故障排查指南](references/troubleshooting.md) - 常见问题和解决方案

## 模板文件

- Markdown 模板：`templates/IP-JL-027(A／0)专利申请技术交底书模板.md`
- DOCX 模板：`templates/发明、实用新型专利申请交底书 模板.docx`

## Scripts

本技能包含以下验证和导出脚本：

| 脚本 | 用途 | 运行方式 |
|------|------|----------|
| validate_disclosure.py | 验证交底书完整性 | `python scripts/validate_disclosure.py --dir .` |
| validate_mermaid.py | 验证 Mermaid 语法 | `python scripts/validate_mermaid.py --dir .` |
| check_figures.py | 检查附图编号连续性 | `python scripts/check_figures.py --dir .` |
| export_mermaid.py | 导出 Mermaid 为黑白 PNG | `python scripts/export_mermaid.py --input diagram.mmd --output diagram.png` |

### 使用示例

```bash
# 验证完整的交底书
python scripts/validate_disclosure.py

# 验证并显示详细信息
python scripts/validate_mermaid.py --verbose

# 检查附图编号
python scripts/check_figures.py

# 导出单个 Mermaid 文件为黑白 PNG
python scripts/export_mermaid.py --input diagram.mmd --output diagram.png

# 从 Markdown 文件提取并导出所有附图
python scripts/export_mermaid.py --markdown chapter.md --output-dir figures/

# 批量处理目录中所有 Markdown 文件
python scripts/export_mermaid.py --dir . --pattern "*.md"
```

### Mermaid 黑白导出说明

`export_mermaid.py` 脚本将 Mermaid 图表导出为**符合专利审核要求的黑白图片**：

- **纯黑白配色**：线条黑色、文字黑色、背景白色
- **白色背景**：完全透明或白色背景，适合打印和提交
- **自动查找 mmdc**：自动定位 Mermaid CLI 安装路径
- **批量处理**：支持从 Markdown 文件批量提取和导出

**依赖安装**：
```bash
npm install -g @mermaid-js/mermaid-cli
```

**导出效果**：
- ✅ 符合专利局审核要求
- ✅ 适合打印和正式提交
- ✅ 保持图表清晰度和可读性

### Exit Codes

| 脚本 | Exit Code | 含义 |
|------|-----------|------|
| validate_disclosure.py | 0 | 验证成功 |
| validate_disclosure.py | 10 | 验证失败 |
| validate_mermaid.py | 0 | 验证成功 |
| validate_mermaid.py | 11 | 验证失败 |
| check_figures.py | 0 | 编号连续 |
| check_figures.py | 12 | 发现跳号 |
| export_mermaid.py | 0 | 导出成功 |
| export_mermaid.py | 20 | 导出失败 |

## Evolution & Extension Points

### Timelessness Score: 8/10

本技能设计基于以下原则确保长期有效性：

**核心原则**:
- **模板抽象**：IP-JL-027 模板可独立更新，不影响生成逻辑
- **MCP 服务抽象**：支持降级模式，不依赖特定外部服务
- **专利类型扩展**：架构支持添加新专利类型（外观设计、国际专利等）
- **附图格式扩展**：当前支持 Mermaid，可扩展到 PlantUML、Graphviz

### Extension Points

| 扩展点 | 当前支持 | 未来扩展方向 |
|--------|----------|-------------|
| **专利类型** | 发明专利、实用新型专利 | 外观设计专利、国际专利（PCT）、美国专利 |
| **输出格式** | Markdown、DOCX | PDF、HTML、XML（专利局格式） |
| **附图类型** | Mermaid | PlantUML、Graphviz、手绘草图识别 |
| **MCP 服务** | 4 个特定服务 | 可插拔服务架构、服务替换策略 |
| **语言** | 中文 | 多语言支持（英文、日文等） |
| **验证规则** | 基础格式验证 | 法律合规性检查、权利要求分析 |

### Obsolescence Triggers

以下变化可能需要更新技能：

| 触发器 | 影响范围 | 应对策略 |
|--------|----------|----------|
| IP-JL-027 模板标准更新 | 章节结构、格式 | 模板版本化，支持多版本并存 |
| 中国专利法重大修订 | 专利类型、保护范围 | 参数化法律要求，配置文件更新 |
| Mermaid 语法不兼容变更 | 附图生成 | 抽象图表生成层，支持多种格式 |
| MCP 协议版本升级 | MCP 服务调用 | 版本检测，兼容性处理 |
| Claude Code API 变更 | 子代理调用 | 适配层封装 |

### Version History

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 2.2.0 | 2025-01-16 | 添加 `/patent-export-figures` 斜杠命令，专门用于导出黑白 PNG 附图 |
| 2.1.0 | 2025-01-16 | 添加 Mermaid 黑白导出功能，符合专利审核要求 |
| 2.0.0 | 2025-01-15 | 添加5人专家团队审核系统，支持分阶段审核、投票机制、争议解决 |
| 1.1.0 | 2025-01-14 | 添加验证脚本、演进性分析 |
| 1.0.0 | 2025-01-14 | 初始版本，支持发明专利和实用新型专利 |
