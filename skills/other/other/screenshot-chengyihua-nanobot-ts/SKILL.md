---
name: screenshot
description: 桌面截图技能，支持macOS系统的全屏截图、区域截图、窗口截图、定时截图等功能。当用户需要捕获屏幕内容、创建教程截图、记录错误信息或制作演示材料时使用此技能。
metadata: {"nanobot":{"emoji":"📸","requires":{"bins":["screencapture"]}}}
---

# 桌面截图技能

本技能提供macOS系统的桌面截图功能，支持多种截图模式和高级功能。

## 快速开始

### 基础截图命令

使用macOS自带的`screencapture`命令进行截图：

```bash
# 1. 全屏截图（保存到桌面）
screencapture ~/Desktop/screenshot.png

# 2. 选择区域截图（交互式）
screencapture -i ~/Desktop/selected.png

# 3. 窗口截图
screencapture -w ~/Desktop/window.png

# 4. 截图到剪贴板
screencapture -c

# 5. 定时截图（5秒后）
screencapture -T 5 ~/Desktop/delayed.png
```

### 常用参数说明

| 参数 | 说明 |
|------|------|
| `-i` | 交互式选择区域截图 |
| `-w` | 窗口截图（点击窗口） |
| `-W` | 窗口截图（当前活动窗口） |
| `-s` | 选择区域截图（非交互式） |
| `-c` | 截图到剪贴板 |
| `-C` | 强制截图到剪贴板 |
| `-T <秒>` | 延迟截图时间 |
| `-t <格式>` | 输出格式（png, jpg, pdf等） |
| `-x` | 不播放快门声音 |
| `-o` | 在预览中打开截图 |
| `-m` | 仅主显示器 |

## 高级功能

### 1. 区域截图并自动发送

```bash
# 截图并保存到临时文件
timestamp=$(date +%Y%m%d_%H%M%S)
screencapture -i /tmp/screenshot_${timestamp}.png

# 然后可以通过nanobot发送给用户
```

### 2. 定时连续截图

```bash
# 每10秒截图一次，共5次
for i in {1..5}; do
    screencapture ~/Desktop/screenshot_${i}.png
    sleep 10
done
```

### 3. 截图特定应用程序

```bash
# 先激活应用程序
osascript -e 'tell application "Safari" to activate'
sleep 1
# 截图当前活动窗口
screencapture -W ~/Desktop/safari_window.png
```

### 4. 截图带阴影效果

```bash
# 默认截图带阴影，要去掉阴影使用：
screencapture -o ~/Desktop/no_shadow.png
```

## Python脚本支持

### 基础截图脚本

参考 `scripts/basic_screenshot.py`：

```python
import subprocess
import datetime
import os

def take_screenshot(screenshot_type="full", output_dir="~/Desktop"):
    """
    截图函数
    :param screenshot_type: full(全屏), area(区域), window(窗口)
    :param output_dir: 输出目录
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    output_path = os.path.expanduser(os.path.join(output_dir, filename))
    
    if screenshot_type == "full":
        cmd = ["screencapture", output_path]
    elif screenshot_type == "area":
        cmd = ["screencapture", "-i", output_path]
    elif screenshot_type == "window":
        cmd = ["screencapture", "-w", output_path]
    else:
        raise ValueError("不支持的截图类型")
    
    subprocess.run(cmd)
    return output_path
```

### 高级截图脚本

参考 `scripts/advanced_screenshot.py`：

