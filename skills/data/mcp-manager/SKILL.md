---
name: mcp-manager
description: MCP 服务器智能管理助手。自动检测 MCP 可用性、智能开关、功能问答，提供人性化的 MCP 管理体验。
---

# MCP 管理助手

智能管理 MCP (Model Context Protocol) 服务器，提供自动检测、智能开关和功能问答。

## 功能特性

### 1. **自动健康检测**
- 定期测试所有 MCP 服务器可用性
- 检测连接状态、响应时间、功能可用性
- 不可用时触发自动提醒

### 2. **智能开关管理**
- 根据使用频率自动关闭闲置 MCP
- 需要时自动启动对应 MCP
- 保存开关历史，支持手动控制

### 3. **人性化功能问答**
- 自然语言询问 MCP 功能
- 告诉你每个 MCP 能做什么、不能做什么
- 推荐最适合的 MCP 组合

## 使用方法

### 健康检测

```bash
# 检查所有 MCP 状态
mcp health check

# 检查特定 MCP
mcp health check github

# 持续监控（每分钟检查一次）
mcp health monitor
```

### 开关管理

```bash
# 列出所有 MCP 及状态
mcp list

# 启用 MCP
mcp enable github

# 禁用 MCP
mcp disable chrome-devtools

# 自动优化（关闭闲置 MCP）
mcp optimize

# 查看使用统计
mcp stats
```

### 功能问答

```
# 自然语言询问
"GitHub MCP 能做什么？"
"哪个 MCP 可以处理浏览器操作？"
"帮我总结一下所有 MCP 的功能"
"Chrome DevTools MCP 的局限性是什么？"
```

## MCP 功能库

### chrome-devtools
**能做什么：**
- 🌐 自动化浏览器操作（点击、输入、导航）
- 📸 截图和快照
- 🔍 网络请求监控
- 🐛 控制台日志查看
- ⚡ 性能分析

**不能做什么：**
- ❌ 需要 API key 的外部服务调用
- ❌ 代码执行（仅 JavaScript 评估）
- ❌ 文件系统访问

**适用场景：** 网页测试、数据抓取、UI 自动化

---

### github
**能做什么：**
- 📂 搜索仓库和代码
- 🔍 查看 Issue 和 PR
- 📊 获取仓库统计信息
- 🌿 分支和标签管理
- 👥 用户和仓库信息查询

**不能做什么：**
- ❌ 修改代码（只读操作）
- ❌ 创建/删除仓库
- ❌ 管理 Issues（需要额外权限）

**适用场景：** 代码搜索、仓库分析、协作信息查询

---

### context7
**能做什么：**
- 🧠 长期记忆存储
- 💾 保存和检索上下文
- 🔗 跨会话信息共享
- 📚 知识库管理

**不能做什么：**
- ❌ 实时数据处理
- ❌ 复杂数值计算
- ❌ 图像/视频处理

**适用场景：** 长期记忆、上下文保持、知识管理

---

### filesystem
**能做什么：**
- 📁 读取和写入文件
- 🔍 搜索文件内容
- 📋 列出目录结构
- 📝 创建和删除文件

**不能做什么：**
- ❌ 执行系统命令
- ❌ 访问受限目录
- ❌ 修改系统配置

**适用场景：** 文件操作、代码生成、文档处理

---

### browser
**能做什么：**
- 🌐 导航到网页
- 📸 页面截图
- 🔍 查看页面内容
- 🖱️ 基本点击操作

**不能做什么：**
- ❌ 复杂表单填写
- ❌ 多标签页管理
- ❌ JavaScript 执行

**适用场景：** 简单网页访问、内容抓取

---

## 智能建议系统

### 场景：网页自动化
**推荐 MCP：** `chrome-devtools`

```bash
# 自动启用
mcp enable chrome-devtools

# 其他关闭以节省资源
mcp disable context7
```

### 场景：代码搜索和分析
**推荐 MCP：** `github`

```bash
mcp enable github
mcp disable chrome-devtools
```

### 场景：长期记忆
**推荐 MCP：** `context7`

```bash
mcp enable context7
```

### 场景：文件操作
**推荐 MCP：** `filesystem`

```bash
mcp enable filesystem
```

---

## 健康检测机制

### 检测指标
- **连接状态**：MCP 进程是否运行
- **响应时间**：调用响应延迟
- **功能测试**：执行简单操作测试
- **错误率**：近期失败次数

### 检测频率
- 实时检测：每次使用前检查
- 定期检测：每小时一次
- 深度检测：每天一次（完整功能测试）

### 失败提醒
检测到 MCP 不可用时：
```
⚠️ MCP Alert: github

状态: 不可用
错误: Connection timeout
建议: 1. 检查网络连接 2. 验证 API token 3. 重启 MCP

[自动禁用] github 已自动禁用
```

---

## 自动优化策略

