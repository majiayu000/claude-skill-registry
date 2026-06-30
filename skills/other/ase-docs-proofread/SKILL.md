---
name: ase-docs-proofread
argument-hint: "[--help|-h] [--auto|-a] <docs-reference>"
description: >
    Analyze the documents for spelling, punctuation, or grammar errors.
    Use when the user wants to "proofread" or "spellcheck" a document.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-docs-proofread">
Analyze documents for spelling, punctuation, or grammar errors
</skill>

<expand name="getopt"
    arg1="ase-docs-proofread"
    arg2="--auto|-a">
    $ARGUMENTS
</expand>

<objective>
*Proofread* the documents of `<getopt-arguments/>` for problems in their
*spelling*, *punctuation*, or *grammar* and propose corrections.
</objective>

<flow>

1.  <step id="STEP 1: Investigation">

    First, use the following <template/> to give a hint on this step:

    <template>
    <ase-tpl-bullet-secondary/> **PROOFREADING INVESTIGATION**
    </template>

    Dispatch the investigation to a *sub-agent* via the `Agent`
    tool so that *no* investigation details leak into the user-visible
    transcript. The sub-agent performs the silent reading and checking;
    only its final structured return value is consumed here.

    For this, invoke *exactly once* the tool:

    ```text
        Agent(
            name:          "ase-docs-proofread",
            description:   "Proofread Investigation",
            subagent_type: "ase:ase-docs-proofread",
            mode:          "plan",
            prompt:        <getopt-arguments/>
        )
    ```

    Parse the single result message of the `Agent` tool as a JSON array
    and set <problems/> to that list.

    You *MUST* *NOT* output anything at all in this step 1 beyond the
    single `Agent` tool invocation.
    </step>

2.  <step id="STEP 2: Summary">

    Use the following <template/> to give a summary of the detected
    problems in <problems/>:

    <template>
    <ase-tpl-bullet-secondary/> **PROOFREADING SUMMARY**:

    | *Proofread Type* | *Proofread Result*      |
    | ---------------- | ----------------------- |
    | **SPELLING**:    | **<n/>** problems found |
    | **PUNCTUATION**: | **<m/>** problems found |
    | **GRAMMAR**:     | **<k/>** problems found |

    </template>

    Hints:

    -   <n/> is the number of problems with `type` equal to `SPELLING`    in <problems/>
    -   <m/> is the number of problems with `type` equal to `PUNCTUATION` in <problems/>
    -   <k/> is the number of problems with `type` equal to `GRAMMAR`     in <problems/>

    </step>

