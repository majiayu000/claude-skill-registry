---
name: ase-meta-eli5
argument-hint: "[--help|-h] [--ground|-g] <topic>"
description: >
    Explain a topic in "Explain Like I'm 5" (ELI5) style, optionally
    grounded in Internet/Web facts. Use when the user wants a topic
    explained in a very simple, child-friendly way, or mentions "eli5"
    or "explain like I'm 5".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-eli5">
Explain a Topic Like I'm 5
</skill>

<expand name="getopt"
    arg1="ase-meta-eli5"
    arg2="--ground|-g">
    $ARGUMENTS
</expand>

<objective>
*Explain* the following topic in "Explain Like I'm 5" (ELI5) style,
so that even a five year old child could understand it:
<topic><getopt-arguments/></topic>
</objective>

<flow>

1.  <step id="STEP 1: Check Topic">

    <if condition="<topic/> is empty">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-meta-eli5**, ▶ ERROR: expected a `<topic>` argument
    </template>
    </if>

    Set <facts></facts> (set to empty)

    </step>

2.  <step id="STEP 2: Ground Topic" condition="<getopt-option-ground/> is equal `true`">

    Use the `ase-meta-search` skill in a sub-agent to gather facts
    about the <topic/>: call the tool...

    `Agent(
        description: "Query Web Search Service",
        subagent_type: "ase:ase-meta-search",
        prompt: "Search the Internet/Web and gather facts about the following topic: <topic/>",
        run_in_background: false
    )`

    ...and store the returned facts in <facts/>.

    <if condition="<facts/> contains no usable facts about <topic/>">

    Set <facts></facts> (set facts to empty), so the explanation below
    falls back to model knowledge, and output the following <template/>:

    <template>
    <ase-tpl-bullet-secondary/> **WARNING**: grounding found no usable facts -- falling back to model knowledge.
    </template>

    </if>

    </step>

3.  <step id="STEP 3: Explain Topic">

    Explain the <topic/> in "Explain Like I'm 5" (ELI5) style: use
    *simple*, *jargon-free* wording a five year old child could
    understand -- short sentences, everyday words, and familiar images.
    Do *not* use technical terms without immediately putting them into
    child-friendly words.

    <if condition="<facts/> is not empty">
    Ground the explanation in the facts of <facts/> and do not
    contradict them.
    </if>

    For this, first, explain *WHAT* the topic is and store it in
    <what/>. Second, give an *ANALOGY* by comparing the topic to
    something from the everyday life of a child and store this in
    <analogy/>. Third, explain *WHY* the topic matters and store this in
    <why/>.

    Ensure that each of <what/>, <analogy/>, and <why/> is a *very
    brief* and *concise* single text paragraph.

    Output the result with the following <template/>:

    <template>
    <ase-tpl-bullet-secondary/> **TOPIC**: **<topic/>**

    <ase-tpl-bullet-normal/> **WHAT**: <what/>.

    <ase-tpl-bullet-normal/> **ANALOGY**: <analogy/>.

    <ase-tpl-bullet-signal/> **WHY**: <why/>.
    </template>

    </step>

</flow>
