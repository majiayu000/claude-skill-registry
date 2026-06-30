---
name: ase-task-condense
argument-hint: "[--help|-h] [--next|-n <option>[,...]] [<id>]"
description: >
    Condense the current or given task plan by compressing its wording.
    Use when the user calls to "condense", "compress", "shrink" or
    "shorten" the "task", "plan", "spec", or "specification".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-task-condense">
Condense a Task Plan
</skill>

<expand name="getopt"
    arg1="ase-task-condense"
    arg2="--next|-n=(none|DONE|EDIT|IMPLEMENT|PREFLIGHT)...">
    $ARGUMENTS
</expand>

<objective>
*Condense* the task plan by removing fluff while preserving all
semantics exactly.
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
            ⧉ **ASE**: ☻ skill: **ase-task-condense**, ▶ ERROR: expected single `[<id>]` argument
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

        Set <words-before><words/></words-before> (remember the loaded
        word count for the strictly-smaller check in step 3).

        <if condition="<content/> contains '⎈   Created:  <text/>'">
        Set <timestamp-created><text/></timestamp-created> (extract the
        original creation timestamp so it can be re-inserted unchanged
        into the condensed <content/> in step 3).
        </if>

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

3.  **Condense Task Plan:**

    1.  *Apply the condense ruleset* to <content/>, producing a shorter
        <content/>. The goal is to make the plan require as *little
        reading* as possible while all semantics remain *fully preserved
        and unchanged*. Honor the following ruleset *strictly*:

        1.  *Preserve-exactly (never alter)*: the plan <format/>
            structure (the headings `#`/`##`, all three `##  CONTEXT`,
            `##  CHANGES`, and `##  VERIFICATION` sections, the
            `Created:`/`Modified:` lines, and
            the `- **<aspect/>**:` bullet labels), all *code spans* and
            code blocks, technical terms, file paths, identifiers,
            numbers, severities (`LOW`/`MEDIUM`/`HIGH`/`ACCEPTED`), and
            the `*<aspect/>*` emphasis highlighting convention.

        2.  *Compress free-text only* (the `**WHAT**`/`**WHY**` prose and
            each bullet's `<specification/>` text):
            -   *Drop* filler ("just", "really", "basically", "simply"),
                pleasantries, and hedging ("I think", "maybe", "perhaps").
            -   *Use* shorter synonyms and common abbreviations.
            -   *Use* `→` for causality and `-` for short subsequent facts.
            -   *Drop* articles ("a", "an", "the") and *replace*
                conjunctions with short separate clauses where this
                shortens the text without introducing ambiguity.
            -   *Re-wrap* the shortened free-text to the ~120-character-
                per-line convention.
            -   *Merge* genuinely-redundant bullets (the same aspect
                restated) and *drop* pure duplication - but *only* when
                truly redundant; *never* lose a distinct aspect.

        3.  *Persona override*: this condense ruleset *always wins* for
            the plan content. This ruleset-based compression is applied
            *regardless* of the currently active session persona style.

        4.  *Hard guardrail - semantics preserved EXACTLY*: condensing
            *only* shortens wording. It *MUST NOT* drop, merge (except
            truly-redundant bullets per sub-item 2), reorder, or alter
            *any* factual claim, requirement, file path, rule, or
            example. If a shortening would change meaning, *keep the
            longer wording*.

    2.  *Persist only if smaller*: calculate the number of words <words/>
        of the condensed <content/>.

        -   <if condition="<words/> is strictly smaller than <words-before/>">
            Update <timestamp-modified/> with the current time in
            ISO-style format, which has to be determined by calling
            the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool
            of the `ase` MCP server and use the `text` field of
            its response. Keep the original <timestamp-created/>,
            re-insert the current <ase-task-id/> and the refreshed
            <timestamp-modified/> into <content/>.

            Call the `ase_task_save(id: "<ase-task-id/>", text:
            "<content/>")` tool of the `ase` MCP server to save the
            condensed task plan content. Do not output anything related
            to this MCP call except the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan condensed**
            </template>
            </if>

        -   <if condition="<words/> is NOT strictly smaller than <words-before/>">
            Do *not* save and do *not* bump the timestamp. Only output
            the following <template/>:

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan already condensed**
            </template>
            </if>

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
                ⧉ **ASE**: ☻ skill: **ase-task-condense**, ▶ ERROR: invalid `--next` token: **<head/>**
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
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan condensed -- done**
            </template>

        -   If <result/> is `EDIT`:
            Set <args></args> (set args to empty).
            <if condition="the condensed plan was saved via `ase_task_save` in step 3">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            tool `Skill(skill: "ase:ase-task-edit", args: "<args/>")`
            to invoke the `ase:ase-task-edit` skill in order to *edit*
            the condensed plan. Immediately stop processing the current
            skill once the `Skill` tool was used.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan condensed -- hand-off to edit**
            </template>

        -   If <result/> is `IMPLEMENT`:
            Set <args></args> (set args to empty).
            <if condition="the condensed plan was saved via `ase_task_save` in step 3">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-implement", args: "<args/>")` tool
            to *apply* the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan condensed -- hand-off to implementation**
            </template>

        -   If <result/> is `PREFLIGHT`:
            Set <args></args> (set args to empty).
            <if condition="the condensed plan was saved via `ase_task_save` in step 3">
                Set <args>--int-reuse-task</args>.
            </if>
            <if condition="<getopt-option-next/> is not equal `none`">
                Set <args><args/> --next <getopt-option-next/></args>
            </if>
            Only output the following <template/> and then call the
            `Skill(skill: "ase:ase-task-preflight", args: "<args/>")` tool
            to *apply* the plan.

            <template>
            ⧉ **ASE**: ◉ task: **<ase-task-id/>**, ✪ plan: **<words/>** words, ▶ status: **plan condensed -- hand-off to pre-flight**
            </template>
