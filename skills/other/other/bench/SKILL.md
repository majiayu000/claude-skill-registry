---
name: bench
description: 测试 API 模型性能 - TTFB 和吐字速度
---

快速测试第三方中转 API 的模型性能。

## 用法

用户提供：
- API Key
- Base URL

## 测试指标

- **TTFB**: 首次响应延迟（10秒超时）
- **Tok/s**: 吐字速度
- 总超时：30秒

## 实现

**必须使用 `uv run`** 运行脚本以自动处理依赖（aiohttp）：

```bash
cd .claude/skills/bench && uv run python test_models.py "<API_KEY>" "<BASE_URL>"
```

## 智能模型过滤

自动从 `/models` 端点获取可用模型，并智能筛选：

**包含的模型版本：**
- Claude: 4.6, 4.5（排除 3.x）
- GPT: 5.x（排除 4.x, 4o, 4.1, o1, o3）
- Gemini: 3.x（排除 2.x）
- Qwen: 3.x（排除 2.x）
- GLM: 4.7+（排除 4.6 及以下）
- Kimi: k2.5+（排除 k2 及以下）

**排除的模型：**
- DeepSeek 全系列
- 多模态模型（embed, vision, image, audio, realtime, tts, vl, lite）
- 过时版本

## 常见问题

### 1. Base URL 格式
- ✅ 正确：`http://example.com:3000/v1`
- ❌ 错误：`http://example.com:3000`（缺少 `/v1` 后缀会导致 `/models` 返回 HTML）

### 2. 依赖问题
- ❌ 错误：`python test_models.py` → `ModuleNotFoundError: No module named 'aiohttp'`
- ✅ 正确：`uv run python test_models.py` → 自动处理依赖

### 3. 模型数量
- API 可能有 300+ 模型，脚本会自动筛选出最新主流文本模型（通常 10-20 个）
- 如果 `/models` 端点失败，会回退到默认模型列表

## 输出示例

```
Fetching available models...
Testing 9 models with streaming...
Task: 请写一篇300字的短文，主题是春天的早晨。

==========================================================================================
Model                                    TTFB         Tok/s        Status
==========================================================================================
gpt-5-chat-latest                        1.81s         81.0       ✓
gpt-5-2025-08-07                         8.52s        411.1       ✓
gemini-3-flash-preview                   8.69s          7.1       ✓
gpt-5                                    --           --           ✗ TTFB timeout (>10s)
...
==========================================================================================
🏆 最快首次响应: gpt-5-chat-latest (1.81s)
⚡ 最快吐字速度: gpt-5-2025-08-07 (411.1 tok/s)
✓ 3/9 模型可用
```
