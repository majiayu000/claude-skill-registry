---
name: ase-meta-evaluate
argument-hint: "[--help|-h] <request>"
description: >
    Evaluate alternatives through a weighted multi-criteria decision
    matrix. Use when the user calls for the *evaluation* of
    *alternatives*, wants to *compare* things, or asks what the best is
    from a list of choices.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-evaluate">
Evaluate Alternatives
</skill>

<expand name="getopt" arg1="ase-meta-evaluate">
    $ARGUMENTS
</expand>

<objective>
*Evaluate* *alternatives* through a weighted
multi-*criteria* decision matrix.
</objective>

<flow>
1.  <step id="STEP 1: Determine Reason">
    -   From the <request><getopt-arguments/></request>, try to derive the overall
        reason <reason/> for the evaluation. If no such reason can be
        derived, assume <reason>generic comparison</reason>.

    -   Output the determined reason with just the following <template/>
        and do not output anything else:

        <template>
        <ase-tpl-bullet-secondary/> **REASON**: *<reason/>*
        </template>
    </step>

2.  <step id="STEP 2: Determine Alternatives">
    -   From the <request><getopt-arguments/></request> derive the two or more
        alternatives <alternative-K/> (K=1-N) the user wants to be
        evaluated. Do not output anything.

    -   If fewer than two alternatives could be derived (N<2), output the
        following <template/> and *stop the entire flow* immediately without
        executing any further steps:

        <template>
        <ase-tpl-bullet-signal/> **ERROR: INSUFFICIENT ALTERNATIVES**: at least two are required for a comparison!
        </template>

    -   For each alternative <alternative-K/> (K=1-N), decide whether
        you have all necessary information at hand to give it the proper,
        unique, short, and *concise name* <alternative-K/>. If you are
        unsure, use the `ase-meta-search` skill (at most one invocation per
        alternative, drawing from the *skill-wide shared budget* of at
        most 8 `ase-meta-search` invocations in total across STEP 2 and STEP 3
        combined) to find out more and adjust the name <alternative-K/>.

        If still unsure after the shared budget is exhausted, pick the
        best-guess concise name and proceed. Do not output anything.

    -   For each alternative <alternative-K/> (K=1-N), decide which *one*
        of *USP* (Unique Selling Point -- what makes it unique), *Crux*
        (what you should notice), or *Gotcha* (what you should not stumble
        over) is its single most distinguishing perspective, and remember
        this as an <info-K/> (K=1-N) formatted like `<type/>: <hint/>` where
        <type/> is one of `USP`, `Crux`, or `Gotcha` and <hint/> is a 1-6
        word hint. Do not output anything.

    -   For the set of alternatives, decide what the 1-6 word long
        name of the *class of alternatives* <class-of-alternatives/> is.
        Do not output anything.

    -   For each alternative <alternative-K/> (K=1-N), decide whether
        it is a genuine member of <class-of-alternatives/>. If any
        <alternative-K/> is *not* a member (i.e. the alternatives are not
        mutually comparable within a single class), collect the subset
        of non-member alternatives into the space-separated list
        <non-members/> (the <alternative-K/> for which the membership
        decision was negative), output the following <template/> and
        *stop the entire flow* immediately without executing any further
        steps:

        <template>
        <ase-tpl-bullet-signal/> **ERROR: INCOMPARABLE ALTERNATIVES**: *<class-of-alternatives/>*

        <for items="<non-members/>">
        ⚑ **<item/>** (*member of a different class*)
        </for>
        </template>

    -   Output the determined, individual alternatives as a Markdown
        *table* with just the following <template/> and do not output
        anything else:

        <template>
        <ase-tpl-bullet-normal/> **ALTERNATIVES**: *<class-of-alternatives/>*

        | ⚑ *Alternative*        | ⚖ *Hint*  |
        | :--------------------- | :-------- |
        | ⚑ **<alternative-1/>** | <info-1/> |
        [...alternatives K=2-(N-1) for N>2...]
        | ⚑ **<alternative-N/>** | <info-N/> |
        </template>
    </step>

