---
name: flutter-style
description: Flutter/Dart coding style guide. **Must use before writing Flutter/Dart code.** Use when creating new files, refactoring code, or reviewing Flutter/Dart code quality.
---

# Flutter/Dart 编码规范

编写 Flutter/Dart 代码前必须遵循以下规范。

## 文件组织

### 一类一文件（强制）
- **每个公开类必须独立一个文件**，严禁多个类堆在同一文件中
- 文件名使用 snake_case，与类名对应
  - `DanmakuMessage` → `danmaku_message.dart`
  - `WebSocketClient` → `websocket_client.dart`
- 例外：枚举可与相关类合并；私有辅助类可与外部类合并（但超过 30 行应拆出）
- 使用 barrel 文件（如 `models.dart`）统一导出

### 文件大小限制
- **单文件不超过 300 行**（硬限制）
- 超过 200 行时主动考虑拆分
- 算法/逻辑类拆分为：配置、数据结构、核心逻辑各一个文件
- Widget 拆分为：页面、子组件、状态管理各一个文件

### 目录结构
```
lib/
  src/
    models/       # 数据模型
    services/     # 服务类
    utils/        # 工具类
    widgets/      # UI 组件
```

### 拆分原则
- 优先按职责拆分，而非按大小拆分
- 配置类（Config）单独文件
- 数据类（Model/DTO）单独文件
- 辅助工具函数可按功能分组到 `_helpers.dart` / `_utils.dart`

## 导入顺序

1. Dart SDK 库
2. Flutter 框架库
3. 第三方包
4. 项目内部文件

## 类成员顺序

1. 静态常量
2. 静态变量
3. 实例变量
4. 构造函数
5. 静态方法
6. 实例方法
7. 私有方法

## 命名规范

| 类型 | 风格 | 示例 |
|------|------|------|
| 类名 | PascalCase | `WebSocketClient` |
| 文件名 | snake_case | `web_socket_client.dart` |
| 变量/方法 | camelCase | `sendMessage()` |
| 常量 | camelCase + const/final | `const maxRetries = 3` |
| 私有成员 | 前缀 `_` | `_connectionState` |

## 注释规范

- 公开 API 必须有文档注释（`///`）
- 复杂逻辑必须有行内注释（`//`）
- 标记：`TODO:`、`FIXME:`、`NOTE:`
