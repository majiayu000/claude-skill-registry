---
name: i18n-translate
description: 管理 iOS/macOS 应用的 *.xcstrings 本地化翻译文件。自动清理过期条目、检测缺失翻译、添加简繁体中文翻译。当用户需要处理翻译、补充缺失的 zh-Hans/zh-HK 翻译、或清理 *.xcstrings 文件时使用此 skill。
---

# iOS/macOS 本地化翻译管理

管理项目中所有 `*.xcstrings` 文件的中文翻译，支持简体中文 (zh-Hans) 和繁体中文 (zh-HK)。

## 工作流程

处理翻译请求时，首先查找所有 .xcstrings 文件，然后按以下顺序执行：

### 0. 查找所有 .xcstrings 文件

```bash
find . -name "*.xcstrings" -not -path ".*" | head -20
```

### 1. 清理过期条目

```bash
python3 scripts/clean_stale.py <文件路径>.xcstrings
```

删除所有 `extractionState` 为 `stale` 的条目。可批量处理所有文件：

```bash
find . -name "*.xcstrings" -not -path ".*" -exec python3 scripts/clean_stale.py {} \;
```

### 2. 检查缺失翻译

```bash
python3 scripts/check_missing.py <文件路径>.xcstrings
```

输出缺失的 zh-Hans 和 zh-HK 翻译统计。可批量检查：

```bash
for f in $(find . -name "*.xcstrings" -not -path ".*"); do
    echo "=== $f ==="
    python3 scripts/check_missing.py "$f"
done
```

### 3. 添加翻译

```bash
python3 scripts/add_translation.py <文件路径>.xcstrings "Key" "简体中文翻译" "繁體中文翻譯"
```

- `<文件路径>.xcstrings`: 目标文件路径（必需）
- `Key`: 条目的 key（必需）
- `zh-Hans`: 简体中文翻译（必需）
- `zh-HK`: 繁体中文翻译（可选，未提供时自动转换）

### 4. 验证文件

```bash
python3 scripts/validate.py <文件路径>.xcstrings
```

验证 JSON 格式正确性并统计翻译完成度。可批量验证：

```bash
for f in $(find . -name "*.xcstrings" -not -path ".*"); do
    echo "=== $f ==="
    python3 scripts/validate.py "$f"
done
```

### 批量处理所有文件

使用 `batch_process.py` 脚本一次性处理所有 .xcstrings 文件：

```bash
# 列出所有 .xcstrings 文件
python3 scripts/batch_process.py list

# 批量清理所有文件的过期条目
python3 scripts/batch_process.py clean

# 批量检查所有文件的缺失翻译
python3 scripts/batch_process.py check

# 批量验证所有文件的格式
python3 scripts/batch_process.py validate

# 指定项目目录
python3 scripts/batch_process.py validate --dir /path/to/project
```

## 翻译原则

- **占位符保持不变**: `%@`, `%lld`, `%1$@`, `%d` 等格式化占位符必须原样保留
- **技术术语**: API, SQLite, Host 等专有名词可保持英文
- **UI 文本**: 简洁明了，符合 macOS/iOS 应用习惯
- **简繁转换**: `add_translation.py` 包含常见词汇的简繁转换映射

## 使用示例

```
用户: 检查项目所有 xcstrings 文件缺少的翻译
→ 运行 batch_process.py list 查看所有文件
→ 运行 batch_process.py check 检查所有文件

用户: 为 Core.xcstrings 中的 "Copy" 添加翻译
→ 运行 add_translation.py Core/Core.xcstrings "Copy" "拷贝" "拷貝"

用户: 清理所有 xcstrings 文件中过期的翻译条目
→ 运行 batch_process.py clean

用户: 验证所有翻译文件的格式和完成度
→ 运行 batch_process.py validate

用户: 处理特定目录下的翻译文件
→ 运行 batch_process.py check --dir ./Modules
```

## 注意事项

- 所有操作会直接修改指定的 `.xcstrings` 文件
- 修改前建议先备份文件
- JSON 缩进使用 2 个空格
- 编码必须是 UTF-8
- 批量处理时使用 `find` 命令过滤掉隐藏文件（`.*/.*`）
