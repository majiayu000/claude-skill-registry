---
name: create-skill
description: "Create a new skill or update an existing skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. Use when the user asks to \"create a skill\", \"make a new skill\", \"build a skill\", \"scaffold a skill\", \"write a skill for...\", or \"new skill that does...\"."
---

# Create Skill

This skill guides the creation of effective skills. For conceptual background, structure details, and writing best practices, read [references/best-practices.md](references/best-practices.md).

## Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

## Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

## Step 3: Initializing the Skill

Skip this step if the skill being developed already exists and iteration is needed. In this case, continue to the next step.

When creating a new skill from scratch, create the skill directory with:

- A `SKILL.md` file with proper YAML frontmatter (`name` and `description`) and TODO placeholders for the body
- Resource directories as needed: `scripts/`, `references/`, and/or `assets/`

After initialization, customize or remove the generated files as needed.

## Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Read [references/best-practices.md](references/best-practices.md) for writing style, structure, and content guidelines before writing SKILL.md.

## Step 5: Review the Skill

After writing all files, spawn a subagent (`model: "opus"`, do not set `run_in_background`) to review the skill. The subagent should:

1. Read [references/skill-reviewer.md](references/skill-reviewer.md) for review guidelines
2. Read all skill files (SKILL.md and any bundled resources)
3. Produce a review report following the format in the guidelines

## Step 6: Run `/evaluate-findings` Skill

Do not blindly apply all review findings. Run the `/evaluate-findings` skill on the reviewer's recommendations if available.

## Step 7: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results. Present the result to the user.
