---
source: ../../../../skills/project-structure-guide/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2025-12-30
status: current
---

# 项目结构指南

> **Language**: [English](../../../../skills/project-structure-guide/SKILL.md) | 简体中文

**版本**：1.0.0
**最後更新**：2025-12-30
**適用性**：Claude Code Skills

---

## 目的

此技能提供根据语言和框架慣例建構项目的指引，協助建立一致、可維護的目录佈局。

## 觸發时机

在以下情况使用此技能：
- 建立新项目
- 重組現有项目结构
- 新增模組或功能
- 设置建構配置
- 建立 .gitignore 文件

## 支援的语言

| 语言 | 框架/模式 |
|------|-----------|
| Node.js | Express、NestJS、Next.js |
| Python | Django、Flask、FastAPI |
| Java | Spring Boot、Maven、Gradle |
| .NET | ASP.NET Core、Console |
| Go | 标准佈局、cmd/pkg |
| Rust | Binary、Library、Workspace |
| Kotlin | Gradle、Android、Multiplatform |
| PHP | Laravel、Symfony、PSR-4 |
| Ruby | Rails、Gem、Sinatra |
| Swift | SPM、iOS App、Vapor |

## 常見结构模式

### 标准目录

```
project-root/
├── src/              # 原始码
├── tests/            # 测试文件
├── docs/             # 文件
├── tools/            # 建構/部署脚本
├── examples/         # 使用範例
├── config/           # 配置文件
└── .github/          # GitHub 配置
```

### 建構输出（始終 gitignore）

```
dist/                 # 發佈输出
build/                # 编譯产物
out/                  # 输出目录
bin/                  # 二进位执行檔
```

## 语言特定指南

### Node.js

```
project/
├── src/
│   ├── index.js
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   └── models/
├── tests/
├── package.json
└── .gitignore
```

### Python

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       └── main.py
├── tests/
├── pyproject.toml
└── .gitignore
```

### Go

```
project/
├── cmd/
│   └── appname/
│       └── main.go
├── internal/
├── pkg/
├── go.mod
└── .gitignore
```

## 快速操作

### 建立项目结构

當被要求建立项目时：
1. 詢問语言/框架
2. 生成適當的目录结构
3. 建立必要的配置文件
4. 生成 .gitignore

### 审查结构

审查現有结构时：
1. 检查语言慣例
2. 验证 gitignore 模式
3. 建议改进
4. 識别放錯位置的文件

## 規則

1. **遵循语言慣例** - 每种语言都有既定模式
2. **分離关注点** - 將原始码、测试、文件分開
3. **Gitignore 建構输出** - 永不提交 dist/、build/、out/
4. **一致命名** - 使用语言適當的命名風格
5. **配置在根目录** - 將配置文件放在项目根目录

## 相关标准

- [核心：项目结构](../../core/project-structure.md)
- [AI：项目结构选项](../../ai/options/project-structure/)
