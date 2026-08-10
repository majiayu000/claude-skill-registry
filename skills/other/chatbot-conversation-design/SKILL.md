---
name: chatbot-conversation-design
description: Design structured, engaging chatbot conversations with robust intent handling, slot filling, disambiguation, error recovery, and graceful fallback strategies. Use when the user requests chatbot conversation design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Chatbot Conversation Design

This skill provides a comprehensive framework for designing chatbot conversations that feel natural, handle ambiguity gracefully, and guide users toward successful outcomes. It covers the full design lifecycle — from persona definition and intent mapping through dialog state management, error recovery, and iterative testing. The focus is on building conversations that are resilient to unexpected inputs while maintaining a consistent, helpful tone.

## Workflow

1. **Define the bot persona and scope.** Establish the chatbot's personality traits (friendly, professional, concise, witty) and guardrails. Define what the bot can and cannot do. A well-scoped bot that excels at five tasks outperforms a vague bot that attempts fifty. Document the persona in a style guide that includes vocabulary preferences, emoji usage rules, response length targets, and escalation triggers.

2. **Map intents, entities, and user journeys.** Identify every intent the bot must handle — both primary task intents (e.g., `order.place`, `account.reset_password`) and meta-intents (e.g., `help`, `cancel`, `speak_to_human`). For each intent, list the required entities (slots) the bot must collect. Map the conversation flows as directed graphs showing happy paths, branching points, and exit conditions. Ensure every path terminates in either a resolution or a graceful handoff.

3. **Design slot-filling and disambiguation dialogs.** For each intent, define the slot-filling sequence — which entities are required, which are optional, and in what order the bot should prompt for them. When user input is ambiguous (e.g., "the large one" when multiple products qualify), design disambiguation prompts that present clear options without overwhelming the user. Use confirmation prompts for high-stakes actions like payments or cancellations.

4. **Build error recovery and fallback flows.** Design three tiers of fallback: (1) rephrasing the question when confidence is low, (2) offering a constrained set of options when the intent is unclear after two attempts, and (3) escalating to a human agent when the bot cannot recover. Never let the conversation hit a dead end. Every error state should include a recovery path and a way to restart or exit gracefully.

