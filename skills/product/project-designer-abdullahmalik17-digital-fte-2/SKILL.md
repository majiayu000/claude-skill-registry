---
name: project-designer
description: Comprehensive project design and ideation skill for AI/ML and web/mobile applications. Use when users present initial project ideas that need enhancement, architectural guidance, technology stack recommendations, feature expansion, or implementation strategy. Triggers include requests like "help me design a [project type]", "I want to build [concept] but need to flesh out the idea", "what features should I add to [project]", "recommend a tech stack for [idea]", or "enhance my project concept". Provides structured design thinking, architectural patterns, feature frameworks, and technology recommendations through progressive disclosure of specialized reference materials.
---

# Project Designer

## Overview

Transform initial project concepts into comprehensive, well-architected designs through systematic analysis, feature enhancement, and technology recommendations. This skill guides you through structured ideation, architectural decision-making, and strategic planning for AI/ML agents, web applications, and mobile projects.

## Workflow

### Phase 1: Concept Understanding

**Objective**: Thoroughly understand the user's core idea, goals, and constraints.

**Actions**:
1. **Extract Core Information**:
   - Project type (AI/ML agent, web app, mobile app)
   - Primary problem being solved
   - Target users or personas
   - Key constraints (budget, timeline, team size, technical expertise)

2. **Identify Gaps**:
   - Missing requirements or specifications
   - Unclear objectives or success criteria
   - Undefined user needs

3. **Ask Clarifying Questions**:
   Use the AskUserQuestion tool when:
   - Project scope is ambiguous
   - Multiple architectural approaches are viable
   - Technical requirements are unclear
   - User needs are not fully specified

### Phase 2: Architecture and Technology Guidance

**Objective**: Recommend appropriate architectural patterns and technology stacks based on project requirements.

**Reference Materials**: Load based on project type and needs:
- **`references/ai-ml-patterns.md`**: For AI/ML agents, RAG systems, conversational AI, ML pipelines
- **`references/web-app-patterns.md`**: For web/mobile applications, API design, full-stack systems
- **`references/tech-stack-matrix.md`**: For technology selection across all project types

**Actions**:
1. Identify project type and match to established architectural patterns
2. Recommend technology stack based on team expertise, budget, scalability needs
3. Explain architectural decisions with clear rationale and trade-offs

### Phase 3: Feature Discovery and Enhancement

**Objective**: Expand the initial concept with comprehensive, prioritized features.

**Reference Material**: `references/feature-frameworks.md`

**Actions**:
1. Apply feature discovery methods (Jobs-to-be-Done, User Story Mapping, Feature Analogies)
2. Categorize features: Must-Have (MVP), Should-Have (Post-MVP), Could-Have (Future)
3. Apply prioritization framework (RICE, ICE, Kano model)
4. Consider enhancement dimensions: capability, UX, integration, intelligence

### Phase 4: Structured Documentation

**Objective**: Produce comprehensive project documentation using standardized templates.

**Asset Templates**: Use appropriate templates based on user needs:
- **`assets/templates/project-brief.md`**: Complete project specification
- **`assets/templates/architecture-blueprint.md`**: Detailed technical architecture
- **`assets/templates/feature-roadmap.md`**: Prioritized feature timeline

### Phase 5: Iterative Refinement

**Objective**: Refine the design based on user feedback and emerging requirements.

**Actions**:
1. Present recommendations clearly with critical decisions highlighted
2. Respond to user feedback and adjust recommendations
3. Provide detailed explanations of recommendations
4. Start high-level, drill down into specifics as needed

## Usage Patterns

### Pattern 1: New Project Ideation
User presents initial idea → Understand requirements → Recommend architecture/stack → Enhance features → Generate project-brief.md

### Pattern 2: Existing Project Enhancement
User has working system → Understand current state → Apply feature frameworks → Prioritize enhancements → Generate feature-roadmap.md

### Pattern 3: Technology Stack Consultation
User needs tech guidance → Clarify requirements → Consult tech-stack-matrix.md → Recommend stack with rationale

### Pattern 4: Architecture Design
User needs technical design → Gather requirements → Recommend pattern → Define components → Generate architecture-blueprint.md

## Best Practices

**Communication**:
- Follow workflow phases sequentially
- Use progressive disclosure (high-level first, details when needed)
- Provide concrete, implementable recommendations

**Technical Recommendations**:
- Balance pragmatism with best practices
- Consider team capabilities and constraints
- Provide primary recommendation + alternatives with trade-offs

**Feature Design**:
- Ground features in user problems and needs
- Define clear MVP scope
- Use quantitative prioritization frameworks

## Reference Material Usage

**Load references/ai-ml-patterns.md when**: AI agents, RAG systems, ML pipelines, NLP/CV applications

**Load references/web-app-patterns.md when**: Web/mobile apps, API design, authentication, database patterns

**Load references/tech-stack-matrix.md when**: Technology selection, team/budget considerations, scalability needs

**Load references/feature-frameworks.md when**: Feature ideation, prioritization, user-centric design, roadmap planning

## Anti-Patterns to Avoid

**Don't**:
- Suggest over-engineered solutions for simple problems
- Ignore constraints (budget, timeline, expertise)
- Skip Phase 1 understanding to rush to recommendations
- Load all references unnecessarily
- Make assumptions without clarifying

**Do**:
- Ask clarifying questions when unclear
- Tailor recommendations to specific context
- Provide rationale for recommendations
- Use reference materials to support recommendations
- Balance comprehensiveness with actionability
