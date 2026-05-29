---
name: hook-creator
description: 创建和配置 Claude Code 钩子以自定义代理行为。当用户需要以下操作时使用：(1) 创建新钩子，(2) 配置自动格式化、日志记录或通知，(3) 添加文件保护或自定义权限，(4) 设置工具执行前后的操作，(5) 询问钩子事件如 PreToolUse、PostToolUse、Notification 等。
---

# Hook 钩子创建器

创建在特定生命周期事件中执行 shell 命令的 Claude Code 钩子。

## 钩子创建工作流程

1. **确定使用场景** - 明确钩子需要完成的功能
2. **选择合适的事件** - 从可用的钩子事件中选择（参见 references/hook-events.md）
3. **设计钩子命令** - 编写从 stdin 处理 JSON 输入的 shell 命令
4. **配置匹配器** - 设置工具/事件过滤器（使用 `*` 匹配所有，或指定工具名称如 `Bash`、`Edit|Write`）
5. **选择存储位置** - 用户设置（`~/.claude/settings.json`）或项目（`.claude/settings.json`）
6. **测试钩子** - 使用简单测试用例验证行为

## 钩子配置结构

```json
{
  "hooks": {
    "<事件名称>": [
      {
        "matcher": "<工具模式>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell命令>"
          }
        ]
      }
    ]
  }
}
```

## 常用模式

### 读取输入数据

钩子通过 stdin 接收 JSON。使用 `jq` 提取字段：

```bash
# 提取工具输入字段
jq -r '.tool_input.file_path'

# 带默认值的提取
jq -r '.tool_input.description // "无描述"'

# 条件处理
jq -r 'if .tool_input.file_path then .tool_input.file_path else empty end'
```

### PreToolUse 的退出代码

- `0` - 允许工具继续执行
- `2` - 阻止工具并向 Claude 提供反馈

### 匹配器模式

- `*` - 匹配所有工具
- `Bash` - 仅匹配 Bash 工具
- `Edit|Write` - 匹配 Edit 或 Write 工具
- `Read` - 匹配 Read 工具

## 快速示例

**记录所有 bash 命令：**

```bash
jq -r '"\(.tool_input.command)"' >> ~/.claude/bash-log.txt
```

**编辑后自动格式化 TypeScript：**

```bash
jq -r '.tool_input.file_path' | { read f; [[ "$f" == *.ts ]] && npx prettier --write "$f"; }
```

**阻止编辑 .env 文件：**

```bash
python3 -c "import json,sys; p=json.load(sys.stdin).get('tool_input',{}).get('file_path',''); sys.exit(2 if '.env' in p else 0)"
```

## 资源文档

- **钩子事件参考**：查看 `references/hook-events.md` 了解详细的事件文档，包含输入/输出架构
- **示例配置**：查看 `references/examples.md` 获取完整的、经过测试的钩子配置