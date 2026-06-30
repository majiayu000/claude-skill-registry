---
name: ase-meta-steelman
argument-hint: "[--help|-h] [--count|-c <count>] [--rounds|-r <rounds>] <thesis>"
description: >
    Build the strongest possible case for a thesis by playing
    "Steelman" (Latin spirit: "Advocatus Dei"). Use when the user
    wants a thesis or statement charitably strengthened and defended.
user-invocable: true
disable-model-invocation: false
effort: xhigh
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-steelman">
    Build the "Steelman" Argument
</skill>

<expand name="getopt"
    arg1="ase-meta-steelman"
    arg2="--count|-c=10 --rounds|-r=1">
    $ARGUMENTS
</expand>

<objective>
    Build the "Steelman" argument by constructing the strongest
    possible case for the thesis: <thesis><getopt-arguments/></thesis>
</objective>

Determine the number of *rounds* to perform: set <rounds/> to
<getopt-option-rounds/>; if <getopt-option-rounds/> is *non-numeric* or
*less than or equal to 0*, use the default *1* instead.

Determine the minimum number of *pro-theses* to surface: set <count/>
to <getopt-option-count/>; if <getopt-option-count/> is *non-numeric* or
*less than or equal to 0*, use the default *10* instead.

<flow>

1.  <step id="STEP 1: Restate Thesis">

    Begin a *round* of fortification and consolidating reasoning. On
    the first visit, set <i>1</i> (set round counter to one); on each
    subsequent visit (via the jump back in the last step), <i/> has
    already been incremented.

    <if condition="<rounds/> is greater than 1">
    Indicate the current round with the following <template/>:

    <template>
    <ase-tpl-bullet-secondary/> **ROUND**: <i/>/<rounds/>
    </template>
    </if>

    Output the thesis with the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **THESIS**: <thesis/>
    </template>

    </step>