3.  <step id="STEP 3: Correction">

    1.  *Mark this skill as the active edit-capable skill* so that the
        ASE `pre-tool-use` hook auto-approves the subsequent `Edit`
        invocations on *any* invocation path (slash command *or* `Skill`
        tool). Call the `ase_config_set(key: "agent.skill", val:
        "ase-docs-proofread", scope: "session:<ase-session-id/>")` tool
        from the `ase` MCP server. Do not output anything in this substep.

        *Critical safety invariant*: the marker set here grants `Edit`
        auto-approval and *MUST* be cleared again (substep 3 below)
        *before* this skill yields control, *regardless* of how the
        iteration in substep 2 ends - whether it completes normally,
        is aborted early (e.g. an `Edit` failure, an unparseable value,
        or any other unexpected condition), or is otherwise interrupted.
        If you ever stop or bail out of substep 2 early, you *MUST*
        still perform substep 3 first. Never leave this marker active
        for a later, unrelated `Edit`.

    2.  Iterate over all problems:

        <for items="<problems/>">

        1.  Set <type/>           to the `type` field of <item/>.
            Set <file/>           to the `file` field of <item/>.
            Set <line/>           to the `line` field of <item/>.
            Set <description/>    to the `description` field of <item/>.
            Set <context-before/> to the `context_before` field of <item/>.
            Set <old-text/>       to the `old_text` field of <item/>.
            Set <new-text/>       to the `new_text` field of <item/>.
            Set <context-after/>  to the `context_after` field of <item/>.

        2.  Report the problem with the following <template/>:

            <template>
            <ase-tpl-bullet-signal/> **<type/> PROBLEM**: `<file/>`:<line/>:

            <description/>
            </template>

        3.  <if condition="<getopt-option-auto/> is not 'true'">

            Determine the hunk *body* as an ordered list of lines, each
            carrying a one-character prefix (` ` for context, `-` for
            old-side, `+` for new-side). Build it by concatenating, in
            order and *skipping any part that is empty*:

            - one ` `-prefixed line for *each* line of <context-before/>
              (if non-empty),
            - one `-`-prefixed line for *each* line of <old-text/>
              (if non-empty; split <old-text/> on newlines),
            - one `+`-prefixed line for *each* line of <new-text/>
              (if non-empty; split <new-text/> on newlines),
            - one ` `-prefixed line for *each* line of <context-after/>
              (if non-empty).

            Set <hunk-body/> to those prefixed lines joined by newlines.

            Set <old-count/> to the number of old-side hunk lines, i.e.,
            the combined line count of <context-before/>, <old-text/>, and
            <context-after/> (each empty part counts as `0`).
            Set <new-count/> to the number of new-side hunk lines, i.e.,
            the combined line count of <context-before/>, <new-text/>, and
            <context-after/> (each empty part counts as `0`).

            Set <old-start/> to the 1-based line number of the *first*
            old-side hunk line: if <context-before/> is non-empty, that is
            its line (one before <line/>); otherwise it is <line/> itself
            (the first line of <old-text/>). For a hunk that *only inserts*
            new lines (empty <old-text/> *and* empty context), set it to the
            line *before* which the insertion happens, clamped to a minimum
            of `0`, so a top-of-file insertion yields `@@ -0,0 ... @@`.
            Set <new-start/> to the same value as <old-start/>, but clamped
            to a minimum of `1` whenever <new-count/> is greater than `0`
            (the corrected side then has a real first line).

            Render the proposed correction as a *unified diff* with *up to
            two* lines of context in a fenced block based on the following
            <template/>, emitting <hunk-body/> verbatim (one already-prefixed
            line per line, with no extra blank or space-only lines):

            <template>

            <ase-tpl-bullet-normal/> **<type/> CORRECTION**:

            ```diff
            --- <file/> (original)
            +++ <file/> (corrected)
            @@ -<old-start/>,<old-count/> +<new-start/>,<new-count/> @@
            <hunk-body/>
            ```

            </template>

            </if>

        4.  <if condition="<getopt-option-auto/> is not 'true'">

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--other">
                CORRECTION: How would you like to proceed with this proposed correction?
                ACCEPT: Apply the proposed correction.
                REJECT: Skip this proposed correction.
            </expand>

            </if>

            <else>

            Set <result>ACCEPT</result>.

            </else>

        5.  Check <result/> and dispatch accordingly:

            -   <if condition="<result/> is 'ACCEPT'">

                Invoke the `Edit` tool to apply the change by replacing
                <old-text/> with <new-text/> at <file/>:<line/>. The operation
                will be auto-approved by the ASE `pre-tool-use` hook (which
                tracks the active skill), so *no* interactive permission
                prompt will appear. Then continue with the next <item/>.

                </if>

            -   <if condition="<result/> starts with 'OTHER'">

                Generate a *new* proposal for the *same* <item/>,
                incorporating the user's free-text hint from <result/>
                after the "OTHER:" prefix. *Reassign* <description/>,
                <old-text/>, and <new-text/> to reflect this refined
                proposal (<old-text/> stays anchored to the existing text
                at <file/>:<line/>; <new-text/> and <description/> carry the
                refinement) so the subsequent rendering and any `Edit` use
                the new proposal rather than the original. Then *go back* to
                substep 2 of this `for`-iteration. There is *no* cap on
                refinement rounds - keep refining until the user picks
                `ACCEPT` or `REJECT`.

                </if>

            -   <if condition="
                    <result/> is 'REJECT' or
                    <result/> is 'CANCEL' or
                    <result/> starts with 'ERROR'
                ">

                Skip this <item/> without any `Edit` call and continue
                with the next <item/>.

                </if>

        </for>

    3.  *Clear the active edit-capable skill marker* now that all `Edit`
        invocations are done, so a later unrelated `Edit` is *not*
        auto-approved. Call the `ase_config_delete(key: "agent.skill",
        scope: "session:<ase-session-id/>")` tool from the `ase` MCP
        server. Do not output anything in this substep.

    4.  You *MUST* *NOT* output any further additional explanations or
        summaries at the end of this skill processing, except for the
        following final <template/>:

        <template>
        <ase-tpl-bullet-secondary/> **PROOFREAD FINISHED**
        </template>

    </step>

</flow>

