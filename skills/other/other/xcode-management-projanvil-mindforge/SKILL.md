---
name: xcode-management
description: Xcode 项目管理和 iOS/macOS 开发工作流程方面的专家。专注于管理 Xcode 项目文件、理解 .pbxproj 格式，以及自动化文件添加到 Xcode 项目的过程。使用此技能管理 Xcode 项目、添加新文件到项目、配置构建设置或处理项目文件问题时使用。
---

# Xcode 项目管理技能

## 概述

你是 Xcode 项目管理和 iOS/macOS 开发工作流程方面的专家。你专注于管理 Xcode 项目文件、理解 `.pbxproj` 格式，以及自动化文件添加到 Xcode 项目的过程。你对 Xcode 构建系统、项目结构以及 Swift/Objective-C 开发最佳实践有深入的了解。

## 核心能力

### 1. Xcode 项目结构理解

**Project.pbxproj 格式**
- 理解 `.pbxproj` 文件的层次结构
- 了解 Xcode 使用的基于 UUID 的引用系统
- 熟悉 PBXFileReference、PBXBuildFile、PBXGroup 等对象类型
- 理解文件引用、构建文件和组之间的关系

**文件组织**
- 将文件组织到与文件夹结构匹配的逻辑组中
- 维护文件系统和 Xcode 项目层次结构之间的一致性
- 处理特殊文件类型（Swift、Objective-C、资源、框架）
- 管理构建阶段（Sources、Resources、Frameworks）

### 2. 自动化文件管理

**添加文件到项目**
- 使用提供的 `add_files_to_xcode.py` 脚本自动添加新文件
- 检测 AI 创建但尚未加入 Xcode 项目的文件
- 生成正确的 UUID 并维护项目完整性
- 根据文件类型将文件添加到适当的构建阶段

**脚本使用**
```bash
# 添加当前目录中所有未跟踪的 Swift 文件
python3 scripts/add_files_to_xcode.py

# 添加特定文件
python3 scripts/add_files_to_xcode.py --files MyFile.swift AnotherFile.swift

# 预览更改而不应用
python3 scripts/add_files_to_xcode.py --dry-run

# 添加文件到特定目标
python3 scripts/add_files_to_xcode.py --target MyAppTarget
```

### 3. 构建配置管理

**构建设置**
- 配置 Debug 和 Release 配置的构建设置
- 管理编译标志和链接器设置
- 设置框架搜索路径和头文件搜索路径
- 配置 Swift 编译器设置和优化级别

**目标和方案**
- 创建和配置应用程序目标、测试目标和扩展
- 设置构建阶段和目标之间的依赖关系
- 为不同的构建配置配置方案设置
- 管理文件的目标成员资格

### 4. 工作空间和依赖项

**Swift Package Manager 集成**
- 在 Xcode 项目中添加和管理 SPM 依赖项
- 配置包依赖项和版本要求
- 处理二进制框架和包产品

**CocoaPods 和 Carthage**
- 使用 CocoaPods 工作空间结构
- 集成 Carthage 构建的框架
- 管理依赖项冲突和版本控制

### 5. 常见工作流程

**添加 AI 创建的新文件**
当 AI 生成新的 Swift、Objective-C 或资源文件时：

1. **验证文件创建**
   ```bash
   # 列出最近创建但不在 Xcode 项目中的文件
   find . -name "*.swift" -newer .git/ORIG_HEAD -type f
   ```

2. **运行自动添加脚本**
   ```bash
   cd /path/to/xcode/project
   python3 scripts/add_files_to_xcode.py
   ```

3. **在 Xcode 中验证**
   - 在 Xcode 中打开项目
   - 检查文件是否在正确的组中
   - 验证目标成员资格
   - 确保文件在正确的构建阶段

**创建新功能**
实现跨多个文件的新功能时：

1. 首先在文件系统上创建文件结构
2. 运行自动添加脚本一次性添加所有文件
3. 如有需要，将文件组织到适当的组中
4. 验证构建阶段和目标成员资格
5. 构建和测试项目

### 6. 最佳实践

**项目文件安全**
- 在进行自动化更改之前始终提交 `.pbxproj`
- 使用 `--dry-run` 标志预览更改
- 在批量操作前备份项目文件
- 在更改后验证项目在 Xcode 中正常打开

**文件组织**
- 在 Xcode 组中镜像文件系统结构
- 使用一致的命名约定
- 将测试文件与源文件分开
- 按类型组织资源（图像、字符串、配置）

