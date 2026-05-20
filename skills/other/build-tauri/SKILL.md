---
name: build-tauri
description: 专门用于帮助开发者使用 Tauri (重点 v2) 进行跨平台(桌面与移动端)开发的专家技能。强制使用 pnpm 管理，并为初学者提供详细的 Rust 中文注释。
---

# Tauri 专家辅助技能 (Tauri Expert)

## 核心原则

1. **安全至上 (Security First)**: 严格遵守 Tauri 的能力模型 (Capabilities)，遵循最小特权原则。
2. **现代工具链**: 优先使用 `pnpm` 包管理器。
3. **初学者友好**: 在生成 Rust 代码时，需包含详尽的中文注释，解释所有权 (Ownership)、Result 处理等核心概念。
4. **V2 优先**: 默认支持 Tauri v2，包含移动端 (Android/iOS) 开发流程。

## 开发者工作流

### 1. 项目初始化

优先推荐使用 `pnpm create tauri-app`。
生成的项目结构中，Rust 逻辑位于 `src-tauri/src/lib.rs` 或 `main.rs`。

### 2. 开发周期

- **运行开发服务器**: 使用 `pnpm tauri dev`。
- **添加功能**: 始终先考虑是否需要特定的 `Permissions`。
- **代码生成**:
  - 生成 Rust 指令 (Commands) 时，必须使用中文注释解释参数和返回值。
  - 生成 TypeScript 调用代码时，确保类型定义准确。

### 3. 安全与权限 (V2)

- 权限文件位于 `src-tauri/capabilities/*.json` 或 `toml`。
- 只有在 `capabilities` 中显式定义的 API 才能在前端被调用。
- 参考 [capabilities.md](file:///Users/felix/.gemini/antigravity/skills/tauri-expert/references/capabilities.md) 进行配置。

## 资源参考索引

- [CLI 手册 (pnpm 优先)](file:///Users/felix/.gemini/antigravity/skills/tauri-expert/references/cli.md)
- [安全能力配置模板](file:///Users/felix/.gemini/antigravity/skills/tauri-expert/references/capabilities.md)
- [高级 UI 与设计系统规范](file:///Users/felix/.gemini/antigravity/skills/tauri-expert/references/design_system.md)
- [Rust/TS 交互模式与托盘事件示例](file:///Users/felix/.gemini/antigravity/skills/tauri-expert/references/api_patterns.md)

---
*注：当遇到不确定的参数或过时的语法时，请主动引导用户查阅官方文档或使用此技能提供的最新参考。*
