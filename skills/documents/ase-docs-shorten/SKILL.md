---
name: ase-docs-shorten
argument-hint: "[--help|-h] [--auto|-a] (--chars|-c <N> | --words|-w <N>) <docs-reference>"
description: >
    Shorten a document toward a target length, given as either `--chars <N>` or `--words <N>`: first
    tighten the sentences, then drop low-value content, then compress the remaining content into
    shorter expressions -- each stage entered only while the target is still not met. Use when the
    user wants to "shorten", "cut down", or "reduce the length of" a document.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-docs-shorten">
Shorten a Document to a Target Length
</purpose>

<expand name="getopt"
    arg1="ase-docs-shorten"
    arg2="--auto|-a --chars|-c=0 --words|-w=0">
    $ARGUMENTS
</expand>

<objective>
*Shorten* the document of `<getopt-arguments/>` until it reaches the
requested *target length* by running three *stages* in order -- tighten
the sentences, drop low-value content, compress the remaining content
into shorter expressions -- and entering each stage *only* while the
target is still not met.
</objective>

Ground Rule
-----------

This skill *removes* text, so unlike `ase-docs-refine` it *MAY* lose
content. It still *MUST* *NOT* corrupt whatever survives: every fact,
number, technical term, qualifier, and negation which *survives* into
the shortened text stays *exactly* as it was, no content is invented,
the order of the surviving argument is kept, and fenced code blocks,
inline code spans, link targets, Markdown frontmatter, and the heading
structure are never touched.

The skill also *MUST* *NOT* shorten *beyond* the target: it stops at the
first change which reaches the target, so a document is never cut more
than the user asked for.

<flow>

1.  <step id="STEP 1: Resolve Target and Document">

    1.  Determine the *target length* from the two mutually exclusive
        options. Set <chars/> to <getopt-option-chars/> and <words/> to
        <getopt-option-words/>, treating a *non-numeric* or *negative*
        value as `0`. Then dispatch:

        -   <if condition="<chars/> is `0` and <words/> is `0`">

            Only output the following <template/> and then *IMMEDIATELY*
            *STOP* all further skill processing:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-docs-shorten**, ▶ ERROR: a target length is required -- pass either `--chars <N>` or `--words <N>`
            </template>

            </if>

        -   <if condition="<chars/> is not `0` and <words/> is not `0`">

            Only output the following <template/> and then *IMMEDIATELY*
            *STOP* all further skill processing:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-docs-shorten**, ▶ ERROR: `--chars` and `--words` are mutually exclusive -- pass only one of them
            </template>

            </if>

        -   <if condition="<chars/> is not `0`">
            Set <unit>chars</unit> and <target><chars/></target>.
            </if>
            <else>
            Set <unit>words</unit> and <target><words/></target>.
            </else>

        Do not output anything else in this substep.

    2.  *Silently* resolve `<getopt-arguments/>` to the list
        <documents/> of individual document files, expanding any
        directory or wildcard reference with the `Glob` tool. Then
        dispatch:

        -   <if condition="<documents/> is empty">

            Only output the following <template/> and then *IMMEDIATELY*
            *STOP* all further skill processing:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-docs-shorten**, ▶ ERROR: no document to shorten
            </template>

            </if>

        -   <if condition="<documents/> carries more than one document">

            A target length applies to *one* document, so a reference
            which expands to several documents is *ambiguous*: it is
            unclear whether the target bounds each document or their
            sum. Set <count/> to the number of documents, then only
            output the following <template/> and *IMMEDIATELY* *STOP*
            all further skill processing:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-docs-shorten**, ▶ ERROR: **<count/>** documents referenced -- a target length applies to exactly one document
            </template>

            </if>

        Set <file/> to the single document of <documents/>.

    3.  Do not output anything else in this STEP 1.

    </step>

