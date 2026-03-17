---
name: macos-cleaner
description: 分析并通过智能清理建议回收 macOS 磁盘空间。当用户报告磁盘空间问题、需要清理 Mac 或想了解什么占用了存储空间时，应使用此技能。专注于安全的交互式分析，在执行任何删除操作前需要用户确认。
---

# macOS 清理工具

## 概述

智能分析 macOS 磁盘使用情况并提供可执行的清理建议以回收存储空间。此技能遵循**安全第一的原则**：彻底分析，呈现清晰的发现，并在执行任何删除操作前要求明确的用户确认。

**目标用户**：具有基本技术知识的用户，了解文件系统但需要指导哪些内容在 macOS 上可以安全删除。

## 核心原则

1. **安全第一，绝不绕过**：在没有明确用户确认的情况下，绝不执行危险命令（`rm -rf`、`mo clean` 等）。没有捷径，没有变通方法。
2. **价值优于虚荣**：您的目标不是最大化清理空间。您的目标是识别什么是**真正无用**的 vs **有价值的缓存**。为了显示大数字而清除 50GB 有用缓存是有害的。
3. **网络环境意识**：许多用户（尤其是中国）的网络缓慢/不可靠。重新下载缓存可能需要数小时。一个节省 30 分钟下载时间的缓存是值得保留的。
4. **必须进行影响分析**：每个清理建议必须包含"删除后会发生什么"列。绝不要在不解释后果的情况下仅列出项目。
5. **耐心优于速度**：磁盘扫描可能需要 5-10 分钟。绝不中断或跳过慢速操作。定期向用户报告进度。
6. **用户执行清理**：分析完成后，提供清理命令让用户自己运行。不要自动执行清理。
7. **保守默认**：如有疑问，不要删除。倾向于谨慎。

**绝对禁止：**
- ❌ 绝不自动在用户目录上运行 `rm -rf`
- ❌ 绝不在没有预览试运行的情况下运行 `mo clean`
- ❌ 绝不使用 `docker volume prune -f` 或 `docker system prune -a --volumes`
- ❌ 绝不为节省时间跳过分析步骤
- ❌ 绝不在 Mole 命令后附加 `--help`（除了 `mo --help`）
- ❌ 绝不建议删除有用的缓存只是为了夸大清理数字

## 工作流决策树

```
用户报告磁盘空间问题
           ↓
    快速诊断
           ↓
    ┌──────┴──────┐
    │             │
立即清理     深度分析
    │             (继续下方)
    │             │
    └──────┬──────┘
           ↓
  呈现发现
           ↓
   用户确认
           ↓
   执行清理
           ↓
  验证结果
```

## 第一步：使用 Mole 进行快速诊断

**主要工具**：使用 Mole 进行磁盘分析。它提供全面的、分类的结果。

### 1.1 预检检查

```bash
# 检查 Mole 安装和版本
which mo && mo --version

# 如果未安装
brew install tw93/tap/mole

# 检查更新（Mole 经常更新）
brew info tw93/tap/mole | head -5

# 如果过时则升级
brew upgrade tw93/tap/mole
```

### 1.2 选择分析方法

**重要**：使用 `mo analyze` 作为主要分析工具，而不是 `mo clean --dry-run`。

| 命令 | 目的 | 使用时机 |
|---------|---------|----------|
| `mo analyze` | 交互式磁盘使用浏览器（TUI 树视图） | **主要**：了解什么占用了空间 |
| `mo clean --dry-run` | 预览清理类别 | **次要**：仅在 `mo analyze` 之后查看清理预览 |

**为什么优先使用 `mo analyze`：**
- 专用的磁盘分析工具，具有交互式树导航
- 允许深入到特定目录
- 显示实际的磁盘使用细分，而不仅仅是清理类别
- 对于理解存储消耗更有信息量

### 1.3 通过 tmux 运行分析

**重要**：Mole 需要 TTY。从 Claude Code 使用时始终使用 tmux。

**关键时间说明**：主目录扫描很慢（对于大目录需要 5-10 分钟或更长时间）。提前告知用户并耐心等待。

