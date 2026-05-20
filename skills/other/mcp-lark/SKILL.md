---
name: mcp-lark
description: Based on FeiShu(飞书) / Lark's OpenAPI MCP server, manage user information, chats, emails, cloud documents, multidimensional tables, tasks, calendars, etc.
---

# MCP Lark / FeiShu
Need to login to the Lark MCP Configuration Platform to add MCP services, obtain the MCP URL, and configure it into environment variables.
- Lark MCP docs: https://open.larksuite.com/document/mcp_open_tools/call-feishu-mcp-server-in-remote-mode
- 飞书 MCP 文档: https://open.feishu.cn/document/mcp_open_tools/end-user-call-remote-mcp-server

## Environment variables
Prioritize fetching from `.env` under the workspace, then use system environment variables. If not configured, ask the user for input and update it to `.env`.
```shell
# Configure multiple MCP service URLs and usage scenarios in environment variables
LARK_MCP_SERVERS='
open.larksuite.com/mcp/stream/xxx:Chats and Mails;
open.larksuite.com/mcp/stream/yyy:Cloud documents;
'
```

## List of available tools
```shell
npx -y mcporter list 'open.larksuite.com/mcp/stream/<token>' --all-parameters

# Get the schema of the specified tool
npx -y mcporter list 'open.larksuite.com/mcp/stream/<token>' --json | jq '.tools[] | select(.name == "<tool_name>")'
```

## Call specified tool
```shell
npx -y mcporter call 'open.larksuite.com/mcp/stream/<token>.<tool_name>' param1:"value1" foo:"bar"
```

## References
- Sent message content: references/message_create.md

## About `mcporter`
To improve compatibility, use `npx -y mcporter` instead of `mcporter` when executing commands.
