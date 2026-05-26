---
name: ai
description: Cheat sheet for AI tools including GEMINI and CODEX configurations.
---

# AI

## GEMINI

```ps1

[Environment]::SetEnvironmentVariable("GOOGLE_GEMINI_BASE_URL", "https://gateway.ai.cloudflare.com/v1/fa0c3c1818cd69ddde353943aa6212f6/demo/google-ai-studio")
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "")
[Environment]::SetEnvironmentVariable("GEMINI_MODEL", "gemini-2.5-flash-lite")
```

## CODEX

```toml
# windows_wsl_setup_acknowledged = true
# model = "gpt-5.1"

# [notice]
# hide_gpt5_1_migration_prompt = true


model_provider = "cf-gateway-gemini-compat"
model = "google-ai-studio/gemini-2.5-flash-lite" 
model_reasoning_effort = "high"
disable_response_storage = true
preferred_auth_method = "apikey"
windows_wsl_setup_acknowledged = true
[model_providers.cf-gateway-gemini-compat]
name = "cf-gateway-gemini-compat"
base_url = "https://gateway.ai.cloudflare.com/v1/fa0c3c1818cd69ddde353943aa6212f6/demo/compat"
wire_api = "chat"
env_key = "GEMINI_API_KEY"


[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]

[mcp_servers.chrome-devtools]
command = "cmd"
args = [
    "/c",
    "npx",
    "-y",
    "chrome-devtools-mcp@latest",
]
env = { SystemRoot="C:\\Windows", PROGRAMFILES="C:\\Program Files" }
startup_timeout_ms = 20_000


[mcp_servers.serena]
command = "uvx"
args = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex"]
```

```sh
codex mcp add playwright npx "@playwright/mcp@latest"
codex mcp add context7 -- npx -y @upstash/context7-mcp
```