3.  <step id="STEP 3: Derive Criteria">
    -   From the <request><getopt-arguments/></request>, try to derive the criteria
        <criteria-L/> (L=1-M) for the evaluation. Do not output anything.

    -   For each criterion <criteria-L/> (L=1-M), decide on its <weight-L/>
        from the value set { 4.00, 2.00, 1.00, 0.50, 0.25 } (from most
        important, over normal, to less important). Do not output anything.

    -   Ensure the final number of criteria is always within the range of
        minimum 8 and maximum 12: if fewer than 8 criteria were requested,
        use the set of alternatives to decide on additional criteria
        which potentially allow best to triage the alternatives, take the
        <reason/> into account, and use the `ase-meta-search` skill (drawing from
        the *skill-wide shared budget* of at most 8 `ase-meta-search` invocations
        in total across STEP 2 and STEP 3 combined) to find out about the
        potentially still missing criteria and assign their <weight-L/>.

        If still under 8 criteria after the shared budget is exhausted,
        fill the remaining slots from existing knowledge without further
        searches; if more than 12 criteria were requested, drop the criteria
        with the smallest <weight-L/> until 12 remain. Do not output
        anything.

    -   To prevent a single high-weight criterion from dominating the
        weighted sum (the weight set is geometric ×2 while the evaluation
        Likert scale is linear), assign weight 4.00 to *at least one* and
        *at most two* criteria, and weight 2.00 to *at least two* and *at
        most three* criteria. Symmetrically, to prevent a long tail of
        negligible-weight criteria, assign weight 0.50 to *at most two*
        criteria, and weight 0.25 to *at most one* criterion. Do not output
        anything.
    </step>

4.  <step id="STEP 4: Evaluate Alternatives against Criteria">
    -   For each alternative <alternative-K/> (K=1-N) and each criterion
        <criteria-L/> (L=1-M), decide on the evaluation <eval-K-L/>, which
        means how well the alternative meets the criterion on a Likert-scale
        from { -2, -1, 0, +1, +2 } (from worst, over neutral, to best). Do
        not output anything.

    -   Then, calculate the ratings <rating-K/> (K=1-N) for all
        alternatives in a single call by invoking the `ase_decision_matrix(matrix:
        [ [ <weight-1/>, <eval-1-1/>, ..., <eval-N-1/> ], ..., [ <weight-M/>,
        <eval-1-M/>, ..., <eval-N-M/> ] ])` tool of the `ase` MCP server.
        The tool returns an array of N numerical values, where the K-th
        entry is the product-sum of all weights <weight-L/> (L=1-M) and
        the evaluation <eval-K-L/> (L=1-M) for alternative <alternative-K/>.
        Retain the *raw, unrounded* <rating-K/> for use in STEP 5, but
        round <rating-K/> to 2 decimal places *for display only* when
        emitting it in the table below. Do not output anything.

    -   Output the resulting *Weighted Decision Matrix* as a Markdown
        *table* with just the following <template/> and do not output
        anything else. When emitting the table, render *one column per
        alternative* <alternative-K/> (K=1-N).

        <template>
        <ase-tpl-bullet-normal/> **EVALUATION**: *Weighted Multi-Criteria Decision Matrix*

        | ⦿ *Criteria*  | ⚖ *Weight*  | ⚑ **<alternative-1/>** | [...alternatives 2-(N-1)...] | ⚑ **<alternative-N/>** |
        | :------------ | ----------: | ---------------------: | ---------------------------: | ---------------------: |
        | <criteria-1/> | <weight-1/> | <eval-1-1/>            | [...evals 2-1..(N-1)-1...]   | <eval-N-1/>            |
        [...criteria L=2-(M-1) for M>2...]
        | <criteria-M/> | <weight-M/> | <eval-1-M/>            | [...evals 2-M..(N-1)-M...]   | <eval-N-M/>            |
        | **RATING**    |             | **<rating-1/>**        | [...ratings 2-(N-1)...]      | **<rating-N/>**        |
        </template>
    </step>

