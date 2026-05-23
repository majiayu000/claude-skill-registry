---
name: image_generation
display_name: AI 图像生成
description: AI图像生成与编辑能力，基于 Nano Banana (Gemini Image) 实现文生图、图生图、图像编辑。适用于创意设计、营销素材、社交媒体内容、演示文稿配图等场景。支持多种风格、高分辨率输出（最高4K）、文字渲染、角色一致性保持。
version: 1.0.0
author: system
tags: [image, generation, editing, design, creative, 生图, 图像, 设计, nano-banana, gemini]
allowed_tools: [generate_image, edit_image, create_document]
max_iterations: 15
timeout: 300
match_threshold: 0.75
priority: 8
enabled: true
---

## 能力概述

AI图像生成能力让你能够：
- **文生图**：根据文字描述生成图像
- **图生图**：基于参考图像生成新图像
- **图像编辑**：修改现有图像的特定部分
- **风格转换**：改变图像风格（写实、动漫、油画等）
- **文字渲染**：在图像中生成清晰可读的文字

底层基于 Google Gemini 的 Nano Banana / Nano Banana Pro 模型。

## 工作流程

### Phase 1: 需求理解
1. 理解用户的图像需求（主题、风格、用途）
2. 确认输出格式（尺寸、分辨率、数量）
3. 如有参考图，确认编辑意图

### Phase 2: Prompt 构建
1. 将用户意图转化为英文 Prompt（效果更好）
2. 遵循 Prompt 公式：`<subject> <action> <scene> <style> <quality>`
3. 补充必要的细节描述

### Phase 3: 图像生成
1. 调用 `generate_image` 工具
2. 如需编辑，调用 `edit_image` 工具
3. 生成多个候选（如用户需要选择）

### Phase 4: 交付
1. 展示生成结果
2. 询问是否需要调整
3. 保存到用户指定位置

## 工具使用

### generate_image
- **用途**：根据文字描述生成图像
- **参数**：
  - `prompt`: 图像描述（英文效果更佳）
  - `style`: 风格预设（realistic, anime, oil_painting, watercolor, minimal, cinematic）
  - `aspect_ratio`: 宽高比（1:1, 16:9, 9:16, 4:3, 3:4）
  - `resolution`: 分辨率（1K, 2K, 4K）
  - `num_images`: 生成数量（1-4）
- **示例**：
  ```python
  generate_image(
      prompt="A majestic horse galloping through cherry blossoms, golden hour lighting, Chinese New Year festive atmosphere",
      style="realistic",
      aspect_ratio="16:9",
      resolution="2K",
      num_images=2
  )
  ```

### edit_image
- **用途**：编辑现有图像
- **参数**：
  - `image_path`: 原图路径或URL
  - `prompt`: 编辑指令（如："将背景改为夜景"）
  - `preserve_subject`: 是否保持主体不变（默认True）
- **示例**：
  ```python
  edit_image(
      image_path="/workspace/photo.jpg",
      prompt="Add Chinese New Year decorations and red lanterns to the background",
      preserve_subject=True
  )
  ```

## Prompt 最佳实践

### 基础公式
```
[主体] + [动作/姿态] + [场景/背景] + [风格] + [氛围/光线]
```

### 风格关键词
- **写实**：photorealistic, hyperrealistic, 8K, detailed
- **动漫**：anime style, Ghibli style, cel shading
- **油画**：oil painting style, impressionist, Van Gogh style
- **极简**：minimal, flat design, vector art
- **电影感**：cinematic, dramatic lighting, movie poster style

### 质量增强词
- `high quality`, `detailed`, `sharp focus`
- `professional photography`, `award winning`
- `4K resolution`, `ultra detailed`

### 避免事项
- ❌ 避免模糊描述："一张好看的图"
- ❌ 避免矛盾描述："写实风格的卡通"
- ❌ 避免敏感内容
- ✅ 具体、清晰、有层次

## 应用场景模板

### 场景1：微信红包封面/节日祝福图
```yaml
prompt_template: |
  A {animal} in {pose}, surrounded by {decorations}, 
  Chinese New Year theme, festive red and gold colors, 
  {style} style, high quality, {text_content}
  
variables:
  animal: "majestic horse" # 马年
  pose: "running gracefully"
  decorations: "cherry blossoms, red lanterns, gold coins"
  style: "elegant illustration"
  text_content: "with Chinese text '恭喜发财' in golden calligraphy"
```

### 场景2：演示文稿配图
```yaml
prompt_template: |
  {concept} visualization, professional infographic style,
  clean white background, modern corporate aesthetic,
  subtle gradients, minimalist design

variables:
  concept: "AI workflow automation"
```

### 场景3：社交媒体内容
```yaml
prompt_template: |
  {subject} {action}, {platform} optimized aspect ratio,
  vibrant colors, eye-catching composition, 
  trending aesthetic, shareable content style
  
variables:
  subject: "coffee cup"
  action: "with steam rising"
  platform: "Instagram" # 1:1 or 4:5
```

## 输出格式

### 生成结果展示
```markdown
## 🎨 图像生成完成

**Prompt**: [使用的英文Prompt]

**参数**:
- 风格: [style]
- 尺寸: [aspect_ratio]
- 分辨率: [resolution]

**生成结果**:
![Generated Image](path/to/image.png)

**下一步**:
- [ ] 满意，保存到指定位置
- [ ] 需要调整风格/颜色
- [ ] 需要修改特定部分
- [ ] 重新生成
```

## 注意事项

1. **版权合规**：生成的图像带有 SynthID 水印
2. **内容政策**：遵守 Google 使用政策，不生成敏感内容
3. **商业使用**：支持商业用途（营销、产品）
4. **文字渲染**：Nano Banana Pro 支持多语言文字，但中文效果需要验证
5. **角色一致性**：跨图保持角色特征需要使用参考图功能

## 资源引用

- `resources/prompt_templates.yaml` - 预设 Prompt 模板
- `resources/style_presets.md` - 风格预设详解
- `resources/chinese_new_year_2026.md` - 马年专属模板
