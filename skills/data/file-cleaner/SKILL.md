---
name: file-cleaner
description: 系统文件清理工具。扫描和识别大文件、垃圾文件（临时文件、缓存、日志、备份等），提供交互式清理界面让用户选择删除。当用户需要清理磁盘空间、整理系统文件、查找大文件、删除垃圾文件或释放存储空间时使用此技能。
---

# File Cleaner

系统文件清理工具，帮助用户扫描、识别和清理大文件与垃圾文件。

## 核心功能

### 1. 大文件扫描
扫描指定目录，找出占用空间的大文件（默认 >10MB）。

```bash
python3 scripts/find_large_files.py <directory> [options]
```

**选项：**
- `--min-size <MB>` - 最小文件大小（默认: 10）
- `--max-results <N>` - 最大结果数（默认: 100）
- `--show <N>` - 显示的文件数（默认: 20）
- `--export <path>` - 导出结果到 JSON

**示例：**
```bash
# 扫描 home 目录的大文件
python3 scripts/find_large_files.py ~

# 扫描大于 50MB 的文件
python3 scripts/find_large_files.py ~ --min-size 50

# 导出结果
python3 scripts/find_large_files.py ~ --export large_files.json
```

### 2. 垃圾文件扫描
扫描并识别各类垃圾文件：临时文件、缓存、日志、备份等。

```bash
python3 scripts/find_garbage.py <directory> [options]
```

**垃圾文件类别：**
- `temp_files` - 临时文件（.tmp, .temp, .bak, .swp, .DS_Store）
- `cache_files` - 缓存文件（__pycache__, *.pyc, .cache）
- `log_files` - 日志文件（*.log）
- `backup_files` - 备份文件（.backup, .old）
- `build_artifacts` - 构建产物（dist, build, .next, out）
- `editor_temp` - 编辑器临时文件（.swo, .swn）
- `download_temp` - 下载临时文件（.crdownload, .part）

**选项：**
- `--categories <cat1> <cat2>` - 指定扫描类别（默认: 全部）
- `--show <N>` - 每个类别显示的文件数（默认: 10）
- `--export <path>` - 导出结果到 JSON
- `--script <path>` - 生成清理脚本

**示例：**
```bash
# 扫描所有垃圾文件
python3 scripts/find_garbage.py ~

# 只扫描缓存和临时文件
python3 scripts/find_garbage.py ~ --categories cache_files temp_files

# 导出结果
python3 scripts/find_garbage.py ~ --export garbage_scan.json

# 生成清理脚本
python3 scripts/find_garbage.py ~ --script cleanup.sh
```

### 3. 交互式清理
基于扫描结果，提供交互式界面让用户选择要清理的文件。

```bash
python3 scripts/clean_interactive.py <scan_result.json> [options]
```

**选项：**
- `--type <garbage|large>` - 扫描结果类型（默认: garbage）
- `--dry-run` - 预演模式，不实际删除文件

**示例：**
```bash
# 清理垃圾文件
python3 scripts/clean_interactive.py garbage_scan.json

# 清理大文件
python3 scripts/clean_interactive.py large_files.json --type large

# 预演模式（测试）
python3 scripts/clean_interactive.py garbage_scan.json --dry-run
```

## 工作流程

### 标准流程：扫描 → 导出 → 清理

```bash
# 步骤 1: 扫描垃圾文件
python3 scripts/find_garbage.py ~ --export /tmp/garbage_scan.json

# 步骤 2: 交互式清理
python3 scripts/clean_interactive.py /tmp/garbage_scan.json
```

### 快速流程：直接清理（推荐）

对于垃圾文件，可以直接生成清理脚本：

```bash
# 生成清理脚本
python3 scripts/find_garbage.py ~ --script cleanup.sh

# 检查脚本（确认要删除的文件）
cat cleanup.sh

# 执行清理
bash cleanup.sh
```

### 大文件流程：分析 → 选择性清理

