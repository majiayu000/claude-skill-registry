---
name: ase-spec-edit
argument-hint: "[--help|-h] [--grill|-g] [--grill-rounds|-r <n>] [--verify|-v] [--worktree|-w] [--loop|-l] [<query>]"
description: >
    Edit Specification: Use when the user wants to "edit" the
    SpecBook-based specification (SPEC) in one shot from a query, with
    optional grilling, SpecBook validation, looping, and Git worktree
    isolation.
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-spec-edit">
Edit Specification
</purpose>

<expand name="getopt"
    arg1="ase-spec-edit"
    arg2="--grill|-g --grill-rounds|-r=1 --verify|-v --worktree|-w --loop|-l">
    $ARGUMENTS
</expand>

<objective>
*Edit* the specification directly from a query -- creating, revising, or
pruning its statements in one shot -- through the states *querying*,
*discovering*, *grilling*, *implementing*, and *verifying*.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-meta.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-spec.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-tenets.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-common-grill.md

Procedure
---------

This skill is *plan-less*: it *never* composes or persists a task plan
and *MUST* *NOT* call `ase_task_save(...)`. Instead, it applies the
requested edit *in place*, so the *implementing* state *requires* `Edit`
and `Write` to modify the affected artifacts. Every modification *MUST*
stay restricted to the `SPEC` artifacts the edit actually demands -- the
kinds `CODE`, `DOCS`, `TASK`, `INFR`, and `OTHR` are *never* touched.

<define name="todo-box">

On finishing the state `<arg1/>`, only output the following <template/>,
which shows the established <todo-what/> and <todo-how/>, where a still
empty <todo-what/> or <todo-how/> renders as `(none)`:

<template>
<ase-tpl-head title="EDIT TODO" subtitle="<arg1/>"/>

**WHAT**: <todo-what/>

**HOW**:  <todo-how/>

<ase-tpl-foot title="EDIT TODO" subtitle="<arg1/>"/>
</template>

</define>

1.  **Initialize:**

    1.  Set <query><getopt-arguments/></query> (with any leading and
        trailing whitespace stripped), set <todo-what></todo-what> and
        <todo-how></todo-how> (both empty), and set
        <worktree-dir></worktree-dir> (empty). Do not output anything.

    2.  If <getopt-option-grill-rounds/> is not a positive integer,
        only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ ERROR: invalid `--grill-rounds` value: **<getopt-option-grill-rounds/>**
        </template>

2.  **Iterate:**

    Perform the states (1) *querying*, (2) *discovering*, (3) *grilling*,
    (4) *implementing*, and (5) *verifying* below as one *iteration*.
    Without `--loop` perform exactly *one* iteration. Under `--loop`
    *repeat* the iteration until the *querying* state receives a
    `STOP SKILL` result. Do not output anything in this item.

3.  **State: querying:**

    1.  <if condition="<query/> is empty">

        1.  In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition. Its
            only answer option is the fixed `STOP SKILL`, so the user
            normally answers with the edit query in *one* free-text
            reply:

            <expand name="custom-dialog" arg1="--other">
                Edit Query: What is your edit query?
                STOP SKILL: stop the entire skill immediately
            </expand>

        2.  If <result/> is `STOP SKILL` or `CANCEL`, only output the
            following <template/> and then immediately *STOP* processing
            the entire current skill:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ status: **editing finished**
            </template>

            Otherwise, strip any leading `OTHER: ` prefix from
            <result/> and set <query/> to the remainder.

        </if>

    2.  Convert the <query/> *fresh* into <todo-what/> -- the
        domain-specific, non-implementation-detail information -- and
        <todo-how/> -- the remaining information -- discarding all
        <todo-what/>/<todo-how/> content of any previous iteration.
        Without `--grill` you *MUST* *NOT* ask any clarifying questions
        and during later implementation just interpret the query best-effort.
        Do not output anything.

    3.  Expand the following:

        <expand name="todo-box" arg1="current state (after querying)"></expand>

    4.  Set <query></query> (clear the query, so every further `--loop`
        iteration asks for a fresh one). Do not output anything.

4.  **State: discovering:**

    1.  Resolve the `SPEC` artifacts by calling the
        `ase_artifact_list(kind: [ "spec" ])` tool of the `ase` MCP
        server *once* and reading the returned `artifacts` array of
        `{ kind, files }` objects to obtain the project-relative file
        list. Do not output anything.

    2.  Read the **SpecBook SCHEMA Model** of the project (resolved as
        described in `ase-format-spec.md`) to learn the allowed object
        kinds, properties, nestings, and value constraints. Do not
        output anything.

    3.  Read all resolved `SPEC` artifacts which are related to
        <todo-what/> and <todo-how/>, and check the structure of the
        existing specification -- its artifacts, object kinds, ids,
        properties, descriptions, and `[[xxx]]` references -- to
        understand the overall models and their relationships. Do not
        output anything.

