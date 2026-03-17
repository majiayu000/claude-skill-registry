---
name: go-import-enforcer
description: Go 包导入规范检查与修复工具。基于 Claude 智能分析的 Go 项目导入规范检查工具，全面扫描和分析项目代码，识别真正的规范问题，提供准确的分析报告和修复建议。
---

# Go 包导入规范检查器

## 概述

基于 Claude 智能分析的 Go 项目导入规范检查工具，通过大模型全面扫描和分析项目代码，识别真正的规范问题，提供准确的分析报告和修复建议。

**核心特点**：
- 🤖 **Claude 驱动**：以大模型为主要分析引擎，提供智能、准确的分析
- 🎯 **精准识别**：区分手写代码和生成代码，避免误报
- 📊 **全面分析**：不仅检查格式，还分析循环依赖和架构设计
- 💡 **智能建议**：每个问题都提供具体的修复方案和最佳实践

**工作原理**：
1. **Claude 扫描**：Claude 扫描项目，分析导入规范问题
2. **Claude 分析**：生成详细分析报告
3. **Claude 调整**：自动调整不规范内容
4. **输出结果**：用户获得规范化后的代码和完整分析报告

**核心定位**：100% Claude（智能分析、报告生成、内容调整）

## 使用场景

- **新项目规范检查** - 检查新项目导入是否符合规范
- **代码审查辅助** - 快速发现导入问题并提供修复建议
- **批量导入规范** - 统一项目导入格式和别名使用
- **重构验证** - 重构后验证导入是否需要调整

## 快速开始

### 智能分析（推荐）

```bash
# 直接将整个项目交给 Claude 进行全面分析
# Claude 会自动：
# 1. 扫描所有 Go 文件
# 2. 分析导入规范问题
# 3. 检测循环依赖
# 4. 提供修复建议和最佳实践
# 5. 自动调整不规范内容
```

**重要提示**：本技能完全由 Claude 主导，无需任何脚本辅助。

## 工作流程

### Claude 全面分析（100% 智能化）

**目标**：全面分析项目导入规范情况

**时间**：3-5 分钟（取决于代码量）

**Claude 分析流程**：
```
开始
  ↓
1. Claude 智能扫描
   ├─ 扫描所有 Go 文件（手写代码 + 生成代码）
   ├─ 分析导入格式规范
   ├─ 验证四段分组规则
   ├─ 检查别名使用规范
   ├─ 检测循环依赖
   ├─ 评估代码质量
   ├─ 识别误报和实际问题
   ├─ 提供修复建议和最佳实践
   └─ 生成详细分析报告
  ↓
2. Claude 自动调整
   ├─ 格式化导入语句
   ├─ 调整分组和排序
   ├─ 应用正确别名
   └─ 解决循环依赖（如果需要）
  ↓
完成（输出规范化代码 + 完整报告）
```

**核心能力**：
- ✅ **区分手写代码和生成代码**：自动识别 `*.pb.go`, `wire_gen.go` 等
- ✅ **识别真正的规范问题**：避免误报，提供准确分析
- ✅ **智能分组判断**：理解导入规范的实际要求
- ✅ **循环依赖分析**：构建依赖图，评估影响和修复方案
- ✅ **提供具体修复建议**：每个问题都有针对性的解决方案
- ✅ **自动调整不规范内容**：直接修复发现的规范问题

## 核心导入规范

### 1. 导入格式强制要求

**三项强制规则**：
1. **括号包裹**：所有 `import` 语句必须使用 `()` 包裹
2. **段落分组**：按段落分组，段与段之间使用空行分隔
3. **字母排序**：每个段内的包按字母顺序排序

**错误示例**：
```go
// ❌ 错误：未使用括号包裹
import "context"
import "fmt"

// ❌ 错误：未分段，未排序
import (
    "github.com/go-kratos/kratos/v2/errors"
    "context"
    kitlog "github.com/fsyyft-go/kit/log"
    "fmt"
)

// ❌ 错误：fsyyft-go 包未取别名
import (
    "github.com/fsyyft-go/kit/log"
)
```

**正确示例**：
```go
// ✅ 正确格式
import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/v2/errors"
	kratoshttp "github.com/go-kratos/kratos/v2/transport/http"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	kitlog "github.com/fsyyft-go/kit/log"
	kitruntime "github.com/fsyyft-go/kit/runtime"

	apphelloworldv1 "github.com/fsyyft-go/kratos-layout/api/helloworld/v1"
	appconf "github.com/fsyyft-go/kratos-layout/internal/pkg/conf"
)
```

### 2. 四段分组规则

| 段落 | 内容 | 别名要求 | 示例 |
|------|------|---------|------|
| **第一段** | Go 标准库 | 无需别名 | `context`, `fmt`, `strings`, `time` |
| **第二段** | 第三方包（github.com 等） | 建议取别名 | `kratoshttp "github.com/go-kratos/..."` |
| **第三段** | fsyyft-go 相关包 | **强制**使用 `kit` 前缀别名 | `kitlog "github.com/fsyyft-go/kit/log"` |
| **第四段** | 项目内部包 | **强制**使用 `app` 前缀别名 | `appconf "github.com/.../internal/pkg/conf"` |

