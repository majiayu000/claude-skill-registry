---
name: genesis
description: 太初有道，道生代码。从零搭建 React19+TailwindV4+Vite 前端、FastAPI Python 后端、Go Gin 后端、Taro 4.x 小程序。用户说"新建项目"、"初始化"、"从零开始"、"搭建项目"、"创建项目"、"生成落地页"、"生成官网"、"生成 Landing Page"、"动画提升"、"动效升级"、"新建小程序"、"创建小程序"、"Taro 项目"时触发。
---

# Genesis

> 太初有道，道生代码

---

## 首要决策：初始化模式

**在开始前，必须询问用户选择初始化模式：**

| 模式            | 说明                               | 适用场景                       |
| --------------- | ---------------------------------- | ------------------------------ |
| **A. 模板复制** | 直接复制 `templates/` 下的现成项目 | 快速启动、标准项目、不需要定制 |
| **B. AI 生成**  | 根据 `references/` 文档从零构建    | 深度定制、学习过程、特殊需求   |

**询问话术**：

> 请选择初始化模式：
>
> - **A 模板复制**：秒级启动，复制现成模板
> - **B AI 生成**：逐步构建，可深度定制
>
> 输入 A 或 B：

---

## 决策流程

```
用户触发 "新建项目"
    ↓
确认项目类型 → Web 前端 / Python 后端 / Go 后端 / Taro 小程序
    ↓
确认项目名称和目标目录
    ↓
询问初始化模式 → A 模板复制 / B AI 生成
    ↓
A: 复制模板 → 改名 → 安装依赖 → 完成
B: 读取 references → 逐步执行 → 完成
```

---

## 前端初始化（React + 设计系统）

**触发词**：创建 React 项目、新建前端项目、Web 应用、H5 项目

**技术栈**：React 19 + Vite + TailwindCSS V4 + shadcn/ui

### 模式 A：模板复制（秒级完成）

**直接执行，无需确认**：

```bash
cp -r ~/.claude/skills/genesis/templates/web-react {目标目录}
cd {目标目录} && sed -i '' 's/"name": "web-react"/"name": "{项目名}"/g' package.json
npm install && npm run dev
```

**模板已包含**：Vite + React 19 + TailwindCSS V4 + shadcn/ui + 微拟物光影

### 模式 B：AI 生成

**执行顺序**：

1. 读取 [web-react.md](references/web-react.md) → 搭建 Vite + React + Tailwind 环境
2. 读取 [design-system.md](references/design-system.md) → 集成 shadcn/ui 组件库
3. 读取 [design-enhance.md](references/design-enhance.md) → 应用微拟物光影质感

---

## Python 后端初始化（FastAPI）

**触发词**：Python 后端、FastAPI、新建 API、初始化 Python 项目、创建 Python 项目

**技术栈**：FastAPI + UV + SQLModel + AsyncPG

### 模式 A：模板复制（秒级完成）

**直接执行，无需确认**：

```bash
cp -r ~/.claude/skills/genesis/templates/backend-python {目标目录}
cd {目标目录} && sed -i '' 's/name = "backend-python"/name = "{项目名}"/g' pyproject.toml
uv sync && ./local-run.sh
```

**模板已包含**：FastAPI + UV + SQLModel + AsyncPG + 统一响应格式

### 模式 B：AI 生成

**参考文档**：[backend-python.md](references/backend-python.md)

按文档逐步执行：环境初始化 → 目录结构 → 核心模块 → 路由配置

---

## Taro 小程序初始化（React + Tailwind）

**触发词**：新建小程序、创建小程序、Taro 项目、小程序开发、跨端小程序

**技术栈**：Taro 4.x + React 18 + TailwindCSS V4 + weapp-tailwindcss

### 模式 A：模板复制（秒级完成）

**直接执行，无需确认**：

```bash
cp -r ~/.claude/skills/genesis/templates/miniapp {目标目录}
cd {目标目录}
sed -i '' 's/"name": "mini0app"/"name": "{项目名}"/g' package.json
sed -i '' 's/projectName: '\''mini0app'\''/projectName: '\''${项目名}'\''/g' config/index.js
npm install && npm run dev:weapp
```

**模板已包含**：Taro 4.x + React + TailwindCSS V4 + weapp-tailwindcss + tweakcn 主题 + 跨端配置

### 模式 B：AI 生成

**参考文档**：[taro-miniapp.md](references/taro-miniapp.md)

按文档逐步执行：Taro CLI 初始化 → Tailwind 集成 → weapp-tailwindcss 配置 → tweakcn 主题集成 → 多端适配

**支持平台**：

- 微信小程序 (`npm run dev:weapp`)
- 支付宝小程序 (`npm run dev:alipay`)
- 抖音小程序 (`npm run dev:tt`)
- H5 (`npm run dev:h5`)

---

## Go 后端初始化（Gin）

**触发词**：Go 后端、Gin、Go API、初始化 Go 项目、创建 Go 项目

**技术栈**：Go + Gin + GORM + Viper

### 模式 A：模板复制（秒级完成）

**直接执行，无需确认**：

```bash
cp -r ~/.claude/skills/genesis/templates/backend-go {目标目录}
cd {目标目录}
# 替换模块名（go.mod + 所有 import）
find . -type f -name "*.go" -exec sed -i '' 's|backend-go|{项目名}|g' {} +
sed -i '' 's|module backend-go|module {项目名}|g' go.mod
go mod tidy && go run cmd/api/main.go
```

**模板已包含**：Gin + GORM + Viper + 标准目录结构 + 中间件

### 模式 B：AI 生成

**参考文档**：[backend-go.md](references/backend-go.md)

按文档逐步执行：go mod init → 目录结构 → 核心模块 → 路由配置

---

## 动画提升（React 项目）

**触发词**：动画提升、Apple 动效、添加动画、动效升级

**前置条件**：已完成前端初始化 + 页面内容搭建

**参考文档**：[design-motion.md](references/design-motion.md)

**执行内容**：

- 为现有 React 项目添加 Framer Motion 动画
- Apple 级 Spring 物理引擎
- 页面路由过渡、组件交互动效

---

## Landing Page 生成（React 项目）

**触发词**：生成落地页、生成 Landing Page、生成官网首页、生成产品页、做一个落地页

**前置条件**：已完成前端初始化

**参考文档**：[landing-page.md](references/landing-page.md)

**执行内容**：

- 一次性生成生产级落地页
- 10 个标准 Section 组件
- 遵循设计系统约束
- Framer Motion 入场动画
- 响应式 + 可访问性

---

## 通用原则

### 模式选择建议

| 场景                     | 推荐模式   |
| ------------------------ | ---------- |
| 快速原型、标准项目       | A 模板复制 |
| 学习技术栈、理解构建过程 | B AI 生成  |
| 需要深度定制、非标准配置 | B AI 生成  |
| 团队统一模板、批量创建   | A 模板复制 |

### 初始化检查清单

- [ ] 确认项目类型
- [ ] 确认项目名称（小写+连字符）
- [ ] 确认目标目录
- [ ] 确认初始化模式（A/B）
- [ ] 安装依赖并验证运行

---

## 交互规范

1. **必须询问模式**：A 模板复制 or B AI 生成
2. **验证运行**：确保项目能正常启动
3. **模板自带文档**：L1/L2/L3 分形文档已内置于模板中，无需额外构建
