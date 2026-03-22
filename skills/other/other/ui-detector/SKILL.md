---
name: ui-detector
description: YOLO UI元素检测器项目管理。训练自定义模型识别界面元素（按钮、输入框、二维码等），用于半自动化操作。
triggers:
  - UI检测
  - 界面元素检测
  - 标注按钮
  - YOLO训练
  - 半自动化
  - ui-detector
---

# UI 元素检测器

基于 YOLO 的界面元素检测系统，支持多项目隔离管理。

## 快速开始

```bash
# 创建项目
ui-detector new <项目名>

# 启动标注
ui-detector annotate <项目名>

# 训练模型
ui-detector train <项目名>

# 检测图片
ui-detector detect <项目名> <图片路径>
```

## 项目结构

```
~/ui-detector/
├── ui-detector              # 主命令
├── projects/                # 项目目录（完全隔离）
│   ├── bilibili/
│   │   ├── classes.txt      # 中文类别定义
│   │   ├── images/raw/      # 原始截图
│   │   ├── labels/          # YOLO格式标注
│   │   └── models/best.pt   # 训练好的模型
│   └── <其他项目>/
├── .venv-labelimg/          # Python 3.11 环境
└── scripts/                 # 辅助脚本
```

## 标注工具快捷键

| 键 | 功能 |
|----|------|
| `W` | 画矩形框 |
| `D` | 下一张 |
| `A` | 上一张 |
| `Ctrl+S` | 保存 |
| `Ctrl+D` | 删除框 |

## 默认类别（中文）

```
登录按钮、注册按钮、确定按钮、取消按钮、返回按钮
提交按钮、发送按钮、搜索按钮、其他按钮、二维码
输入框、密码框、搜索框、下拉框、复选框
单选框、开关、图标、头像、链接、文本
```

可在 `classes.txt` 中自定义。

## 训练建议

| 数据量 | 效果 |
|--------|------|
| 每类 10-20 张 | 基本可用 |
| 每类 30-50 张 | 稳定可靠 |
| 每类 100+ 张 | 高精度 |

## 训练参数

```bash
# 快速训练（测试用）
ui-detector train bilibili --epochs 10

# 标准训练
ui-detector train bilibili --epochs 50

# 大模型（更准确但更慢）
ui-detector train bilibili --model s --epochs 50
```

模型大小：`n`(nano最快) < `s`(small) < `m`(medium) < `l`(large) < `x`(xlarge)

## 检测输出

检测后输出：
- `detected_<图片名>` - 标注后的图片
- JSON 格式坐标（可选）

## 工作流程

### 半自动化方案

```
1. 采集截图 → 放入 projects/<名>/images/raw/
2. 启动标注 → ui-detector annotate <名>
3. 训练模型 → ui-detector train <名>
4. 检测元素 → 输出坐标 → 自动点击
```

### 迭代优化

```
标注少量数据 → 训练初版 → 检测新截图 → 修正标注 → 再训练
```

## 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Python | 3.11 | 标注工具 |
| labelImg | 1.8.6 | 标注界面 |
| PyTorch | 2.x | 深度学习 |
| Ultralytics | 8.x | YOLOv8 |
| CUDA | 12.x | GPU加速 |

## 显存需求

| 模型 | 训练 | 推理 |
|------|------|------|
| yolov8n | ~2GB | ~1GB |
| yolov8s | ~4GB | ~2GB |
| yolov8m | ~6GB | ~3GB |

RTX 3060 (6GB) 推荐 `n` 或 `s` 模型。

## 故障排除

### labelImg 启动失败

```bash
# 检查环境
ls ~/ui-detector/.venv-labelimg/bin/python

# 手动启动
cd ~/ui-detector/projects/<项目名>
~/ui-detector/.venv-labelimg/bin/python -c "
import sys
sys.argv = ['labelImg', 'images/raw', 'classes.txt']
from labelImg import labelImg
labelImg.main()
"
```

### 训练报错

```bash
# 检查标注数量
ls ~/ui-detector/projects/<名>/labels/*.txt | wc -l

# 至少需要 10 个标注文件
```

### 显存不足

```bash
# 使用更小的批次
ui-detector train <名> --batch 8

# 或用 CPU（很慢）
export CUDA_VISIBLE_DEVICES=""
ui-detector train <名>
```

## 与自动化结合

训练好的模型可用于：

1. **Playwright 自动化**：检测按钮坐标后点击
2. **PyAutoGUI 脚本**：屏幕检测 + 鼠标操作
3. **OpenClaw 集成**：视觉理解 + 自动执行

示例代码：

```python
from ultralytics import YOLO

model = YOLO("~/ui-detector/projects/bilibili/models/best.pt")
results = model("screenshot.png")

for box in results[0].boxes:
    cls = int(box.cls)
    xywh = box.xywh[0]  # 中心点坐标
    print(f"元素类型: {cls}, 点击位置: ({int(xywh[0])}, {int(xywh[1])})")
```

## 相关技能

- `browser-use`: 浏览器自动化
- `visual-analyzer`: 视觉分析
- `agent-browser`: 无头浏览器

---

## 安装位置

```
~/ui-detector/                    # 主目录
~/.local/bin/ui-detector          # 命令入口
~/.local/share/yolo-venv/         # YOLO 环境
~/ui-detector/.venv-labelimg/     # 标注环境
```