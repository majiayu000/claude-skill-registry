---
name: ast-grep
description: 语法感知的代码搜索、linting 和重写工具。支持基于 AST 的结构化代码搜索和批量代码转换。
---

# AST-Grep

AST-Grep (ast-grep/sg) 是一个快速且用户友好的工具，用于代码搜索、linting 和大规模代码重写。

## 执行环境

| 路径类型 | 说明 |
|---------|------|
| **使用方式** | 命令行工具，需要安装 ast-grep |
| **调用场景** | 语法感知的代码搜索、结构化代码分析、批量代码转换 |
| **工作目录** | 项目根目录 |

## 安装

```bash
# macOS
brew install ast-grep

# Linux
cargo install ast-grep

# 验证安装
ast-grep --version
```

## 核心功能

### 1. 语法感知搜索

使用 AST（抽象语法树）进行代码搜索，而非简单的文本匹配。

```bash
# 搜索特定模式
ast-grep --lang python -p "def $FUNC($$$ARGS):"

# 搜索函数调用
ast-grep --lang ts -p "console.log($$$MSG)"

# 搜索条件语句
ast-grep --lang ts -p "if ($$COND) { $$$BODY }"
```

### 2. 代码 Linting

基于 AST 的代码检查，比传统 linter 更精确。

```bash
# 扫描项目
ast-grep scan -r sgconfig.yml

# 扫描特定目录
ast-grep scan src/

# 扫描特定文件
ast-grep scan src/main.ts
```

### 3. 代码重写

批量转换代码模式。

```bash
# 简单替换
ast-grep run -p "oldFunction($$$ARGS)" -r "newFunction($$ARGS)" --lang ts

# 复杂转换（使用 YAML 规则）
ast-grep run -r rule.yml
```

### 4. 规则测试

测试 ast-grep 规则是否正确。

```bash
# 测试规则
ast-grep test -r rule.yml

# 测试特定模式
ast-grep test -p "pattern" --lang ts
```

## 规则开发流程

### 通用流程

1. **理解查询**：明确用户需求，必要时询问更多细节
2. **编写示例**：编写匹配查询的简单代码示例
3. **编写规则**：编写匹配示例的 ast-grep 规则
4. **测试规则**：使用 `test_match_code_rule` 验证规则
   - 如果不匹配，移除部分子规则并调试
   - 如果使用 `inside` 或 `has`，确保使用 `stopBy: end`
5. **搜索代码**：使用规则搜索代码库

### 规则开发步骤

1. **分解查询**：将用户查询分解为更小的部分
2. **识别子规则**：识别可用于匹配代码的子规则
3. **组合规则**：使用关系规则或组合规则组合子规则
4. **调试规则**：如果规则不匹配示例代码，移除部分子规则并调试不匹配的部分
5. **使用工具**：使用 ast-grep mcp 工具转储 AST 或转储模式查询
6. **测试规则**：使用 ast-grep mcp 工具针对示例代码片段测试规则

## 规则类型

### 1. 原子规则

匹配单个 AST 节点，基于内在属性。

#### `pattern` - 模式匹配

```yaml
# 字符串模式
pattern: console.log($ARG)

# 对象模式（更精细的控制）
pattern:
  selector: field_definition
  context: class { $F }
  strictness: relaxed
```

#### `kind` - 节点类型匹配

```yaml
kind: call_expression
```

#### `regex` - 正则表达式匹配

```yaml
regex: ^[a-z]+$
```

#### `nthChild` - 位置匹配

```yaml
# 数字
nthChild: 1

# An+B 公式
nthChild: 2n+1

# 对象形式
nthChild:
  position: 1
  reverse: true
  ofRule:
    kind: function_declaration
```

#### `range` - 范围匹配

```yaml
range:
  start:
    line: 0
    column: 0
  end:
    line: 0
    column: 10
```

### 2. 关系规则

基于目标节点与其他节点的关系过滤目标。

#### `inside` - 在父节点内

```yaml
inside:
  pattern: class $C { $$$ }
  stopBy: end
```

#### `has` - 包含子节点

```yaml
has:
  pattern: await $EXPR
  stopBy: end
```

#### `precedes` - 在节点之前

```yaml
precedes:
  pattern: return $VAL
```

#### `follows` - 在节点之后

```yaml
follows:
  pattern: import $M from '$P'
```

#### `stopBy` - 搜索终止控制

```yaml
# neighbor（默认）：在直接周围节点不匹配时停止
stopBy: neighbor

# end：搜索到方向末尾（inside 为根，has 为叶子）
stopBy: end

# 规则对象：在周围节点匹配提供的规则时停止（包含）
stopBy:
  pattern: class $END
```

#### `field` - 字段匹配

```yaml
has:
  field: operator
  pattern: $$OP
```

### 3. 组合规则

使用逻辑操作组合其他规则。

#### `all` - 逻辑与（AND）

```yaml
all:
  - kind: call_expression
  - pattern: console.log($ARG)
```

#### `any` - 逻辑或（OR）

```yaml
any:
  - pattern: console.log($ARG)
  - pattern: console.warn($ARG)
  - pattern: console.error($ARG)
```

#### `not` - 逻辑非（NOT）

```yaml
not:
  pattern: console.log($ARG)
```