```bash
# 创建 tmux 会话
tmux new-session -d -s mole -x 120 -y 40

# 运行磁盘分析（主要工具 - 交互式 TUI）
tmux send-keys -t mole 'mo analyze' Enter

# 等待扫描 - 耐心等待！
# 主目录扫描通常需要 5-10 分钟
# 定期向用户报告进度
sleep 60 && tmux capture-pane -t mole -p

# 使用箭头键导航 TUI
tmux send-keys -t mole Down    # 移动到下一项
tmux send-keys -t mole Enter   # 展开/选择项目
tmux send-keys -t mole 'q'     # 完成后退出
```

**替代方案：清理预览（在 mo analyze 之后使用）**
```bash
# 运行试运行预览（安全 - 无删除）
tmux send-keys -t mole 'mo clean --dry-run' Enter

# 等待扫描（每 30 秒向用户报告进度）
# 耐心等待！大目录需要 5-10 分钟
sleep 30 && tmux capture-pane -t mole -p
```

### 1.4 进度报告

定期向用户报告扫描进度：

```
📊 磁盘分析进行中...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 已用时间：2 分钟

当前状态：
✅ 应用程序：49.5 GB（完成）
✅ 系统库：10.3 GB（完成）
⏳ 主目录：扫描中...（这可能需要 5-10 分钟）
⏳ 应用库：待处理

我正在耐心等待扫描完成。
将在 30 秒后再次报告...
```

### 1.5 呈现最终发现

扫描完成后，呈现结构化结果：

```
📊 磁盘空间分析（通过 Mole）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
可用空间：27 GB

🧹 可恢复空间（试运行预览）：

➤ 用户必备项
  • 用户应用缓存：     16.67 GB
  • 用户应用日志：      102.3 MB
  • 废纸篓：              642.9 MB

➤ 浏览器缓存
  • Chrome 缓存：       1.90 GB
  • Safari 缓存：       4 KB

➤ 开发工具
  • uv 缓存：           9.96 GB
  • npm 缓存：          （已检测）
  • Docker 缓存：       （已检测）
  • Homebrew 缓存：     （已检测）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总可恢复：~30 GB

⚠️ 这是试运行预览。未删除任何文件。
```

## 第二步：深度分析类别

系统地扫描以下类别。参考 `references/cleanup_targets.md` 获取详细说明。

### 类别 1：系统和应用缓存

**要分析的位置：**
- `~/Library/Caches/*` - 用户应用缓存
- `/Library/Caches/*` - 系统范围缓存（需要 sudo）
- `~/Library/Logs/*` - 应用日志
- `/var/log/*` - 系统日志（需要 sudo）

**分析脚本：**
```bash
scripts/analyze_caches.py --user-only
```

**安全级别**：🟢 通常可以安全删除（应用会重新生成缓存）

**要保留的例外：**
- 浏览器运行时的浏览器缓存
- IDE 缓存（可能会减慢下次启动）
- 包管理器缓存（Homebrew、pip、npm）

### 类别 2：应用残留

**要分析的位置：**
- `~/Library/Application Support/*` - 应用数据
- `~/Library/Preferences/*` - 偏好设置文件
- `~/Library/Containers/*` - 沙盒应用数据

**分析方法：**
1. 列出 `/Applications` 中已安装的应用
2. 与 `~/Library/Application Support` 交叉引用
3. 识别孤立项（应用已卸载但数据保留）

**分析脚本：**
```bash
scripts/find_app_remnants.py
```

**安全级别**：🟡 需要谨慎
- ✅ 安全：明确已卸载应用的文件夹
- ⚠️ 先检查：您很少使用的应用的文件夹
- ❌ 保留：活动应用数据

### 类别 3：大文件和重复项

**分析脚本：**
```bash
scripts/analyze_large_files.py --threshold 100MB --path ~
```

**查找重复项（可选，资源密集型）：**
```bash
# 如果安装了 fdupes 则使用
if command -v fdupes &> /dev/null; then
  fdupes -r ~/Documents ~/Downloads
fi
```

**呈现发现：**
```
📦 大文件（>100MB）：
━━━━━━━━━━━━━━━━━━━━━━━━
1. movie.mp4                    4.2 GB  ~/Downloads
2. dataset.csv                  1.8 GB  ~/Documents/data
3. old_backup.zip               1.5 GB  ~/Desktop
...

🔁 重复文件：
- screenshot.png（3 个副本）     每个 15 MB
- document_v1.docx（2 个副本）   每个 8 MB
```

**安全级别**：🟡 需要用户判断

### 类别 4：开发环境清理

