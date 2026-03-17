---
name: project-overview
description: Background knowledge about CaCrFeedFormula project architecture, features, and context. Automatically loaded for AI reference, not directly user-invocable.
version: 1.0.0
user-invocable: false
---

# CaCrFeedFormula Project Overview

**Intelligent Feed Formula Optimization System** built with Tauri + Rust + React TypeScript.

## Project Context

**CaCrFeedFormula** is an industrial-grade desktop application for feed formula optimization, integrating AI-assisted optimization, linear programming (HiGHS solver), and comprehensive feed management capabilities.

### Core Technology Stack

**Backend (Rust 2021)**:
- **Framework**: Tauri 2.9.0 + Tokio 1.37 (full async runtime)
- **Database**: SQLite + SQLx 0.7 (compile-time type safety)
- **Optimization**: HiGHS 1.12 (industrial-grade LP solver)
- **Caching**: Moka 0.12 (high-performance concurrent cache)
- **Type Binding**: specta 2.0 + tauri-specta 2.0 (auto TypeScript generation)
- **AI Integration**: reqwest + eventsource-stream (streaming responses)
- **Parallel Compute**: Rayon 1.8

**Frontend (React 19.1 + TypeScript 5.8)**:
- **UI Framework**: Ant Design 5.26 + Tailwind CSS 4.1
- **State Management**: TanStack Query 5.17
- **Build Tool**: Vite 7.0
- **Visualization**: Recharts 2.15
- **Animation**: Framer Motion 11

## Project Structure

```
cacrfeedformula/
├── src/                          # Rust backend source
│   ├── ai/                       # AI service module
│   ├── database/                 # Database connection
│   ├── formula/                  # Formula optimization core
│   ├── material/                 # Material management
│   ├── species/                  # Species management
│   ├── factory/                  # Factory management
│   ├── premix/                   # Premix design
│   ├── profit/                   # Profit/loss analysis
│   ├── prediction/               # Nutrition prediction
│   ├── production_batch/         # Production batch management
│   └── system/                   # System services
├── frontend/                     # React frontend source
│   └── src/
│       ├── components/           # React components
│       │   ├── AIChat/          # AI chat component
│       │   └── common/          # Common components
│       └── bindings.ts          # Auto-generated type bindings
├── migrations/                   # Database migrations
└── .claude/
    ├── skills/                   # Custom Claude Code skills
    └── rules/                    # Detailed development standards
```

## Core Features

### 1. Formula Optimization System
- Linear programming optimization (cost minimization)
- Manual formula design
- Premix reverse calculation design
- Formula version management
- Formula analysis and reporting
- **167 Tauri commands** for comprehensive formula operations

### 2. Data Management
- Material management (built-in China Feed Composition & Nutrition Value Database)
- Species management (multiple species, growth stages, nutrition standards)
- Factory management (multi-factory data isolation)
- Production batch management (batch lifecycle, material requirement calculation)
- Inventory management (stock check, variance analysis, purchase planning)

### 3. Analysis & Decision Support
- Profit/loss analysis (comprehensive cost accounting, real-time P&L)
- Nutrition prediction (NRC-based energy prediction)
- Sensitivity analysis (shadow prices, bottleneck constraint identification)

### 4. AI Intelligent Assistant
- Context-aware professional feed formula consultation
- Streaming responses with typewriter effect
- Multi-turn conversations
- Supports OpenAI, DeepSeek, OpenRouter platforms

## Project Characteristics

1. **Desktop Application**: Not a web app; cross-platform desktop app built with Tauri
2. **High-Performance Computing**: Rust backend ensures speed and stability
3. **Type Safety**: specta auto-generates TypeScript types, ensuring frontend-backend type consistency
4. **Async-First**: Comprehensive use of Tokio async runtime
5. **Industrial-Grade Optimization**: HiGHS solver supports large-scale formula optimization
6. **AI Integration**: Streaming AI responses with real-time typewriter effect

## Development Workflow Context

### Typical Development Scenarios:
- **Formula Engine**: Implementing complex linear programming algorithms with HiGHS
- **Material Database**: Managing large datasets with SQLite + SQLx
- **Desktop UI**: Building responsive Ant Design interfaces with React 19
- **Tauri Commands**: Creating type-safe Rust ↔ TypeScript communication
- **AI Features**: Integrating streaming AI responses into desktop workflows
- **Batch Processing**: Handling production batch calculations and scheduling

### Key Integration Points:
- **Rust ↔ TypeScript**: specta generates bindings.ts after every Rust change
- **Database ↔ Business Logic**: SQLx macros provide compile-time SQL validation
- **Frontend ↔ Backend**: TanStack Query manages server state via Tauri commands
- **AI ↔ User**: Streaming SSE responses with real-time UI updates

## Project Scale

- **167 Tauri commands** across 10 modules
- **Comprehensive feed database** with 1000+ materials
- **Multi-tenancy support** with factory-level data isolation
- **Complex optimization** handling 100+ variables and 50+ constraints

## Development Standards

The project follows strict development standards documented in `.claude/rules/`:
- Rust backend standards (02-rust-backend-standards.md)
- React frontend standards (03-react-frontend-standards.md)
- Database standards (04-database-standards.md)
- LSP usage standards (05-lsp-usage-standards.md)

All these standards are enforced via automated hooks and skills.

## When This Context Is Useful

This project overview is automatically loaded to help Claude understand:
- **Architecture decisions** when proposing changes
- **Technology choices** when solving problems
- **Integration patterns** when adding features
- **Scale considerations** when optimizing performance
- **Domain context** (feed formulation, nutrition, optimization)

This knowledge enables Claude to make more informed, project-appropriate recommendations without requiring repeated explanations of the project's nature and structure.