2.  <step id="STEP 2: Investigation">

    <if condition="<ase-project-boxing/> is equal `black`">

    The project source artifacts are classified as a *black box*, so
    the user does *not* want them inspected or their problems surfaced.
    *Skip* the entire investigation and reporting: do *not* invoke any
    `Agent` tool and do *not* read any document, only output the
    following <template/> and then *SKIP* the remaining steps STEP 3,
    STEP 4, and STEP 5:

    <template>
    <ase-tpl-bullet-normal/> **SHORTEN**: *suppressed* (`project.boxing` is `black`)
    </template>

    </if>

    First, use the following <template/> to give a hint on this step:

    <template>
    <ase-tpl-bullet-secondary/> **SHORTENING INVESTIGATION**: `<file/>` → **<target/>** <unit/>
    </template>

    Dispatch the investigation to a *sub-agent* via the `Agent` tool so
    that *no* investigation details leak into the user-visible
    transcript. The sub-agent performs the silent reading, measuring,
    and shortening; only its final structured return value is consumed
    here. As a target length applies to exactly *one* document, exactly
    *one* sub-agent is invoked, which keeps the length budget coherent:

    ```text
        Agent(
            description:       "Shorten Investigation",
            subagent_type:     "ase:ase-docs-shorten",
            prompt:            "UNIT:   <unit/>\nTARGET: <target/>\nFILE:   <file/>",
            run_in_background: false
        )
    ```

    Parse the result message of the `Agent` tool invocation as a JSON
    object. Set <length-before/> to its `length_before` field,
    <length-projected/> to its `length_projected` field, and <blocks/>
    to its `blocks` array, ordered by ascending `line`.

    You *MUST* *NOT* output anything at all in this STEP 2 beyond the
    above hint template and the `Agent` tool invocation.
    </step>

3.  <step id="STEP 3: Summary">

    <if condition="<blocks/> is empty">

    The document already meets the target, so nothing is shortened.
    Only output the following <template/> and then *SKIP* the remaining
    steps STEP 4 and STEP 5:

    <template>
    <ase-tpl-bullet-normal/> **ALREADY SHORT ENOUGH**: **<length-before/>** <unit/> ≤ **<target/>** <unit/>
    </template>

    </if>

    Use the following <template/> to give a summary of the proposed
    shortenings in <blocks/>:

    <template>
    <ase-tpl-bullet-secondary/> **SHORTENING SUMMARY**:

    | *Shortening Stage* | *Shortening Result*      |
    | ------------------ | ------------------------ |
    | **TIGHTEN**:       | **<t/>** blocks proposed |
    | **DROP**:          | **<d/>** blocks proposed |
    | **COMPRESS**:      | **<c/>** blocks proposed |

    </template>

    Hints:

    -   <t/> is the number of blocks with `stage` equal to `TIGHTEN`  in <blocks/>
    -   <d/> is the number of blocks with `stage` equal to `DROP`     in <blocks/>
    -   <c/> is the number of blocks with `stage` equal to `COMPRESS` in <blocks/>

    </step>

