---
name: pptx-generator
description: Generate PowerPoint presentations with slides, charts, and formatting. Use when creating presentations programmatically.
---

# PowerPoint Generator Skill

PowerPointプレゼンテーション（.pptx）を生成するスキルです。

## 主な機能

- **スライド作成**: タイトル、コンテンツ
- **グラフ**: 棒、折れ線、円グラフ
- **画像**: 画像挿入
- **テーブル**: 表作成
- **テンプレート**: デザインテンプレート

## Python (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# タイトルスライド
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title = title_slide.shapes.title
subtitle = title_slide.placeholders[1]
title.text = "プレゼンテーションタイトル"
subtitle.text = "サブタイトル"

# コンテンツスライド
content_slide = prs.slides.add_slide(prs.slide_layouts[1])
title = content_slide.shapes.title
title.text = "主なポイント"

content = content_slide.placeholders[1]
tf = content.text_frame
tf.text = "ポイント1"

p = tf.add_paragraph()
p.text = "ポイント2"
p.level = 1

# 画像スライド
img_slide = prs.slides.add_slide(prs.slide_layouts[6])
left = Inches(1)
top = Inches(1)
img_slide.shapes.add_picture('chart.png', left, top, width=Inches(8))

prs.save('presentation.pptx')
```

## バージョン情報
- Version: 1.0.0
