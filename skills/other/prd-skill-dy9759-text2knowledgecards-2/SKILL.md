---
name: prd
description: Complete PRD (Product Requirements Document) creation workflow that guides users from initial idea to implementation-ready specification using the integrated toolset in this repository. Handles everything from brainstorming and market analysis to technical requirements and team coordination.
license: Apache 2.0
tools: []
---

# PRD Master - Complete Product Requirements Document Workflow

## Overview

This skill orchestrates the complete PRD creation process using the integrated toolset available in this repository. It guides users through six systematic phases: exploration, project foundation, requirements gathering, quality validation, design preparation, and implementation planning.

**Key Capabilities:**
- 🎯 **Intelligent Phase Selection** - Automatically selects the right tool based on project complexity and scope
- 🔄 **Interactive Workflow** - Guides users through structured decision-making processes
- 📋 **Quality Assurance** - Built-in validation and expert review processes
- 👥 **Team Coordination** - Generates role-specific prompts and checklists
- 📊 **Business Intelligence** - Integrates multi-expert analysis when needed

## When to Use This Skill

**Perfect for:**
- New product development projects
- Major feature additions to existing products
- System redesigns or architectural changes
- Complex feature requirements with multiple stakeholders
- When you need both business and technical requirements

**Triggers:**
- "Help me create a PRD for..."
- "I need to write product requirements for..."
- "Let's spec out a new feature..."
- "We need requirements documentation for..."
- Any mention of PRD, product specs, or requirements documents

## Phase Selection Logic

The skill automatically selects the appropriate starting phase based on user input:

### 🚀 Phase 1: Exploration (Ideation Stage)
**Use when:**
- User has vague ideas or initial concepts
- Multiple possible directions exist
- Market validation is needed
- Business case needs strengthening

**Tools used:**
```bash
/sc:brainstorm "user concept"          # Interactive discovery
/sc:business-panel "market analysis"    # Multi-expert analysis
```

### 🏗️ Phase 2: Project Foundation (Scoping Stage)
**Use when:**
- User has clear idea but needs structure
- Project scope needs definition
- Success metrics need establishment

**Tools used:**
```bash
# Create project brief using BMAD template
# Uses .bmad-core/templates/project-brief-tmpl.yaml
```

### 📋 Phase 3: Requirements Generation (Specification Stage)
**Use when:**
- Clear project scope established
- Ready for detailed requirements
- **Default starting point for most projects**

**Tools used:**
```bash
# Choose based on complexity:
- /speckit.specify "feature description"     # Single feature
- BMAD PRD Template (.bmad-core/templates/prd-tmpl.yaml)  # Complex product
- openspec changes/ for architecture modifications
```

### 🔍 Phase 4: Quality Validation (Review Stage)
**Always executed after requirements generation**

**Tools used:**
```bash
# BMAD quality checklists
openspec validate [change] --strict  # For OpenSpec workflows
```

### 🎨 Phase 5: Design Preparation (Handoff Stage)
**Use when:**
- Requirements validated and approved
- Ready for technical design

**Tools used:**
```bash
/sc:design "system architecture"
/sc:spec-panel "technical review"
```

### 🛠️ Phase 6: Implementation Planning (Execution Stage)
**Use when:**
- Design complete and approved
- Ready for development work

**Tools used:**
```bash
/sc:workflow "implementation planning"
# Generates team-specific prompts and checklists
```

## Workflow Execution

### Step 1: Assess User Input
Analyze the user's request to determine:
- **Clarity Level**: Vague idea vs. clear concept
- **Complexity**: Simple feature vs. complex product
- **Scope**: Single function vs. multi-epic project
- **Stakeholder Count**: Individual vs. team project

### Step 2: Select Starting Phase
Based on assessment, choose the appropriate phase:
- **Low clarity, high uncertainty** → Phase 1 (Exploration)
- **Moderate clarity, defined scope** → Phase 2 (Foundation)
- **High clarity, ready for specs** → Phase 3 (Requirements) - *Default*

### Step 3: Execute Phase Workflow
Follow the structured workflow for the selected phase, automatically triggering the appropriate tools and processes.

### Step 4: Progressive Enhancement
After each phase completion, assess readiness for the next phase. Users can:
- **Continue automatically** to the next phase
- **Pause for review** and manual approval
- **Jump to specific phase** if ready

### Step 5: Generate Team Deliverables
Create role-specific outputs:
- **Product Manager**: Complete PRD with checklists
- **UX Expert**: Design brief and user scenarios
- **Architect**: Technical requirements and constraints
- **Development Team**: Implementation roadmap

## Usage Examples

### Example 1: New Product Idea
```
User: "Help me create a PRD for a new task management app"

Workflow:
1. Phase 1: /sc:brainstorm "task management app features"
2. Phase 1: /sc:business-panel "productivity app market analysis"
3. Phase 2: Create project brief
4. Phase 3: BMAD PRD Template generation
5. Phase 4: Quality validation
6. Phase 5: /sc:design preparation
7. Phase 6: /sc:workflow generation
```

### Example 2: Single Feature Addition
```
User: "I need to write requirements for adding user authentication"

Workflow:
1. Phase 3: /speckit.specify "add user authentication system"
2. Phase 4: Quality checklist generation
3. Phase 5: /sc:design "authentication architecture"
```

