---
name: notion-automation
description: 自动化 Notion 操作。当用户需要管理 Notion 页面、数据库、块内容、项目跟踪或进行内容组织和搜索时使用此技能。
allowed-tools: mcp__notionApi__*, Bash, Read, Write, Edit, Grep, Glob
---

# Notion 自动化管理

## 功能说明
此技能专门用于自动化 Notion 平台的各种操作，包括：
- 页面创建、内容编辑和管理
- 数据库创建、配置和查询
- 块（Block）操作和内容更新
- 页面搜索和内容检索
- 项目和任务跟踪管理
- 团队协作和评论管理
- 页面移动和组织结构管理

## 使用场景
- "创建一个新的项目页面"
- "更新 Notion 数据库中的记录"
- "搜索包含特定关键词的页面"
- "批量管理页面内容"
- "设置项目跟踪看板"
- "管理团队协作和评论"
- "整理和组织 Notion 工作空间"

## 核心功能模块

### 1. 页面管理
- **创建页面**：创建新页面并添加初始内容
- **更新页面**：修改页面属性、标题和封面
- **获取页面**：检索页面详细信息
- **移动页面**：在不同数据库或父页面间移动
- **删除页面**：归档或删除页面
- **页面搜索**：按关键词搜索页面和数据库

### 2. 数据库管理
- **创建数据库**：创建新的数据库并配置字段
- **查询数据库**：筛选和检索数据库记录
- **更新数据库**：修改数据库结构和属性
- **获取数据库详情**：查看数据库元数据
- **数据库模板**：应用预设模板创建数据库

### 3. 块（Block）操作
- **获取块内容**：读取页面下的所有块
- **更新块内容**：修改块的文本、样式
- **添加子块**：在块中添加子元素
- **删除块**：移除不需要的块
- **批量操作**：一次性更新多个块

### 4. 内容搜索
- **全文搜索**：搜索页面标题和内容
- **数据库搜索**：在特定数据库中查找
- **筛选搜索**：按对象类型筛选结果
- **排序结果**：按编辑时间排序

### 5. 协作管理
- **获取用户**：列出工作空间用户
- **创建评论**：在页面或块中添加评论
- **获取评论**：查看页面讨论
- **页面权限**：管理页面访问权限

### 6. 项目管理
- **项目页面**：创建项目概览页面
- **任务看板**：设置 Kanban 风格任务管理
- **进度跟踪**：更新任务状态和进度
- **里程碑管理**：设置项目里程碑
- **依赖关系**：管理任务间依赖

## 工作流程

### 标准页面创建流程
1. **创建页面**：创建新页面并设置标题
2. **添加封面**：设置页面封面图片
3. **添加图标**：设置页面图标
4. **填充内容**：使用块添加初始内容
5. **关联数据库**：如需要，关联到数据库
6. **添加协作人**：设置页面协作者

### 数据库设置流程
1. **创建数据库**：创建新数据库
2. **定义字段**：配置属性类型（文本、数字、日期等）
3. **设置视图**：创建不同视图（表格、看板、日历）
4. **添加记录**：批量添加初始记录
5. **配置筛选**：设置常用筛选条件
6. **设置模板**：创建页面模板

### 内容更新流程
1. **获取当前内容**：读取页面块结构
2. **定位目标块**：找到需要更新的块
3. **更新块内容**：修改块文本或属性
4. **添加新块**：如需要，插入新内容块
5. **验证更新**：确认更改正确应用

### 项目跟踪流程
1. **创建项目数据库**：建立项目看板
2. **定义任务状态**：设置状态字段（待办、进行中、已完成）
3. **添加任务**：创建任务记录
4. **分配负责人**：设置任务负责人
5. **设置截止日期**：添加日期字段
6. **更新进度**：随进度更新状态

## 最佳实践

### 页面组织
- 使用层级结构组织页面
- 合理使用数据库代替普通页面
- 定期清理归档不需要的页面
- 使用图标和封面区分不同页面
- 建立统一的命名规范

### 数据库设计
- 字段类型选择要准确
- 合理使用关系字段连接数据库
- 设置默认视图提高使用效率
- 使用筛选条件减少噪音
- 定期维护数据库结构

### 内容编辑
- 使用块组织内容结构
- 合理使用标题层级
- 保持内容简洁明了
- 及时保存重要修改
- 使用评论进行讨论

### 协作规范
- 明确页面负责人
- 使用 @提及通知协作者
- 及时回复评论
- 定期同步更新状态
- 尊重页面权限设置

## 常用代码示例

### 1. 创建页面并添加内容
```javascript
// 创建新页面
const page = await createPage({
  parent: {
    type: "page_id",
    page_id: "parent_page_id"
  },
  properties: {
    title: {
      type: "title",
      title: [
        {
          type: "text",
          text: {
            content: "项目文档"
          }
        }
      ]
    }
  },
  children: [
    {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [
          {
            type: "text",
            text: {
              content: "这是项目文档的概述内容。"
            }
          }
        ]
      }
    }
  ],
  icon: {
    type: "emoji",
    emoji: "📝"
  },
  cover: {
    type: "external",
    external: {
      url: "https://example.com/cover.jpg"
    }
  }
});
```

