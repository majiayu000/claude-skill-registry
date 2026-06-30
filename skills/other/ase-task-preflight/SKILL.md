---
name: ase-task-preflight
argument-hint: "[--help|-h] [--next|-n <option>[,...]] [<id>]"
description: >
    Preflight the implementation of current or given task plan.
    Use when the user calls to "preflight", "dry-run" or "test-drive"
    the "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-preflight">
Preflight a Task Plan
</skill>

<expand name="getopt"
    arg1="ase-task-preflight"
    arg2="--next|-n=(none|DONE|EDIT|IMPLEMENT)... --int-reuse-task">
    $ARGUMENTS
</expand>

<objective>
*Preflight* the implementation of a task plan by creating a draft
for a corresponding, *complete source code change set*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md

Procedure
---------

1.  **Determine Task:**

    1.  Set <instruction><getopt-arguments/></instruction> initially.
        Inherit the always existing <ase-task-id/> from the current context.
        Inherit the always existing <ase-session-id/> from the current context.
        Do not output anything.

    2.  React on task id:

        1.  <if condition="
                <instruction/> matches the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`
            ">
            Set <ase-task-id><instruction/></ase-task-id> (set task
            id to instruction) and <instruction></instruction> (set
            instruction empty), call the `ase_task_id(id: "<ase-task-id/>",
            session: "<ase-session-id/>")` tool from the `ase` MCP
            server to switch the task, and then only output the
            following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task given**
            </template>
            </if>

        2.  <elseif condition="
                <instruction/> has the format `<id/>: <text/>` where
                <id/> matches the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$` and
                <text/> is *empty*
            ">
            Set <instruction></instruction> (set instruction to empty)
            and <ase-task-id><id/></ase-task-id> (set task id to
            id) and call the `ase_task_id(id: "<ase-task-id/>", session:
            "<ase-session-id/>")` tool from the `ase` MCP server to
            switch the task, and then only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task given**
            </template>
            </elseif>

        3.  <elseif condition="<instruction/> is NOT empty">
            The argument is neither empty nor a valid task id. As this
            skill only accepts an optional `[<id>]` argument and *never*
            a free-text instruction, only output the following <template/>
            and then immediately *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-preflight**, ▶ ERROR: expected single `[<id>]` argument
            </template>
            </elseif>

2.  **Determine Operation:**

    1.  Determine the current task plan content:

        <if condition="
            <getopt-option-int-reuse-task/> is equal `true`
            *and* a `ase_task_save(id: '<ase-task-id/>', ...)` tool call
            exists earlier in the current session
        ">
            Set <text/> to the `text` argument of the most recent
            `ase_task_save(id: '<ase-task-id/>', ...)` tool call,
            *without* calling `ase_task_load` again. Set <status>plan
            reused</status>. Do not output anything.
        </if>
        <else>
            Call the `ase_task_load(id: "<ase-task-id/>")` tool of the
            `ase` MCP server to load the current task plan content and
            set <text/> to the `text` output field of this `ase_task_load`
            tool call. Do not output anything related to this MCP tool
            call. Set <status>plan loaded</status>.
        </else>

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Set <content></content> (set content to empty).
            Set <words/> to "0".

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Set <content><text/></content> (set content to text).
            Calculate the number of words <words/> of <content/>.

        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **<status/>**
        </template>

    2.  If the <content/> is still empty, complain and tell the user to
        use the `ase-code-resolve`, `ase-code-refactor`, `ase-code-craft`,
        or `ase-task-edit` skills first to create a task plan. Then
        immediately stop processing this skill.

3.  **Create Implementation Draft:**

    1.  Perform a *preflight* of the *implementation* of <content/> by creating a
        draft for a corresponding, *complete artifact change set*
        which *would* fully implement the task plan <content/>. Store
        this artifact change set in *unified diff* format in <unified-diff/>.

    2.  Append this artifact change set <unified-diff/> to the end
        of the <content/> with the following <template/>. If a section
        named `##  IMPLEMENTATION DRAFT` already exists from a
        previous run of this skill, *replace* this entire existing
        section.

        <template>

        ##  IMPLEMENTATION DRAFT

        ```text
        <unified-diff/>
        ```

        </template>

    3.  <if condition="<content/> contains '⚙   Modified:'">
        Update <timestamp-modified/> with the current time in
        ISO-style format, which has to be determined by calling the
        `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the `ase`
        MCP server and use the `text` field of its response. Update
        the `⚙   Modified: ...` line of <content/> with the new
        `⚙   Modified: <timestamp-modified/>`.
        Do not output anything.
        </if>

    4.  Finally, call the `ase_task_save(id: "<ase-task-id/>",
        text: "<content/>")` of the `ase` MCP server to save the updated
        task plan content. Calculate the number of words <words/> of
        <content/>. Do not output anything related to this MCP tool call
        except the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated**
        </template>

4.  **Decide Next Step:**

    1.  *Determine next step*:

        -   If <getopt-option-next/> is not equal to `none`:
            Treat <getopt-option-next/> as a comma-separated chronological
            list of pre-selected next-step tokens. *Split* it on `,`,
            take the *first* token as <head/>, and store the remaining
            tokens (joined back with `,`, or `none` if empty) into
            <getopt-option-next/> so downstream skills can consume the tail.

            -   If <head/> matches the regex `^(DONE|EDIT|IMPLEMENT)$`:
                Honor the pre-selected token.
                Set <result><head/></result>.

            -   else:
                Only output the following <template/> and then immediately
                *STOP* processing the entire current skill:

                <template>
                ⧉ **ASE**: ☻ skill: **ase-task-preflight**, ▶ ERROR: invalid `--next` token: **<head/>**
                </template>

        -   If <getopt-option-next/> is equal to `none`:

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--no-other">
                Next Step: How would you like to proceed with the plan?
                DONE: Stop processing.
                EDIT: Hand processing off to editing.
                IMPLEMENT: Hand processing off to implementation.
            </expand>

    2.  Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `DONE` or `CANCEL`:
            Only output the following <template/> and then *STOP*.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated -- done**
            </template>

        -   If <result/> is `EDIT`:
            Set <args>--int-reuse-task</args>.
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            tool `Skill(skill: "ase:ase-task-edit", args: "<args/>")`
            to invoke the `ase:ase-task-edit` skill in order to *edit*
            the updated plan. Immediately stop processing the current
            skill once the `Skill` tool was used.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated -- hand-off to edit**
            </template>

        -   If <result/> is `IMPLEMENT`:
            Set <args>--int-reuse-task</args>.
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            tool `Skill(skill: "ase:ase-task-implement", args: "<args/>")`
            to invoke the `ase:ase-task-implement` skill in order to
            *implement* the updated plan. Immediately stop processing
            the current skill once the `Skill` tool was used.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated -- hand-off to implement**
            </template>