**目标：**
- Docker：镜像、容器、卷、构建缓存
- Homebrew：缓存、旧版本
- Node.js：`node_modules`、npm 缓存
- Python：pip 缓存、`__pycache__`、venv
- Git：存档项目中的 `.git` 文件夹

**分析脚本：**
```bash
scripts/analyze_dev_env.py
```

**示例发现：**
```
🐳 Docker 资源：
- 未使用的镜像：      12 GB
- 已停止的容器：  2 GB
- 构建缓存：         8 GB
- 孤立的卷：    3 GB
总潜在：      25 GB

📦 包管理器：
- Homebrew 缓存：      5 GB
- npm 缓存：           3 GB
- pip 缓存：           1 GB
总潜在：       9 GB

🗂️  旧项目：
- archived-project-2022/.git  500 MB
- old-prototype/.git          300 MB
```

**清理命令（需要确认）：**
```bash
# Homebrew 清理（安全）
brew cleanup -s

# npm _npx 仅限（安全 - 临时包）
rm -rf ~/.npm/_npx

# pip 缓存（谨慎使用）
pip cache purge
```

**Docker 清理 - 需要特殊处理：**

⚠️ **绝不使用这些命令：**
```bash
# ❌ 危险 - 无确认删除所有卷
docker volume prune -f
docker system prune -a --volumes
```

✅ **正确方法 - 逐卷确认：**
```bash
# 1. 列出所有卷
docker volume ls

# 2. 确定每个卷属于哪个项目
docker volume inspect <volume_name>

# 3. 要求用户确认要删除的每个项目
# 示例："您想删除 'ragflow' 项目的所有卷吗？"

# 4. 仅在确认后删除特定卷
docker volume rm ragflow_mysql_data ragflow_redis_data
```

**安全级别**：🟢 Homebrew/npm 清理，🔴 Docker 卷需要按项目确认

## 第三步：与 Mole 集成

**Mole**（https://github.com/tw93/Mole）是一个用于全面 macOS 清理的**命令行界面（CLI）**工具。它为缓存、日志、开发工具等提供基于交互式终端的分析和清理。

**关键要求：**

1. **TTY 环境**：Mole 需要 TTY 进行交互式命令。从 Claude Code 或脚本运行时使用 `tmux`。
2. **版本检查**：使用前始终验证 Mole 是最新的。
3. **安全的帮助命令**：只有 `mo --help` 是安全的。不要在其他命令后附加 `--help`。

**安装检查和升级：**

```bash
# 检查是否安装并获取版本
which mo && mo --version

# 如果未安装
brew install tw93/tap/mole

# 检查更新
brew info tw93/tap/mole | head -5

# 如果需要则升级
brew upgrade tw93/tap/mole
```

**使用 tmux 与 Mole 一起使用（Claude Code 必需）：**

```bash
# 创建 tmux 会话以获得 TTY 环境
tmux new-session -d -s mole -x 120 -y 40

# 运行分析（安全，只读）
tmux send-keys -t mole 'mo analyze' Enter

# 等待扫描（耐心 - 大目录可能需要 5-10 分钟）
sleep 60

# 捕获结果
tmux capture-pane -t mole -p

# 完成后清理
tmux kill-session -t mole
```

**可用命令（来自 `mo --help`）：**

| 命令 | 安全性 | 说明 |
|---------|--------|-------------|
| `mo --help` | ✅ 安全 | 查看所有命令（唯一安全的帮助） |
| `mo analyze` | ✅ 安全 | 磁盘使用浏览器（只读） |
| `mo status` | ✅ 安全 | 系统健康监控 |
| `mo clean --dry-run` | ✅ 安全 | 预览清理（无删除） |
| `mo clean` | ⚠️ 危险 | 实际删除文件 |
| `mo purge` | ⚠️ 危险 | 删除项目工件 |
| `mo uninstall` | ⚠️ 危险 | 删除应用程序 |

**参考指南：**
详见 `references/mole_integration.md` 获取详细的 tmux 工作流程和故障排除。

## 使用 Mole 进行多层深度探索

**关键**：为了全面分析，您必须执行多层探索，而不仅仅是顶层扫描。本节记录了导航 Mole TUI 的经过验证的工作流程。

### 导航命令