4.  <step id="STEP 4: Shortening">

    1.  *Mark this skill as the active edit-capable skill* so that the
        ASE `pre-tool-use` hook auto-approves the subsequent `Edit`
        invocations on *any* invocation path (slash command *or* `Skill`
        tool). Call the `ase_config_set(key: "agent.skill", val:
        "ase-docs-shorten", scope: "session:<ase-session-id/>")` tool
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

    2.  Set <total/> to the number of blocks in <blocks/> and <index/>
        to `0`. Then iterate over all blocks:

        <for items="<blocks/>">

        1.  Increment <index/> by one (the 1-based position of the
            current <item/> within <blocks/>).
            Set <stage/>         to the `stage` field of <item/>.
            Set <line/>          to the `line` field of <item/>.
            Set <description/>   to the `description` field of <item/>.
            Set <old-text/>      to the `old_text` field of <item/>.
            Set <new-text/>      to the `new_text` field of <item/>.
            Set <block-before/>  to the `length_before` field of <item/>.
            Set <block-after/>   to the `length_after` field of <item/>.

            Then *verify the Ground Rule* for this <item/>: compare
            <new-text/> against <old-text/> and *drop* the <item/>
            entirely -- continuing with the next <item/> without any
            output -- whenever a fact, number, technical term,
            qualifier, or negation which *survives* into <new-text/> was
            altered, whenever <new-text/> states something <old-text/>
            did not, or whenever a fenced code block, an inline code
            span, a link target, or a heading was touched.

            Then set <block-delta/> to (<block-before/> -
            <block-after/>) and <block-percent/> to that difference
            expressed as a *rounded* percentage of <block-before/>, so
            the reviewer sees what the block actually saves.

            Then set <context-before/> and <context-after/> to empty and
            *normalize* the change to its *minimal* form, so that the
            proposed diff shows exactly the lines the later `Edit` will
            actually change: while the *first* line of <old-text/> is
            identical to the *first* line of <new-text/>, *move* that
            line from both to the end of <context-before/> and increment
            <line/> by one; likewise, while the *last* line of
            <old-text/> is identical to the *last* line of <new-text/>,
            *move* that line from both to the front of <context-after/>.
            Finally, *trim* <context-before/> to its *last* two lines and
            <context-after/> to its *first* two lines.

            Then, unless <ase-project-boxing/> is equal `grey` (where
            the full unified diff is suppressed and no context lines are
            rendered at all), *silently* read the current content of
            <file/> with the `Read` tool - reusing the content read
            earlier in this iteration, unless an `Edit` was applied in
            between - and set <file-lines/> to its lines, *stripped* of
            the line-number prefixes the tool adds. Set <file-lines/> to
            empty if the file cannot be read.

            Whenever <file-lines/> is non-empty, *re-derive* both
            context parts from it, so the rendered diff shows real
            context: set <context-before/> to the *up to two* lines of
            <file-lines/> directly *before* line <line/> (empty if
            <line/> is `1`) and <context-after/> to the *up to two*
            lines of <file-lines/> starting at line (<line/> + <n/>),
            where <n/> is the number of lines in <old-text/> (empty if
            that line is beyond the end of the document).

        2.  Report the proposed block with the following <template/>:

            <template>
            <ase-tpl-bullet-signal/> [<index/>/<total/>]: **<stage/> BLOCK**: `<file/>`:<line/>:

            <description/>
            </template>

        3.  <if condition="<getopt-option-auto/> is not equal `true` and <ase-project-boxing/> is equal `grey`">

            The project source artifacts are classified as a *grey box*,
            so the user does *not* want the full artifact internals
            surfaced: *suppress* the full unified diff and instead show
            only a *condensed* two-line hunk. Unlike a proofreading
            correction or a refinement, a shortening block spans whole
            paragraphs, so both sides *MUST* be *normalized* and
            *elided* onto *one* line each -- an unelided side-by-side
            collapse exceeds the terminal width and wraps into an
            unreadable run.

            Determine <old-snippet/> from <old-text/> by replacing every
            run of whitespace (line breaks included) with a *single*
            space and trimming the result, then -- only if it is longer
            than `100` characters -- keeping just its *first* `60` and
            *last* `30` characters, joined by ` […] `. Determine
            <new-snippet/> the same way from <new-text/>, or set it to
            `∅` when <new-text/> is empty for a pure removal. Then
            report the shortening with the following <template/>,
            emitting both snippet lines verbatim (no wrapping, no extra
            blank lines):

            <template>

            <ase-tpl-bullet-normal/> **<stage/> SHORTENING** (**<block-before/>** → **<block-after/>** <unit/>, **-<block-percent/>%**):

            ```diff
            - <old-snippet/>
            + <new-snippet/>
            ```

            </template>

            </if>
            <elseif condition="<getopt-option-auto/> is not equal `true`">

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
            the line of its *first* context line, i.e., <line/> minus the
            number of lines in <context-before/>; otherwise it is <line/> itself
            (the first line of <old-text/>).
            Set <new-start/> to the same value as <old-start/>, but clamped
            to a minimum of `1` whenever <new-count/> is greater than `0`
            (the shortened side then has a real first line).

            Render the proposed shortening as a *unified diff* with *up to
            two* lines of context in a fenced block based on the following
            <template/>, emitting <hunk-body/> verbatim (one already-prefixed
            line per line, with no extra blank or space-only lines):

            <template>

            <ase-tpl-bullet-normal/> **<stage/> SHORTENING** (**<block-before/>** → **<block-after/>** <unit/>, **-<block-percent/>%**):

            ```diff
            --- <file/> (original)
            +++ <file/> (shortened)
            @@ -<old-start/>,<old-count/> +<new-start/>,<new-count/> @@
            <hunk-body/>
            ```

            </template>

            </elseif>

        4.  <if condition="<getopt-option-auto/> is not equal `true`">

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition:

            <expand name="custom-dialog" arg1="--other">
                SHORTENING: How would you like to proceed with this proposed shortening?
                ACCEPT: Apply this proposed shortening.
                REJECT: Skip this proposed shortening.
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
                <old-text/>, <new-text/>, <block-before/>, and
                <block-after/> to reflect this refined proposal
                (<old-text/> stays anchored to the existing text at
                <file/>:<line/>; <new-text/> and <description/> carry the
                new shortening) so the subsequent rendering and any `Edit`
                use the new proposal rather than the original. Then
                *re-apply* the minimal-form normalization and the context
                re-derivation of substep 1 to the refined <old-text/> and
                <new-text/> (so the re-rendered diff again shows exactly
                the changed lines) and *go
                back* to substep 2 of this `for`-iteration. There is *no*
                cap on refinement rounds - keep refining until the user
                picks `ACCEPT` or `REJECT`.

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

    </step>

