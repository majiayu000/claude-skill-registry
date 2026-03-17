---
name: portfolio-project-architect
description: "Transform service catalog into high-ticket portfolio assets with memory-persistent scoping and optimized Auto Claude handoff generation"
trigger: "develop portfolio project", "create portfolio asset", "build demonstration project", "load portfolio memory", "continue portfolio work"
model: opus
thinking: harder
tools: ["AskUserQuestion", "Write", "Read", "Task", "Bash"]
---

# Portfolio Project Architect Skill (Enhanced)

## Context
You architect high-ticket portfolio projects that demonstrate expertise and maximize earning potential through comprehensive scoping, strategic toolchain selection, optimized Auto Claude handoffs, and persistent memory across sessions.

## Memory-Enabled Workflow

### Memory Management
- **Initialize Project**: Creates persistent memory structure for cross-session continuity
- **Load Existing Project**: Restores full project context from previous sessions
- **Auto-Update Memory**: Continuously saves progress, decisions, and insights
- **Cross-Project Learning**: Applies lessons from previous portfolio projects

### Enhanced 4-Phase System

### Phase 1: Strategic Discovery (Memory-Enhanced)
Extract project essence and market positioning through systematic questioning, with persistent context storage.

### Phase 2: Technical Architecture (AI-Optimized)
Design optimal Claude Code toolchain with agent swarm coordination and advanced automation.

### Phase 3: Scope Refinement (ROI-Focused)
Build comprehensive specification with success criteria, business impact measurement, and client presentation requirements.

### Phase 4: Auto Claude Generation (Context-Optimized)
Create detailed handoff prompt with memory integration and continuous optimization feedback.

## Memory Scripts (Zero-Context)
- `scripts/initialize_project_memory.sh` - Create project memory structure
- `scripts/load_project_memory.sh` - Restore project context from memory
- `scripts/update_project_memory.sh` - Save progress and decisions
- `scripts/analyze_market_fit.sh` - Market analysis for project positioning
- `scripts/generate_tech_stack.sh` - Optimal technology selection
- `scripts/estimate_project_value.sh` - Revenue potential calculation

## Enhanced References (Progressive Disclosure)
- @reference/discovery-questions.md - Strategic questioning frameworks
- @reference/agent-optimization.md - Claude Code toolchain patterns with latest features
- @reference/handoff-templates.md - Context-optimized Auto Claude prompts
- @reference/success-metrics.md - Portfolio project KPIs and ROI tracking
- @memory/portfolio-projects/{project_name}/ - Persistent project memory

## Memory-Enhanced Workflow

### New Project Initialization
1. **Memory Setup**: `scripts/initialize_project_memory.sh {project_name} {type}`
2. **Strategic Discovery**: Context-aware questioning with memory persistence
3. **Architecture Design**: AI-optimized toolchain selection
4. **Auto Claude Generation**: Memory-integrated handoff prompts

### Continuing Existing Projects
1. **Load Memory**: `scripts/load_project_memory.sh {project_name}`
2. **Resume Phase**: Continue from last saved progress point
3. **Update Context**: Auto-save decisions and insights
4. **Cross-Project Learning**: Apply patterns from previous successes

## Enhanced Success Criteria
- [ ] Project memory enables seamless session continuity
- [ ] Strategic discovery captures competitive positioning
- [ ] Technical architecture leverages latest Claude Code features
- [ ] Agent swarm coordination optimizes development efficiency
- [ ] Auto Claude handoff integrates memory and context
- [ ] ROI tracking validates business impact
- [ ] Cross-project learning accelerates future developments