# Video Generation Skill

使用 xingjiabiapi 的视频生成 API 创建 AI 视频。

## 支持的模型

| 模型 | 别名 | 说明 | 价格 |
|------|------|------|------|
| veo3.1 | `veo` | Google Veo 标准版 | 0.12元/8s |
| veo3.1-pro | `veopro` | Google Veo 专业版 | 高质量 |
| veo3.1-pro-4k | `veo4k` | Google Veo 4K | 4K分辨率 |
| sora-2-pro-all | `sora` | OpenAI Sora 专业版 | 电影级 |
| sora-2-all | - | OpenAI Sora 标准版 | 标准 |
| kling-video | `kling` | 快手可灵 | 动作流畅 |
| MiniMax-Hailuo-2.3 | - | 海螺视频 | 性价比 |

## 使用方法

### 命令行

```bash
# 列出可用模型
python3 ~/clawd/skills/video-generation/video_api.py models

# 生成视频
python3 ~/clawd/skills/video-generation/video_api.py generate "A cat walking on the beach" -m veo3.1 -d 8

# 使用 Sora
python3 ~/clawd/skills/video-generation/video_api.py generate "Cinematic shot of a sunset" -m sora-2-pro-all -d 10

# 查询任务状态
python3 ~/clawd/skills/video-generation/video_api.py poll <task_id>
```

### Python API

```python
from skills.video_generation.video_api import generate_video, list_models

# 生成视频
result = generate_video(
    prompt="A beautiful sunset over the ocean",
    model="veo3.1",
    duration=8,
    aspect_ratio="16:9",
    output_dir="/tmp/videos"
)

print(result)
# {
#   "status": "completed",
#   "video_url": "https://...",
#   "local_path": "/tmp/videos/video_xxx.mp4"
# }
```

## API 端点

- **提交任务**: `POST /v1/video/generations`
- **查询状态**: `GET /v1/video/generations/{task_id}`

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| prompt | string | 必填 | 视频描述 |
| model | string | veo3.1 | 模型名称 |
| duration | int | 8 | 视频时长（秒） |
| aspect_ratio | string | 16:9 | 宽高比 |

## 注意事项

1. 视频生成是异步任务，需要轮询获取结果
2. 生成时间通常需要 1-5 分钟
3. 高峰期可能出现"负载饱和"错误，稍后重试即可
4. 生成的视频 URL 有时效性，建议及时下载

## 与 multimodal-agent 集成

multimodal-agent 可以调用此脚本生成视频：

```python
import subprocess
import json

result = subprocess.run([
    "python3", 
    "/home/aa/clawd/skills/video-generation/video_api.py",
    "generate",
    "Your prompt here",
    "-m", "veo3.1"
], capture_output=True, text=True)

output = json.loads(result.stdout)
```
