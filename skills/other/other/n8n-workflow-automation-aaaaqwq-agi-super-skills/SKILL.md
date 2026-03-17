---
name: n8n-workflow-automation
description: 自动化创建和管理 n8n 工作流。当用户需要设计工作流、配置节点、优化自动化流程或集成多个服务时使用此技能。
allowed-tools: mcp__n8n-mcp__search_workflows, mcp__n8n-mcp__execute_workflow, mcp__n8n-mcp__get_workflow_details, Bash, Read, Write, Edit
---

# n8n 工作流自动化

## 功能说明
此技能专门用于自动化 n8n 工作流的创建、配置和管理，包括：
- 设计和创建新的工作流
- 配置各种节点（HTTP Request、数据处理、条件判断等）
- 优化现有工作流的性能和可靠性
- 集成多个服务（Gmail、Google Drive、Slack、API 等）
- 调试和故障排除工作流问题

## 使用场景
- "创建一个 n8n 工作流来监控邮件并保存附件"
- "优化我的 n8n 工作流，它有太多节点"
- "设计一个自动化流程来处理客户数据"
- "配置 n8n 的 OAuth2 认证"
- "帮我调试这个工作流为什么一直失败"

## 工作流程
1. **需求分析**：理解用户的自动化需求和业务流程
2. **工作流设计**：规划节点结构和数据流
3. **节点配置**：详细配置每个节点的参数
4. **测试验证**：确保工作流正确运行
5. **优化建议**：提供性能和可维护性改进建议

## 最佳实践
- 使用清晰的节点命名
- 添加错误处理节点
- 合理使用条件分支
- 避免过度复杂的工作流
- 使用环境变量管理敏感信息
- 定期测试和监控工作流

## 常用节点类型
- **触发器**：Webhook、Schedule、Email Trigger
- **数据处理**：Set、Function、Code
- **条件控制**：IF、Switch、Merge
- **外部服务**：HTTP Request、Gmail、Slack、Google Sheets
- **数据库**：MySQL、PostgreSQL、MongoDB

## 示例工作流
### 邮件附件自动保存
1. Gmail Trigger（监控新邮件）
2. Filter（筛选包含附件的邮件）
3. Extract Attachments（提取附件）
4. Google Drive（保存到云盘）
5. Slack（发送通知）

### API 数据同步
1. Schedule Trigger（定时触发）
2. HTTP Request（获取 API 数据）
3. Function（数据转换）
4. Database（保存到数据库）
5. Error Handler（错误处理）
