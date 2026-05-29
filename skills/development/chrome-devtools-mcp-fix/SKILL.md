---
name: chrome-devtools-mcp-fix
description: 修复 chrome-devtools MCP 连接问题。当用户遇到 chrome-devtools disconnected、MCP 连接失败、autoConnect 不工作时触发。
---

# Chrome DevTools MCP 连接修复

## 前提条件

1. Chrome 已启动
2. 已在 `chrome://inspect/#remote-debugging` 启用远程调试

## 修复步骤

```bash
bash ~/.factory/skills/chrome-devtools-mcp-fix/scripts/update-mcp-config.sh
```

然后重启 Droid。

## 注意

Chrome 重启后 browser ID 会变，需要重新运行脚本。
