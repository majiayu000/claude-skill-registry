---
name: ase-sync-import
argument-hint: "[--help|-h] [--target|-t <target>[,...]] <hint>"
description: >
    Import information from foreign sources into a set of artifact kinds
    (the target), generating or updating them to reflect the imported
    information. Use when the user wants to "import", "ingest", or
    "bring in" external sources like files, URLs, or pasted text into
    artifacts like SPEC, ARCH, CODE, DOCS, TASK, INFR, or OTHR.
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-sync-import">
    Import Foreign Sources into Artifact Set
</skill>

<expand name="getopt"
    arg1="ase-sync-import"
    arg2="--target|-t=SPEC,ARCH">
    $ARGUMENTS
</expand>

<objective>
    *Import* the information of the *foreign sources* (named by the
    <hint/>) into the *target* artifact kinds, by reading the foreign
    sources and generating or updating the target artifacts to faithfully
    reflect the imported information:
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

1.  <step id="STEP 1: Determine Target">

    1.  The recognized artifact kinds are the seven tokens `TASK`,
        `SPEC`, `ARCH`, `CODE`, `DOCS`, `INFR`, and `OTHR`. Parse
        <getopt-target/> as the comma-separated <target/> kind list.
        Upper-case and trim every parsed kind token. Do not output
        anything.

    2.  <if condition="<target/> is empty">

        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-import**, ▶ ERROR: empty target artifact list
        </template>

        </if>

    3.  If any token in <target/> is *not* one of the seven recognized
        kinds, only output the following <template/> (with <kind/> set to
        the first offending token) and then immediately *STOP* processing
        the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-import**, ▶ ERROR: unknown or unsupported artifact kind: **<kind/>**
        </template>

    4.  <if condition="<hint/> is empty">

        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-import**, ▶ ERROR: empty source hint -- nothing to import from
        </template>

        </if>

    5.  Report the resolved target and source hint with the following <template/>:

        <template>
        <ase-tpl-bullet-signal/> **TARGET**: <target/>
        <ase-tpl-bullet-normal/> **SOURCE**: <hint/>
        </template>

    </step>

2.  <step id="STEP 2: Ingest Foreign Sources">

    1.  Do not output anything in this STEP 2.

    2.  Interpret the <hint/> as the description of the *foreign sources*
        to import from. The foreign sources are *external* to the ASE
        artifact sets and may be local files or directories, remote URLs,
        pasted text passages, or references to other documents.

    3.  Read or fetch all foreign sources named by the <hint/>: read local
        files and directories via the `Read` tool, and fetch remote URLs
        via the available web tools. Build a precise understanding of the
        *information* the foreign sources represent.

    </step>

3.  <step id="STEP 3: Generate or Update Artifacts">

    1.  For all kinds in <target/>, call the `ase_artifact_list(kind: [
        ... ])` tool of the `ase` MCP server *once*, passing the
        lower-cased `kind` tokens, and read the returned `artifacts`
        array of `{ kind, files }` objects to obtain the project-relative
        file list per kind. Read all *existing* target artifacts to
        understand their current state.

    2.  Internalize and honor the artifact-format conventions:

        -   the artifact-set/artifact/aspect meta information (`ase-format-meta.md`),
        -   the `SPEC` format (`ase-format-spec.md`),
        -   the `ARCH` format (`ase-format-arch.md`),
        -   the `TASK` format (`ase-format-task.md`).

        Whenever a target artifact belongs to one of these kinds, it
        *MUST* be kept (or made) conformant to the corresponding format
        (headings, structure, identifiers, and the `<timestamp-modified/>`
        rule). The kinds `CODE`, `DOCS`, `INFR`, and `OTHR` have no
        dedicated format contract and are treated as free-form.

    3.  You *MUST* internalize and strictly honor the **GENERIC TENETS**,
        the **CRAFTING TENETS**, and the **RECONCILIATION TENETS** of the
        **ASE Tenets** when generating or updating in the following. Do
        not output anything.

    4.  Once call the `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of
        the `ase` MCP server to find out the current time and store it in
        <timestamp-modified/>.

    5.  *Generate or update* the <target/> artifact files so that they
        faithfully *reflect* the information of the imported foreign
        sources:

        -   *Generate* a target artifact that does not yet exist but is
            warranted by the imported information, using the current time
            for both its `Created:` and `Modified:` timestamps.

        -   *Update* an existing target artifact so it reflects the
            imported information. Keep changes as *surgical* as possible:
            change only what the imported information actually requires,
            and do *not* rewrite unrelated parts of an artifact. Whenever
            an existing artifact is changed and contains a `Modified:
            <timestamp-modified-old/>` line, replace this with `Modified:
            <timestamp-modified/>`.

        Honor **No Fabrication**: never invent target content the foreign
        sources do not support; if the sources are silent or ambiguous on
        something the target needs, surface the gap rather than guessing.
        Re-express the imported facts at the *target's* level of
        abstraction (a SPEC states intent, an ARCH states structure).

        Apply the generation/update directly to the target artifacts via
        the `Write`/`Edit` tools.

    6.  Report the performed changes with the following <template/>, listing
        one bullet line per generated or updated file (with <file/> its
        project-relative path and <note/> an ultra-brief description of
        what was imported):

        <template>
        <ase-tpl-bullet-signal/> **IMPORTED ARTIFACTS**:

        -   `<file/>`: <note/>
        [...]
        </template>

        <if condition="no target artifact required any change">

        Only output the following <template/>:

        <template>
        <ase-tpl-bullet-normal/> **IMPORTED ARTIFACTS**: none -- all targets already reflect the imported sources
        </template>

        </if>

    </step>

</flow>
