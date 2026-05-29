---
name: python-venv-manager
description: Python 虚拟环境自动化管理工具。当项目需要创建或管理 Python 虚拟环境（.venv）时使用此技能：检测现有环境、创建新环境、生成 requirements.txt、安装依赖包、配置 Git 忽略规则。
---

# Python 虚拟环境管理器

## 概述

自动化 Python 虚拟环境（.venv）的创建、管理和依赖安装，确保项目依赖隔离和开发环境的可重现性。

## 使用场景

- **新项目初始化** - 为全新 Python 项目设置虚拟环境
- **现有项目环境化** - 为没有虚拟环境的项目添加依赖隔离
- **依赖管理** - 自动生成和维护 requirements.txt
- **环境健康检查** - 验证虚拟环境状态和完整性
- **团队协作** - 确保所有开发者使用相同的环境配置

## 快速开始

### 一键初始化（推荐）

对于全新项目，执行完整流程：

```bash
# 1. 检查虚拟环境状态
python3 .claude/skills/python-venv-manager/scripts/check_venv.py

# 2. 创建虚拟环境
python3 .claude/skills/python-venv-manager/scripts/create_venv.py

# 3. 生成 requirements.txt（如果不存在）
python3 .claude/skills/python-venv-manager/scripts/generate_requirements.py

# 4. 安装依赖
python3 .claude/skills/python-venv-manager/scripts/install_deps.py

# 5. 更新 .gitignore
python3 .claude/skills/python-venv-manager/scripts/update_gitignore.py
```

### 分步执行

根据项目实际情况选择需要的步骤。

## 工作流程

### 场景 1：全新项目

```
开始
  ↓
1. 检查是否已有虚拟环境
   [check_venv.py]
   ├─ 已存在 → 显示状态，询问是否继续
   └─ 不存在 → 继续
       ↓
2. 创建虚拟环境
   [create_venv.py]
   使用系统默认 python3
       ↓
3. 生成 requirements.txt
   [generate_requirements.py]
   ├─ 扫描所有 .py 文件
   ├─ 提取 import 语句
   ├─ 过滤标准库和本地模块
   └─ 生成 requirements.txt
       ↓
4. 审查 requirements.txt
   人工检查生成的依赖列表
   ├─ 调整版本要求
   └─ 添加遗漏的包
       ↓
5. 安装依赖
   [install_deps.py]
   ├─ 升级 pip
   └─ 安装 requirements.txt 中的包
       ↓
6. 配置 Git
   [update_gitignore.py]
   添加 .venv/ 到 .gitignore
       ↓
完成
```

### 场景 2：现有项目（有 requirements.txt）

```
开始
  ↓
1. 检查虚拟环境
   [check_venv.py]
       ↓
2. 创建虚拟环境
   [create_venv.py]
       ↓
3. 安装依赖
   [install_deps.py]
   使用现有 requirements.txt
       ↓
4. 配置 Git
   [update_gitignore.py]
       ↓
完成
```

### 场景 3：现有项目（无 requirements.txt）

```
开始
  ↓
1. 检查虚拟环境
   [check_venv.py]
       ↓
2. 生成 requirements.txt
   [generate_requirements.py]
   从代码分析生成
       ↓
3. 审查 requirements.txt
   人工检查和调整
       ↓
4. 创建虚拟环境
   [create_venv.py]
       ↓
5. 安装依赖
   [install_deps.py]
       ↓
6. 配置 Git
   [update_gitignore.py]
       ↓
完成
```

## 脚本说明

### check_venv.py - 虚拟环境检查器

检查项目根目录是否存在有效的 .venv 虚拟环境。

**功能**：
- 检查 .venv 目录是否存在
- 验证虚拟环境完整性（激活脚本、Python 解释器）
- 显示虚拟环境的 Python 版本
- 报告 pip 可用性

**返回值**：
- `0` - 虚拟环境存在且有效
- `1` - 虚拟环境不存在
- `2` - 虚拟环境存在但无效

**用法**：
```bash
python3 .claude/skills/python-venv-manager/scripts/check_venv.py
```

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### create_venv.py - 虚拟环境创建器

创建 .venv 虚拟环境。

**功能**：
- 使用系统默认 python3 或指定 Python 版本创建虚拟环境
- 检测并处理已存在的虚拟环境（交互模式）
- 显示激活命令提示

