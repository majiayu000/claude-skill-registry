---
name: ase-sync-reconcile
argument-hint: "[--help|-h] [--bidirectional|-b] [--target|-t <target>[,...]] [--source|-s <source>[,...]] [<hint>]"
description: >
    Reconcile one set of artifact kinds (the target) to reflect the
    current state of another set of artifact kinds (the source), while
    optionally honoring a filtering hint. Use when the user wants to
    "reconcile", "sync", "align", or "update" artifacts like SPEC, ARCH,
    CODE, DOCS, TASK, INFR, or OTHR against each other.
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-sync-reconcile">
    Reconcile Artifact Set to Artifact Set
</skill>

<expand name="getopt"
    arg1="ase-sync-reconcile"
    arg2="--bidirectional|-b --target|-t=CODE,DOCS,INFR,OTHR --source|-s=AUTO">
    $ARGUMENTS
</expand>

<objective>
    *Reconcile* the *target* artifact kinds to *reflect* the *current
    state* of the *source* artifact kinds, by reading the source
    artifacts and aligning the target artifacts accordingly:
    <hint><getopt-arguments/></hint>.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-meta.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-spec.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-arch.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-task.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-tenets.md

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Target and Source">

    1.  The recognized artifact kinds are the seven tokens `TASK`,
        `SPEC`, `ARCH`, `CODE`, `DOCS`, `INFR`, and `OTHR`. Parse
        <getopt-target/> as the comma-separated <target/> kind list and
        <getopt-source/> as the comma-separated <source/> kind list.
        Upper-case and trim every parsed kind token. Do not output
        anything.

    2.  <if condition="<target/> is empty">

        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-reconcile**, ▶ ERROR: empty target artifact list
        </template>

        </if>

    3.  <if condition="<source/> is equal 'AUTO'">

        Set <source/> to the seven recognized kinds
        `TASK,SPEC,ARCH,CODE,DOCS,INFR,OTHR` *minus* all kinds present
        in <target/>. Do not output anything.

        </if>

    4.  If any token in <target/> or <source/> is *not* one of the seven
        recognized kinds, only output the following <template/> (with
        <kind/> set to the first offending token) and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-reconcile**, ▶ ERROR: unknown artifact kind: **<kind/>**
        </template>

    5.  <if condition="<getopt-bidirectional/> is not 'true'">

        Remove from <source/> any kind that is also present in <target/>
        (a kind is never its own source).

        <if condition="<source/> is empty">

        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-reconcile**, ▶ ERROR: empty source -- nothing to update from
        </template>

        </if>

        </if>

    6.  Report the resolved target and source with the following <template/>:

        <template>
        <ase-tpl-bullet-signal/> **TARGET**: <target/>
        <ase-tpl-bullet-normal/> **SOURCE**: <source/>
        </template>

    </step>

2.  <step id="STEP 2: Resolve and Read Artifacts">

    1.  Do not output anything in this STEP 2.

    2.  For all kinds in the union of <target/> and <source/>,
        call the `ase_artifact_list(kind: [ ... ])` tool of the `ase`
        MCP server *once*, passing the lower-cased `kind` tokens, and
        read the returned `artifacts` array of `{ kind, files }` objects
        to obtain the project-relative file list per kind.

    3.  <if condition="<hint/> is not empty">

        Honor the filtering <hint/> to reduce the source and/or target
        artifacts and/or the aspects of those artifacts you should take
        into account.

        </if>

    4.  Read all (optionally filtered) source and target artifacts
        previously resolved and build a precise understanding of the
        *current state* they represent.

    </step>

3.  <step id="STEP 3: Update Artifacts">

    1.  Internalize and honor the artifact-format conventions:

        -   the artifact-set/artifact/aspect meta information (`ase-format-meta.md`),
        -   the `SPEC` format (`ase-format-spec.md`),
        -   the `ARCH` format (`ase-format-arch.md`),
        -   the `TASK` format (`ase-format-task.md`).

        Whenever a target artifact belongs to one of these
        kinds, the update *MUST* keep it conformant to the
        corresponding format (headings, structure, identifiers, and the
        `<timestamp-modified/>` rule). The kinds `CODE`, `DOCS`, `INFR`,
        and `OTHR` have no dedicated format contract and are treated as
        free-form.

    2.  You *MUST* internalize and strictly honor the **GENERIC TENETS**,
        the **RECONCILIATION TENETS**, the **REFACTORING TENETS**, and
        the **CRAFTING TENETS** of the **ASE Tenets** when updating in
        the following. Do not output anything.

    3.  Once call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of
        the `ase` MCP server to find out the current time and store it in
        <timestamp-modified/>.

    4.  <if condition="<getopt-bidirectional/> is equal 'true'">

        *Bidirectionally update* the <target/> and <source/> artifacts
        so that they faithfully *reflect the current state* of each
        other.

        </if>
        <else>

        *Unidirectionally update* the <target/> artifact files so that
        they faithfully *reflect the current state* of the <source/>
        artifacts.

        </else>

        Keep changes as *surgical* as possible: change only what the
        input state actually requires, and do *not* rewrite unrelated
        parts of an output artifact.

        Apply the update directly to the output artifacts via the
        `Write`/`Edit` tools.

        For each formatted output artifact kind, strictly honor its
        format contract.

        Whenever an output artifact is changed and contains a `Modified:
        <timestamp-modified-old/>` line, replace this with `Modified:
        <timestamp-modified/>`.

    5.  Report the performed updates with the following <template/>, listing
        one bullet line per changed output file (with <file/> its
        project-relative path and <note/> an ultra-brief description of
        what was reconciled):

        <template>
        <ase-tpl-bullet-signal/> **UPDATED ARTIFACTS**:

        -   `<file/>`: <note/>
        [...]
        </template>

        <if condition="no output artifact required any change">

        Only output the following <template/>:

        <template>
        <ase-tpl-bullet-normal/> **UPDATED ARTIFACTS**: none -- all outputs already reflected source state
        </template>

        </if>

    </step>

</flow>

