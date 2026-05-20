---
name: peekaboo
description: "macOS截图与视觉分析。自动截图、UI分析、窗口捕获。关键词: 截图, screenshot, 界面, UI, 看看, 显示, 样式, 报错弹窗, 视觉分析"
---

# Peekaboo 视觉分析 Skill

通过peekaboo进行macOS截图和视觉分析，帮助调试UI问题。

## 截图保存目录

默认目录变量：
```bash
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
```

所有截图保存到: `${PEEKABOO_IMG_DIR}/`

## 自动触发条件

当遇到以下情况时，主动使用peekaboo截图分析：
- 用户描述UI/界面问题但未提供截图时
- 调试前端/客户端代码遇到视觉相关bug时
- 用户提到"看看"、"界面"、"显示"、"样式"、"报错弹窗"等词汇时
- 命令执行后需要确认GUI状态时
- 用户描述的问题可能通过视觉信息更容易理解时

## 截图策略

- 默认使用 `--mode frontmost` 截取当前活动窗口
- 用户提到具体应用时，使用 `--app "应用名"` 指定
- 需要分析内容时，使用 `--analyze "分析目标"` 直接获取AI分析
- 需要定位UI元素时，使用 `--annotate` 生成带标注的截图
- **必须使用 `--path` 参数指定保存路径到 peekabooImg 目录**

## 常用命令

### 截取当前窗口
```bash
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
peekaboo see --mode frontmost --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --json
```

### 截取指定应用
```bash
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
peekaboo see --app "IntelliJ IDEA" --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --json
peekaboo see --app "Safari" --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --json
peekaboo see --app "Terminal" --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --json
```

### 截图并AI分析
```bash
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
peekaboo see --mode frontmost --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --analyze "描述界面内容"
```

### 列出所有窗口
```bash
peekaboo list windows --json
```

### 截取指定标题窗口
```bash
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
peekaboo see --window-title "窗口标题" --path "${PEEKABOO_IMG_DIR}/screenshot_$(date +%s).png" --json
```

## 清理规则

**重要：截图任务完成后，必须执行清理操作：**

```bash
# 清理截图文件
PEEKABOO_IMG_DIR="${HOME}/Documents/peekabooImg"
rm -f "${PEEKABOO_IMG_DIR}"/*.png

# 清理peekaboo快照缓存
peekaboo clean --all-snapshots 2>/dev/null || true
```

清理时机：
- 截图分析完成并向用户反馈结果后
- 用户明确表示不再需要截图时
- 任务结束时

## 使用原则

- 截图前简要说明原因
- 优先截取相关窗口而非全屏
- 分析结果要结合代码上下文给出建议
- **任务完成后务必清理截图文件和缓存**

## 前置条件

1. peekaboo已安装: `brew install steipete/tap/peekaboo`
2. 已授予屏幕录制权限: 系统设置 > 隐私与安全性 > 屏幕与系统音频录制
