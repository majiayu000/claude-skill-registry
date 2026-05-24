---
name: tech-research-skill-builder
description: >
  Research latest library documentation, industry best practices, and technical knowledge
  to automatically generate project-level skills. Use when asked to: (1) Research and
  create a skill for a library/framework, (2) Build a skill based on architectural patterns,
  (3) Generate skills from technical research, (4) Create domain-specific technical skills
  from web research, or (5) Any request combining research with skill creation.
---

# Tech Research Skill Builder

Automatically research technical topics and generate comprehensive project-level skills with the latest documentation and best practices.

## Overview

This skill enables automated creation of project-level skills through web research. It:
1. Conducts comprehensive web research on specified technical topics
2. Gathers library documentation, best practices, and code examples
3. Structures findings into an organized skill format
4. Generates a complete, ready-to-use skill package

## Workflow

### Step 1: Parse Request and Plan Research

When a user requests skill creation, identify:
- **Topic**: The library, framework, or technical domain to research
- **Scope**: What aspects to cover (API docs, patterns, best practices)
- **Output location**: Where to create the skill (default: `.claude/skills`)

### Step 2: Execute Comprehensive Research

Conduct research across four categories:

#### 1. Library Documentation
Search for:
- Official documentation (latest version)
- API references and method signatures
- Getting started guides
- Migration guides

**Example searches:**
- `[topic] official documentation 2025`
- `[topic] API reference latest`
- `[topic] getting started guide`

#### 2. Best Practices
Search for:
- Industry standards and conventions
- Production deployment guidelines
- Security best practices
- Performance optimization

**Example searches:**
- `[topic] best practices 2025`
- `[topic] production deployment`
- `[topic] industry standards`

#### 3. Code Examples
Search for:
- Real-world usage patterns
- Common implementations
- Integration examples
- Sample projects

**Example searches:**
- `[topic] code examples`
- `[topic] common patterns`
- `[topic] example project github`

#### 4. Architectural Patterns
Search for:
- Design patterns
- Architecture decisions
- Scalability patterns
- Implementation strategies

**Example searches:**
- `[topic] architecture patterns`
- `[topic] design patterns`
- `[topic] implementation strategies`

**For detailed research strategies**, see [research-workflow.md](references/research-workflow.md).

### Step 3: Structure Research Data

Organize findings into this format:

```json
{
  "topic": "Topic name",
  "metadata": {
    "name": "topic-name",
    "description": "Comprehensive description with triggers"
  },
  "library_docs": [
    {
      "title": "Doc title",
      "summary": "Overview",
      "url": "Source URL",
      "key_points": ["Point 1", "Point 2"],
      "content": "Detailed content"
    }
  ],
  "best_practices": [
    {
      "category": "Category name",
      "description": "Practice description",
      "guidelines": ["Guideline 1", "Guideline 2"],
      "source": "Source URL"
    }
  ],
  "code_examples": [
    {
      "title": "Example title",
      "description": "What it demonstrates",
      "code": "Code snippet",
      "language": "python",
      "source": "Source URL"
    }
  ],
  "architectural_patterns": [
    {
      "name": "Pattern name",
      "description": "Pattern overview",
      "use_cases": ["Use case 1", "Use case 2"],
      "trade_offs": "Pros and cons",
      "source": "Source URL"
    }
  ]
}
```

Save this structured data to a temporary JSON file for skill generation.

### Step 4: Generate Skill Package

Use the `generate_skill.py` script to create the skill:

```bash
python .claude/skills/tech-research-skill-builder/scripts/generate_skill.py \
  /tmp/research_data.json \
  .claude/skills
```

This generates:
- **SKILL.md**: Core skill file with frontmatter and navigation
- **references/core-concepts.md**: Fundamental concepts and terminology
- **references/patterns.md**: Implementation patterns and code examples
- **references/best-practices.md**: Production guidelines and recommendations
- **references/api-reference.md**: Detailed API documentation

