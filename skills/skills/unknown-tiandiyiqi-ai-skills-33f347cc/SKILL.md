---
name: skill-share
description: A skill that creates new Claude skills and automatically shares them on Slack using Rube for seamless team collaboration and skill discovery.
license: Complete terms in LICENSE.txt
---

## 何时使用此技能

当您需要以下操作时使用此技能：
- **创建新的Claude技能**，具有正确的结构和元数据
- **生成可分发的技能包**
- **自动在Slack上分享创建的技能**，以便团队可见
- **分享前验证技能结构**
- **打包并分发技能**给您的团队

 также在以下情况下使用此技能：
- **用户说他想要创建/分享他的技能**

此技能适用于：
- 在团队工作流程中创建技能
- 构建需要技能创建+团队通知的内部工具
- 自动化技能开发流程
- 协作创建技能并通知团队

## 主要功能

### 1. 技能创建
- 创建结构正确的技能目录，包含SKILL.md
- 生成标准化的scripts/、references/和assets/目录
- 自动生成带有必需元数据的YAML frontmatter
- 强制执行命名约定（连字符分隔）

### 2. 技能验证
- 验证SKILL.md格式和必需字段
- 检查命名约定
- 确保打包前的元数据完整性

### 3. 技能打包
- 创建可分发的zip文件
- 包含所有技能资产和文档
- 打包前自动运行验证

### 4. 通过Rube集成Slack
- 自动将创建的技能信息发送到指定的Slack频道
- 分享技能元数据（名称、描述、链接）
- 发布技能摘要以便团队发现
- 提供技能文件的直接链接

## 工作原理

1. **初始化**：提供技能名称和描述
2. **创建**：创建具有正确结构的技能目录
3. **验证**：验证技能元数据的正确性
4. **打包**：将技能打包成可分发的格式
5. **Slack通知**：将技能详情发布到团队的Slack频道

## 使用示例

```
当您要求Claude创建一个名为"pdf-analyzer"的技能时：
1. 创建/skill-pdf-analyzer/，包含SKILL.md模板
2. 生成结构化目录（scripts/、references/、assets/）
3. 验证技能结构
4. 将技能打包成zip文件
5. 发布到Slack："新技能已创建：pdf-analyzer - 高级PDF分析和提取功能"
```

## 与Rube的集成

此技能利用Rube实现：
- **SLACK_SEND_MESSAGE**：向团队频道发布技能信息
- **SLACK_POST_MESSAGE_WITH_BLOCKS**：分享格式丰富的技能元数据
- **SLACK_FIND_CHANNELS**：发现技能公告的目标频道

## 要求

- 通过Rube连接Slack工作区
- 对技能创建目录的写入权限
- Python 3.7+用于技能创建脚本
- 用于技能通知的目标Slack频道
