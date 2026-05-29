---
name: screen-capture
description: 使用系统原生方法进行屏幕捕获和内容分析，支持 macOS screencapture 命令和 Python 截图库
version: 1.0.0
---

# 屏幕捕获与分析专家

## 触发条件
当用户提到以下内容时自动触发：
- "截图"
- "屏幕内容"
- "获取屏幕"
- "分析屏幕"
- "屏幕文本"
- "OCR识别"

## 核心能力

### 屏幕捕获 (macOS)
- **screencapture 命令**: 使用 macOS 原生 `screencapture` 工具
- **全屏截图**: `screencapture -S screen.png`
- **区域截图**: `screencapture -i screen.png` (交互式选择)
- **窗口截图**: `screencapture -w window.png`

### 屏幕捕获 (Python)
- **pyautogui**: 跨平台截图库
- **mss**: 高性能截图库
- **pyscreenshot**: 简单易用的截图工具

### 文本提取
- **OCR 识别**: 使用 pytesseract 进行文字识别
- **系统辅助**: 读取系统可访问性 API

### 图像分析
- **OpenCV**: 图像处理和分析
- **PIL**: 图像分析和处理

## 常用场景

### 场景1：截取全屏

```markdown
请截取整个屏幕并保存到文件。
```

**执行步骤：**
1. 使用 `screencapture -S screen.png` 捕获全屏
2. 返回截图文件路径

### 场景2：截取区域

```markdown
请让我选择区域进行截图。
```

**执行步骤：**
1. 使用 `screencapture -i -s screen.png` 交互式选择区域
2. 返回截图文件路径

### 场景3：识别屏幕文字

```markdown
请识别屏幕上的文字内容。
```

**执行步骤：**
1. 截取屏幕
2. 使用 pytesseract 进行 OCR 识别
3. 返回识别出的文字

### 场景4：保存屏幕截图

```markdown
把当前屏幕保存为 screenshot.png。
```

**执行步骤：**
```bash
screencapture -S /Users/liubinbin/screenshot.png
```

## MCP 工具映射

| 功能 | 工具 |
|------|------|
| 屏幕截图 | `screencapture` 命令 |
| OCR 识别 | `pytesseract` |
| 图像处理 | `PIL` / `OpenCV` |
| Python 执行 | `python3` 脚本 |

## 注意事项

1. **macOS 权限**: 首次使用需要在系统偏好设置中授权屏幕录制权限
2. **Tesseract OCR**: 需要安装 `brew install tesseract`
3. **Python 依赖**: `pip3 install pyautogui pytesseract pillow opencv-python`

## 安装依赖

```bash
# macOS 屏幕录制权限工具
brew install tesseract

# Python 依赖
pip3 install pyautogui pytesseract pillow opencv-python
```