5.  **State: grilling:**

    Enter this state only if <getopt-option-grill/> is equal `true`;
    otherwise silently *skip* the entire state. Do not output anything
    about the skipping.

    1.  Understand what "grilling" is about:

        <expand name="grill-understanding" arg1="the edit query in <todo-what/> and <todo-how/>"></expand>

    2.  Perform <getopt-option-grill-rounds/> grilling *rounds*,
        numbered <m/> (1-<getopt-option-grill-rounds/>).

        For each round:

        1.  INITIALIZE TODO:

            Explicitly start *from scratch* from *only* the current
            <todo-what/> and <todo-how/> and *forget* all information
            gathered in previous rounds. Set <round-id/> to
            `GRILLING ROUND <m/>/<getopt-option-grill-rounds/>` if
            <getopt-option-grill-rounds/> is greater than 1, or to
            `GRILLING` otherwise (a single round needs no round
            numbering). Do not output anything.

        2.  DETERMINE QUESTIONS:

            Determine the questions, comprised of a round-local id
            <question-N-id/> of `Q<N/>` -- where <N/> restarts at `1`
            in *every* round, independent of the numbering of previous
            rounds --, and a very brief but precise question text
            <question-N-text/>. Each question is chosen to
            resolve the open points related to the above understanding
            of grilling, by focusing on the mentioned *Focus Areas*.

            For <question-N-text/> use the format `Shall...?` for
            questions of focus area `DOMAIN` and `INTERFACE`, the format
            `Should...?` for questions of focus area `ARCHITECTURE`,
            and the format `May...?` for questions of focus area
            `IMPLEMENTATION`.

            In every <question-N-text/>, encode all *literal aspects*
            -- file paths, artifact ids, object kinds, object ids,
            property keys, references, and literal values -- with
            backticks.

            Keep every <question-N-text/> at most *200 characters* long
            -- compact the text until it fits --, as a longer question
            overflows its table cell and silently degrades the entire
            table into a plain text rendering.

        3.  DETERMINE CONTEXT:

            For each question, determine its focus area
            <context-N-focus/> from the mentioned *Focus Areas*, a 1-3
            word hint <context-N-topic/>, describing what the question
            is about, and a <context-N-severity/>, describing how
            important this question is.

            Set <context-N-id/> to `DOM` for <context-N-focus/> of
            `DOMAIN`, `IFC` for <context-N-focus/> of `INTERFACE`, `ARC`
            for <context-N-focus/> of `ARCHITECTURE`, and `IMP` for
            <context-N-focus/> of `IMPLEMENTATION`.

        4.  SORT QUESTIONS:

            Finally, *sort* the questions by descending focus area
            order -- first all `DOMAIN`, then all `INTERFACE`, then all
            `ARCHITECTURE`, and then all `IMPLEMENTATION` ones -- and
            renumber <N/> according to this order, starting at `1`.
            Truncate the list after a maximum of 10 questions and set
            <n/> to the number of remaining questions. Do not output
            anything.

            Finally, assemble the <question-N/> out of
            `**<question-N-id/>** ▶ **<context-N-id/>** ▷
            **<context-N-topic/>**: <question-N-text/>`.

        5.  DETERMINE ANSWERS:

            For all remaining <question-N/>, check the specification and
            your world knowledge to find *two to three* grounded answer
            alternatives <answer-N-K/> with a question-local id
            <answer-N-K-id/> of `A<K/>` -- where <K/> restarts at `1`
            for *every* question, independent of the numbering of other
            questions --, a 1-3 word label <answer-N-K-label/>, and
            an ultra brief description <answer-N-K-description/> of
            at most *10 words*. For the answer which reflects the
            current <todo-what/>/<todo-how/> understanding, append
            ` ⚑` to its <answer-N-K-label/>.

            Assemble an <answer-N/> out of `**<answer-N-1-id/>**
            ▶ **<answer-N-1-label/>**: <answer-N-1-description/>,
            **<answer-N-2-id/>** ▶ **<answer-N-2-label/>**:
            <answer-N-2-description/>[, ...]`.

            Keep every assembled <answer-N/> at most *240 characters*
            long -- drop the least relevant alternative and compact the
            descriptions until it fits -- as a longer answer overflows
            its table cell and silently degrades the entire table into a
            plain text rendering.

        6.  INTERACTIVE DIALOG:

            In the following, you *MUST* *NOT* use your built-in
            <user-dialog-tool/> tool! Instead, you *MUST* just show a
            custom dialog according to the expanded `custom-dialog`
            definition. You *MUST* closely follow this definition. The
            dialog below carries the two fixed answer options
            `SKIP GRILLING` and `STOP SKILL`, dispatched as follows:

            -   If a <result/> is `SKIP GRILLING` or `CANCEL`, ask no
                further questions, continue with item 7 below (merging
                the answers gathered so far), and after item 8 skip all
                remaining rounds and continue with the *implementing*
                state.

            -   If a <result/> is `STOP SKILL`, only output the
                following <template/> and then immediately *STOP*
                processing the entire current skill:

                <template>
                ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ status: **editing stopped**
                </template>

            1.  Output only the following <template/> -- it lists *all*
                questions of the round up-front, one table row per
                aspect, so the subsequent dialog only has to ask for the
                combined answer. Align all column edges of the table.

                In every table cell you *MUST* escape each literal pipe
                character outside a code span as `\|` and you *MUST*
                open *and* close every backtick code span within the
                *same* cell -- an unescaped pipe or an unbalanced
                backtick run splits the cell and silently degrades the
                entire table into a plain text rendering:

                <template>
                ⧉ **ASE**: <round-id/>: *Relentless Interviewing Until Clarity*

                | QUESTION      | ANSWERS     |
                | ------------- | ----------- |
                | <question-1/> | <answer-1/> |
                | <question-2/> | <answer-2/> |
                | [...]         | [...]       |

                Legend: **DOM**: Domain (MUST), **IFC**: Interface (MUST), **ARC**: Architecture (SHOULD), **IMP**: Implementation (MAY)
                        **Qn**: round-local question id, **An**: question-local answer id, ⚑: current decision state
                </template>

            2.  Show a custom dialog. Its only answer options are the
                two fixed ones, so the user normally answers all aspects in
                *one* free-text reply:

                <expand name="custom-dialog" arg1="--other">
                    <round-id/>: What is your (combined) answer to all (or a subset) of the above questions? (keywords or `Qn:An` references are sufficient)
                    SKIP GRILLING: skip all remaining grilling and continue with the implementation
                    STOP SKILL: stop the entire skill immediately
                </expand>

                Dispatch `SKIP GRILLING`, `STOP SKILL`, and `CANCEL` as
                defined above. Otherwise, strip any leading `OTHER: `
                prefix from <result/> and treat the remainder as the
                combined free-text answers to all questions of the
                round.

        7.  MERGE ANSWERS INTO TODO:

            Merge all gathered answers in <result/> of the round -- the
            combined reply -- *exclusively* back into <todo-what/> and
            <todo-how/>. Do not output anything.

        8.  SHOW CURRENT TODO:

            Set <round-suffix/> to
            ` round <m/>/<getopt-option-grill-rounds/>` if
            <getopt-option-grill-rounds/> is greater than 1, or to
            empty otherwise, and expand the following -- this
            intentionally closes *every* round, so the intermediate
            <todo-what/>/<todo-how/> states stay visible:

            <expand name="todo-box" arg1="current state (after grilling<round-suffix/>)"></expand>

