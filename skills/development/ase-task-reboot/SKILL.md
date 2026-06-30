---
name: ase-task-reboot
argument-hint: "[--help|-h] [--next|-n <option>[,...]] [<id>]"
description: >
    Reboot the current or given task plan by re-creating it from scratch.
    Use when the user calls to "reboot", "recreate" or "refresh"
    the "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-reboot">
Reboot a Task Plan
</skill>

<expand name="getopt"
    arg1="ase-task-reboot"
    arg2="--next|-n=(none|DONE|EDIT|IMPLEMENT|PREFLIGHT)...">
    $ARGUMENTS
</expand>

<objective>
*Reboot* the task plan by crafting it from scratch,
based on the existing *WHAT* and *WHY*.
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

        2.  <elseif condition="<instruction/> is NOT empty">
            The argument is neither empty nor a valid task id. As this
            skill only accepts an optional `[<id>]` argument and *never*
            a free-text instruction, only output the following <template/>
            and then immediately *STOP* processing the entire current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-reboot**, ▶ ERROR: expected single `[<id>]` argument
            </template>
            </elseif>

2.  **Determine Operation:**

    1.  Call the `ase_task_load(id: "<ase-task-id/>")` tool of the `ase` MCP
        server to load the current task plan content and set <text/> to
        the `text` output field of the `ase_task_load` tool call.

        -   If <text/> starts with `ERROR:` or `WARNING:`:
            Set <content></content> (set content to empty).
            Set <words/> to "0".

        -   If <text/> starts NOT with `ERROR:` and NOT with `WARNING:`:
            Set <content><text/></content> (set content to text).
            Calculate the number of words <words/> of <content/>.

        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan loaded**
        </template>

    2.  <if condition="<content/> is empty">
        Complain and tell the user to use the `ase-code-resolve`,
        `ase-code-refactor`, `ase-code-craft`, or `ase-task-edit` skills
        first to create a task plan. Then immediately stop processing
        this skill.
        </if>

3.  **Reboot Task Plan:**

    1.  Start with <instruction></instruction> (set instruction to empty).

    2.  <if condition="<content/> contains neither '-   **WHAT**:' nor '-   **WHY**:'">
        Set <instruction><content/></instruction> (set instruction to content).
        </if>

    3.  <if condition="<content/> contains '-   **WHAT**: <text/>'">
        Set <instruction><text/></instruction> (set instruction to extracted text).
        </if>

    4.  <if condition="<content/> contains '-   **WHY**: <text/>' and <instruction/> is empty">
        Set <instruction><text/></instruction> (set instruction to extracted text).
        </if>

    5.  <if condition="<content/> contains '-   **WHY**: <text/>' and <instruction/> is NOT empty">
        Set <instruction><instruction/>, BECAUSE <text/></instruction>
        (append extracted text to instruction).
        </if>

    6.  <if condition="<content/> contains '⎈   Created:  <text/>'">
        Set <timestamp-created><text/></timestamp-created> (set
        timestamp-created to extracted text)
        </if>

    7.  <if condition="<instruction/> is empty or contains only whitespace">
        The WHAT/WHY extraction yielded no usable text (e.g. a
        `-   **WHAT**:` line existed but captured empty text, so the
        whole-content fallback above did not fire). Fall back to the
        full previous plan content: set <instruction><content/></instruction>
        (set instruction to content).
        <if condition="<instruction/> is still empty or contains only whitespace">
            There is nothing to reboot from. Only output the following
            <template/> and then immediately *STOP* processing the entire
            current skill:

            <template>
            ⧉ **ASE**: ☻ skill: **ase-task-reboot**, ▶ ERROR: empty instruction -- nothing to reboot from
            </template>
        </if>
        </if>

    8.  Create a new plan from scratch and store the result as
        <content/> by closely following the defined plan format
        <format/> and injecting into it all the information from
        the <instruction/> and all decisions you derived from the
        <instruction/>.

    9.  Call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the
        `ase` MCP server and use the `text` field of its response for
        <timestamp-modified/> information. If <timestamp-created/> is
        still unset (because the previous <content/> had no `Created:`
        line), set <timestamp-created><timestamp-modified/></timestamp-created>
        (fall back to the modified timestamp). Then insert the current
        <ase-task-id/>, previous <timestamp-created/>, and refreshed
        <timestamp-modified/> information and calculate the number of
        words <words/> of <content/>.

    10. Call the `ase_task_save(id: "<ase-task-id/>",
        text: "<content/>")` of the `ase` MCP server to save the updated
        task plan content. Do not output anything related to this MCP
        call.

    11. Only output the following <template/> and continue processing:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan rebooted**
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
        </template>

4.  **Decide Next Step:**

    1.  *Determine next step*:

        -   If <getopt-option-next/> is not equal to `none`:
            Treat <getopt-option-next/> as a comma-separated chronological
            list of pre-selected next-step tokens. *Split* it on `,`,
            take the *first* token as <head/>, and store the remaining
            tokens (joined back with `,`, or `none` if empty) into
            <getopt-option-next/> so downstream skills can consume the tail.

            -   If <head/> matches the regex `^(DONE|EDIT|IMPLEMENT|PREFLIGHT)$`:
                Honor the pre-selected token.
                Set <result><head/></result>.

            -   else:
                Only output the following <template/> and then immediately
                *STOP* processing the entire current skill:

                <template>
                ⧉ **ASE**: ☻ skill: **ase-task-reboot**, ▶ ERROR: invalid `--next` token: **<head/>**
                </template>

        -   If <getopt-option-next/> is equal to `none`:

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--no-other">
                Next Step: How would you like to proceed with the plan?
                DONE: Stop processing.
                EDIT: Hand off plan to editing.
                IMPLEMENT: Hand off plan to implementation.
                PREFLIGHT: Hand off plan to pre-flighting.
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
            `Skill(skill: "ase:ase-task-implement", args: "<args/>")` tool
            to *apply* the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated -- hand-off to implementation**
            </template>

        -   If <result/> is `PREFLIGHT`:
            Set <args>--int-reuse-task</args>.
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-preflight", args: "<args/>")` tool
            to *apply* the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan updated -- hand-off to pre-flight**
            </template>

