---
name: debugging
description: 当用户要求排查Bug、定位问题、异常排查或性能瓶颈时使用。
---

# Debugging Skill

## 适用范围
- Rust/Tauri 后端问题排查
- React 前端状态与渲染异常
- 数据库/迁移问题

## 关键规则（Critical Rules）
- 先复现，再定位
- 优先缩小范围与影响面
- 记录关键输入与边界条件

## 系统化流程
1. 复现问题（最小输入）
2. 收集上下文（日志、参数、数据状态）
3. 提出假设并验证
4. 修复后回归验证

## 常见检查点
- Tauri 命令未注册：检查 `#[tauri::command]` 与 `#[specta::specta]`
- 类型不匹配：检查 DTO `specta::Type` 与 camelCase
- 数据库错误：确认迁移已执行、表名/字段名正确
- React 过度渲染：检查依赖与 `useMemo`/`useCallback`

## 工具建议
- Rust：使用 `tracing` 记录关键路径
- DB：使用 `EXPLAIN QUERY PLAN` 分析索引
- 前端：用 UI 提示展示关键状态，避免 `console.*`

## 检查清单
- [ ] 已复现并最小化输入
- [ ] 已验证关键假设
- [ ] 修复后回归验证通过