**参数**：
- `python_path` - 可选的 Python 解释器路径

**用法**：
```bash
# 使用系统默认 python3
python3 .claude/skills/python-venv-manager/scripts/create_venv.py

# 使用指定 Python 版本
python3 .claude/skills/python-venv-manager/scripts/create_venv.py python3.11
```

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### generate_requirements.py - 依赖生成器

分析项目代码生成 requirements.txt。

**功能**：
- 扫描项目中所有 .py 文件（排除虚拟环境和缓存目录）
- 使用 AST 解析提取所有 import 语句
- 过滤 Python 标准库（包含 Python 3.8-3.14 完整列表）
- 过滤本地模块导入
- 处理常见包别名映射（如 yaml → pyyaml）
- 生成使用宽松版本的 requirements.txt
- 检测可疑导入（动态导入、条件性依赖）
- 提示人工检查特殊情况

**用法**：
```bash
python3 .claude/skills/python-venv-manager/scripts/generate_requirements.py
```

**输出**：
- requirements.txt 文件
- 特殊情况报告（需要人工检查）

**包别名处理**：
- `yaml` → `pyyaml`
- `PIL` → `pillow`
- `cv2` → `opencv-python`
- `bs4` → `beautifulsoup4`
- `sklearn` → `scikit-learn`

**自动化程度**：80% 脚本 + 20% 大模型辅助

**大模型介入点**：
- 分析检测到的可疑导入
- 判断动态导入是否为必需依赖
- 判断条件性依赖是否必需
- 优化版本策略（哪些包需要固定版本）
- 建议是否拆分 requirements-dev.txt

---

### install_deps.py - 依赖安装器

安装 requirements.txt 中的依赖到虚拟环境。

**功能**：
- 验证虚拟环境和 requirements.txt 存在性
- 升级 pip 到最新版本
- 安装 requirements.txt 中的所有包
- 显示已安装的包列表

**用法**：
```bash
python3 .claude/skills/python-venv-manager/scripts/install_deps.py
```

**自动化程度**：100% 脚本自动化，无需大模型介入

---

### update_gitignore.py - Git 忽略规则更新器

更新 .gitignore 文件，确保 .venv 被忽略。

**功能**：
- 如果 .gitignore 不存在，创建它
- 检查是否已包含 .venv 规则
- 仅在缺失时添加 .venv 规则
- 保留现有 .gitignore 内容

**用法**：
```bash
python3 .claude/skills/python-venv-manager/scripts/update_gitignore.py
```

**自动化程度**：100% 脚本自动化，无需大模型介入

## 最佳实践

### 虚拟环境命名

**推荐**：`.venv`（现代标准，PEP 405）

### requirements.txt 版本策略

**开发环境**（宽松版本）：
```txt
package>=1.0.0
```

**生产环境**（固定版本）：
```txt
package>=1.2.0,<2.0.0
```

**多文件管理**：
- `requirements.txt` - 生产依赖
- `requirements-dev.txt` - 开发依赖
- `requirements.lock` - 精确锁定（由 pip-compile 生成）

### 工作流程建议

**新项目**：
1. 创建虚拟环境
2. 安装依赖
3. 生成 requirements.txt
4. 配置 .gitignore
5. 提交到 Git

**克隆项目**：
1. 创建虚拟环境
2. 安装依赖（使用现有 requirements.txt）
3. 验证环境

## 故障排除

### 虚拟环境激活失败

**症状**：运行激活命令后提示符没有变化

**解决方案**：
```bash
# 检查虚拟环境是否存在
ls -la .venv/bin/

# 验证 Python 可用
.venv/bin/python --version

# 重新创建虚拟环境
rm -rf .venv
python3 -m venv .venv
```

### requirements.txt 生成不准确

**症状**：遗漏某些包或包含不必要的包

**解决方案**：
```bash
# 1. 查看可疑导入报告
python3 generate_requirements.py

# 2. 人工检查生成的 requirements.txt
cat requirements.txt

# 3. 手动调整：
#    - 添加遗漏的包
#    - 删除不必要的包
#    - 调整版本要求
```

### 依赖安装失败

**症状**：pip install 报错

**解决方案**：
```bash
# 1. 升级 pip
.venv/bin/pip install --upgrade pip

# 2. 清理 pip 缓存
pip cache purge

# 3. 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 逐个安装，找出冲突包
pip install package1
pip install package2
```

