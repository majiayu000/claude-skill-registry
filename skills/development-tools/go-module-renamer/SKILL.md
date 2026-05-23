---
name: go-module-renamer
description: Go 模块重命名自动化工具。用于新 git clone 的项目进行 Go 模块重命名，支持全量/部分重命名智能识别，文本替换优先策略，完善的验证和回滚机制。
---

# Go 模块重命名器

## 概述

自动化 Go 项目模块重命名，支持智能识别重命名类型（全量/部分），使用文本替换策略快速更新模块引用，提供浅层和深层双重验证，确保重命名安全可靠。

## 使用场景

- **新克隆的项目重命名** - Git clone 后快速重命名模块到自己的仓库
- **项目迁移** - 将项目从一个组织迁移到另一个组织
- **项目重命名** - 仅更改项目名称而保持组织结构
- **模块重构** - 重组项目结构并更新模块路径

## 快速开始

### 一键重命名（推荐）

对于全新克隆的项目：

```bash
# 1. 检测当前模块名
.claude/skills/go-module-renamer/scripts/detect_module.sh

# 2. 分析重命名类型
python3 .claude/skills/go-module-renamer/scripts/analyze_rename_type.py \
  <旧模块名> <新模块名>

# 3. 执行重命名
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  <旧模块名> <新模块名>

# 4. 浅层验证
.claude/skills/go-module-renamer/scripts/validate_quick.sh

# 5. 深层验证
python3 .claude/skills/go-module-renamer/scripts/validate_deep.py <旧模块名>
```

### 试运行模式

在实际重命名前先查看影响范围：

```bash
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  <旧模块名> <新模块名> --dry-run
```

## 工作流程

### 场景 1：全量重命名

**适用情况**：域名或用户名变更

```
github.com/fsyyft-go/kratos-layout → github.com/new-org/new-project
```

**工作流程**：

```
开始
  ↓
1. 检测当前模块名
   [detect_module.sh]
   输出：模块名结构（域名、用户名、项目名）
  ↓
2. 分析重命名类型
   [analyze_rename_type.py]
   判断：全量重命名（前两部分不同）
  ↓
3. 执行重命名
   [perform_rename.py]
   ├─ 创建备份（.backup/）
   ├─ 替换完整模块路径
   │  ├─ go.mod 模块声明
   │  ├─ .go 文件导入路径
   │  ├─ .proto 文件 go_package
   │  └─ 文档中的代码示例
   ├─ 替换项目名
   │  ├─ Makefile 变量
   │  ├─ 配置文件
   │  └─ 文档标题
   └─ 清理模板注释
  ↓
4. 浅层验证
   [validate_quick.sh]
   ├─ go fmt
   ├─ go mod tidy
   ├─ make lint
   └─ make build
  ↓
5. 深层验证
   [validate_deep.py]
   ├─ 搜索代码文件残留
   ├─ 检查配置文件
   └─ 审查文档引用
  ↓
完成
```

---

### 场景 2：部分重命名

**适用情况**：仅项目名变更

```
github.com/fsyyft-go/kratos-layout → github.com/fsyyft-go/new-project
```

**工作流程**：

```
开始
  ↓
1. 检测当前模块名
   [detect_module.sh]
  ↓
2. 分析重命名类型
   [analyze_rename_type.py]
   判断：部分重命名（仅最后部分不同）
  ↓
3. 执行重命名
   [perform_rename.py]
   ├─ 创建备份（.backup/）
   └─ 替换项目名
      ├─ Makefile 变量
      ├─ Docker 镜像名
      ├─ 配置文件
      └─ 文档标题
  ↓
4. 验证（同上）
  ↓
完成
```

---

## 脚本说明

### detect_module.sh - 模块名检测器

**功能**：
- 从 go.mod 读取当前模块名
- 解析模块名结构（域名、用户名、项目名）
- 输出 JSON 格式信息

**用法**：
```bash
.claude/skills/go-module-renamer/scripts/detect_module.sh
```

**输出示例**：
```json
{
  "full_path": "github.com/fsyyft-go/kratos-layout",
  "domain": "github.com",
  "username": "fsyyft-go",
  "project": "kratos-layout"
}
```

**返回值**：
- `0` - 成功
- `1` - go.mod 不存在
- `2` - 无法解析模块名

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### analyze_rename_type.py - 重命名类型分析器

**功能**：
- 比较新旧模块名
- 判断全量或部分重命名
- 生成替换规则列表

**用法**：
```bash
python3 .claude/skills/go-module-renamer/scripts/analyze_rename_type.py \
  <旧模块名> <新模块名>
```

**示例**：
```bash
python3 .claude/skills/go-module-renamer/scripts/analyze_rename_type.py \
  github.com/fsyyft-go/kratos-layout \
  github.com/new-org/new-project
```

