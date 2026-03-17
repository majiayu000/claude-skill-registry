---
name: image-gen
description: "图片生成, 架构图, 流程图, 时序图, 泳道图, diagram, architecture, flowchart, sequence, swimlane, image generation, nano banana, 生图, 画图, 画一个, 生成图片, generate image, draw diagram"
---

# Image Gen Skill

通用图片生成技能，支持自由生图和结构化图表生成（架构图、流程图、时序图、泳道图）。通过可配置的 API Provider 调用图片生成模型。

## Prerequisites

1. Python3 可用。
2. 已配置 API Provider（编辑 `~/.codex/skills/image-gen/providers.json` 填入 api_key）。

## Script Path

```
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SCRIPT="${CODEX_HOME}/skills/image-gen/scripts/image-gen.py"
```

## Config（配置管理）

### 查看当前配置
**Triggers:** "image-gen 配置", "查看生图配置", "image config"
```bash
python3 "$SCRIPT" config
```

### 切换 Provider
**Triggers:** "切换生图 provider", "switch image provider"
```bash
python3 "$SCRIPT" config --switch <provider_key>
```
可选 provider_key: `huan`, `undying`, `google`

## Generate（自由生图）

**Triggers:** "生成图片", "画一个", "generate image", "生图", "画图"

直接传入 prompt 生成图片：
```bash
python3 "$SCRIPT" generate "一个微服务架构图，包含网关、用户服务、订单服务和数据库"
```

可选参数：
- `--output <path>`：指定输出路径（默认 `/tmp/image-gen-<timestamp>.png`）
- `--ratio <16:9>`：宽高比（默认 `16:9`）
- `--style <clean>`：风格 `clean` / `detailed` / `minimal`（默认 `clean`）
- `--debug-raw`：将原始请求/响应 JSON 落盘，便于排查接口返回问题
- `--debug-dir <path>`：调试文件目录（默认 `/tmp/image-gen-debug`）

## Diagram（图表模式）

根据图表类型自动包装专业 prompt 模板，生成高质量技术图表。

### 架构图 Architecture
**Triggers:** "画架构图", "architecture diagram", "系统架构"
```bash
python3 "$SCRIPT" diagram --type architecture --input "Client -> API Gateway -> Auth Service, User Service -> PostgreSQL"
```

### 流程图 Flowchart
**Triggers:** "画流程图", "flowchart", "流程"
```bash
python3 "$SCRIPT" diagram --type flowchart --input "用户注册流程：输入信息->验证邮箱->创建账号->发送欢迎邮件"
```

### 时序图 Sequence
**Triggers:** "画时序图", "sequence diagram", "时序"
```bash
python3 "$SCRIPT" diagram --type sequence --input "Browser->Server: HTTP Request; Server->DB: Query; DB->Server: Result; Server->Browser: Response"
```

### 泳道图 Swimlane
**Triggers:** "画泳道图", "swimlane diagram", "泳道"
```bash
python3 "$SCRIPT" diagram --type swimlane --input "前端: 发送请求; 网关: 鉴权转发; 服务: 业务处理; 数据库: 读写数据"
```

### 从文件读取描述
```bash
python3 "$SCRIPT" diagram --type architecture --file description.txt
```

### Diagram 通用可选参数
- `--output <path>`：指定输出路径（默认 `/tmp/image-gen-<timestamp>.png`）
- `--ratio <16:9>`：宽高比（默认 `16:9`）
- `--style <clean>`：风格 `clean` / `detailed` / `minimal`（默认 `clean`）
- `--debug-raw`：将原始请求/响应 JSON 落盘，便于排查接口返回问题
- `--debug-dir <path>`：调试文件目录（默认 `/tmp/image-gen-debug`）

## 输出约定

脚本成功后会输出图片文件路径，使用 Read 工具查看图片内容展示给用户。

## 失败策略（严格）

- 若 `generate` / `diagram` 命令返回非 0、超时、或提示“未在响应中找到图片/只返回文本”，必须直接向用户报告失败原因。
- 禁止使用 PIL/Pillow/Canvas/matplotlib 等本地绘制作为“兜底图”。
- 仅当脚本标准输出返回真实图片路径且文件存在时，才可声明“已生成成功”。

## Important Notes

- 首次使用前需编辑 `~/.codex/skills/image-gen/providers.json` 填入 api_key。
- 默认使用 Huan API + nano-banana-pro 模型。
- 生成的图片默认保存到 `/tmp/` 目录。
- 支持 OpenAI 兼容格式和 Google Gemini 原生格式两种 API 协议。
- 可通过环境变量 `IMAGE_GEN_TIMEOUT` 调整请求超时（默认 300 秒）。
- 可通过 `IMAGE_GEN_DEBUG_RAW=1` 开启调试落盘；目录可用 `IMAGE_GEN_DEBUG_DIR` 指定。
