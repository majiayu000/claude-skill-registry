---
name: feishu-mcp
description: 飞书全能 MCP - 创建/编辑文档、插入图表、管理表格、搜索知识库。整合社区版+官方 MCP，适配 Moltbot/Clawdbot。
metadata: {"clawdbot":{"emoji":"📘","requires":{"bins":["mcporter"]}}}
---

# 飞书全能 MCP

整合社区版 feishu-mcp（文档编辑）+ 官方 lark-mcp（多维表格/搜索），让 Clawdbot 完整操作飞书。

## 快速配置

```bash
curl -fsSL https://raw.githubusercontent.com/AlexAnys/feishu-mcp/main/setup.sh | bash
```

## 三个 MCP 服务

| 服务 | 来源 | 能力 |
|------|------|------|
| `feishu` | 社区版 | 创建/编辑文档、图表、图片 |
| `lark` | 官方 | 多维表格、发消息 |
| `lark-user` | 官方 | 搜索文档、读取知识库 |

## 主要工具

### 文档操作 (feishu)
```bash
# 创建文档
mcporter call feishu.create_feishu_document --args '{"title":"新文档"}'

# 添加内容
mcporter call feishu.batch_create_feishu_blocks --args '{"document_id":"xxx","blocks":[...]}'

# 插入表格
mcporter call feishu.create_feishu_table --args '{"document_id":"xxx","rows":3,"cols":3}'
```

### 多维表格 (lark)
```bash
# 创建表格
mcporter call lark.bitable_v1_app_create --args '{"data":{"name":"项目表"}}'

# 写入记录
mcporter call lark.bitable_v1_appTableRecord_create --args '{"path":{"app_token":"xxx","table_id":"xxx"},"data":{"fields":{"标题":"任务1"}}}'
```

### 搜索 (lark-user)
```bash
# 搜索文档
mcporter call lark-user.docx_builtin_search --args '{"data":{"search_key":"会议","count":5}}'

# 读取内容
mcporter call lark-user.docx_v1_document_rawContent --args '{"path":{"document_id":"xxx"}}'

# 搜索知识库
mcporter call lark-user.wiki_v1_node_search --args '{"data":{"query":"入职"}}'
```

## 权限配置

飞书开放平台开通：
- `docx:document` - 读写文档
- `drive:drive` - 云空间
- `wiki:wiki` - 知识库
- `bitable:app` - 多维表格
- `search:docs:read` - 搜索

重定向 URL：
- `http://localhost:3000/callback`
- `http://localhost:3333/callback`

## 详细文档

https://github.com/AlexAnys/feishu-mcp
