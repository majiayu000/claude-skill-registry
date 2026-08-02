---
name: prototype-logic
description: 'Build a throwaway single-file HTML demo that answers one question about a state model, logic, or data shape. Use when someone needs to press buttons and watch state change, including a non-developer. For what a UI should look like, this is the wrong shape.'
---

# Prototype logic

Answer "does this logic feel right", not "what should this look like". Build no UI variants and touch no production rendering path.

A logic prototype is throwaway code that answers one question by letting a person press buttons and watch state change.

## Process

1. **State the question.** Write the state model and the question in one paragraph. Show that paragraph at the top of the demo itself, not in a comment.
2. **Isolate the logic.** Put the logic in a portable pure module inside one `<script>` block. Choose the shape the question needs:
   - Use a pure `(state, action) => state` reducer for discrete events over one value.
   - Use an explicit state machine when legal actions depend on the current state.
   - Use pure functions over a plain data type when there is no implicit current state.
   - Use a module with a clear method surface when the logic genuinely owns ongoing state.

   The module touches no DOM, `document`, or event handlers. The page calls the module. Nothing flows back from the module to the page. This boundary makes the logic liftable.
3. **Build one HTML file.** Keep all HTML, CSS, and JavaScript inline.
4. **Hand it over.** Let the user drive the demo. Add actions or scenarios only when their feedback asks for them.

## Page contract

Lay out the file in this order:

1. **Title and question.** Give the demo a title and one-line explanation that carries the question.
2. **Current state.** Show the full relevant state as labelled fields, never a raw JSON dump. Re-render after every click and call out what changed.
3. **Free play.** Provide one button for each action. Keep every button enabled so actions can be tried in any order.
4. **Guided walkthroughs.** Give each scenario its own tab. Include a plain-language description and an ordered sequence of real buttons. Each click performs the action and advances the walkthrough. Reset the tab to a known initial state so the same scenario runs the same way every time.

Include the happy path, a tricky edge case, and an attempt at an action that should be illegal.

Write every label in domain language, not code. Use plain HTML, CSS, and JavaScript with no framework, bundler, or server. The file must open by double-click and survive being emailed.

## Shared prototype rules

1. Mark the prototype as throwaway in its name so a casual reader cannot mistake it for production code.
2. Make it trivial to run. Opening the one HTML file is the full start procedure.
3. Keep state in memory by default. If persistence is the question, use a scratch target whose name says it must be wiped.
4. Add no tests, no error handling beyond runnability, and no abstractions.
5. Surface the full relevant state after every action.
6. When the question is settled, fold the validated module into the real code. Commit the demo to a throwaway branch off main and record both the verdict and the question it settled.

## Anti-patterns

- Do not add tests.
- Do not use a real database.
- Do not generalize for hypothetical futures.
- Do not blur the pure module into the page.
- Do not add a framework or development server.
- Never ship the HTML shell to production.
