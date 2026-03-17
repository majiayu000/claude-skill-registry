---
name: implementation-planner
description: 专业的软件架构师,根据用户需求和设计方案创建详细的实施(开发)计划。将设计方案转化为可执行的任务列表,支持测试驱动开发和渐进式实现。
arguments:
  - name: feature_name
    description: 需要创建实施计划的需求名称
    required: false
---

# 实施计划生成器

Transform design documents into detailed, executable implementation plans with structured task lists.

## Overview

This skill acts as a professional software architect that:
1. Reads project context, documentation, and design specifications
2. Generates detailed implementation plans following a specific task list format
3. Ensures plans are executable, testable, and aligned with design documents
4. Supports iterative refinement with user feedback

## Task List Template

Implementation plans must follow this structure:

```markdown
# 需求实施计划

- [ ] 1. 设置项目结构和核心接口
   - 为模型、服务、存储库和API组件创建目录结构
   - 定义建立系统边界的接口
   - 设置测试框架

- [ ] 2. 实现数据模型和验证
  - [ ] 2.1 创建核心数据模型接口和类型
    - 为所有数据模型编写TypeScript接口
    - 实现数据完整性验证函数

  - [ ] 2.2 实现带有验证的用户模型
    - 编写带有验证方法的用户类

  - [ ] 2.3 实现带有关系的文档模型
     - 编写带有关系处理的文档类代码

  - [ ]* 2.4 为数据模型编写单元测试
     - 为用户模型验证创建单元测试
     - 为文档模型编写单元测试
     - 为关系管理编写单元测试

- [ ] 3. 检查点 - 确保所有测试通过
  - 确保所有测试通过,如有疑问请询问用户

- [ ] 4. 创建存储机制
  - [ ] 4.1 实现数据库连接工具
     - 编写连接管理代码
     - 为数据库操作创建错误处理工具

  - [ ] 4.2 实现数据访问的存储库模式
     - 编写基础存储库接口代码
     - 实现具有CRUD操作的具体存储库
```

## Workflow

### Step 1: Gather Context

Read the following content to build comprehensive understanding:

1. **Project Code Structure**
   - Analyze existing codebase organization
   - Identify architectural patterns and conventions

2. **Project Documentation** (`.monkeycode/docs/`)
   - `INDEX.md` - Project overview
   - `ARCHITECTURE.md` - System architecture
   - Other relevant documentation files

3. **Current Feature Design** (`.monkeycode/specs/[feature-name]/design.md`)
   - Read the design specification for the current feature
   - Understand requirements, architecture, and components

4. **Historical Feature Specs** (`.monkeycode/specs/*/*.md`)
   - **IMPORTANT**: First use Glob to list all subdirectories under `.monkeycode/specs/`
   - Only read specifications from related historical features based on subdirectory names
   - Avoid reading too many unrelated files to prevent context overflow

### Step 2: Generate Task List

Create a detailed implementation plan following these **CRITICAL CONSTRAINTS**:

#### Format Requirements

- **Output ONLY the task list template content** - no additional sections or commentary
- **Maximum 2 levels of hierarchy**:
  - Top-level items (epics) - use only when needed
  - Sub-tasks with decimal numbering (e.g., 1.1, 1.2, 2.1)
- **Every item must be a checkbox**
- **Prefer simple, flat structure when possible**

#### Task Content Requirements

Each task must include:
- **Clear objective** describing what code to write, modify, or test
- **Additional details** as sub-bullets under the task
- **References to specific requirements** from the design document (reference fine-grained sub-requirements, not just user stories)

#### Testing Strategy

**CRITICAL TESTING PATTERNS**:

1. **Property-Based Testing**
   - Write property-based tests for universal attributes all inputs should have
   - Unit tests and property tests are complementary:
     - Unit tests catch specific errors
     - Property tests verify general correctness

2. **Test Task Organization**
   - Testing tasks MUST NOT exist as standalone top-level tasks
   - Testing tasks MUST be sub-tasks under parent implementation tasks
   - Testing sub-tasks are marked as **optional** with suffix "*" to indicate they're not required for core functionality

3. **Optional Task Marking**
   - Testing-related sub-tasks include: unit tests, property tests, integration tests
   - **Top-level tasks MUST NEVER have "*" suffix**
   - **Only sub-tasks can have "*" suffix**
   - ❌ WRONG: `- [ ]* 2. 设置项目结构和核心接口`
   - ✅ CORRECT: `- [ ]* 2.2 编写集成测试` (as a sub-task)

