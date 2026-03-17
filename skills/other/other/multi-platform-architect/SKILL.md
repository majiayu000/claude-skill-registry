---
name: multi-platform-architect
description: Multi-Platform AI Ecosystem Architect - Master skill for creating ecosystem components across Claude Code, Codex, Auggie, Kilocode, Goose, Gemini-CLI
keywords: [architecture, meta-creation, workflow-design, ecosystem-building, component-generation, multi-platform]
---

# Multi-Platform AI Ecosystem Architect

## What This Skill Does
Transforms any AI CLI into a master architect capable of designing and implementing complete ecosystem solutions. Automatically detects the current platform, analyzes requirements, recommends optimal component combinations, and generates production-ready components tailored to each platform's specific architecture and conventions.

## Supported Platforms

### 1. Claude Code
- **Directory:** `.claude/`
- **Components:** Skills, Commands, Hooks, Agents, Plugins
- **Triggers:** `/command`, `@agent`, automatic detection
- **Resource:** Token-based optimization

### 2. Codex
- **Directory:** `.codex/` or `.vscode/codex/`
- **Components:** Workspace config, Commands, Scripts, Extensions
- **Triggers:** `!command`, workspace automation
- **Resource:** Context-based optimization

### 3. Auggie
- **Directory:** `.auggie/`
- **Components:** Agents, Workflows, Integrations, Modules
- **Triggers:** `agent:`, workflow automation
- **Resource:** Task-based optimization

### 4. Kilocode
- **Directory:** `.kilocode/`
- **Components:** Tasks, Workflows, Tools, Configurations
- **Triggers:** `task:`, automation workflows
- **Resource:** Process-based optimization

### 5. Goose
- **Directory:** `.goose/`
- **Components:** Agents, Commands, Modules, Extensions
- **Triggers:** `goose:`, command modules
- **Resource:** Memory-based optimization

### 6. Gemini-CLI
- **Directory:** `.gemini/`
- **Components:** Contexts, Commands, Workflows, Prompts
- **Triggers:** `gemini:`, context loading
- **Resource:** Context-based optimization

## Core Capabilities

### 1. Automatic Platform Detection
- Scans for platform-specific directories and files
- Detects command patterns and syntax
- Identifies platform capabilities and limitations
- Falls back to generic templates for unknown platforms

### 2. Multi-Platform Component Generation
- Generates platform-appropriate file structures
- Adapts component types to each platform's conventions
- Creates platform-specific configuration schemas
- Handles different resource models (tokens vs context)

### 3. Cross-Platform Integration
- Designs components that work across multiple platforms
- Creates migration guides between platforms
- Establishes interoperability patterns
- Handles platform-specific limitations gracefully

## Platform Detection Logic

### Directory-Based Detection
```python
def detect_platform():
    platform_checks = [
        ('claude-code', ['.claude/']),
        ('codex', ['.codex/', '.vscode/codex/']),
        ('auggie', ['.auggie/']),
        ('kilocode', ['.kilocode/']),
        ('goose', ['.goose/']),
        ('gemini-cli', ['.gemini/'])
    ]

    for platform, paths in platform_checks:
        if any(os.path.exists(path) for path in paths):
            return platform
    return 'generic'
```

### Command Pattern Detection
- **Claude Code:** `/command`, `@agent` delegation
- **Codex:** `!command`, workspace commands
- **Auggie:** `agent:`, workflow triggers
- **Kilocode:** `task:`, automation definitions
- **Goose:** `goose:`, module invocations
- **Gemini-CLI:** `gemini:`, context loading

## When This Skill Auto-Triggers

The AI will automatically use this skill when detecting requests for:
- "create a workflow for [platform]"
- "build a [component type] for [platform]"
- "design [component] that works across multiple platforms"
- "automate this process for [platform]"
- "set up project structure for [platform]"
- "optimize my [platform] setup"
- "create templates for [platform]"
- "generate cross-platform components"
- "build ecosystem components"
- "design custom commands for [platform]"
- "create automation for [platform]"

## Multi-Platform Component Generation

### Platform Analysis Process
```yaml
Analysis Flow:
1. Detect current platform
2. Analyze user requirements
3. Map requirements to platform-specific components
4. Generate optimized component architecture
5. Create platform-appropriate file structures
```

### Component Mapping Matrix

| Requirement | Claude Code | Codex | Auggie | Kilocode | Goose | Gemini-CLI |
|-------------|-------------|-------|--------|-----------|-------|-------------|
| **Automation** | SKILL.md | Script | Agent | Task | Module | Workflow |
| **User Control** | Command | Command | Workflow | Config | Command | Command |
| **Validation** | Hook | Extension | Integration | Tool | Extension | Context |
| **Specialization** | Agent | Extension | Agent | Tool | Agent | Prompt |

