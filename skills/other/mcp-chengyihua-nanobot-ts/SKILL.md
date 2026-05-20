---
name: mcp
description: MCP（Model Context Protocol）集成技能，支持自动安装、配置和使用MCP服务器，连接各种数据源和工具。当用户需要让AI模型安全访问外部数据源、数据库、API或文件系统时使用此技能。
metadata: {"nanobot":{"emoji":"🔌","requires":{"bins":["node","npm"]},"install":[{"id":"mcp-server","kind":"command","command":"npm install -g @modelcontextprotocol/server @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-sqlite @modelcontextprotocol/server-http","label":"Install MCP Servers"}]}}
---

# MCP（Model Context Protocol）集成技能

## 什么是MCP？

MCP是Anthropic推出的协议，允许AI模型**安全地访问外部工具和数据源**，而无需直接集成到模型中。

### 核心优势：
1. **安全性**：模型不能直接执行代码，只能通过MCP服务器访问
2. **灵活性**：可以连接各种数据源（数据库、API、文件系统等）
3. **标准化**：统一的协议，不同模型都可以使用

## 快速开始

### 1. 安装MCP服务器

```bash
# 安装常用MCP工具
npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-sqlite @modelcontextprotocol/server-http
```

### 2. 启动MCP服务器

```bash
# 启动文件系统服务器
npx @modelcontextprotocol/server-filesystem --directory /path/to/data

# 启动SQLite服务器
npx @modelcontextprotocol/server-sqlite --database /path/to/database.db

# 启动HTTP服务器
npx @modelcontextprotocol/server-http --port 8080
```

### 3. 在nanobot中配置MCP

```javascript
// 在nanobot配置中添加MCP支持
const { createMCPClient } = require('@ai-sdk/openai');

const mcpClient = createMCPClient({
  transport: 'stdio',
  command: 'mcp-server',
  args: ['filesystem', '--directory', '/path/to/data']
});
```

## 常用MCP服务器

### 1. 文件系统服务器
```bash
# 访问本地文件系统
mcp-server filesystem --directory /Users/chengyihua/Documents

# 使用示例：读取文件列表
curl -X POST http://localhost:8080/tools/list \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/chengyihua/Documents"}'
```

### 2. SQLite服务器
```bash
# 连接SQLite数据库
mcp-server sqlite --database /path/to/database.db

# 使用示例：执行SQL查询
curl -X POST http://localhost:8080/tools/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM users LIMIT 10"}'
```

### 3. HTTP服务器
```bash
# 启动HTTP API服务器
mcp-server http --port 8080

# 使用示例：调用API
curl -X POST http://localhost:8080/tools/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://api.example.com/data", "method": "GET"}'
```

### 4. PostgreSQL服务器
```bash
# 连接PostgreSQL数据库
mcp-server postgres --connection-string "postgresql://user:password@localhost:5432/dbname"
```

### 5. GitHub服务器
```bash
# 访问GitHub API
mcp-server github --token YOUR_GITHUB_TOKEN
```

## 在nanobot中使用MCP

### 1. 配置MCP客户端

```javascript
// 在nanobot的agent配置中添加
const mcpConfig = {
  servers: [
    {
      name: 'filesystem',
      transport: 'stdio',
      command: 'mcp-server',
      args: ['filesystem', '--directory', process.cwd()]
    },
    {
      name: 'sqlite',
      transport: 'stdio', 
      command: 'mcp-server',
      args: ['sqlite', '--database', '/path/to/data.db']
    }
  ]
};
```

### 2. 使用MCP工具

```javascript
// 通过MCP访问文件系统
const files = await mcpClient.callTool('filesystem.list', {
  path: '/Users/chengyihua/Documents'
});

// 通过MCP执行SQL查询
const results = await mcpClient.callTool('sqlite.query', {
  sql: 'SELECT * FROM products WHERE price > 100'
});

// 通过MCP调用HTTP API
const response = await mcpClient.callTool('http.fetch', {
  url: 'https://api.example.com/data',
  method: 'GET'
});
```

## 自动安装脚本

### 安装脚本 (scripts/install_mcp.sh)

```bash
#!/bin/bash

# MCP自动安装脚本
echo "开始安装MCP..."

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "安装Node.js..."
    brew install node
fi

# 安装MCP服务器
echo "安装MCP服务器..."
npm install -g @modelcontextprotocol/server

# 安装常用MCP工具
echo "安装MCP工具..."
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-sqlite
npm install -g @modelcontextprotocol/server-http
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-github

# 验证安装
echo "验证安装..."
mcp-server --version

echo "MCP安装完成！"
```