#### `matches` - 规则重用

```yaml
matches: my-utility-rule-id
```

## 元变量

### `$VAR` - 单个命名节点捕获

```yaml
# 有效
pattern: console.log($GREETING)

# 匹配
console.log('Hello World')
```

### `$$VAR` - 单个未命名节点捕获

```yaml
# 匹配操作符
rule:
  kind: binary_expression
  has:
    field: operator
    pattern: $$OP
```

### `$$$VAR` - 多节点捕获

```yaml
# 匹配零个或多个节点（非贪婪）
pattern: console.log($$$)

# 匹配可变参数
pattern: function $FUNC($$$ARGS) { $$$ }
```

### `_VAR` - 非捕获元变量

```yaml
# 不捕获，可以匹配不同内容
pattern: $_FUNC($_FUNC)

# 匹配
test(a)
testFunc(1 + 1)
```

## 编写规则的最佳实践

1. **始终使用 `stopBy: end`**：对于关系规则，确保搜索到方向末尾

```yaml
has:
  pattern: await $EXPR
  stopBy: end
```

2. **简单结构使用 pattern**：代码结构简单时直接使用模式

```yaml
pattern: console.log($ARG)
```

3. **复杂结构使用 rule**：代码结构复杂时使用规则分解

```yaml
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
```

4. **使用 kind 调试**：如果 pattern 不工作，先用 kind 匹配节点类型

```yaml
# 先确认节点类型
kind: call_expression

# 再使用 has 或 inside
has:
  pattern: console.log($ARG)
```

5. **关系规则无匹配时添加 stopBy**：确保搜索到末尾

```yaml
inside:
  pattern: class $C { $$$ }
  stopBy: end
```

## YAML 规则配置

### 简单规则

```yaml
# rule.yml
id: no-console-log
language: ts
rule:
  pattern: console.log($$$MSG)
```

### 复杂规则

```yaml
# complex-rule.yml
id: prefer-const
language: ts
rule:
  all:
    - pattern: let $VAR = $INIT
    - not:
        pattern: $VAR = $EXPR
```

### 带修复的规则

```yaml
# fix-rule.yml
id: no-var
language: ts
rule:
  pattern: var $VAR = $INIT
fix: const $VAR = $INIT
```

### 使用关系规则

```yaml
# async-without-await.yml
id: async-without-await
language: ts
rule:
  all:
    - pattern: async function $FUNC($$$ARGS) { $$$BODY }
    - not:
        has:
          pattern: await
          stopBy: end
```

## 常用场景

### 1. 查找特定代码模式

```bash
# 查找所有 console.log
ast-grep -p "console.log($$$MSG)" --lang ts

# 查找所有未使用的变量
ast-grep -p "let $VAR = $INIT" --lang ts | grep -v "$VAR ="
```

### 2. 重构代码

```bash
# 替换 var 为 const
ast-grep run -p "var $VAR = $INIT" -r "const $VAR = $INIT" --lang ts

# 重命名函数
ast-grep run -p "oldFunc($$$ARGS)" -r "newFunc($$ARGS)" --lang ts
```

### 3. 代码审计

```bash
# 查找潜在的安全问题
ast-grep -p "eval($$$EXPR)" --lang js

# 查找 SQL 注入风险
ast-grep -p "query('$$SQL')" --lang py
```

### 4. API 迁移

```bash
# 迁移旧 API 到新 API
ast-grep run -p "oldApi($$$ARGS)" -r "newApi($$ARGS)" --lang ts

# 批量更新导入
ast-grep run -p "from 'old-lib' import $$IMPORT" -r "from 'new-lib' import $$IMPORT" --lang ts
```

## 与其他工具对比

| 特性 | ast-grep | grep | ripgrep |
|------|----------|------|---------|
| 语法感知 | 是 | 否 | 否 |
| 代码结构理解 | 是 | 否 | 否 |
| 跨语言支持 | 是 | 否 | 否 |
| 性能 | 快 | 快 | 最快 |
| 重写功能 | 是 | 否 | 否 |

## 参考资源

- 官方文档: https://ast-grep.github.io/
- GitHub: https://github.com/ast-grep/ast-grep
- 规则示例: https://ast-grep.github.io/catalog/
- Playground: https://ast-grep.github.io/playground/
- MCP 服务器: https://github.com/ast-grep/ast-grep-mcp

## 集成 Pi 工作流

### Phase 1: 上下文检索

当需要理解代码结构时，使用 ast-grep 进行语法感知搜索：

```bash
# 查找特定模式
ast-grep -p "pattern" --lang <language>
```

### Phase 4: 编码实施

使用 ast-grep 进行批量代码转换：

```bash
# 应用重构规则
ast-grep run -r rule.yml
```

### Phase 5: 审计

使用 ast-grep 验证代码质量：

```bash
# 扫描潜在问题
ast-grep scan -r sgconfig.yml
```

## 注意事项

- ast-grep 需要安装才能使用
- 模式语法需要熟悉 AST 结构
- 复杂规则建议先测试再应用
- 大规模重构前建议备份代码
- 使用 `stopBy: end` 确保关系规则搜索完整
- 元变量必须符合语法要求（$VAR, $$VAR, $$$VAR）