5.  <step id="STEP 5: Length Report">

    1.  *Silently* call the `ase_text_metric(file: "<file/>")` tool of
        the `ase` MCP server and set <length-after/> to the <unit/>
        field of its result, so the report states the *measured,
        achieved* length rather than the projected one -- rejected
        blocks otherwise falsify the numbers. Then set
        <reduction/> to (<length-before/> - <length-after/>) and
        <percent/> to that reduction expressed as a *rounded*
        percentage of <length-before/>. Do not output anything in this
        substep.

    2.  Report the achieved length with the following <template/>:

        <template>
        <ase-tpl-bullet-secondary/> **LENGTH REPORT**: `<file/>`

        | *Length Metric* | *Length Value*                             |
        | --------------- | ------------------------------------------ |
        | **BEFORE**:     | **<length-before/>** <unit/>               |
        | **AFTER**:      | **<length-after/>** <unit/>                |
        | **TARGET**:     | **<target/>** <unit/>                      |
        | **REDUCTION**:  | **<reduction/>** <unit/> (**<percent/>%**) |

        </template>

    3.  <if condition="<length-after/> is less than or equal to <target/>">

        <template>
        <ase-tpl-bullet-normal/> **TARGET MET**
        </template>

        </if>
        <else>

        Set <missed/> to (<length-after/> - <target/>).

        <template>
        <ase-tpl-bullet-signal/> **TARGET MISSED** by **<missed/>** <unit/> (rejected shortenings)
        </template>

        </else>

    4.  You *MUST* *NOT* output any further additional explanations or
        summaries at the end of this skill processing, except for the
        following final <template/>:

        <template>
        <ase-tpl-bullet-secondary/> **SHORTEN FINISHED**
        </template>

    5.  Finally, give the closing hint by expanding the following
        (which, depending on the configured <ase-guidance-level/>, may
        expand into nothing and hence emit no output at all):

        <if condition="<getopt-option-auto/> is not equal `true`">
        <ase-tpl-hint level="verbose">
        Use `/ase-docs-shorten --auto` to apply all shortenings unattended.
        </ase-tpl-hint>
        </if>

    </step>

</flow>

