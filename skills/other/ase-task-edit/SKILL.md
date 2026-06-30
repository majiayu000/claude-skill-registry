---
name: ase-task-edit
argument-hint: "[--help|-h] [--plan|-p <option>] [--dry|-d] [--next|-n <option>[,...]] [<id> | <id>: <instruction> | <instruction>]"
description: >
    Iteratively edit and refine a named plan for a task through a
    conversational loop. Each round, the current plan is shown and the
    user is asked whether to keep refining, mark the plan as done, or
    proceed to the implementation or preflight. Use when the user wants
    to plan a task purely through chat-driven refinement.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-edit">
Iteratively Edit a Task Plan
</skill>

<expand name="getopt"
    arg1="ase-task-edit"
    arg2="--plan|-p=(none|OVERWRITE|REFINE|PRESERVE) --dry|-d --next|-n=(none|DONE|GRILL|PREFLIGHT|IMPLEMENT)... --int-reuse-task">
    $ARGUMENTS
</expand>

<objective>
Establish and refine the *task plan* purely through a *chat-driven
loop*. The user steers each round via an interactive dialog that offers
continued refinement, finalization, or hand-off to implementation or
preflight.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md

Procedure
---------

<define name="apply-refinement">
Treat the <instruction/> as a *refinement instruction* for
the plan, and update <content/> in-place by *applying* the
requested <instruction/> to the *plan*.

When refining the plan this way, preserve the overall structure of the
plan and only modify what the user actually requested. Do *not* rewrite
unrelated sections of the plan.

Calculate the number of words <words/> of <content/>.
Set <content-dirty>true</content-dirty>.
</define>

<define name="generate-plan">
Create a new plan from scratch and store the result as
<content/> by closely following the defined plan format
<format/> and injecting into it all the information from
the <instruction/> and all decisions you derived from the
<instruction/>.

If a `CHANGELOG.md` file exists in the project (or in any
affected sub-package), the plan *MUST* include, as part of
its `##  CHANGES` section, an explicit bullet point
describing the addition of a corresponding new entry to
that `CHANGELOG.md` file, aligned with its existing style
and conventions.

<if condition="<getopt-option-dry/> is equal `true`">
You *MUST* completely omit the `##  VERIFICATION` section
(including its heading and all of its bullet points) from
<content/>.
</if>

Call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the
`ase` MCP server and use the `text` field of its response
for fresh <timestamp-created/> and <timestamp-modified/>
information. Then insert the current <ase-task-id/>,
<timestamp-created/>, and <timestamp-modified/> information
and calculate the number of words <words/> of <content/>.
Set <content-dirty>true</content-dirty>.
</define>

