---
name: project-overview
description: 项目背景知识，自动加载，不可手动调用。
---

# CaCrFeedFormula 项目概览

## 项目简介
**饲料配方优化系统** - Tauri + Rust + React TypeScript 桌面应用

## 核心技术栈

### 后端 (Rust 2021)
- Tauri 2.9.0 + Tokio 1.37（异步运行时）
- SQLite + SQLx 0.7（编译时类型安全）
- HiGHS 1.12（工业级线性规划求解器）
- Moka 0.12（高性能缓存）
- specta 2.0 + tauri-specta 2.0（自动类型生成）
- Rayon 1.8（并行计算）

### 前端 (React 19.1 + TypeScript 5.8)
- Ant Design 5.26 + Tailwind CSS 4.1
- TanStack Query 5.17（状态管理）
- Vite 7.0（构建工具）
- Recharts 2.15（可视化）

## 项目结构
```
src/                    # Rust 后端
├── ai/                 # AI 服务
├── formula/            # 配方优化核心
├── material/           # 原料管理
├── species/            # 品种管理
├── premix/             # 预混料设计
├── profit/             # 盈亏测算
├── prediction/         # 营养预测
└── production_batch/   # 生产批次管理

frontend/               # React 前端
└── src/
    ├── components/     # React 组件
    └── bindings.ts     # 自动生成的类型绑定
```

## 核心功能
1. **配方优化系统**：线性规划优化、手工配方设计、预混料反向计算
2. **数据管理**：原料、品种、工厂、生产批次、库存管理
3. **分析决策**：盈亏测算、营养预测、敏感性分析
4. **AI 助手**：流式响应、多轮对话、支持多平台

## 项目特点
- **桌面应用**：非 Web 应用，跨平台桌面应用
- **高性能计算**：Rust 后端保证速度和稳定性
- **类型安全**：specta 自动生成 TypeScript 类型
- **异步优先**：全面使用 Tokio 异步运行时
- **工业级优化**：HiGHS 求解器支持大规模配方优化
- **167 个 Tauri 命令**：覆盖 10 个模块

## 开发场景
- **配方引擎**：实现复杂线性规划算法
- **原料数据库**：管理大规模数据集
- **桌面 UI**：构建响应式 Ant Design 界面
- **Tauri 命令**：创建类型安全的 Rust ↔ TypeScript 通信
- **AI 功能**：集成流式 AI 响应
- **批次处理**：处理生产批次计算和调度

## 关键集成点
- **Rust ↔ TypeScript**：specta 生成 bindings.ts
- **数据库 ↔ 业务逻辑**：SQLx 宏提供编译时 SQL 验证
- **前端 ↔ 后端**：TanStack Query 管理服务器状态
- **AI ↔ 用户**：流式 SSE 响应实时更新 UI

## 开发规范
详见 `.claude/rules/` 目录：
- 02-rust-backend-standards.md
- 03-react-frontend-standards.md
- 04-database-standards.md
- 05-lsp-usage-standards.md
- 06-security-standards.md
- 07-testing-standards.md
- 08-performance-standards.md