---
name: task-to-agent-matcher
description: Matches tasks to appropriate agents by analyzing task requirements and finding agents with matching capabilities. Use when you need to assign tasks to agents or determine which agent should handle a task. Considers task type, requirements, and agent capabilities.
---

# Task-to-Agent Matcher Skill

## Instructions

1. Analyze the task to understand requirements
2. Identify task type and key requirements
3. Review available agents and their capabilities
4. Match task requirements to agent capabilities
5. Rank agents by suitability
6. Recommend best agent(s) for the task
7. Identify if new agent is needed

## Matching Process

### Step 1: Analyze Task
- Read task description, requirements, and acceptance criteria
- Identify task type (Design, Implementation, Infrastructure, Testing, etc.)
- Extract key requirements and capabilities needed
- Note any special requirements or constraints

### Step 2: Identify Task Characteristics
- **Task Type**: Design, Implementation, Infrastructure, Testing, Documentation, etc.
- **Domain**: Frontend, Backend, Database, DevOps, Security, etc.
- **Complexity**: Simple, Medium, Complex
- **Special Requirements**: Accessibility, Performance, Security, etc.

### Step 3: Review Available Agents
- List all available agents from `.cursor/agents/` directory
- For each agent, understand their capabilities
- Use agent-capability-assessor if needed for detailed assessment

### Step 4: Match Tasks to Agents
- Compare task requirements to each agent's capabilities
- Score each agent on match quality
- Consider both capability match and workflow fit

### Step 5: Make Recommendation
- Rank agents by suitability
- Recommend best agent(s)
- Identify if new agent is needed
- Note any gaps or concerns

## Matching Criteria

### Task Type Matching

**Design Tasks** → `ui-ux-designer`
- UI/UX design work
- Component design
- Layout design
- Design system work

**Implementation Tasks** → `implementation-engineer`
- Code implementation
- Feature development
- API endpoints
- Component implementation

**Infrastructure Tasks** → `infrastructure-engineer`
- Database setup
- Deployment
- CI/CD
- Environment configuration

**Specification Tasks** → `specification-writer`
- Creating specifications
- Requirements analysis
- Technical planning

**Task Breakdown** → `scrum-master`
- Breaking down specifications
- Creating task lists
- Dependency management

**Code Review** → `code-reviewer` or `code-reviewer-feedback`
- Reviewing code
- Providing feedback

**Testing Tasks** → `test-runner` or `test-writer`
- Running tests
- Writing tests

**Documentation Tasks** → `documentation`
- Creating documentation
- Writing docs

### Domain Matching

**Frontend** → `ui-ux-designer`, `implementation-engineer` (for frontend)
**Backend** → `implementation-engineer` (for backend), `api-implementer`
**Database** → `infrastructure-engineer`, `database-implementer`
**DevOps** → `infrastructure-engineer`
**Security** → `security-auditor`
**Accessibility** → `ui-ux-designer` (design), accessibility skills

## Matching Output Format

```markdown
## Task-to-Agent Matching

### Task: [Task ID and Title]
**Type**: [Task Type]
**Domain**: [Domain]
**Complexity**: [Complexity]

### Task Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Agent Matches

#### 1. [Agent Name] - [Match Quality]
**Match Score**: [Excellent/Good/Fair/Poor]
**Capabilities**:
- [Capability 1]
- [Capability 2]

**Why This Match**:
[Explanation of why this agent matches]

**Gaps/Concerns**:
[Any gaps or concerns]

#### 2. [Agent Name] - [Match Quality]
[Similar format]

### Recommendation
**Best Match**: [Agent Name]
**Alternative**: [Alternative Agent] (if applicable)
**New Agent Needed**: [Yes/No]

**Rationale**: [Why this recommendation]
```

## Examples

### Example 1: Clear Match

**Input**: Match task "TASK-010: Style the submit button"

