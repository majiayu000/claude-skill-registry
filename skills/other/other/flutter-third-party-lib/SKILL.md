---
name: flutter-third-party-lib
description: "**Must use before adding any new Flutter/Dart dependency.** Use when adding a new package to pubspec.yaml, using an unfamiliar library, or when code uses a third-party API incorrectly. Triggers on 'add dependency', 'new package', 'pub.dev', 'third-party lib', or any pubspec.yaml dependency addition."
---

# Flutter Third-Party Library Usage Flow

添加任何新的 Flutter/Dart 第三方依赖前，必须先从 pub.dev 学习并编写用法文档，再根据文档编写代码。

## 强制流程

```
发现需要新依赖
    ↓
1. 从 pub.dev 查阅官方文档
    ↓
2. 编写用法文档到 md/设计/flutter/第三方库/{库名}.md
    ↓
3. 根据文档编写/修改代码
```

**禁止跳过任何步骤。禁止凭记忆或猜测使用 API。**

## 步骤 1：从 pub.dev 学习

使用 `web_fetch` 工具访问 `https://pub.dev/packages/{包名}` 获取：

| 必须确认 | 说明 |
|----------|------|
| API 签名 | 构造函数参数、方法签名、返回类型 |
| 平台支持 | 各平台是否支持、是否有差异行为 |
| 必要配置 | 权限、entitlements、AndroidManifest 等 |
| 版本约束 | 当前稳定版本 |

**不要假设 API 用法。** 例如 `Logger()` 构造函数是否需要参数、`FilePicker.saveFile` 在不同平台行为是否一致，都必须从官方文档确认。

## 步骤 2：编写文档

输出到 `md/设计/flutter/第三方库/{库名}.md`，遵循 docs-style skill 规范。

### 文档结构模板

```markdown
# {库名}

一句话说明本项目用途。

## 核心用途

| 用途 | 说明 |
|------|------|

## 平台支持（如有差异）

| 功能 | Android | iOS | Web | macOS | Windows | Linux |
|------|---------|-----|-----|-------|---------|-------|

## 必要配置（如有）

平台权限、entitlements 等。

## API 用法

核心 API 的代码示例，只包含本项目实际使用的部分。

## 本项目使用场景

| 场景 | 使用方式 |
|------|----------|
```

### 文档约束

| 应写 | 不应写 |
|------|--------|
| 本项目实际使用的 API | 库的全部 API |
| 平台行为差异 | 安装命令 |
| 代码模式和用法示例 | 版本号 |
| 关键约束和注意事项 | 冗余说明 |

## 步骤 3：根据文档编码

- 代码中的 API 调用必须与文档一致
- 发现文档与实际行为不符时，更新文档而非忽略差异
- 遇到文档未覆盖的用法时，先补充文档再写代码

## 红线

- ❌ 凭记忆猜测 API 用法
- ❌ 跳过文档直接写代码
- ❌ 从其他项目（如 `ln/`）复制用法
- ❌ 写完代码后才补文档
