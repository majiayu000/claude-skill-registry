---
name: ase-meta-review
argument-hint: "[--help|-h] [--severity|-S=(LOW|MEDIUM|HIGH)]"
description: >
    Perform a holistic, human-reviewer-style critique of the currently
    staged Git changes and emit an approve/reject verdict with
    prioritized, severity-tagged, line-cited findings. Use when the user
    wants the staged diff "reviewed", "critiqued", or "code-reviewed"
    before committing.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git diff *)"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-review">
Review Staged Changes
</skill>

<expand name="getopt"
    arg1="ase-meta-review"
    arg2="--severity|-S=(LOW|MEDIUM|HIGH)">
    $ARGUMENTS
</expand>

<objective>
Review the currently staged Git changes the way an *experienced human
reviewer* would - judging them *holistically* against the change's *own
intent* and against *correctness*, *design fit*, *clarity*, *robustness*,
and *project-convention conformance* - and emit a single *approve /
request-changes verdict* backed by *prioritized*, *severity-tagged*,
*line-cited* findings. This is a *synthesizing critique*, not a mechanical
scan: it complements `ase-code-lint` (mechanical quality), `ase-code-analyze`
(logic/semantics), and `ase-meta-diff` (intent narrative and risk).
</objective>

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Change Set">

    1.  Determine *whether there are staged changes at all* by running the
        corresponding command (taken exactly as given) and capturing its
        output - the bare *list of staged file names* - into <diff/>. This
        is a lightweight gate; the full diff is fetched by the sub-agent
        in STEP 2, so capturing only the file-name list here is sufficient:

        `git diff --cached --name-only HEAD`

    2.  <if condition="<diff/> is empty">
        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-review**, ▶ status: **no changes to review**
        </template>
        </if>

    </step>

2.  <step id="STEP 2: Review Investigation">

    First, use the following <template/> to give a hint on this step:

    <template>
    <ase-tpl-bullet-secondary/> **REVIEW INVESTIGATION**
    </template>

    Dispatch the review investigation to a *sub-agent* via the `Agent`
    tool so that *no* investigation details leak into the user-visible
    transcript. The sub-agent performs the silent reading, the read-only
    repository probing, and the critique; only its final structured return
    value is consumed here.

    For this, invoke *exactly once* the tool:

    ```text
        Agent(
            name:          "ase-meta-review",
            description:   "Review Investigation",
            subagent_type: "ase:ase-meta-review",
            mode:          "plan",
            prompt:        "Review the staged changes."
        )
    ```

    Parse the single result message of the `Agent` tool as a JSON object,
    set <summary/> to its `summary` field (a single crisp sentence
    reconstructing the change's intent), and set <findings/> to its
    `findings` field (a list).

    Then *derive* the overall <verdict/> from <findings/>: set
    <verdict/> to `REJECT - DEMANDS CHANGES` if *any* finding in
    <findings/> has a `severity` field of `HIGH`; otherwise set
    <verdict/> to `APPROVE`. The verdict is derived *before* the
    severity floor below, so the floor only affects which findings are
    *rendered*, never the verdict.

    Then *apply the severity floor* selected via <getopt-option-severity/>
    (default `LOW`): define the ordinal rank `LOW`=1, `MEDIUM`=2,
    `HIGH`=3. *Keep* a finding in <findings/> if and only if its
    `severity` field is `ACCEPTED` *or* `rank(severity)` is greater than
    or equal to `rank(<getopt-option-severity/>)`; *silently drop* all
    other findings. With the default floor `LOW`, all findings are kept.
    `ACCEPTED` findings are *never* dropped.

    You *MUST* *NOT* output anything else in this STEP 2.

    </step>

3.  <step id="STEP 3: Verdict and Findings">

    1.  Use the following <template/> to output the overall review in
        <verdict/> and the reconstructed intent <summary/>:

        <template>

        <ase-tpl-bullet-signal/> **REVIEW VERDICT**: **<verdict/>**

        <ase-tpl-bullet-normal/> **CHANGE INTENT**: <summary/>

        </template>

        You *MUST* *NOT* output anything else in this STEP 3.1.

    2.  <if condition="<findings/> is empty">
        Only output the following <template/> and then *SKIP* the
        remainder of this STEP 3:

        <template>

        <ase-tpl-bullet-normal/> **NO FINDINGS**: the change is clean, nothing to flag.

        </template>
        </if>

    3.  <if condition="<findings/> is NOT empty">
        Sort the findings by <severity/> from highest to lowest in the
        fixed order `HIGH`, `MEDIUM`, `LOW`, `ACCEPTED`. Within the same
        severity, keep the order returned by the sub-agent.

        Then render a *three-column table* with one row per finding by
        using the following output <template/>. For each finding, repeat
        the third line, set <severity/> to its `severity` field, set
        <dimension/> to its `dimension` field set <location/> to its
        `location` field, and set <finding/> to its `finding` field.

        In the <location/> column, markup the `file:line` reference
        as code (with backticks) and prepend it with `▢ ` - keep the
        sub-agent's own `:N` / `:N-M` line citation intact and do *not*
        append any further line-count decoration.

        Because the <finding/> text is free-form Markdown, *before*
        emitting any row you *MUST* escape every literal `|` pipe
        character inside <location/> and <finding/> as `\|` so it cannot
        break the table column structure.

        <template>
        | Severity        | Dimension    | Finding                 |
        | --------------- | ------------ | ----------------------- |
        | **<severity/>** | <dimension/> | <location/>: <finding/> |
        </template>

        Keep the overall report *concise* and *brief*.
        Do *not* output any further explanation.
        </if>

    </step>

</flow>
