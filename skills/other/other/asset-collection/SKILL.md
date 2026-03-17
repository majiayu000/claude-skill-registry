---
name: asset-collection
description: 从公开网站收集视频素材（图片、Logo、图标）。当需要为图文视频准备素材时使用。包含免版权图片来源、下载规范和素材组织方式。
argument-hint: [素材主题 如:NVIDIA/数据中心/AI]
---

# 素材收集技能

## 适用场景

- 图文展示型视频的素材准备
- 公司介绍视频的 Logo、人物照片收集
- 产品宣传片的背景图、场景图收集

## 免版权图片来源

### 推荐网站

| 网站 | URL | 特点 | 授权 |
|------|-----|------|------|
| **Unsplash** | unsplash.com | 高质量摄影，分类清晰 | 免费商用，无需署名 |
| **Pexels** | pexels.com | 摄影+视频，搜索强大 | 免费商用，无需署名 |
| **Pixabay** | pixabay.com | 插画+照片+矢量 | 免费商用，无需署名 |
| **Wikipedia** | wikipedia.org | 人物照片、公司 Logo | 检查具体授权 |
| **官方新闻室** | 各公司官网 | 官方产品图、高管照片 | 仅限相关报道 |

### URL 构造技巧

**Unsplash 直接下载**:
```
https://images.unsplash.com/photo-{ID}?w={宽度}&q={质量}

示例:
https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80
```

**Wikipedia 图片**:
```
https://upload.wikimedia.org/wikipedia/commons/thumb/{路径}/{尺寸}px-{文件名}

示例:
https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Nvidia_logo.svg/400px-Nvidia_logo.svg.png
```

## 素材规格要求

### 图片尺寸

| 用途 | 最低要求 | 推荐规格 | 格式 |
|------|----------|----------|------|
| 视频背景 | 1920×1080 | 2560×1440 | JPG (q=80+) |
| Logo | 400×400 | 800×800 | PNG (透明背景) |
| 人物照片 | 800×800 | 1200×1200 | JPG/PNG |
| 产品图 | 1000×1000 | 1500×1500 | PNG (透明背景优先) |
| 图标 | 256×256 | 512×512 | PNG/SVG |

### 质量检查

下载后验证：
```bash
# 检查图片尺寸
file image.jpg
# 或
identify image.jpg  # 需要 ImageMagick

# 检查文件大小 (背景图应 > 200KB)
ls -lh image.jpg
```

## 素材下载脚本

### 单个下载

```bash
# 基本下载
curl -L "URL" -o output.jpg

# 带超时和重试
curl -L --connect-timeout 30 --retry 3 "URL" -o output.jpg

# 批量下载 (使用循环)
urls=(
  "https://images.unsplash.com/photo-1?w=1920&q=80"
  "https://images.unsplash.com/photo-2?w=1920&q=80"
)
for i in "${!urls[@]}"; do
  curl -L "${urls[$i]}" -o "image_$i.jpg"
done
```

### 素材收集脚本模板

```bash
#!/bin/bash
# collect_assets.sh - 素材收集脚本

set -e

PROJECT_DIR="$(dirname "$0")/.."
IMAGES_DIR="$PROJECT_DIR/public/images"

# 创建目录结构
mkdir -p "$IMAGES_DIR"/{logos,backgrounds,photos,icons}

echo "开始收集素材..."

# Logo
echo "  下载 Logo..."
curl -sL "https://upload.wikimedia.org/xxx/logo.png" \
  -o "$IMAGES_DIR/logos/company_logo.png"

# 背景图
echo "  下载背景图..."
curl -sL "https://images.unsplash.com/photo-xxx?w=1920&q=80" \
  -o "$IMAGES_DIR/backgrounds/bg_01.jpg"

# 验证下载
echo ""
echo "素材验证:"
for f in "$IMAGES_DIR"/**/*; do
  if [ -f "$f" ]; then
    size=$(ls -lh "$f" | awk '{print $5}')
    echo "  ✓ $(basename "$f") - $size"
  fi
done

echo ""
echo "素材收集完成!"
```

