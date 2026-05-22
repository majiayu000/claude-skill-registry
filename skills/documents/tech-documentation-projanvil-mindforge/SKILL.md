---
name: tech-documentation
description: 技术文档编写技能，涵盖 API 文档、架构文档、部署指南和各种技术写作最佳实践。使用此技能创建技术文档、编写 API 文档、创建架构设计文档，或需要部署和运维手册模板时使用。
---

# 技术文档编写技能

技术文档编写技能库，提供全面的技术文档写作方法论和模板。

## 概述

这是一个专注于技术文档编写的综合性技能模块，涵盖各类技术文档的编写规范、模板和最佳实践，帮助团队产出高质量、易理解、易维护的技术文档。

## 核心能力

### 1. API文档
- **OpenAPI/Swagger规范**
- **RESTful API文档**
- **GraphQL文档**
- **gRPC接口文档**
- **API变更日志**
- **认证授权说明**

### 2. 架构文档
- **架构设计文档** (Architecture Design Document)
- **架构决策记录** (Architecture Decision Records, ADR)
- **系统架构图** (C4模型、UML)
- **技术选型报告**
- **架构演进路线图**

### 3. 详细设计文档
- **模块设计文档**
- **数据库设计文档**
- **接口设计文档**
- **算法设计说明**
- **时序图/流程图**

### 4. 部署运维文档
- **部署手册**
- **运维手册**
- **故障处理手册**
- **监控告警配置**
- **性能优化指南**
- **备份恢复流程**

### 5. 用户手册
- **产品使用手册**
- **快速开始指南**
- **常见问题FAQ**
- **故障排查指南**
- **最佳实践**

### 6. 开发者文档
- **贡献指南** (CONTRIBUTING.md)
- **代码规范**
- **开发环境搭建**
- **测试指南**
- **发布流程**

### 7. 项目管理文档
- **项目计划**
- **需求文档**
- **测试计划**
- **发布说明** (Release Notes)
- **变更日志** (CHANGELOG)

### 8. 知识库文档
- **技术博客**
- **案例分析**
- **问题总结**
- **学习笔记**

## 文档编写原则

### 1. 5C原则
- **Clear (清晰)**: 语言简洁，逻辑清晰
- **Concise (简洁)**: 避免冗余，直击要点
- **Complete (完整)**: 信息全面，覆盖所需
- **Correct (正确)**: 内容准确，经过验证
- **Consistent (一致)**: 风格统一，术语规范

### 2. 读者导向
- 了解目标读者（开发者、运维、产品、用户）
- 使用读者熟悉的语言和概念
- 提供不同层次的信息（概览→详细）
- 包含实际示例和最佳实践

### 3. 结构化
- 清晰的层次结构
- 统一的格式和风格
- 目录和导航
- 交叉引用

### 4. 可维护性
- 版本控制
- 变更记录
- 定期审查和更新
- 反馈机制

## 文档模板

> **API文档模板**（OpenAPI格式、接口列表、错误码、变更日志）：参见 [references/api-doc-template.md](references/api-doc-template.md)
> **架构设计文档模板**（概述、需求、架构设计、技术栈、数据架构、部署）：参见 [references/architecture-template.md](references/architecture-template.md)
> **部署文档模板**（环境、前置条件、部署步骤、回滚、监控）：参见 [references/deployment-template.md](references/deployment-template.md)

## 使用场景

### 新项目启动
```
为新项目创建完整的文档体系：
- README.md
- API文档
- 架构设计文档
- 部署文档
- 贡献指南
```

### API设计评审
```
编写API设计文档，包括：
- 接口定义
- 数据模型
- 错误处理
- 安全认证
```

### 系统交付
```
准备系统交付文档包：
- 系统架构文档
- 部署运维手册
- 用户使用手册
- 故障处理手册
```

### 知识沉淀
```
技术方案总结：
- 问题分析
- 解决方案
- 技术决策
- 经验教训
```

## 集成示例

### 在Agent中使用
```json
{
  "agent": "tech-writer",
  "skills": [
    "tech-documentation",
    "system-architecture",
    "api-design"
  ]
}
```

### 在对话中引用
```
@tech-documentation 请为这个API创建完整的文档
```

## 文档质量检查清单

### 内容质量
- [ ] 信息准确完整
- [ ] 逻辑清晰连贯
- [ ] 示例真实可用
- [ ] 术语统一规范

### 可读性
- [ ] 语言简洁明了
- [ ] 结构层次分明
- [ ] 格式统一美观
- [ ] 配图清晰易懂

### 可维护性
- [ ] 版本信息明确
- [ ] 变更记录完整
- [ ] 联系方式准确
- [ ] 定期审查更新

### 可访问性
- [ ] 目录导航清晰
- [ ] 搜索功能完善
- [ ] 链接有效准确
- [ ] 支持多种格式

## 工具推荐

### 文档编写
- **Markdown编辑器**: Typora, VS Code
- **API文档**: Swagger Editor, Postman
- **图表工具**: Draw.io, PlantUML, Mermaid
- **截图工具**: Snipaste, Xnip

### 文档托管
- **静态站点**: GitBook, Docusaurus, VuePress
- **团队协作**: Confluence, Notion
- **版本控制**: Git, GitHub/GitLab

### 文档生成
- **API文档**: Swagger/OpenAPI, ApiDoc
- **代码文档**: JavaDoc, JSDoc, Sphinx
- **README生成**: readme-md-generator

## 学习资源

### 推荐书籍
- 《技术写作手册》
- 《Docs for Developers》
- 《The Documentation Compendium》

### 在线资源
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
- [Microsoft Writing Style Guide](https://docs.microsoft.com/style-guide/)
- [Write the Docs](https://www.writethedocs.org/)

---

**版本**: 1.0.0  
**最后更新**: 2024-12  
**维护者**: MindForge Team
