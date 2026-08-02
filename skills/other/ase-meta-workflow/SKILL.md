---
name: ase-meta-workflow
argument-hint: "[--help|-h] [--scope|-s local|user] [--force|-f] <skill-name> <workflow-description>"
description: >
    Generate a new agent tool skill, written in the style of ASE
    skills, which orchestrates a workflow of sequential actions,
    parallel actions, sub-agent calls, and skill calls. Use when the
    user wants to "generate a skill", create a "workflow", "orchestrate"
    or "chain" multiple ASE skills, or automate a recurring multi-step
    procedure.
user-invocable: true
disable-model-invocation: false
effort: xhigh
allowed-tools:
    - "Read"
    - "Write"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<purpose name="ase-meta-workflow">
Generate a Workflow Skill
</purpose>

<expand name="getopt"
    arg1="ase-meta-workflow"
    arg2="--scope|-s=(local|user) --force|-f">
    $ARGUMENTS
</expand>

<objective>
*Generate* a new skill for the current *agent tool* <ase-agent-tool/>,
written in the style of *ASE* skills, which orchestrates the workflow
described by:
<arguments><getopt-arguments/></arguments>
</objective>

References
----------

-   The following <sample/> is a *reference skill* demonstrating the
    usual *layout* of a generated workflow skill -- its frontmatter, its
    `ase meta` preamble, and the indentation of its `<flow>`:

    <sample>
    @${CLAUDE_SKILL_DIR}/sample.md
    </sample>

    *IMPORTANT*: <sample/> is authoritative for the usual *layout* only.
    The *syntax* of every control construct is defined *exclusively* by
    the `Control Flow Constructs` section above, and its frontmatter and
    preamble show the `claude` flavor only -- the actual frontmatter
    fields and the actual preamble are dispatched on <ase-agent-tool/> as
    defined by the `Generated Skill Contract` below.

-   The following <graph/> is the *ASE workflow graph*, carrying one
    `<from/> -> <to/>` transition per line, where each side is either an
    `ase-xxx-xxx` skill or an upper-case logical state (`START`, `SKETCH`,
    `APPROACHES`, `TASK`, `ARTIFACT`, `END`):

    <graph>
    @${CLAUDE_SKILL_DIR}/workflow.txt
    </graph>

    The <graph/> tells which ASE skill sequences are *usually
    meaningful*. It *guides* the workflow, but it does *not* restrict
    it: a workflow may contain arbitrary *non-ASE* actions, and it may
    contain ASE transitions the <graph/> does not list.

-   The following <catalog/> is the *accumulated help* of all ASE skills --
    the concatenation of every skill's `help.md` file -- and is the
    *sole* source for the options and arguments of every `<skill/>`
    invocation (for an `ase-xxx-xxx` skill) you emit:

    <catalog>
    @${CLAUDE_SKILL_DIR}/../ase-help-intent/data.md
    </catalog>

Generated Skill Contract
------------------------

A generated skill is a *regular* skill of the current agent tool
<ase-agent-tool/> which is *independent* of the *ASE plugin*
installation path. It therefore *MUST* strictly follow this contract:

-   **Frontmatter**: `name: <new-skill-name/>` and a `description` of one
    to three sentences summarizing the workflow and its trigger phrases.

    The *remaining* frontmatter fields are *tool-specific*, because every
    agent tool accepts its own field set and its own `allowed-tools`
    grammar, and hence have to be dispatched on <ase-agent-tool/>:

    <if condition="<ase-agent-tool/> is `codex`">
    Emit *only* an `allowed-tools` field, carrying the space-separated
    string `Bash(ase meta *)`, because *OpenAI Codex* accepts *no*
    frontmatter fields besides `name`, `description`, `license`,
    `allowed-tools`, and `metadata`.
    </if>

    <elseif condition="<ase-agent-tool/> is `copilot`">
    Emit an `argument-hint` derived from the declared options and
    arguments, plus `user-invocable: true`, `disable-model-invocation:
    false`, and an `allowed-tools` list which *always* contains
    `"shell(ase:*)"` plus any further tool the workflow actually uses.
    *IMPORTANT*: *GitHub Copilot* uses the permission pattern grammar
    `shell(<command/>:*)`, `write(<path/>)`, and `<mcp-server/>(<tool/>)`
    -- a `Bash(...)` entry would be misread as an unknown MCP server, and
    plain tool names like `Skill` or `Agent` are *no* permission patterns
    at all and hence *MUST NOT* be emitted.
    </elseif>

    <else>
    Emit an `argument-hint` derived from the declared options and
    arguments, plus `user-invocable: true`, `disable-model-invocation:
    false`, and an `allowed-tools` list which *always* contains
    `"Bash(ase meta *)"` plus `"Skill"` and/or `"Agent"` whenever the
    workflow emits `<skill/>` and/or `<agent/>` invocations, plus any
    further tool the workflow actually uses.
    </else>

