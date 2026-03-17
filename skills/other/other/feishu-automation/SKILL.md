---
name: feishu-automation
description: 飞书（Lark）全通道自动化。使用 lark-mcp 工具操作飞书多维表格（Bitable）、发送消息、管理文档、创建群组、自动化工作流等。当用户需要操作飞书平台、同步数据到飞书表格、发送飞书通知、管理飞书文档或自动化飞书业务流程时使用此技能。
allowed-tools: mcp__lark-mcp_*, Bash, Read, Write, Edit
---

# 飞书全通道自动化

使用 lark-mcp 工具实现飞书平台的全面自动化操作。

## 核心功能

### 1. 多维表格（Bitable）
- 创建多维表格和数据表
- 添加、修改、删除字段
- 增删改查记录数据
- 批量导入导出数据
- 数据筛选和排序

### 2. 消息发送
- 发送文本、富文本、卡片消息
- 群组消息和私聊消息
- 消息模板和交互式卡片
- 文件和图片发送

### 3. 文档管理
- 搜索云文档
- 创建新文档
- 编辑文档内容
- 文档权限管理
- 文档协作者管理

### 4. 群组管理
- 创建群组
- 添加/移除成员
- 获取群组列表
- 群组信息查询

### 5. 知识库（Wiki）
- 搜索知识库节点
- 获取节点详情
- 创建和管理知识库内容

### 6. 日历和任务
- 创建和查询日历事件
- 创建和管理任务
- 任务分配和跟踪

## 快速开始

### 检查 MCP 可用性
```javascript
// 检查 lark-mcp 工具是否可用
// 可用工具前缀：mcp__lark-mcp_
```

### 发送测试消息
```javascript
// 发送文本消息到群组
await mcp__lark-mcp_sendMessage({
  receive_id: "oc_xxxxxxxxx",
  msg_type: "text",
  content: JSON.stringify({
    text: "Hello from Clawdbot!"
  })
});
```

## 工作流程

### 数据同步流程
1. 连接数据源
2. 转换数据格式
3. 创建/更新多维表格
4. 批量写入数据
5. 发送通知

### 消息推送流程
1. 触发事件（定时/事件驱动）
2. 构建消息内容
3. 获取接收者 ID
4. 发送消息
5. 记录日志

### 文档自动化流程
1. 获取文档模板
2. 填充内容
3. 创建新文档
4. 设置权限
5. 分享给团队

## API 工具参考

### 多维表格相关
- `createBitable` - 创建多维表格
- `createTable` - 创建数据表
- `addRecord` - 添加记录
- `updateRecord` - 更新记录
- `deleteRecord` - 删除记录
- `searchRecords` - 搜索记录
- `getRecord` - 获取记录详情

### 消息相关
- `sendMessage` - 发送消息
- `getMessages` - 获取消息历史
- `replyMessage` - 回复消息

### 文档相关
- `searchDocs` - 搜索文档
- `createDoc` - 创建文档
- `getDoc` - 获取文档内容
- `updateDoc` - 更新文档
- `setDocPermission` - 设置文档权限

### 群组相关
- `createGroup` - 创建群组
- `addMember` - 添加成员
- `getGroupList` - 获取群组列表
- `getGroupInfo` - 获取群组信息

## 实用场景

### 1. 自动化日报收集
- 每日定时创建表格记录
- 成员填写日报
- 自动汇总统计
- 发送到群组

### 2. 审批流程
- 创建审批表格
- 监听状态变更
- 自动通知审批人
- 记录审批历史

### 3. 任务管理
- 创建任务表格
- 分配任务给成员
- 发送任务提醒
- 跟踪完成状态

### 4. 客户管理
- 客户信息表格
- 跟进记录
- 自动提醒
- 数据可视化

### 5. 报表生成
- 从表格提取数据
- 生成统计报表
- 创建飞书文档
- 定期推送更新

## 最佳实践

### 认证配置
- 使用提供的 App ID 和 App Secret
- 遵守 API 调用频率限制
- 缓存 access_token

### 数据操作
- 批量操作使用分页
- 数据写入前验证格式
- 错误处理和重试
- 记录操作日志