6.  **State: implementing:**

    1.  You *MUST* first forget all previous internalized tenets and
        then freshly internalize and strictly honor the **GENERIC
        TENETS** and the **SPECIFYING TENETS** of the **ASE Tenets** in
        the following creation and updating of specification content. Do
        not output anything.

    2.  <if condition="<getopt-option-worktree/> is equal `true` and <worktree-dir/> is empty">

        One *single* worktree serves the whole skill run: it is created
        *once* before the first change set is applied, and all further
        `--loop` iterations land in it, too.

        1.  Set <worktree-name/> to a unique name, derived from
            <todo-what/>, which consists of two lower-case words
            concatenated with a `-` character. Do not output anything.

        2.  Determine the *worktree directory* by calling the
            `ase_worktree_path(id: "<worktree-name/>", create: true)`
            tool of the `ase` MCP server and capturing its output into
            <worktree-dir/>. You *MUST* *NEVER* assemble this path
            yourself. If this tool call fails, only output the following
            <template/> and then immediately *STOP* processing the
            entire current skill, leaving the working copy *untouched*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ ERROR: no Git repository or unsafe worktree directory -- cannot create worktree
            </template>

        3.  Determine the *existing worktrees* and *existing branches*
            by running the commands `git worktree list --porcelain` and
            `git branch --list` (taken exactly as given) and capturing
            their outputs. If the worktree directory <worktree-dir/> or
            the branch <worktree-name/> already exists, only output the
            following <template/> and then immediately *STOP* processing
            the entire current skill, leaving the existing worktree, its
            branch, and the working copy *untouched*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ ERROR: worktree or branch **<worktree-name/>** already exists
            </template>

        4.  Create the worktree by running the command
            `git worktree add "<worktree-dir/>"` (taken exactly as
            given), which creates the directory *and* -- named after its
            last path component -- the branch <worktree-name/> from
            `HEAD`. If this command fails, only output the following
            <template/> and then immediately *STOP* processing the
            entire current skill, leaving the working copy *untouched*:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ ERROR: worktree **<worktree-name/>** failed to create
            </template>

        5.  Only output the following <template/>:

            <template>
            ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ◉ worktree: **.ase/worktree/<worktree-name/>**, ▶ status: **worktree created**
            </template>

        </if>

    3.  Call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the
        `ase` MCP server *once* to find out the current time and store
        it in <timestamp-modified/>. Do not output anything.

    4.  Apply the edit by modifying the affected `SPEC` *artifacts* with
        a corresponding, complete *change set*, honoring *only*
        <todo-what/> and <todo-how/> plus the information gathered in
        the *discovering* state.

        The change set *MUST* keep every touched artifact conformant to
        the `SPEC` format contract (`ase-format-spec.md`): the
        `Created:`/`Modified:` frontmatter block, the heading levels,
        the Complex/Concise/Grouped format variants, the schema-allowed
        object kinds, nestings, and property keys, the object ids and
        `{{<id/>}}` anchors, the `, BECAUSE ` rationale split, and the
        `[[xxx]]` references.

        *Generate* a `SPEC` artifact which does not yet exist but is
        warranted by the edit, using <timestamp-modified/> for both its
        `Created:` and `Modified:` timestamps. Whenever an *existing*
        artifact is changed and carries a `Modified:
        <timestamp-modified-old/>` line, replace this with `Modified:
        <timestamp-modified/>`.

        Also, if a `CHANGELOG.md` file exists, make an appropriate entry
        there, too.

        <if condition="<worktree-dir/> is not empty">
        The change set *MUST* land *exclusively inside* the worktree
        <worktree-dir/>: resolve *every* file path relative to
        <worktree-dir/> instead of the original working copy. You *MUST*
        *NEVER* modify, stage, stash, revert, or commit anything
        *outside* of this worktree. Leave the worktree *uncommitted*:
        do *not* run `git add` and do *not* run `git commit`, so the
        user keeps full control over the final commit.
        </if>

    5.  Output only the following <template/>. You *MUST* *NOT* output a
        change summary, a list of modified artifacts, a rationale, or a
        unified diff of the changes -- *independent* of
        <ase-project-boxing/>, whose exposure rules are explicitly
        *overridden* here:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ status: **changes applied**
        </template>

