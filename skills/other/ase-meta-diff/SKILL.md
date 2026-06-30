---
name: ase-meta-diff
argument-hint: "[--help|-h] [--coherence|-c] [--risk|-r] [--blast|-b]"
description: >
    Summarize the currently staged Git changes as a human-readable,
    intent-grouped narrative. Use when the user wants a concise and
    brief report of what changed and why. Optionally can check the diff
    for intent coherence and show a risk and blast radius report.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Bash(git diff *)"
    - "Bash(git grep *)"
    - "Bash(git ls-files *)"
    - "Bash(grep *)"
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-diff">
Summarize Diff
</skill>

<expand name="getopt"
    arg1="ase-meta-diff"
    arg2="--coherence|-c --risk|-r --blast|-b">
    $ARGUMENTS
</expand>

<objective>
Summarize the currently staged Git changes into a *concise*,
*human-readable* narrative of what changed and why, *grouped by intent*
rather than by file. Optionally *reconstruct the change's single
intended purpose* and *flag hunks that do not serve it*. Optionally
*score* the diff against a *coupling-criticality-coverage-reversibility*
rubric and emit a *graded risk report* with *mitigations*. Optionally
render a *blast-radius map*.
</objective>

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Change Set">

    1.  Determine the *diff details* by running the corresponding command
        (taken exactly as given) and capturing the full diff output into
        <diff/> for the subsequent analysis:

        `git diff --cached HEAD`

    2.  Determine the *diff statistics* by running the corresponding command
        (taken exactly as given) and capturing the full stat output into
        <stat/> for the subsequent analysis:

        `git diff --cached --numstat HEAD`

    </step>

2.  <step id="STEP 2: Summarize By Intent">

    1.  <if condition="<diff/> is empty">
        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-diff**, ▶ status: **no changes to summarize**
        </template>
        </if>

    2.   Analyze the <diff/> and <stat/> and synthesize a *concise* narrative of
         WHAT changed and WHY, *grouped by intent* rather than by file.
         Honor the following intents:

         -   `FEATURE`:     new        functionality or configuration
         -   `IMPROVEMENT`: improved   functionality or configuration
         -   `BUGFIX`:      corrected  functionality or configuration
         -   `UPDATE`:      updated    functionality or configuration
         -   `CLEANUP`:     cleaned up functionality or configuration
         -   `REFACTOR`:    refactored functionality or configuration

    3.  <if condition="<diff/> is NOT empty">
        1.  First, output the following header <template/>:

            <template>

            <ase-tpl-bullet-normal/> **CHANGE INTENT REPORT**:

            </template>

        2.  Render a *three-column table* with one row per discovered
            *intent group* present in the <diff/>. Output the following
            table header <template/>:

            <template>
            | Intent | Changes (LoC) | Files &amp; Description |
            | ------ | ------------- | ----------------------- |
            </template>

        3.  For each discovered *intent group*, emit the following row
            <template/>, where <intent/> is the intent label, <changes/>
            is the total number of lines changed per intent group in format
            `+N/-M`, <files/> is the list of affected file references,
            and <description/> is a *brief* one-to-two-sentence
            narrative of what changed and why:

            <template>
            | **<intent/>** | <changes/> | <files/>: <description/> |
            </template>

            In the <files/> part of the second column, markup all file
            references as code (with backticks), prepend them with `▢ `,
            append ` [+N/-M]` (based on the information in <stat/>) to them,
            and separate them with `, ` (a comma and space). Do *not* repeat
            file references in the <description/>.

            Keep the overall report *concise* and *brief*. Try to keep the
            number of intent groups (table rows) in the range of 1-10. Do
            *not* output any further explanation.
        </if>

    </step>

