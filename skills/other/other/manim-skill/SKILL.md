---
name: manim_skill
description: Create mathematical animations using Manim (Community Edition or ManimGL). Includes best practices, examples, and rules for creating high-quality videos.
---

# Manim Skill

This skill provides comprehensive capabilities for generating mathematical animations. It consolidates best practices for both **Manim Community Edition** and **ManimGL**.

## 📚 Libraries
- **Manim Community (`manim`)**: Use for production, education, and stability. `from manim import *`
- **ManimGL (`manimgl`)**: Use for 3D, interactive scenes, and performance. `from manimlib import *`

## 🚀 How to Use
This skill repository contains detailed rule files. When writing Manim code, refer to the following paths for patterns:

### Manim Community Edition
- **Animations**: `manimce-best-practices/rules/animations.md`
- **Scenes**: `manimce-best-practices/rules/scenes.md`
- **Text/LaTeX**: `manimce-best-practices/rules/text.md`

### ManimGL
- **3D Scenes**: `manimgl-best-practices/rules/3d.md`
- **Camera**: `manimgl-best-practices/rules/camera.md`
- **Interactive**: `manimgl-best-practices/rules/interactive.md`

## 🛠️ Usage Protocol
1. **Choose the Library**: Decide between CE (2D/Standard) or GL (3D/Performance).
2. **Review Rules**: Read the relevant best practice file before generating code.
3. **Execute**: Use the `manim` or `manimgl` CLI to render.

## 📦 Dependencies
Ensure FFmpeg and LaTeX are installed.
- **Python**: `uv add manim` or `uv add manimgl`
- **System**: `ffmpeg`, `latex` (TeX Live/MiKTeX)
