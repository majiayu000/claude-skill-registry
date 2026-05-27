---
name: chinese-interface-doc-generator
description: Generates concise Chinese documentation for code interfaces (functions, classes, APIs) with Chinese comment extraction, optimized for Chinese development teams
---

# 接口文档生成助手

此技能为中文开发者自动分析代码中的接口定义（函数、类、模块、API端点等），提取中文注释和文档字符串，生成简洁清晰的中文接口文档。专注于内部文档、快速原型和团队协作场景，支持交互式选项选择。

区别于OpenAPI生成器：通用接口支持（非仅API）、中文优先、简单交互、无复杂规范验证。

## 能力

- **接口分析**：识别Python/JS代码中的函数、类方法、API端点等接口定义
- **中文文档提取**：优先提取中文注释、docstring，支持简繁体中文
- **多格式输出**：Markdown、HTML、JSON，支持REST/GraphQL/函数接口
- **交互选项**：选择详细程度（简要/详细）、格式、包含示例
- **报告生成**：一键生成完整中文接口报告，保存为时间戳文件
- **团队友好**：简洁输出，便于中文团队审阅和协作

## 输入要求

- **代码内容**：代码字符串、文件路径或目录（支持.py, .js, .ts）
- **语言类型**：python（默认）、javascript、typescript
- **可选参数**：
  - `detail_level`: 简要/详细 (default: 详细)
  - `output_format`: markdown/html/json (default: markdown)
  - `include_examples`: true/false (default: true)

示例输入：
```json
{
  "code": "def 用户登录(user: str, pwd: str) -> bool:\n    '''用户登录接口\n    参数:\n    - user: 用户名\n    - pwd: 密码\n    返回: 登录成功True'''\n    pass",
  "lang": "python",
  "detail_level": "详细"
}
```

## 输出格式

- **主要输出**：中文Markdown报告，格式：`接口文档_YYYY-MM-DD_HH-MM-SS.md`
- **保存位置**：`.claude/interface_docs/`
- **内容包括**：
  - 接口列表与签名
  - 中文描述/参数/返回值
  - 示例调用（若有）
  - 错误码/异常处理
  - 生成元数据

## 如何使用

“使用chinese-interface-doc-generator技能分析这个Python文件中的接口并生成中文文档”

“为这个函数生成简要中文接口文档，包括参数说明”

“提取这个JS模块的所有方法文档，用HTML格式输出”

## 脚本

- `interface_analyzer.py`: 接口定义分析器，使用AST解析Python代码
- `chinese_doc_extractor.py`: 中文注释和docstring提取器，支持正则匹配中文
- `doc_formatter.py`: 文档格式化，支持Markdown/HTML/JSON
- `report_generator.py`: 完整报告生成器，整合分析结果并写入文件

## 最佳实践

1. **代码规范**：使用中文docstring，便于自动提取
2. **结构清晰**：接口定义使用标准语法，避免嵌套过深
3. **提供示例**：代码中包含调用示例，提高文档质量
4. **分模块分析**：大型项目分目录处理，避免单次过载
5. **审阅输出**：自动生成后手动补充业务上下文

## 限制

- 主要支持Python/JS/TS，复杂语言需手动调整
- 依赖代码注释质量，无注释时仅提取签名
- 非动态语言的二进制接口不支持
- 大型代码库建议分批处理