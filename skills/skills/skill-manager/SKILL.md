---
name: skill-manager
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends an agent's capabilities with specialized knowledge, workflows, or tool integrations.
metadata:
  author: gohypergiant
  version: "1.0"
---

# Skill Manager

This skill provides guidance for creating and managing effective agent skills.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks. They can transform an agent into a specialized problem solver equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks
5. Best practices - Documentation and examples regarding best practices for particular subjects

## Skill Creation Workflow

To create a or refactor a skill, follow the "Skill Creation Workflow" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate-pdf.sh` script would be helpful to store in the skill

Example: When designing a `frontend-app-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend app requires the same boilerplate React/Next.js code each time
2. An `assets/hello-world/` template containing the boilerplate project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill. 

Check available skills to identify potentially relevant ones the user may have missed:

```bash
view .claude/skills    # Current project skills (if available)
view ~/.claude/skills  # Global skills (if available)
```

Look for skills related to:
- File types the command will process (docx, pdf, xlsx, pptx)
- Domain expertise (frontend-design, product-self-knowledge)
- Workflows or patterns (skill-creator, mcp-builder)

Present relevant skills to the user:
- "I found these skills that might be relevant: [list]. Should any of these be included?"
- Be concise; only mention skills with clear relevance

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

Follow the instructions and conventions outlined in the [AGENTS.md](AGENTS.md) outline as well as the references.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of an agent to use. Focus on including information that would be beneficial and non-obvious to an agent. Consider what procedural knowledge, domain-specific details, or reusable assets would help another agent instance execute these tasks more effectively.