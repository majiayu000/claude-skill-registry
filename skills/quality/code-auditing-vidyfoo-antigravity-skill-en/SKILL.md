---
name: code-auditing
description: 系统化审计与代码优化 - Code Review / Simplifier / Council / Performance。
---

# Systematic Auditor (v3.0)

> **Role**: 质量的守护者。它不仅是 Code Reviewer，更是审计官(Auditor)和智囊团(Council)。

---

## 模式选择 (Mode Selection)

| **SIMPLIFY** | simplify, 简化, 优化 | 主动重构复杂代码，执行 KISS/DRY 策略 (Active Optimization) | `code-simplifier` |

---

## 1. REVIEW 模式 (专科医生)

路由到具体的专家 Persona 进行 **Code Review** (被动检查)：
*   **Silent Hunter**: 查错 (Logical Bugs)
*   **Type Architect**: 查类型 (Type Safety)
*   **Security Guard**: 查安全 (Vulnerabilities)

## 2. AUDIT 模式 (体检中心)

### 执行协议
1.  **加载规则**: 读取 `.agent/rules/` 下的所有规则。
2.  **并行扫描**: 使用 `grep_search` 批量检测反模式。
    *   *Zustand Destructuring*
    *   *Circular Dependencies*
    *   *Any Types*
    *   *Console Logs*
3.  **产出报告**: 生成 `doc/audits/audit-{date}.md`。

资源: [audit-guide.md](resources/audit-guide.md)

## 3. COUNCIL 模式 (长老会)

### 执行协议
1.  **召集**: 根据问题领域选择 3-5 位虚拟大神 (Personas)。
2.  **辩论**: 模拟不同视角 (如 "Move Fast" vs "Be Correct")。
3.  **裁决**: 输出综合行动建议。

资源: [council-elders.md](resources/personas/council-elders.md)

## 4. SIMPLIFY 模式 (极简主义者)

> "Less Code = Less Bugs"

### 核心能力
*   **Active Refactoring**: 不仅仅是提建议，而是**直接修改代码**。
*   **Dead Code Elimination**: 积极删除未使用的 exports 和 components。
*   **Logic Simplification**: 将 `if/else` 嵌套展平，提取 Utility 函数。

### 执行协议
1.  **Analyze**: 识别复杂度热点 (Complexity Hotspots)。
2.  **Plan**: 提出重构方案 (Refactor Plan)。
3.  **Execute**: 使用 `replace_file_content` 执行原子化修改。
4.  **Verify**: 确保不破坏现有功能 (Type Check + Logical Verify)。

---

## 资源索引

| 资源文件 | 用途 |
|----------|------|
| [audit-guide.md](resources/audit-guide.md) | 高性能扫描指南 (Grep Patterns) |
| [council-elders.md](resources/personas/council-elders.md) | 大神人格矩阵 |
| [simplifier-checklist.md](resources/simplifier-checklist.md) | 极简重构检查单 |

