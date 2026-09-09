---
name: ase-spec-activate
argument-hint: "[--help|-h] [<query>]"
description: >
    Activate Specification Know-How: load the SpecBook format contract,
    the SpecBook schema configuration of the project, and the list of
    specification (SPEC) artifacts into the context, so the specification
    can be read, queried, explained, and edited ad-hoc in plain
    conversation. Use *automatically* whenever the user wants to work
    with the specification files -- asks what the "spec" or
    "specification" says, wants to "look up", "query", "check", or
    "explain" specification content, or wants a small ad-hoc change to
    it -- and no dedicated specification skill (`ase-spec-edit`,
    `ase-sync-import`, `ase-sync-reconcile`, `ase-sync-export`) is
    invoked, as those activate the know-how implicitly.
user-invocable: true
disable-model-invocation: false
effort: medium
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-spec-activate">
Activate Specification Know-How
</purpose>

<expand name="getopt" arg1="ase-spec-activate">
    $ARGUMENTS
</expand>

<objective>
*Activate* the know-how about the **SpecBook**-based specification --
the format contract, the schema configuration, and the artifact set --
so the specification can be worked with *ad-hoc* in plain conversation.
</objective>

@${CLAUDE_SKILL_DIR}/../../meta/ase-format-meta.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-format-spec.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-tenets.md

Procedure
---------

This skill is *plan-less* and *read-mostly*: it *never* composes or
persists a task plan and *MUST* *NOT* call `ase_task_save(...)`. It
only *loads* know-how into the context and answers an optional *query*.
It modifies `SPEC` artifacts only when the *query* explicitly asks for
an ad-hoc change, and it *never* touches the artifact kinds `CODE`,
`DOCS`, `TASK`, `INFR`, and `OTHR`.

1.  **Initialize:**

    Set <query><getopt-arguments/></query> (with any leading and
    trailing whitespace stripped). Do not output anything.

2.  **Activate Format:**

    The **SpecBook** format contract is already loaded into the context
    through the included `ase-format-spec.md` (and its nested
    `ase-format-specbook.md`). Internalize it now: the object kinds,
    the object ids and `{{<id/>}}` anchors, the `[[xxx]]` references,
    the `, BECAUSE ` rationale split, the Complex/Concise/Grouped
    format variants, and the `Created:`/`Modified:` frontmatter block.
    Do not output anything.

3.  **Activate Schema:**

    1.  Set <schema-file/> to the path of the **SpecBook SCHEMA Model**
        of the project (resolved as described in `ase-format-spec.md`)
        and <schema-kind/> to `standard` for the bundled schema or
        `custom` for a project-specific one. Do not output anything.

    2.  <if condition="the content of <schema-file/> was *not* already read into the current context -- neither by an earlier run of this skill nor by a dedicated specification skill">
        Read the **SpecBook SCHEMA Model** in <schema-file/> via the
        `Read` tool to learn the allowed object kinds, properties,
        nestings, and value constraints. Do not output anything.
        </if>
        <else>
        Do *not* read <schema-file/> again -- its content is already
        active in the context. Do not output anything.
        </else>

4.  **Activate Artifacts:**

    Resolve the `SPEC` artifacts by calling the
    `ase_artifact_list(kind: [ "spec" ])` tool of the `ase` MCP server
    *once* and reading the returned `artifacts` array of `{ kind, files
    }` objects. Set <artifact-files/> to the project-relative file list
    and <artifact-count/> to its length. Do *not* read the artifacts
    themselves in this step. Do not output anything.

5.  **Report Activation:**

    Only output the following <template/>:

    <template>
    <ase-tpl-boxed title="SPEC" subtitle="ACTIVATED">

    **SCHEMA**: `<schema-file/>` (<schema-kind/>)
    **SPEC**:   `<ase-spec-basedir/>` (<artifact-count/> artifacts)

    </ase-tpl-boxed>
    </template>