3.  <step id="STEP 3: Assess Intent Coherence"
        condition="<getopt-option-coherence/> is equal `true` and <diff/> is NOT empty">

    1.  From the *same* captured <diff/> and <stat/>, *reconstruct the
        single intended change* as a thesis - the one logical, coherent purpose
        the diff *as a whole* is trying to accomplish.

        If the <diff/> genuinely spans *several* unrelated purposes,
        pick the *dominant* one as the thesis (the residue will surface
        as flagged hunks below).

        Multiple intents discovered in STEP 2 are a strong indicator of
        incoherence. In this case, be very sceptical and do *NOT* form a
        thesis which is just the superset of all those intents.

        Finally, phrase the thesis as a *single* crisp sentence and
        capture it as <thesis/>.

    2.  Walk *every* hunk in the <diff/> and *classify* each one as
        either *serving* <thesis/> or *not serving* it. A hunk does *not*
        serve the thesis when it is one of the following <deviation/> kinds:

        -   `SCOPE-CREEP`: an unrelated change riding along (e.g. a second
            feature, a drive-by refactor, an opportunistic rename, a
            reformatting sweep) that should be its own commit.

        -   `STRAY-DEBUG`: leftover debug/diagnostic residue (e.g. debug
            prints, `console.log`, commented-out code, temporary
            logging, `TODO`/`FIXME` scaffolding, disabled tests), which
            should be just removed and not part of any commit.

    3.  A hunk that *serves* <thesis/> will be *not* reported. Only hunks that
        do *not* serve it will be reported. If *every* hunk serves the thesis,
        the diff is *coherent* and you report *no* flagged hunks.

        Judge overall *coherence* from the flagged hunks: the diff
        is `COHERENT` when there are *no* `SCOPE-CREEP` and *no*
        `STRAY-DEBUG` deviations, otherwise it is `INCOHERENT`. Store
        the result in <verdict/>.

    4.  Emit the following header <template/>:

        <template>

        <ase-tpl-bullet-normal/> **CHANGE COHERENCE THESIS**: <thesis/>

        <ase-tpl-bullet-signal/> **CHANGE COHERENCE REPORT**: Verdict: **<verdict/>**

        </template>

    5.  <if condition="<verdict/> is `INCOHERENT`">
        Render a *three-column table* with one row per hunk, flagged
        for *not serving* the <thesis/> above. Output the following table in <template/>.

        For each flagged hunk, repeat the third line, where <deviation/>
        is the deviation kind label, <location/> is the affected file
        reference, and <reason/> is a *brief* one-sentence note on why
        the hunk does not serve <thesis/> and what to do with it (e.g.
        split into its own commit, drop the debug residue).

        In the <location/> column, markup all file references as code
        (with backticks), prepend them with `▢ ` and append ` [+N/-M]`
        (based on the information in <stat/>) to them.

        Keep the overall texts in <reason/> *very concise* and *brief*.
        Do *not* output any further explanation.

        <template>

        | Deviation        | Location    | Why it does not serve the thesis? |
        | ---------------- | ----------- | --------------------------------- |
        | **<deviation/>** | <location/> | <reason/>                         |

        </template>
        </if>
    </step>

