---
name: cross-platform-command-generator
description: Generates cross-platform commands and scripts for Linux, macOS, and Windows with security validation and compatibility guidance
---

# Cross-Platform Command Generator

这个技能为 DevOps、系统运维、软件开发自动化和安全运维提供跨平台命令行和脚本生成能力,支持自然语言描述转换为可执行命令,并提供安全性检查和危险命令预警。

## Capabilities

- **自然语言命令生成**: 根据用户描述生成适用于多操作系统的命令行
  - Linux/Unix (Bash/Zsh)
  - macOS (Bash/Zsh)
  - Windows (PowerShell/CMD)

- **脚本文件生成**: 创建完整的跨平台脚本文件
  - `.sh` - Shell 脚本 (Linux/macOS)
  - `.ps1` - PowerShell 脚本 (Windows)
  - `.bat`/`.cmd` - 批处理脚本 (Windows)

- **安全性检查**: 危险命令检测和风险评估
  - 权限提升命令识别 (sudo, runas)
  - 破坏性操作警告 (rm -rf, format, del /f)
  - 网络安全风险评估

- **兼容性分析**: 提供跨平台兼容性建议
  - 平台特定命令差异
  - 替代命令推荐
  - 依赖项检查

- **参数验证**: 命令参数合法性检查和错误处理

## Input Requirements

用户提供以下信息:

### 命令生成模式
- **任务描述**: 自然语言描述要执行的操作 (例如: "列出当前目录下所有文件的详细信息")
- **目标平台**: 选择一个或多个目标操作系统 (Linux/macOS/Windows)
- **安全级别**: 可选,指定是否允许需要提升权限的命令 (默认: false)
- **输出格式**: 命令行 (单条命令) 或脚本文件 (完整脚本)

### 脚本生成模式
- **脚本用途**: 描述脚本的功能和目标
- **目标平台**: 选择生成哪些平台的脚本
- **功能模块**: 列出脚本需要包含的功能 (例如: 参数解析、日志记录、错误处理)
- **安全要求**: 是否需要输入验证、权限检查、危险操作确认

输入格式支持:
- JSON 结构化输入
- 自然语言文本描述
- 混合模式 (部分结构化 + 自然语言)

## Output Formats

### 命令行输出
```json
{
  "task_description": "原始任务描述",
  "platforms": {
    "linux": {
      "command": "生成的 Linux 命令",
      "description": "命令说明",
      "requires_sudo": false,
      "safety_level": "safe"
    },
    "macos": {
      "command": "生成的 macOS 命令",
      "description": "命令说明",
      "requires_sudo": false,
      "safety_level": "safe"
    },
    "windows": {
      "powershell": "PowerShell 命令",
      "cmd": "CMD 命令",
      "description": "命令说明",
      "requires_admin": false,
      "safety_level": "safe"
    }
  },
  "compatibility_notes": [
    "跨平台兼容性说明"
  ],
  "security_warnings": [
    "安全风险提示 (如有)"
  ]
}
```

### 脚本文件输出
生成的脚本文件包含:
- 脚本头部 (shebang, 版权信息, 用途说明)
- 参数解析逻辑
- 输入验证
- 核心功能实现
- 错误处理和日志记录
- 使用示例和帮助信息

文件清单:
- `script_linux.sh` - Linux/Unix Shell 脚本
- `script_macos.sh` - macOS Shell 脚本
- `script_windows.ps1` - Windows PowerShell 脚本
- `script_windows.bat` - Windows 批处理脚本
- `README.md` - 脚本使用说明

## How to Use

### 命令生成示例

**基础用例**:
```
@cross-platform-command-generator

生成跨平台命令: 查找当前目录下所有大于 100MB 的文件
目标平台: Linux, macOS, Windows
```

**安全运维用例**:
```
@cross-platform-command-generator

生成命令: 检查系统中所有监听端口和对应的进程
目标平台: 所有平台
安全级别: 需要管理员权限
```

### 脚本生成示例

**自动化部署脚本**:
```
@cross-platform-command-generator

生成部署脚本:
- 功能: 自动化应用部署
- 平台: Linux, Windows
- 包含: 参数解析、环境检查、备份机制、回滚功能、日志记录
- 安全: 需要权限检查和危险操作确认
```