### Python 版本不兼容

**症状**：某些包需要特定 Python 版本

**解决方案**：
```bash
# 1. 检查当前 Python 版本
python3 --version

# 2. 使用特定 Python 版本创建虚拟环境
python3.11 -m venv .venv

# 3. 或使用 pyenv 管理多版本
pyenv install 3.11.0
pyenv local 3.11.0
python3 -m venv .venv
```

## 资源

### scripts/ 目录

包含 5 个可执行脚本：

1. **check_venv.py** - 虚拟环境检查器（约 70 行）
2. **create_venv.py** - 虚拟环境创建器（约 100 行）
3. **generate_requirements.py** - 依赖生成器（约 250 行）
4. **install_deps.py** - 依赖安装器（约 120 行）
5. **update_gitignore.py** - Git 忽略规则更新器（约 60 行）

所有脚本：
- 使用 Python 3.8+ 语法
- 包含完整的中文注释
- 提供详细的错误处理
- 跨平台支持（Windows/macOS/Linux）
- 可以独立执行或在大模型指导下执行

### references/ 目录

包含详细的参考资料：

1. **best_practices.md**
   - 虚拟环境的重要性
   - 命名规范
   - 版本固定策略
   - .gitignore 最佳实践
   - 跨平台兼容性
   - 常见问题和解决方案

2. **common_packages.md**
   - 常用开发工具包（black, pytest, mypy 等）
   - Web 框架包（django, flask, fastapi）
   - 数据科学包（numpy, pandas, scipy）
   - 网络工具包（requests, httpx, beautifulsoup4）
   - 包别名映射表

## 示例用法

### 示例 1：新项目快速启动

```bash
# 克隆项目后
git clone https://github.com/user/project.git
cd project

# 一键设置环境
python3 .claude/skills/python-venv-manager/scripts/check_venv.py
python3 .claude/skills/python-venv-manager/scripts/create_venv.py
python3 .claude/skills/python-venv-manager/scripts/generate_requirements.py
# 编辑 requirements.txt（如需要）
python3 .claude/skills/python-venv-manager/scripts/install_deps.py
python3 .claude/skills/python-venv-manager/scripts/update_gitignore.py

# 开始工作
source .venv/bin/activate
python main.py
```

### 示例 2：检测到的可疑导入

当 `generate_requirements.py` 检测到特殊情况时：

```bash
$ python3 generate_requirements.py

⚠️  检测到 2 个需要人工检查的情况：
   - src/utils.py (行 45): 可能的条件性导入
   - src/config.py: 使用动态导入 importlib.import_module

💡 提示：某些动态导入或条件性依赖可能需要手动添加到 requirements.txt
```

**大模型分析**：
- 查看这些文件的具体代码
- 判断动态导入的包是否为必需依赖
- 提供优化建议（如添加到 requirements-opt.txt 作为可选依赖）

### 示例 3：版本策略优化

脚本生成的 requirements.txt 使用默认的 `>=1.0.0` 版本要求。

**大模型建议**：
```
"检测到数据科学包：numpy, pandas"
"建议固定 numpy 版本：numpy>=1.20.0,<2.0.0"
"检测到开发工具：pytest, black"
"建议创建 requirements-dev.txt 包含开发工具"
```

## 技术规格

- **Python 版本**：3.8+（使用系统默认 python3）
- **虚拟环境**：.venv（标准 venv 模块）
- **依赖文件**：requirements.txt
- **跨平台**：Windows, macOS, Linux
- **标准库**：包含 Python 3.8-3.14 完整列表

## 注意事项

1. **动态导入**：`importlib.import_module()` 等动态导入无法通过 AST 解析检测，需要手动添加
2. **条件性依赖**：try/except 块中的导入可能是可选依赖，需要人工判断
3. **本地模块**：相对导入（如 `from .utils import helper`）会被正确过滤
4. **版本兼容性**：生成的 requirements.txt 使用宽松版本，生产环境建议固定版本
5. **Git 安全**：确保 .venv 在 .gitignore 中，不要提交虚拟环境到版本控制

## 相关资源

- [PEP 405 -- Python Virtual Environments](https://www.python.org/dev/peps/pep-0405/)
- [Python venv 文档](https://docs.python.org/3/library/venv.html)
- [pip 用户指南](https://pip.pypa.io/en/stable/user_guide/)
