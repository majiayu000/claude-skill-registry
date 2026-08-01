---
name: ase-meta-proximity
argument-hint: "[--help|-h] [--ground|-g] [--loop|-l] <topic>"
description: >
    Determine the conceptual proximity of a topic -- its parent topic,
    its most relevant sibling topics, and its most relevant child
    topics -- optionally grounded in Internet/Web facts and optionally
    navigable in an interactive loop. Use when the user wants to explore
    the conceptual neighborhood of a topic, or mentions "proximity" or
    "related topics".
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-dialog.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-proximity">
Determine the Conceptual Proximity of a Topic
</skill>

<expand name="getopt"
    arg1="ase-meta-proximity"
    arg2="--ground|-g --loop|-l">
    $ARGUMENTS
</expand>

<objective>
*Determine* the *conceptual proximity* of the following topic -- its
*parent* topic, its most relevant *sibling* topics, and its most
relevant *child* topics:
<topic><getopt-arguments/></topic>
</objective>

<define name="gather-facts">
<if condition="<getopt-option-ground/> is equal `true`">
Set <prompt>Search the Internet/Web and gather facts about
<arg1/></prompt>.

Then use the `ase-meta-search` skill in a sub-agent to gather facts with
the following tool call and store the returned facts in the placeholder
named `<arg2/>`:

`Agent(
    description: "Query Web Search Service",
    subagent_type: "ase:ase-meta-search",
    prompt: "<prompt/>",
    run_in_background: false
)`

<if condition="the placeholder named `<arg2/>` contains no usable facts">
Set the placeholder named `<arg2/>` to empty, so the determination below
falls back to model knowledge, and output the following <template/>:

<template>
<ase-tpl-bullet-secondary/> **WARNING**: grounding found no usable facts -- falling back to model knowledge.
</template>
</if>
</if>
<else>
Use the model's world knowledge and determine facts about <arg1/> and
store those facts in the placeholder named `<arg2/>`.
</else>
</define>

<flow>

1.  <step id="STEP 1: Check Topic">

    <if condition="<topic/> is empty">
    Only output the following <template/> and then immediately *STOP*
    processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-meta-proximity**, ▶ ERROR: expected a `<topic>` argument
    </template>
    </if>

    </step>

2.  <step id="STEP 2: Explore Proximity">

    *REPEAT* the following sub-steps in a *LOOP* until either
    <getopt-option-loop/> is *not* equal `true` (then the loop runs
    exactly *once* and stops after rendering), or the user declines/cancels
    the dialog in sub-step 5:

    1.  *Determine Topic*:

        Determine the canonical name of the central *topic* which is stored
        in <topic/>.

        <expand name="gather-facts"
            arg1="the following topic: <topic/>"
            arg2="facts-topic"></expand>

        Ground the determination of the canonical name of the topic
        <topic/> in the facts of <facts-topic/> and do not contradict
        them. Update <topic/> accordingly.

    2.  *Determine Proximity*:

        Determine the *conceptual proximity* of the current <topic/>
        along three *dimensions*:

        -   **PARENT**:

            The single most relevant *parent* topic (the broader topic
            that <topic/> is a specialization of), which will be stored
            in <parent/>.

            <expand name="gather-facts"
                arg1="the PARENT topic (the broader topic that the given topic is a specialization of) of the following topic: <topic/>"
                arg2="facts-parent"></expand>

            Ground the determination of the canonical name of the parent
            topic <parent/> in the facts of <facts-parent/> and do not
            contradict them.

        -   **SIBLINGS**:

            The *four* most relevant *sibling* topics (topics on the
            same level that share the same parent), which will be stored
            in <sibling-1/> to <sibling-4/>.

            <expand name="gather-facts"
                arg1="the SIBLING topics (topics on the same level that share the same parent) of the following topic: <topic/>"
                arg2="facts-siblings"></expand>

            Ground the determination of the canonical names of the most
            relevant sibling topics <sibling-1/> to <sibling-4/> in the
            facts of <facts-siblings/> and do not contradict them.

        -   **CHILDREN**:

            The *four* most relevant *children* topics (narrower topics
            that are specializations of <topic/>), stored in <child-1/>
            to <child-4/>.

            <expand name="gather-facts"
                arg1="the CHILDREN topics (narrower topics that are specializations) of the following topic: <topic/>"
                arg2="facts-children"></expand>

            Ground the determination of the canonical names of the most
            relevant children topics <child-1/> to <child-4/> in the
            facts of <facts-children/> and do not contradict them.

    3.  *Render Proximity*:

        Output the result with the following <template/>, listing each
        proximity topic under its bullet-prefixed section header.

        <template>
        <ase-tpl-head title="PROXIMITY TOPICS"/>

        ●   **PARENT**:
        ↑   <parent/>

        ●   **TOPIC**:
        ○   **<topic/>**

        ●   **SIBLINGS**:
        ⇄   <sibling-1/>
        ⇄   <sibling-2/>
        ⇄   <sibling-3/>
        ⇄   <sibling-4/>

        ●   **CHILDREN**:
        ↓   <child-1/>
        ↓   <child-2/>
        ↓   <child-3/>
        ↓   <child-4/>

        <ase-tpl-foot title="PROXIMITY TOPICS"/>
        </template>

    4.  <if condition="<getopt-option-loop/> is not equal `true`">
        The loop runs only once in non-interactive mode: *break* out of
        the *loop* and stop processing without any further output.
        </if>

    5.  *Navigate Proximity*:

        In the following, you *MUST* *NOT* use your built-in
        <user-dialog-tool/> tool! Instead, you *MUST* just show a custom
        dialog according to the expanded `custom-dialog` definition. You
        *MUST* closely follow this definition.

        Let the user pick one of the nine proximity topics to navigate
        to by raising a question with the following custom dialog:

        <expand name="custom-dialog" arg1="--no-other">
            Navigate: Which proximity topic would you like to navigate to?
            PARENT:    ↑ <parent/>
            SIBLING-1: ⇄ <sibling-1/>
            SIBLING-2: ⇄ <sibling-2/>
            SIBLING-3: ⇄ <sibling-3/>
            SIBLING-4: ⇄ <sibling-4/>
            CHILD-1:   ↓ <child-1/>
            CHILD-2:   ↓ <child-2/>
            CHILD-3:   ↓ <child-3/>
            CHILD-4:   ↓ <child-4/>
        </expand>

        Check the tool <result/> and dispatch accordingly:

        -   If <result/> is `CANCEL`:
            *Break* out of the *loop* and stop processing without any
            further output.

        -   Otherwise: Set <topic/> to the proximity topic corresponding
            to the selected <result/> (the <parent/>, <sibling-K/>, or
            <child-K/> value behind the chosen label).

            Then you *MUST* *continue* the *loop* at step **2.1**.

    </step>

</flow>