### 2. 数据库操作
```javascript
// 创建数据库
const database = await createDatabase({
  parent: {
    type: "page_id",
    page_id: "parent_page_id"
  },
  title: [
    {
      type: "text",
      text: {
        content: "项目管理数据库"
      }
    }
  ],
  properties: {
    "任务名称": {
      title: {}
    },
    "状态": {
      select: {
        options: [
          { name: "待办", color: "gray" },
          { name: "进行中", color: "blue" },
          { name: "已完成", color: "green" }
        ]
      }
    },
    "负责人": {
      people: {}
    },
    "截止日期": {
      date: {}
    }
  }
});

// 查询数据库记录
const records = await queryDatabase({
  database_id: "database_id",
  filter: {
    property: "状态",
    select: {
      equals: "进行中"
    }
  },
  sorts: [
    {
      property: "截止日期",
      direction: "ascending"
    }
  ]
});
```

### 3. 页面搜索
```javascript
// 搜索页面
const searchResults = await search({
  query: "项目计划",
  filter: {
    property: "object",
    value: "page"
  },
  sort: {
    direction: "descending",
    timestamp: "last_edited_time"
  }
});

// 搜索数据库
const dbResults = await search({
  query: "任务",
  filter: {
    property: "object",
    value: "database"
  }
});
```

### 4. 块内容更新
```javascript
// 获取页面块
const blocks = await getBlockChildren({
  block_id: "page_id"
});

// 更新块内容
await updateBlock({
  block_id: "block_id",
  paragraph: {
    rich_text: [
      {
        type: "text",
        text: {
          content: "更新后的内容"
        }
      }
    ]
  }
});

// 添加新块
await appendBlockChildren({
  block_id: "parent_block_id",
  children: [
    {
      object: "block",
      type: "heading_2",
      heading_2: {
        rich_text: [
          {
            type: "text",
            text: {
              content: "新的章节标题"
            }
          }
        ]
      }
    }
  ]
});
```

### 5. 评论管理
```javascript
// 创建评论
await createComment({
  parent: {
    page_id: "page_id"
  },
  rich_text: [
    {
      type: "text",
      text: {
        content: "建议在这里添加更多细节描述。"
      }
    }
  ]
});

// 获取评论
const comments = await retrieveComments({
  block_id: "page_id"
});
```

### 6. 页面移动
```javascript
// 移动页面到其他父页面
await movePage({
  page_id: "page_id",
  parent: {
    type: "page_id",
    page_id: "new_parent_id"
  }
});

// 或移动到数据库
await movePage({
  page_id: "page_id",
  parent: {
    type: "database_id",
    database_id: "database_id"
  }
});
```

### 7. 批量操作
```javascript
// 批量创建页面记录
const batchCreate = async (databaseId, records) => {
  for (const record of records) {
    await createPage({
      parent: {
        type: "database_id",
        database_id: databaseId
      },
      properties: {
        "任务名称": {
          title: [{ text: { content: record.title } }]
        },
        "状态": {
          select: { name: record.status }
        }
      }
    });
  }
};

// 批量更新块
const batchUpdate = async (updates) => {
  for (const update of updates) {
    await updateBlock({
      block_id: update.blockId,
      ...update.content
    });
  }
};
```

### 8. 用户和权限
```javascript
// 获取用户信息
const users = await listUsers();

// 获取特定用户
const user = await getUser({
  user_id: "user_id"
});

// 获取当前用户
const me = await getSelf();
```

## 集成场景

### 1. 项目管理系统
- 创建项目概览页面
- 设置任务跟踪数据库
- 管理里程碑和时间线
- 生成项目报告
- 跟踪团队进度

### 2. 知识库管理
- 组织文档结构
- 创建知识库页面
- 维护文档索引
- 设置文档权限
- 定期更新内容

### 3. 内容创作工作流
- 创建内容日历
- 管理草稿和发布
- 协作编辑文档
- 追踪评论反馈
- 自动化内容发布

### 4. 团队协作平台
- 建立团队主页
- 管理团队成员
- 设置会议记录
- 共享资源和链接
- 跟踪团队任务

### 5. 自动化报告生成
- 收集数据更新
- 生成定期报告
- 导出报告内容
- 分发报告给团队
- 存档历史记录

## 注意事项
- 遵守 Notion API 速率限制
- 正确处理认证和权限
- 验证块类型和内容格式
- 保护敏感信息不被泄露
- 定期备份重要数据
- 注意页面和数据库的层级关系
- 使用正确的 ID 类型（page_id、database_id、block_id）
- 处理 API 错误和异常情况
- 遵守 Notion 的使用条款
- 尊重数据隐私和安全规范
