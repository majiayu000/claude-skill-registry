---
name: ase-code-craft
argument-hint: "[--help|-h] [--auto|-a] [--dry|-d] [--quick|-Q] [--next|-n <option>[,...]] [<task-id>:] <feature>"
description: >
    Craft Source:
    Use when user wants to "create", "add", or "craft" a new feature from scratch.
user-invocable: true
disable-model-invocation: false
effort: xhigh
allowed-tools:
    - "Skill"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-code-craft">
Craft Source Code
</skill>

<expand name="getopt"
    arg1="ase-code-craft"
    arg2="--auto|-a --dry|-d --quick|-Q --next|-n=(none|DONE|EDIT|PREFLIGHT|IMPLEMENT)...">
    $ARGUMENTS
</expand>

<if condition="<getopt-option-quick/> is equal `true`">
The `--quick`/`-Q` flag is a *shorthand alias*: set <getopt-option-auto/>
to `true`, <getopt-option-dry/> to `true`, and <getopt-option-next/> to
`IMPLEMENT,DELETE`. Do not output anything.
</if>

<objective>
From scratch *craft* the following feature:
<feature><getopt-arguments/></feature>
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-tenets.md

Procedure
---------

You *MUST* *NOT* call `Edit`, `Write`, `NotebookEdit`, or any
filesystem-modifying tool during this entire skill. The *only*
permitted way to persist artifacts is via `ase_task_save(...)`.

<flow>

1.  <step id="STEP 1: Reason About Feature">

    1.  <if condition="
            <feature/> matches the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`
        ">
        Set <ase-task-id><feature/></ase-task-id> (set task id to feature)
        and <feature></feature> (set feature empty), call the
        `ase_task_id(id: "<ase-task-id/>", session: "<ase-session-id/>")` tool
        from the `ase` MCP server to switch the task, and then only
        output the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **task given**
        </template>
        </if>

    2.  <if condition="
            <feature/> has the format `<id/>: <text/>` AND
            <id/> matches the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`
        ">
        Set <feature><text/></feature> and
        <ase-task-id><id/></ase-task-id> and call the `ase_task_id(id:
        "<ase-task-id/>", session: "<ase-session-id/>")` tool from the
        `ase` MCP server to implicitly switch the task. Do not output
        anything.
        </if>

    3.  <if condition="<feature/> is empty">
        Ask the user interactively, without a special tool, for the
        initial feature with a single question:

        `**No feature known yet. What is the feature you want to craft?**`

        Then set <feature/> to the response of the user.
        </if>

    4.  <if condition="
            <ase-task-id/> is equal `default` and
            <feature/> is not empty
        ">
        Set <ase-task-id/> to a unique task id, derived from <feature/>,
        which consists of two lower-case words concatenated with a
        `-` character. Then call the `ase_task_id(id: "<ase-task-id/>",
        session: "<ase-session-id/>")` tool from the `ase` MCP server to
        implicitly switch the task. Do not output anything.
        </if>

    5.  Report the task and feature with the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**
        ⧉ **ASE**: ⇌ feature: **<feature/>**
        </template>

    6.  Figure out what the requested <feature/> to be crafted is about.

    7.  Ask the user for clarification if the goal of this crafting is too
        unclear.

    8.  Do not output anything in this step, unless you asked the user.

    </step>

2.  <step id="STEP 2: Investigate Code Base">

    1.  Check the existing source files for all code which is related to the
        requested new <feature/>.

    2.  Check the architecture of the existing code base to understand the
        overall structures and dynamics.

    3.  Do not output anything in this STEP 2.

    </step>

3.  <step id="STEP 3: Internalize Crafting Tenets">

    1.  You *MUST* internalize and strictly honor the **GENERIC TENETS**,
        and the **CRAFTING TENETS** of the **ASE Tenets** when updating
        in the following. Do not output anything.

    2.  Do not output anything in this STEP 3.

    </step>

