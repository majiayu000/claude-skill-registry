---
name: zhimeng-agent
description: |
  zhimeng's Agent 智能助手操作技能。
  触发场景：用户提到"问知识库"、"发日报"、"检查Agent"、"重建索引"、"知识问答"等。
---

# zhimeng's Agent 操作技能

## 概述

zhimeng's Agent 是基于 Obsidian 知识库的 RAG 智能问答助手，由 Claude Opus 4.5 驱动。支持知识库问答、日报同步、飞书消息推送等功能。

## 服务信息

| 项目 | 值 |
|------|-----|
| 服务地址 | `http://localhost:8001` |
| 项目路径 | `/Users/qitmac001395/workspace/QAL/ideas/apps/zhimeng-agent` |
| 知识库路径 | `/Users/qitmac001395/Documents/Obsidian Vault` |
| 向量数据库 | ChromaDB (`data/chroma/`) |
| LLM 模型 | `anthropic/claude-sonnet-4-20250514` |

## 核心能力

| 能力 | 端点 | 用途 | 示例触发词 |
|------|------|------|-----------|
| 知识问答 | `POST /ask` | 基于知识库的 RAG 问答 | "问知识库"、"查一下" |
| 健康检查 | `GET /health` | 检查服务状态和文档数量 | "检查Agent"、"服务状态" |
| 重建索引 | `POST /index` | 重新索引 Obsidian 文档 | "重建索引"、"更新知识库" |
| 飞书Webhook | `POST /webhook/feishu` | 接收飞书消息事件 | - |

## API 详细说明

### 1. 问答接口 (`POST /ask`)

**请求体**:
```json
{
  "question": "用户问题",
  "top_k": 5,
  "include_sources": true,
  "filter_folder": null,
  "user_id": "用户唯一标识"
}
```

**响应体**:
```json
{
  "answer": "回答内容",
  "sources": [
    {"file": "文件名.md", "folder": "文件夹", "relevance": 0.85}
  ],
  "tokens_used": 1234
}
```

**参数说明**:
- `question` (必填): 用户问题
- `top_k` (可选, 默认5): 检索文档数量 (1-20)
- `include_sources` (可选, 默认true): 是否返回来源
- `filter_folder` (可选): 限定搜索的文件夹
- `user_id` (可选): 用户标识，用于对话记忆

### 2. 健康检查 (`GET /health`)

**响应体**:
```json
{
  "status": "healthy",
  "vectorstore_loaded": true,
  "document_count": 1316
}
```

### 3. 重建索引 (`POST /index`)

**请求体**:
```json
{
  "paths": ["Journal", "Projects"],
  "force": false
}
```

**响应体**:
```json
{
  "status": "success",
  "chunks_indexed": 1500
}
```

## 标准操作流程 (SOP)

### SOP 1: 知识库问答

```
步骤1: 检查服务状态
  curl http://localhost:8001/health

步骤2: 发送问题
  curl -X POST http://localhost:8001/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "你的问题", "top_k": 5}'

步骤3: 解析响应中的 answer 和 sources
```

### SOP 2: 日报同步到飞书

```
步骤1: 读取今日日报
  读取 ~/Documents/Obsidian Vault/Journal/YYYYMMDD.md

步骤2: 提取关键内容
  - 完成的工作
  - 代码变更统计
  - AI 消耗统计

步骤3: 格式化为飞书消息
  使用 feishu-messaging 技能发送

步骤4: 发送到目标用户
  调用 mcp__feishu__im_v1_message_create
  收件人: 王植萌 (open_id: ou_18b8063b232cbdec73ea1541dfb74890)
```

### SOP 3: 重建知识库索引

```
步骤1: 停止正在进行的查询

步骤2: 调用索引接口
  curl -X POST http://localhost:8001/index \
    -H "Content-Type: application/json" \
    -d '{"force": true}'

步骤3: 验证索引结果
  curl http://localhost:8001/health
  确认 document_count 已更新
```

### SOP 4: 启动/停止服务

**启动服务**:
```bash
cd /Users/qitmac001395/workspace/QAL/ideas/apps/zhimeng-agent
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**启动飞书长连接** (本地开发，无需公网IP):
```bash
cd /Users/qitmac001395/workspace/QAL/ideas/apps/zhimeng-agent
poetry run python src/feishu_ws.py
```

**后台启动**:
```bash
# 主服务
nohup poetry run uvicorn src.main:app --host 0.0.0.0 --port 8001 > /tmp/zhimeng-agent.log 2>&1 &

# 飞书长连接
nohup poetry run python src/feishu_ws.py > feishu_ws.log 2>&1 &
```

## 与其他技能的集成

### 集成 feishu-messaging

日报同步工作流:
1. 本技能读取 Obsidian 日报
2. 格式化内容
3. 调用 `feishu-messaging` 技能发送消息

### 集成 obsidian-organize

知识库维护工作流:
1. 使用 `obsidian-organize` 整理文档结构
2. 触发本技能的 `/index` 重建索引
3. 验证检索质量

## 常见问题

### Q: 服务无法启动？

检查:
1. Python 环境: `poetry install`
2. 端口占用: `lsof -i :8001`
3. 环境变量: `config/.env` 是否存在

### Q: 检索结果不准确？

尝试:
1. 重建索引: `POST /index {"force": true}`
2. 增加 top_k 值
3. 使用 filter_folder 限定范围

### Q: 飞书长连接断开？

检查:
1. 网络连接
2. App 凭证是否过期
3. 查看日志: `tail -f feishu_ws.log`

## 配置文件

### config/.env

```env
# LLM 配置
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=sk-ant-xxx

# 飞书配置
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx

# 服务配置
HOST=0.0.0.0
PORT=8001
DEBUG=true
```

### config/settings.py

主要配置项:
- `obsidian_vault_path`: 知识库路径
- `chroma_persist_dir`: 向量数据库持久化目录
- `chunk_size`: 文档分块大小 (默认1000)
- `chunk_overlap`: 分块重叠 (默认200)

## 监控与日志

### 日志位置
- 主服务: 标准输出 或 `/tmp/zhimeng-agent.log`
- 飞书长连接: `feishu_ws.log`

### 关键日志模式
```
INFO:src.retriever:检索到 X 个相关文档  # 检索成功
INFO:httpx:HTTP Request: POST https://api.anthropic.com/v1/messages  # LLM 调用
INFO:src.smart_agent:已更新用户 xxx 的对话历史  # 对话记忆更新
```

## 注意事项

1. **API 密钥安全**: `.env` 文件不要提交到 Git
2. **成本控制**: 每次问答约消耗 Claude API $0.01-0.05
3. **索引时间**: 完整重建约需 2-5 分钟 (取决于文档数量)
4. **对话记忆**: 基于 user_id 隔离，无 user_id 时不保留历史
5. **飞书长连接**: 需要 App 开启"机器人消息长连接"能力