**输出示例**：
```json
{
  "type": "full",
  "old_module": "github.com/fsyyft-go/kratos-layout",
  "new_module": "github.com/new-org/new-project",
  "old_project": "kratos-layout",
  "new_project": "new-project",
  "replacements": {
    "full_replace": [...],
    "partial_replace": [...]
  }
}
```

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### perform_rename.py - 重命名执行器（核心）

**功能**：
- 创建备份
- 执行文本替换（根据类型选择策略）
- 清理模板注释
- 生成操作报告

**用法**：
```bash
# 基本用法
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  <旧模块名> <新模块名>

# 指定重命名类型
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  <旧模块名> <新模块名> --type=full

# 试运行模式（不实际修改文件）
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  <旧模块名> <新模块名> --dry-run
```

**参数说明**：
- `old_module` - 旧模块名（必需）
- `new_module` - 新模块名（必需）
- `--type` - 重命名类型：auto（默认）、full、partial
- `--dry-run` - 试运行模式，不实际修改文件

**Python 环境管理**：
- 自动检测 `.venv` 虚拟环境
- 如果虚拟环境存在，优先使用
- 如果不存在，提示使用 python-venv-manager 创建

**自动化程度**：
- 脚本自动化：90%
- 大模型介入：10%（处理特殊情况、环境管理）

---

### validate_quick.sh - 浅层验证脚本

**功能**：
- 执行快速验证命令
- 收集验证结果
- 返回通过/失败状态

**用法**：
```bash
# 完整验证
.claude/skills/go-module-renamer/scripts/validate_quick.sh

# 跳过 lint 检查
.claude/skills/go-module-renamer/scripts/validate_quick.sh --skip-lint

# 跳过编译验证
.claude/skills/go-module-renamer/scripts/validate_quick.sh --skip-build
```

**验证命令序列**：
1. `go fmt ./...` - 代码格式化
2. `go mod tidy` - 依赖管理
3. `make lint` - Lint 检查（可选）
4. `make build` - 编译验证（可选）

**输出示例**：
```
======================================
步骤 1: 代码格式化 (go fmt)
======================================
✓ 通过: 代码格式化完成

======================================
步骤 2: 依赖管理 (go mod tidy)
======================================
✓ 通过: 依赖管理完成

...
======================================
验证总结
======================================
总步骤数: 4
通过: 4
失败: 0

✅ 浅层验证全部通过！
```

**返回值**：
- `0` - 全部通过
- `1` - 有失败

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### validate_deep.py - 深层验证脚本

**功能**：
- 搜索所有包含旧模块名的文件
- 分类文件类型（代码/配置/文档）
- 对不同类型采取不同策略

**用法**：
```bash
# 基本用法
python3 .claude/skills/go-module-renamer/scripts/validate_deep.py <旧模块名>

# 指定旧项目名
python3 .claude/skills/go-module-renamer/scripts/validate_deep.py \
  <旧模块名> --old-project=<旧项目名>
```

**分类规则**：