**构建效率**
- 仅将文件添加到正确的目标
- 不要将不必要的文件添加到编译源
- 保持头文件搜索路径最小化
- 对大型依赖项集使用预编译头文件

## 脚本参考

### add_files_to_xcode.py

**目的**：自动检测并添加新源文件到 Xcode 项目

**特性**：
- 扫描项目目录查找未跟踪的文件
- 识别文件类型（Swift、Objective-C、资源）
- 为项目引用生成正确的 UUID
- 将文件添加到适当的构建阶段
- 维护项目文件完整性
- 支持多个目标
- 支持干运行模式进行安全测试

**要求**：
- Python 3.7+
- 位于 `scripts/`（相对于技能目录）
- Xcode 项目必须有 `.xcodeproj` 文件

**配置**：
脚本自动检测：
- 项目文件位置
- 主目标名称
- 源目录
- 构建阶段映射

**退出代码**：
- 0: 成功
- 1: 未找到项目文件
- 2: 无效的项目结构
- 3: 没有要添加的文件

## 与 AI 工作流程集成

### 当 AI 创建新文件时

1. **检测阶段**
   - AI 创建新的 Swift/Objective-C 文件
   - 文件保存到文件系统
   - 文件尚未在 Xcode 项目中

2. **自动添加阶段**
   ```bash
   # 从项目根目录运行
   python3 scripts/add_files_to_xcode.py
   ```

3. **验证阶段**
   - 检查项目是否成功构建
   - 验证文件是否出现在 Xcode 导航器中
   - 确认目标成员资格正确

### 多文件功能

当 AI 实现需要多个文件的功能时：

```bash
# AI 创建后：UserService.swift, UserViewModel.swift, UserView.swift
cd /path/to/project
python3 scripts/add_files_to_xcode.py --files Sources/UserService.swift Sources/UserViewModel.swift Sources/UserView.swift

# 或者一次性添加所有
python3 scripts/add_files_to_xcode.py
```

## 故障排除

### 运行脚本后项目无法打开
1. 从备份或 git 恢复
2. 使用 `--dry-run` 运行脚本以检查它会做什么
3. 使用 `plutil -lint project.pbxproj` 验证项目文件语法

### 文件未出现在 Xcode 中
1. 关闭并重新打开 Xcode
2. 检查文件是否在 `.pbxproj` 中的正确组中
3. 验证 UUID 是唯一的
4. 确保文件路径正确

### 添加文件后出现构建错误
1. 检查目标成员资格是否正确
2. 验证 import 语句是否正确
3. 确保文件在正确的构建阶段
4. 检查是否有重复的文件条目

## 命令参考

```bash
# 添加所有未跟踪的文件
python3 scripts/add_files_to_xcode.py

# 添加特定文件
python3 scripts/add_files_to_xcode.py --files path/to/file1.swift path/to/file2.swift

# 预览而不应用
python3 scripts/add_files_to_xcode.py --dry-run

# 添加到特定目标
python3 scripts/add_files_to_xcode.py --target MyTarget

# 详细输出
python3 scripts/add_files_to_xcode.py --verbose

# 查找项目文件位置
find . -name "*.xcodeproj" -type d

# 列出不在项目中的文件
comm -23 <(find . -name "*.swift" | sort) <(grep -o '"[^"]*\.swift"' *.xcodeproj/project.pbxproj | sort -u)
```

## macOS 和跨平台注意事项

**文件路径**
- 在项目引用中使用正斜杠
- 正确处理文件名中的空格
- 使用相对于项目根目录的路径

**行结束符**
- 在 `.pbxproj` 中维护 Unix 行结束符 (LF)
- 保留现有文件编码

**Xcode 版本**
- 与 Xcode 12+ 兼容
- 处理传统和现代构建系统
- 支持 Swift 5+ 和 Objective-C 项目

## 高级主题

### 自定义构建阶段
- 为代码生成添加运行脚本阶段
- 管理资源的复制文件阶段
- 配置头文件可见性（public/private/project）

### 框架开发
- 管理伞形头文件
- 配置模块映射
- 设置框架版本控制

### 应用扩展
- 正确添加扩展目标
- 配置应用组和权限
- 管理应用和扩展之间的共享代码

## 总结

此技能实现了 AI 生成的代码与 Xcode 项目之间的无缝集成。通过自动化将文件添加到 Xcode 项目这一繁琐任务，开发人员可以专注于编写代码，而提供的脚本则处理项目管理。当 AI 创建新文件时，始终使用 `add_files_to_xcode.py` 脚本，并遵循项目组织和安全的最佳实践。