7.  **State: verifying:**

    Enter this state only if <getopt-option-verify/> is equal `true`.
    Otherwise you *MUST* *strictly skip* the entire state and *any*
    verification: do *NOT* validate the specification at all and do
    *NOT* run any build, tests, linter, or type-checker.

    1.  Validate the specification and capture its <diagnostics/> array
        of `{ file, line, column, message }` objects:

        <if condition="<worktree-dir/> is not empty">
        Run the command `ase spec lint` with <worktree-dir/> as its
        working directory and parse its
        `<file/>:<line/>:<column/>: <message/>` output lines into
        <diagnostics/> -- the `ase_specbook_lint` tool always validates
        the *project* working copy and hence *MUST* *NOT* be used here.
        </if>
        <else>
        Call the `ase_specbook_lint()` tool of the `ase` MCP server and
        read its returned `diagnostics` array into <diagnostics/>.
        </else>

    2.  If <diagnostics/> is not empty, fix the reported problems in the
        affected `SPEC` artifacts via the `Edit`/`Write` tools and
        re-validate as in item 7.1 -- for at most *three* rounds in
        total.

    3.  <if condition="<diagnostics/> is not empty after the last round">

        Only output the following <template/>, listing one bullet line
        per remaining diagnostic:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ status: **verification failed**

        <ase-tpl-bullet-signal/> **REMAINING DIAGNOSTICS**:

        -   `<file/>:<line/>:<column/>`: <message/>
        [...]
        </template>

        </if>
        <else>

        Only output the following <template/>:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-spec-edit**, ▶ status: **verification passed**
        </template>

        </else>

8.  **Loop or Finish:**

    <if condition="<getopt-option-loop/> is equal `true`">
    Continue with the *next* iteration at the *querying* state
    (item 3 above). Do not output anything in this item.
    </if>
    <else>
    Finish the skill processing, but first give the closing hints by
    expanding the following (which, depending on the configured
    <ase-guidance-level/>, may each expand into nothing and hence emit
    no output at all):

    <ase-tpl-hint level="normal">
    Use `/ase-sync-reconcile -s SPEC` to propagate the specification changes into the remaining artifact kinds, and `/ase-sync-export` to re-materialize the derived export files.
    </ase-tpl-hint>

    <ase-tpl-hint level="verbose">
    Use `/ase-spec-edit --grill` to stress-test the query first, `--verify` to validate the specification afterwards, and `--loop` to chain several edits.
    </ase-tpl-hint>
    </else>