### Template Adaptation Patterns

#### 1. Directory Structure Adaptation
```yaml
Template Variables:
- PLATFORM: Detected platform
- BASE_DIR: Platform-specific directory
- FILE_EXT: Platform-appropriate file extension
- SYNTAX: Platform-specific syntax (YAML, JSON, etc.)
```

#### 2. Resource Budget Optimization
```yaml
Resource Models:
- Claude Code: Token-based (30-600 tokens)
- Codex: Context-based (100-400 units)
- Auggie: Task-based (50-300 units)
- Kilocode: Process-based (100-500 units)
- Goose: Memory-based (100-512MB)
- Gemini-CLI: Context-based (200-2048 tokens)
```

#### 3. Trigger Pattern Adaptation
```yaml
Trigger Adaptation:
- Claude Code: /command, @agent, automatic
- Codex: !command, workspace, automation
- Auggie: agent:, workflow, automation
- Kilocode: task:, automation, workflow
- Goose: goose:, command, module
- Gemini-CLI: gemini:, context, workflow
```

## Cross-Platform Workflow Examples

### Example 1: Testing Workflow
**User Input:** "Create a testing workflow that works in Claude Code and Goose"

**Generated Solution:**
- **Claude Code Version:**
  - Skill: `testing-automation` (auto-trigger)
  - Command: `/run-tests [type]` (manual)
  - Hook: `pre-commit-test-validation` (blocking)
- **Goose Version:**
  - Agent: `testing-agent` (task specialist)
  - Module: `test-runner.py` (execution)
  - Command: `goose:test` (invocation)

### Example 2: Documentation System
**User Input:** "Build documentation generation for Codex and Gemini-CLI"

**Generated Solution:**
- **Codex Version:**
  - Command: `!generate-docs` (workspace automation)
  - Script: `doc-generator.py` (generation logic)
  - Extension: `docs-viewer.js` (display)
- **Gemini-CLI Version:**
  - Context: `documentation-expert` (specialist)
  - Workflow: `doc-generation.yaml` (process)
  - Prompt: `doc-template.txt` (format)

### Example 3: Deployment Pipeline
**User Input:** "Create deployment automation for Auggie and Kilocode"

**Generated Solution:**
- **Auggie Version:**
  - Agent: `deployment-manager` (orchestration)
  - Workflow: `deploy-pipeline.yaml` (process)
  - Integration: `k8s-deploy.py` (infrastructure)
- **Kilocode Version:**
  - Task: `deploy-app` (deployment action)
  - Workflow: `ci-cd-pipeline.yaml` (process)
  - Tool: `infrastructure.json` (config)

## Platform-Specific Best Practices

### Claude Code
- Focus on token efficiency and progressive loading
- Use slash commands for user-controlled workflows
- Implement hooks for quality gates and validation
- Leverage subagents for specialized tasks

### Codex
- Integrate with Visual Studio ecosystem
- Use workspace configurations for team settings
- Leverage extensions for IDE integration
- Focus on automation within development workflows

### Auggie
- Design agent-based architectures
- Use YAML configurations for declarative workflows
- Implement modular integration patterns
- Focus on task automation and orchestration

### Kilocode
- Create task-based automation systems
- Use JSON configurations for structured data
- Implement workflow orchestration patterns
- Focus on process automation and tool integration

### Goose
- Design modular agent systems
- Use Python modules for extensibility
- Implement memory-efficient workflows
- Focus on command-based interactions

### Gemini-CLI
- Create context-based expertise systems
- Use YAML for structured prompts
- Implement workflow-based automation
- Focus on conversation and context management

## Cross-Platform Migration

### Migration Patterns
```yaml
Claude Code → Codex:
  SKILL.md → workspace.json + script.py
  /command → !command + extension.js
  @agent → agent.yaml + module.py

Codex → Claude Code:
  workspace.json → AGENTS.md
  !command → /command
  extension.js → SKILL.md

Generic Template:
  Adaptable to any platform with minimal modifications
  Platform-agnostic file structures
  Universal component patterns
```

### Interoperability Strategies
1. **Adapter Components:** Create wrapper components that bridge platforms
2. **Shared Configurations:** Use common configuration formats (YAML, JSON)
3. **Standard Interfaces:** Implement consistent API patterns
4. **Migration Tools:** Generate platform-specific migration scripts

## Platform Detection and Adaptation

### Auto-Detection Algorithm
```python
def detect_and_adapt(user_input):
    # 1. Detect current platform
    platform = detect_platform()

    # 2. Analyze user requirements
    requirements = analyze_requirements(user_input)

    # 3. Adapt to platform constraints
    adapted_specs = adapt_to_platform(requirements, platform)

    # 4. Generate components
    components = generate_components(adapted_specs)

    return components
```