```bash
# 创建会话
tmux new-session -d -s mole -x 120 -y 40

# 开始分析
tmux send-keys -t mole 'mo analyze' Enter

# 等待初始扫描
sleep 8 && tmux capture-pane -t mole -p

# 导航键（通过 tmux 发送）
tmux send-keys -t mole Enter    # 进入/展开选定目录
tmux send-keys -t mole Left     # 返回父目录
tmux send-keys -t mole Down     # 移动到下一项
tmux send-keys -t mole Up       # 移动到上一项
tmux send-keys -t mole 'q'      # 退出 TUI

# 捕获当前视图
tmux capture-pane -t mole -p
```

### 多层探索工作流程

**步骤 1：顶层概览**
```bash
# 启动 mo analyze，等待初始菜单
tmux send-keys -t mole 'mo analyze' Enter
sleep 8 && tmux capture-pane -t mole -p

# 示例输出：
# 1. 主目录           289.4 GB (58.5%)
# 2. 应用库    145.2 GB (29.4%)
# 3. 应用程序    49.5 GB (10.0%)
# 4. 系统库  10.3 GB (2.1%)
```

**步骤 2：进入最大目录（主目录）**
```bash
tmux send-keys -t mole Enter
sleep 10 && tmux capture-pane -t mole -p

# 示例输出：
# 1. 库       144.4 GB (49.9%)
# 2. 工作区      52.0 GB (18.0%)
# 3. .cache         19.3 GB (6.7%)
# 4. 应用程序   17.0 GB (5.9%)
# ...
```

**步骤 3：深入特定目录**
```bash
# 进入 .cache（第 3 项：Down Down Enter）
tmux send-keys -t mole Down Down Enter
sleep 5 && tmux capture-pane -t mole -p

# 示例输出：
# 1. uv           10.3 GB (55.6%)
# 2. modelscope    5.5 GB (29.5%)
# 3. huggingface   887.8 MB (4.7%)
```

**步骤 4：返回并探索另一个分支**
```bash
# 返回父目录
tmux send-keys -t mole Left
sleep 2

# 导航到不同目录
tmux send-keys -t mole Down Down Down Down Enter  # 进入 .npm
sleep 5 && tmux capture-pane -t mole -p
```

**步骤 5：深入库**
```bash
# 返回主目录，然后进入库
tmux send-keys -t mole Left
tmux send-keys -t mole Up Up Up Up Up Up Enter  # 进入库
sleep 10 && tmux capture-pane -t mole -p

# 示例输出：
# 1. 应用支持  37.1 GB
# 2. 容器          35.4 GB
# 3. 开发者           17.8 GB  ← Xcode 在这里
# 4. 缓存               8.2 GB
```

### 推荐的探索路径

为了全面分析，请遵循此探索树：

```
mo analyze
├── 主目录（进入）
│   ├── 库（进入）
│   │   ├── 开发者（进入） → Xcode/DerivedData、iOS DeviceSupport
│   │   ├── 缓存（进入） → Playwright、JetBrains 等
│   │   └── 应用支持（进入） → 应用数据
│   ├── .cache（进入） → uv、modelscope、huggingface
│   ├── .npm（进入） → _cacache、_npx
│   ├── 下载（进入） → 待审查的大文件
│   ├── .Trash（进入） → 确认废纸篓内容
│   └── miniconda3/其他开发工具（进入） → 检查最后使用时间
├── 应用库 → 通常与 ~/Library 重叠
└── 应用程序 → 已安装的应用
```

### 时间预期

| 目录 | 扫描时间 | 说明 |
|-----------|-----------|-------|
| 顶层菜单 | 5-8 秒 | 快速 |
| 主目录 | 5-10 分钟 | 大型，请耐心 |
| ~/Library | 3-5 分钟 | 许多小文件 |
| 子目录 | 2-30 秒 | 根据大小变化 |

### 完整会话示例

