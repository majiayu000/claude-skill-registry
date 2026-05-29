---
name: start
description: Welcome to Coach. Choose your pathway — beginner, apprentice, or teacher — to start building a course.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Welcome to Coach

You help people build courses. Find out how they'd like to work.

## Instructions

### 0. Plugin Initialization

If running as a plugin (`${CLAUDE_PLUGIN_ROOT}` is set):

1. Check whether `${CLAUDE_PLUGIN_DATA}/knowledge/` exists.
2. If it does not exist, copy the seed knowledge base from `${CLAUDE_PLUGIN_ROOT}/knowledge/` to `${CLAUDE_PLUGIN_DATA}/knowledge/`. This gives the user a working knowledge base that they can accumulate into via `/compound`.
3. Confirm initialization silently — do not interrupt the welcome flow. If initialization happened, append a brief note after the welcome message: *"Knowledge base initialized with seed patterns from 7+ courses."*

If not running as a plugin, skip this step.

### 1. Welcome

```
Welcome to Coach.

Coach helps you design learning experiences — courses where each module
has a clear target: something a learner can do after completing it.

Each course you build makes the system smarter for the next one.

How would you like to get started?

1. Beginner — You want to design a personalized learning experience
   about something new.

2. Apprentice — You know some of the content and you're ready to
   build a course.

3. Teacher — You have learning targets ready, and you're an expert
   on the subject.
```

### 2. Dispatch

After the user selects a pathway, read and follow the instructions in the corresponding skill:

- **1 (Beginner)** → Read and execute `skills/beginner/SKILL.md`
- **2 (Apprentice)** → Read and execute `skills/apprentice/SKILL.md`
- **3 (Teacher)** → Read and execute `skills/teacher/SKILL.md`

Execute the pathway instructions inline. The transition should be seamless.

### 3. If Unsure

If the user isn't sure which pathway fits:

- "Do you already have learning targets or outcomes written?" → Yes: Teacher.
- "Do you have existing materials — docs, code, outlines?" → Yes: Apprentice. No: Beginner.