### Constraint Handling
```yaml
Platform Constraints:
  claude-code:
    - Token limits
    - Context window size
    - MCP integration

  codex:
    - Workspace limitations
    - IDE integration
    - Extension compatibility

  auggie:
    - Task isolation
    - Workflow complexity
    - Memory usage

  kilocode:
    - Process coordination
    - Tool availability
    - Configuration complexity

  goose:
    - Memory constraints
    - Module loading
    - Extension system

  gemini-cli:
    - Context length
    - Model limitations
    - Prompt management
```

## Advanced Features

### 1. Platform-Hopping Workflows
Create workflows that span multiple platforms, using each platform's strengths:
- **Claude Code:** Complex reasoning and token optimization
- **Codex:** IDE integration and development workflows
- **Goose:** Memory-intensive processing
- **Gemini-CLI:** Context management and conversation

### 2. Hybrid Component Systems
Design components that combine capabilities from multiple platforms:
- **Shared Configuration:** Common configs stored in neutral formats
- **Bridge Components:** Adapters that enable inter-platform communication
- **Fallback Mechanisms:** Alternative approaches for platform failures

### 3. Progressive Enhancement
Build solutions that start simple and add complexity as needed:
- **Basic:** Generic templates that work everywhere
- **Intermediate:** Platform-specific optimizations
- **Advanced:** Full platform-native capabilities

## Usage Examples

### Cross-Platform Testing
**User Input:** "I need a testing solution that works in both Claude Code and Auggie"

**Generated Solution:**
1. **Analysis:** Detect current platform, generate appropriate components
2. **Claude Code Version:**
   - Skill: `universal-testing` (auto-triggering)
   - Command: `/test-everything` (manual)
   - Hook: `validate-quality` (blocking)
3. **Auggie Version:**
   - Agent: `testing-coordinator` (orchestration)
   - Workflow: `testing-pipeline` (process)
   - Module: `quality-checker` (validation)

### Multi-Platform Documentation
**User Input:** "Create documentation that works in Codex, Goose, and Gemini-CLI"

**Generated Solution:**
1. **Codex Components:**
   - Workspace config for VS Code integration
   - JavaScript extension for display
   - Automated script for generation
2. **Goose Components:**
   - Agent for content processing
   - Python module for generation logic
   - Command for manual invocation
3. **Gemini-CLI Components:**
   - Context specialist for content expertise
   - Workflow for generation process
   - Prompts for formatting templates

### Platform Migration Assistant
**User Input:** "Help me migrate my Claude Code setup to work with Goose"

**Generated Solution:**
1. **Analysis Tool:** Scripts to analyze existing Claude Code setup
2. **Migration Generator:** Automatic component conversion
3. **Bridge Components:** Adapters to maintain functionality
4. **Validation System:** Testing frameworks to ensure compatibility
5. **Documentation:** Migration guides and best practices

## Platform-Specific Troubleshooting

### Common Issues and Solutions

#### Claude Code
- **Token Exhaustion:** Implement progressive loading and caching
- **Context Window Issues:** Use subagents for isolation
- **MCP Integration:** Configure external tool access

#### Codex
- **Extension Conflicts:** Manage extension compatibility
- **Workspace Issues:** Resolve VS Code integration problems
- **Automation Limitations:** Work within IDE constraints

#### Auggie
- **Agent Isolation:** Handle context separation properly
- **Workflow Complexity:** Break down complex workflows
- **Memory Management:** Optimize task resource usage

#### Kilocode
- **Process Coordination:** Handle task dependencies
- **Tool Integration:** Ensure tool compatibility
- **Configuration Complexity:** Simplify setup processes

#### Goose
- **Memory Constraints:** Optimize for memory efficiency
- **Module Loading:** Handle dynamic module imports
- **Extension Conflicts:** Resolve dependency issues

#### Gemini-CLI
- **Context Limits:** Manage conversation length
- **Model Constraints:** Work within model capabilities
- **Prompt Management:** Optimize prompt efficiency

## Future Platform Support

### Extensible Architecture
The skill is designed to easily support new platforms:

1. **Add Platform Detection:** Extend platform checks
2. **Create Templates:** Build platform-specific templates
3. **Define Components:** Specify component types and structures
4. **Implement Patterns:** Create platform-specific patterns

### Community Contributions
Users can contribute:
- **Platform Templates:** Create templates for new platforms
- **Component Types:** Define new component categories
- **Integration Patterns:** Document best practices
- **Migration Guides:** Share platform migration experiences

This multi-platform architect skill transforms any AI CLI into a comprehensive ecosystem builder, capable of generating optimized components for any supported platform while maintaining cross-platform compatibility and interoperability.