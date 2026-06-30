---
name: ase-sync-export
argument-hint: "[--help|-h] [--source|-s <source>[,...]] [<filter>]"
description: >
    Export artifact content into side-by-side, ready-to-consume files,
    one per artifact that declares an export. Use when the user wants to
    "export", "render", or "materialize" artifacts like SPEC or ARCH into
    derived files such as diagrams or tables.
user-invocable: true
disable-model-invocation: false
effort: xhigh
allowed-tools:
    - Write
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-sync-export">
    Export Artifact Set to Side-by-Side Files
</skill>

<expand name="getopt"
    arg1="ase-sync-export"
    arg2="--source|-s=SPEC,ARCH">
    $ARGUMENTS
</expand>

<objective>
    *Export* the *source* artifact kinds (optionally filtered by
    <hint/>) into side-by-side files, by reading the source artifacts
    and materializing, for every artifact that declares an export,
    the corresponding derived file next to the artifact itself.
    <hint><getopt-arguments/></hint>.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-meta.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-spec.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-arch.md

Procedure
---------

<flow>

1.  <step id="STEP 1: Determine Source">

    1.  The recognized artifact kinds are the seven tokens `TASK`,
        `SPEC`, `ARCH`, `CODE`, `DOCS`, `INFR`, and `OTHR`. Parse
        <getopt-source/> as the comma-separated <source/> kind list.
        Upper-case and trim every parsed kind token. Do not output
        anything.

    2.  <if condition="<source/> is empty">

        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-export**, ▶ ERROR: empty source artifact list
        </template>

        </if>

    3.  If any token in <source/> is *not* one of the seven recognized
        kinds, only output the following <template/> (with <kind/> set to
        the first offending token) and then immediately *STOP* processing
        the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-sync-export**, ▶ ERROR: unknown artifact kind: **<kind/>**
        </template>

    4.  Report the resolved source with the following <template/>:

        <template>
        <ase-tpl-bullet-signal/> **SOURCE**: <source/>
        </template>

    </step>

2.  <step id="STEP 2: Resolve and Read Artifacts">

    1.  Do not output anything in this STEP 2.

    2.  For all kinds in <source/>, call the `ase_artifact_list(kind: [
        ... ])` tool of the `ase` MCP server *once*, passing the
        lower-cased `kind` tokens, and read the returned `artifacts`
        array of `{ kind, files }` objects to obtain the project-relative
        file list per kind.

    3.  <if condition="<hint/> is not empty">

        Honor the filtering <hint/> to reduce the source artifacts
        and/or the aspects of those artifacts you should take into
        account.

        </if>

    4.  Internalize and honor the artifact-format conventions:

        -   the artifact-set/artifact/aspect/export meta information (`ase-format-meta.md`),
        -   the `SPEC` format (`ase-format-spec.md`),
        -   the `ARCH` format (`ase-format-arch.md`).

        In particular, internalize the generic *Artifact Export*
        contract of `ase-format-meta.md` (the `-   Export:` bullet, the
        side-by-side file-name convention, and the rule that an artifact
        without an `-   Export:` bullet is *not* exported), and which
        artifacts declare an export in the `SPEC` and `ARCH` formats.

    5.  Read all resolved source artifacts and build a precise
        understanding of the content of each artifact that declares an
        export.

    </step>

3.  <step id="STEP 3: Materialize Exports">

    1.  For *each* read source artifact that declares an `-   Export:`
        bullet in its format definition, *materialize* the declared
        export:

        -   *Build* the derived rendering exactly as described by the
            artifact's <export-transform/>, faithfully reflecting the
            artifact's current content -- no more, no less. Honor **No
            Fabrication**: never invent content the artifact does not
            support.

        -   For an export whose <export-transform/> is a *Mermaid
            diagram converted to SVG*, build the Mermaid specification
            from the artifact content and render it to an SVG document by
            calling the `ase_diagram(diagram: "<mermaid-spec/>", format:
            "svg")` tool of the `ase` MCP server, using its `text` output
            field as the SVG document. For a textual export (e.g. a
            Markdown table), build the content directly. For Markdown
            *tables*, honor the table-alignment rule of `ase-skill.md`.

        -   *Determine* the side-by-side target file name
            <export-filename/>
            as `<basedir/>/<artifact-set-id/>-<artifact-no/>-<artifact-id/>-<artifact-slug/>-<export-name/>.<export-ext/>`
            and resolve it to a project-relative path inside the
            artifact's own base directory by calling the
            `ase_artifact_name(filename: "<file-name/>", kind:
            "<export-filename/>")` tool of the `ase` MCP server.

        -   *Write* the derived rendering to that resolved path via the
            `Write` tool, overwriting any pre-existing export file of the
            same name.

    2.  Report the materialized exports with the following <template/>,
        listing one bullet line per written file (with <file/> its
        project-relative path and <note/> an ultra-brief description of
        what was exported):

        <template>
        <ase-tpl-bullet-signal/> **EXPORTED ARTIFACTS**:

        -   `<file/>`: <note/>
        [...]
        </template>

        <if condition="no source artifact declares an export">

        Only output the following <template/>:

        <template>
        <ase-tpl-bullet-normal/> **EXPORTED ARTIFACTS**: none -- no source artifact declares an export
        </template>

        </if>

    </step>

</flow>
