---
name: videocut:安装
description: 环境准备。安装依赖、下载模型。触发词：安装、环境准备、初始化
---

<!--
input: 无
output: 环境就绪
pos: 前置 skill，首次使用前运行

架构守护者：一旦我被修改，请同步更新：
1. ../README.md 的 Skill 清单
2. /CLAUDE.md 路由表
-->

# 安装

> 首次使用前的环境准备（本地模式）

## 快速使用

```
用户: 安装环境
用户: 初始化
```

### 依赖清单

| 依赖 | 用途 | 安装命令 |
|------|------|----------|
| Python 3.8+ | 运行 FunASR | `brew install python` |
| funasr | 语音识别 | `pip install funasr` |
| modelscope | 模型下载 | `pip install modelscope` |
| FFmpeg | 视频处理 | `brew install ffmpeg` |
| Node.js 18+ | 运行转录模块 | `brew install node` |

### 模型清单

首次运行自动下载到 `~/.cache/modelscope/`：

| 模型 | 大小 | 用途 |
|------|------|------|
| paraformer-zh | 953MB | 语音识别（带时间戳） |
| punc_ct | 1.1GB | 标点预测 |
| fsmn-vad | 4MB | 语音活动检测 |
| **小计** | **~2GB** | |

### 安装步骤

#### 1. 安装系统依赖

```bash
# macOS
brew install python node ffmpeg

# Ubuntu
sudo apt install python3 python3-pip nodejs ffmpeg
```

#### 2. 安装 Python 依赖

```bash
pip install funasr modelscope
```

#### 3. 下载模型（约2GB）

```bash
cd /path/to/videocut-skills/安装/scripts

# 自动下载所有模型
python test_funasr_local.py --download
```

#### 4. 验证环境

```bash
cd /path/to/videocut-skills/安装/scripts

# 快速验证（检查依赖）
python test_funasr_local.py

# 综合验证（加载完整模型）
python test_funasr_local.py --verify
```

成功输出：
```
🎉 本地模式完全就绪！可以使用以下命令转录：

   python 剪口播/scripts/transcribe_local.py video.mp4
```

---

## 完整安装流程

```
1. 安装系统依赖（Python、Node.js、FFmpeg）
       ↓
2. 安装 Python 依赖（funasr、modelscope）
       ↓
3. 下载模型（约2GB）
       ↓
4. 验证环境
       ↓
5. 完成 ✅
```

---

## 常见问题

### Q1: 模型下载慢

**解决**：使用国内镜像或手动下载

### Q2: ffmpeg 命令找不到

**解决**：确认已安装并添加到 PATH

```bash
which ffmpeg  # 应该输出路径
```

### Q3: Node.js 版本太低

**解决**：需要 Node.js 18+

```bash
node --version  # 需要 v18.x 或更高
```

### Q4: pip 和 python 版本不一致

**解决**：确保 pip 和 python 指向同一个版本

```bash
# 检查版本
python --version
pip --version

# 如果不一致，在 ~/.zshrc 添加 alias
alias python=python3.11
alias pip=pip3.11
```