1.  **Determine Task and Instruction:**

    1.  Set <instruction><getopt-arguments/></instruction> initially.
        Inherit the always existing <ase-task-id/> from the current context.
        Inherit the always existing <ase-session-id/> from the current context.
        Do not output anything.

    2.  React on task and/or instruction:

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

        3.  <elseif condition="
                <instruction/> has the format `<id/>: <text/>` where
                <id/> matches the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$` and
                <text/> is *not empty*
            ">
            Set <instruction><text/></instruction> (set instruction to
            text) and <ase-task-id><id/></ase-task-id> (set task id
            to id) and call the `ase_task_id(id: "<ase-task-id/>", session:
            "<ase-session-id/>")` tool from the `ase` MCP server to
            switch the task, and then only output the following
            <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task given**
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
            </template>
            </elseif>

        4.  <elseif condition="
                <instruction/> is not empty
            ">
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task inherited**
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
            </template>
            </elseif>

        5.  <elseif condition="
                <instruction/> is empty
            ">
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task inherited**
            </template>
            </elseif>

2.  **Determine Plan:**

    1.  Determine any existing plan content:

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
            `ase` MCP server to load any existing plan content and set
            <text/> to the `text` output field of this `ase_task_load`
            tool call. Do not output anything related to this MCP tool
            call. Set <status>plan loaded</status>.
        </else>

        Set <content-dirty>false</content-dirty>.

        -   If <text/> starts with `ERROR:`:
            Silently ignore the MCP error.
            Set <content/> to empty.
            Set <words/> to "0".
            Do not output anything.

        -   If <text/> starts NOT with `ERROR:`:
            Set <content><text/></content> (set content to text).
            Calculate the number of words <words/> of <content/>.
            Only output the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **<status/>**
            </template>

    2.  <if condition="<content/> is empty AND <instruction/> is empty">
        Ask the user interactively, without a special tool, for the
        initial plan content with a single question:

        `**No plan content yet. What is the task you want to plan?**`

        Then set <instruction/> to the response of the user and only
        output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
        </template>
        </if>

    3.  <if condition="<content/> is not empty AND
            <instruction/> is not empty AND
            <instruction/> is not equal <content/>">
        *Determine previous-plan handling*:

        -   If <getopt-option-plan/> matches the regex `^(OVERWRITE|REFINE|PRESERVE)$`:
            Honor the pre-selection what to do with the previous plan.
            Set <result><getopt-option-plan/></result>.

        -   If <getopt-option-plan/> is equal to `none`:

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--other">
                Previous Plan: Should the previous plan content be overwritten, refined, or preserved?
                OVERWRITE: Continue operation, overwrite previous plan.
                REFINE: Continue operation, refine previous plan.
                PRESERVE: Cancel operation, preserve previous plan.
            </expand>

        Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `CANCEL` or `PRESERVE`:

            Only output the following <template/> and then immediately
            *STOP* processing this skill:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan preserved**
            </template>

        -   If <result/> is `OVERWRITE`:

            <expand name="generate-plan"/>

            Only output the following <template/> and continue processing:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan overwritten**
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
            </template>

        -   If <result/> is `REFINE`:

            <expand name="apply-refinement"/>

            Only output the following <template/> and continue processing:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan refined**
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
            </template>

        -   If <result/> matches `OTHER: <text/>`:

            Set <instruction><instruction/> <text/></instruction> (append
            the user's free-text hint to the existing instruction).

            <expand name="apply-refinement"/>

            Only output the following <template/> and continue processing:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan refined**
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
            </template>
        </if>

    4.  <if condition="no line of <content/> matches the case-insensitive regex `^\s*#+\s*TASK\b` AND <instruction/> is empty">
        Set <instruction><content/></instruction> (set instruction to content).
        Set <content></content> (set content to empty).
        Set <content-dirty>true</content-dirty>.
        Do not output anything.
        </if>

    5.  <if condition="<content/> is empty AND <instruction/> is not empty">
        <expand name="generate-plan"/>

        Only output the following <template/> and continue processing:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **instruction given**
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan generated**
        </template>
        </if>

