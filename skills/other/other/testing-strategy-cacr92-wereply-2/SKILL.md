---
name: testing-strategy
description: 当用户要求测试策略、单元/集成测试、TDD或测试覆盖率时使用。
---

# Testing Strategy Skill

## 适用范围
- Rust 单元/集成测试
- Tauri 命令与服务层测试
- 前端关键流程验证

## 关键规则（Critical Rules）
- 改动行为时优先补测试
- 异步测试使用 `#[tokio::test]`
- 只在存在脚本时执行前端测试命令

## Rust 测试模板
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn should_sum_materials() {
        let total = 10.0 + 20.0;
        assert_eq!(total, 30.0);
    }
}
```

## 常用命令
```bash
cargo test
cargo test --all
```

## 前端验证
- 无测试脚本时，执行 `npm run lint` 并进行关键流程手测
- 重要交互建议补充可重复的操作步骤

## TDD 流程
1. 编写失败测试
2. 实现最小代码通过测试
3. 重构并保持测试通过

## 检查清单
- [ ] 行为改动有对应测试或明确手测步骤
- [ ] 异步测试使用 `tokio::test`
- [ ] 运行 `cargo test` 通过
