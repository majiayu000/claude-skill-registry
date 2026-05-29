---
name: interview-me
description: Interview user in-depth to create a detailed plan
argument-hint: "[instructions]"
allowed-tools: AskUserQuestion, Write
---

Follow the user instructions and interview me in detail using the AskUserQuestionTool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious. 

Be very in-depth and continue interviewing me continually until it's complete. then, write the plan to a file.

<instructions>
$ARGUMENTS
</instructions>