### 消息发送
- 使用交互式卡片提升体验
- 合理控制发送频率
- 避免发送敏感信息
- 支持用户交互

### 权限管理
- 最小权限原则
- 定期审查权限
- 协作者生命周期管理

## 错误处理

### 常见错误
- 权限不足 - 检查应用权限配置
- 限流错误 - 实现重试和等待
- 无效 ID - 验证用户/群组 ID 格式
- 网络错误 - 实现重试机制

### 重试策略
- 指数退避算法
- 最大重试次数限制
- 记录失败请求
- 通知管理员

## 安全注意事项

- 保护 App Secret
- 不要在日志中记录敏感信息
- 使用环境变量管理凭证
- 定期轮换访问令牌
- 遵守数据隐私法规

## 示例代码

### 创建多维表格并添加数据
```javascript
// 创建多维表格
const bitable = await mcp__lark-mcp_createBitable({
  name: "项目管理",
  folder_token: "folder_token"
});

// 创建数据表
const table = await mcp__lark-mcp_createTable({
  app_token: bitable.app_token,
  table: {
    name: "任务列表",
    fields: [
      { field_name: "任务名称", type: 1 },
      { field_name: "负责人", type: 13 },
      { field_name: "状态", type: 3 },
      { field_name: "截止日期", type: 5 }
    ]
  }
});

// 添加记录
await mcp__lark-mcp_addRecord({
  app_token: bitable.app_token,
  table_id: table.table_id,
  fields: {
    "任务名称": "完成项目文档",
    "负责人": "user_id",
    "状态": "进行中",
    "截止日期": Date.now()
  }
});
```

### 发送卡片消息
```javascript
await mcp__lark-mcp_sendMessage({
  receive_id: "chat_id",
  msg_type: "interactive",
  content: JSON.stringify({
    config: {
      wide_screen_mode: true
    },
    header: {
      template: "turquoise",
      title: {
        content: "重要通知",
        tag: "plain_text"
      }
    },
    elements: [
      {
        tag: "div",
        text: {
          content: "**项目里程碑已完成**",
          tag: "lark_md"
        }
      },
      {
        tag: "action",
        actions: [
          {
            tag: "button",
            text: {
              content: "查看详情",
              tag: "plain_text"
            },
            type: "primary",
            url: "https://example.com"
          }
        ]
      }
    ]
  })
});
```

### 批量导入数据
```javascript
const data = [
  { name: "张三", phone: "13800138000" },
  { name: "李四", phone: "13900139000" }
];

for (const item of data) {
  await mcp__lark-mcp_addRecord({
    app_token: "app_token",
    table_id: "table_id",
    fields: {
      "姓名": item.name,
      "电话": item.phone
    }
  });

  // 避免限流
  await new Promise(resolve => setTimeout(resolve, 100));
}
```

## 配置验证

### 检查 MCP 服务器
```bash
# 检查 .claude.json 中的 lark-mcp 配置
cat ~/.claude.json | grep -A 15 "lark-mcp"
```

### 测试连接
```javascript
// 发送测试消息验证连接
await mcp__lark-mcp_sendMessage({
  receive_id: "your_chat_id",
  msg_type: "text",
  content: JSON.stringify({
    text: "🎉 飞书 MCP 连接成功！"
  })
});
```

## 进阶用法

### Webhook 集成
- 监听飞书 Webhook 事件
- 自动触发工作流
- 实时数据同步

### 自动化定时任务
- 定时发送报告
- 自动数据备份
- 定期清理

### 跨平台集成
- 与 GitHub 集成（Issue 同步）
- 与邮件集成（通知推送）
- 与日历集成（日程管理）

## 故障排查

### MCP 工具不可用
1. 重启 Claude Desktop
2. 检查网络连接
3. 验证凭证是否有效
4. 查看错误日志

### API 调用失败
1. 检查应用权限配置
2. 验证用户/群组 ID
3. 查看限流状态
4. 检查数据格式

### 权限不足
1. 登录飞书开放平台
2. 检查应用权限范围
3. 重新授权
4. 等待权限生效