5. **Implement context carryover and state management.** Define how dialog state persists across turns. Specify which slots carry forward (e.g., the user's name should persist for the session) and which reset between tasks. Design the context stack so the bot can handle mid-conversation topic switches ("Actually, before that, can you check my balance?") and return to the original flow afterward.

6. **Prototype, test, and iterate.** Build a low-fidelity prototype using conversation scripts or tools like Botmock, Voiceflow, or Dialogflow CX. Test with real users to identify where conversations break down. Track metrics: task completion rate, average turns to resolution, fallback trigger rate, and escalation rate. Iterate on the weakest flows first.

## Usage

This skill is for developers, UX writers, and product managers designing conversational interfaces. Provide the agent with the bot's purpose, target user base, and the list of tasks it should handle.

- **For new chatbots:** Follow the workflow end-to-end to build a complete conversational architecture.
- **For existing chatbots:** Use this skill to audit conversation flows, identify dead ends, and improve error handling.

**Prompt format:**

~~~
Design a chatbot conversation for [use case].
Bot persona: [personality traits]
Supported tasks: [list of tasks]
Platform: [web widget / Slack / WhatsApp / voice assistant]
~~~

## Examples

### Example 1: Customer Support Bot — Complete Conversation Flow

**Design specification:**

~~~json
{
  "bot_name": "HelpBot",
  "persona": "Friendly, efficient, empathetic",
  "intent": "order.track",
  "required_entities": [
    { "name": "order_id", "type": "string", "prompt": "What's your order number?" },
    { "name": "email", "type": "email", "prompt": "What email did you use for the order?" }
  ],
  "optional_entities": [
    { "name": "issue_type", "type": "enum", "values": ["delayed", "damaged", "wrong_item", "other"] }
  ]
}
~~~

**Conversation flow:**

~~~
User: Where's my order?

HelpBot: I'd be happy to look that up for you! Could you share your order number?
         It usually starts with "ORD-" and is in your confirmation email.

User: ORD-29481

HelpBot: Got it. And what email address did you place the order with?

User: marcus@email.com

HelpBot: Thanks, Marcus. I found your order — here's the latest status:

         Order: ORD-29481
         Status: In transit
         Carrier: FedEx
         Tracking: 7749 2381 0042
         Estimated delivery: Thursday, March 6

         Is there anything else about this order I can help with?

User: It was supposed to arrive yesterday.

HelpBot: I'm sorry about the delay. It looks like there was a weather-related
         shipping disruption. Based on the latest tracking update, it should
         arrive by end of day Thursday.

         Would you like me to:
         1. Send you tracking updates via email
         2. Connect you with our shipping team
         3. Something else

User: Option 1 please.

HelpBot: Done! You'll receive email updates at marcus@email.com whenever the
         tracking status changes. Is there anything else I can help with?
~~~

### Example 2: Error Handling and Fallback Flow

**Scenario:** The bot receives an input it cannot classify.

~~~
User: asdfghjkl

HelpBot: I didn't quite catch that. Could you rephrase what you're looking for?
         I can help with things like:
         - Tracking an order
         - Returns and refunds
         - Account questions

User: I want to do the thing with the stuff

HelpBot: I want to make sure I help you with the right thing. Which of these
         is closest to what you need?
         1. Track an existing order
         2. Start a return or refund
         3. Update your account info
         4. Something else

User: 4

HelpBot: No problem — let me connect you with a team member who can help.
         You'll be transferred to a live agent shortly. Your reference
         number is #SUP-8842 so you won't have to repeat anything.

         [Escalating to human agent...]
~~~

**State management notes:** After two failed classification attempts (confidence < 0.3), the bot transitions from open-ended prompts to a constrained option list. After a third failure or explicit "something else" selection, it escalates with full context attached to the handoff payload.

## Best Practices

- **Design for the unhappy path first.** Most conversations will deviate from the ideal flow. Invest more time in error recovery and edge cases than in the happy path, which is straightforward to build.
- **Keep bot utterances under 3 sentences.** Long bot responses cause users to skim or disengage. Break complex information into multiple turns or use structured formats (lists, cards).
- **Confirm before executing irreversible actions.** Always add a confirmation step before actions like cancellations, payments, or data deletion. Show the user exactly what will happen.
- **Use progressive disclosure.** Don't dump all options upfront. Start with the most common paths and offer "more options" only when needed.
- **Carry context across turns naturally.** If a user says "I'd like a large," the bot should remember they were discussing pizza from the previous turn. Explicit confirmation ("A large pizza, right?") is better than asking them to repeat.
- **Provide escape hatches at every step.** Users should always be able to say "cancel," "start over," or "talk to a human" and get an immediate, helpful response.

## Edge Cases

- **Multi-intent inputs.** When a user says "Track my order and also start a return," the bot should acknowledge both intents and handle them sequentially, confirming when it transitions from one task to the next.
- **Mid-flow topic switching.** If a user changes topics mid-conversation, push the current dialog state onto a stack and handle the new intent. Offer to return to the previous task when the interruption resolves.
- **Contradictory information.** When a user provides conflicting details (e.g., different email addresses in the same session), flag the inconsistency and ask for clarification rather than silently using the latest value.
- **Sensitive or emotional content.** If the user expresses frustration, anger, or distress, the bot should acknowledge the emotion ("I understand this is frustrating") before proceeding with the solution. Never respond with generic cheerfulness to a clearly upset user.
- **Platform-specific constraints.** WhatsApp limits message length and button options differently than a web widget. Design conversations that adapt to the platform's capabilities rather than forcing a one-size-fits-all flow.
