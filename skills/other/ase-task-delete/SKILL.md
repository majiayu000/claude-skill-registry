---
name: ase-task-delete
argument-hint: "[--help|-h] [<id>]"
description: >
    Delete the current or given task plan.
    Use when the user calls to "delete", "remove" or "clear" the
    "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-delete">
Delete a Task Plan
</skill>

<expand name="getopt" arg1="ase-task-delete">
    $ARGUMENTS
</expand>

<objective>
*Delete* the task plan.
</objective>

Procedure
---------

1.  **Determine Task:**

    1.  Set <id><getopt-arguments/></id> initially, with any leading and trailing
        whitespace stripped.
        Inherit the always existing <ase-task-id/> from the current context.
        Inherit the always existing <ase-session-id/> from the current context.
        Do not output anything.

    2.  <if condition="<id/> is empty">
        Set <id><ase-task-id/></id>
        Do not output anything.
        </if>

    3.  <if condition="<id/> does NOT match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-delete**, ▶ ERROR: expected single `[<id>]` argument
        </template>
        </if>

2.  **Perform Operation**:

    1.  Call the `ase_task_delete(id: "<id/>")` tool of the `ase` MCP
        server to delete the task plan content and set <text/> to the
        `text` output field of this `ase_task_delete` tool call. Do not
        output anything related to this MCP tool call.

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Set <deleted>false</deleted> and only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Set <deleted>true</deleted> and only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **task deleted**
            </template>

    2.  <if condition="<deleted/> is equal 'true' AND <id/> is equal <ase-task-id/> AND <ase-task-id/> is not equal 'default'">
        Set <ase-task-id>default</ase-task-id>. Call the `ase_task_id(id:
        "<ase-task-id/>", session: "<ase-session-id/>")` tool from the `ase`
        MCP server to switch the task to the default task. Only output
        the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task switched to default**
        </template>
        </if>

