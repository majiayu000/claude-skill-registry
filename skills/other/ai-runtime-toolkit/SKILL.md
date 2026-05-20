---
name: external-tools-skill
description: 外部CLI工具装备系统，支持10+个成熟CLI工具的深度整合，包括fzf、ripgrep、jq等，提供模糊搜索、代码查找、JSON处理等高级功能
license: MIT
version: 2.0.0
---

# 外部工具装备系统

## 概述

外部工具装备系统遵循"**整合 > 创造**"的核心理念，通过深度整合成熟的CLI工具，为AI Runtime提供强大的外部能力扩展。系统支持10+个经过社区验证的工具，无需重复造轮子。

## 核心能力

### 工具生态
- **基础必备**: fzf、eza、bat、ripgrep、zoxide、jq
- **搜索增强**: fd、ripgrep的高性能代码搜索
- **数据处理**: jq的强大JSON处理能力
- **界面优化**: 美化文件列表、语法高亮、智能跳转

### 深度整合
- **自动检测**: 系统自动发现已安装的工具
- **元数据管理**: 标准化的工具描述和参数定义
- **统一接口**: 通过discover-toolkit.py统一调用

## 快速开始

### 安装推荐工具

**macOS**:
```bash
brew install fzf eza zoxide fd bat ripgrep jq
```

**Ubuntu/Debian**:
```bash
sudo apt-get install fzf ripgrep jq bat
```

### 基本使用

```bash
# 进入工具装备目录
cd .ai-runtime/toolkit

# 查看外部工具
python3 discover-toolkit.py list --external

# 检查安装状态
python3 discover-toolkit.py check-external
```

## 推荐工具详解

### 基础必备工具

#### fzf - 模糊查找器
```bash
# 交互式文件选择
find . -name "*.py" | fzf

# 历史命令搜索
history | fzf
```

#### eza - 现代化ls
```bash
# 美化文件列表
eza -la

# 树状结构显示
eza -T
```

#### bat - 语法高亮cat
```bash
# 带语法高亮的代码查看
bat script.py

# 与fzf结合使用
find . -name "*.md" | fzf | xargs bat
```

#### ripgrep - 极速搜索
```bash
# 递归搜索代码
rg "TODO|FIXME"

# 搜索特定文件类型
rg "function" --type py
```

#### zoxide - 智能跳转
```bash
# 跳转到常用目录
z project-name

# 查看权重统计
zoxide query
```

#### jq - JSON处理器
```bash
# 格式化JSON
cat data.json | jq '.'

# 提取字段
cat package.json | jq '.dependencies | keys[]'
```

## 渐进式披露文档

### 工具详解
- **[fzf使用指南](../docs/tools/external/fzf.md)** - 模糊查找器的完整指南
- **[eza使用指南](../docs/tools/external/eza.md)** - 现代化文件列表工具
- **[bat使用指南](../docs/tools/external/bat.md)** - 语法高亮文件查看器
- **[ripgrep使用指南](../docs/tools/external/ripgrep.md)** - 高性能代码搜索工具
- **[zoxide使用指南](../docs/tools/external/zoxide.md)** - 智能目录跳转工具
- **[jq使用指南](../docs/tools/external/jq.md)** - JSON命令行处理器

### 整合指南
- **[外部工具整合详解](../docs/guides/external-integration.md)** - 如何整合更多第三方工具

## 使用场景

### 代码开发
```bash
# 搜索代码模式
rg "class.*Test" src/

# 交互式文件选择和查看
find src/ -name "*.py" | fzf | xargs bat

# 智能目录跳转
z projects/my-api
```

### 数据处理
```bash
# 处理API响应
curl -s http://api.example.com/data | jq '.items[] | select(.active == true)'

# 日志分析
cat app.log | rg "ERROR" | jq -R 'fromjson?' 2>/dev/null || cat app.log | rg "ERROR"
```

### 系统管理
```bash
# 美化文件列表
eza -la --git

# 快速文件预览
bat /etc/hosts

# 历史命令搜索
history | fzf | bash
```

## 相关系统

- **[工具装备总览](SKILL.md)** - 完整的工具装备系统
- **[内部工具详解](../docs/references/internal-tools.md)** - AI Runtime自主创建的工具
- **[宪法文档](../.ai-runtime/constitution.md)** - 治理原则和约束

## 版本信息

- **版本**: 2.0.0
- **工具数量**: 10+个外部CLI工具
- **最后更新**: 2025-11-14

---

*基于 anthropics/skills 渐进式披露架构设计*
