---
name: goframe-v2
description: GoFrame开发框架专属技能集。为Go语言开发者提供完整的框架使用指南，涵盖命令行管理、配置管理、日志组件、错误处理、数据校验、类型转换、缓存管理、模板引擎、数据库ORM、I18n国际化等核心组件的最佳实践。包含项目工程化结构规范、开发模式指引、常见问题解决方案以及丰富的实战代码示例。适用于构建RESTful API、gRPC微服务、Web应用等各类Go项目，帮助开发者快速掌握GoFrame框架特性，提升开发效率和代码质量。
license: Apache-2.0
---
# 重要规范
## 工程开发规范
- 开发完整工程类型的项目如HTTP、微服务项目时，需要先安装GoFrame CLI开发工具，并使用CLI工具创建项目骨架，对应命令为gf init，命令的具体使用方式需参考文档[项目创建-init](./references/开发工具/项目创建-init.md)。
- 在GoFrame工程规范中，由开发工具自动维护的代码文件，如dao、do、entity等源码文件，不允许手动创建或修改。
- 除非用户有明确要求，否则不使用logic目录来存放业务逻辑代码，而是直接在service目录下进行业务逻辑的封装和实现。
- 完整工程目录、代码封装以及源码实现的示例需参考已有示例项目，如：
  - HTTP项目最佳实践示例：[user-http-service](./examples/practices/user-http-service)
  - gRPC项目最佳实践示例：[user-grpc-service](./examples/practices/user-grpc-service)

## 组件使用规范
- 创建新的方法或变量前要先分析是否在其它位置中已经存在，尽量引用已有的实现。
- 错误处理统一使用gerror组件，确保错误信息带有完整堆栈信息以提供可追踪性。
- 在调研使用新组件时，优先考虑引用GoFrame框架中已有组件、优先参考示例代码中的最佳实践源码。

# Go开发资料
完整的GoFrame开发资料，包含各类组件的设计介绍、使用说明、最佳实践、注意事项：[Go开发资料](./references/README.MD)

# Go示例代码
丰富的GoFrame实战代码示例，涵盖HTTP服务、gRPC服务等多种项目类型：[Go示例代码](./examples/README.MD)