---
name: feishu-automation
description: 自动化操作飞书（Lark）平台。当用户需要操作飞书多维表格、发送消息、管理文档、创建群组或自动化飞书工作流时使用此技能。
allowed-tools: mcp__feishu__*, Bash, Read, Write, Edit
---

# 飞书自动化操作

## 功能说明
此技能专门用于自动化飞书平台的各种操作，包括：
- 多维表格（Bitable）的创建和数据管理
- 发送消息到用户或群组
- 文档和知识库管理
- 群组创建和成员管理
- 云文档权限管理
- 工作流自动化

## 使用场景
- "在飞书多维表格中添加一条记录"
- "创建一个飞书群组并邀请成员"
- "发送消息到飞书群"
- "搜索飞书文档内容"
- "自动化飞书审批流程"
- "批量导入数据到飞书表格"

## 核心功能模块

### 1. 多维表格（Bitable）
- **创建表格**：创建新的多维表格和数据表
- **字段管理**：添加、修改字段类型和属性
- **记录操作**：增删改查记录数据
- **数据查询**：使用筛选条件查询数据
- **批量操作**：批量导入导出数据

### 2. 消息管理
- **发送消息**：文本、富文本、卡片、图片等
- **群组消息**：向群组发送通知
- **私聊消息**：向个人发送消息
- **消息历史**：获取会话历史记录
- **消息模板**：使用卡片模板

### 3. 文档管理
- **文档搜索**：搜索云文档内容
- **文档创建**：创建新文档
- **权限管理**：添加协作者和设置权限
- **内容提取**：获取文档纯文本内容

### 4. 群组管理
- **创建群组**：创建新的群聊
- **成员管理**：添加或移除成员
- **群组列表**：获取用户所在群组
- **群组信息**：查询群组详情

### 5. 知识库（Wiki）
- **搜索节点**：搜索知识库内容
- **节点信息**：获取知识库节点详情
- **内容管理**：管理知识库文档

## 工作流程

### 数据同步流程
1. **连接飞书**：配置 API 凭证
2. **获取数据**：从外部系统获取数据
3. **数据转换**：转换为飞书格式
4. **写入表格**：批量写入多维表格
5. **发送通知**：通知相关人员

### 消息推送流程
1. **触发条件**：监听事件或定时触发
2. **构建消息**：准备消息内容和格式
3. **获取接收者**：确定用户或群组 ID
4. **发送消息**：调用消息接口
5. **记录日志**：保存发送记录

## 最佳实践

### 认证配置
- 使用 `user_access_token` 进行用户身份操作
- 使用 `tenant_access_token` 进行应用身份操作
- 妥善保管 App ID 和 App Secret
- 定期刷新 access_token

### 数据操作
- 批量操作时注意 API 限流
- 使用分页查询大量数据
- 数据写入前进行验证
- 保持数据格式一致性

### 错误处理
- 实现重试机制
- 记录详细错误日志
- 处理权限不足情况
- 验证用户和群组 ID

## 常用代码示例

### 1. 创建多维表格并添加数据
```javascript
// 创建多维表格
const app = await createBitable({
  name: "客户管理表",
  folder_token: "folder_id"
});

// 创建数据表
const table = await createTable({
  app_token: app.app_token,
  table: {
    name: "客户信息",
    fields: [
      { field_name: "客户名称", type: 1 },
      { field_name: "联系电话", type: 13 },
      { field_name: "创建时间", type: 5 }
    ]
  }
});

// 添加记录
await createRecord({
  app_token: app.app_token,
  table_id: table.table_id,
  fields: {
    "客户名称": "张三",
    "联系电话": "13800138000",
    "创建时间": Date.now()
  }
});
```

### 2. 发送群组消息
```javascript
// 发送文本消息
await sendMessage({
  receive_id: "chat_id",
  msg_type: "text",
  content: JSON.stringify({
    text: "这是一条测试消息"
  })
});

// 发送卡片消息
await sendMessage({
  receive_id: "chat_id",
  msg_type: "interactive",
  content: JSON.stringify({
    elements: [
      {
        tag: "div",
        text: {
          content: "**重要通知**",
          tag: "lark_md"
        }
      }
    ]
  })
});
```

### 3. 搜索和查询数据
```javascript
// 搜索多维表格记录
const records = await searchRecords({
  app_token: "app_token",
  table_id: "table_id",
  filter: {
    conjunction: "and",
    conditions: [
      {
        field_name: "状态",
        operator: "is",
        value: ["进行中"]
      }
    ]
  }
});

// 搜索文档
const docs = await searchDocs({
  search_key: "项目计划",
  count: 10
});
```

## 集成场景

### 1. CRM 数据同步
- 从 CRM 系统获取客户数据
- 同步到飞书多维表格
- 自动更新客户状态
- 发送变更通知

### 2. 审批流程自动化
- 监听审批事件
- 更新相关表格数据
- 通知相关人员
- 记录审批历史

### 3. 报表自动生成
- 定时从表格提取数据
- 生成统计报表
- 创建飞书文档
- 分享给团队成员

### 4. 任务管理
- 创建任务表格
- 分配任务给成员
- 发送任务提醒
- 跟踪任务进度

## 注意事项
- 遵守飞书 API 调用频率限制
- 正确处理用户 ID 类型（open_id、union_id、user_id）
- 确保应用有足够的权限范围
- 测试时使用测试环境
- 保护用户隐私和数据安全
