---
name: cpa-codex-free
description: CPA认证文件自动生成及清理
---

# 技能描述
此技能用于生成 CLI Proxy API 的认证文件，请确保已为openai域名分流至非中国地区。

## 环境变量
优先从工作空间下的`.env`获取，其次从系统环境变量获取。未配置时向用户索取并更新`.env`。

- `MAIL_API_KEY`: 邮箱服务API密钥，默认`gpt-test`为官方测试密钥(每天20万额度)，获取地址: https://shop.chatgpt.org.uk/buy/prod_1768420938389
- `CLI_PROXY_API_BASE`: CPA Base URL
- `CLI_PROXY_API_MKEY`: CPA Management Key


## 工作流程
```shell
# 生成认证文件
uv scripts/main.py > {tempdir}/{temp-name}.json

# 上传至CPA服务
curl -X POST -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $CLI_PROXY_API_MKEY" \
  "$CLI_PROXY_API_BASE/v0/management/auth-files?name=codex-<email>.json" \
  -d "@{tempdir}/{temp-name}.json"

# 检查认证文件
curl "${CLI_PROXY_API_BASE}/v0/management/auth-files" \
  -H "Authorization: Bearer ${CLI_PROXY_API_MKEY}" \
| jq '.files[] | select(.provider == "codex" and .email == "<email>") | {auth_index, id_token, status}'

# 查询剩余额度
curl "$CLI_PROXY_API_BASE/v0/management/api-call" \
  -H "Authorization: Bearer $CLI_PROXY_API_MKEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "authIndex":"<auth_index>",
  "method":"GET",
  "url":"https://chatgpt.com/backend-api/wham/usage",
  "header":{
    "Authorization":"Bearer $TOKEN$",
    "Content-Type":"application/json",
    "User-Agent":"codex_cli_rs/0.76.0 (Debian 13.0.0; x86_64) WindowsTerminal",
    "Chatgpt-Account-Id":"<chatgpt_account_id>"
  }
}'

# 清理临时文件
rm {tempdir}/{temp-name}.json
```

## 清理流程
```shell
# 获取失效的认证文件列表
curl "${CLI_PROXY_API_BASE}/v0/management/auth-files" \
  -H "Authorization: Bearer ${CLI_PROXY_API_MKEY}" \
| jq '.files[] | select(.provider == "codex" and .status == "error") | {name, status_message}'

# 删除认证文件
curl -X DELETE "${CLI_PROXY_API_BASE}/v0/management/auth-files?name=<name.json>" \
  -H "Authorization: Bearer ${CLI_PROXY_API_MKEY}"
```

## 清理规则
只清理**明确失效**的认证文件。

### 不清理（网络/瞬时错误）
- `i/o timeout`
- `EOF` / `unexpected EOF`
- `context canceled`

### 可清理（明确失效）
- `usage_limit_reached`
- `invalid auth`
- `revoked`
- `malformed token`
