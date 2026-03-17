---
name: project-overview
description: Background knowledge about WeReply project architecture, features, and context. Automatically loaded for AI reference, not directly user-invocable.
version: 1.0.0
user-invocable: false
---

# WeReply Project Overview

**微信回复建议助手** (WeChat Reply Suggestion Assistant) built with Tauri + Rust + React TypeScript.

## Project Context

**WeReply** is a desktop application that monitors WeChat conversations and provides AI-powered reply suggestions using DeepSeek API. The system consists of a Rust Orchestrator, Platform-specific Agents (Windows/macOS), and a React-based Assistant Panel.

### Core Technology Stack

**Backend (Rust 2021)**:
- **Framework**: Tauri 2.x + Tokio (full async runtime)
- **IPC Protocol**: JSON via stdin/stdout
- **AI Integration**: reqwest (DeepSeek API client)
- **Type Binding**: specta 2.0 + tauri-specta 2.0 (auto TypeScript generation)
- **Logging**: tracing + tracing-subscriber
- **Configuration**: System keychain (API key storage) + JSON (user config)

**Platform Agents**:
- **Windows**: Python 3.12 + wxauto v4 (UI Automation)
- **macOS**: Swift + Accessibility API
- **Communication**: JSON protocol via stdin/stdout

**Frontend (React 19.1 + TypeScript 5.8)**:
- **UI Framework**: Ant Design 5.26 + Tailwind CSS 4.1
- **State Management**: TanStack Query 5.17
- **Build Tool**: Vite 7.0
- **Window Management**: Tauri Window API (window following)

## Project Structure

```
wereply/
├── src/                          # Rust Orchestrator source
│   ├── wechat/                   # WeChat monitoring module
│   ├── ai/                       # DeepSeek API integration
│   ├── orchestrator/             # Core orchestration logic
│   ├── system/                   # System services
│   └── main.rs                   # Entry point
├── platform_agents/              # Platform-specific agents
│   ├── windows_agent/           # Windows Python agent
│   │   ├── wechat_monitor.py   # WeChat monitoring
│   │   └── input_writer.py     # Input box control
│   └── macos_agent/             # macOS Swift agent
│       ├── WeChatMonitor.swift  # WeChat monitoring
│       └── InputWriter.swift    # Input box control
├── frontend/                     # React frontend source
│   └── src/
│       ├── components/           # React components
│       │   ├── AssistantPanel/  # Main assistant panel
│       │   ├── SuggestionList/  # Suggestion display
│       │   └── ConfigDialog/    # Configuration UI
│       └── bindings.ts          # Auto-generated type bindings
└── .claude/
    ├── skills/                   # Custom Claude Code skills
    └── rules/                    # Detailed development standards
```

## System Architecture

### Data Flow Design

```
微信窗口
   ↓ (Accessibility API / UI Automation)
Platform Agent (Python/Swift)
   ↓ (JSON via stdin/stdout)
Rust Orchestrator
   ├→ DeepSeek API (HTTP)
   └→ React Frontend (Tauri IPC)
       ↓
   用户选择建议
       ↓
Rust Orchestrator
   ↓ (JSON via stdin/stdout)
Platform Agent
   ↓ (UI Automation)
微信输入框
```

### Key Components

1. **Platform Agent**: Monitors WeChat, extracts messages, writes to input box
2. **Rust Orchestrator**: Coordinates Agent and AI, manages state
3. **DeepSeek Service**: Generates reply suggestions via API
4. **Assistant Panel**: Displays suggestions, floats beside WeChat window

## Core Features

### 1. WeChat Message Monitoring
- Real-time message detection (Platform Agent)
- Context extraction (last N messages)
- Sender identification
- Message deduplication

### 2. AI Reply Suggestions
- DeepSeek API integration
- Context-aware suggestions
- Multiple reply styles (formal, friendly, humorous)
- Configurable suggestion count (1-5)

### 3. Assistant Panel
- Floating window beside WeChat
- Real-time suggestion display
- One-click reply insertion
- Window position following

### 4. IPC Communication
- JSON protocol between Rust and Agent
- Message types: MessageNew, InputWrite, HealthCheck
- Error handling and retry mechanism
- Graceful Agent crash recovery

## Project Characteristics

1. **Desktop Application**: Not a web app; cross-platform desktop app built with Tauri
2. **IPC Architecture**: Rust Orchestrator communicates with Platform Agents via JSON
3. **Type Safety**: specta auto-generates TypeScript types, ensuring frontend-backend type consistency
4. **Async-First**: Comprehensive use of Tokio async runtime
5. **Platform-Specific Agents**: Python (Windows) and Swift (macOS) for native automation
6. **AI-Powered**: DeepSeek API for intelligent reply generation
7. **Privacy-First**: No data persistence, API keys in system keychain

## Development Workflow Context

### Typical Development Scenarios:
- **WeChat Monitoring**: Implementing platform-specific automation with wxauto/Accessibility API
- **IPC Communication**: Designing JSON message protocols between Rust and Agents
- **DeepSeek Integration**: Managing HTTP connections, handling API errors and rate limits
- **Desktop UI**: Building floating panels with window follow feature
- **Tauri Commands**: Creating type-safe Rust ↔ TypeScript communication
- **Configuration**: Managing API keys via system keychain, user settings via JSON

### Key Integration Points:
- **Rust ↔ TypeScript**: specta generates bindings.ts after every Rust change
- **Rust ↔ Agent**: JSON protocol via stdin/stdout
- **Frontend ↔ Backend**: TanStack Query manages server state via Tauri commands
- **AI ↔ User**: DeepSeek API provides suggestions, user selects and sends

## Performance Targets

- **Message Listening**: < 500ms (Agent detection latency)
- **Agent Communication**: < 100ms (IPC round-trip)
- **DeepSeek API**: < 3s (suggestion generation)
- **UI Response**: < 100ms (user interaction to UI update)
- **Window Follow**: < 200ms (WeChat window move to panel update)
- **Startup Time**: < 2s (application launch to ready)

## Development Standards

The project follows strict development standards documented in `.claude/rules/`:
- Project overview (01-project-overview.md)
- Rust backend standards (02-rust-backend-standards.md)
- React frontend standards (03-react-frontend-standards.md)
- Configuration management (04-configuration-standards.md)
- LSP usage standards (05-lsp-usage-standards.md)
- Security standards (06-security-standards.md)
- Testing standards (07-testing-standards.md)
- Performance standards (08-performance-standards.md)

All these standards are enforced via automated hooks and skills.

## When This Context Is Useful

This project overview is automatically loaded to help Claude understand:
- **Architecture decisions** when proposing changes (e.g., IPC vs direct API)
- **Technology choices** when solving problems (e.g., platform-specific automation)
- **Integration patterns** when adding features (e.g., new Tauri commands)
- **Scale considerations** when optimizing performance (e.g., IPC batching)
- **Domain context** (WeChat automation, AI suggestions, desktop UX)

This knowledge enables Claude to make more informed, project-appropriate recommendations without requiring repeated explanations of the project's nature and structure.