-   **Preamble**: the generated skill has to pull in the ASE meta
    definitions through the `ase meta` command, because it resolves them
    from the bundled tool package, whereas the
    `@${CLAUDE_SKILL_DIR}/../../meta/` includes used *inside* the ASE
    plugin have *no* resolvable path from outside of it. Append further
    meta names only when the workflow needs them (`dialog` for a
    `custom-dialog`, `tenets`, `format-task`, ...).

    *How* the command is pulled in is *tool-specific*, because only
    *Anthropic Claude Code* expands the ``!`<command/>` `` construct
    before the skill content reaches the model, hence dispatch on
    <ase-agent-tool/>:

    <if condition="<ase-agent-tool/> is `copilot` or `codex`">
    Emit the following <preamble-block/> as the first body element,
    because the ``!`<command/>` `` construct would otherwise reach the
    model *verbatim* and silently stay unexpanded:

    <preamble-block>
    *IMPORTANT*: *Before* anything else, run the shell command...

    `ase meta control skill getopt`

    ...and treat its *entire* output as if it were written here. It
    defines the control flow constructs, the skill conventions, and the
    option parsing used below. Do *not* proceed before you have done this.
    </preamble-block>
    </if>

    <else>
    Emit the *single* line ``!`ase meta control skill getopt` `` as the
    first body line.
    </else>

-   **Identification**: a `<purpose name="<new-skill-name/>">` block
    carrying a short title-case purpose.

-   **Argument Parsing**: an `<expand name="getopt" arg1="<new-skill-name/>"
    arg2="<spec/>">$ARGUMENTS</expand>` block -- but *only* when the
    workflow wants to declare options.

-   **Objective**: an optional `<objective/>` block declaring the
    official objective of the workflow skill.

-   **Body**: usually the `<flow>` derived in `STEP 3` below.
    But everything is allowed here.

Procedure
---------

<flow>

1.  <step id="STEP 1: Reason About Workflow">

    1.  Set <new-skill-name/> to the *first* whitespace-separated token of
        <getopt-arguments/> and <workflow-description/> to the *entire
        remainder*. Do not output anything.

    2.  <if condition="<new-skill-name/> does not match the regexp `^[a-zA-Z][a-zA-Z0-9_-]*$`">
        Ask the user interactively, without a special tool, for the skill
        name with a single question:

        `**No valid skill name given. What should the generated skill be named?**`

        Then set <new-skill-name/> to the response of the user and set
        <workflow-description/> to the *entire* original
        <getopt-arguments/>.
        Repeat this question until the response matches the regexp
        `^[a-zA-Z][a-zA-Z0-9_-]*$`, so that no path separator or traversal
        segment can ever reach <target-skill/>.
        </if>

    3.  <if condition="<workflow-description/> is empty">
        Ask the user interactively, without a special tool, for the
        workflow with a single question:

        `**No workflow description yet. Which workflow should the skill perform?**`

        Then set <workflow-description/> to the response of the user.
        </if>

    4.  Determine the *skill locations* of the current agent tool, because
        every agent tool discovers its skills in its *own* directories:

        <skill-dir-user>~/.claude/skills</skill-dir-user>
        <skill-dir-local>.claude/skills</skill-dir-local>
        <if condition="<ase-agent-tool/> is `copilot`">
        <skill-dir-user>~/.copilot/skills</skill-dir-user>
        <skill-dir-local>.github/skills</skill-dir-local>
        </if>
        <if condition="<ase-agent-tool/> is `codex`">
        <skill-dir-user>~/.codex/skills</skill-dir-user>
        <skill-dir-local>.agents/skills</skill-dir-local>
        </if>

        <if condition="<getopt-option-scope/> is equal `user`">
        Set <dir><skill-dir-user/></dir>.
        </if>
        <else>
        Set <dir><skill-dir-local/></dir>.
        </else>

        Then set <target-skill><dir/>/<new-skill-name/>/SKILL.md</target-skill>.
        Expand a leading `~` in <target-skill/> into the absolute home
        directory of the user, as the file tools accept absolute paths only.
        Do not output anything.

    5.  Check whether <target-skill/> already exists.

        <if condition="<target-skill/> exists and <getopt-option-force/> is not equal `true`">
        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-workflow**, ▶ ERROR: target already exists: **<target-skill/>**
        </template>

        Directly *after* this error <template/>, and *before* stopping,
        give the corrective hint by expanding the following:

        <ase-tpl-hint level="minimal">
        Re-run with `--force`/`-f` to overwrite the existing skill.
        </ase-tpl-hint>
        </if>

    6.  Report the workflow with the following <template/>:

        <template>
        ⧉ **ASE**: ✪ workflow: **<new-skill-name/>**, ⎈ tool: **<ase-agent-tool/>**, ◉ target: **<target-skill/>**
        ⧉ **ASE**: ✪ workflow: **<new-skill-name/>**, ⇌ description: **<workflow-description/>**
        </template>

    7.  Do not output anything else in this STEP 1, unless you asked the user.

    </step>

