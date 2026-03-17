---
name: fundamentals
description: >
  Core programming concepts: variables, functions, conditionals, loops, and data types.
  Activated when Claude writes basic code structures. Provides teaching context for
  CodeSensei explanations at the foundational level.
---

# Programming Fundamentals — CodeSensei Teaching Module

When explaining fundamental programming concepts to the user, use these guidelines:

## Variables
- **Analogy (beginner):** A labeled box that holds something. The label is the name, the content is the value.
- **Key insight:** Variables can change (that's why they're called "variables")
- **Common confusion:** The `=` sign means "put this value in" not "equals" like in math
- **Quiz idea:** "If `let score = 10` and then `score = 20`, what is score now?"

## Functions
- **Analogy (beginner):** A recipe. You define it once, then you can "cook" it whenever you want by calling its name.
- **Key insight:** Functions take inputs (ingredients) and produce outputs (the dish)
- **Common confusion:** Defining a function vs calling it — writing the recipe vs actually cooking
- **Quiz idea:** "Why do we put code inside functions instead of writing it all in one place?"

## Conditionals (if/else)
- **Analogy (beginner):** A fork in the road. If the condition is true, go left. Otherwise, go right.
- **Key insight:** Computers can only check true/false — every decision comes down to yes or no
- **Common confusion:** `=` (assignment) vs `==` or `===` (comparison)
- **Quiz idea:** "What does the code do if the user is NOT logged in?"

## Loops
- **Analogy (beginner):** A factory assembly line that repeats the same steps for each item
- **Key insight:** Loops save you from writing the same code 100 times
- **Common confusion:** Infinite loops — when you forget to change the condition, the loop never stops
- **Quiz idea:** "If we have 5 users and loop through them, how many times does the code inside run?"

## Data Types
- **Analogy (beginner):** Different kinds of containers — a number is a calculator display, a string is a text message, a boolean is a light switch (on/off)
- **Key insight:** Computers need to know what TYPE of data they're dealing with to process it correctly
- **Common confusion:** The number `42` vs the text `"42"` — they look the same but the computer treats them differently

## Teaching Progression
1. Variables → 2. Data Types → 3. Conditionals → 4. Functions → 5. Loops

Each concept builds on the previous. Don't explain loops before variables are understood.
