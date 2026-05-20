---
name: code-review
description: 当用户要求代码审查、Review、找风险或列问题时使用。
---

# Code Review Skill

## 适用范围
- Rust/Tauri 后端审查
- React 前端审查
- 数据库与性能风险检查

## 关键规则（Critical Rules）
- 优先发现逻辑错误与回归风险
- 检查命令签名与类型导出是否完整
- 检查前端是否违反 `console.*` / `as any`
- UI 表格：检查表格行高/内边距是否符合紧凑规范（默认 th/td padding 6px 10px、line-height 1.2；表格内 Tag 紧凑化）

## 审查要点
- Tauri：`#[tauri::command]` + `#[specta::specta]` 是否齐全
- 类型：入参/出参 `specta::Type` 与 camelCase 一致
- 数据库：`sqlx::query_as!`、显式列名、事务正确
- 前端：仅用 `commands`，错误 `message.*` 提示
- 性能：重复计算、N+1、无谓 clone

## 快速命令
```bash
cargo clippy --all-targets --all-features -- -D warnings
cargo fmt --all
cd frontend && npm run lint
```

## 反馈结构
- 先列出问题（严重性排序）
- 给出可操作修复建议
- 标注文件路径与关键位置

## 检查清单
- [ ] 关键路径无回归风险
- [ ] Tauri 命令与类型导出完整
- [ ] 前端无 `console.*` / `as any`
- [ ] Lint/Clippy 无警告
- [ ] 表格行高与内边距保持紧凑统一