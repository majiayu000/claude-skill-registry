---
name: ase-task-rename
argument-hint: "[--help|-h] [<old>] <new>"
description: >
    Rename the current or given task plan.
    Use when the user calls to "rename", "move" or "relabel" the
    "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-rename">
Rename a Task Plan
</skill>

<expand name="getopt" arg1="ase-task-rename">
    $ARGUMENTS
</expand>

<objective>
*Rename* the task plan.
</objective>

Procedure
---------

1.  **Determine Task:**

    1.  Parse <arguments><getopt-arguments/></arguments> into a whitespace-separated
        list of tokens. Inherit the always existing <ase-task-id/> and
        <ase-session-id/> from the current context. Do not output anything.

    2.  <if condition="<arguments/> contains two tokens">
        Set <old/> to the first token of <arguments/>.
        Set <new/> to the second token of <arguments/>.
        Do not output anything.
        </if>

    3.  <if condition="<arguments/> contains exactly one token">
        Set <old><ase-task-id/></old>.
        Set <new/> to the single token of <arguments/>.
        Do not output anything.
        </if>

    4.  <if condition="<arguments/> is empty OR contains more than two tokens">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-rename**, ▶ ERROR: expected `[<old>] <new>` arguments
        </template>
        </if>

    5.  <if condition="<old/> does NOT match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$` OR <new/> does NOT match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-rename**, ▶ ERROR: invalid task id (expected `^[a-zA-Z][a-zA-Z0-9_-]*$`)
        </template>
        </if>

    6.  <if condition="<old/> is equal <new/>">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ◉ task: **<old/>**, ▶ status: **task unchanged (old and new task id are equal)**
        </template>
        </if>

2.  **Perform Operation**:

    1.  Call the `ase_task_rename(old: "<old/>", new: "<new/>")` tool of the
        `ase` MCP server to rename the task plan and set <text/> to the
        `text` output field of this `ase_task_rename` tool call. Do not
        output anything related to this MCP tool call.

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Set <renamed/> to `false`.
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<old/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Set <renamed/> to `true`.
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<new/>**, ▶ status: **task renamed**
            </template>

    2.  <if condition="<renamed/> is `true` AND <old/> is equal <ase-task-id/>">
        Set <ase-task-id><new/></ase-task-id>. Call the `ase_task_id(id:
        "<ase-task-id/>", session: "<ase-session-id/>")` tool from the `ase`
        MCP server to switch the task to the renamed task. Only output
        the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task switched**
        </template>
        </if>
