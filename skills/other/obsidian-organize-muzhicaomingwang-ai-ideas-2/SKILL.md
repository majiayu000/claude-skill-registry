---
name: obsidian-organize
description: |
  Obsidian 知识库整理工作流。
  触发场景：用户提到"整理Obsidian"、"清理文件夹"、"知识库混乱"、"目录太多"、"合并分类"。
  适用于：个人知识管理、笔记整理、文件夹重组。
---

# Obsidian 知识库整理 Skill

## 概述

此 Skill 定义了 **Obsidian 知识库文件夹整理** 的标准操作流程，目标是将混乱的目录结构精简为 7-10 个顶级分类。

## 核心原则

1. **7±2 原则** - 顶级文件夹控制在 5-9 个（认知负载最优）
2. **MECE 原则** - 分类互斥且穷尽，避免重叠
3. **渐进式** - 保留原结构痕迹，便于回溯
4. **安全第一** - 合并前确认，删除前备份

## 标准分类体系（推荐）

| 分类 | 命名 | 包含内容 |
|------|------|---------|
| 收件箱 | `_Inbox` | 未分类笔记、临时文件、待处理内容 |
| 附件 | `_attachments` | 图片、PDF、音频等媒体文件 |
| 日记 | `Journal` | 日记、周记、月度复盘、年度总结 |
| 阅读 | `Reading` | 书籍笔记、文章摘录、播客记录 |
| 工作 | `Work` | 工作项目、会议纪要、团队分享 |
| 技术 | `Tech` | 技术笔记、代码片段、工具配置 |
| 人物 | `People` | 人物档案、社交关系、联系方式 |
| 项目 | `Projects` | 个人项目、副业、创业想法 |
| 成长 | `Growth` | 认知提升、学习计划、技能发展 |

> 注意：`_` 前缀使系统文件夹排在最前

## 标准操作流程 (SOP)

### Phase 1: 分析现状

1. 定位 Obsidian Vault 路径（通常在 `~/Documents/Obsidian Vault/`）
2. 统计现有顶级文件夹数量和名称
3. 统计各文件夹内文件数量
4. 识别重复/相似/可合并的分类

```bash
# 查看目录结构
ls -la "/path/to/Obsidian Vault/"

# 统计各文件夹文件数
for dir in "/path/to/Obsidian Vault/"*/; do
  echo "$(basename "$dir"): $(find "$dir" -type f | wc -l) files"
done
```

### Phase 2: 制定整理计划

根据现有文件夹，制定合并映射表：

```markdown
| 原文件夹 | 目标分类 | 操作 |
|---------|---------|------|
| 日记/ | Journal | 合并 |
| 当日日记/ | Journal | 合并 |
| books/ | Reading | 合并 |
| 读书/ | Reading | 合并 |
| QAL分享/ | Work | 合并 |
| 临时文件/ | _Inbox | 合并 |
```

### Phase 3: 执行合并

**合并操作模板**（使用 cp + rm 更安全）：

```bash
# 1. 创建目标目录（如不存在）
mkdir -p "/path/to/Obsidian Vault/TargetFolder"

# 2. 复制源文件夹内容到目标
cp -r "/path/to/Obsidian Vault/SourceFolder/"* "/path/to/Obsidian Vault/TargetFolder/"

# 3. 确认复制成功后删除源文件夹
rm -rf "/path/to/Obsidian Vault/SourceFolder"
```

**批量合并示例**：

```bash
VAULT="/Users/xxx/Documents/Obsidian Vault"

# 合并日记类
mkdir -p "$VAULT/Journal"
cp -r "$VAULT/日记/"* "$VAULT/Journal/" 2>/dev/null
cp -r "$VAULT/当日日记/"* "$VAULT/Journal/" 2>/dev/null
rm -rf "$VAULT/日记" "$VAULT/当日日记"

# 合并阅读类
mkdir -p "$VAULT/Reading"
cp -r "$VAULT/books/"* "$VAULT/Reading/" 2>/dev/null
cp -r "$VAULT/读书/"* "$VAULT/Reading/" 2>/dev/null
rm -rf "$VAULT/books" "$VAULT/读书"
```

### Phase 4: 验证结果

1. 检查顶级文件夹数量是否 ≤ 10
2. 确认无空文件夹残留
3. 抽查合并后文件是否完整
4. 更新 Obsidian 索引（重启 Obsidian 或刷新）

```bash
# 统计最终结构
ls -d "$VAULT"/*/ | wc -l

# 查找空目录
find "$VAULT" -type d -empty
```

## 常见问题处理

### 路径包含空格
```bash
# 错误
cd /path/Obsidian Vault  # 会失败

# 正确
cd "/path/Obsidian Vault"
```

### 文件夹名有特殊字符
```bash
# 文件夹名以空格开头（如 " books"）
rm -rf "/path/ books"  # 包含空格
```

### rmdir 失败（目录非空）
```bash
# 使用 rm -rf 替代 rmdir
rm -rf "/path/to/folder"
```

### 合并时文件冲突
```bash
# 使用 -n 避免覆盖
cp -rn source/* dest/

# 或使用 rsync 更精细控制
rsync -av --ignore-existing source/ dest/
```

## 整理前后对比示例

**整理前（20+ 文件夹）**：
```
APP.ai/
Memory Engineering/
QAL分享/
books/
secondme/
信息熵/
当日日记/
日记/
读书/
鲲鹏会/
...（共 20+ 个）
```

**整理后（10 文件夹）**：
```
_Inbox/          # 临时文件
_attachments/    # 附件
AI-Engineering/  # AI 技术
Cognitive-Growth/# 认知成长
Journal/         # 日记
People/          # 人物
Reading/         # 阅读
Tech-Foundation/ # 技术基础
Travel-Product/  # 旅行产品
Work-Sharing/    # 工作分享
```

## 使用示例

### 示例 1：快速整理

```
用户: 我的 Obsidian 太乱了，帮我整理一下

Claude:
1. [定位 Vault 路径]
2. [统计现有文件夹]
3. [制定合并计划]
4. [用户确认后执行]
5. [验证结果]
```

### 示例 2：指定目标数量

```
用户: 把我的 Obsidian 整理到 7 个分类以内

Claude:
1. [分析现有结构]
2. [设计 7 分类方案]
3. [展示合并映射表]
4. [执行并验证]
```

## 注意事项

1. **备份优先** - 大规模整理前建议备份整个 Vault
2. **渐进执行** - 一次合并一个分类，确认无误后继续
3. **保留索引** - 不要删除 `.obsidian/` 配置目录
4. **更新链接** - 合并后检查双链是否需要更新（Obsidian 通常自动处理）

## 相关资源

- Obsidian 官方文档：https://help.obsidian.md/
- PARA 方法论：Projects, Areas, Resources, Archives
- Johnny Decimal 系统：数字化分类法
