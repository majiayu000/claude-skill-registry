---
name: docs-chain-ml-council-writing-assis
description: Let's continue by implementing a Skill for writing or revising article
  sections.
---

# Skill Implementation: Article Section Writer

Let's continue by implementing a Skill for writing or revising article sections.


```python
from council.skills import SkillBase
from council.contexts import ChatMessage, SkillContext, LLMContext
from council.llm import LLMBase, LLMMessage

from string import Template
```

Once again, we'll start by designing our prompts for this skill.


```python
self.system_prompt = "You are an expert research writer and editor. Your role is to write or revise detailed sections of research articles in markdown format."

self.main_prompt_template = Template("""
    # Task Description
    Your task is to write specific sections of research articles using your own knowledge.
    First consider the CONVERSATION HISTORY, ARTICLE OUTLINE, ARTICLE, and INSTRUCTIONS.
    Then revise the article according to the context and INSTRUCTIONS provided below.
    All headings, sections, and subsections must consist of at least three detailed paragraphs each.
    The entire REVISED ARTICLE should be written using markdown formatting.

    ## CONVERSATION HISTORY
    $conversation_history

    ## ARTICLE OUTLINE
    $outline

    ## ARTICLE
    $article

    ## INSTRUCTIONS
    $instructions

    ## REVISED ARTICLE
    ```markdown
""")
```

With this prompt, we will be asking an LLM to write or revise particular parts of an article. The `$`-variables indicate the skill's expected inputs, and just as we did for the OutlineWriterSkill, we will access values for these variables at runtime from the ChainContext.

Let's proceed by building the **SectionWriterSkill**.


```python
class SectionWriterSkill(SkillBase):
    """Write a specific section of an article."""

    def __init__(self, llm: LLMBase):
        """Build a new SectionWriterSkill."""

        super().__init__(name="SectionWriterSkill")
        self.llm = self.new_monitor("llm", llm)
```

Next we implement the skill's `execute` function.


```python
def execute(self, context: SkillContext) -> ChatMessage:
    """Execute `SectionWriterSkill`."""
```

Just as we did for the other skill, we can always access the conversation history directly from the `context`.


```python
conversation_history = [
    f"{m.kind}: {m.message}" for m in context.messages
]
```

Next we will access parts of the context that are specific to this application.

**Note:** The contents of `context.last_message` (both the `message` and `data` fields) depend on how they were populated by the Controller. This is because the Controller is responsible for *deciding how invoke Chains and their underlying Skills*, like the one we're designing now. By implementing this Skill's `execute` function with the expectation that `article`, `outline`, and `iteration` all exist, we'll need to make sure that we design and implement a Controller that will provide these.


```python
# Get the instructions
instructions = context.last_message.message

# Get the article
article = context.last_message.data['article']

# Get the outline
outline = context.last_message.data['outline']

# Get the iteration
iteration = context.last_message.data['iteration']
```

Now that we've accessed all of these state values from the context, we can fill in the main prompt, call the LLM, and format a response.


```python
main_prompt = self.main_prompt_template.substitute(
    conversation_history=conversation_history,
    outline=outline,
    article=article,
    instructions=instructions
)

messages_to_llm = [
    LLMMessage.system_message(self.system_prompt),
    LLMMessage.assistant_message(
        main_prompt
    ),
]

llm_result = self.llm.inner.post_chat_request(
    context=LLMContext.from_context(context, self.llm),
    messages=messages_to_llm,
    temperature=0.1

)
llm_response = llm_result.first_choice

return ChatMessage.skill(
    source=self.name,
    message="I've written or edited the article and placed it in the 'data' field.",
    data={'article': llm_response, 'instructions': instructions, 'iteration': iteration},
)
```

Finally, here is the entire SectionWriterSkill implementation.


```python
class SectionWriterSkill(SkillBase):
    """Write a specific section of an article."""

    def __init__(self, llm: LLMBase):
        """Build a new SectionWriterSkill."""

        super().__init__(name="SectionWriterSkill")
        self.llm = self.new_monitor("llm", llm)

        self.system_prompt = "You are an expert research writer and editor. Your role is to write or revise detailed sections of research articles in markdown format."

        self.main_prompt_template = Template("""
        # Task Description
        Your task is to write specific sections of research articles using your own knowledge.
        First consider the CONVERSATION HISTORY, ARTICLE OUTLINE, ARTICLE, and INSTRUCTIONS.
        Then revise the article according to the context and INSTRUCTIONS provided below.
        All headings, sections, and subsections must consist of at least three detailed paragraphs each.
        The entire REVISED ARTICLE should be written using markdown formatting.

        ## CONVERSATION HISTORY
        $conversation_history

        ## ARTICLE OUTLINE
        $outline

        ## ARTICLE
        $article

        ## INSTRUCTIONS
        $instructions

        ## REVISED ARTICLE
        ```markdown
        """)

    def execute(self, context: SkillContext) -> ChatMessage:
        """Execute `SectionWriterSkill`."""

        # Get the chat message history
        conversation_history = [
            f"{m.kind}: {m.message}" for m in context.messages
        ]

        # Get the article
        article = context.last_message.data['article']

        # Get the outline
        outline = context.last_message.data['outline']

        # Get the iteration
        iteration = context.last_message.data['iteration']

        # Get the instructions
        instructions = context.last_message.message

        main_prompt = self.main_prompt_template.substitute(
            conversation_history=conversation_history,
            outline=outline,
            article=article,
            instructions=instructions
        )

        messages_to_llm = [
            LLMMessage.system_message(self.system_prompt),
            LLMMessage.assistant_message(
                main_prompt
            ),
        ]

        llm_result = self.llm.inner.post_chat_request(
            context=LLMContext.from_context(context, self.llm),
            messages=messages_to_llm,
            temperature=0.1

        )
        llm_response = llm_result.first_choice

        return ChatMessage.skill(
            source=self.name,
            message="I've written or edited the article and placed it in the 'data' field.",
            data={'article': llm_response, 'instructions': instructions, 'iteration': iteration},
        )
```

Next we will move on to defining one of the most important parts of a Council Agent - the [Controller](./4_controller.md).
