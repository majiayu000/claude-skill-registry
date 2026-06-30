---
name: ase-meta-chat
argument-hint: "[--help|-h] <llm> <query>"
description: >
    Query foreign LLM for chat.
    Use this skill if a foreign LLM like OpenAI ChatGPT, Google Gemini,
    DeepSeek or xAI Grok should be queried with a single chat message.
user-invocable: true
disable-model-invocation: false
effort: medium
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-meta-chat">
Query Foreign LLM for Chat
</skill>

<expand name="getopt" arg1="ase-meta-chat">
    $ARGUMENTS
</expand>

<objective>
Query foreign LLM for: <query><getopt-arguments/></query>
</objective>

1.  You *MUST* *NOT* output anything in this step.
    Just call the underlying agent with the following tool:

    ```text
        Agent(
            name:          "ase-meta-chat",
            description:   "Query Foreign LLM for Chat",
            subagent_type: "ase:ase-meta-chat",
            prompt:        <query/>
        )
    ```

2.  Output the *plain response* of the `ase:ase-meta-chat` agent
    *verbatim* and *without any modifications*. Especially, do *NOT* add or
    remove any text from the agent response on your own and do not interpret
    the result in any way.