6.  **Answer Query:**

    <if condition="<query/> is empty">
    Silently *skip* this item. Do not output anything about the skipping.
    </if>
    <else>
    The <query/> argument *mainly* serves the *automatic* invocation by
    the agent harness, which passes the triggering user request
    *verbatim*, so activation and answer happen in *one* skill run.

    Serve <query/> *ad-hoc* under the **Activated Behavior** below:
    read the `SPEC` artifacts of <artifact-files/> which are related to
    <query/>, resolve their `[[xxx]]` references across artifacts, and
    answer the query grounded in the specification content, citing the
    artifact file and object id of every statement you rely on. If
    <query/> asks for a change, apply it as an *ad-hoc modification*
    according to the **Activated Behavior**. Set <answer/> to the
    resulting answer and only output the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **SPEC ANSWER**:

    <answer/>
    </template>
    </else>

7.  **Finish:**

    Finish the skill processing, but first give the closing hints by
    expanding the following (which, depending on the configured
    <ase-guidance-level/>, may each expand into nothing and hence emit
    no output at all):

    <ase-tpl-hint level="normal">
    The specification know-how now stays active for this session: read, query, and ad-hoc edit
    the `SPEC` artifacts in plain conversation, or use `/ase-spec-edit` for a complete one-shot edit.
    </ase-tpl-hint>

    <ase-tpl-hint level="verbose">
    Use `/ase-sync-import -t SPEC` to bring foreign sources into the specification,
    use `/ase-sync-reconcile -s SPEC` to propagate it into the other artifact kinds, and
    use `/ase-sync-export` to render it into HTML or PDF.
    </ase-tpl-hint>

Activated Behavior
------------------

Once this skill has run, the following rules stay in force for the
*remainder of the session* whenever `SPEC` artifacts are read, queried,
explained, or modified *ad-hoc* in plain conversation -- i.e. *outside*
of any dedicated specification skill:

-   **Resolution**: You *MUST* resolve the `SPEC` artifacts via the
    `ase_artifact_list(kind: [ "spec" ])` tool of the `ase` MCP server
    and *never* guess their file paths. Re-resolve them whenever
    artifacts might have been added or removed.

-   **Interpretation**: You *MUST* interpret the specification content
    strictly according to the **SpecBook** format contract and the
    **SpecBook SCHEMA Model**: object kinds, object ids and `{{<id/>}}`
    anchors, properties, `[[xxx]]` references, and `, BECAUSE `
    rationales. Before answering a query, resolve the `[[xxx]]`
    references *across* artifacts, and ground every answer in the
    specification content by citing artifact file and object id.

-   **Modification**: Every ad-hoc modification of a `SPEC` artifact
    *MUST* honor the **GENERIC TENETS** and the **SPECIFYING TENETS** of
    the **ASE Tenets**, and *MUST* keep the artifact conformant to the
    format contract and the schema: the `Created:`/`Modified:`
    frontmatter block, the heading levels, the format variants, the
    schema-allowed object kinds, nestings, and property keys, the object
    ids and anchors, the rationale split, and the references. Call the
    `ase_timestamp(format: "yyyy-LL-dd HH:mm")` tool of the `ase` MCP
    server *once* per change set and use its result to refresh the
    `Modified:` line of every changed artifact and for both the
    `Created:` and `Modified:` lines of every generated artifact.

-   **Validation**: After every ad-hoc modification, call the
    `ase_specbook_lint()` tool of the `ase` MCP server, fix the reported
    `diagnostics` in the affected `SPEC` artifacts for at most *three*
    rounds, and report any remaining diagnostics as
    `<file/>:<line/>:<column/>: <message/>` lines.

-   **Restriction**: An ad-hoc modification of the specification *MUST*
    stay restricted to the `SPEC` artifacts -- the artifact kinds
    `CODE`, `DOCS`, `TASK`, `INFR`, and `OTHR` are *never* touched as
    part of it. For a substantial or multi-artifact change, point the
    user to `/ase-spec-edit` instead of applying it ad-hoc.

-   **Tandem**: The dedicated specification skills `ase-spec-edit`,
    `ase-sync-import`, `ase-sync-reconcile`, and `ase-sync-export`
    include the format contract themselves and activate the know-how
    *implicitly*. Whenever one of them is invoked, its own procedure
    takes *precedence* over these rules, and this skill *MUST* *NOT* be
    invoked from within it. Conversely, a run of this skill *never*
    replaces such a dedicated skill when the user explicitly asks for
    it.