**For skill generation guidelines**, see [skill-generation-guide.md](references/skill-generation-guide.md).

### Step 5: Validate and Package

After generation:

1. **Validate the skill structure**:
   ```bash
   python /root/.claude/skills/skill-creator/scripts/quick_validate.py \
     .claude/skills/[generated-skill-name]
   ```

2. **Package the skill** (if validation passes):
   ```bash
   python /root/.claude/skills/skill-creator/scripts/package_skill.py \
     .claude/skills/[generated-skill-name]
   ```

3. **Report to user**: Provide the skill location and .skill file path

## Example Usage

### Example 1: Library-Specific Skill

**User request:**
> "Research FastAPI and create a skill for it"

**Workflow:**
1. Parse: Topic = "FastAPI", Scope = comprehensive
2. Research:
   - FastAPI official docs (latest version)
   - Best practices for production deployment
   - Common patterns (authentication, database integration)
   - Architecture examples
3. Structure: Organize into JSON format
4. Generate: Create skill at `.claude/skills/fastapi`
5. Validate and package: Create `fastapi.skill` file

### Example 2: Architectural Pattern Skill

**User request:**
> "Create a skill for microservices architecture patterns"

**Workflow:**
1. Parse: Topic = "microservices architecture", Scope = patterns
2. Research:
   - Microservices design patterns
   - Best practices for service communication
   - Code examples (API gateways, service mesh)
   - Architecture decisions (monolith vs microservices)
3. Structure: Organize findings
4. Generate: Create skill at `.claude/skills/microservices-architecture`
5. Validate and package

### Example 3: Domain-Specific Technical Skill

**User request:**
> "Research authentication best practices and build a skill"

**Workflow:**
1. Parse: Topic = "authentication", Scope = best practices
2. Research:
   - Authentication patterns (OAuth, JWT, sessions)
   - Security best practices
   - Implementation examples
   - Industry standards
3. Structure: Organize by authentication type
4. Generate: Create skill at `.claude/skills/authentication`
5. Validate and package

## Quality Criteria

Generated skills should meet these standards:

- **Current information**: From 2025 or latest version
- **Comprehensive coverage**: All major aspects of the topic
- **Practical examples**: Real-world code and patterns
- **Clear organization**: Logical structure with navigation
- **Valid structure**: Passes skill validation
- **Proper triggers**: Description includes when to use

## Research Depth Guidelines

Adjust research depth based on topic complexity:

**Quick (20-30 min)**: Simple libraries, basic patterns
- 3-5 sources per category
- Focus on official docs
- Basic examples

**Medium (1-2 hours)**: Standard frameworks, common patterns
- 10-15 sources per category
- Include community resources
- Multiple examples

**Deep (3-4 hours)**: Complex systems, architectural patterns
- 20+ sources per category
- Comprehensive coverage
- Edge cases and advanced topics

## Troubleshooting

### Research yields limited results
- Broaden search terms
- Include alternative names for the technology
- Search for related technologies/patterns

### Generated skill has gaps
- Conduct targeted follow-up research
- Manually add missing sections
- Update research data and regenerate

### Validation fails
- Check SKILL.md frontmatter format
- Ensure description is comprehensive
- Verify all reference files are linked

## Advanced Usage

### Custom Research Scope

Modify the research categories in `scripts/research_and_build_skill.py` to focus on specific aspects:

```python
def collect_research_requirements(self) -> Dict[str, List[str]]:
    return {
        "security_practices": [...],  # Custom category
        "performance_optimization": [...],
        # Add or remove categories as needed
    }
```

### Multiple Topic Skills

For skills covering multiple related topics:
1. Research each topic separately
2. Merge research data
3. Organize references by topic
4. Generate unified skill

### Skill Updates

To update an existing skill with new research:
1. Conduct fresh research
2. Merge with existing content
3. Regenerate skill
4. Replace old skill with updated version