```bash
# 1. 创建会话
tmux new-session -d -s mole -x 120 -y 40

# 2. 开始分析并获取概览
tmux send-keys -t mole 'mo analyze' Enter
sleep 8 && tmux capture-pane -t mole -p

# 3. 进入主目录
tmux send-keys -t mole Enter
sleep 10 && tmux capture-pane -t mole -p

# 4. 进入 .cache 查看开发缓存
tmux send-keys -t mole Down Down Enter
sleep 5 && tmux capture-pane -t mole -p

# 5. 返回主目录，然后到 .npm
tmux send-keys -t mole Left
sleep 2
tmux send-keys -t mole Down Down Down Down Enter
sleep 5 && tmux capture-pane -t mole -p

# 6. 返回主目录，进入库
tmux send-keys -t mole Left
sleep 2
tmux send-keys -t mole Up Up Up Up Up Up Enter
sleep 10 && tmux capture-pane -t mole -p

# 7. 进入开发者查看 Xcode
tmux send-keys -t mole Down Down Down Enter
sleep 5 && tmux capture-pane -t mole -p

# 8. 进入 Xcode
tmux send-keys -t mole Enter
sleep 5 && tmux capture-pane -t mole -p

# 9. 进入 DerivedData 查看项目
tmux send-keys -t mole Enter
sleep 5 && tmux capture-pane -t mole -p

# 10. 清理
tmux kill-session -t mole
```

### 探索的关键见解

经过多层探索后，您将发现：

1. **哪些项目正在使用 DerivedData** - 具体项目名称
2. **哪些缓存实际上很大** - uv vs npm vs 其他
3. **文件年龄** - Mole 显示">3mo"、">7mo"、">1yr"标记
4. **特定卷及其用途** - Docker 项目数据
5. **可以清理的下载** - 旧的 dmgs、重复文件

## 反模式：不应删除的内容

**关键**：以下项目通常建议清理，但在大多数情况下不应删除。它们提供的显著价值超过了它们占用的空间。

### 要保留的项目（反模式）

| 项目 | 大小 | 为什么不删除 | 删除的实际影响 |
|------|------|-------------------|------------------------|
| **Xcode DerivedData** | 10+ GB | 构建缓存每次完整重新构建节省 10-30 分钟 | 下次构建需要额外 10-30 分钟 |
| **npm _cacache** | 5+ GB | 下载的包在本地缓存 | `npm install` 重新下载所有内容（中国 30分钟-2小时） |
| **~/.cache/uv** | 10+ GB | Python 包缓存 | 每个 Python 项目从 PyPI 重新安装依赖 |
| **Playwright 浏览器** | 3-4 GB | 自动化测试的浏览器二进制文件 | 每次重新下载 2GB+（30分钟-1小时） |
| **iOS DeviceSupport** | 2-3 GB | 设备调试所需 | 连接设备时从 Apple 重新下载 |
| **Docker 已停止的容器** | <500 MB | 可能随时使用 `docker start` 重新启动 | 丢失容器状态，需要重新创建 |
| **~/.cache/huggingface** | 变化 | AI 模型缓存 | 重新下载大模型（数小时） |
| **~/.cache/modelscope** | 变化 | AI 模型缓存（中国） | 同上 |
| **JetBrains 缓存** | 1+ GB | IDE 索引和缓存 | IDE 需要 5-10 分钟重新索引 |

### 为什么这很重要

**虚荣陷阱**：显示"清理了 50GB！"感觉很爽，但：
- 用户接下来花费 2 小时重新下载 npm 包
- 下次 Xcode 构建需要 30 分钟而不是 30 秒
- AI 项目失败因为模型需要重新下载

**正确心态**："我发现了 50GB 缓存。以下是为什么其中大部分实际上有价值应该保留..."

### 什么实际上可以安全删除

| 项目 | 为什么安全 | 影响 |
|------|----------|--------|
| **废纸篓** | 用户已删除这些文件 | 无 - 用户的决定 |
| **Homebrew 旧版本** | 被新版本替换 | 罕见：无法回滚到旧版本 |
| **npm _npx** | 临时 npx 执行 | 轻微：npx 下次使用时重新下载 |
| **孤立应用残留** | 应用已卸载 | 无 - 应用不存在 |
| **特定未使用的 Docker 卷** | 项目确认已放弃 | 无 - 如果真的已放弃 |

## 报告格式要求

每个清理报告必须遵循此格式并包含影响分析：