### 3. 别名规范表

**fsyyft-go 包别名**：
| 包路径 | 强制别名 |
|-------|---------|
| `github.com/fsyyft-go/kit/log` | `kitlog` |
| `github.com/fsyyft-go/kit/runtime` | `kitruntime` |
| `github.com/fsyyft-go/kit/kratos/middleware/validate` | `kitkratosmiddlewarevalidate` |

**项目内部包别名**：
| 包路径 | 强制别名 |
|-------|---------|
| `github.com/fsyyft-go/kratos-layout/api/helloworld/v1` | `apphelloworldv1` |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/conf` | `appconf` |
| `github.com/fsyyft-go/kratos-layout/internal/pkg/log` | `applog` |

## 故障排除

### 常见问题

#### 问题 1：Claude 分析时间较长

**症状**：
```
Claude 分析需要较长时间
```

**解决方案**：
1. 大型项目分析需要 3-5 分钟，请耐心等待
2. 如果超时，可以分目录分析
3. 确保网络连接稳定

---

#### 问题 2：生成文件被误修改

**症状**：
```
生成文件被意外修改
```

**解决方案**：
1. Claude 会自动识别生成文件（`*.pb.go`, `wire_gen.go`）
2. 生成文件的导入顺序由工具决定，不强制要求调整
3. 如果有问题，可以回滚到修改前

---

### 回滚操作

**触发条件**：
- 修复后发现新问题
- 不满意修复结果
- 想重新开始

**回滚方法**：
```bash
# 使用 Git 回滚
git checkout .

# 或恢复备份
git reset --hard HEAD~
```

---

## 最佳实践

### 检查前准备

1. **确保代码可编译**
   - 运行 `go build ./...`
   - 确保无编译错误

2. **创建分支**
   - 在新分支上进行修复
   - 便于回滚和代码审查

3. **提交更改**
   - 修复前先提交当前状态
   - 便于对比和回滚

---

### 检查过程

1. **Claude 全面分析**
   - 直接将项目交给 Claude
   - Claude 会自动完成所有工作
   - 等待分析完成

2. **审查调整结果**
   - 查看 Claude 提供的报告
   - 检查自动调整的内容
   - 确认是否满意

---

### 修复后处理

1. **验证修复**
   - 运行 `go build ./...`
   - 运行 `go test ./...`
   - 检查修复结果

2. **查看分析报告**
   - Claude 会生成完整的 Markdown 报告
   - 包含所有发现的问题和解决方案
   - 提供最佳实践建议

3. **提交更改**
   - 创建清晰的 commit message
   - 推送到远程仓库

4. **代码审查**
   - 让团队成员审查
   - 确保修复质量

---

## 工作原理总结

**第一步：Claude 扫描**
- Claude 扫描项目所有 Go 文件
- 分析导入规范问题
- 识别手写代码和生成代码

**第二步：Claude 分析**
- 验证格式、分组、别名规范
- 检测循环依赖
- 生成详细分析报告

**第三步：Claude 调整**
- 自动调整不规范内容
- 应用正确格式和别名
- 解决发现的问题

**最终结果**
- 规范化后的代码
- 完整的分析报告
- 最佳实践建议

---

## 技术规格

- **Go 版本**：1.16+（Go modules）
- **Python 版本**：无需（完全由 Claude 处理）
- **跨平台**：Windows, macOS, Linux
- **大模型**：Anthropic Claude API

---

## 注意事项

1. **100% Claude 驱动**
   - 完全由 Claude 负责所有工作
   - 无需脚本辅助
   - Claude 能够识别和纠正任何潜在问题

2. **区分代码类型**
   - 手写代码：严格按照导入规范检查
   - 生成代码：自动识别并特殊处理（如 `*.pb.go`, `wire_gen.go`）
   - 生成代码的导入顺序由工具决定，不强制要求调整

3. **Claude 自动调整**
   - Claude 会自动调整不规范的内容
   - 修复前建议创建 Git 分支
   - Claude 会生成完整的分析报告说明所有调整

4. **性能考虑**
   - Claude 分析时间：3-5 分钟（取决于代码量）
   - 大型项目建议使用 Claude 进行全面分析
   - 分析结果更准确、更全面

---

## 相关资源

### 规范来源
- `references/import_standards.md` - 提取的导入规范
- `references/alias_mapping.md` - 标准别名映射表

### 示例代码
- `internal/biz/greeter.go` - 业务层示例
- `internal/service/greeter.go` - 服务层示例
- `cmd/web/main.go` - 应用入口示例

### 参考文档
- [Effective Go](https://golang.org/doc/effective_go.html#imports)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments#imports)
- [Kratos Framework Documentation](https://go-kratos.dev/)