4.  <step id="STEP 4: Choose Feature Crafting Approaches">

    You *MUST* perform the following sub-steps *internally* and *without
    any output* until and including the recommendation decision. Only
    sub-steps 4-6 below are allowed to produce output, and only if
    <getopt-option-auto/> is equal `false`. If <getopt-option-auto/> is
    equal `true`, *skip* the reporting sub-steps 4-6 entirely (perform
    no output at all) to speed up processing.

    1.  *Propose* corresponding *feature approach*, including optionally,
        some *alternative* feature approaches. Do *not* output anything
        in this sub-step.

    2.  *Reflect* on and *critique* the proposed approaches by deriving,
        per approach, a small set of concrete *pros* and *cons*. Do
        *not* output anything in this sub-step.

    3.  Based on the reflection, *decide* which approach to recommend
        and annotate it with an <annotation/> of
        ` ⚝ **RECOMMENDATION** ⚝`. All other approaches receive an
        empty <annotation/>. Do *not* output anything in this sub-step.

    4.  Indicate start of reporting by showing the following <template/>:

        <template>
        <ase-tpl-head title="APPROACHES"/>
        </template>

    5.  Now report each approach with the following <template/>,
        inlining its pros/cons derived in sub-step 2, and do not output
        anything else in this step:

        <template>
        ●   **APPROACH A<n/>**<annotation/>: **<summary/>**
        ○   [...]
        ⊕   *PRO*: [...]
        ⊖   *CON*: [...]
        </template>

        Hints:

        -   Give a short one-sentence <summary/> of the feature
            approach plus *precise* and *ultra brief and concise*
            feature information. Try to keep the number of bullet points
            (`○ [...]`) in the range of 1-4.

    6.  Indicate end of reporting by showing the following <template/>:

        <template>
        <ase-tpl-foot title="APPROACHES"/>
        </template>

    7.  <if condition="<getopt-option-auto/> is not equal `true`">

        In the following, you *MUST* *NOT* use your built-in
        <user-dialog-tool/> tool! Instead, you *MUST* just show a
        custom dialog according to the expanded `custom-dialog`
        definition. You *MUST* closely follow this definition.

        Let the user choose the preferred approach A<n/> by raising
        a question with the following custom dialog, where per
        approach A<n/>, you determine an ultra brief summary
        <short-summary/> and then use the answer option `A<n/>:
        ⚝ **RECOMMENDATION** ⚝ - <short-summary/>` for your
        recommended approach plus zero or more answer options `A<n/>:
        <short-summary/>` for all other approaches:

        <expand name="custom-dialog" arg1="--no-other">
            Select Approach: Select your preferred crafting approach to follow?
            A<n/>: <short-summary/>
            [...]
        </expand>

        </if>
        <else>

        Set <n/> to the number of the feature approach A<n/> you recommend.
        Output a hint with the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ▶ status: **auto-chosen approach A<n/>**
        </template>

        </else>

    </step>

5.  <step id="STEP 5: Compose Feature Crafting Plan">

    1.  *Compose a feature plan* for the chosen feature A<n/> by
        closely aligning to the existing architecture and the existing
        code base. Use the <format/> defined for a task plan and inject
        the information from feature A<n/> and all derived realization
        decisions into it. Store the resulting task plan in <content/>.

        If a `CHANGELOG.md` file exists in the project (or in any
        affected sub-package), the plan *MUST* include, as part of its
        `## ※ CHANGES` section, an explicit bullet point describing
        the addition of a corresponding new entry to that `CHANGELOG.md`
        file, aligned with its existing style and conventions.

        <if condition="<getopt-option-dry/> is equal `true`">
        You *MUST* completely omit the `##  VERIFICATION` section
        (including its heading and all of its bullet points) from
        <content/>.
        </if>

        You *MUST* *NOT* call `Edit`, `Write`, `NotebookEdit`, or any
        filesystem-modifying tool during this step.

    2.  Call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the
        `ase` MCP server and use the `text` field of its response for
        <timestamp-created/> and <timestamp-modified/> information. Then
        insert the current <ase-task-id/>, <timestamp-created/>, and
        <timestamp-modified/> information and calculate the number of
        words <words/> of <content/>.

    3.  You then *MUST* *save* the resulting plan content with the
        `ase_task_save(id: "<ase-task-id/>", text: "<content/>")`.

    4.  Output a hint with the following <template/>:

        <template>
        ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan created**
        </template>

    5.  Directly pass-through control to the next skill:

        Treat <getopt-option-next/> as a comma-separated chronological
        list of pre-selected next-step tokens. *Peek* the *first* token
        as <head/> (or `none` if the list is `none`/empty).
        Set <args>--int-reuse-task</args>.

        1.  <if condition="<head/> is equal `DONE`">
            Consume the head: set <getopt-option-next/> to the remaining
            tokens (joined back with `,`, or `none` if empty). `DONE`
            means the freshly composed plan is finalized as-is, so do
            *not* hand off to `ase-task-edit`. Only output the following
            <template/> and then *STOP*. Do *not* implement the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan finalized -- done**
            </template>
            </if>

        2.  <elseif condition="<head/> is equal `IMPLEMENT`">
            Consume the head: set <getopt-option-next/> to the remaining
            tokens (joined back with `,`, or `none` if empty).
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Call the tool `Skill(skill: "ase:ase-task-implement", args: "<args/>")`
            to *implement* the freshly composed plan, bypassing `ase-task-edit`.
            </elseif>

        3.  <elseif condition="<head/> is equal `PREFLIGHT`">
            Consume the head: set <getopt-option-next/> to the remaining
            tokens (joined back with `,`, or `none` if empty).
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Call the tool `Skill(skill: "ase:ase-task-preflight", args: "<args/>")`
            to *preflight* the freshly composed plan, bypassing `ase-task-edit`.
            </elseif>

        4.  <else>
            Hand off to `ase-task-edit`.
            <if condition="<head/> is equal `EDIT`">
                Consume the head: set <getopt-option-next/> to the remaining
                tokens (joined back with `,`, or `none` if empty). `EDIT`
                is this skill's own dispatch token, *not* part of
                `ase-task-edit`'s `--next` vocabulary, so it must be
                stripped here rather than forwarded.
            </if>
            All remaining tokens are `ase-task-edit`'s own vocabulary
            and are forwarded verbatim, so `ase-task-edit` consumes its
            own head itself.
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Then call the tool `Skill(skill: "ase:ase-task-edit", args: "<args/>")`.
            </else>

    </step>

</flow>