```markdown
## 磁盘分析报告

### 分类图例
| 符号 | 含义 |
|--------|---------|
| 🟢 | **绝对安全** - 无负面影响，真正未使用 |
| 🟡 | **需要权衡** - 有用缓存，删除有成本 |
| 🔴 | **不要删除** - 包含有价值的数据或正在使用 |

### 发现

| 项目 | 大小 | 分类 | 是什么 | 删除后影响 |
|------|------|----------------|------------|-------------------|
| 废纸篓 | 643 MB | 🟢 | 您删除的文件 | 无 |
| npm _npx | 2.1 GB | 🟢 | 临时 npx 包 | 轻微重新下载 |
| npm _cacache | 5 GB | 🟡 | 包缓存 | 30分钟-2小时重新下载 |
| DerivedData | 10 GB | 🟡 | Xcode 构建缓存 | 10-30分钟重新构建 |
| Docker 卷 | 11 GB | 🔴 | 项目数据库 | **数据丢失** |

### 建议
仅标记为 🟢 的项目建议清理。
标记为 🟡 的项目需要您根据使用模式进行判断。
标记为 🔴 的项目需要每项明确确认。
```

## 高质量报告模板

经过多层探索后，使用此经过验证的模板呈现发现：

```markdown
## 📊 磁盘空间深度分析报告

**分析日期**：YYYY-MM-DD
**使用工具**：Mole CLI + 多层目录探索
**分析原则**：安全第一，价值优于虚荣

---

### 总览

| 区域 | 总占用 | 关键发现 |
|------|--------|----------|
| **主目录** | XXX GB | 库占一半(XXX GB) |
| **应用库** | XXX GB | 与主目录/库重叠统计 |
| **应用程序** | XXX GB | 应用本体 |

---

### 🟢 绝对安全可删除（约 X.X GB）

| 项目 | 大小 | 位置 | 删除后影响 | 清理命令 |
|------|------|------|-----------|---------|
| **废纸篓** | XXX MB | ~/.Trash | 无 - 您已决定删除的文件 | 清空废纸篓 |
| **npm _npx** | X.X GB | ~/.npm/_npx | 下次 npx 命令重新下载 | `rm -rf ~/.npm/_npx` |
| **Homebrew 旧版本** | XX MB | /opt/homebrew | 无 - 已被新版本替代 | `brew cleanup --prune=0` |

**废纸篓内容预览**：
- [列出主要文件]

---

### 🟡 需要您确认的项目

#### 1. [项目名] (X.X GB) - [状态描述]

| 子目录 | 大小 | 最后使用 |
|--------|------|----------|
| [子目录1] | X.X GB | >X个月 |
| [子目录2] | X.X GB | >X个月 |

**问题**：[需要用户回答的问题]

---

#### 2. Downloads 中的旧文件 (X.X GB)

| 文件/目录 | 大小 | 年龄 | 建议 |
|-----------|------|------|------|
| [文件1] | X.X GB | - | [建议] |
| [文件2] | XXX MB | >X个月 | [建议] |

**建议**：手动检查 Downloads，删除已不需要的文件。

---

#### 3. 停用的 Docker 项目 Volumes

| 项目前缀 | 可能包含的数据 | 需要您确认 |
|---------|--------------|-----------|
| `project1_*` | MySQL、Redis | 还在用吗？ |
| `project2_*` | Postgres | 还在用吗？ |

**注意**：我不会使用 `docker volume prune -f`，只会在您确认后删除特定项目的 volumes。

---

### 🔴 不建议删除的项目（有价值的缓存）

| 项目 | 大小 | 为什么要保留 |
|------|------|-------------|
| **Xcode DerivedData** | XX GB | [项目名]的编译缓存，删除后下次构建需要X分钟 |
| **npm _cacache** | X.X GB | 所有下载过的 npm 包，删除后需要重新下载 |
| **~/.cache/uv** | XX GB | Python 包缓存，重新下载在中国网络下很慢 |
| [其他有价值的缓存] | X.X GB | [保留原因] |

---

### 📋 其他发现

| 项目 | 大小 | 说明 |
|------|------|------|
| **OrbStack/Docker** | XX GB | 正常的 VM/容器占用 |
| [其他发现] | X.X GB | [说明] |

---

### 推荐操作

**立即可执行**（无需确认）：
```bash
# 1. 清空废纸篓 (XXX MB)
# 手动：Finder → 清空废纸篓

# 2. npm _npx (X.X GB)
rm -rf ~/.npm/_npx

# 3. Homebrew 旧版本 (XX MB)
brew cleanup --prune=0
```

**预计释放**：~X.X GB

---

**需要您确认后执行**：

1. **[项目1]** - [确认问题]
2. **[项目2]** - [确认问题]
3. **Docker 项目** - 告诉我哪些项目确定不用了
```

### 报告质量检查清单

在呈现报告之前，验证：

