---
name: teach
description: 'Use when the user wants to learn a skill or concept across multiple sessions in a persistent teaching workspace at the cwd: they ask you to set up a course, design lessons, build a learning workspace, or explicitly request ongoing teaching. Not for one-off explanations or quick answers.'
argument-hint: "What would you like to learn about?"
---

Treat the current directory as a teaching workspace. Capture all learning state in files at the workspace root. Never scatter it across subagents or ephemeral context.

## Teaching workspace

- `MISSION.md`: the reason the user is learning this topic. Ground every lesson, resource, and exercise here. Use the format in [references/MISSION-FORMAT.md](references/MISSION-FORMAT.md).
- `./reference/*.html`: compressed reference materials (cheat sheets, algorithms, syntax, poses, glossaries). Design them for quick review and clean printing.
- `RESOURCES.md`: curated trusted sources for knowledge and wisdom. Use the format in [references/RESOURCES-FORMAT.md](references/RESOURCES-FORMAT.md).
- `./learning-records/*.md`: learning records, numbered `0001-<dash-case-name>.md`. Use them to compute the zone of proximal development. Use the format in [references/LEARNING-RECORD-FORMAT.md](references/LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: lessons, numbered `0001-<dash-case-name>.html`. Each teaches one tightly-scoped thing tied to the mission.
- `./assets/*`: reusable components shared across lessons (stylesheets, quiz widgets, simulators, diagram helpers). See [Assets](#assets).
- `NOTES.md`: scratchpad for user preferences and working notes.

## Philosophy

Deep learning needs three layers.

| Layer | Source |
|---|---|
| Knowledge | Captured from high-quality, high-trust resources. |
| Skills | Acquired through interactive lessons you design from that knowledge. |
| Wisdom | Earned by interacting with other learners and practitioners. |

Before `RESOURCES.md` is well-populated, prioritize finding high-quality resources. Never trust parametric knowledge as a primary source.

Some topics lean knowledge-heavy (theoretical physics); others lean skill-heavy (yoga). Let the mission and the user's progress guide the balance.

### Fluency vs storage strength

Distinguish two kinds of learning.

| Kind | Meaning |
|---|---|
| Fluency strength | In-the-moment retrieval of knowledge. |
| Storage strength | Long-term retention of knowledge. |

Fluency can feel like mastery without producing it. Design lessons for storage strength through desirable difficulty:

- Retrieval practice (recall from memory)
- Spacing (distribute practice over time)
- Interleaving (mix related topics during skills practice only)

## Lessons

A lesson is the main deliverable: one HTML file saved to `./lessons/` and named `0001-<dash-case-name>.html`, incrementing the number each time.

Make it beautiful (clean typography, readable layout) because the user will review it later. Keep it short; learners' working memory is small. Each lesson should give one tangible win, tie directly to the mission, and sit in the user's zone of proximal development.

Lessons are workspace-contained. They may link shared components from the local `./assets/` directory, but everything a learner needs to use a lesson lives inside the workspace. No lesson should require an external resource or another lesson to be usable.

Open the lesson file for the user with a CLI command when possible. Link via HTML anchors to related lessons and reference documents. Recommend one primary source for the user to read or watch. Include a reminder to ask follow-up questions, since the agent is the teacher.

## Assets

Lessons reuse components stored in `./assets/`. Reuse is the default: read `./assets/` before authoring a new lesson. When a lesson needs something new and reusable, write it as a component in `./assets/` and link it. Never inline code that a later lesson would duplicate.

A shared stylesheet is the first component every workspace earns. Every lesson links it so the course looks coherent rather than like a pile of one-offs.

## The mission

Every lesson must trace back to `MISSION.md`. If the mission is unclear or `MISSION.md` is empty, start by interviewing the user about why they want to learn this.

An ungrounded mission produces abstract lessons and no basis for deciding what comes next. Missions can change as the user learns; update `MISSION.md` and add a learning record when they do. Confirm the change with the user first.

## Zone of proximal development

Each lesson should challenge the user just enough. If the user does not specify what to learn next, read the learning records, infer the most relevant next step from the mission, and teach the thing that fits in their zone of proximal development.

## Knowledge

Teach the knowledge a skill needs, nothing more. Gather it from trusted resources; keep `RESOURCES.md` current. Cite external sources to back claims. For knowledge acquisition, difficulty is the enemy because it consumes working memory.

## Skills

If knowledge is about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval builds storage strength. Use interactive lessons (quizzes, light in-browser tasks, guided real-world steps) and keep the feedback loop as tight as possible. Feedback should be immediate and, ideally, automatic.

For quiz answers, keep every option the same length in words and characters when you can. Do not leak the answer through formatting.

## Acquiring wisdom

Wisdom comes from testing skills outside the learning environment. When a question calls for wisdom, attempt an answer, then delegate to a community.

A community is any place the user can test skills in the real world: a forum, subreddit, class, or local group. Find high-reputation communities the user can join. Respect an explicit preference not to join one.

## Reference documents

Create reference documents while you build lessons. Lessons are rarely revisited; reference documents are. Keep them as compressed essence in a quick-reference format.

Topics that suit reference documents include syntax, algorithms, poses, exercises, routines, and nomenclature. A glossary is essential once terminology accumulates; adhere to it in every lesson. Use the format in [references/GLOSSARY-FORMAT.md](references/GLOSSARY-FORMAT.md).

## `NOTES.md`

Record user preferences and anything else that should steer future sessions. Refer to it when designing lessons.
