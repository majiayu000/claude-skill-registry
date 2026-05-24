---
name: user-customization
description: 指导用户如何自定义 Trae Skills 的配置，包括覆盖角色设定、调整技术偏好和定义全局规则。
---

# User Customization & Preferences

本 Skill 旨在帮助用户根据个人或团队的需求，定制 Trae 的行为模式。通过创建 `USER_PREFERENCES.md`，你可以让所有的 Skill 和 Agent 都遵循你的特定偏好。

## ⚙️ 配置文件机制

Trae 会优先寻找并遵循以下位置的配置文件：
*   `.trae/USER_PREFERENCES.md` (推荐)

### 配置文件模板

你可以直接复制以下内容到 `.trae/USER_PREFERENCES.md`：

```markdown
# User Preferences

## 1. 技术栈偏好 (Tech Stack)
*   **CSS Framework**: Tailwind CSS (严禁使用 CSS Modules 或 Styled Components)
*   **State Management**: Zustand (React), Riverpod (Flutter)
*   **Testing**: Vitest (不使用 Jest)
*   **Language**: TypeScript (Strict Mode enabled)

## 2. 交互风格 (Communication Style)
*   **Language**: 请始终使用**中文**回复，但技术术语保留英文。
*   **Detail Level**: 我是资深开发者，请直接给代码，少讲废话。
*   **Emoji**: 禁用 Emoji，保持职业化。

## 3. 角色覆盖 (Role Overrides)
*   **@Office Architect**:
    *   在处理 Excel 时，优先使用 pandas 而不是 openpyxl。
*   **@DevOps Engineer**:
    *   生成的 K8s Manifest 必须包含 Resource Limits。

## 4. 禁令 (Constraints)
*   严禁使用 `any` 类型。
*   严禁创建 `.env` 文件（使用 config map）。
```

## 🔄 它是如何工作的？

1.  **全局生效**: `universal-dev-team` 在调度角色时，会先读取此文件。
2.  **角色感知**: 只要你在 Trae 中定义 Agent 时，在 System Prompt 的开头加上一句：
    > "Always check .trae/USER_PREFERENCES.md before answering."
    那么所有的手动配置 Agent 都会遵循这些规则。

## 🛠️ 高级用法：自定义 Skill

如果你需要更深度的定制（例如完全重写 React 规范），建议：
1.  **Fork**: 复制 `03_Developer_ReactBestPractices` 目录到 `Custom_React_Skills`。
2.  **Modify**: 修改其中的 `SKILL.md` 和 `rules/`。
3.  **Register**: 更新 `universal-dev-team/SKILL.md` 中的路由表，指向你的新目录。

---
