---
name: volcengine-image-gen
description: 使用火山引擎（豆包）Seedream 系列模型生成高质量图片。支持文生图、多种分辨率、多种比例。
---

# 火山引擎图片生成

使用火山方舟 (Ark) 平台的 **Seedream** 系列模型生成高质量图片。

## 支持的模型

| 模型 ID | 名称 | 特点 |
|---------|------|------|
| `doubao-seedream-3-0-t2i-250115` | Seedream 3.0 | 轻量级，速度快 |
| `doubao-seedream-4-0-t2i-250115` | Seedream 4.0 | 标准质量 |
| `doubao-seedream-4-5-251128` | Seedream 4.5 | 最新高质量 (默认) |

## 快速开始

### 1. 配置 API Key

在 skill 目录的 `.env` 文件中配置：

```bash
VOLCENGINE_IMAGE_API_KEY=你的-api-key
VOLCENGINE_IMAGE_ENDPOINT=https://ark.cn-beijing.volces.com/api/v3
VOLCENGINE_IMAGE_DEFAULT_MODEL=doubao-seedream-4-5-251128
```

或者在环境变量中设置：

```bash
export VOLCENGINE_IMAGE_API_KEY=你的-api-key
```

### 2. 生成图片

```bash
# 基础生成
python3 scripts/generate.py "一只可爱的猫咪" -o cat.png

# 指定比例
python3 scripts/generate.py "科幻城市夜景" -r 16:9 -o city.png

# 指定尺寸 (2K)
python3 scripts/generate.py "山水画" -W 2048 -H 2048 -o landscape.png

# 使用特定模型
python3 scripts/generate.py "赛博朋克风格" -m doubao-seedream-4-0-t2i-250115 -o cyber.png

# 生成多张
python3 scripts/generate.py "不同角度的跑车" -n 4 -o car.png
```

## 使用示例

### 示例 1: 基础文生图

```bash
cd ~/clawd/skills/volcengine-image-gen
python3 scripts/generate.py "一只可爱的橘猫在窗台上晒太阳，水彩风格" -o cat.png
```

### 示例 2: 指定比例

```bash
python3 scripts/generate.py "未来城市夜景，霓虹灯，赛博朋克" -r 16:9 -o cyberpunk.png
```

支持的比例：
- `1:1` - 正方形
- `16:9` / `9:16` - 宽屏/竖屏
- `4:3` / `3:4` - 标准比例
- `2:3` / `3:2` - 照片比例

### 示例 3: Python 调用

```python
import sys
sys.path.insert(0, '/Users/xdrshjr/clawd/skills/volcengine-image-gen/scripts')
from generate import generate_image

# 生成图片
paths = generate_image(
    prompt="一只可爱的猫咪在花园里玩耍",
    ratio="1:1",
    output_path="cat.png"
)

print(f"图片已保存: {paths[0]}")
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述提示词 | 必填 |
| `-o, --output` | 输出文件路径 | 自动生成 |
| `-m, --model` | 模型名称 | Seedream 4.5 |
| `-r, --ratio` | 图片比例 | 1:1 |
| `-W, --width` | 图片宽度 | 根据比例计算 |
| `-H, --height` | 图片高度 | 根据比例计算 |
| `-n, --number` | 生成数量 (1-4) | 1 |
| `--no-watermark` | 不添加水印 | - |
| `--url` | 返回 URL 而不是下载 | - |
| `--list-models` | 列出支持的模型 | - |
| `--debug` | 开启调试模式 | - |

## 尺寸要求

- **最小像素**: 3,686,400 (约 1920x1920)
- **推荐尺寸**: 2048x2048 (2K)
- 如果指定的比例尺寸不满足最小像素，会自动放大

## 环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `VOLCENGINE_IMAGE_API_KEY` | 火山引擎 API Key | ✅ |
| `VOLCENGINE_IMAGE_ENDPOINT` | API 端点 | ❌ |
| `VOLCENGINE_IMAGE_DEFAULT_MODEL` | 默认模型 | ❌ |

## 获取 API Key

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark/)
2. 点击右上角 **API Key 管理**
3. 创建新的 API Key
4. 复制 Key 并配置到 `.env` 文件

## 安装依赖

```bash
cd ~/clawd/skills/volcengine-image-gen
pip3 install -r requirements.txt
```

## 故障排除

### API Key 无效

```
AuthenticationError: The API key format is incorrect
```

**解决**: 确认使用的是火山方舟 (Ark) 的 API Key，不是语音合成的 Access Token。

### 尺寸太小

```
InvalidParameter: image size must be at least 3686400 pixels
```

**解决**: 使用更大的尺寸，如 2048x2048 或更大的比例。

### 网络超时

```
网络请求失败
```

**解决**: 图片生成可能需要 30-60 秒，请检查网络连接。

## 提示词技巧

### 有效的提示词结构

```
[主体], [细节描述], [风格], [光线], [构图], [色彩]
```

### 示例

```
一只可爱的橘猫，趴在窗台上晒太阳，毛发柔软蓬松，
水彩画风格，柔和的自然光线，温馨的氛围，
暖色调，细节丰富，高清画质
```

### 常用风格关键词

- **写实**: photorealistic, realistic, detailed
- **动漫**: anime, manga, cartoon style
- **油画**: oil painting, classical art
- **水彩**: watercolor, soft colors
- **赛博朋克**: cyberpunk, neon lights, futuristic
- **中国风**: Chinese traditional style, ink wash painting

## 参考文档

- [火山方舟文档](https://www.volcengine.com/docs/82379/1302017)
- [Seedream 提示词指南](https://www.volcengine.com/docs/82379/1829186)
