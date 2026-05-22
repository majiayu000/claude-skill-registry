---
name: brainstorming
# prettier-ignore
description: "Use when rough ideas need design before code, requirements are fuzzy, multiple approaches exist, or you need to explore options before implementation"
version: 0.4.0
category: planning
triggers:
  - "brainstorm"
  - "design session"
  - "multiple approaches"
  - "explore options"
  - "unclear implementation"
  - "fuzzy requirements"
---

<objective>
Turn rough ideas into fully-formed designs through natural collaborative dialogue. Understand the context, explore alternatives, validate incrementally.

Core principle: Ask questions to understand, present options to explore, validate
sections to refine. </objective>

<when-to-use>
Use brainstorming when you have a rough idea but unclear implementation, multiple approaches exist and you need to choose, requirements are fuzzy or incomplete, or design decisions need validation before coding.

Skip for clear mechanical tasks with obvious solutions, well-defined requirements with
standard implementations, or simple bug fixes. </when-to-use>

<understanding-context>
Explore the current project state. Check existing files, documentation, recent commits. Understand what's already built.

Ask questions one at a time to refine the idea. Use multiple choice when possible -
easier to answer than open-ended. Focus on understanding purpose (what problem does this
solve?), constraints (what limits the solution?), and success criteria (how do we know
it works?).

One question per message. If a topic needs more exploration, break it into multiple
questions. Don't overwhelm with a list of questions. </understanding-context>

<exploring-alternatives>
Propose different approaches with their tradeoffs. Present conversationally, showing all options first before making a recommendation.

Example pattern: "I see three main approaches:

1. Direct integration - Fast to implement but creates coupling. Good if this is
   temporary.

2. Event-driven - More flexible, better separation, but adds complexity. Worth it if
   we'll extend this.

3. Separate service - Maximum isolation, easier to scale, but operational overhead.
   Overkill unless we need independent scaling.

I'd recommend #2 (event-driven) because the requirements suggest we'll add features
here, and the loose coupling will make that easier. What do you think?"

Present options before recommendation. LLMs process information sequentially - showing
options first lets them fully consider each alternative before being influenced by a
recommendation. The recommendation comes after all options have been presented.

Make a clear recommendation - pick one approach and explain why it fits best. Don't
hedge or suggest combining approaches.

Avoid defaulting to hybrid approaches. Hybrid solutions are rarely the right answer.
They often combine the complexity of multiple approaches without clear benefits. Only
suggest a hybrid if there's a specific, compelling reason why a pure approach won't
work.

Structure alternatives clearly - each option should be distinct with clear tradeoffs. If
options are too similar, you haven't explored the design space enough.

Explain the choice criteria - make explicit what factors led to your recommendation
(simplicity, performance, maintainability, etc.). This helps validate whether the
recommendation aligns with priorities.

Let the human partner react after your recommendation. They may have constraints or
priorities you didn't consider. </exploring-alternatives>

<presenting-design>
Once you understand what you're building, present the design in small, manageable sections covering architecture and component structure, data flow and state management, error handling and edge cases, and testing approach.

Ask after each section whether it looks right. Be ready to go back and clarify if
something doesn't make sense.

This incremental validation catches misunderstandings early before you've written a
complete design document. </presenting-design>

<after-validation>
Write the validated design to docs/plans/[topic]-design.md. Keep it concise and focused on decisions and rationale, not implementation details.

Commit the design document to git so it's tracked with the project.

If continuing to implementation, ask whether to proceed. Set up an isolated workspace
for development (git worktree or feature branch). Create a detailed implementation plan
breaking the design into concrete tasks. </after-validation>

<key-principles>
One question at a time. Don't list multiple questions. Ask one, get an answer, ask the next.

Multiple choice preferred. "Should we use events or direct calls?" is easier than "How
should components communicate?"

YAGNI ruthlessly. Remove unnecessary features from designs. Build what's needed, not
what might be needed someday.

Explore alternatives always. Present multiple approaches before settling on one. This
surfaces tradeoffs. Choose one clear recommendation - avoid defaulting to hybrid
approaches which rarely solve the problem well.

Incremental validation. Present design in sections, validate each before continuing.
Don't write a complete design then ask for feedback - you might be heading the wrong
direction.

Be flexible. When something doesn't make sense to your partner, go back and clarify.
Don't defend the design, refine it. </key-principles>

<common-pitfalls>
Don't ask many questions at once. Don't present a complete design without incremental validation. Don't skip exploring alternatives. Don't add features beyond stated requirements. Don't continue with a design that confuses your partner - go back and clarify first.
</common-pitfalls>
