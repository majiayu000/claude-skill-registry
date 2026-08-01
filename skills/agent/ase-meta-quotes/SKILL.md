---
name: ase-meta-quotes
argument-hint: "[--help|-h] [--ground|-g] [--proximity|-p] [--count|-c <count>] <topic-keywords>"
description: >
    Find quotes for a set of topic keywords and place them into a
    2x2 matrix, spanned by the presence of an author/origin and by
    the literal containment of a keyword, optionally grounded in
    Internet/Web facts and optionally widened to the conceptual
    neighborhood of the topic. Use when the user wants "quotes",
    "sayings", "aphorisms", or "citations" on a topic.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-quotes">
Find Quotes on a Topic
</skill>

<expand name="getopt"
    arg1="ase-meta-quotes"
    arg2="--ground|-g --proximity|-p --count|-c=8">
    $ARGUMENTS
</expand>

<objective>
*Find* quotes for the following topic keywords:
<keywords><getopt-arguments/></keywords>
</objective>

<flow>

1.  <step id="STEP 1: Sanity Check Usage">

    1.  <if condition="<keywords/> is empty">
        Only output the following <template/> and then immediately *STOP*
        processing the entire current skill:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-meta-quotes**, ▶ ERROR: expected a `<topic-keywords>` argument
        </template>
        </if>

    2.  Set <quotes></quotes> (set to empty).

    3.  Determine the maximum total number of *quotes* to surface: set
        <count/> to <getopt-option-count/>; if <getopt-option-count/> is
        *non-numeric* or *less than or equal to 0*, use the default *8*
        instead.

    </step>

2.  <step id="STEP 2: Harvest Quotes">

    1.  Determine *quotes* -- sayings, aphorisms, maxims, proverbs, and
        citations -- which are about the topic <keywords/>, and store them in
        <quotes/>. Per quote, record its *text*, its *author* (a named person
        or organization, if any is known), its *origin* (a named work,
        standard, or document, if any is known), and <keywords/> as its
        *source topic*.

    2.  <if condition="<getopt-option-ground/> is equal `true`">

        *Additionally* -- and never *instead* -- gather quotes from the
        Internet/Web by using the `ase-meta-search` skill in a sub-agent
        with the following tool call:

        `Agent(
            description: "Query Web Search Service",
            subagent_type: "ase:ase-meta-search",
            prompt: "Search the Internet/Web and gather quotes about the following topic: <keywords/>",
            run_in_background: false
        )`

        Merge the returned quotes into <quotes/>, deduplicating quotes which
        differ only in punctuation, capitalization, or attribution wording,
        and remember for every quote whether the search *confirmed* its exact
        wording and attribution.

        <if condition="the sub-agent returned no usable quotes">
        Output the following <template/> and continue with the model
        knowledge only:

        <template>
        <ase-tpl-bullet-secondary/> **WARNING**: grounding found no usable quotes -- falling back to model knowledge.
        </template>
        </if>

        </if>

    </step>

3.  <step id="STEP 3: Widen Topic via Proximity" condition="<getopt-option-proximity/> is equal `true`">

    1.  Set <prompt><keywords/></prompt>.

    2.  <if condition="<getopt-option-ground/> is equal `true`">
        Set <prompt>GROUND <keywords/></prompt>, so the agent grounds
        its determination in Internet/Web facts instead of using model
        knowledge only.
        </if>

    3.  Determine the *conceptual neighborhood* of <keywords/> by using the
        `ase-meta-proximity` agent in a sub-agent with the following
        tool call:

        `Agent(
            description: "Determine Conceptual Proximity",
            subagent_type: "ase:ase-meta-proximity",
            prompt: "<prompt/>",
            run_in_background: false
        )`

    4.  <if condition="the sub-agent returned no usable neighborhood">
        Output the following <template/>, *SKIP* the remaining sub-steps
        of this step, and continue with the quotes harvested in STEP 2
        only:

        <template>
        <ase-tpl-bullet-secondary/> **WARNING**: proximity agent returned no usable result -- keeping the narrow topic only.
        </template>
        </if>

    5.  Parse the returned labeled list and set <neighborhood/> to the values
        of its `PARENT:` line (the *broader* topic), of its four
        `SIBLING:` lines (the *same-level* topics), and of its four
        `CHILD:` lines (the *narrower* topics).

    6.  Harvest quotes for *each* topic of <neighborhood/> exactly as in
        STEP 2 (Harvest Quotes), record the contributing neighborhood
        topic as the *source topic* of each of those quotes, and merge
        the results into <quotes/>.

    </step>

4.  <step id="STEP 4: Classify and Render Quotes">

    1.  *Classify Quotes*:

        Classify every quote of <quotes/> along two *orthogonal* axes:

        -   **ATTRIBUTION**:
            A quote is `ATTRIBUTED` if a named *author* and/or a named
            *origin* is known for it, and `ANONYMOUS` otherwise.

        -   **LITERALNESS**:
            A quote is `LITERAL` if its text contains at least one of
            the topic keywords of <keywords/> as a *whole word* --
            matched *case-insensitively* and tolerating *inflections*
            (e.g. `architect` and `architectural` match the keyword
            `architecture`), but *never* as a mere *substring* (e.g.
            `art` does *not* match `architecture`). A quote is
            `THEMATIC` otherwise.

        Both axes span the four *quadrants*:

        -   `Q1` (`ATTRIBUTED` and `LITERAL`)
        -   `Q2` (`ATTRIBUTED` and `THEMATIC`)
        -   `Q3` (`ANONYMOUS`  and `LITERAL`)
        -   `Q4` (`ANONYMOUS`  and `THEMATIC`)

    2.  Finally, reduce <quotes/> to at most <count/> quotes in *total*,
        distributed as evenly as possible across the four quadrants
        and preferring the most relevant and most well-known quote per
        quadrant.

    3.  *Render Quotes*:

        Render every quote on its own `○`-prefixed line, with the
        following *suffixes* appended in this order:

        -   ` — *<author/>*, <origin/>` in the two `ATTRIBUTED` quadrants,
            omitting whichever of <author/> and <origin/> is unknown.

        -   ` [from proximity: `<source-topic/>`]` if the quote was
            harvested for a *neighborhood* topic in STEP 3 rather than for
            <keywords/> itself.

        -   ` *(unverified)*` if the exact wording or the attribution of
            the quote could not be established with confidence -- but
            omit this marker for a quote whose wording and attribution
            the Internet/Web search of STEP 2.2 confirmed -- including
            its re-application for a neighborhood topic in STEP 3.

        Render the single line `○   (none)` for a quadrant without any
        quote. Output the result with the following <template/>:

        <template>
        <ase-tpl-head title="QUOTES"/>

        ●   **Q1 - ATTRIBUTED / LITERAL**:
        ○   [...]

        ●   **Q2 - ATTRIBUTED / THEMATIC**:
        ○   [...]

        ●   **Q3 - ANONYMOUS / LITERAL**:
        ○   [...]

        ●   **Q4 - ANONYMOUS / THEMATIC**:
        ○   [...]

        <ase-tpl-foot title="QUOTES"/>
        </template>

    </step>

</flow>
