---
name: bench
description: 测试 API 模型性能 - TTFB 和吐字速度
---

快速测试第三方 API 的模型性能。两个脚本，按 API 格式选择。

## 用法

用户提供：API Key + Base URL

**默认 → OpenAI 格式**（`/v1/chat/completions`）：
```bash
cd .claude/skills/bench && uv run python test_models.py "<API_KEY>" "<BASE_URL>"
```

**用户说"Anthropic 格式"→ Anthropic 原生**（`/v1/messages`）：
```bash
cd .claude/skills/bench && uv run python test_anthropic.py "<API_KEY>" "<BASE_URL>"
```

## 判断规则

- 默认走 `test_models.py`（OpenAI 格式）
- 仅当用户明确说"Anthropic 格式/原生 API"时，走 `test_anthropic.py`
- 不要自动猜测，由用户指定

## 测试指标

- **TTFB**: 首次响应延迟（10秒超时）
- **Tok/s**: 吐字速度
- 总超时：30秒

## OpenAI 脚本特性（test_models.py）

- 自动从 `/models` 端点获取可用模型并智能筛选
- 筛选最新主流文本模型（Claude 4.x, GPT 5.x, Gemini 3.x, Qwen 3.x, GLM 4.7+, Kimi k2.5+）
- 排除 DeepSeek、多模态模型、过时版本
- Base URL 必须带 `/v1` 后缀

## Anthropic 脚本特性（test_anthropic.py）

- 使用 `x-api-key` + `anthropic-version` 认证
- 默认测试：opus-4-6, sonnet-4-6, sonnet-4-5, haiku-4-5
- Base URL 带不带 `/v1` 都行（自动处理）

## 常见问题

- **依赖**：必须用 `uv run`，不能直接 `python`
- **OpenAI Base URL**：必须带 `/v1`，否则 `/models` 返回 HTML
- **Anthropic `/models` 被拦截**：正常，Cloudflare 保护，脚本用默认模型列表
