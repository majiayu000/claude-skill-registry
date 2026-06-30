---
name: ase-task-view
argument-hint: "[--help|-h] [--full|-f] [<id>]"
description: >
    View current or given task plan.
    Use when the user calls to "view", "show" or "see" the
    "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-view">
View a Task Plan
</skill>

<expand name="getopt"
    arg1="ase-task-view"
    arg2="--full|-f">
    $ARGUMENTS
</expand>

<objective>
*View* the task plan.
</objective>

Procedure
---------

1.  **Determine Task:**

    1.  Set <id><getopt-arguments/></id> initially, with any leading and trailing
        whitespace stripped.
        Inherit the always existing <ase-task-id/> from the current context.
        Do not output anything.

    2.  <if condition="<id/> is empty">
        Set <id><ase-task-id/></id>
        Do not output anything.
        </if>

    3.  <if condition="<id/> does NOT match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-view**, ▶ ERROR: expected single `[<id>]` argument
        </template>
        </if>

2.  **Perform Operation**:

    1.  Call the `ase_task_load(id: "<id/>")` tool of the `ase` MCP
        server to load the task plan content and set <text/> to the
        `text` output field of this `ase_task_load` tool call. Do not
        output anything related to this MCP tool call.

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Set <content></content> (set content to empty).
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Set <content><text/></content> (set content to text).
            Calculate the number of words <words/> of <content/>.
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ✪ plan: **<words/>** words, ▶ status: **plan loaded**
            </template>

    2.  <if condition="<content/> is not empty">
        Treat <content/> as *verbatim* Markdown.
        *Render plan*: Only output the following <template/>. If
        <getopt-option-full/> is *not* `true`, <content/> is longer than
        90 lines, and a `##  IMPLEMENTATION DRAFT` section (from the
        companion skill `ase-task-preflight`) exists, replace the entire
        content of the `##  IMPLEMENTATION DRAFT` section with `[...]`.
        Else, do *not* truncate, summarize, or partially show the plan.
        Use the following <template/>:

        <template>
        <ase-tpl-head title="TASK"/>
        <content/>
        <ase-tpl-foot title="TASK"/>
        </template>
        </if>

