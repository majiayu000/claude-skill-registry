---
name: vibe-orchestrator
description: Take a simple description and orchestrate multiple skills/agents to build
  a complete, production-ready application.
---

# ✨ Vibe Orchestrator Skill

---
name: vibe-orchestrator
description: Transform natural language descriptions into complete, working applications through AI orchestration
---

## 🎯 Purpose

Take a simple description and orchestrate multiple skills/agents to build a complete, production-ready application.

## 📋 When to Use

- "Build me a [type of app]"
- "Create a [description] system"
- Rapid prototyping from ideas
- MVP development

## 🔧 Orchestration Flow

```
User: "Create an e-commerce store"
              │
              ▼
┌─────────────────────────────────────────────────┐
│                VIBE ORCHESTRATOR                 │
└─────────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┬─────────┬─────────┐
    ▼         ▼         ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│ Plan  │ │  UI   │ │  Dev  │ │ Test  │ │Deploy │
│ Agent │ │ Agent │ │ Agent │ │ Agent │ │ Agent │
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘
              │
              ▼
        Working App! 🎉
```

## 📝 Vibe Process

### Phase 1: Understand (📐 Plan)
```markdown
Input: "Create a coffee shop ordering system"

Analysis:
- Domain: Food & Beverage / Ordering
- Users: Customers, Staff
- Core Features:
  - [ ] Menu display
  - [ ] Cart management
  - [ ] Order placement
  - [ ] Order tracking
- Tech Stack: React + Node.js + DB
```

### Phase 2: Design (🎨 UI)
```markdown
Pages to create:
1. Home - Menu display
2. Cart - Order items
3. Checkout - Payment
4. Orders - Track orders

Components:
- MenuCard
- CartItem
- OrderSummary
- Header/Footer
```

### Phase 3: Build (⚙️ Dev)
```markdown
Implementation order:
1. Project setup (Vite + React)
2. Create components
3. Add routing
4. Connect state management
5. Add API integration
```

### Phase 4: Test (🧪 Test)
```markdown
Testing:
1. Component tests
2. Integration tests
3. E2E flow tests
4. Mobile responsiveness
```

### Phase 5: Polish (✨ Design)
```markdown
Final touches:
1. Animations
2. Loading states
3. Error handling
4. Performance optimization
```

### Phase 6: Ship (🚀 Deploy)
```markdown
Deployment:
1. Build production bundle
2. Run final tests
3. Deploy to hosting
4. Verify live site
```

## 🎯 Vibe Commands

| Command | Action |
|---------|--------|
| `/vibe [description]` | Create full app |
| `/vibe-ui [description]` | UI only |
| `/vibe-api [description]` | API only |
| `/vibe-fix [issue]` | Fix and continue |

## 📊 Agent Coordination

### Parallel Execution
```
Phase 1: Planning (sequential - needed for others)
    │
    ▼
Phase 2: UI + API (parallel - independent)
    │
    ▼
Phase 3: Integration (sequential - needs both)
    │
    ▼
Phase 4: Testing + Docs (parallel - independent)
```

### Agent Announcements
```
[📐 Planner] Starting: Analyze requirements
[📐 Planner] ✅ Complete: 5 features identified

[🎨 UI Builder] Starting: Create HomePage
[⚙️ Dev Agent] Starting: Setup API routes
[🎨 UI Builder] ✅ Complete: HomePage with 3 sections
[⚙️ Dev Agent] ✅ Complete: 4 API endpoints

[🧪 Tester] Starting: Run test suite
[🧪 Tester] ✅ Complete: 12/12 tests passed
```

## 💡 Example Vibes

### E-commerce
```
/vibe Online store with products, cart, and checkout
```

### SaaS Dashboard
```
/vibe Analytics dashboard with charts, filters, and export
```

### Social App
```
/vibe Twitter clone with posts, likes, and comments
```

### Management System
```
/vibe Project management tool with tasks, teams, and deadlines
```

## ✅ Vibe Checklist

- [ ] Requirements understood
- [ ] Features prioritized
- [ ] UI designed and built
- [ ] Logic implemented
- [ ] Tests passing
- [ ] Design polished
- [ ] Ready for deployment

## 🔧 Error Recovery

```markdown
If agent fails:
1. Identify failure point
2. Log error details
3. Attempt auto-fix
4. If can't fix: pause and report
5. After fix: continue from checkpoint
```

## 🔗 Related Skills

- `business-context` - Understand requirements
- `ui-first-builder` - Build UI
- `testing` - Test application
- `deployment` - Deploy result
- `memory-system` - Track progress
