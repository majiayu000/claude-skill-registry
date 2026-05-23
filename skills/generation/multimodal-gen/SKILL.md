# 多模态生成 Skill

多模态内容生成（图片、视频）。当用户需要生成图片、生成图像、生成视频、AI绘画、AI作图、画一张图、做个视频时使用此技能。自动优化提示词后调用生成模型。

## 触发条件

当用户需要：
- 生成图片/图像/AI绘画
- 生成视频
- 图像理解/分析

## 工作流程

```
用户输入 → DeepSeek V3.2 优化提示词 → 生成模型 → 输出文件
```

## 统一入口

```bash
python3 ~/clawd/skills/multimodal-gen/generate.py "描述" [image|video] [model]
```

### 示例
```bash
# 生成图片（默认 gemini）
python3 ~/clawd/skills/multimodal-gen/generate.py "可爱的猫咪在阳光下睡觉"

# 生成图片（指定模型）
python3 ~/clawd/skills/multimodal-gen/generate.py "赛博朋克城市" image flux

# 生成视频（默认 veo3.1）
python3 ~/clawd/skills/multimodal-gen/generate.py "海浪拍打礁石" video

# 跳过优化
python3 ~/clawd/skills/multimodal-gen/generate.py "prompt" image --no-optimize
```

## 图像生成

### 默认模型
- `gemini` → gemini-3-pro-image-preview ⭐默认

### 其他模型
- `flux` → flux-pro-max
- `flux-ultra` → flux-pro-1.1-ultra
- `imagen` → google/imagen-4-ultra
- `dalle` → gpt-image-1
- `kling` → kling-image
- `seedream` → doubao-seedream-4-5-251128

### 输出
- 图片保存到 `~/clawd/output/images/`

## 视频生成

### 默认模型
- `veo3.1` → veo3.1 ⭐默认（普通版，性价比高）

### 其他模型
- `veo3.1-4k` → veo3.1-4k
- `veo3.1-pro` → veo3.1-pro
- `veo3` → veo3
- `sora2` → sora-2-all
- `kling` → kling-video
- `hailuo` → MiniMax-Hailuo-2.3
- `runway` → runwayml-gen4_turbo-10
- `grok` → grok-video-3

### ⚠️ 异步生成流程（重要！）
视频生成耗时较长（1-5分钟），**必须使用 spawn 子任务**，不要阻塞 main agent！

**正确做法：**
```python
# 在 main agent 中使用 sessions_spawn
sessions_spawn(
    task="生成视频：xxx描述，使用 veo3.1 模型。完成后发送给用户。",
    label="video-gen-xxx"
)
```

**子任务流程：**
1. 优化 prompt
2. 提交视频任务，获取 task_id
3. 轮询查询状态（每 10 秒）
4. 完成后下载视频并发送给用户

### 命令行用法
```bash
# 提交任务（立即返回）
python3 ~/clawd/skills/multimodal-gen/generate_video.py submit "prompt" [model]

# 查询任务状态
python3 ~/clawd/skills/multimodal-gen/generate_video.py query <task_id>

# 一键生成（阻塞等待，仅用于子任务）
python3 ~/clawd/skills/multimodal-gen/generate_video.py "prompt" [model]
```

### 输出
- 视频保存到 `~/clawd/output/videos/`

## Prompt 优化器

使用 DeepSeek V3.2 自动优化提示词：
- 翻译成英文
- 添加艺术风格、画质、光影、构图描述
- 自动规避敏感词（如 loli → young girl）

单独调用：
```bash
python3 ~/clawd/skills/multimodal-gen/prompt_optimizer.py "描述" [image|video]
```

## API 配置

- **Base URL**: https://xingjiabiapi.com/v1
- **API Key**: `pass api/xingjiabiapi`
- **优化模型**: deepseek-v3.2

## 注意事项

1. 图像生成约 10-30 秒
2. 视频生成约 1-5 分钟
3. 生成完成后将文件发送给用户
4. Gemini 对某些内容敏感，优化器会自动处理
