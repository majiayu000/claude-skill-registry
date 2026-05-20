---
name: flutter-build
description: 编译测试 Flutter 应用。修改代码确认提交前执行，验证编译是否通过。
---

# Flutter Build

编译 Flutter 应用并过滤输出，只显示关键信息。自动检测当前操作系统选择编译目标平台。

## 用法

```bash
dart run <skill_path>/scripts/build.dart <app模块相对路径>
```

## 示例

```bash
dart run <skill_path>/scripts/build.dart apps/video_concat_app
```

## 行为

- 编译成功：输出 `编译成功`
- 编译失败：仅输出错误信息，过滤掉警告和依赖解析等噪音

## 关于 flutter build

`flutter build <platform> --debug` 执行 Debug 编译，包含：
1. 依赖解析（Resolving dependencies）
2. Dart 编译（kernel snapshot）
3. 平台原生构建

常见错误类型：
- Dart 语法/类型错误：`lib/file.dart:行:列: Error: 消息`
- 资源缺失或配置错误
