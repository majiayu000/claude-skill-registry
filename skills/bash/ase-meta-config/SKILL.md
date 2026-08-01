---
name: ase-meta-config
argument-hint: "[--help|-h] [--scope|-s <scope>] <operation> [<args>]"
description: >
    List, get, set, or delete the layered ASE configuration values across
    the user/project/task/session scope chain.
    Use when the user wants to "configure" ASE, or to inspect or change a
    configuration key like `agent.persona`, `agent.guidance`, `agent.task`,
    or `project.boxing`.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-config">
Configuration Management
</skill>

<expand name="getopt"
    arg1="ase-meta-config"
    arg2="--scope|-s=">
    $ARGUMENTS
</expand>

<objective>
*List*, *get*, *set*, or *delete* the values of the *layered
configuration* of ASE, mirroring the non-interactive `ase config
<operation>` CLI subcommands *exclusively* through the `ase` MCP server.
</objective>

Procedure
---------

1.  **Determine Operation:**

    1.  Set <arguments><getopt-arguments/></arguments>, with any leading
        and trailing whitespace stripped. Split <arguments/> into
        whitespace-separated tokens, honoring single and double quotes
        (a quoted token is *one* token, with its surrounding quotes
        removed). Set <operation/> to the *first* token, lower-cased,
        and <operands/> to the list of the *remaining* tokens. If
        <arguments/> is empty, set <operation>(none)</operation> and
        <operands/> to the empty list. Inherit the always existing
        <ase-session-id/> from the current context.
        Do not output anything.

    2.  Determine the target scope chain:

        <if condition="<getopt-option-scope/> is empty">
        Set <scope>session:<ase-session-id/></scope>. Reads then cascade
        `user` -> `project` -> `session`, and writes land on the *session*
        layer -- the only layer on which the `agent.task` and `agent.skill`
        keys are writable at all.
        </if>
        <else>
        Set <scope><getopt-option-scope/></scope>, forwarding the given
        scope chain verbatim.
        </else>

        Do not output anything.

    3.  You *MUST* *NOT* use `Bash`, `Read`, `Write`, `Edit`, or any
        other filesystem-touching tool anywhere in this skill. *Every*
        configuration access is performed *exclusively* through the
        `ase_config_*` tools of the `ase` MCP server.
        Do not output anything.

2.  **Dispatch Operation:**

    1.  <if condition="<operation/> is `list` AND <operands/> is empty">
        Call the `ase_config_list(scope: "<scope/>")` tool from the `ase`
        MCP server. The result is a structured object with an `entries`
        array where each entry has a `key`, a `value`, and a `scope` field.

        -   If the `entries` array is empty, output the following <template/>:

            <template>
            ⧉ **ASE**: ⚙ config (scope: `<scope/>`): *(none)*
            </template>

        -   Else output the following <template/>, where each <key/>,
            <value/>, and <entry-scope/> correspond to one entry of the
            `entries` array, in the given order:

            <template>
            ⧉ **ASE**: ⚙ config (scope: `<scope/>`):

            | *Key*            | *Value*          | *Scope*          |
            |------------------|------------------|------------------|
            | `<key/>`         | **<value/>**     | `<entry-scope/>` |
            | [...]            | [...]            | [...]            |

            </template>
        </if>

    2.  <elseif condition="<operation/> is `get` AND <operands/> has exactly one token">
        Set <key/> to the single token of <operands/>. Call the
        `ase_config_get(key: "<key/>", scope: "<scope/>")` tool from the
        `ase` MCP server and set <text/> to its `text` output field.

        -   If <text/> is empty, the key is not set at all. Output the
            following <template/>:

            <template>
            ⧉ **ASE**: ⚙ config: `<key/>` (scope: `<scope/>`): *(not set)*
            </template>

        -   Else set <value/> to the JSON-decoded <text/> and output the
            following <template/>:

            <template>
            ⧉ **ASE**: ⚙ config: `<key/>` (scope: `<scope/>`): **<value/>**
            </template>
        </elseif>

    3.  <elseif condition="<operation/> is `set` AND <operands/> has exactly two tokens">
        Set <key/> to the *first* and <value/> to the *second* token of
        <operands/>. Call the `ase_config_set(key: "<key/>", val:
        "<value/>", scope: "<scope/>")` tool from the `ase` MCP server.

        Then, if <key/> is one of the three keys steering your *own*
        behaviour, you *MUST* immediately adopt the new <value/> for
        the remainder of the session -- *including* the output of this
        very skill run -- by re-evaluating and internalizing the
        corresponding rules of the constitution: for `agent.persona` set
        <ase-persona-style><value/></ase-persona-style> and re-evaluate
        the `Persona Communication Style` rules, for `agent.guidance` set
        <ase-guidance-level><value/></ase-guidance-level> and re-evaluate
        the `Guidance Hint Level` rules, and for `project.boxing` set
        <ase-project-boxing><value/></ase-project-boxing> and re-evaluate
        the `Artifact Boxing Transparency` rules. Do not output anything
        for this.

        Then only output the following <template/>:

        <template>
        ⧉ **ASE**: ⚙ config: `<key/>` (scope: `<scope/>`): **<value/>** (*updated*)
        </template>
        </elseif>

    4.  <elseif condition="<operation/> is `delete` AND <operands/> has exactly one token">
        Set <key/> to the single token of <operands/>. Call the
        `ase_config_delete(key: "<key/>", scope: "<scope/>")` tool from
        the `ase` MCP server. Then only output the following <template/>:

        <template>
        ⧉ **ASE**: ⚙ config: `<key/>` (scope: `<scope/>`): (*deleted*)
        </template>
        </elseif>

    5.  <else>
        The <operation/> is either missing, unknown, or was given with
        the wrong number of operands. Notice that the `init` and `edit`
        subcommands of the `ase config` CLI are deliberately *not*
        mirrored by this skill. Only output the following <template/>
        and then immediately *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ☻ skill: **ase-meta-config**, ▶ ERROR: invalid operation: **<operation/>** (expected `list`, `get <key>`, `set <key> <value>`, or `delete <key>`)
        </template>
        </else>
