---
name: debug
description: "Systematic debugging methods, log analysis, and performance diagnostics. Use when debugging issues, analyzing errors, or troubleshooting incidents."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
parent: quality
---

# 调试技能

本技能提供系统化的调试方法和技巧。

## 触发条件

- 调试代码问题
- 分析错误日志
- 调查性能问题
- 排查生产事故
- 修复 Bug

## 调试原则

### 黄金法则

1. **复现问题** - 先能稳定复现，再开始调试
2. **最小化** - 找到最小可复现用例
3. **二分法** - 缩小问题范围
4. **假设验证** - 提出假设，验证假设
5. **记录过程** - 记录尝试过的方法

### 调试流程

```
问题描述 → 复现问题 → 缩小范围 → 定位原因 → 修复验证 → 记录总结
```

## 问题描述模板

记录时包含以下要素:

| 要素         | 内容                     |
| ------------ | ------------------------ |
| 问题描述     | 简要描述问题现象         |
| 预期 vs 实际 | 期望行为与实际行为的差异 |
| 复现步骤     | 可稳定复现的最小步骤     |
| 环境信息     | OS、语言版本、依赖版本   |
| 错误信息     | 完整的错误堆栈或日志     |
| 已尝试方案   | 每个方案及其结果         |

## 日志调试

### 有效的日志输出

```typescript
// ❌ 无用的日志
console.log("here");
console.log(data);

// ✅ 有信息量的日志
console.log("[UserService.createUser] 开始创建用户:", {
  email: user.email,
  timestamp: new Date().toISOString(),
});

console.log("[UserService.createUser] 数据库插入成功:", {
  userId: result.id,
  duration: Date.now() - startTime,
});

console.error("[UserService.createUser] 创建失败:", {
  error: error.message,
  stack: error.stack,
  input: { email: user.email },
});
```

```python
# ❌ 无用的日志
print("here")
print(data)

# ✅ 有信息量的日志
import logging
logger = logging.getLogger(__name__)

logger.info(f"[create_user] 开始创建用户: email={email}")
logger.info(f"[create_user] 创建成功: user_id={user.id}, duration={duration}ms")
logger.error(f"[create_user] 创建失败: error={str(e)}", exc_info=True)
```

### 日志级别使用

| 级别  | 用途           | 示例               |
| ----- | -------------- | ------------------ |
| DEBUG | 详细调试信息   | 函数参数、中间状态 |
| INFO  | 正常操作信息   | 用户登录、订单创建 |
| WARN  | 警告但可继续   | 配置缺失使用默认值 |
| ERROR | 错误但可恢复   | API 调用失败重试   |
| FATAL | 致命错误需退出 | 数据库连接失败     |

## 断点调试

### VS Code 调试配置 (`.vscode/launch.json`)

| 场景      | type     | 关键配置                                   |
| --------- | -------- | ------------------------------------------ |
| Node.js   | `node`   | `program`, `preLaunchTask`, `outFiles`     |
| Python    | `python` | `program: "${file}"`, `integratedTerminal` |
| Jest 测试 | `node`   | `program: jest`, `args: ["--runInBand"]`   |

### 条件断点

在循环中设置条件表达式 (如 `item.id === 'target-id'`)，仅在满足条件时暂停。

## 网络与数据库调试

> 详见 [network-debug.md](network-debug.md)

- **网络调试**: Axios 拦截器日志、cURL 调试技巧
- **数据库调试**: Prisma/SQLAlchemy 查询日志、慢查询分析 (EXPLAIN ANALYZE)

## 性能调试

> 详见 [performance-debug.md](performance-debug.md)

- **时间测量**: `performance.now()` / `console.time` / Python `timeit` 装饰器
- **内存分析**: Node.js `process.memoryUsage()` / Python `tracemalloc`

## 前端调试与常见问题

> 详见 [frontend-debug.md](frontend-debug.md)

- **Console 高级方法**: `group` / `table` / `assert` / `trace` / `count`
- **React DevTools**: `displayName` / `useDebugValue`
- **常见 JS 陷阱**: 忘记 await、闭包捕获、this 丢失

## 调试清单

```markdown
## 调试前

- [ ] 能稳定复现问题吗？
- [ ] 最小复现用例是什么？
- [ ] 最近改动了什么？

## 调试中

- [ ] 查看错误日志和堆栈
- [ ] 添加必要的日志输出
- [ ] 使用断点逐步执行
- [ ] 检查输入数据是否正确
- [ ] 检查环境变量和配置

## 调试后

- [ ] 修复是否解决了根本原因？
- [ ] 是否需要添加测试？
- [ ] 是否需要更新文档？
- [ ] 是否有类似问题需要检查？
```

## 最佳实践

1. **先复现后调试** - 不能复现就无法确认修复
2. **二分法定位** - 缩小问题范围
3. **记录尝试** - 避免重复无效尝试
4. **查看最近改动** - git diff, git log
5. **橡皮鸭调试** - 向他人解释问题
6. **休息一下** - 换个思路
7. **搜索错误信息** - 可能他人遇到过
8. **检查假设** - 你认为正确的可能是错的
9. **简化问题** - 去除无关因素
10. **写测试固化** - 防止问题复现

> **记住**: 调试的第一步是复现——稳定复现问题后，解决方案通常就在眼前。