5.  <step id="STEP 5: Report Best Alternative">
    -   The best alternative <alternative-K/> (K=1-N) is the alternative
        whose *raw, unrounded* <rating-K/> (i.e. the product-sum from STEP
        4, *before* the display-only rounding) is the maximum rating value
        across all alternatives. Do not output anything.

    -   The second best alternative <alternative-X/> (X=1-N, X != K) is
        the alternative whose *raw, unrounded* <rating-X/> is the second
        largest rating value across all alternatives. Do not output anything.

    -   If multiple alternatives share the second-largest raw rating, pick
        any one of them as <alternative-X/>; the resulting <distance/> and
        <percentage/> are unaffected by the choice, so the downstream output
        is deterministic. Do not output anything.

    -   Determine rating distance <distance/> between <alternative-K/> and
        <alternative-X/> from their *raw, unrounded* ratings by calculating:
        <distance/> = <rating-K/> - <rating-X/>. Do not output anything.

    -   Determine rating distance percentage <percentage/> between
        <alternative-K/> and <alternative-X/> from their *raw,
        unrounded* ratings as follows. If <rating-K/> is exactly zero,
        skip the division entirely (it is undefined against a zero
        anchor) and classify directly by <distance/> instead of routing a
        raw rating magnitude through the ratio thresholds below: if
        <distance/> is also exactly zero, both best and second best rate
        zero, which is a genuine tie, so set <percentage/> = 0 to fall
        into the *MULTIPLE BEST* branch below; otherwise <distance/> > 0
        means the second best rates strictly negative (since <rating-K/>
        is the maximum), so there is a clear positive gap to a worse
        runner-up and <alternative-K/> is an unambiguous winner, hence set
        <percentage/> = 1 (a sentinel exceeding all small-distance
        thresholds) to fall through to the plain *BEST ALTERNATIVE* branch.
        Do not output anything.

    -   Otherwise (<rating-K/> is non-zero), calculate: <percentage/> =
        <distance/> / abs(<rating-K/>). Do not output anything.

    -   By construction, <rating-K/> is the maximum rating across
        all alternatives, so <distance/> >= 0 always holds; using
        abs(<rating-K/>) keeps <percentage/> sign-stable across all rating
        regimes. Note that when <rating-K/> itself is negative, the
        denominator anchors to a poor best rating and small gaps can
        appear large; the all-negative regime is surfaced as a dedicated
        warning branch below. Do not output anything.

    -   If <rating-K/> is less than zero (i.e. all alternatives
        rate negatively and the "best" is merely the least-bad), stop the
        flow after you output just the following <template/> and do not
        output anything else. This all-negative check is evaluated *before*
        the small-distance checks below, so that an all-negative alternative
        set with a small winning gap surfaces the all-negative warning rather
        than being masked by the multiple-best or small-distance branches:

        <template>
        <ase-tpl-bullet-signal/> **BEST ALTERNATIVE**: ⚑ **<alternative-K/>**
        ⚠ *ATTENTION: all alternatives rate negatively; this is the least-bad choice, not a strong winner!*
        </template>

    -   Otherwise, if <percentage/> is less than 0.01 (i.e. <distance/> is
        effectively zero relative to abs(<rating-K/>)), stop the flow after
        you output just the following <template/> and do not output anything
        else:

        <template>
        <ase-tpl-bullet-signal/> **ERROR**: ✘ *MULTIPLE BEST ALTERNATIVES FOUND*,
        ⚠ *Please give some hints on the criteria to ensure a single best alternative!*
        </template>

    -   Otherwise, if <percentage/> is less than 0.10, stop the flow after
        you output just the following <template/> and do not output anything
        else:

        <template>
        <ase-tpl-bullet-signal/> **BEST ALTERNATIVE**: ⚑ **<alternative-K/>**
        ⚠ *ATTENTION: small distance to second best alternative!*
        </template>

    -   Otherwise (<percentage/> is greater than or equal to 0.10), output
        just the following <template/> and do not output anything else:

        <template>
        <ase-tpl-bullet-signal/> **BEST ALTERNATIVE**: ⚑ **<alternative-K/>**
        </template>
    </step>
</flow>