2.  <step id="STEP 2: Internalize ASE Capabilities">

    1.  Absorb the <catalog/> to know which ASE skills exist and which
        options and arguments each of them accepts.

    2.  Absorb the <graph/> to know which ASE skill sequences are usually
        meaningful, and treat every transition it does *not* list as
        merely *unusual*, never as *forbidden*.

    3.  Do not output anything in this STEP 2.

    </step>

3.  <step id="STEP 3: Derive Workflow Structure">

    1.  Decompose <workflow-description/> into an *ordered* list of
        *top-level* actions. Each top-level action becomes a numbered
        list item wrapping a `<step id="STEP <n/>: <title/>">` element,
        and all of them together are wrapped into a single `<flow>`
        element.

    2.  Map every action of <workflow-description/> onto the matching
        control construct:

        -   *sequential* actions become consecutive `<step/>` elements,
        -   *concurrent* actions become a `<parallel>` element,
        -   *sub-agent* invocations become `<agent/>` elements,
        -   *ASE skill* invocations become `<skill name="ase:ase-xxx-xxx"
            args="..."/>` elements, whose options and arguments are taken
            *verbatim* from the <catalog/> and never invented,
        -   *foreign skill* invocations become `<skill name="..." args="..."/>`
            elements, whose options and arguments are taken *verbatim*,
        -   *repetitions* become `<while/>` or `<for/>` elements,
        -   *conditional* actions become `<if/>`/`<elseif/>`/`<else/>` elements,
        -   all *remaining* actions become plain instruction prose inside
            their `<step/>`.

        Every *top-level* `<skill/>` element -- one which is not already
        placed inside an `<agent/>` element -- *MUST* be enclosed in
        its own dedicated `<agent/>` element, always *without* an
        `isolation` attribute and always with `run_in_background=false`,
        because the `TaskCreate` and `TaskUpdate` tool calls of the
        called skill would otherwise interfere with the task tracking of
        the generated workflow skill itself.

    3.  For *every* `<parallel>` element which contains at least one
        `<agent isolation="worktree">`, you *MUST* append a *dedicated*
        consolidation `<step/>` directly after the `<step/>` holding that
        `<parallel>` element, and this consolidation step *MUST* contain
        an `<agent-consolidation/>` element, so the Git WorkTrees of the
        concurrent sub-agents are merged and removed again.

    4.  Determine the *options* of the generated skill: declare an option
        only when <workflow-description/> actually asks for it, and
        express it in the `--<long/>[|-<short/>][=<default/>|=(<c1/>|<c2/>|...)[...]]`
        spec syntax of the `getopt` definition, which also covers the fixed
        *choice* form and the comma-separated *list* form.

    5.  Do not output anything in this STEP 3.

    </step>

4.  <step id="STEP 4: Generate Workflow Skill">

    1.  <if condition="<ase-project-boxing/> is not equal `black`">
        Set <structure/> to a compact rendering of the derived workflow --
        one line per `<step/>`, prefixed with its number, and one indented
        line per contained `<parallel/>`, `<agent/>`, `<skill/>`, or
        `<agent-consolidation/>` element -- and report it with the
        following <template/>:

        <template>
        <ase-tpl-boxed title="WORKFLOW" subtitle="<new-skill-name/>">
        <structure/>
        </ase-tpl-boxed>
        </template>
        </if>

    2.  Assemble <skill-content/> from the derived workflow, strictly
        following the `Generated Skill Contract` above.

    3.  Write <skill-content/> to <target-skill/>, creating the directory
        `<dir/>/<new-skill-name/>` if it does not exist yet. Calculate the
        number of words <words/> of <skill-content/>.

    4.  Report the result with the following <template/>:

        <template>
        ⧉ **ASE**: ✪ workflow: **<new-skill-name/>**, ✎ skill: **<words/>** words, ▶ status: **skill generated**
        ⧉ **ASE**: ✪ workflow: **<new-skill-name/>**, ◉ files: **<target-skill/>**
        </template>

    5.  Give the follow-up pointer, dispatched on <ase-agent-tool/>,
        because every agent tool reloads and invokes its skills
        differently, by expanding the following:

        <if condition="<ase-agent-tool/> is `copilot`">
        <ase-tpl-hint level="minimal">
        Run `/skills reload` to reload all skills.
        Run `/<new-skill-name/>` to execute the new generated workflow.
        </ase-tpl-hint>
        </if>
        <elseif condition="<ase-agent-tool/> is `codex`">
        <ase-tpl-hint level="minimal">
        Run `/skills` to check that the new skill was picked up.
        Mention `$<new-skill-name/>` to execute the new generated workflow.
        </ase-tpl-hint>
        </elseif>
        <else>
        <ase-tpl-hint level="minimal">
        Run `/reload-skills` to reload all skills.
        Run `/<new-skill-name/>` to execute the new generated workflow.
        </ase-tpl-hint>
        </else>

    6.  Do not output anything else in this STEP 4.

    </step>

</flow>
