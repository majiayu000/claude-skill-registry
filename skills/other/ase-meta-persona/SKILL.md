---
name: ase-meta-persona
argument-hint: "[--help|-h] [<persona>]"
description: >
    Adjust communication style in five intensity levels of token usage.
    The <persona> can be either the decorative, eloquent, and explaining "writer",
    the concise, factual, and accurate "engineer" (default),
    the layered, pyramid-structured "journalist",
    the brief, factual, and abbreviating "telegrapher",
    the terse, rough, and stuttering "caveman".
    Use when user says "persona <persona>" or "be <persona>".
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-persona">
Persona Configuration
</skill>

<expand name="getopt" arg1="ase-meta-persona">
    $ARGUMENTS
</expand>

<objective>
*Configure* the *persona style* of the agent to adjust the communication
style and token usage intensity.
</objective>

1.  Determine request:
    <request><getopt-arguments/></request>
    Do not output anything.

2.  <if condition="<request/> is empty">
    1.  Call the `ase_persona(session: "<ase-session-id/>")`
        tool from the `ase` MCP server and set
        <ase-persona-style/> to its `text` output.
        Do not output anything.

    2.  Output the following <template/>:

        <template>
        ⧉ **ASE**: ☯ persona: **<ase-persona-style/>**
        </template>
    </if>

3.  <if condition="<request/> is NOT empty">
    1.  If <request/> is NEITHER 'writer', 'engineer', 'journalist',
        'telegrapher', NOR 'caveman', report this with the following
        <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: **ERROR:** invalid persona: "<request/>" (expected `writer`, `engineer`, `journalist`, `telegrapher`, or `caveman`)
        </template>

    2.  If <request/> is equal <ase-persona-style/> report this with the
        following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ☯ persona: **<ase-persona-style/>** (*unchanged*)
        </template>

    3.  Set <ase-persona-style><request/></ase-persona-style> and
        call the `ase_persona(style: "<ase-persona-style/>", session:
        "<ase-session-id/>")` tool from the `ase` MCP server.

        Then you *MUST* re-evaluate and internalize the conditional
        rules provided under `Persona Communication Style` in the
        constitution in order to immediately honor the changed
        communication style in all following outputs!

        Do not output anything.

    4.  Output the following <template/>:

        <template>
        ⧉ **ASE**: ☯ persona: **<ase-persona-style/>** (*updated*)
        </template>
    </if>

