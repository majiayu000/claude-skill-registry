---
name: ase-help-skill
argument-hint: "[--help|-h] [<skill-name>]"
description: >
    Show the manual page of an ASE skill, addressed by its full name, by
    any abbreviation of it, or by a description of its purpose, and list
    the entire skill catalog when no name is given. Use when the user
    wants the "manual", "man page", "manpage", or "help" of a particular
    ASE skill, or asks what a certain `ase-xxx-xxx` skill does.
user-invocable: true
disable-model-invocation: false
effort: medium
allowed-tools:
    - "Read"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-help-skill">
Show the Manual Page of an ASE Skill
</skill>

<expand name="getopt"
    arg1="ase-help-skill"
    arg2="">
    $ARGUMENTS
</expand>

<objective>
*Show* the *manual page* of the ASE skill addressed by the following
skill name, abbreviation of it, or description of its purpose:
<skill-ref><getopt-arguments/></skill-ref>
</objective>

The following <catalog/> is index of all ASE skills -- one
`⎈ **<group/>**` entry per skill group and one
``○ `<name/>`: <purpose/>`` entry per skill -- and this is
the *sole* index <skill-ref/> is resolved against:

<catalog>
@${CLAUDE_SKILL_DIR}/catalog.md
</catalog>

<flow>

1.  <step id="STEP 1: Resolve Skill Name">

    1.  <if condition="<skill-ref/> is empty">
        No particular skill was addressed, so render the *entire*
        <catalog/> as a browsable list with the following <template/>
        -- one list entry per catalog entry, in catalog order, where
        <name/> and <purpose/> are the two fields of the entry (and
        <name-padded/> is <name/>, padded to 22 characters with
        spaces on the right) -- and then immediately *STOP* processing
        the entire current skill:

        <template>
        <ase-tpl-head title="SKILL CATALOG"/>

        <catalog/>

        <ase-tpl-foot title="SKILL CATALOG"/>

        ⧉ **ASE**: ✪ skill: **ase-help-skill**, ▶ hint: **run `/ase-help-skill ase-xxx-xxx` for manual page of individual skill**
        </template>
        </if>

    2.  Set <skill-ref-raw/> to <skill-ref/> with only its leading and
        trailing whitespace stripped, as the *verbatim* wording of the
        user is required later on.

        *Normalize* <skill-ref/> by stripping all leading and trailing
        whitespace and then, repeatedly, any leading `/` and `ase:`
        prefix, so that `ase-code-lint`, `/ase-code-lint`,
        `ase:ase-code-lint`, and `/ase:ase-code-lint` all normalize to
        `ase-code-lint`. Do not output anything.

    3.  Resolve the normalized <skill-ref/> against <catalog/> in *three*
        tiers and store the outcome in <candidates/>. Each tier is tried
        only if all preceding tiers yielded *no* candidate at all:

        1.  *Exact Name Tier*:

            If a catalog *name* is *equal* to <skill-ref/>, set
            <candidates/> to exactly that *single* name.

        2.  *Substring Name Tier*:

            Set <candidates/> to *all* catalog *names* *containing*
            <skill-ref/> as a substring, in alphabetical order.

        3.  *Fuzzy Purpose Tier*:

            Set <candidates/> to *all* catalog names whose *purpose* --
            the part *after* the colon of the catalog entry -- *fuzzily*
            matches <skill-ref-raw/>, in *descending* order of match
            quality. Match against <skill-ref-raw/>, and *not* against
            <skill-ref/>, as this tier matches free-text wording, which
            the normalization of sub-step 2 would distort.

            A purpose matches fuzzily if it shares the topic, the
            wording, or evident synonyms with <skill-ref-raw/>, so
            that e.g. `manpage` matches `Show the Manual Page of an
            ASE Skill` and `root cause` matches `Five-Whys Root-Cause
            Analysis`. Include *plausible* matches only -- if none is
            plausible, leave <candidates/> empty.

        Set <count/> to the number of entries in <candidates/>.
        Do not output anything.

    </step>

2.  <step id="STEP 2: Dispatch Resolution">

    1.  <if condition="<count/> is equal 0">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-help-skill**, ▶ ERROR: unknown skill: **<skill-ref-raw/>**
        </template>
        </if>

    2.  <elseif condition="<count/> is equal 1">
        Set <name/> to the single entry of <candidates/> and continue
        processing. Do not output anything.
        </elseif>

    3.  <else>
        The abbreviation is *ambiguous*, so let the user pick the
        intended skill.

        Set <shown/> to the *first* 9 entries of <candidates/>, as the
        dialog renders at most *nine* answer lines.

        <if condition="<count/> is greater than 9">
            Set <truncation> (showing 9 of <count/> candidates)</truncation>
        </if>
        <else>
            Set <truncation></truncation> (set to empty)
        </else>

        In the following, you *MUST* *NOT* use your built-in
        <user-dialog-tool/> tool! Instead, you *MUST* just show a custom
        dialog according to the expanded `custom-dialog` definition. You
        *MUST* closely follow this definition.

        Let the user select the intended skill by raising a question
        with the following custom dialog, where each answer line
        corresponds to one entry of <shown/>, using the catalog *name*
        as the label and its catalog *purpose* as the description:

        <expand name="custom-dialog" arg1="--no-other">
            Ambiguous Skill: Which skill's manual page should be shown?<truncation/>
            <name/>: <purpose/>
            [...]
        </expand>

        Check the <result/> and dispatch accordingly:

        -   If <result/> is `CANCEL`:
            *STOP* processing without any further output.

        -   Otherwise: Set <name/> to the selected skill name and
            continue processing.
        </else>

    </step>

3.  <step id="STEP 3: Render Manual Page">

    1.  Use the `Read` tool to read the manual page of the resolved
        skill <name/> and set <manual/> to its content. The file path is
        formed by joining <ase-plugin-root/> and `skills/<name/>/help.md`
        with exactly *one* `/` separator, as <ase-plugin-root/> may or
        may not carry a trailing `/`. Do not output anything related to
        this tool call.

    2.  <if condition="<manual/> is empty or could not be read">
        Only output the following <template/> and then immediately
        *STOP* processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-help-skill**, ▶ ERROR: unreadable manual page: **<name/>**
        </template>
        </if>

    3.  Treat <manual/> as *verbatim* Markdown. You *MUST* *NOT*
        truncate, summarize, reformat, or partially show it. Only output
        the following <template/>:

        <template>
        <ase-tpl-head title="MANUAL PAGE: <name/>"/>
        <manual/>
        <ase-tpl-foot title="MANUAL PAGE: <name/>"/>
        </template>

    </step>

</flow>
