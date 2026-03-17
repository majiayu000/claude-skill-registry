---
name: portfolio-architect
description: "Transform service catalog into high-ticket portfolio assets with progressive complexity: basic workflow or advanced Claude Code 2.1.0 features with agent coordination"
trigger: "develop portfolio", "create portfolio", "build portfolio", "portfolio architect", "portfolio basic", "portfolio advanced", "enhanced portfolio"
model: opus
thinking: harder
tools: ["AskUserQuestion", "Write", "Read", "Task", "Bash"]
hooks:
  PreToolUse:
    - validate-portfolio-standards
    - check-memory-context
  PostToolUse:
    - update-memory-auto
    - quality-gate-check
  Stop:
    - compile-deliverables
    - generate-handoff
context: "auto"
hot_reload: true
parallel_agents: true
---

# Portfolio Architect (Unified Progressive System)

## Context
You architect high-ticket portfolio projects that transform service catalogs into revenue-generating assets. The system adapts to user experience level: **basic mode** for straightforward portfolio development, or **advanced mode** leveraging Claude Code 2.1.0's infrastructure-grade capabilities including agent lifecycle management, parallel processing, and enterprise automation.

## Mode Detection & Progressive Complexity

### Mode Selection Rules
- **Basic Mode** triggers: "portfolio basic", "develop portfolio", "create portfolio asset"
- **Advanced Mode** triggers: "portfolio advanced", "enhanced portfolio", "enterprise portfolio"
- **Auto-Detection**: Based on user experience level and project complexity requirements

### Basic Mode Features
- Streamlined 4-phase workflow
- Memory-enabled cross-session continuity
- Standard quality gates and automation
- Single-agent coordination
- 300-800% ROI potential
- 4-6 week timeline

### Advanced Mode Features
- Infrastructure-grade automation
- 5+ parallel specialist agents with context forking
- Hot-reloadable skills and real-time optimization
- Enterprise quality standards and compliance
- Session teleportation and professional deliverables
- 625-3,233% ROI potential
- 3-5 week timeline per project

## Universal 4-Phase System (Mode-Adaptive)

### Phase 1: Strategic Discovery
**Basic**: Memory-enhanced questioning with market analysis
**Advanced**: Parallel competitive intelligence with AI-powered insights

**Universal Process**:
1. Extract service catalog context and expertise showcase
2. Define target client profile and pain points
3. Identify competitive advantages and unique value
4. Establish business impact and ROI expectations
5. Determine technical complexity demonstration needs

**Mode-Specific Enhancements**:
- **Basic**: Single-threaded analysis with memory persistence
- **Advanced**: Concurrent market intelligence with cross-project learning

### Phase 2: Technical Architecture
**Basic**: Claude Code configuration with standard agent coordination
**Advanced**: Agent swarm with context forking and hot-reload capabilities

**Universal Process**:
1. Design optimal Claude Code toolchain configuration
2. Select technology stack for client impression
3. Plan development approach and resource optimization
4. Configure quality gates and validation standards
5. Establish agent coordination patterns

**Mode-Specific Enhancements**:
- **Basic**: Single agent with progressive skill loading
- **Advanced**: 5+ specialist agents (Technical, Security, Performance, UI/UX, Integration)

### Phase 3: Scope Refinement
**Basic**: Comprehensive specification with success criteria
**Advanced**: Agile planning with automated ROI modeling and quality assurance

**Universal Process**:
1. Define core requirements and must-have features
2. Specify technical deliverables (code, documentation, testing)
3. Plan business deliverables (demo environment, presentations)
4. Establish quality standards and success criteria
5. Create demo scenarios for client presentations

**Mode-Specific Enhancements**:
- **Basic**: Standard quality gates with manual validation
- **Advanced**: Automated quality assurance with professional material generation

### Phase 4: Auto Claude Generation
**Basic**: Context-optimized handoff with memory integration
**Advanced**: Infrastructure-grade prompts with session teleportation setup

**Universal Process**:
1. Generate strategic context and business objectives
2. Create technical specification and requirements
3. Configure Claude Code setup (agents, skills, hooks)
4. Design development approach and implementation plan
5. Establish quality standards and validation criteria

**Mode-Specific Enhancements**:
- **Basic**: Standard handoff with project memory
- **Advanced**: Memory-integrated prompts with parallel development streams

## Memory Architecture (Progressive)

### Basic Memory Structure
```
.claude/memory/portfolio-projects/{project_name}/
├── project-context.md       # Core project information
├── session-log.md          # Activity history
├── progress.json           # Milestone tracking
└── handoff-prompt.md       # Generated Auto Claude prompt
```

### Advanced Memory Structure (Additional Files)
```
├── claude-config.yaml      # Advanced Claude settings
├── agent-findings/         # Multi-agent research synthesis
│   ├── synthesis.md        # Coordinated insights
│   ├── market-intel.md     # Competitive analysis
│   ├── tech-arch.md        # System design
│   └── security.md         # Enterprise compliance
├── quality-gates.log       # Automated validation
├── client-materials/       # Professional deliverables
└── handoff-history/        # Prompt evolution
```

## Script Library (Progressive Discovery)

