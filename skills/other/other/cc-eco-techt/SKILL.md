---
name: cc-eco-techt
description: Claude Code Ecosystem Architect - Master skill for creating Claude Code ecosystem components (skills, commands, hooks, subagents, plugins)
keywords: [architecture, meta-creation, workflow-design, ecosystem-building, component-generation]
---

# Claude Code Ecosystem Architect (cc-eco-techt)

## What This Skill Does
Transforms Claude into a master architect capable of designing and implementing complete Claude Code ecosystem solutions. Analyzes requirements, recommends optimal component combinations, and generates production-ready skills, commands, hooks, and subagents based on the comprehensive documentation system.

## Core Capabilities

### 1. Requirements Analysis & Architecture Design
- Analyze project scope, team size, and workflow patterns
- Map requirements to optimal component combinations
- Design token-efficient architectures
- Plan progressive complexity (start simple, add complexity as needed)

### 2. Component Generation Engine
- Generate AGENTS.md with proper project context
- Create SKILL.md files with auto-triggering patterns
- Build slash commands with argument handling
- Design hooks with proper event context
- Architect subagents with isolated contexts

### 3. Integration & Optimization
- Ensure components work together harmoniously
- Optimize for token usage and performance
- Create proper file structures and naming
- Design escalation patterns (simple → complex)

## When This Skill Auto-Triggers
Claude will automatically use this skill when detecting requests for:
- "create a workflow for"
- "build a skill to"
- "design an agent for"
- "automate this process"
- "set up project structure"
- "optimize my claude setup"
- "create templates for"
- "generate claude code components"
- "build ecosystem components"
- "design slash commands"
- "create hooks for"

## Component Generation Templates

### Skill Generation Template
```yaml
Skill Analysis Context:
- Domain: [Analyze the domain from user request]
- Frequency: [How often will this be used?]
- Complexity: [Simple/Medium/Complex]
- Token Budget: [Estimate token requirements]
- Integration Points: [What other components needed?]

Generated Skill Structure:
1. Clear trigger patterns in keywords
2. Progressive disclosure architecture
3. Efficient tool selection
4. Error handling patterns
5. Integration hooks with other components
```

### Command Generation Template
```yaml
Command Analysis Context:
- Workflow Type: [Deployment/Testing/Generation/etc.]
- User Control: [Manual/Automated/Hybrid]
- Arguments Required: [List with types and defaults]
- Error Scenarios: [Common failure modes]
- Integration Needs: [Skills/subagents required]

Generated Command Structure:
1. Clear YAML frontmatter with schema
2. Step-by-step workflow documentation
3. Error handling and recovery procedures
4. Success criteria and output format
5. Integration with other components
```

### Hook Generation Template
```yaml
Hook Analysis Context:
- Event Type: [pre/post/validate]
- Blocking Requirements: [Can it block the action?]
- Validation Logic: [What needs to be checked?]
- Performance Constraints: [Time limits]
- Rollback Capabilities: [Can actions be undone?]

Generated Hook Structure:
1. YAML configuration with type and settings
2. Event context parsing documentation
3. Validation logic flow
4. Success/failure decision paths
5. User feedback and bypass mechanisms
```

### Subagent Generation Template
```yaml
Subagent Analysis Context:
- Specialization Domain: [Specific area of expertise]
- Isolation Requirements: [Why needs separate context]
- Tool Requirements: [Specific tools needed]
- Interaction Patterns: [How main agent delegates]
- Escalation Criteria: [When to involve main agent]

Generated Subagent Structure:
1. Clear domain definition and boundaries
2. Specific expertise documentation
3. Tool access patterns
4. Interaction protocols
5. Escalation procedures
```

## Workflow Generation Process

### Phase 1: Requirements Analysis
1. **Understand the Problem**
   - Parse user request for core requirements
   - Identify frequency and usage patterns
   - Determine target audience and skill level
   - Anticipate failure modes and edge cases

2. **Map to Ecosystem Components**
   - Automatic triggering needed? → Skill
   - Specialist task with isolation? → Subagent
   - User-triggered workflow? → Command
   - Validation/automation needed? → Hook
   - External dependencies? → MCP integration

3. **Design Token Architecture**
   - Estimate token costs for each component
   - Plan progressive disclosure strategies
   - Design efficient loading sequences
   - Plan context window management

### Phase 2: Component Generation
1. **Generate Primary Component**
   - Create the main component file structure
   - Implement proper YAML frontmatter
   - Add comprehensive documentation
   - Include examples and usage patterns

2. **Generate Supporting Components**
   - Create helper skills for complex tasks
   - Design supporting commands for workflows
   - Add validation hooks for quality gates
   - Plan integration coordination

3. **Create Integration Layer**
   - Design component interaction patterns
   - Create escalation and delegation flows
   - Plan error recovery mechanisms
   - Document usage workflows

### Phase 3: Optimization & Validation
1. **Token Optimization**
   - Review component sizes and efficiency
   - Optimize loading and caching patterns
   - Plan context cleanup procedures
   - Design progressive complexity

2. **Integration Testing Plan**
   - Define component interaction tests
   - Plan error handling validation
   - Test edge cases and failure modes
   - Validate user experience flows

## Example Generation Patterns

### Example 1: Testing Automation Workflow
**User Input:** "I need a comprehensive testing workflow for our React TypeScript project"