**系统健康检查脚本**:
```
@cross-platform-command-generator

生成健康检查脚本:
- 检查 CPU/内存/磁盘使用率
- 检查关键服务运行状态
- 生成报告并发送邮件通知
- 平台: Linux, macOS, Windows
```

## Scripts

### command_generator.py
核心命令生成引擎,包含:
- `PlatformCommandGenerator` 类: 根据任务描述生成特定平台命令
- `cross_platform_translate()`: 自然语言到命令的转换逻辑
- 平台命令映射表 (Linux/macOS/Windows 常用命令对照)

### security_validator.py
安全检查模块,包含:
- `SecurityValidator` 类: 命令安全性验证
- `check_dangerous_commands()`: 危险命令检测
- `assess_risk_level()`: 风险等级评估 (safe/warning/dangerous)
- `privilege_required()`: 权限需求检查

### script_builder.py
脚本文件生成器,包含:
- `ScriptBuilder` 类: 多平台脚本构建
- `generate_bash_script()`: 生成 Shell 脚本
- `generate_powershell_script()`: 生成 PowerShell 脚本
- `generate_batch_script()`: 生成批处理脚本
- 脚本模板管理

### compatibility_checker.py
兼容性分析器,包含:
- `CompatibilityChecker` 类: 跨平台兼容性检查
- `find_equivalent_commands()`: 查找等效命令
- `suggest_alternatives()`: 推荐替代方案
- 平台特性差异数据库

## Best Practices

### 1. 安全优先原则
- 始终检查生成的命令是否包含危险操作
- 对需要提升权限的命令进行明确标注
- 在执行破坏性操作前添加确认机制
- 避免在脚本中硬编码敏感信息 (密码、密钥)

### 2. 兼容性验证
- 生成命令前验证目标平台是否支持所需功能
- 提供跨平台差异的详细说明
- 推荐使用跨平台工具 (如 Python, Node.js) 替代平台特定命令
- 测试生成的命令在目标平台上的实际执行效果

### 3. 参数和错误处理
- 对用户输入进行严格验证
- 在脚本中包含完善的错误处理逻辑
- 提供清晰的错误消息和调试信息
- 实现优雅的失败回退机制

### 4. 文档和可维护性
- 为生成的脚本添加详细注释
- 包含使用示例和帮助信息
- 遵循平台特定的脚本编写规范
- 使用版本控制管理脚本文件

### 5. 性能和效率
- 优先使用系统原生命令
- 避免不必要的外部依赖
- 对资源密集型操作提供进度反馈
- 考虑命令执行的性能影响

## Limitations

### 技术限制
- **平台差异**: 某些高级功能可能无法在所有平台上完全等效实现
- **命令版本**: 不同操作系统版本的命令语法可能存在差异
- **依赖项**: 生成的命令可能依赖特定工具或软件的安装
- **权限控制**: 某些操作需要管理员/root 权限,无法在受限环境中执行

### 安全限制
- **静态分析**: 安全检查基于已知危险模式,无法识别所有潜在风险
- **上下文依赖**: 某些命令的安全性取决于具体执行环境和参数
- **第三方工具**: 对第三方工具的安全性不做保证

### 使用场景限制
- **不适用于**: 高度定制化的系统配置、复杂的企业级部署流程
- **需要人工审核**: 生产环境部署前应由专业人员审核生成的命令和脚本
- **测试环境优先**: 建议先在测试环境验证生成的命令

### 语言和本地化
- 主要支持英文命令和参数
- 部分平台特定工具可能需要额外的本地化配置
- 错误消息和日志输出语言取决于系统设置

## Industry Context

本技能特别适用于以下场景:

### DevOps / 系统运维
- 基础设施即代码 (IaC) 脚本生成
- 跨云平台自动化部署
- 系统监控和健康检查脚本
- 灾难恢复和备份自动化

### 软件开发 / 自动化
- CI/CD 流水线脚本
- 构建和测试自动化
- 环境配置和依赖安装
- 代码质量检查自动化

### 安全运维
- 安全审计脚本生成
- 漏洞扫描自动化
- 日志分析和威胁检测
- 合规性检查脚本

### 混合云和多云环境
- 跨平台资源管理
- 统一的运维工具链
- 平台迁移和数据同步
- 多环境配置管理
