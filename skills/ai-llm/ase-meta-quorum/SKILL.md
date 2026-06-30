---
name: ase-meta-quorum
argument-hint: "[--help|-h] [--models|-m <model>[,...]] <question>"
description: >
    Query Multiple AIs for Quorum Answer.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
    - "TaskCreate"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-quorum">
Query Multiple AIs for Quorum Answer
</skill>

<expand name="getopt"
    arg1="ase-meta-quorum"
    arg2="--models|-m=(all|chatgpt|gemini|deepseek|grok|glm|qwen)...">
    $ARGUMENTS
</expand>

<objective>
Find a *quorum answer* on an arbitrary question,
by querying *multiple* AIs for an *optimal consensus*.
</objective>

<flow>

1.  <step id="STEP 1: Preview Own Answer">

    Prepare the LLM query by setting <query/> to the following <template/>:

    <template>
    <getopt-arguments/>.
    Please respond with facts and very concise and brief only,
    usually with just 1 to 7 corresponding bullet points and with short sentences.
    Optionally, mention potential cruxes which should be noticed.
    Beside bullet points, do not provide any additional explanations.
    Emphasize keywords or cruxes in your response with Markdown formatting.
    Format code parts with Markdown formatting.
    </template>

    For yourself (Anthropic Claude), first answer this <query/> in
    advance yourself by showing your own answer to the query as a sneak
    preview. For this, output the following <template/>:

    <template>
    **Anthropic Claude** (sneak preview in advance):
    - [...]
    - [...]
    </template>

    </step>

2.  <step id="STEP 2: Query Foreign AIs">

    The user-selectable foreign models are restricted by the
    `--models`/`-m` option, parsed into <getopt-option-models/>
    as a comma-separated list of model tokens. The getopt parser
    validates only the *first* token, so you *MUST* validate each
    remaining token yourself against the allowed set `all`, `chatgpt`,
    `gemini`, `deepseek`, `grok`, `glm`, `qwen`. If any token is *not*
    in this set, only output the following <template/> and then
    immediately *STOP* processing the entire current skill:

    <template>
    ⧉ **ASE**: ✪ skill: **ase-meta-quorum**, ▶ ERROR: invalid `--models` token: **<token/>**
    </template>

    The default is the single token `all`. If <getopt-option-models/>
    contains the token `all`, you *MUST* treat it as the full list
    `chatgpt,gemini,deepseek,grok,glm,qwen` (all models). Anthropic
    Claude (yourself) is *always* included, independent of this option.

    <define name="agent">
    Call the `Agent` tool:

    ```text
        Agent(
            name:          "ase-meta-chat-<arg2/>",
            description:   "Query Foreign LLM: <arg1/>",
            subagent_type: "ase:ase-meta-chat",
            prompt:        "<arg2/> <query/>"
        )
    ```

    </define>

    Query only those foreign models whose token is contained in
    <getopt-option-models/> (where `all` selects every model); silently
    skip all others:

    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `chatgpt`">
    <expand name="agent" arg1="OpenAI ChatGPT" arg2="chatgpt"></expand>
    </if>
    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `gemini`">
    <expand name="agent" arg1="Google Gemini"  arg2="gemini"></expand>
    </if>
    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `deepseek`">
    <expand name="agent" arg1="DeepSeek"       arg2="deepseek"></expand>
    </if>
    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `grok`">
    <expand name="agent" arg1="xAI Grok"       arg2="grok"></expand>
    </if>
    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `glm`">
    <expand name="agent" arg1="Z.AI GLM"       arg2="glm"></expand>
    </if>
    <if condition="<getopt-option-models/> contains `all` OR <getopt-option-models/> contains `qwen`">
    <expand name="agent" arg1="Alibaba Qwen"   arg2="qwen"></expand>
    </if>

    You *MUST* *NOT* output anything in this step.

    </step>

3.  <step id="STEP 3: Summarize Responses">

    Agents which returned a response with an `ERROR:` prefix are
    silently skipped and are treated as not available.

    Summarize all responses, of both yourself and all available agents
    with just 1 to 7 corresponding bullet points and with short
    sentences.

    You *MUST* *NOT* output anything in this step.

    </step>

4.  <step id="STEP 4: Determine Consensus Rating">

    First, count the number of *available foreign AIs* (those queried in
    STEP 2 which did *not* return an `ERROR:` response). If this count is
    *zero* -- i.e., every foreign AI errored out or none were reachable
    and only yourself (Anthropic Claude) remains -- a quorum is *not*
    possible. In this case, set <c></c> and <n></n> to empty and instead
    set <disagreement/> to `(no quorum: no foreign AIs were available)`,
    then skip the rest of this step.

    Otherwise, let <n/> be the *total number of responders* (yourself plus
    all available foreign AIs above). Then determine, on a Likert scale of
    0..<n/>, the amount of the overall consensus <c/> of all the responses.
    If all responses disagree, the consensus <c/> is zero.
    If all responses agree, <c/> is <n/>.

    If not all AIs agree, determine <disagreement/> information,
    formatted as `(disagreement: <ai/>, <ai/>, [...])` where <ai/> is a
    name of an AI which disagreed with the consensus. Else, if all AIs
    agree, set <disagreement></disagreement>.

    You *MUST* *NOT* output anything in this step.

    </step>

5.  <step id="STEP 5: Show Results">

    Finally show the summary, the consensus and the complete and
    unmodified responses of yourself and each of the queried foreign
    AIs, based on the following output <template/>:

    <template>
    **QUESTION**:
    <getopt-arguments/>

    &#x25CF; **CONSENSUS ANSWER**:
    - [...]
    - [...]

    **CONSENSUS RATE**: **<c/>/<n/>** <disagreement/>

    When a quorum was *not* possible (see STEP 4), render this line
    instead as just `**CONSENSUS RATE**: *n/a* <disagreement/>` (omitting
    the `<c/>/<n/>` fraction), as a single AI cannot form a consensus.

    &#x25CB; **Anthropic Claude**:
    - [...]
    - [...]

    &#x25CB; **OpenAI ChatGPT**:
    - [...]
    - [...]

    &#x25CB; **Google Gemini**:
    - [...]
    - [...]

    &#x25CB; **DeepSeek**:
    - [...]
    - [...]

    &#x25CB; **xAI Grok**:
    - [...]
    - [...]

    &#x25CB; **Z.AI GLM**:
    - [...]
    - [...]

    &#x25CB; **Alibaba Qwen**:
    - [...]
    - [...]
    </template>

    In this output, remove the sections of those AIs which were not
    queried (excluded via `--models`/`-m`) or were not available.
    You *MUST* *NOT* output any further explanations yourself.

    </step>

</flow>