| 文件类型 | 残留引用处理 | 理由 |
|---------|-------------|------|
| .go、.proto | ❌ 报告错误 | 代码文件不应该有残留 |
| Makefile、config.yaml | ⚠️ 警告 | 可能需要手动检查 |
| README.md | ✅ 自动替换 | 明显的文档引用 |
| .github/*.md | ✅ 自动替换 | GitHub 文档 |
| 注释、文档 | ℹ️ 信息提示 | 可能是历史说明 |

**输出示例**：
```
🔍 深层验证：搜索残留引用
   搜索模式：
   - github.com/fsyyft-go/kratos-layout
   - kratos-layout

📂 搜索代码文件...
📂 搜索配置文件...
📂 搜索文档文件...

==================================================
📊 深层验证结果
==================================================

❌ 代码文件中的残留（2 个文件）：
   - internal/server/server.go
     行 10: import "github.com/fsyyft-go/kratos-layout/internal/conf"
   - api/helloworld/v1/greeter.proto
     行 5: option go_package = "github.com/fsyyft-go/kratos-layout/api"

⚠️  配置文件中的残留（1 个文件）：
   - Makefile
     行 5: IMAGE_NAME := fsyyft/kratos-layout

ℹ️  文档文件中的残留（3 个文件）：
   - README.md
   - docs/api.md
   - .github/CONTRIBUTING.md
```

**返回值**：
- `0` - 无残留或仅有文档残留
- `1` - 代码文件中有残留
- `2` - 配置文件中有残留

**自动化程度**：
- 脚本自动化：70%
- 大模型介入：30%（分析文档上下文）

---

## 验证策略

### 浅层验证（快速验证）

**目标**：快速发现明显的编译和语法错误

**时间**：1-3 分钟

**验证内容**：
- ✅ 代码格式化
- ✅ 依赖管理
- ✅ Lint 检查（可选）
- ✅ 编译验证（可选）

**通过标准**：
- 所有命令返回码为 0
- 无编译错误
- 无关键 Lint 错误

---

### 深层验证（全面检查）

**目标**：发现所有残留的旧模块名引用

**时间**：3-5 分钟

**验证内容**：
- ✅ 代码文件无残留
- ⚠️  配置文件检查
- ℹ️  文档文件审查

**通过标准**：
- 代码文件中无残留引用
- 配置文件残留已审查
- 文档残留已记录

---

## 故障排除

### 常见问题

#### 问题 1：编译失败

**症状**：
```
cannot find package "github.com/old/module/path"
```

**解决方案**：
1. 检查导入路径是否正确
2. 运行 `go mod tidy`
3. 检查 go.mod 中的模块名

---

#### 问题 2：残留引用未清理

**症状**：
深层验证发现代码文件中有残留引用

**解决方案**：
1. 使用 grep 定位所有残留
2. 手动修复或使用批量替换
3. 重新运行验证

**示例**：
```bash
grep -rn "旧模块名" --include="*.go" .
sed -i '' 's|旧模块名|新模块名|g' file.go
```

---

#### 问题 3：验证失败，是否回滚？

**判断依据**：
- **应该回滚**：编译失败、大量测试失败、无法快速修复
- **可以继续**：仅文档残留、配置文件警告

**回滚方法**：
```bash
# 自动回滚（使用备份）
cp -r .backup/* .

# 或使用 Git
git checkout .
```

---

#### 问题 4：Python 环境问题

**症状**：
```
ModuleNotFoundError: No module named 'yaml'
```

**解决方案**：
1. 检查虚拟环境是否存在
2. 安装依赖：`pip install pyyaml`
3. 或使用 python-venv-manager 创建虚拟环境

---

### 回滚操作

**触发条件**：
- 编译失败且无法快速修复
- 大量测试失败
- 关键功能异常

**回滚步骤**：
1. 停止当前操作
2. 恢复备份文件
3. 验证恢复结果
4. 分析失败原因
5. 修复问题后重新尝试

---

## 最佳实践

### 重命名前准备

1. **备份代码**
   - 创建 Git 分支
   - 推送到远程仓库

2. **通知团队**
   - 告知团队成员重命名计划
   - 协调重命名时间

3. **准备环境**
   - 确保依赖工具已安装
   - 检查 Python 虚拟环境

4. **规划验证**
   - 准备测试用例
   - 确定验证标准

---

### 重命名过程

1. **使用试运行模式**
   - 先执行 `--dry-run` 查看影响范围
   - 审查替换规则是否正确

2. **创建备份**
   - 脚本会自动创建 `.backup` 目录
   - 保留备份直到验证完成

3. **分步执行**
   - 按顺序执行每个步骤
   - 每步执行后检查结果

4. **验证结果**
   - 先运行浅层验证
   - 再运行深层验证
   - 最后运行功能测试

---

### 重命名后处理

1. **提交更改**
   - 创建清晰的 commit message
   - 推送到远程仓库

2. **更新文档**
   - 更新 README.md
   - 更新 API 文档
   - 更新贡献指南

3. **通知相关人员**
   - 通知团队成员
   - 更新相关系统
   - 更新 CI/CD 配置

---

## 自动化程度

**总体自动化程度**：80% 脚本 + 20% 大模型辅助

### 大模型介入点

| 介入点 | 触发条件 | 大模型职责 | 介入程度 |
|-------|---------|-----------|---------|
| Python 环境检测 | 脚本启动时 | 检查虚拟环境，决定是否创建 | 10% |
| 类型分析确认 | 分析完成 | 显示结果，让用户确认 | 5% |
| 未知文件类型 | 遇到新类型文件 | 判断如何处理 | 5% |
| 特殊情况处理 | 发现复杂情况 | 提供处理建议 | 10% |
| 文档引用分析 | 深层验证 | 判断是否需要更新 | 20% |
| 验证失败诊断 | lint/build 失败 | 分析错误，提供解决方案 | 30% |
| 用户指导 | 用户询问 | 解释操作，提供后续步骤 | 按需 |

---

## 资源

### scripts/

包含 5 个可执行脚本：

1. **detect_module.sh** - 模块名检测器（约 70 行）
2. **analyze_rename_type.py** - 重命名类型分析器（约 250 行）
3. **perform_rename.py** - 重命名执行器（约 450 行）
4. **validate_quick.sh** - 浅层验证脚本（约 180 行）
5. **validate_deep.py** - 深层验证脚本（约 350 行）

所有脚本：
- 使用 Python 3.8+ 和 Bash
- 包含完整的中文注释
- 提供详细的错误处理
- 跨平台支持（Windows/macOS/Linux）
- 可以独立执行或在大模型指导下执行

---

### references/

包含详细的参考资料：

1. **file_patterns.md**
   - Go 项目标准文件类型
   - 每种文件类型的替换模式
   - 全量 vs 部分替换的判断规则
   - 特殊文件的处理方法

2. **validation_rules.md**
   - 验证命令的执行顺序
   - 每个命令的预期结果
   - 常见错误和解决方案
   - 回滚触发条件

---

### assets/

包含报告模板和示例文件（待补充）。

---

## 示例用法

### 示例 1：新克隆项目快速启动

```bash
# 克隆项目
git clone https://github.com/fsyyft-go/kratos-layout.git my-project
cd my-project

# 1. 检测当前模块名
.claude/skills/go-module-renamer/scripts/detect_module.sh
# 输出：github.com/fsyyft-go/kratos-layout

# 2. 试运行查看影响
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  github.com/fsyyft-go/kratos-layout \
  github.com/myorg/my-project \
  --dry-run

# 3. 执行重命名
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  github.com/fsyyft-go/kratos-layout \
  github.com/myorg/my-project

# 4. 验证
.claude/skills/go-module-renamer/scripts/validate_quick.sh
python3 .claude/skills/go-module-renamer/scripts/validate_deep.py \
  github.com/fsyyft-go/kratos-layout

# 5. 提交
git add .
git commit -m "feat: 重命名模块为 github.com/myorg/my-project"
```

---

### 示例 2：检测到残留引用

当 `validate_deep.py` 发现代码文件中有残留时：

```bash
$ python3 validate_deep.py github.com/fsyyft-go/kratos-layout

❌ 代码文件中的残留（1 个文件）：
   - internal/server/server.go
     行 15: import "github.com/fsyyft-go/kratos-layout/internal/conf"

⚠️  发现代码文件中的残留引用，这可能导致编译或运行时错误。
   建议：手动检查并修复这些文件
```

**修复方法**：
```bash
# 方法 1：使用 sed
sed -i '' 's|github.com/fsyyft-go/kratos-layout|github.com/myorg/my-project|g' \
  internal/server/server.go

# 方法 2：使用编辑器批量替换
# 在 VSCode 中：Cmd+Shift+H，查找旧模块名，替换为新模块名

# 方法 3：重新运行 perform_rename.py
python3 .claude/skills/go-module-renamer/scripts/perform_rename.py \
  github.com/fsyyft-go/kratos-layout \
  github.com/myorg/my-project
```

---

### 示例 3：浅层验证失败

当 `validate_quick.sh` 执行失败时：

```bash
$ validate_quick.sh

======================================
步骤 3: Lint 检查 (make lint)
======================================
✗ 失败: Lint 检查失败

level=error msg="internal/server/server.go:15:2: import shadowing: \
  conf \"github.com/myorg/my-project/internal/conf\""
```

**大模型分析**：
- 识别错误类型：import shadowing（包名冲突）
- 提供解决方案：使用别名避免冲突
- 生成修复代码：

```go
// 修复前
import "github.com/myorg/my-project/internal/conf"

// 修复后（使用别名）
import serverconf "github.com/myorg/my-project/internal/conf"
```

---

## 技术规格

- **Go 版本**：1.16+（Go modules）
- **Python 版本**：3.8+（脚本执行）
- **虚拟环境**：.venv（推荐使用 python-venv-manager）
- **跨平台**：Windows, macOS, Linux
- **备份位置**：`.backup/` 在项目根目录
- **替换策略**：文本替换优先（更快，无需工具链）

---

## 注意事项

1. **Git 远程仓库**
   - 重命名前更新 Git 远程仓库 URL
   - 确保新模块路径在远程仓库中存在

2. **依赖包**
   - 如果有私有依赖包，更新 import 路径
   - 检查 go.work 文件（如果使用 Go workspaces）

3. **CI/CD**
   - 更新 GitHub Actions / GitLab CI 配置
   - 更新 Docker 镜像名称

4. **文档**
   - 更新 README.md 中的克隆命令
   - 更新 API 文档中的包路径示例
   - 更新贡献指南

5. **团队协作**
   - 重命名前通知团队成员
   - 协调重命名时间
   - 提供迁移指南

---

## 相关资源

- [Go Modules Reference](https://golang.org/ref/mod)
- [Protocol Buffers Style Guide](https://developers.google.com/protocol-buffers/docs/style)
- [Kratos Framework Documentation](https://go-kratos.dev/)
- [Go Module Mirror and Checksum Database](https://sum.golang.org/)