```python
import subprocess
import time
import os

class ScreenshotManager:
    def __init__(self):
        self.screenshot_count = 0
    
    def timed_screenshot(self, delay_seconds=5, output_dir="~/Desktop"):
        """定时截图"""
        print(f"{delay_seconds}秒后截图...")
        time.sleep(delay_seconds)
        return self.take_screenshot("full", output_dir)
    
    def multiple_screenshots(self, count=3, interval=2, output_dir="~/Desktop"):
        """连续多次截图"""
        screenshots = []
        for i in range(count):
            print(f"截图 {i+1}/{count}")
            path = self.take_screenshot("full", output_dir)
            screenshots.append(path)
            if i < count - 1:
                time.sleep(interval)
        return screenshots
    
    def take_screenshot(self, screenshot_type="full", output_dir="~/Desktop"):
        """基础截图方法"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_count += 1
        filename = f"screenshot_{timestamp}_{self.screenshot_count}.png"
        output_path = os.path.expanduser(os.path.join(output_dir, filename))
        
        cmd = ["screencapture"]
        if screenshot_type == "area":
            cmd.append("-i")
        elif screenshot_type == "window":
            cmd.append("-w")
        cmd.append(output_path)
        
        subprocess.run(cmd)
        return output_path
```

## 使用场景

### 1. 错误报告
```bash
# 截图错误信息
screencapture ~/Desktop/error_report.png
```

### 2. 教程制作
```bash
# 制作步骤截图
for step in {1..5}; do
    echo "准备步骤 $step，按回车继续..."
    read
    screencapture ~/Desktop/step_${step}.png
done
```

### 3. 演示材料
```bash
# 截图演示内容
screencapture -W ~/Desktop/demo_slide.png
```

### 4. 网页存档
```bash
# 截图整个网页
osascript -e 'tell application "Safari" to activate'
sleep 2
screencapture ~/Desktop/webpage.png
```

## 故障排除

### 常见问题

1. **权限问题**
   ```bash
   # 检查屏幕录制权限
   tccutil reset ScreenCapture
   # 然后需要在系统设置中重新授权
   ```

2. **截图失败**
   ```bash
   # 尝试使用不同的参数
   screencapture -x ~/Desktop/test.png  # 静音模式
   ```

3. **格式问题**
   ```bash
   # 指定输出格式
   screencapture -t jpg ~/Desktop/screenshot.jpg
   screencapture -t pdf ~/Desktop/screenshot.pdf
   ```

### 调试命令

```bash
# 查看screencapture帮助
screencapture -h

# 测试基本功能
screencapture ~/Desktop/test.png && echo "截图成功" || echo "截图失败"

# 检查文件权限
ls -la ~/Desktop/test.png
```

## 最佳实践

### 1. 文件命名
- 使用时间戳：`screenshot_20250210_143022.png`
- 包含描述：`error_login_20250210.png`
- 序列号：`tutorial_step_01.png`

### 2. 文件管理
```bash
# 创建截图目录
mkdir -p ~/Screenshots/$(date +%Y-%m)

# 自动整理截图
mv ~/Desktop/screenshot_*.png ~/Screenshots/$(date +%Y-%m)/
```

### 3. 质量优化
```bash
# 使用PNG格式（无损）
screencapture -t png ~/Desktop/high_quality.png

# 调整JPEG质量（如果需要）
screencapture -t jpg ~/Desktop/compressed.jpg
```

## 与nanobot集成

### 通过nanobot调用
```bash
# 使用nanobot执行截图
nanobot screenshot --type full --output ~/Desktop/screenshot.png

# 截图并直接发送
nanobot screenshot --type area --send-to-user
```

### 在对话中使用
当用户需要截图时：
1. 询问截图类型（全屏、区域、窗口）
2. 询问保存位置
3. 执行相应命令
4. 发送截图给用户或提供文件路径

## 参考资源

- [macOS screencapture手册页](https://ss64.com/osx/screencapture.html)
- [Apple官方截图指南](https://support.apple.com/zh-cn/guide/mac-help/mh26782/mac)
- [Python subprocess文档](https://docs.python.org/3/library/subprocess.html)

---

**注意**：截图功能需要屏幕录制权限。如果遇到权限问题，请前往"系统设置 > 隐私与安全性 > 屏幕录制"中授权终端或相关应用。