4. **Optional Task Categories**
   - Property-based tests
   - Unit tests
   - Integration tests
   - Test utilities and fixtures
   - Other supporting test infrastructure

5. **Task Execution Rules**
   - **Core implementation tasks must NEVER be marked as optional**
   - **Optional tasks (marked with *) should NOT be implemented by the agent**
   - **Required tasks (no *) MUST be implemented by the agent**
   - Example:
     - `- [ ]* 2.2 编写集成测试` → Agent skips this
     - `- [ ] 2.2 为存储库操作编写单元测试` → Agent must implement this

#### Planning Principles

- **Discrete, manageable coding steps** - each task should be a single, focused action
- **Reference specific requirements** - link each task to design document requirements
- **Avoid excessive implementation details** - design document already covers those
- **Assume all context is available** - requirements and design docs will be accessible during implementation
- **Progressive building** - each step builds upon previous steps
- **Cover all codeable aspects** - ensure the plan addresses everything that can be implemented

#### Checkpoints

- Include checkpoint tasks at reasonable breakpoints
- Checkpoint task format: `"确保所有测试通过,如有疑问请询问用户"`
- Multiple checkpoints are allowed
- Checkpoints ensure code quality before proceeding

#### Implementation-First Development

- **Implement functionality BEFORE writing corresponding tests**
- **Validate core functionality early** through code execution
- Focus on making features work first, then ensure they work correctly

#### Scope Boundaries

**Tasks MUST be actionable by a coding agent:**
- Writing, modifying, or testing specific code components
- Specifying files or components to create/modify
- Specific enough to execute without additional clarification
- Focused on implementation details, not high-level concepts
- Scoped to concrete coding activities (e.g., "Implement X function" not "Support X feature")

**Tasks MUST NOT include non-coding activities:**
- ❌ User acceptance testing or feedback collection
- ❌ Deployment to production/staging environments
- ❌ Performance metrics collection or analysis
- ❌ Running the application for end-to-end testing (but automated E2E tests are OK)
- ❌ User training or documentation creation
- ❌ Business process or organizational changes
- ❌ Marketing or communication activities
- ❌ Anything that cannot be completed by writing/modifying/testing code

#### Coverage and Quality

- **Ensure all requirements are covered** in implementation tasks
- **Proactively identify gaps** - if gaps are found during planning, suggest returning to requirements or design phase
- **Translate correctness properties** into property-based tests
  - Each property in its own separate sub-task
  - Place property tasks close to implementation for early error detection
  - Annotate with property number and requirement clause reference
  - Explicitly reference the design document property being checked

### Step 3: User Review and Iteration

After generating the initial task list:

1. **Ask for Additions** using the AskUserQuestion tool:
   - Question: "对当前的任务列表是否有需要补充的内容?"
   - If user requests changes or doesn't explicitly approve, go back to Step 2
   - If user explicitly approves, proceed to next step

2. **Ask about Optional Tasks** using the AskUserQuestion tool:
   - Question: "任务列表中默认将一些非开发任务(例如测试、文档)标记为可选,以便优先关注核心功能。是否要在本次实施过程中执行这些任务?"
   - Options:
     - "目前只执行开发任务,将其他任务标记为可选" (keep "*" markers)
     - "执行所有任务" (remove "*" markers)
   - If tool unavailable, send message to user and wait for response
   - If user wants all tasks executed, remove all "*" markers to make them required

### Step 4: Write Task List

Write the final task list to:
```
.monkeycode/specs/{FEATURE_NAME}/tasklist.md
```

## Output File Structure

```
.monkeycode/specs/{FEATURE_NAME}/
├── requirements.md    # Feature requirements (from previous phase)
├── design.md          # Technical design (from previous phase)
└── tasklist.md        # Implementation plan (generated by this skill)
```

## Quality Checklist

Before finalizing the task list, verify:

- [ ] Uses maximum 2 levels of hierarchy
- [ ] All items are checkboxes
- [ ] Testing tasks are sub-tasks, not top-level
- [ ] Optional tasks marked with "*" suffix (only sub-tasks)
- [ ] Top-level tasks have NO "*" suffix
- [ ] Each task references specific requirements
- [ ] Tasks are actionable by coding agents
- [ ] No non-coding activities included
- [ ] Checkpoints included at reasonable intervals
- [ ] All design aspects covered
- [ ] Progressive, buildable task sequence

## Notes

- All communication uses the project's configured language
- If gaps are found during planning, proactively suggest returning to requirements/design phase
- Focus on creating actionable, executable tasks for coding agents
- Balance detail with clarity - provide enough context without over-specifying implementation
