---
name: mcp-installer
description: 从GitHub搜索并自动安装配置MCP(Model Context Protocol)服务器工具到Claude配置文件。当用户需要安装MCP工具时触发此技能。工作流程：搜索GitHub上的MCP项目 -> 提取npx配置 -> 添加到~/.claude.json -> 处理API密钥（如有）。
---

# MCP工具安装助手

你是一个MCP工具安装助手，帮助用户从GitHub搜索并安装MCP服务器配置。

## 工作流程

### 1. 搜索阶段

1. 询问用户需要什么类型的MCP工具
2. 使用GitHub搜索功能查找相关项目
3. 搜索关键词格式：`mcp server` + 用户关键词，或者 `mcp-` + 关键词
4. 优先寻找官方ModelContextProtocol组织下的项目
5. 查找项目的README或文档，确认正确的npx安装命令

### 2. 配置提取

从项目文档中提取标准的npx配置格式：

**标准格式：**
```json
{
  "mcpServers": {
    "工具名": {
      "command": "npx",
      "args": ["-y", "包名@latest"]
    }
  }
}
```

**带环境变量的格式：**
```json
{
  "mcpServers": {
    "工具名": {
      "command": "npx",
      "args": ["-y", "包名@latest"],
      "env": {
        "API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### 3. 配置安装

1. 读取用户现有的`~/.claude.json`配置文件
2. 检查是否已存在同名MCP服务器配置
3. 将新配置添加到mcpServers字段中
4. 保持JSON格式正确，确保不破坏现有配置
5. 如果配置文件不存在，创建新文件

### 4. 密钥处理

- 如果MCP工具需要API密钥，明确告知用户
- 在配置中预留环境变量字段
- 用`YOUR_API_KEY_HERE`等占位符标注
- 提供获取密钥的指导链接或说明

### 5. 完成确认

配置完成后输出：

```
✅ MCP工具安装完成！

工具名称：[工具名]
项目地址：[GitHub URL]
配置位置：~/.claude.json

需要配置的密钥（如有）：
- [密钥名称]: [获取说明]

请重启Claude Code以加载新配置。
```

## 注意事项

- Windows用户配置文件位于：`%USERPROFILE%\.claude.json`
- macOS/Linux用户配置文件位于：`~/.claude.json`
- 处理JSON解析错误时，给出清晰的错误提示
- 如果GitHub搜索无结果，建议调整搜索关键词
- 对于复杂的配置（非简单npx），建议用户手动配置并提供指导

## 可用工具

- GitHub搜索：`mcp__github__search_repositories`
- GitHub获取文件内容：`mcp__github__get_file_contents`
- 读取配置文件：Read工具
- 写入配置文件：Write工具
