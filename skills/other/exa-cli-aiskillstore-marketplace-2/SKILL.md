---
name: exa-cli
description: 使用 Exa 搜索与代码上下文命令行进行信息检索与编程资料检索。适用于需要从实时网页获取资料、定位权威来源、或查询具体代码示例/库用法的任务（如技术调研、API 使用方式确认、示例代码查找）。
---

## 使用方式

说明：以下调用方式均以当前 `SKILL.md` 文件所在文件夹为 workdir。必须直接当作可执行文件执行。

- 运行脚本：`scripts/exa-cli.py`
- 网页搜索：`scripts/exa-cli.py web-search-exa <query>`
- 编程检索：`scripts/exa-cli.py get-code-context-exa <query>`

### web-search-exa

说明：实时网页搜索并返回结果与正文片段。  
必填参数：`query`（搜索查询语句）。  
可选参数：  
`--type`：搜索类型（auto/fast/deep）。  
`--livecrawl`：抓取模式（fallback/preferred）。  
`--num-results`：返回结果数量。  
`--context-max-characters`：返回上下文的最大字符数。  
`--endpoint`：服务地址（默认 `https://mcp.exa.ai/mcp`）。  
`--token`：认证令牌，默认读取环境变量。  
`--timeout`：请求超时秒数（默认 30.0）。  
`--cache-ttl`：缓存有效期（秒，默认 3600）。  
`--no-cache`：禁用本地缓存。  
`--json`：以 JSON 输出完整响应。  
`--verbose`：输出调试日志。

### get-code-context-exa

说明：面向编程问题的检索，返回高质量上下文信息。  
必填参数：`query`（上下文检索查询）。  
可选参数：  
`--tokens-num`：返回的 token 数量。  
`--endpoint`：服务地址（默认 `https://mcp.exa.ai/mcp`）。  
`--token`：认证令牌，默认读取环境变量。  
`--timeout`：请求超时秒数（默认 30.0）。  
`--cache-ttl`：缓存有效期（秒，默认 3600）。  
`--no-cache`：禁用本地缓存。  
`--json`：以 JSON 输出完整响应。  
`--verbose`：输出调试日志。

## 参考信息

- [exa-cli.py](scripts/exa-cli.py)
