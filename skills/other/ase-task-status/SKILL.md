---
name: ase-task-status
argument-hint: "[--help|-h] [<id>:] [<status>]"
description: >
    Get or set the lifecycle status of the current or given task plan.
    Use when the user wants to know or change the "status" or "state"
    of the "task" or "plan", e.g. to "close", "shelve", "cancel", or
    "re-open" it.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-task-status">
Configure Task Status
</purpose>

<expand name="getopt" arg1="ase-task-status">
    $ARGUMENTS
</expand>

<objective>
*Get* or *set* the lifecycle *status* of the task plan.
</objective>

Procedure
---------

1.  **Determine Task and Status:**

    1.  Parse <arguments><getopt-arguments/></arguments> (with any
        leading and trailing whitespace stripped) into a
        whitespace-separated list of tokens. Inherit the always
        existing <ase-task-id/> from the current context. Set
        <id><ase-task-id/></id> and <status></status> (empty). Set
        <states/> to the states of the task lifecycle model
        <ase-project-task-lifecycle/> of the current project:

        -   If <ase-project-task-lifecycle/> is `solo` (or absent):
            `OPEN`, `SHELVED`, `CLOSED`, and `CANCELLED`.

        -   If <ase-project-task-lifecycle/> is `team`:
            `PLANNING`, `SHELVED`, `IMPLEMENTING`, `STALLED`,
            `IMPLEMENTED`, and `CANCELLED`.

        -   If <ase-project-task-lifecycle/> is `enterprise`:
            `DRAFTED`, `SHELVED`, `PLANNING`, `PLANNED`, `STALLED`,
            `IMPLEMENTING`, `IMPLEMENTED`, `DECLINED`, `APPROVING`,
            `APPROVED`, `DEFERRED`, `INTEGRATING`, `INTEGRATED`, and
            `CANCELLED`.

        Do not output anything.

    2.  <if condition="<arguments/> contains two tokens">
        Set <id/> to the first token with a trailing `:` removed and
        <status/> to the second token. Do not output anything.
        </if>

    3.  <if condition="<arguments/> contains exactly one token">
        -   If the token ends with `:`:
            Set <id/> to the token with the trailing `:` removed.
        -   Else if the token, upper-cased, is one of <states/>:
            Set <status/> to the token.
        -   Else:
            Set <id/> to the token.

        Do not output anything.
        </if>

    4.  <if condition="<arguments/> contains more than two tokens">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-status**, ▶ ERROR: expected `[<id>:] [<status>]` arguments
        </template>
        </if>

    5.  <if condition="<id/> does NOT match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-task-status**, ▶ ERROR: invalid task id `<id/>` (expected `^[a-zA-Z][a-zA-Z0-9_-]*$`)
        </template>
        </if>

2.  **Perform Operation:**

    1.  <if condition="<status/> is empty">
        Call the `ase_task_status(id: "<id/>")` tool of the `ase` MCP
        server to get the lifecycle status of the task plan and set
        <text/> to the `text` output field of this tool call. Do not
        output anything related to this MCP tool call.

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ◐ status: **<text/>**
            </template>
        </if>

    2.  <if condition="<status/> is NOT empty">
        Call the `ase_task_status(id: "<id/>", status: "<status/>")`
        tool of the `ase` MCP server to set the lifecycle status of the
        task plan and set <text/> to the `text` output field of this
        tool call. Do not output anything related to this MCP tool
        call.

        -   If <text/> starts with `ERROR:`:
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ▶ status: **<text/>**
            </template>

        -   If <text/> starts with `WARNING:`:
            The status was set nevertheless. Only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ◐ status: **<status/>** (*updated*), ▶ **<text/>**
            </template>

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Strip the leading `OK: ` prefix from <text/> and only output
            the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<id/>**, ◐ status: **<status/>** (*updated*), ▶ <text/>
            </template>
        </if>

