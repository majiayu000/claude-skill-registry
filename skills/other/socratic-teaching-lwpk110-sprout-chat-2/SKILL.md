---
name: socratic-teaching
description: 实现苏格拉底式引导教学，通过提问引导学生思考，支持7种引导类型和错误类型映射。
---

# 苏格拉底引导技能

## 引导类型定义

| 类型 | 标识 | 作用 | 示例 |
|------|------|------|------|
| 澄清型 | clarify | 澄清学生理解 | "你觉得这道题在问什么？" |
| 提示型 | hint | 给出提示不直接给答案 | "先看看题目里有哪些数字？" |
| 分解型 | break_down | 将问题分解为小步骤 | "第一步我们应该做什么？" |
| 可视化型 | visualize | 建议用可视化方式 | "能不能把这个问题画出来？" |
| 检查型 | check_work | 引导学生检查答案 | "我们一起来验算一下？" |
| 替代法型 | alternative_method | 建议用其他方法 | "还有没有其他方法？" |
| 鼓励型 | encourage | 给予鼓励和信心 | "你很接近了，再想一想！" |

---

## 错误类型分类

| 类型 | 标识 | 表现 |
|------|------|------|
| 计算错误 | calculation | 步骤对，结果错 |
| 概念错误 | concept | 步骤和结果都错 |
| 理解错误 | understanding | 读错题意 |
| 粗心错误 | careless | 偶发性错误 |

---

## 错误-引导映射

### 首次尝试
```python
FIRST_ATTEMPT_MAPPING = {
    "calculation": ["hint", "check_work"],
    "concept": ["clarify", "break_down"],
    "understanding": ["clarify"],
    "careless": ["check_work", "encourage"],
}
```

### 多次尝试后
```python
RETRY_MAPPING = {
    "calculation": ["break_down", "visualize"],
    "concept": ["visualize", "alternative_method"],
    "understanding": ["break_down", "hint"],
    "careless": ["encourage", "check_work"],
}
```

---

## 相关技能
- `sprout-persona` - 人格和语言规范
- `teaching-strategy` - 问题类型识别
- `tdd-cycle` - TDD 开发流程