### 启动脚本 (scripts/start_mcp.sh)

```bash
#!/bin/bash

# 启动MCP服务器
echo "启动MCP服务器..."

# 启动文件系统服务器
mcp-server filesystem --directory /Users/chengyihua/Documents &

# 启动SQLite服务器（如果有数据库）
if [ -f "/path/to/database.db" ]; then
    mcp-server sqlite --database /path/to/database.db &
fi

# 启动HTTP服务器
mcp-server http --port 8080 &

echo "MCP服务器已启动"
echo "文件系统服务器: 访问本地文件"
echo "HTTP服务器: http://localhost:8080"
```

## 使用示例

### 示例1：通过MCP读取文件

```bash
# 使用curl调用MCP服务器
curl -X POST http://localhost:8080/tools/read \
  -H "Content-Type: application/json" \
  -d '{"path": "/Users/chengyihua/Documents/example.txt"}'
```

### 示例2：通过MCP查询数据库

```bash
# 查询SQLite数据库
curl -X POST http://localhost:8080/tools/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT name, price FROM products ORDER BY price DESC LIMIT 5"}'
```

### 示例3：通过MCP调用GitHub API

```bash
# 获取GitHub仓库信息
curl -X POST http://localhost:8080/tools/github \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "/repos/owner/repo", "method": "GET"}'
```

## 故障排除

### 常见问题

#### 1. MCP服务器无法启动
```bash
# 检查端口占用
lsof -i :8080

# 检查MCP安装
mcp-server --version
```

#### 2. 连接被拒绝
```bash
# 检查防火墙设置
sudo ufw status

# 检查MCP服务器日志
tail -f /var/log/mcp-server.log
```

#### 3. 权限问题
```bash
# 检查文件权限
ls -la /path/to/data

# 以正确用户运行
sudo -u username mcp-server filesystem --directory /path/to/data
```

### 调试模式

```bash
# 启用调试日志
DEBUG=mcp:* mcp-server filesystem --directory /path/to/data

# 详细日志
mcp-server filesystem --directory /path/to/data --verbose
```

## 安全最佳实践

### 1. 访问控制
```bash
# 使用认证令牌
mcp-server filesystem --directory /path/to/data --token SECRET_TOKEN

# 限制访问IP
mcp-server http --port 8080 --allowed-ips 192.168.1.0/24
```

### 2. 数据加密
```bash
# 使用HTTPS
mcp-server http --port 8443 --ssl-cert /path/to/cert.pem --ssl-key /path/to/key.pem
```

### 3. 审计日志
```bash
# 启用访问日志
mcp-server filesystem --directory /path/to/data --log-file /var/log/mcp-access.log
```

## 高级配置

### 1. 多服务器配置
```json
{
  "servers": [
    {
      "name": "production-db",
      "transport": "stdio",
      "command": "mcp-server",
      "args": ["postgres", "--connection-string", "postgresql://user:pass@prod-db:5432/prod"]
    },
    {
      "name": "development-fs",
      "transport": "stdio",
      "command": "mcp-server", 
      "args": ["filesystem", "--directory", "/home/dev/data"]
    }
  ]
}
```

### 2. 负载均衡
```bash
# 启动多个MCP实例
mcp-server http --port 8081 &
mcp-server http --port 8082 &
mcp-server http --port 8083 &

# 使用负载均衡器
nginx -c /path/to/nginx-mcp.conf
```

### 3. 监控和指标
```bash
# 启用Prometheus指标
mcp-server http --port 8080 --metrics-port 9090

# 查看健康检查
curl http://localhost:8080/health
```

## 参考资料

### 官方文档
- [MCP官方文档](https://modelcontextprotocol.io)
- [MCP GitHub仓库](https://github.com/modelcontextprotocol)
- [MCP服务器列表](https://github.com/modelcontextprotocol/servers)

### 社区资源
- [MCP示例项目](https://github.com/modelcontextprotocol/examples)
- [MCP最佳实践](https://modelcontextprotocol.io/docs/best-practices)
- [MCP故障排除](https://modelcontextprotocol.io/docs/troubleshooting)

### 相关工具
- [MCP客户端库](https://www.npmjs.com/package/@modelcontextprotocol/sdk)
- [MCP服务器SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk-server)
- [MCP浏览器扩展](https://github.com/modelcontextprotocol/browser-extension)
