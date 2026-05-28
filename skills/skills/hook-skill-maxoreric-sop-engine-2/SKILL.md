---
name: hook-skill
description: Claude Code Hook 开发专家。当需要创建、调试、配置 Hook 时触发。触发词：创建 hook、写 hook、hook 配置、stop hook、pre tool use、post tool use、session start。
---

# Hook 开发

创建和配置 Claude Code Hooks，用于在特定事件时执行自定义逻辑。

## Hook 基础

### 什么是 Hook？

Hook 是在 Claude Code 执行过程中特定时机自动触发的脚本或命令。可以用于：
- 验证和拦截工具调用
- 自动批准特定操作
- 添加上下文信息
- 实现循环执行
- 通知和日志记录

### 10 种 Hook 事件

| 事件 | 触发时机 | 常见用途 |
|-----|---------|---------|
| **PreToolUse** | 工具执行前 | 验证、拦截、修改输入 |
| **PostToolUse** | 工具执行后 | 验证结果、触发后续 |
| **PermissionRequest** | 权限对话框显示时 | 自动批准/拒绝 |
| **UserPromptSubmit** | 用户提交 prompt 时 | 添加上下文、验证 |
| **Stop** | Claude 完成响应时 | 实现循环、强制继续 |
| **SubagentStop** | Subagent 完成时 | 链式触发、验证完成 |
| **PreCompact** | 压缩操作前 | 保存状态 |
| **SessionStart** | 会话开始时 | 加载上下文、初始化 |
| **SessionEnd** | 会话结束时 | 清理、保存状态 |
| **Notification** | 通知时 | 自定义通知 |

### Exit Code 含义

| Exit Code | 含义 | 效果 |
|-----------|------|------|
| **0** | 成功 | 继续执行，stdout 可返回 JSON |
| **2** | 阻止 | 阻止操作，stderr 反馈给 Claude |
| **其他** | 非阻止错误 | 显示警告，继续执行 |

## 配置结构

### hooks.json 格式

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### 字段说明

- **matcher**：工具名匹配模式（仅 PreToolUse、PostToolUse、PermissionRequest）
  - 精确匹配：`Write`
  - 正则匹配：`Edit|Write`、`Notebook.*`
  - 匹配所有：`*` 或省略
- **type**：`command`（bash 命令）或 `prompt`（LLM 评估）
- **command**：要执行的命令
- **timeout**：超时时间（秒），默认 60

### 环境变量

- `$CLAUDE_PROJECT_DIR`：项目根目录
- `$CLAUDE_PLUGIN_ROOT`：插件根目录（插件 Hook 专用）
- `$CLAUDE_ENV_FILE`：环境变量文件（仅 SessionStart）

## Hook 输入（stdin JSON）

### 通用字段

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

### PreToolUse 输入

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

### Stop 输入

```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": true  // 是否已被 Stop hook 继续过
}
```

### UserPromptSubmit 输入

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "用户的 prompt 内容"
}
```

### SessionStart 输入

```json
{
  "hook_event_name": "SessionStart",
  "source": "startup"  // startup | resume | clear | compact
}
```

## Hook 输出（JSON）

### PreToolUse 控制

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",  // allow | deny | ask
    "permissionDecisionReason": "原因",
    "updatedInput": { }  // 可选：修改输入
  }
}
```

### Stop 控制

```json
{
  "decision": "block",  // block = 阻止停止，继续执行
  "reason": "告诉 Claude 为什么要继续"
}
```

### UserPromptSubmit 控制

```json
{
  "decision": "block",  // 可选：阻止 prompt
  "reason": "阻止原因",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "添加的上下文"
  }
}
```

### SessionStart 控制

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "启动时添加的上下文"
  }
}
```

## 常用模式

### 1. 实现循环执行（Stop Hook）

```bash
#!/bin/bash
# stop-loop.sh - 阻止停止，让 Claude 继续

HOOK_INPUT=$(cat)
STOP_ACTIVE=$(echo "$HOOK_INPUT" | jq -r '.stop_hook_active // false')

# 检查状态文件
if [ -f ".loop-status.json" ]; then
    CURRENT=$(jq -r '.current // 0' .loop-status.json)
    MAX=$(jq -r '.max // 5' .loop-status.json)
    
    if [ "$CURRENT" -lt "$MAX" ]; then
        # 更新计数
        jq ".current = $((CURRENT + 1))" .loop-status.json > .tmp && mv .tmp .loop-status.json
        # 阻止停止
        echo "继续执行 ($((CURRENT + 1))/$MAX)" >&2
        exit 2
    fi
fi

exit 0
```

### 2. 自动批准文档文件读取

```python
#!/usr/bin/env python3
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name == "Read":
    file_path = tool_input.get("file_path", "")
    if file_path.endswith((".md", ".txt", ".json")):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "文档文件自动批准"
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

### 3. 添加时间上下文（SessionStart）

```bash
#!/bin/bash
# session-start.sh

echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "项目目录: $CLAUDE_PROJECT_DIR"

# 如果有 CLAUDE_ENV_FILE，设置环境变量
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "export PROJECT_START_TIME=$(date +%s)" >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

### 4. 验证 Bash 命令（PreToolUse）

```python
#!/usr/bin/env python3
import json
import sys
import re

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

if tool_name != "Bash":
    sys.exit(0)

command = tool_input.get("command", "")

# 危险命令检查
dangerous_patterns = [
    (r"\brm\s+-rf\s+/", "禁止删除根目录"),
    (r"\bsudo\b", "禁止使用 sudo"),
]

for pattern, message in dangerous_patterns:
    if re.search(pattern, command):
        print(message, file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

### 5. Prompt 类型 Hook（LLM 评估）

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "评估 Claude 是否应该停止。检查：1. 所有任务是否完成 2. 是否有错误需要处理。返回 JSON: {\"decision\": \"approve\" 或 \"block\", \"reason\": \"原因\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 调试

### 基本调试

```bash
# 查看 Hook 执行详情
claude --debug

# 检查 Hook 配置
# 在 Claude Code 中运行 /hooks
```

### 常见问题

1. **Hook 不触发**
   - 检查 matcher 是否正确（大小写敏感）
   - 检查 hooks.json 语法
   - 运行 `/hooks` 查看注册状态

2. **命令找不到**
   - 使用绝对路径
   - 检查执行权限 `chmod +x script.sh`

3. **JSON 解析失败**
   - 确保输出是有效 JSON
   - 检查引号转义

## 安全注意

- Hook 以当前用户权限运行
- 始终验证和清理输入
- 使用引号包裹变量：`"$VAR"`
- 检查路径遍历：`..`
- 敏感文件要跳过：`.env`、`.git/`

## 创建 Hook 的步骤

1. **确定事件** - 选择合适的 Hook 事件
2. **设计逻辑** - 确定输入输出和处理逻辑
3. **编写脚本** - Python 或 Bash
4. **配置 hooks.json** - 添加到配置文件
5. **测试** - 使用 `--debug` 调试
6. **设置权限** - `chmod +x`

## 参考

官方文档：`site:code.claude.com hooks`