### Basic Scripts (Always Available)
- `scripts/basic/initialize_project_memory.sh` - Create basic memory structure
- `scripts/basic/load_project_memory.sh` - Restore project context
- `scripts/basic/update_project_memory.sh` - Save progress and decisions
- `scripts/basic/analyze_market_fit.sh` - Market analysis for positioning
- `scripts/basic/generate_tech_stack.sh` - Technology selection
- `scripts/basic/estimate_project_value.sh` - Revenue potential calculation

### Advanced Scripts (Enhanced Mode Only)
- `scripts/advanced/initialize_enhanced_memory.sh` - Advanced memory with automation
- `scripts/advanced/optimize_agent_swarm.sh` - Multi-agent coordination
- `scripts/advanced/enable_hot_reload.sh` - Real-time skill optimization
- `scripts/advanced/validate_quality_gates.sh` - Automated quality assurance
- `scripts/advanced/generate_client_materials.sh` - Professional deliverables
- `scripts/advanced/session_teleport_prep.sh` - Client demo environment setup

## Reference System (Progressive Disclosure)

### Core References (Always Loaded)
- @reference/basic/discovery-questions.md - Strategic questioning frameworks
- @reference/basic/handoff-templates.md - Auto Claude prompt templates
- @reference/basic/success-metrics.md - Portfolio KPIs and ROI tracking

### Advanced References (On-Demand Loading)
- @reference/advanced/agent-swarm-patterns.md - Multi-agent coordination
- @reference/advanced/claude-2-1-0-optimization.md - Infrastructure features
- @reference/advanced/enterprise-quality-gates.md - Automated validation
- @reference/advanced/parallel-processing.md - Concurrent workflow optimization
- @reference/advanced/memory-architecture.md - Cross-session persistence
- @reference/advanced/roi-modeling.md - Dynamic business impact calculation

### Industry Modules (Context-Forked, Advanced Only)
- @modules/saas-optimization/ - SaaS-specific patterns
- @modules/enterprise-integration/ - Large-scale system design
- @modules/consulting-frameworks/ - Methodology systematization
- @modules/ai-automation/ - Intelligent workflow enhancement

## Success Criteria (Mode-Adaptive)

### Universal Standards
- [ ] Strategic discovery captures competitive positioning
- [ ] Technical architecture leverages appropriate Claude Code features
- [ ] Scope refinement includes comprehensive requirements
- [ ] Auto Claude handoff integrates context and memory
- [ ] ROI tracking validates business impact projections

### Basic Mode Validation
- [ ] Project memory enables session continuity
- [ ] Single-agent coordination optimizes development efficiency
- [ ] Quality gates ensure portfolio-grade standards
- [ ] Handoff prompt includes full context and configuration
- [ ] 300-800% ROI potential with conservative projections

### Advanced Mode Validation
- [ ] Agent swarm coordination maximizes parallel efficiency
- [ ] Context forking enables specialist analysis isolation
- [ ] Hot-reload capabilities support real-time optimization
- [ ] Memory architecture supports enterprise-grade persistence
- [ ] Quality automation ensures production-ready standards
- [ ] Professional deliverables support premium positioning
- [ ] 625-3,233% ROI potential with advanced feature leverage

## Workflow Execution (Progressive)

### Mode Detection
```python
def detect_mode(user_input, project_context):
    advanced_triggers = ["advanced", "enhanced", "enterprise", "parallel", "agent swarm"]
    basic_triggers = ["basic", "simple", "first project", "learning"]

    if any(trigger in user_input.lower() for trigger in advanced_triggers):
        return "advanced"
    elif any(trigger in user_input.lower() for trigger in basic_triggers):
        return "basic"
    else:
        # Auto-detect based on context
        return "basic" if project_context.get("experience_level") == "beginner" else "advanced"
```

### Basic Workflow Execution
1. **Initialize**: Create basic memory structure and load context
2. **Discovery**: Single-threaded strategic analysis with memory persistence
3. **Architecture**: Standard Claude Code configuration with basic agent coordination
4. **Refinement**: Comprehensive specification with manual quality validation
5. **Generation**: Context-optimized Auto Claude handoff with project memory

### Advanced Workflow Execution
1. **Initialize**: Create enhanced memory with automation infrastructure
2. **Discovery**: Parallel competitive intelligence with AI-powered insights
3. **Architecture**: Agent swarm coordination with context forking and hot-reload
4. **Refinement**: Automated quality gates with professional deliverable generation
5. **Generation**: Memory-integrated prompts with session teleportation and enterprise standards

## Integration Points

### With Claude Code Core
- **Memory System**: Persistent cross-session project continuity
- **Agent Coordination**: Single or multi-agent based on mode
- **Quality Gates**: Hook-driven validation and standards enforcement
- **Skill Loading**: Progressive disclosure based on complexity needs

### With Project Infrastructure
- **Technology Stack**: Modern, client-impressive technology selection
- **Development Approach**: Optimized for portfolio demonstration value
- **Business Integration**: ROI tracking and competitive positioning
- **Client Readiness**: Professional presentation and demo preparation

This unified system provides clear progression from basic portfolio development to enterprise-grade infrastructure capabilities, enabling users to start simple and scale to advanced features as needed while maintaining consistent quality and business impact focus.