3.  **Iterative Plan Refinement Loop:**

    *REPEAT* the following steps from 3.1 up to and including 3.4 in
    a *LOOP* until the user selects `DONE`, `GRILL`, `IMPLEMENT`, or
    `PREFLIGHT`, or declines/cancels in the dialog of step 3.4:

    1.  *Update timestamp*:
        <if condition="<content/> contains '⚙   Modified:' AND <content-dirty/> is 'true'">
        Update <timestamp-modified/> with the current time in
        ISO-style format, which has to be determined by calling the
        `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the `ase`
        MCP server and use the `text` field of its response. Update
        the `⚙   Modified: ...` line of <content/> with the new
        `⚙   Modified: <timestamp-modified/>`.
        Do not output anything.
        </if>

    2.  *Persist plan*:
        <if condition="<content-dirty/> is 'true'">
        Call the `ase_task_save(id: "<ase-task-id/>", text: "<content/>")` tool
        of the `ase` MCP server to persist the current plan, and then
        set <content-dirty>false</content-dirty> again. Calculate the
        number of words <words/> of <content/>. Do not output anything
        related to this MCP tool call except the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan saved**
        </template>
        </if>

    3.  *Render plan*: Treat <content/> as *verbatim* Markdown.
        Only output the following <template/>, so the user
        can read the plan and react to it. If <content/> is longer
        than 90 lines and a `##  IMPLEMENTATION DRAFT` section (from the
        companion skill `ase-task-preflight`) exists, replace the entire
        content of the `##  IMPLEMENTATION DRAFT` section with `[...]`.
        Else, do *not* truncate, summarize, or partially show the plan.
        Use the following <template/>:

        <template>
        <ase-tpl-head title="TASK"/>
        <content/>
        <ase-tpl-foot title="TASK"/>
        </template>

    4.  *Determine next step*:

        -   If <getopt-option-next/> is not equal to `none`:
            Treat <getopt-option-next/> as a comma-separated chronological
            list of pre-selected next-step tokens. *Split* it on `,`,
            take the *first* token as <head/>, and store the remaining
            tokens (joined back with `,`, or `none` if empty) into
            <getopt-option-next/> so subsequent loop iterations or
            downstream skills can consume the tail.

            -   If <head/> matches the regex `^(DONE|GRILL|IMPLEMENT|PREFLIGHT)$`:
                Honor the pre-selected token.
                Set <result><head/></result>.

                Set <instruction></instruction> (clear the instruction, as
                any instruction carried in via the arguments was already
                applied to the plan in step 2 before this loop), so that a
                later `OTHER: <text/>` refinement correctly starts from a
                *fresh* refinement instruction below.

            -   else:
                Only output the following <template/> and then immediately
                *STOP* processing the entire current skill:

                <template>
                ⧉ **ASE**: ☻ skill: **ase-task-edit**, ▶ ERROR: invalid `--next` token: **<head/>**
                </template>

        -   If <getopt-option-next/> is equal to `none`:

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--other">
                Next Step: How would you like to proceed with the plan?
                DONE: Mark plan finalized, exit planning loop.
                GRILL: Hand off plan to grilling.
                PREFLIGHT: Hand off plan to pre-flighting.
                IMPLEMENT: Hand off plan to implementation.
            </expand>

        Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `DONE`:

            *Break* out of the *loop*, only output the following <template/>
            and then *STOP*. Do *not* implement the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan finalized -- done**
            </template>

        -   If <result/> is `GRILL`:

            *Break* out of the *loop*.
            Set <args></args> (set args to empty).
            <if condition="the plan was saved via `ase_task_save` in step 3.2">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-grill", args: "<args/>")` tool
            to *grill* the finalized plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan finalized -- hand-off to grilling**
            </template>

        -   If <result/> is `PREFLIGHT`:

            *Break* out of the *loop*.
            Set <args></args> (set args to empty).
            <if condition="the plan was saved via `ase_task_save` in step 3.2">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-preflight", args: "<args/>")` tool
            to *apply* the finalized plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan finalized -- hand-off to pre-flight**
            </template>

        -   If <result/> is `IMPLEMENT`:

            *Break* out of the *loop*.
            Set <args></args> (set args to empty).
            <if condition="the plan was saved via `ase_task_save` in step 3.2">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-implement", args: "<args/>")` tool
            to *apply* the finalized plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan finalized -- hand-off to implementation**
            </template>

        -   If <result/> matches `OTHER: <text/>`:

            Set <instruction><text/></instruction> (replace existing instruction).

            <expand name="apply-refinement"/>

            Finally, only output the following <template/> and then
            *continue* the *loop* at step **3.1**!

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ⇌ instruction: **<instruction/>**, ▶ status: **plan refined**
            </template>

        -   If <result/> is `CANCEL`:

            *Break* out of the *loop*, only output the following <template/>
            and then *STOP*. Do *not* implement the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan refinement cancelled**
            </template>