2.  <step id="STEP 2: Determine Pro-Theses">

    Reason on the thesis in <thesis/> by playing *Steelman* (Latin
    spirit: "Advocatus Dei") - building the strongest possible case
    *for* it - by charitably strengthening and defending it with the
    help of the following tenets:

    -   **Charitable Interpretation**:
        Defend the strongest ("steelman") interpretation of the
        <thesis/>, not the weakest ("strawman"), because the most
        generous reading is the one worth defending and the one a fair
        critic must ultimately confront.

    -   **Strengthen the Fundamentals**:
        Identify the soundest fundamental ideas behind the thesis and
        make them explicit, because a position rests on the strength of
        its foundation and a solid foundation carries everything built
        on top of it.

    -   **Credit Claims, Not Person**:
        Support the thesis, the assumption, the evidence - never appeal
        to the proponent's authority or reputation, because a case that
        leans on who said it instead of what was said is no stronger
        than its weakest argument.

    -   **Make the Enabling Assumptions Explicit**:
        Surface the reasonable assumptions the thesis depends on and
        show they hold, because most strong arguments gain their force
        from premises that are sound once stated out loud.

    -   **Supply Evidence Proportional to Claim**:
        Ask "How do we know this?" and "What best supports it?", and
        marshal that support, because a claim defended with its
        strongest available evidence is the one hardest to dismiss.

    -   **Seek the Confirming Case**:
        Actively hunt for the supporting example, the favourable
        scenario, the precedent where the position succeeds, because
        one solid confirming case anchors the argument in reality.

    -   **Merit Identification**:
        Focus on the genuine strengths of the thesis with the highest
        potential value only, because marginal merits are not worth the
        explicit discussion.

    -   **Push the Logic to its Best Conclusion**:
        Ask "If we accept this, then what follows?" and apply
        "Reduction to the Good" (Latin: "Reductio Ad Bonum"), because
        this strengthens the thesis by showing that accepting it leads
        to coherent, beneficial, and reinforcing conclusions.

    -   **Surface the Upside and Leverage**:
        Name the opportunity gained, the compounding benefit, the
        problem dissolved, because every choice in the thesis unlocks
        possibilities that a fair appraisal must count.

    -   **Stay Falsifiable and Concrete**:
        Frame each supporting point so it can be checked and confirmed
        with facts, because vague enthusiasm ("I just like it") adds no
        strength to the case.

    -   **Argue in Good Faith**:
        Make clear you are building the best honest case, not
        overselling, because the goal of the objective is a better
        final decision, not a sales pitch.

    -   **Concede the Real Weaknesses**:
        Acknowledging where the thesis genuinely falls short is what
        makes the defence credible, because a Steelman who can never
        admit a flaw is just an apologist.

    -   **Pre-Parade Thinking**:
        Imagine success scenarios of the thesis, because envisioning
        how it wins clarifies the conditions worth securing in advance.

    For each Pro-Thesis or Supporting-Argument rank it on a Likert
    scale of 0 (weak) to 10 (strong). Repeat the process of finding
    more Pro-Theses or Supporting-Arguments until you EITHER have found
    at least <count/> Pro-Theses or Supporting-Arguments with at least a
    rank of 7 OR you have already checked a total of <count/> x 5
    Pro-Theses or Supporting-Arguments. If the second condition is
    reached first and fewer than <count/> Pro-Theses or
    Supporting-Arguments reached a rank of at least 7, nevertheless
    surface the <count/> highest-ranked ones found so far, because
    <count/> is the *minimum* number of Pro-Theses to surface.

    Then, for the top-<count/> highest-ranked Pro-Theses or
    Supporting-Arguments, sort them by their rank from highest to lowest,
    store each in <prothesis-N/> with the format `**<aspect-N/>**
    (rank: <rank-N/>/10): <statement-N/>` (where <aspect-N/> is a short
    1-3 word summary of <statement-N/>, <rank-N/> is the determined
    rank on the Likert scale, and <statement-N/> is a single-sentence
    statement of not more than 40 words), and then output the following
    <template/>:

    <template>
    <ase-tpl-bullet-signal/> **PRO-THESIS**: <prothesis-N/>
    </template>
    </step>

3.  <step id="STEP 3: Consolidating Reasoning">

    Following the consolidation of...

        *Thesis* + *Pro-Theses* → *Fortification*

    ...with...

    -   *Thesis*: the initial statement, claim, or position. It is asserted
        as true, but on its own it is under-developed: it captures part of the
        truth while leaving its own strongest support implicit, unstated, or
        unproven.

    -   *Pro-Theses*: the reinforcing forces. They are the corroboration,
        evidence, or supporting positions that the thesis invites - precisely
        the role a Steelman played. The pro-theses make explicit what the
        thesis assumed or left unsaid.

    -   *Fortification*: the consolidation. Not an uncritical "cheerleading"
        of the thesis, and not a mere restatement of it, but a stronger
        position that consolidates everything that genuinely strengthens it
        while honestly bounding where it holds. The fortification reinforces
        the position by sharpening it.

    ...then derive a strong single-sentence (not more than 40 words)
    fortification of the <thesis/> and all found <prothesis-N/> - the
    strongest defensible form of the thesis - store it in <fortification/>,
    and then finally output the following <template/>:

    <template>
    <ase-tpl-bullet-normal/> **FORTIFICATION**: <fortification/>
    </template>

    Finally, decide whether to perform a further round:

    <if condition="<i/> is less than <rounds/>">
    Carry the result forward to the next round: set
    <thesis><fortification/></thesis> (the fortification becomes the
    thesis to be strengthened next), set <i/> to <i/> + 1 (increment the
    round counter), and then *REPEAT* the operation at **STEP 1**!
    </if>

    <if condition="<i/> is greater than or equal to <rounds/>">
    All <rounds/> rounds are complete; *STOP* the loop here.
    Do not output any further explanations.
    </if>

    </step>

</flow>
