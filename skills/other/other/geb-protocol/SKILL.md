---
name: geb-protocol
description: |
  项目架构约定：通过 Root/Folder/File 三层极简元数据（_dir.md + I/O/Pos 注释）
  让 AI 在任意位置自定位。

  **AI 创建文件夹时自动触发**：hook 会生成 _dir.md 模板，AI 填写 Input/Output/Pos。
---

# GEB 路标协议

分形式项目导航。让 AI 在任意位置都能自定位。

## 核心结构

```
Root   → 项目是什么、模块有哪些（5行）
Folder → 这个文件夹负责什么（3-4行 _dir.md）
File   → Input/Output/Pos（3行头部注释）
```

**不是文档，是坐标系统。**

---

## 实施

### Root（CLAUDE.md）

```markdown
# 项目名

一句话描述。

模块：A(职责) → B(职责) → C(职责)
分层：cli → flows → core → data

深度文档：docs/architecture.md
```

### Folder（_dir.md）

```markdown
模块名称（一句话职责）
Input: 依赖什么
Output: 提供什么
Pos: 在分层中的位置
```

### File（头部注释 - Python）

```python
# Input: 依赖的类型/协议
# Output: 对外暴露的类/函数
# Pos: 层级定位（如 core/rules）

from decimal import Decimal
# ... 代码 ...
```

---

## 自愈机制

在工作流程中强制：

```
修改后检查：
- 更新文件头 I/O/Pos（依赖变了）
- 更新 _dir.md（模块职责变了）
- 更新 architecture.md（结构变了）
```

---

## 适用规模

| 项目规模 | 建议 |
|---------|------|
| < 10 文件 | 不需要 |
| 10-50 文件 | Root + 核心文件头部 |
| 50+ 文件 | 完整三层路标 |

---

## 详细示例

见 [references/examples.md](references/examples.md)