4.  <step id="STEP 4: Score Against Risk Rubric"
        condition="<getopt-option-risk/> is equal `true` and <diff/> is NOT empty">

    1.  Score the *same* captured <diff/> and <stat/> information
        against the four-axis rubric below. Each axis is scored on an
        integer scale of *1* (lowest risk) to *5* (highest risk) against
        the *fixed anchors* given, and *every* score *MUST* be backed
        by a one-line <evidence/> grounded in the *actual* hunks or the
        read-only repository probe.

        Probe the repository *read-only* and *heuristically* (via `git
        grep` / `grep` / `git ls-files`, restricted to first-party code)
        only as needed to substantiate the *Coupling* and *Coverage*
        axes (e.g. who imports a touched module, whether touched code has
        adjacent tests). Do not output anything during the probe.

    2.  Score each axis against these anchors:

        1.  **COUPLING** - how widely the touched code is depended upon.
            *1*: self-contained, no first-party importers.
            *3*: a handful of dependent modules.
            *5*: a hub touched by many modules or a public interface.

        2.  **CRITICALITY** - how essential the touched path is.
            *1*: docs, comments, dead/peripheral code.
            *3*: ordinary feature logic.
            *5*: core/security/auth/data-integrity/money path.

        3.  **COVERAGE** - how well the change is exercised by tests.
            *1*: tests touched in this diff or directly covering the
            changed hunks.
            *3*: adjacent tests exist but are not clearly exercising the
            changed hunks.
            *5*: no tests anywhere near the touched code.

        4.  **REVERSIBILITY** - how easily the change can be undone.
            *1*: pure code change, revert restores prior state.
            *3*: needs coordinated revert or a config rollback.
            *5*: irreversible-by-revert (schema/data migration, released
            artifact, external side effect).

    3.  Compute the *aggregate risk* as the *equal-weighted* mean of
        the four risk contributions (Coupling, Criticality, Coverage,
        Reversibility), rounded to one decimal, and map it to a *graded
        band*: *1.0-1.9* → **LOW**, *2.0-2.9* → **MODERATE**, *3.0-3.9*
        → **HIGH**, *4.0-5.0* → **CRITICAL**.

    4.  Emit the following <template/>, with the overall band and
        aggregate score, followed by a *three-column table* with one row
        per axis: column 1 is the *axis*, column 2 is the *score*, and
        column 3 is the *evidence* (as a `●` bullet point) plus -
        *only* if the axis reached the mitigation threshold of '>= 4' -
        the *mitigation* (as a second `●` bullet point). If an axis did
        not reach that threshold, omit the ` ● **MITIGATION**:
        <mitigation/>` part from its row. Keep the overall <evidence/>
        and <mitigation/> texts *concise* and *ultra brief*. Do *not*
        output any further explanation.

        In <evidence/> markup all file references as code (with
        backticks), prepend them with `▢ ` and append ` [+N/-M]` (based
        on the information in <stat/>) to them.

        <template>

        <ase-tpl-bullet-signal/> **CHANGE RISK REPORT**: Overall: **<band/>** (<aggregate/>/5)

        | Axis        | Score      | Findings                                                                                              |
        | ----------- | ---------- | ----------------------------------------------------------------------------------------------------- |
        | **<axis/>** | <score/>/5 | ● **EVIDENCE**: <evidence/><if condition="axis score is `>= 4`"> ● **MITIGATION**: <mitigation/></if> |
        </template>
    </step>

5.  <step id="STEP 5: Render Blast-Radius Map"
        condition="<getopt-option-blast/> is equal `true` and <diff/> is NOT empty">

    1.  From the *same* captured <diff/> and <stat/>, *extract the
        touched modules* - the distinct changed source files (or their
        enclosing modules/ packages, according to the language idiom).

    2.  Then, for each touched module, *scan its reverse dependencies*
        - the other first-party files that *import* or *reference* it
        across the current project (e.g. by the module's basename,
        exported symbol, or import path). Keep the scan *read-only*
        and *heuristic*; restrict it to first-party code within the
        repository. Do not output anything during the scan.

    3.  Then build a *blast-radius graph* and render it as a diagram:

        1.  Build a Mermaid specification <mermaid-spec/> for a `flowchart
            TB` whose *touched* modules are the origin nodes and whose
            *reverse-dependency* edges fan out to the dependent modules
            (origin → dependent).

            Flag each *touched* node as a problem node per the
            `ase-meta-diagram` anomaly convention - prefix its label
            with `⚑ ` inside quotes, e.g. `T1["⚑ src/core.ts"]`. Keep
            labels ultra short (basenames or module names only).

        2.  Dispatch the rendering to the `ase-meta-diagram` sub-agent by
            calling the tool `Agent(name: "ase-meta-diagram",
            description: "Diagram Rendering", subagent_type:
            "ase:ase-meta-diagram", prompt: "<mermaid-spec/>")` and capture
            its returned `text` field as <diagram/>.

    4.  Then emit the following <template/>, showing <diagram/> and
        appending a *brief impact summary* of bullets, where each
        <module/> is a *touched* module and <impact/> is a one-sentence
        note on *what depends on it* and *how far the blast reaches*.

        In <module/> and <impact/>, markup all file references as code
        (with backticks), prepend them with `▢ ` and append ` [+N/-M]`
        (based on the information in <stat/>) to them.

        Keep the overall report *concise* and *brief*. Do *not* output
        any further explanation.

        <template>
        <ase-tpl-head title="CHANGE BLAST RADIUS"/>

        <ase-tpl-bullet-signal/> **CHANGE BLAST RADIUS MAP**:

        ```text
        <diagram/>
        ```

        <ase-tpl-bullet-signal/> **BLAST**: ⚑ **<module/>**: <impact/>

        <ase-tpl-bullet-signal/> **BLAST**: ⚑ **<module/>**: <impact/>

        [...]

        <ase-tpl-foot/>
        </template>

    </step>

</flow>