**Output**:
```markdown
## Task-to-Agent Matching

### Task: TASK-010: Style the submit button
**Type**: Implementation (Design needed first)
**Domain**: Frontend
**Complexity**: Simple

### Task Requirements
- Create button styling
- Implement design specifications
- Ensure accessibility
- Add responsive design

### Agent Matches

#### 1. ui-ux-designer - Excellent Match
**Match Score**: Excellent
**Capabilities**:
- Creates design specifications
- Designs UI components
- Considers accessibility
- Plans responsive design

**Why This Match**:
This task needs design specifications first. ui-ux-designer specializes in creating design specs for components like buttons, including accessibility and responsive considerations.

**Gaps/Concerns**: None

#### 2. implementation-engineer - Good Match (after design)
**Match Score**: Good
**Capabilities**:
- Implements design specs
- Handles frontend implementation
- Ensures code quality

**Why This Match**:
After design is complete, implementation-engineer would implement the button styling according to design specs.

**Gaps/Concerns**: Requires design specs first

### Recommendation
**Best Match**: ui-ux-designer (for design), then implementation-engineer (for implementation)
**New Agent Needed**: No

**Rationale**: This task requires both design and implementation. ui-ux-designer should create design specs first, then implementation-engineer should implement them.
```

### Example 2: Multiple Options

**Input**: Match task "TASK-015: Set up PostgreSQL database with user and task tables"

**Output**:
```markdown
## Task-to-Agent Matching

### Task: TASK-015: Set up PostgreSQL database with user and task tables
**Type**: Infrastructure
**Domain**: Database
**Complexity**: Medium

### Task Requirements
- Set up PostgreSQL database
- Create database schema
- Create user and task tables
- Set up migrations
- Configure database connection

### Agent Matches

#### 1. infrastructure-engineer - Excellent Match
**Match Score**: Excellent
**Capabilities**:
- Handles infrastructure tasks
- Sets up databases
- Creates database schemas
- Handles deployment and configuration

**Why This Match**:
infrastructure-engineer specializes in infrastructure tasks including database setup, schema creation, and configuration.

**Gaps/Concerns**: None

#### 2. database-implementer (skill) - Good Match
**Match Score**: Good
**Capabilities**:
- Creates database schemas
- Handles migrations
- Creates data access layers

**Why This Match**:
The database-implementer skill provides database-specific capabilities, but would need to be used by an agent like infrastructure-engineer.

**Gaps/Concerns**: This is a skill, not an agent. Needs to be used by an agent.

### Recommendation
**Best Match**: infrastructure-engineer
**New Agent Needed**: No

**Rationale**: infrastructure-engineer is the best match for database infrastructure tasks. It can use the database-implementer skill for detailed database work.
```

### Example 3: New Agent Needed

**Input**: Match task "TASK-020: Create machine learning model for image classification"

**Output**:
```markdown
## Task-to-Agent Matching

### Task: TASK-020: Create machine learning model for image classification
**Type**: Implementation
**Domain**: Machine Learning / AI
**Complexity**: High

### Task Requirements
- Design ML model architecture
- Train image classification model
- Evaluate model performance
- Deploy model

### Agent Matches

#### 1. implementation-engineer - Poor Match
**Match Score**: Poor
**Capabilities**:
- General code implementation
- API and backend work
- Standard software development

**Why This Match**:
Implementation-engineer handles general implementation but doesn't specialize in machine learning.

**Gaps/Concerns**:
- Lacks ML-specific knowledge
- No ML model training experience
- No ML deployment expertise

#### 2. No other existing agents match

### Recommendation
**Best Match**: None (new agent needed)
**New Agent Needed**: Yes

**Rationale**: This task requires specialized machine learning capabilities that no existing agent has. A new ML-engineer or data-scientist agent should be created to handle this task effectively.
```

## Multi-Task Matching

When matching multiple tasks:

1. Match each task individually
2. Consider agent workload
3. Optimize assignments
4. Identify patterns

```markdown
## Multi-Task Agent Matching

### Tasks to Match
- TASK-001: [description]
- TASK-002: [description]
- TASK-003: [description]

### Task Assignments
- TASK-001 → [agent-name]
- TASK-002 → [agent-name]
- TASK-003 → [agent-name]

### Agent Workload
- [agent-name]: [number] tasks
- [agent-name]: [number] tasks

### Recommendations
[Overall recommendations and patterns]
```

## Best Practices

- **Be Thorough**: Analyze task requirements completely
- **Consider Workflow**: Match workflow fit, not just capabilities
- **Think About Dependencies**: Consider task dependencies when matching
- **Optimize Assignments**: Balance workload across agents
- **Identify Gaps**: Clearly identify when new agents are needed
- **Document Rationale**: Explain why each match was chosen
