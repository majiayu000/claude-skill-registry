---
name: hud-first
description: This skill should be used when the user asks to "build an AI assistant", "create a chatbot", "make an agent that does X for me", "design a copilot feature", "automate this workflow with AI", or requests delegation-style AI features. Offers a reframe from copilot patterns (conversation, delegation) to HUD patterns (ambient awareness, perception augmentation).
---

<objective>
Shift from the copilot anti-pattern (delegation, conversation, context-switching) to the HUD pattern (perception, ambient awareness, flow preservation). Based on Mark Weiser's 1992 critique of AI agents, Douglas Engelbart's Intelligence Augmentation, Steve Jobs' "bicycle for the mind," and Amber Case's Calm Technology principles.
</objective>

<quick_start>
When facing a problem, ask:

**Instead of:** "What agent/assistant can do this for me?"
**Ask:** "What new sense would let me perceive this problem differently?"

The goal is not automation. The goal is augmentation.
</quick_start>

<essential_distinction>
| Copilot (Anti-pattern) | HUD (Target) |
|------------------------|--------------|
| You talk to it | You see through it |
| Demands attention | Operates in periphery |
| Delegates your judgment | Extends your perception |
| Context-switching tax | Flow-state preserving |
| "Do this for me" | "Now I notice more" |
</essential_distinction>

<reframing_process>
To reframe any problem using HUD-first thinking:

1. **Identify the copilot instinct**
   - What task are you tempted to delegate?
   - What conversation would you have with an assistant?

2. **Extract the information need**
   - What does the assistant need to *know* to help?
   - What would you need to *perceive* to not need the assistant?

3. **Design the sense extension**
   - What visual/auditory/haptic signal would make this obvious?
   - How could this information be ambient rather than on-demand?

4. **Validate with the spellcheck test**
   - Spellcheck doesn't ask "would you like help spelling?"
   - It just shows red squiggles. You notice. You decide.
   - Does your solution pass this test?
</reframing_process>

<examples>
<example name="code_review">
<copilot_approach>
"Review this code for bugs and suggest improvements"
→ Conversation, delegation, waiting, context-switch to read response
</copilot_approach>

<hud_approach>
- Inline complexity warnings (like spell-check for cognitive load)
- Test coverage heatmap in the gutter
- Type inference annotations that appear on hover
- Mutation testing results as background highlights
→ You *see* code quality. No conversation needed.
</hud_approach>
</example>

<example name="email_triage">
<copilot_approach>
"Summarize my inbox and tell me what's urgent"
→ You're now reading the AI's interpretation, not the emails
</copilot_approach>

<hud_approach>
- Urgency highlighting (color gradient based on signals)
- Relationship context badges (how often you interact)
- Sentiment indicators (tone of message)
- Thread age/velocity visualization
→ You *perceive* inbox state at a glance. You decide what matters.
</hud_approach>
</example>

<example name="debugging">
<copilot_approach>
"Find the bug in this function"
→ Delegation of understanding. You learn nothing.
</copilot_approach>

<hud_approach>
- Live variable values overlaid during execution
- Control flow visualization (which branches taken)
- State diff between invocations
- Anomaly highlighting (this value is unusual)
→ You *see* program behavior. The bug becomes obvious.
</hud_approach>
</example>

<example name="writing">
<copilot_approach>
"Rewrite this paragraph to be clearer"
→ You lose your voice. You're editing AI output, not your thoughts.
</copilot_approach>

<hud_approach>
- Readability score in margin (updates as you type)
- Sentence complexity highlighting
- Passive voice indicators
- Repetition detection
→ You *sense* where prose is weak. You fix it your way.
</hud_approach>
</example>
</examples>

<design_principles>
From Calm Technology (Weiser, Case):

1. **Require minimal attention** — Lives in peripheral awareness
2. **Extend senses, don't replace judgment** — New information channels, same human decision-maker
3. **Communicate without speaking** — Color, position, sound, vibration—not dialog boxes
4. **Stay invisible until needed** — Information surfaces when relevant, recedes when not
5. **Amplify Human+Machine** — Optimize the interface between them, not either alone
</design_principles>

<when_copilot_is_fine>
Delegation works for:
- Routine, predictable tasks (autopilot for straight-level flight)
- Tasks you genuinely don't want to understand
- One-time operations with clear success criteria

But for expert work, creative work, complex judgment—you want instruments, not a chatbot to argue with.
</when_copilot_is_fine>

<challenge>
For your current problem:

1. What would a "red squiggly" look like for this domain?
2. What sense would you need to perceive the solution space directly?
3. How could the information be *ambient and continuous* rather than *requested and discrete*?

The best AI interface is often invisible. You just become aware of more.
</challenge>

<success_criteria>
HUD-first reframing is successful when:

- The proposed solution doesn't require conversation or explicit requests
- Information flows continuously rather than on-demand
- The human remains in control of judgment and decision
- Flow state is preserved (no context-switching to interact with AI)
- The user would describe it as "now I just *notice* things I didn't before"
</success_criteria>