对于大文件，推荐使用交互式清理：

```bash
# 扫描大文件
python3 scripts/find_large_files.py ~ --export /tmp/large_files.json

# 交互式选择删除
python3 scripts/clean_interactive.py /tmp/large_files.json --type large
```

## 安全特性

### 自动排除
以下目录和文件会自动排除，避免误删：
- 系统目录：`/proc`, `/sys`, `/dev`, `/usr`, `/bin`等
- 版本控制：`.git`, `.svn`, `.hg`
- Python 环境：`venv`, `.venv`, `env`

### 垃圾文件分类
垃圾文件分为两类：

**🟢 安全删除（自动标记）：**
- 临时文件
- 缓存文件
- 备份文件
- 构建产物
- 编辑器临时文件

**🟡 需要确认（需手动检查）：**
- 日志文件（可能用于调试）
- 下载临时文件（可能未完成）

### 预演模式
使用 `--dry-run` 测试清理操作，不实际删除：

```bash
python3 scripts/clean_interactive.py scan.json --dry-run
```

## 使用建议

### 定期清理
建议每月执行一次文件清理：

```bash
# 每月清理脚本
python3 scripts/find_garbage.py ~ --export /tmp/monthly_scan.json
python3 scripts/clean_interactive.py /tmp/monthly_scan.json
```

### 磁盘空间不足
当磁盘空间不足时：

```bash
# 1. 找出最大的文件
python3 scripts/find_large_files.py ~ --min-size 100 --show 20

# 2. 清理垃圾文件
python3 scripts/find_garbage.py ~ --script cleanup.sh
bash cleanup.sh
```

### 项目清理
清理开发项目目录：

```bash
# 清理构建产物和缓存
python3 scripts/find_garbage.py ~/projects \
  --categories build_artifacts cache_files \
  --script project_cleanup.sh
```

## 注意事项

⚠️ **使用前必读：**

1. **先预览再删除**
   - 使用 `--dry-run` 测试
   - 查看扫描结果后再确认

2. **重要文件备份**
   - 删除前备份重要数据
   - 日志文件可能包含重要信息

3. **权限问题**
   - 某些文件可能需要 sudo 权限
   - 无权限的文件会自动跳过

4. **不可恢复**
   - 删除操作不可撤销
   - 建议使用 `trash` 命令而不是直接删除

## 脚本说明

### find_large_files.py
扫描大文件，输出文件列表和总大小。自动排除系统目录和版本控制目录。

### find_garbage.py
识别 7 种垃圾文件类型，分类统计，标记安全删除状态。可生成自动清理脚本。

### clean_interactive.py
交互式清理界面，支持按类别选择、批量操作、预演模式。显示文件详情和总大小。

## 示例场景

### 场景 1：磁盘空间告急
```bash
# 快速找出大文件
python3 scripts/find_large_files.py ~ --min-size 500 --show 10
```

### 场景 2：开发环境清理
```bash
# 清理所有构建产物
python3 scripts/find_garbage.py ~/projects \
  --categories build_artifacts cache_files \
  --export dev_cleanup.json

python3 scripts/clean_interactive.py dev_cleanup.json
```

### 场景 3：定期维护
```bash
# 完整扫描
python3 scripts/find_garbage.py ~ --export monthly_scan.json
python3 scripts/find_large_files.py ~ --export large_files.json

# 分别处理
python3 scripts/clean_interactive.py monthly_scan.json
python3 scripts/clean_interactive.py large_files.json --type large
```

## 故障排除

### 权限错误
```bash
# 使用 sudo（谨慎）
sudo python3 scripts/find_large_files.py /
```

### 扫描太慢
```bash
# 限制扫描深度（只扫描指定目录）
python3 scripts/find_large_files.py ~/Downloads --max-results 50
```

### JSON 导出失败
```bash
# 确保目录存在
mkdir -p /tmp
python3 scripts/find_garbage.py ~ --export /tmp/scan.json
```