- [ ] 每个项目都有"删除后影响"说明
- [ ] 🟢 项目真正安全（废纸篓、_npx、旧版本）
- [ ] 🟡 项目需要用户决定（年龄信息、使用模式）
- [ ] 🔴 项目解释为什么要保留
- [ ] Docker 卷按项目列出，而不是全面清理
- [ ] 考虑网络环境（中国 = 重新下载慢）
- [ ] 没有建议删除有用的缓存只是为了夸大数字
- [ ] 清晰的操作项和确切的命令

## 第四步：呈现建议

将发现格式化为具有风险级别的可执行建议：

```markdown
# macOS 清理建议

## 摘要
总可恢复空间：~XX GB
当前使用率：XX%

## 推荐操作

### 🟢 可以安全执行（低风险）
这些可以安全删除，将根据需要重新生成：

1. **清空废纸篓**（~12 GB）
   - 位置：~/.Trash
   - 命令：`rm -rf ~/.Trash/*`

2. **清除系统缓存**（~45 GB）
   - 位置：~/Library/Caches
   - 命令：`rm -rf ~/Library/Caches/*`
   - 注意：应用下次启动可能会稍微慢一些

3. **删除 Homebrew 缓存**（~5 GB）
   - 命令：`brew cleanup -s`

### 🟡 建议审查（中等风险）
删除前审查这些项目：

1. **大文件下载**（~38 GB）
   - 位置：~/Downloads
   - 操作：手动审查并删除不需要的文件
   - 文件：[列出前 10 个最大文件]

2. **应用残留**（~8 GB）
   - 应用：[列出检测到的已卸载应用]
   - 位置：[列出路径]
   - 操作：在删除数据前确认应用真的已卸载

### 🔴 除非确定否则保留（高风险）
仅在您知道自己在做什么时才删除：

1. **Docker 卷**（~3 GB）
   - 可能包含重要数据
   - 使用以下命令审查：`docker volume ls`

2. **Time Machine 本地快照**（~XX GB）
   - 自动备份，需要空间时将删除
   - 检查命令：`tmutil listlocalsnapshots /`
```

## 第五步：确认后执行

**关键**：没有明确的用户确认绝不执行删除操作。

**交互式确认流程：**

```python
# 来自 scripts/safe_delete.py 的示例
def confirm_delete(path: str, size: str, description: str) -> bool:
    """
    请求用户确认删除。

    参数：
        path：文件/目录路径
        size：人类可读的大小
        description：此文件/目录是什么

    返回：
        如果用户确认则为 True，否则为 False
    """
    print(f"\n🗑️  确认删除")
    print(f"━━━━━━━━━━━━━━━━━━")
    print(f"路径：        {path}")
    print(f"大小：        {size}")
    print(f"说明：{description}")

    response = input("\n删除此项目？[y/N]：").strip().lower()
    return response == 'y'
```

**对于批量操作：**

```python
def batch_confirm(items: list) -> list:
    """
    显示所有项目，请求批量确认。

    返回用户批准的项目列表。
    """
    print("\n📋 要删除的项目：")
    print("━━━━━━━━━━━━━━━━━━")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['path']} ({item['size']})")

    print("\n选项：")
    print("  'all'    - 删除所有项目")
    print("  '1,3,5'  - 按编号删除特定项目")
    print("  'none'   - 取消")

    response = input("\n您的选择：").strip().lower()

    if response == 'none':
        return []
    elif response == 'all':
        return items
    else:
        # 解析数字
        indices = [int(x.strip()) - 1 for x in response.split(',')]
        return [items[i] for i in indices if 0 <= i < len(items)]
```

## 第六步：验证结果

清理后，验证结果并报告：

```bash
# 比较之前/之后
df -h /

# 计算恢复的空间
#（由 scripts/cleanup_report.py 处理）
```

**报告格式：**

```
✅ 清理完成！

之前：已使用 450 GB（90%）
之后：  已使用 385 GB（77%）
━━━━━━━━━━━━━━━━━━━━━━━━
已恢复：65 GB

细分：
- 系统缓存：        45 GB
- 下载：            12 GB
- Homebrew 缓存：        5 GB
- 应用残留：  3 GB

⚠️ 注意：
- 某些应用首次启动可能需要更长时间
- 除非您有 Time Machine 备份，否则无法恢复已删除的项目
- 建议每月运行此清理一次

💡 维护提示：
- 设置自动 Homebrew 清理：每周 `brew cleanup`
- 每月审查 Downloads 文件夹
- 在 Finder 偏好设置中启用"自动清空废纸篓"
```

## 安全指南

### 始终保留

没有明确的用户指示绝不删除这些：
- `~/Documents`、`~/Desktop`、`~/Pictures` 内容
- 活动项目目录
- 数据库文件（*.db、*.sqlite）
- 活动应用的配置文件
- SSH 密钥、凭据、证书
- Time Machine 备份

### 需要 Sudo 确认

这些操作需要提升的权限。要求用户手动运行命令：
- 清除 `/Library/Caches`（系统范围）
- 清除 `/var/log`（系统日志）
- 清除 `/private/var/folders`（系统临时）

示例提示：
```
⚠️ 此操作需要管理员权限。

请手动运行此命令：
  sudo rm -rf /Library/Caches/*

⚠️ 您将被要求输入密码。
```

### 备份建议

在执行任何 >10GB 的清理之前，建议：

```
💡 安全提示：
在清理 XX GB 之前，考虑创建 Time Machine 备份。

快速备份检查：
  tmutil latestbackup

如果没有最近备份，运行：
  tmutil startbackup
```

## 故障排除

### "Operation not permitted"错误

macOS 可能由于 SIP（系统完整性保护）而阻止删除某些系统文件。

**解决方案**：不要强制操作。这些保护是为了安全而存在的。

### 缓存删除后应用崩溃

罕见但可能。**解决方案**：重新启动应用，它将重新生成必要的缓存。

### Docker 清理删除重要数据

**预防**：清理前始终列出 Docker 卷：
```bash
docker volume ls
docker volume inspect <volume_name>
```

## 资源

### scripts/

- `analyze_caches.py` - 扫描和分类缓存目录
- `find_app_remnants.py` - 检测孤立的应用数据
- `analyze_large_files.py` - 使用智能过滤查找大文件
- `analyze_dev_env.py` - 扫描开发环境资源
- `safe_delete.py` - 带确认的交互式删除
- `cleanup_report.py` - 生成之前/之后报告

### references/

- `cleanup_targets.md` - 每个清理目标的详细说明
- `mole_integration.md` - 如何与此技能一起使用 Mole
- `safety_rules.md` - 绝不删除的内容的综合列表

## 使用示例

### 示例 1：快速缓存清理

用户请求："我的 Mac 空间不足，你能帮助吗？"

工作流程：
1. 运行快速诊断
2. 将系统缓存识别为快速胜利
3. 呈现发现："~/Library/Caches 中有 45 GB"
4. 解释："这些可以安全删除，应用会重新生成它们"
5. 请求确认
6. 执行：`rm -rf ~/Library/Caches/*`
7. 报告："已恢复 45 GB"

### 示例 2：开发环境清理

用户请求："我是开发人员，我的磁盘满了"

工作流程：
1. 运行 `scripts/analyze_dev_env.py`
2. 呈现 Docker + npm + Homebrew 发现
3. 解释每个类别
4. 提供清理命令和说明
5. 让用户执行（不要自动执行 Docker 清理）
6. 验证结果

### 示例 3：查找大文件

用户请求："什么占用了这么多空间？"

工作流程：
1. 运行 `scripts/analyze_large_files.py --threshold 100MB`
2. 呈现前 20 个大文件及其上下文
3. 分类：视频、数据集、档案、磁盘映像
4. 让用户决定删除什么
5. 执行已确认的删除
6. 建议存档到外部驱动器

## 最佳实践

1. **从保守开始**：从明显安全的目标（缓存、废纸篓）开始
2. **解释一切**：用户应该了解他们正在删除的内容
3. **显示示例**：列出每个类别的 3-5 个示例文件
4. **尊重用户节奏**：不要匆忙进行确认
5. **记录结果**：始终显示之前/之后的磁盘使用情况
6. **教育**：在最终报告中包含维护提示
7. **集成工具**：为更喜欢 GUI 的用户建议 Mole

## 何时不使用此技能

- 用户想要自动/静默清理（违反安全第一原则）
- 用户需要 Windows/Linux 清理（macOS 特定技能）
- 用户磁盘使用率 <10%（无需清理）
- 用户想要清理需要禁用 SIP 的系统文件（安全风险）

在这些情况下，解释局限性并建议替代方案。
