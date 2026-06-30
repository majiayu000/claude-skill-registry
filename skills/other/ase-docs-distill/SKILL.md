---
name: ase-docs-distill
argument-hint: "[--help|-h] [--top|-t <N>] <document-reference>"
description: >
    Distill a provided document into a flat, importance-ranked list
    of its key points, each with a salience rank, a rationale, and a
    verbatim line-cited evidence snippet. Use when the user wants to
    "distill", "summarize the key points", or "extract the essence" of a
    document or pasted text.
user-invocable: true
disable-model-invocation: false
effort: high
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-docs-distill">
    Distill Key Points
</skill>

<expand name="getopt"
    arg1="ase-docs-distill"
    arg2="--top|-t=5">
    $ARGUMENTS
</expand>

<objective>
    *Distill* the content `<getopt-arguments/>` into a *flat*,
    *importance-ranked* list of its *key points* - each point an
    *atomic* claim carrying a *0-10 salience rank*, a *one-line
    rationale*, and a *verbatim, line-cited evidence* snippet - keeping
    at most `<getopt-option-top/>` points.
</objective>

Procedure
---------

<flow>

1.  <step id="STEP 1: Resolve Input">

    Resolve the document source from <getopt-arguments/> using
    *probe-as-file-first* semantics:

    1.  <if condition="<getopt-arguments/> is empty">

        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-docs-distill**, ▶ status: **no document to distill**
        </template>

        </if>

    2.  Treat the *entire* <getopt-arguments/> as a *file path*. If it
        resolves to a *readable file*, read that file and capture its
        content together with its *line numbers* into <source/>, and set
        <origin/> to the file path.

    3.  <if condition="<getopt-arguments/> does NOT resolve to a readable file">

        Treat <getopt-arguments/> *verbatim* as *pasted text*, capture it
        into <source/> numbering its lines from *1*, and set <origin/>
        to empty (so locations are cited as `:Ls-Le`).

        </if>

    4.  <if condition="<source/> is empty">

        Only output the following <template/> and then *STOP* immediately:

        <template>
        ⧉ **ASE**: ✪ skill: **ase-docs-distill**, ▶ status: **no document to distill**
        </template>

        </if>

    You *MUST* *NOT* output anything in this STEP 1.

    </step>

2.  <step id="STEP 2: Distill Key Points">

    Read <source/> and distill it into its *key points*.

    1.  Extract the document's *key points*, where each point is *one
        atomic, self-contained claim, decision, or fact* - *not* a
        section-level summary that blends several claims.

    2.  For each point, determine:

        -   A <rank/> on a *0-10* salience scale reflecting its
            *importance-to-the-reader* (impact, centrality, consequence)
            - *not* its position in the document.

        -   A one-line <rationale/> that justifies *why* the point earns
            that <rank/>.

        -   A <location/> citing the exact source line range as
            `<origin/>:Ls-Le` (for a file) or `:Ls-Le` (for pasted text),
            where `Ls` is the start line and `Le` is the end line.

        -   A *verbatim* <evidence/> snippet, copied exactly from
            <source/> (but with all newlines replaced with spaces
            and multiple spaces collapsed into a single space), that
            *proves* the point. The cited snippet *MUST* prove the
            point verbatim. If it does not, *re-investigate and re-cite
            correctly*.

    3.  *Sort* the points by <rank/> from *highest to lowest*. Within the
        same rank, keep the order of first appearance in <source/>.

    4.  Apply the *top-bound* <getopt-option-top/> as an *upper bound
        only*: keep at most `min(<getopt-option-top/>, number of salient
        points)` points and *never pad* the list with filler to reach
        the bound. If <getopt-option-top/> is *non-numeric* or *less
        than or equal to 0*, use the default *5* instead.

    You *MUST* *NOT* output anything in this STEP 2.

    </step>

3.  <step id="STEP 3: Report Ranked Points">

    For each distilled point, emit the following <template/>,
    where <rank/> is its salience rank, <point/> is the atomic claim,
    <location/> is its line-range citation, <evidence/> is the
    verbatim proving snippet, and <rationale/> is the one-line
    salience justification:

    <template>

    <ase-tpl-bullet-normal/> **KEY POINT**: **<point/>**

    ◯ LOCATION:  <location/>
    ◯ EVIDENCE:  "`<evidence/>`"
    ◯ RATIONALE: <rationale/>
    ◯ RANK:      <rank/>/10

    </template>

    In the <location/>, markup the line-range reference as
    code (with backticks) and prepend it with `▢ `.

    Keep the overall report *concise* and *brief*. Do *not* output any
    further explanation.

    </step>

</flow>
