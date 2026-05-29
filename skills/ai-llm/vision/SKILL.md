---
name: vision
description: 这个技能接收用户给出的图片、pdf文件，按照用户的要求进行描述、综述、解释、界面截图复刻等功能。
---

# **vision**的主要功能

## 图片/pdf内容描述
## 跟据给出的图片/pdf，使用css+html+js 精准的复刻图片/pdf中的内容
## 跟据图片/pdf内容进行分析、推断、预测、总结

# 输入
用户给出的文件和需求描述文本


# 功能要求

使用下面示例调用处理程序，并获取结果
```
cd .claude/skills/vision && uv run vision_analyzer.py ../../{image.jpg} "请描述这个图片"
```
将输出的结果按照markdown格式直接输出给用户