### Example 3: System Redesign
```
User: "We need to restructure our microservices architecture"

Workflow:
1. Phase 3: openspec changes/ (create change proposal)
2. Phase 4: openspec validate --strict
3. Phase 5: /sc:spec-panel "architecture review"
```

## Integration with Repository Tools

### BMAD Core Integration
- Uses `.bmad-core/templates/prd-tmpl.yaml` for comprehensive PRDs
- Leverages `.bmad-core/checklists/` for quality assurance
- Accesses `.bmad-core/agents/` for role-specific guidance

### SpeckKit Integration
- Triggers `/speckit.specify` for rapid feature specification
- Utilizes `.specify/templates/spec-template.md` for consistency
- Manages feature branching and validation

### OpenSpec Integration
- Creates structured change proposals under `openspec/changes/`
- Maintains traceability between requirements and specifications
- Supports ongoing requirement evolution

### SuperClaude Commands Integration
- Orchestrates `/sc:*` commands for specialized analysis
- Accesses business panel experts for market insights
- Generates structured workflows for implementation

## Quality Assurance Mechanisms

### Automated Validation
- **Requirement Completeness**: All mandatory sections populated
- **Clarity Assessment**: No ambiguous language or implementation details
- **Testability Criteria**: Every requirement has clear acceptance criteria
- **Stakeholder Alignment**: Business value clearly articulated

### Expert Review Integration
- **Multi-Expert Analysis**: Business panel review for strategic alignment
- **Technical Validation**: Architecture and feasibility assessment
- **UX Review**: User experience and accessibility validation
- **Quality Gate**: Checklist-based signoff process

## Output Deliverables

### Primary Deliverable: Complete PRD Package
```markdown
docs/
├── prd.md                          # Main requirements document
├── project-brief.md               # Executive summary (optional)
├── checklists/
│   ├── pm-checklist.md           # Product manager validation
│   ├── architect-checklist.md    # Technical review checklist
│   └── quality-assurance.md      # Quality validation results
├── prompts/
│   ├── ux-expert-prompt.md       # Design team handoff
│   ├── architect-prompt.md       # Architecture team handoff
│   └── dev-team-prompt.md        # Development team handoff
└── workflows/
    ├── implementation-workflow.md # Development roadmap
    └── validation-workflow.md     # Testing and validation plan
```

### Supporting Artifacts
- **Change Proposals**: OpenSpec change files (if applicable)
- **Feature Branches**: Git branches for specification work (SpeckKit)
- **Quality Reports**: Validation results and remediation plans
- **Team Prompts**: Role-specific guidance documents

## Advanced Features

### Intelligent Tool Selection
The skill automatically chooses the optimal tool combination based on:
- **Project Complexity**: Simple vs. multi-faceted requirements
- **Team Size**: Individual vs. enterprise workflows
- **Timeline Pressure**: Rapid prototyping vs. comprehensive analysis
- **Risk Level**: Low-risk features vs. high-impact changes

### Contextual Adaptation
- **Domain Knowledge**: Adapts terminology and focus areas based on project type
- **Team Experience**: Adjusts detail level based on presumed team expertise
- **Organizational Context**: Considers enterprise vs. startup constraints
- **Technical Debt**: Accounts for existing system constraints and legacy considerations

### Continuous Improvement
- **Pattern Learning**: Learns from successful PRD patterns in your organization
- **Feedback Integration**: Incorporates lessons learned from previous projects
- **Template Evolution**: Improves templates based on usage patterns
- **Quality Metrics**: Tracks PRD effectiveness and implementation success rates

## Best Practices

### For Product Managers
- **Start Early**: Engage this skill at the concept stage, not just before implementation
- **Iterative Refinement**: Use the quality validation phases to progressively improve requirements
- **Stakeholder Involvement**: Leverage the multi-expert analysis for comprehensive perspective

### For Development Teams
- **Clear Handoffs**: Use the generated prompts to ensure smooth transitions between phases
- **Feedback Loops**: Provide implementation feedback to improve future PRD quality
- **Traceability**: Maintain links between requirements and implemented features

### For Organizations
- **Template Customization**: Adapt the BMAD templates to match organizational standards
- **Process Integration**: Integrate with existing product development lifecycle
- **Quality Gates**: Establish organizational standards based on the generated checklists

## Troubleshooting

### Common Issues
- **Tool Selection Confusion**: Skill will recommend the optimal starting point based on user input
- **Scope Creep**: Use the quality validation phases to maintain appropriate boundaries
- **Stakeholder Alignment**: Leverage business panel analysis for consensus building
- **Technical Feasibility**: Use architecture review phases early for complex projects

### Recovery Mechanisms
- **Phase Restart**: Can restart from any phase if issues are discovered
- **Tool Switching**: Can switch between BMAD, SpeckKit, and OpenSpec based on evolving needs
- **Quality Revalidation**: Can re-run quality checks after major revisions
- **Expert Re-engagement**: Can re-involve business panel experts for critical decisions

---

This skill transforms the complex process of PRD creation into a structured, guided experience that leverages the full power of your integrated development toolset. It ensures comprehensive coverage of business requirements, technical constraints, user experience considerations, and implementation planning while maintaining high quality standards throughout the process.