**Generated Solution:**
1. **Main Skill:** `react-testing-automation`
   - Auto-triggers on test file changes
   - Orchestrates unit, integration, and E2E tests
   - Progressive disclosure of results
   - Integration with CI/CD pipelines

2. **Command:** `/run-tests [type] [coverage] [report]`
   - Manual test execution with arguments
   - Support for different test suites
   - Coverage reporting options
   - Integration with testing frameworks

3. **Hook:** `pre-commit-test-validation`
   - Runs critical tests before commits
   - Blocks commits on test failures
   - Provides immediate feedback
   - Configurable test selection

### Example 2: Documentation Generation System
**User Input:** "Create a system to automatically generate and update API documentation"

**Generated Solution:**
1. **Main Skill:** `api-documentation-generator`
   - Analyzes code changes for documentation impact
   - Generates documentation updates
   - Maintains consistency across formats
   - Integration with multiple doc generators

2. **Command:** `/update-docs [section] [format] [publish]`
   - Manual documentation updates
   - Section-specific regeneration
   - Multiple output formats (Markdown, OpenAPI, etc.)
   - Publishing integration

3. **Hook:** `post-commit-doc-update`
   - Updates docs after relevant commits
   - Non-blocking validation
   - Automated publishing to documentation sites
   - Change tracking and notifications

4. **MCP Integration:** GitHub API for documentation deployment
   - Fetches PR and release information
   - Updates GitHub Pages and wiki
   - Manages documentation versioning

## Component Decision Matrix

| Requirement | Best Component | Why |
|-------------|----------------|-----|
| Automatic trigger on content | **Skill** | Auto-detection and progressive loading |
| Specialist with isolated context | **Subagent** | Clean separation and focused expertise |
| User-controlled workflow | **Command** | Manual invocation with arguments |
| Quality validation/automation | **Hook** | Event-driven and can block actions |
| External tool integration | **MCP** | Standardized external access |
| Complete solution bundle | **Plugin** | Multiple related components |
| Project-wide standards | **AGENTS.md** | Foundation for all components |

## Best Practices for Generated Components

### 1. Progressive Complexity
- Start with minimum viable implementation
- Add features incrementally based on usage
- Maintain backward compatibility
- Plan clear upgrade paths

### 2. Token Efficiency
- Use progressive disclosure patterns
- Load metadata before full content
- Implement smart caching strategies
- Plan context window management

### 3. Error Handling
- Anticipate common failure modes
- Provide clear, actionable error messages
- Implement graceful degradation
- Plan recovery and retry procedures

### 4. User Experience
- Make component interactions intuitive
- Provide clear feedback and progress indication
- Include comprehensive examples
- Document usage patterns and workflows

### 5. Integration Design
- Design clear interfaces between components
- Plan interaction patterns and data flows
- Implement proper isolation boundaries
- Create escalation and delegation paths

## Advanced Features

### 1. Self-Improving Patterns
Components can include analytics and learning mechanisms to optimize based on usage patterns.

### 2. Template Library Integration
Access to growing library of proven templates for common patterns and workflows.

### 3. Automated Testing
Components can generate their own test suites and validation procedures.

### 4. Performance Monitoring
Built-in token usage tracking and performance optimization recommendations.

## Implementation Tools

### Core Analysis Tools
- **Requirements Parser**: Extract and categorize user requirements
- **Component Mapper**: Map requirements to optimal ecosystem components
- **Token Estimator**: Calculate token costs and optimization strategies
- **Integration Planner**: Design component interaction patterns

### Generation Tools
- **Template Engine**: Generate properly structured component files
- **Documentation Generator**: Create comprehensive usage documentation
- **Example Generator**: Produce realistic usage examples
- **Test Case Generator**: Create validation and test procedures

### Validation Tools
- **Syntax Validator**: Ensure proper YAML and markdown structure
- **Integration Tester**: Validate component interactions
- **Performance Analyzer**: Check token efficiency and loading patterns
- **Usability Reviewer**: Validate user experience and workflows

## Usage Patterns

### For Simple Automation Requests
1. Detect automation keywords in user request
2. Analyze complexity and frequency
3. Recommend single component (usually Skill or Command)
4. Generate component with basic template
5. Provide usage examples

### For Complex Workflow Requests
1. Parse multi-step requirements
2. Identify component dependencies
3. Design multi-component solution
4. Generate integrated component system
5. Provide complete workflow documentation

### For Team/Project Setup Requests
1. Analyze project scope and team requirements
2. Design comprehensive ecosystem architecture
3. Generate multiple coordinated components
4. Create integration and usage documentation
5. Provide team onboarding materials

## Quality Assurance Checklist

### Component Validation
- [ ] Proper YAML frontmatter structure
- [ ] Clear trigger patterns and keywords
- [ ] Comprehensive documentation and examples
- [ ] Error handling and edge cases covered
- [ ] Token usage optimized
- [ ] Integration patterns documented

### Integration Validation
- [ ] Components work together harmoniously
- [ ] Clear escalation and delegation patterns
- [ ] Proper isolation and boundaries maintained
- [ ] User workflows intuitive and documented
- [ ] Performance meets requirements

### Documentation Validation
- [ ] Usage examples clear and realistic
- [ ] Integration patterns well documented
- [ ] Troubleshooting guidance included
- [ ] Best practices and limitations documented
- [ ] Cross-references to related components

This skill transforms Claude into a comprehensive ecosystem architect, capable of designing and implementing complete Claude Code ecosystem solutions tailored to specific user requirements and organizational needs.