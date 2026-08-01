---
name: ase-meta-intent
argument-hint: "[--help|-h] <intent>"
description: >
    Match a free-text intent against the accumulated help of all ASE
    skills, generate the single best-fitting `/ase:ase-xxx-xxx` command
    with concrete options and arguments, and let the user execute it,
    refine the intent, or cancel. Use when the user knows what they want
    but not which skill or flags realize it, or mentions "intent" or
    requests "help".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Skill"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-intent">
Match an Intent to an ASE Command
</skill>

<expand name="getopt"
    arg1="ase-meta-intent"
    arg2="">
    $ARGUMENTS
</expand>

<objective>
*Match* the following free-text intent against the accumulated help of
all ASE skills and *generate* the single best-fitting `/ase:ase-xxx-xxx`
command that realizes it:
<intent><getopt-arguments/></intent>
</objective>

The following <corpus/> is the *accumulated help* of all ASE skills --
the concatenation of every skill's `help.md` file -- and is the *sole*
catalog you match <intent/> against:

<corpus>
@${CLAUDE_SKILL_DIR}/data.md
</corpus>

<flow>

1.  <step id="STEP 1: Check Intent">

    <if condition="<intent/> is empty">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-meta-intent**, ▶ ERROR: expected a `<intent>` argument
    </template>
    </if>

    </step>

2.  <step id="STEP 2: Match Intent and Dialog">

    *REPEAT* the following sub-steps in a *LOOP* until the user either
    *executes* the generated command or *cancels* the dialog in sub-step 4:

    1.  *Match Intent*:

        Match the current <intent/> against the <corpus/> and select the
        *single* best-fitting skill. From that skill's `##  SYNOPSIS`,
        `##  OPTIONS`, and `##  ARGUMENTS` sections in <corpus/>,
        *generate* a concrete command that realizes <intent/>:

        -   Set <name/> to the selected skill's name (e.g. `ase-code-lint`).
        -   Set <arguments/> to the concrete option flags and positional
            arguments -- derived from the skill's `##  OPTIONS` and
            `##  ARGUMENTS` -- that best realize <intent/> (may be empty).
        -   Set <command>/ase:<name/> <arguments/></command> (the full
            command line, with surplus inner spaces collapsed).
        -   Set <rationale/> to a *very brief*, single-sentence
            justification of why the selected skill and its options match
            <intent/>.

    2.  *Guard No Match*:

        <if condition="no skill in <corpus/> adequately matches <intent/>">
        Output the following <template/> and then *continue* the *loop*
        at sub-step 4 to prompt the user for a refined or clearer intent
        via the dialog's free-text channel (do *not* stop and do *not*
        render a command):

        <template>
        <ase-tpl-bullet-secondary/> **WARNING**: no confident match for the intent -- please refine or clarify it.
        </template>
        </if>

    3.  *Render Command*:

        Output the generated command with the following <template/>:

        <template>
        <ase-tpl-head title="SKILL COMMAND PROPOSAL"/>

        ●   **INTENT**:
        ○   <intent/>

        ●   **COMMAND**:
        ⌘   `<command/>`

        ●   **RATIONALE**:
        ○   <rationale/>

        <ase-tpl-foot title="SKILL COMMAND PROPOSAL"/>
        </template>

    4.  *Dispatch Command*:

        In the following, you *MUST* *NOT* use your built-in
        <user-dialog-tool/> tool! Instead, you *MUST* just show a custom
        dialog according to the expanded `custom-dialog` definition. You
        *MUST* closely follow this definition.

        Let the user decide what to do with the generated command by
        raising a question with the following custom dialog (invoked with
        `--other`, so that any free-text instruction is accepted as an
        intent refinement):

        <expand name="custom-dialog" arg1="--other">
            Dispatch: What would you like to do with the generated command?
            EXECUTE: Execute the generated command now.
            CANCEL:  Cancel this dialog.
        </expand>

        Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `CANCEL`:
            *Break* out of the *loop* and stop processing without any
            further output.

        -   If <result/> is `EXECUTE`:
            *Break* out of the *loop*, output the following <template/>,
            and then call the tool `Skill(skill: "ase:<name/>", args:
            "<arguments/>")` to *execute* the generated command:

            <template>
            ⧉ **ASE**: ◉ intent: **<intent/>**, ⌘ command: **<command/>**, ▶ status: **command executing**
            </template>

        -   If <result/> matches `OTHER: <text/>`:
            Set <intent><intent/> <text/></intent> (fold the free-text
            instruction into the intent). Then you *MUST* *continue* the
            *loop* at sub-step **2.1** to re-match the refined intent.

    </step>

</flow>
