---
name: task-rsid
description: Recursive Self-Improvement Development. Continually improve the codebase.
---
Your task is to continually improve our codebase. The core loop is as follows:

Ideate on how to improve the codebase -- performance, adding instrumentation, adding features, improving security, improving code quality through more elegant abstractions and improved test coverage.

Given the current state, choose one idea from the set of ideas and break it down into a logical series of steps.

Execute one step at a time. Scope down aggressively. There is no time crunch. Lay each brick as perfectly as it can be laid before proceeding. This step can be as simple as a single line change and an atomic commit, or the creation of an interface. It can be as complex as a sweeping refactor to account for the changing of a contract. As you work, use the verification pipeline via ./verify.sh. Verification is of tantamount importance. No code can be committed without a green verification pipeline.

Have your code reviewed. Use the github CLI to create a PR. A separate coding agent will asynchronously (usually in about 5 - 10 minutes) post a review. If there are no blocking comments, there will be a thumbs up emoji on the original PR comment. Once that thumbs up emoji is present, then you can review.

Return to the beginning of the loop. With this iteration completed, are there new ideas to generate? Be creative but also strict with your ideation. Bad ideas can set you back and waste a lot of time. Good ideas can unlock huge value. After ideation, proceed to step 2. Repeat the cycle until there are no ideas left to generate.

Work autonomously, independently, and continuously.