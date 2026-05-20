---
name: arcanea-architect
description: Expert guidance for building the Arcanea creative agent ecosystem with attention to detail, design excellence, and systematic implementation.
version: 1.0.0
author: Arcanea Team
emoji: 🏗️
tags: [architecture, system-design, agents, implementation]
---

# Arcanea Architect Skill

## Purpose

This skill guides the design and implementation of the Arcanea ecosystem—the 64-agent creative intelligence system with multi-platform integration.

## When to Use

- Designing agent architectures
- Implementing orchestration systems
- Creating multi-platform integrations
- Building creative AI tools
- Establishing systematic workflows

## Core Principles

### 1. Excellence in Design
- Every component must have clear purpose
- Architecture should be elegant, not clever
- User experience is paramount
- Code quality matters (tested, documented, maintainable)

### 2. Attention to Detail
- No shortcuts in critical paths
- Validate all assumptions
- Document reasoning for decisions
- Test everything

### 3. Systematic Implementation
- Build foundation first, features second
- Integration over isolation
- Progressive enhancement
- Backward compatibility when possible

## Architecture Patterns

### Agent Registry Pattern
```typescript
// Centralized agent definitions
interface Agent {
  id: string;           // Unique identifier
  name: string;         // Display name
  court: string;        // Elemental court
  frequency: string;    // Operating frequency
  specialty: string;    // What they do best
  skills: string[];     // Available skills
  prompts: Template[];  // Invocation templates
}
```

### Conductor Pattern
```typescript
// Multi-agent orchestration
class Conductor {
  async orchestrate(task: Task): Promise<Result> {
    // 1. Analyze task complexity
    // 2. Select optimal agent team
    // 3. Determine execution strategy
    // 4. Execute with monitoring
    // 5. Learn from results
  }
}
```

### Skill Pattern
```typescript
// Capability definitions
interface Skill {
  id: string;
  gate: number;         // Which gate (1-10)
  frequency: string;    // Associated frequency
  invocation: string;   // How to trigger
  process: Step[];      // Step-by-step procedure
  agents: string[];     // Which agents can use
}
```

## Implementation Checklist

### Phase 1: Foundation
- [ ] Agent registry (64 agents defined)
- [ ] Core conductor (orchestration engine)
- [ ] Skill system (50+ skills)
- [ ] AI router (opencode + Claude BYOK)
- [ ] Documentation architecture

### Phase 2: Integration
- [ ] .claude/CLAUDE.md (Claude Code)
- [ ] .opencode/ skills (opencode editor)
- [ ] Tauri desktop app
- [ ] VS Code extension
- [ ] Obsidian plugin

### Phase 3: Polish
- [ ] UI/UX refinement
- [ ] Performance optimization
- [ ] Error handling
- [ ] User onboarding
- [ ] Testing & validation

## Design Decisions

### Why 64 Agents?
**Decision:** Use I Ching structure (8×8 = 64)
**Reasoning:** 
- Complete symbolic system
- Sacred geometry (8 = cosmic order)
- Manageable yet comprehensive
- Each can spawn sub-agents

### Why Ten Gates?
**Decision:** Solfeggio frequency scale (174-1111Hz)
**Reasoning:**
- Historical resonance
- Metaphorical value
- Organizational clarity
- Memorable categorization

### Why Hybrid AI?
**Decision:** opencode primary + Claude BYOK
**Reasoning:**
- Local-first (privacy, speed)
- Cost efficiency (free tier for most tasks)
- No vendor lock-in
- User control

### Why Tauri Desktop?
**Decision:** Tauri over Electron
**Reasoning:**
- Smaller bundle (600KB vs 100MB)
- Rust performance
- Native OS integration
- Better security

## Quality Standards

### Code Quality
- TypeScript strict mode
- Comprehensive error handling
- Unit tests for core logic
- Integration tests for workflows
- Documentation for all public APIs

### User Experience
- Sub-500ms response times
- Clear error messages
- Progressive disclosure
- Offline capability
- Consistent cross-platform UI

### Performance
- LRU caching for AI responses
- Lazy loading for agents
- Debounced UI updates
- Optimized renders
- Memory management

## Resources

### Documentation
- `AGENT_ARCHITECTURE_v4.md` - Why 64 agents
- `IMPLEMENTATION_ARCHITECTURE.md` - How it fits
- `BYOK_SAAS_ARCHITECTURE.md` - AI integration
- `SKILL_ARCHITECTURE_ANALYSIS.md` - Skills system

### Code
- `arcanea-agents/` - Agent registry and conductor
- `desktop/` - Tauri desktop application
- `.claude/` - Claude Code integration
- `.opencode/` - opencode editor integration

### Templates
- Use `SKILL.md` template for new skills
- Use agent template for new agents
- Use component templates for UI

## Anti-Patterns to Avoid

❌ **Don't:** Create agents without clear purpose
✅ **Do:** Every agent solves specific problems

❌ **Don't:** Use frequencies as acoustic prescriptions
✅ **Do:** Use as metaphorical categories

❌ **Don't:** Build features before foundation
✅ **Do:** Foundation first, features second

❌ **Don't:** Lock users into specific AI provider
✅ **Do:** Support multiple providers (BYOK)

❌ **Don't:** Over-engineer simple solutions
✅ **Do:** Elegant simplicity

## Success Metrics

- **Technical:** 100% test pass rate, <500ms response time
- **User:** Can complete tasks without documentation
- **Adoption:** Daily active users, retention rate
- **Satisfaction:** User feedback, feature requests

## Conclusion

Building Arcanea requires:
1. **Vision** - Clear understanding of what we're building
2. **Discipline** - Following architecture, not shortcuts
3. **Craft** - Attention to every detail
4. **Iteration** - Build, test, refine, repeat

The foundation determines the height. Build it well.

---

*This skill should be used whenever implementing or extending the Arcanea ecosystem.*