## 素材搜索策略

### 按场景搜索关键词

| 场景 | 英文关键词 | 中文备选 |
|------|-----------|----------|
| 数据中心 | data center, server room, cloud computing | 服务器机房 |
| AI/人工智能 | artificial intelligence, machine learning, neural network | 人工智能 |
| 芯片/半导体 | chip, semiconductor, circuit board, processor | 芯片 电路板 |
| 科技感 | technology, futuristic, digital, cyber | 科技 数字 |
| 办公/商务 | office, business, meeting, teamwork | 办公室 商务 |
| 创业/车库 | startup, garage, entrepreneur | 创业 |

### 搜索技巧

1. **使用英文搜索** - 结果更多更好
2. **添加颜色词** - "blue technology", "green energy"
3. **添加风格词** - "minimal", "abstract", "realistic"
4. **排除干扰** - "-people" 排除人物

## 素材组织规范

### 目录结构

```
public/images/
├── logos/              # Logo 和品牌标识
│   ├── company_logo.png
│   └── product_logo.svg
├── backgrounds/        # 背景图
│   ├── scene_01_bg.jpg
│   ├── scene_02_bg.jpg
│   └── gradient_overlay.png
├── photos/             # 人物、产品照片
│   ├── founder.jpg
│   ├── product_shot.jpg
│   └── team.jpg
├── icons/              # 图标素材
│   ├── feature_01.png
│   └── feature_02.png
└── assets.json         # 素材清单 (可选)
```

### 命名规范

```
{用途}_{序号}_{描述}.{格式}

示例:
bg_01_datacenter.jpg     # 背景图 #1 - 数据中心
logo_nvidia.png          # NVIDIA Logo
photo_jensen_huang.jpg   # 黄仁勋照片
icon_gpu.png             # GPU 图标
```

### 素材清单 (assets.json)

```json
{
  "project": "NVIDIA History Video",
  "collected_at": "2024-01-25",
  "assets": [
    {
      "file": "logos/nvidia_logo.png",
      "source": "Wikipedia",
      "license": "Public Domain",
      "size": "400x400"
    },
    {
      "file": "backgrounds/datacenter.jpg",
      "source": "Unsplash",
      "license": "Unsplash License",
      "size": "1920x1080",
      "author": "Taylor Vick"
    }
  ]
}
```

## 特殊素材处理

### Logo 背景去除

如果 Logo 有白色背景：
```bash
# 使用 ImageMagick 去除白色背景
convert logo.jpg -fuzz 10% -transparent white logo.png
```

### 图片尺寸调整

```bash
# 缩放到指定宽度，保持比例
convert input.jpg -resize 1920x output.jpg

# 裁剪为指定尺寸
convert input.jpg -resize 1920x1080^ -gravity center -extent 1920x1080 output.jpg
```

### 图片优化

```bash
# JPEG 质量优化 (需要 jpegoptim)
jpegoptim --max=85 image.jpg

# PNG 优化 (需要 pngquant)
pngquant --quality=65-80 image.png
```

## 版权注意事项

### 可以使用

- Unsplash/Pexels/Pixabay 图片（商用免费）
- Wikipedia 标注为 Public Domain 或 CC0 的图片
- 公司官方新闻室提供的媒体素材（用于相关报道）

### 需要谨慎

- Wikipedia 标注为 CC BY-SA 的图片（需署名）
- 搜索引擎找到的图片（来源不明）
- 社交媒体上的图片（版权复杂）

### 禁止使用

- 明确标注版权的图片
- Getty Images、Shutterstock 等付费图库的预览图
- 他人作品（未经授权）

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| 下载超时 | 增加 `--max-time 120` 参数 |
| 图片太小 | 在 URL 中调整 `w=` 参数 |
| Logo 有背景 | 使用 ImageMagick 去背景 |
| 找不到合适图片 | 尝试不同关键词组合 |
| 图片模糊 | 选择更高分辨率版本 |
