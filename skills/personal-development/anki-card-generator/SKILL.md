---
name: anki-card-generator
description: Generate and manage Anki flashcards in Markdown format. Trigger when user asks to create flashcards, add knowledge cards, make Anki cards, or requests cards for learning programming concepts, algorithms, or technical knowledge.
---

# Anki Card Generator

Generate Anki cards as Markdown, sync to Anki via AnkiConnect.

## Core Concept

- **一个 .md 文件 = 一张卡片**
- **文件夹 = 牌组**

## Directory Structure (示例)

```
project/
├── cards/                        # 卡片源文件根目录（必需）
│   ├── python/                   # → 牌组 "python"
│   │   ├── walrus.md             # → 牌组 "python", 卡片 "walrus"
│   │   ├── f-string.md           # → 牌组 "python", 卡片 "f-string"
│   │   └── tools/                # → 牌组 "python/tools"
│   │       ├── venv.md           # → 牌组 "python/tools", 卡片 "venv"
│   │       └── pip.md            # → 牌组 "python/tools", 卡片 "pip"
│   └── algorithms/
│       └── sorting/
│           ├── quicksort.md      # → 牌组 "algorithms/sorting"
│           └── mergesort.md      # → 牌组 "algorithms/sorting"
├── venv/                         # Python 虚拟环境（必需）
└── .claude/skills/anki-card-generator/  # 本 skill（必需）
```

**映射规则**: `cards/<folder>/<file>.md` → 牌组 `<folder>`, 卡片来自文件

## Card Format

```markdown
# 卡片正面（H1 标题）

卡片背面内容
支持代码块、表格、列表等
```

- H1 = 卡片正面（若无 H1，则用文件名）
- H1 之后的内容 = 卡片背面
- SourceID = `hash(文件相对路径)`

## Content Best Practices

- **Bullet points** - 结构清晰，易于记忆
- **Tables** - 对比类知识一目了然
- **Code blocks** - 指定语言以启用语法高亮
- 💡 强调关键点或记忆技巧
- ⚠️ 标注易错点或注意事项

## Example Card

文件: `cards/python/walrus.md`

```markdown
# Python 海象运算符 `:=` 用法

`(x := value)` 在表达式中赋值并返回值

```python
if (n := len(data)) > 10:
    print(f"Too long: {n}")
```

💡 Python 3.8+ 特性，避免重复计算
```

→ 牌组 `python`, 正面 "Python 海象运算符 `:=` 用法"

## Sync

**前置条件**: Anki 运行中 + AnkiConnect 插件 (code: `2055492159`)

```bash
# 1. 首次设置：创建 venv 并安装依赖
python -m venv venv
./venv/Scripts/pip.exe install requests

# 2. 同步卡片到 Anki
./venv/Scripts/python.exe .claude/skills/anki-card-generator/scripts/anki_sync.py

# 3. 预览变更（不执行）
./venv/Scripts/python.exe .claude/skills/anki-card-generator/scripts/anki_sync.py --dry-run
```

**同步行为**:
- 新文件 → 添加卡片
- 文件内容变更 → 更新卡片
- 文件删除 → 删除对应卡片（孤儿清理）
- 文件移动/重命名 → 视为删除旧卡 + 添加新卡（SourceID 变化）

## Project Validation

同步前检查项目结构是否规范：

**必须存在**:
- `cards/` - 卡片源文件目录
- `venv/` - Python 虚拟环境
- `.claude/skills/anki-card-generator/` - 本 skill

**Markdown 文件检查**:
- 每个 .md 文件应有 H1 标题（否则用文件名作为正面）
- H1 后必须有内容（不能为空卡片）
- 代码块正确闭合