### 闲置检测
- 30分钟未使用 → 标记为候选关闭
- 1小时未使用 → 自动关闭（除非手动启用）
- 持续使用 → 保持启用

### 资源占用优先级
**高优先级（始终保持启用）：**
- filesystem（文件操作）
- 当前项目必需的 MCP

**低优先级（可自动关闭）：**
- chrome-devtools（资源占用高）
- context7（可选功能）

### 智能预测
根据用户历史行为预测需求：
```
用户经常：上午代码搜索 + 下午网页自动化

预测：
- 09:00-12:00: 启用 github
- 14:00-18:00: 启用 chrome-devtools
- 其他时间: 两者都关闭
```

---

## 使用示例

### 示例 1：自动健康监控

```bash
# 启动监控服务
mcp health monitor

# 输出示例：
🔍 MCP Health Monitor
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ chrome-devtools: OK (45ms)
✅ github: OK (120ms)
✅ context7: OK (89ms)

[Last check: 2026-01-31 17:50:00]
[Next check: 2026-01-31 17:51:00]
```

### 示例 2：功能问答

```
用户: "chrome-devtools 能做什么？"

助手: 🎯 Chrome DevTools MCP 功能概览

✅ 强项：
  • 网页自动化 - 点击、输入、导航
  • 截图和快照 - 可视化页面状态
  • 网络监控 - 查看请求和响应
  • 性能分析 - 页面加载性能

⚠️ 局限：
  • 需要 Chrome 浏览器运行
  • 无法访问受限网站
  • JavaScript 评估受限

💡 适用场景：
  • 网页测试自动化
  • 数据抓取
  • UI 交互测试

需要我帮你启用它吗？
```

### 示例 3：智能优化

```bash
mcp optimize

# 输出：
📊 MCP 使用分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━

活跃 MCP (3个):
  • github - 使用: 15次/小时 ✅ 保持启用
  • filesystem - 使用: 8次/小时 ✅ 保持启用
  • chrome-devtools - 使用: 0次 (闲置30分钟)

闲置 MCP (2个):
  • context7 - 未使用2小时
  • browser - 未使用4小时

🔧 优化建议:
  关闭 chrome-devtools (节省 ~200MB 内存)
  关闭 context7 (节省 ~50MB 内存)

[应用优化] y/N? y
✅ 已优化，节省 ~250MB 内存
```

---

## 配置文件

### ~/.mcp-manager/config.json

```json
{
  "healthCheck": {
    "interval": 3600,
    "timeout": 10,
    "retryCount": 3
  },
  "autoOptimize": {
    "enabled": true,
    "idleTimeout": 3600,
    "saveHistory": true
  },
  "notifications": {
    "enabled": true,
    "channels": ["whatsapp", "console"],
    "urgency": "high"
  },
  "preferences": {
    "alwaysKeep": ["filesystem"],
    "autoClose": ["chrome-devtools", "context7"]
  }
}
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `mcp list` | 列出所有 MCP |
| `mcp status [name]` | 查看 MCP 状态 |
| `mcp enable <name>` | 启用 MCP |
| `mcp disable <name>` | 禁用 MCP |
| `mcp health check` | 健康检查 |
| `mcp health monitor` | 持续监控 |
| `mcp optimize` | 自动优化 |
| `mcp stats` | 使用统计 |
| `mcp help <name>` | MCP 功能说明 |

---

## 最佳实践

### 1. 按需启用
只在需要时启用资源密集型 MCP（如 chrome-devtools）

### 2. 定期优化
每天运行 `mcp optimize` 清理闲置 MCP

### 3. 监控健康
启动 `mcp health monitor` 持续监控

### 4. 功能先行
不确定需求时，先询问"哪个 MCP 能做 X？"

### 5. 保留必需
设置 `alwaysKeep` 配置，确保核心 MCP 始终可用

---

## 故障排查

### MCP 无法启动
```bash
# 查看详细日志
mcp status github --verbose

# 检查配置
cat ~/.claude.json | grep -A 10 github

# 测试连接
mcp health check github --debug
```

### 资源占用过高
```bash
# 查看占用
mcp stats

# 优化
mcp optimize --aggressive

# 手动关闭
mcp disable chrome-devtools
```

### 频繁掉线
```bash
# 检查健康检测
mcp health check --full

# 调整超时设置
# 编辑 config.json，增加 timeout 值

# 启用自动重连
mcp config set autoReconnect true
```

---

## 开发计划

### v1.0 (当前)
- ✅ 基础健康检测
- ✅ 手动开关管理
- ✅ 功能问答

### v1.1 (计划中)
- ⏳ 自动开关
- ⏳ 智能预测
- ⏳ 使用统计

### v2.0 (未来)
- ⏳ MCP 性能优化建议
- ⏳ 自动依赖解决
- ⏳ MCP 更新管理

---

## 贡献

欢迎提交 Issue 和 PR！

---

让 MCP 管理变得简单智能 🚀
