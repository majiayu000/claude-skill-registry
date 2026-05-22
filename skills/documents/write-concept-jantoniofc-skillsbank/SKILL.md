---
name: write-concept
description: Write or review JavaScript concept documentation pages for the 33 JavaScript
  Concepts project, following strict structure and quality guidelines
risk: safe
source: community
license: MIT
---

# Skill: Write JavaScript Concept Documentation

Use this skill when writing or improving concept documentation pages for the 33 JavaScript Concepts project.

## When to Use

- Creating a new concept page in `/docs/concepts/`
- Rewriting or significantly improving an existing concept page
- Reviewing an existing concept page for quality and completeness
- Adding explanatory content to a concept

## Target Audience

Remember: **the reader might be someone who has never coded before or is just learning JavaScript**. Write with empathy for beginners while still providing depth for intermediate developers. Make complex topics feel approachable and never assume prior knowledge without linking to prerequisites.

## Writing Guidelines

### Voice and Tone

- **Conversational but authoritative**: Write like you're explaining to a smart friend
- **Encouraging**: Make complex topics feel approachable
- **Practical**: Focus on real-world applications and use cases
- **Concise**: Respect the reader's time; avoid unnecessary verbosity
- **Question-driven**: Open sections with questions the reader might have

### Avoiding AI-Generated Language

Your writing must sound human, not AI-generated. Here are specific patterns to avoid:

#### Words and Phrases to Avoid

| ❌ Avoid | ✓ Use Instead |
|----------|---------------|
| "Master [concept]" | "Learn [concept]" |
| "dramatically easier/better" | "much easier" or "cleaner" |
| "one fundamental thing" | "one simple thing" |
| "one of the most important concepts" | "This is a big one" |
| "essential points" | "key things to remember" |
| "understanding X deeply improves" | "knowing X well makes Y easier" |
| "To truly understand" | "Let's look at" or "Here's how" |
| "This is crucial" | "This trips people up" |
| "It's worth noting that" | Just state the thing directly |
| "It's important to remember" | "Don't forget:" or "Remember:" |
| "In order to" | "To" |
| "Due to the fact that" | "Because" |
| "At the end of the day" | Remove entirely |
| "When it comes to" | Remove or rephrase |
| "In this section, we will" | Just start explaining |
| "As mentioned earlier" | Remove or link to the section |

#### Repetitive Emphasis Patterns

Don't use the same lead-in pattern repeatedly. Vary your emphasis:

| Instead of repeating... | Vary with... |
|------------------------|--------------|
| "Key insight:" | "Don't forget:", "The pattern:", "Here's the thing:" |
| "Best practice:" | "Pro tip:", "Quick check:", "A good habit:" |
| "Important:" | "Watch out:", "Heads up:", "Note:" |
| "Remember:" | "Keep in mind:", "The rule:", "Think of it this way:" |

#### Em Dash (—) Overuse

AI-generated text overuses em dashes. Limit their use and prefer periods, commas, or colons:

| ❌ Em Dash Overuse | ✓ Better Alternative |
|-------------------|---------------------|
| "async/await — syntactic sugar that..." | "async/await. It's syntactic sugar that..." |
| "understand Promises — async/await is built..." | "understand Promises. async/await is built..." |
| "doesn't throw an error — you just get..." | "doesn't throw an error. You just get..." |
| "outside of async functions — but only in..." | "outside of async functions, but only in..." |
| "Fails fast — if any Promise rejects..." | "Fails fast. If any Promise rejects..." |
| "achieve the same thing — the choice..." | "achieve the same thing. The choice..." |

**When em dashes ARE acceptable:**
- In Key Takeaways section (consistent formatting for the numbered list)
- In MDN card titles (e.g., "async function — MDN")
- In interview answer step-by-step explanations (structured formatting)
- Sparingly when a true parenthetical aside reads naturally

**Rule of thumb:** If you have more than 10-15 em dashes in a 1500-word document outside of structured sections, you're overusing them. After writing, search for "—" and evaluate each one.

#### Superlatives and Filler Words

Avoid vague superlatives that add no information:

| ❌ Avoid | ✓ Use Instead |
|----------|---------------|
| "dramatically" | "much" or remove entirely |
| "fundamentally" | "simply" or be specific about what's fundamental |
| "incredibly" | remove or be specific |
| "extremely" | remove or be specific |
| "absolutely" | remove |
| "basically" | remove (if you need it, you're not explaining clearly) |
| "essentially" | remove or just explain directly |
| "very" | remove or use a stronger word |
| "really" | remove |
| "actually" | remove (unless correcting a misconception) |
| "In fact" | remove (just state the fact) |
| "Interestingly" | remove (let the reader decide if it's interesting) |

#### Stiff/Formal Phrases

Replace formal academic-style phrases with conversational alternatives:

| ❌ Stiff | ✓ Conversational |
|---------|------------------|
| "It should be noted that" | "Note that" or just state it |
| "One might wonder" | "You might wonder" |
| "This enables developers to" | "This lets you" |
| "The aforementioned" | "this" or name it again |
| "Subsequently" | "Then" or "Next" |
| "Utilize" | "Use" |
| "Commence" | "Start" |
| "Prior to" | "Before" |
| "In the event that" | "If" |
| "A considerable amount of" | "A lot of" or "Many" |

#### Playful Touches (Use Sparingly)

Add occasional human touches to make the content feel less robotic, but don't overdo it:

```javascript
// ✓ Good: One playful comment per section
// Callback hell - nested so deep you need a flashlight

// ✓ Good: Conversational aside  
// forEach and async don't play well together — it just fires and forgets:

// ✓ Good: Relatable frustration
// Finally, error handling that doesn't make you want to flip a table.

// ❌ Bad: Trying too hard
// Callback hell - it's like a Russian nesting doll had a baby with a spaghetti monster! 🍝

// ❌ Bad: Forced humor
// Let's dive into the AMAZING world of Promises! 🎉🚀
```

**Guidelines:**
- One or two playful touches per major section is enough
- Humor should arise naturally from the content
- Avoid emojis in body text (they're fine in comments occasionally)
- Don't explain your jokes
- If a playful line doesn't work, just be direct instead

### Page Structure (Follow This Exactly)

Every concept page MUST follow this structure in this exact order:

```mdx
---
title: "Concept Name: [Hook] in JavaScript"
sidebarTitle: "Concept Name: [Hook]"
description: "SEO-friendly description in 150-160 characters starting with action word"
---

[Opening hook - Start with engaging questions that make the reader curious]
[Example: "How does JavaScript get data from a server? How do you load user profiles, submit forms, or fetch the latest posts from an API?"]

[Immediately show a simple code example demonstrating the concept]

```javascript
// This is how you [do the thing] in JavaScript
const example = doSomething()
console.log(example)  // Expected output
```

[Brief explanation connecting to what they'll learn, with **[inline MDN links](https://developer.mozilla.org/...)** for key terms]

<Info>
**What you'll learn in this guide:**
- Key learning outcome 1
- Key learning outcome 2
- Key learning outcome 3
- Key learning outcome 4 (aim for 5-7 items)
</Info>

<Warning>
[Optional: Prerequisites or important notices - place AFTER Info box]
**Prerequisite:** This guide assumes you understand [Related Concept](/concepts/related-concept). If you're not comfortable with that yet, read that guide first!
</Warning>

---

## [First Major Section - e.g., "What is X?"]

[Core explanation with inline MDN links for any new terms/APIs introduced]

[Optional: CardGroup with MDN reference links for this section]

---

## [Analogy Section - e.g., "The Restaurant Analogy"]

[Relatable real-world analogy that makes the concept click]

[ASCII art diagram visualizing the concept]

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DIAGRAM TITLE                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│    [Visual representation of the concept]                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## [Core Concepts Section]

[Deep dive with code examples, tables, and Mintlify components]

<Steps>
  <Step title="Step 1">
    Explanation of the first step
  </Step>
  <Step title="Step 2">
    Explanation of the second step
  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Subtopic 1">
    Detailed explanation with code examples
  </Accordion>
  <Accordion title="Subtopic 2">
    Detailed explanation with code examples
  </Accordion>
</AccordionGroup>

<Tip>
**Quick Rule of Thumb:** [Memorable summary or mnemonic]
</Tip>

---

## [The API/Implementation Section]

[How to actually use the concept in code]

### Basic Usage

```javascript
// Basic example with step-by-step comments
// Step 1: Do this
const step1 = something()

// Step 2: Then this
const step2 = somethingElse(step1)

// Step 3: Finally
console.log(step2)  // Expected output
```

### [Advanced Pattern]

```javascript
// More complex real-world example
```

---

## [Common Mistakes Section - e.g., "The #1 Fetch Mistake"]

[Highlight the most common mistake developers make]

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VISUAL COMPARISON                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  WRONG WAY                           RIGHT WAY                           │
│  ─────────                           ─────────                           │
│  • Problem 1                         • Solution 1                        │
│  • Problem 2                         • Solution 2                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

```javascript
// ❌ WRONG - Explanation of why this is wrong
const bad = wrongApproach()

// ✓ CORRECT - Explanation of the right way
const good = correctApproach()
```

<Warning>
**The Trap:** [Clear explanation of what goes wrong and why]
</Warning>

---

## [Advanced Patterns Section]

[Real-world patterns and best practices]

### Pattern Name

```javascript
// Reusable pattern with practical application
async function realWorldExample() {
  // Implementation
}

// Usage
const result = await realWorldExample()
```

---

## Key Takeaways

<Info>
**The key things to remember:**

1. **First key point** — Brief explanation

2. **Second key point** — Brief explanation

3. **Third key point** — Brief explanation

4. **Fourth key point** — Brief explanation

5. **Fifth key point** — Brief explanation

[Aim for 8-10 key takeaways that summarize everything]
</Info>

---

## Test Your Knowledge

<AccordionGroup>
  <Accordion title="Question 1: [Specific question about the concept]">
    **Answer:**
    
    [Clear explanation]
    
    ```javascript
    // Code example demonstrating the answer
    ```
  </Accordion>
  
  <Accordion title="Question 2: [Another question]">
    **Answer:**
    
    [Clear explanation with code if needed]
  </Accordion>
  
  [Aim for 5-6 questions covering the main topics]
</AccordionGroup>

---

## Related Concepts

<CardGroup cols={2}>
  <Card title="Related Concept 1" icon="icon-name" href="/concepts/slug">
    How it connects to this concept
  </Card>
  <Card title="Related Concept 2" icon="icon-name" href="/concepts/slug">
    How it connects to this concept
  </Card>
</CardGroup>

---

## Reference

<CardGroup cols={2}>
  <Card title="Main Topic — MDN" icon="book" href="https://developer.mozilla.org/...">
    Official MDN documentation for the main concept
  </Card>
  <Card title="Related API — MDN" icon="book" href="https://developer.mozilla.org/...">
    Additional MDN reference
  </Card>
</CardGroup>

## Articles

<CardGroup cols={2}>
  <Card title="Article Title" icon="newspaper" href="https://...">
    Brief description of what the reader will learn from this article.
  </Card>
  [Aim for 4-6 high-quality articles]
</CardGroup>

## Videos

<CardGroup cols={2}>
  <Card title="Video Title" icon="video" href="https://...">
    Brief description of what the video covers.
  </Card>
  [Aim for 3-4 quality videos]
</CardGroup>
```

---

## SEO Guidelines

SEO (Search Engine Optimization) is **critical** for this project. Each concept page should rank for the various ways developers search for that concept. Our goal is to appear in search results for queries like:

- "what is [concept] in JavaScript"
- "how does [concept] work in JavaScript"  
- "[concept] JavaScript explained"
- "[concept] JavaScript tutorial"
- "JavaScript [concept] example"

Every writing decision — from title to structure to word choice — should consider search intent.

---

### Target Keywords for Each Concept

Each concept page targets a **keyword cluster** — the family of related search queries. Before writing, identify these for your concept:

| Keyword Type | Pattern | Example (DOM) |
|--------------|---------|---------------|
| **Primary** | [concept] + JavaScript | "DOM JavaScript", "JavaScript DOM" |
| **What is** | what is [concept] in JavaScript | "what is the DOM in JavaScript" |
| **How does** | how does [concept] work | "how does the DOM work in JavaScript" |
| **How to** | how to [action] with [concept] | "how to manipulate the DOM" |
| **Tutorial** | [concept] tutorial/guide/explained | "DOM tutorial JavaScript" |
| **Comparison** | [concept] vs [related] | "DOM vs virtual DOM" |

**More Keyword Cluster Examples:**

<AccordionGroup>
  <Accordion title="Closures Keyword Cluster">
    | Type | Keywords |
    |------|----------|
    | Primary | "JavaScript closures", "closures in JavaScript" |
    | What is | "what is a closure in JavaScript", "what are closures" |
    | How does | "how do closures work in JavaScript", "how closures work" |
    | Why use | "why use closures JavaScript", "closure use cases" |
    | Example | "JavaScript closure example", "closure examples" |
    | Interview | "closure interview questions JavaScript" |
  </Accordion>
  
  <Accordion title="Promises Keyword Cluster">
    | Type | Keywords |
    |------|----------|
    | Primary | "JavaScript Promises", "Promises in JavaScript" |
    | What is | "what is a Promise in JavaScript", "what are Promises" |
    | How does | "how do Promises work", "how Promises work JavaScript" |
    | How to | "how to use Promises", "how to chain Promises" |
    | Comparison | "Promises vs callbacks", "Promises vs async await" |
    | Error | "Promise error handling", "Promise catch" |
  </Accordion>
  
  <Accordion title="Event Loop Keyword Cluster">
    | Type | Keywords |
    |------|----------|
    | Primary | "JavaScript event loop", "event loop JavaScript" |
    | What is | "what is the event loop in JavaScript" |
    | How does | "how does the event loop work", "how event loop works" |
    | Visual | "event loop explained", "event loop visualization" |
    | Related | "call stack and event loop", "task queue JavaScript" |
  </Accordion>
  
  <Accordion title="Call Stack Keyword Cluster">
    | Type | Keywords |
    |------|----------|
    | Primary | "JavaScript call stack", "call stack JavaScript" |
    | What is | "what is the call stack in JavaScript" |
    | How does | "how does the call stack work" |
    | Error | "call stack overflow JavaScript", "maximum call stack size exceeded" |
    | Visual | "call stack explained", "call stack visualization" |
  </Accordion>
</AccordionGroup>

---

### Title Tag Optimization

The frontmatter has **two title fields**:
- `title` — The page's `<title>` tag (SEO, appears in search results)
- `sidebarTitle` — The sidebar navigation text (cleaner, no "JavaScript" since we're on a JS site)

**The Two-Title Pattern:**

```mdx
---
title: "Closures: How Functions Remember Their Scope in JavaScript"
sidebarTitle: "Closures: How Functions Remember Their Scope"
---
```

- **`title`** ends with "in JavaScript" for SEO keyword placement
- **`sidebarTitle`** omits "JavaScript" for cleaner navigation

**Rules:**
1. **50-60 characters** ideal length for `title` (Google truncates longer titles)
2. **Concept name first** — lead with the topic, "JavaScript" comes at the end
3. **Add a hook** — what will the reader understand or be able to do?
4. **Be specific** — generic titles don't rank

**Title Formulas That Work:**

```
title: "[Concept]: [What You'll Understand] in JavaScript"
sidebarTitle: "[Concept]: [What You'll Understand]"

title: "[Concept]: [Benefit or Outcome] in JavaScript"
sidebarTitle: "[Concept]: [Benefit or Outcome]"
```

**Title Examples:**

| ❌ Bad | ✓ title (SEO) | ✓ sidebarTitle (Navigation) |
|--------|---------------|----------------------------|
| `"Closures"` | `"Closures: How Functions Remember Their Scope in JavaScript"` | `"Closures: How Functions Remember Their Scope"` |
| `"DOM"` | `"DOM: How Browsers Represent Web Pages in JavaScript"` | `"DOM: How Browsers Represent Web Pages"` |
| `"Promises"` | `"Promises: Handling Async Operations in JavaScript"` | `"Promises: Handling Async Operations"` |
| `"Call Stack"` | `"Call Stack: How Function Execution Works in JavaScript"` | `"Call Stack: How Function Execution Works"` |
| `"Event Loop"` | `"Event Loop: How Async Code Actually Runs in JavaScript"` | `"Event Loop: How Async Code Actually Runs"` |
| `"Scope"` | `"Scope and Closures: Variable Visibility in JavaScript"` | `"Scope and Closures: Variable Visibility"` |
| `"this"` | `"this: How Context Binding Works in JavaScript"` | `"this: How Context Binding Works"` |
| `"Prototype"` | `"Prototype Chain: Understanding Inheritance in JavaScript"` | `"Prototype Chain: Understanding Inheritance"` |

**Character Count Check:**
Before finalizing, verify your `title` length:
- Under 50 chars: Consider adding more descriptive context
- 50-60 chars: Perfect length
- Over 60 chars: Will be truncated in search results — shorten it

---

### Meta Description Optimization

The `description` field becomes the meta description — **the snippet users see in search results**. A compelling description increases click-through rate.

**Rules:**
1. **150-160 characters** maximum (Google truncates longer descriptions)
2. **Include primary keyword** in the first half
3. **Include secondary keywords** naturally if space allows
4. **Start with an action word** — "Learn", "Understand", "Discover" (avoid "Master" — sounds AI-generated)
5. **Promise specific value** — what will they learn?
6. **End with a hook** — give them a reason to click

**Description Formula:**

```
[Action word] [what the concept is] in JavaScript. [Specific things they'll learn]: [topic 1], [topic 2], and [topic 3].
```

**Description Examples:**

| Concept | ❌ Too Short (Low CTR) | ✓ SEO-Optimized (150-160 chars) |
|---------|----------------------|--------------------------------|
| DOM | `"Understanding the DOM"` | `"Learn how the DOM works in JavaScript. Understand how browsers represent HTML as a tree, select and manipulate elements, traverse nodes, and optimize rendering."` |
| Closures | `"Functions that remember"` | `"Learn JavaScript closures and how functions remember their scope. Covers lexical scoping, practical use cases, memory considerations, and common closure patterns."` |
| Promises | `"Async JavaScript"` | `"Understand JavaScript Promises for handling asynchronous operations. Learn to create, chain, and combine Promises, handle errors properly, and write cleaner async code."` |
| Event Loop | `"How async works"` | `"Discover how the JavaScript event loop manages async code execution. Understand the call stack, task queue, microtasks, and why JavaScript is single-threaded but non-blocking."` |
| Call Stack | `"Function execution"` | `"Learn how the JavaScript call stack tracks function execution. Understand stack frames, execution context, stack overflow errors, and how recursion affects the stack."` |
| this | `"Understanding this"` | `"Learn the 'this' keyword in JavaScript and how context binding works. Covers the four binding rules, arrow function behavior, and how to use call, apply, and bind."` |

**Character Count Check:**
- Under 120 chars: You're leaving value on the table — add more specifics
- 150-160 chars: Optimal length
- Over 160 chars: Will be truncated — edit ruthlessly

---

### Keyword Placement Strategy

Keywords must appear in strategic locations — but **always naturally**. Keyword stuffing hurts rankings.

**Priority Placement Locations:**

| Priority | Location | How to Include |
|----------|----------|----------------|
| 🔴 Critical | Title | Primary keyword in first half |
| 🔴 Critical | Meta description | Primary keyword + 1-2 secondary |
| 🔴 Critical | First paragraph | Natural mention within first 100 words |
| 🟠 High | H2 headings | Question-format headings with keywords |
| 🟠 High | "What you'll learn" box | Topic-related phrases |
| 🟡 Medium | H3 subheadings | Related keywords and concepts |
| 🟡 Medium | Key Takeaways | Reinforce main keywords naturally |
| 🟢 Good | Alt text | If using images, include keywords |

**Example: Keyword Placement for DOM Page**

```mdx
---
title: "DOM: How Browsers Represent Web Pages in JavaScript"      ← 🔴 Primary: "in JavaScript" at end
sidebarTitle: "DOM: How Browsers Represent Web Pages"             ← Sidebar: no "JavaScript"
description: "Learn how the DOM works in JavaScript. Understand   ← 🔴 Primary: "DOM works in JavaScript"
how browsers represent HTML as a tree, select and manipulate      ← 🔴 Secondary: "manipulate elements"
elements, traverse nodes, and optimize rendering."
---

How does JavaScript change what you see on a webpage?             ← Hook question
The **Document Object Model (DOM)** is a programming interface    ← 🔴 Primary keyword in first paragraph
for web documents. It represents your HTML as a **tree of 
objects** that JavaScript can read and manipulate.

<Info>
**What you'll learn in this guide:**                              ← 🟠 Topic reinforcement
- What the DOM actually is
- How to select elements (getElementById vs querySelector)        ← Secondary keywords
- How to traverse the DOM tree
- How to create, modify, and remove elements                      ← "DOM" implicit
- How browsers render the DOM (Critical Rendering Path)
</Info>

## What is the DOM in JavaScript?                                 ← 🟠 H2 with question keyword

The DOM (Document Object Model) is...                             ← Natural repetition

## How the DOM Works                                              ← 🟠 H2 with "how" keyword

## DOM Manipulation Methods                                       ← 🟡 H3 with related keyword

## Key Takeaways                                                  ← 🟡 Reinforce in summary
```

**Warning Signs of Keyword Stuffing:**
- Same exact phrase appears more than 3-4 times per 1000 words
- Sentences read awkwardly because keywords were forced in
- Using keywords where pronouns ("it", "they", "this") would be natural

---

### Answering Search Intent

Google ranks pages that **directly answer the user's query**. Structure your content to satisfy search intent immediately.

**The First Paragraph Rule:**

The first paragraph after any H2 should directly answer the implied question. Don't build up to the answer — lead with it.

```mdx
<!-- ❌ BAD: Builds up to the answer -->
## What is the Event Loop?

Before we can understand the event loop, we need to talk about JavaScript's 
single-threaded nature. You see, JavaScript can only do one thing at a time, 
and this creates some interesting challenges. The way JavaScript handles 
this is through something called... the event loop.

<!-- ✓ GOOD: Answers immediately -->
## What is the Event Loop?

The **event loop** is JavaScript's mechanism for executing code, handling events, 
and managing asynchronous operations. It continuously monitors the call stack 
and task queue, moving queued callbacks to the stack when it's empty — this is 
how JavaScript handles async code despite being single-threaded.
```

**Question-Format H2 Headings:**

Use H2s that match how people search:

| Search Query | H2 to Use |
|--------------|-----------|
| "what is the DOM" | `## What is the DOM?` |
| "how closures work" | `## How Do Closures Work?` |
| "why use promises" | `## Why Use Promises?` |
| "when to use async await" | `## When Should You Use async/await?` |

---

### Featured Snippet Optimization

Featured snippets appear at **position zero** — above all organic results. Structure your content to win them.

**Snippet Types and How to Win Them:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      FEATURED SNIPPET TYPES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  QUERY TYPE           SNIPPET FORMAT        YOUR CONTENT STRUCTURE       │
│  ───────────          ──────────────        ─────────────────────────    │
│                                                                          │
│  "What is X"          Paragraph             40-60 word definition        │
│                                             immediately after H2         │
│                                                                          │
│  "How to X"           Numbered list         <Steps> component or         │
│                                             numbered Markdown list       │
│                                                                          │
│  "X vs Y"             Table                 Comparison table with        │
│                                             clear column headers         │
│                                                                          │
│  "Types of X"         Bulleted list         Bullet list under            │
│                                             descriptive H2               │
│                                                                          │
│  "[X] examples"       Bulleted list or      Code examples with           │
│                       code block            brief explanations           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Pattern 1: Definition Snippet (40-60 words)**

For "what is [concept]" queries:

```mdx
## What is a Closure in JavaScript?

A **closure** is a function that retains access to variables from its outer 
(enclosing) scope, even after that outer function has finished executing. 
Closures are created every time a function is created in JavaScript, allowing 
inner functions to "remember" and access their lexical environment.
```

**Why this wins:**
- H2 matches search query exactly
- Bold keyword in first sentence
- 40-60 word complete definition
- Explains the "why" not just the "what"

**Pattern 2: List Snippet (Steps)**

For "how to [action]" queries:

```mdx
## How to Make a Fetch Request in JavaScript

<Steps>
  <Step title="1. Call fetch() with the URL">
    The `fetch()` function takes a URL and returns a Promise that resolves to a Response object.
  </Step>
  
  <Step title="2. Check if the response was successful">
    Always verify `response.ok` before processing — fetch doesn't throw on HTTP errors.
  </Step>
  
  <Step title="3. Parse the response body">
    Use `response.json()` for JSON data, `response.text()` for plain text.
  </Step>
  
  <Step title="4. Handle errors properly">
    Wrap everything in try/catch to handle both network and HTTP errors.
  </Step>
</Steps>
```

**Pattern 3: Table Snippet (Comparison)**

For "[X] vs [Y]" queries:

```mdx
## == vs === in JavaScript

| Aspect | `==` (Loose Equality) | `===` (Strict Equality) |
|--------|----------------------|------------------------|
| Type coercion | Yes — converts types before comparing | No — types must match |
| Speed | Slower (coercion overhead) | Faster (no coercion) |
| Predictability | Can produce surprising results | Always predictable |
| Recommendation | Avoid in most cases | Use by default |

```javascript
// Examples
5 == "5"    // true (string coerced to number)
5 === "5"   // false (different types)
```
```

**Pattern 4: List Snippet (Types/Categories)**

For "types of [concept]" queries:

```mdx
## Types of Scope in JavaScript

JavaScript has three types of scope that determine where variables are accessible:

- **Global Scope** — Variables declared outside any function or block; accessible everywhere
- **Function Scope** — Variables declared inside a function with `var`; accessible only within that function
- **Block Scope** — Variables declared with `let` or `const` inside `{}`; accessible only within that block
```

---

### Content Structure for SEO

How you structure content affects both rankings and user experience.

**The Inverted Pyramid:**

Put the most important information first. Search engines and users both prefer content that answers questions immediately.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THE INVERTED PYRAMID                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                                                                          │
│            ┌─────────────────────────────────────┐                       │
│            │       ANSWER THE QUESTION           │  ← First 100 words   │
│            │       Definition + Core Concept     │    (most important)  │
│            └──────────────────┬──────────────────┘                       │
│                               │                                          │
│              ┌────────────────┴────────────────┐                         │
│              │       EXPLAIN HOW IT WORKS       │  ← Next 300 words     │
│              │       Mechanism + Visual Diagram │    (supporting info)  │
│              └────────────────┬─────────────────┘                        │
│                               │                                          │
│            ┌──────────────────┴──────────────────┐                       │
│            │         SHOW PRACTICAL EXAMPLES      │  ← Code examples    │
│            │         Code + Step-by-step          │    (proof it works) │
│            └──────────────────┬──────────────────┘                       │
│                               │                                          │
│        ┌──────────────────────┴──────────────────────┐                   │
│        │            COVER EDGE CASES                  │  ← Advanced      │
│        │            Common mistakes, gotchas          │    (depth)       │
│        └──────────────────────┬──────────────────────┘                   │
│                               │                                          │
│    ┌──────────────────────────┴──────────────────────────┐               │
│    │               ADDITIONAL RESOURCES                   │  ← External  │
│    │               Related concepts, articles, videos     │    (links)   │
│    └──────────────────────────────────────────────────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Scannable Content Patterns:**

Google favors content that's easy to scan. Use these elements:

| Element | SEO Benefit | When to Use |
|---------|-------------|-------------|
| Short paragraphs | Reduces bounce rate | Always (2-4 sentences max) |
| Bullet lists | Often become featured snippets | Lists of 3+ items |
| Numbered lists | "How to" snippet potential | Sequential steps |
| Tables | High snippet potential | Comparisons, reference data |
| Bold text | Highlights keywords for crawlers | First mention of key terms |
| Headings (H2/H3) | Structure signals to Google | Every major topic shift |

**Content Length Guidelines:**

| Length | Assessment | Action |
|--------|------------|--------|
| Under 1,000 words | Too thin | Add more depth, examples, edge cases |
| 1,000-1,500 words | Minimum viable | Acceptable for simple concepts |
| 1,500-2,500 words | Good | Standard for most concept pages |
| 2,500-4,000 words | Excellent | Ideal for comprehensive guides |
| Over 4,000 words | Evaluate | Consider splitting into multiple pages |

**Note:** Length alone doesn't guarantee rankings. Every section must add value — don't pad content.

---

### Internal Linking for SEO

Internal links help search engines understand your site structure and distribute page authority.

**Topic Cluster Strategy:**

Think of concept pages as an interconnected network. Every concept should link to 3-5 related concepts:

```
                              ┌─────────────────┐
                      ┌───────│    Promises     │───────┐
                      │       └────────┬────────┘       │
                      │                │                │
                      ▼                ▼                ▼
              ┌───────────┐    ┌───────────────┐    ┌─────────────┐
              │async/await│◄──►│  Event Loop   │◄──►│  Callbacks  │
              └───────────┘    └───────────────┘    └─────────────┘
                      │                │                │
                      │                ▼                │
                      │       ┌───────────────┐        │
                      └──────►│  Call Stack   │◄───────┘
                              └───────────────┘
```

**Link Placement Guidelines:**

1. **In Prerequisites (Warning box):**
```mdx
<Warning>
**Prerequisite:** This guide assumes you understand [Promises](/concepts/promises) and the [Event Loop](/concepts/event-loop). Read those first if you're not comfortable with asynchronous JavaScript.
</Warning>
```

2. **In Body Content (natural context):**
```mdx
When the callback finishes, it's added to the task queue — which is managed by the [event loop](/concepts/event-loop).
```

3. **In Related Concepts Section:**
```mdx
<CardGroup cols={2}>
  <Card title="Promises" icon="handshake" href="/concepts/promises">
    async/await is built on top of Promises
  </Card>
  <Card title="Event Loop" icon="arrows-spin" href="/concepts/event-loop">
    How JavaScript manages async operations
  </Card>
</CardGroup>
```

**Anchor Text Best Practices:**

| ❌ Bad Anchor Text | ✓ Good Anchor Text | Why |
|-------------------|-------------------|-----|
| "click here" | "event loop guide" | Descriptive, includes keyword |
| "this article" | "our Promises concept" | Tells Google what page is about |
| "here" | "JavaScript closures" | Keywords in anchor text |
| "read more" | "understanding the call stack" | Natural, informative |

---

### URL and Slug Best Practices

URLs (slugs) are a minor but meaningful ranking factor.

**Rules:**
1. **Use lowercase** — `closures` not `Closures`
2. **Use hyphens** — `call-stack` not `call_stack` or `callstack`
3. **Keep it short** — aim for 3-5 words maximum
4. **Include primary keyword** — the concept name
5. **Avoid stop words** — skip "the", "and", "in", "of" unless necessary

**Slug Examples:**

| Concept | ❌ Avoid | ✓ Use |
|---------|---------|-------|
| The Event Loop | `the-event-loop` | `event-loop` |
| this, call, apply and bind | `this-call-apply-and-bind` | `this-call-apply-bind` |
| Scope and Closures | `scope-and-closures` | `scope-and-closures` (acceptable) or `scope-closures` |
| DOM and Layout Trees | `dom-and-layout-trees` | `dom` or `dom-layout-trees` |

**Note:** For this project, slugs are already set. When creating new pages, follow these conventions.

---

### Opening Paragraph: The SEO Power Move

The opening paragraph is prime SEO real estate. It should:
1. Hook the reader with a question they're asking
2. Include the primary keyword naturally
3. Provide a brief definition or answer
4. Set up what they'll learn

**Template:**

```mdx
[Question hook that matches search intent?] [Maybe another question?]

The **[Primary Keyword]** is [brief definition that answers "what is X"]. 
[One sentence explaining why it matters or what it enables].

```javascript
// Immediately show a simple example
```

[Brief transition to "What you'll learn" box]
```

**Example (Closures):**

```mdx
Why do some functions seem to "remember" variables that should have disappeared? 
How can a callback still access variables from a function that finished running 
long ago?

The answer is **closures** — one of JavaScript's most powerful (and often 
misunderstood) features. A closure is a function that retains access to its 
outer scope's variables, even after that outer scope has finished executing.

```javascript
function createCounter() {
  let count = 0  // This variable is "enclosed" by the returned function
  return function() {
    count++
    return count
  }
}

const counter = createCounter()
console.log(counter())  // 1
console.log(counter())  // 2 — it remembers!
```

Understanding closures unlocks patterns like private variables, factory functions, 
and the module pattern that power modern JavaScript.
```

**Why this works for SEO:**
- Question hooks match how people search ("why do functions remember")
- Bold keyword in first paragraph
- Direct definition answers "what is a closure"
- Code example demonstrates immediately
- Natural setup for learning objectives

---

## Inline Linking Rules (Critical!)

### Always Link to MDN

Whenever you introduce a new Web API, method, object, or JavaScript concept, **link to MDN immediately**. This gives readers a path to deeper learning.

```mdx
<!-- ✓ CORRECT: Link on first mention -->
The **[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)** is JavaScript's modern way to make network requests.

The **[Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)** object contains everything about the server's reply.

Most modern APIs return data in **[JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON)** format.

<!-- ❌ WRONG: No links -->
The Fetch API is JavaScript's modern way to make network requests.
```

### Link to Related Concept Pages

When mentioning concepts covered in other pages, link to them:

```mdx
<!-- ✓ CORRECT: Internal links to related concepts -->
If you're not familiar with it, check out our [async/await concept](/concepts/async-await) first.

This guide assumes you understand [Promises](/concepts/promises).

<!-- ❌ WRONG: No internal links -->
If you're not familiar with async/await, you should learn that first.
```

### Common MDN Link Patterns

| Concept | MDN URL Pattern |
|---------|-----------------|
| Web APIs | `https://developer.mozilla.org/en-US/docs/Web/API/{APIName}` |
| JavaScript Objects | `https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/{Object}` |
| HTTP | `https://developer.mozilla.org/en-US/docs/Web/HTTP` |
| HTTP Methods | `https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/{METHOD}` |
| HTTP Headers | `https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers` |

---

## Code Examples Best Practices

### 1. Start with the Simplest Possible Example

```javascript
// ✓ GOOD: Start with the absolute basics
// This is how you fetch data in JavaScript
const response = await fetch('https://api.example.com/users/1')
const user = await response.json()
console.log(user.name)  // "Alice"
```

### 2. Use Step-by-Step Comments

```javascript
// Step 1: fetch() returns a Promise that resolves to a Response object
const responsePromise = fetch('https://api.example.com/users')

// Step 2: When the response arrives, we get a Response object
responsePromise.then(response => {
  console.log(response.status)      // 200
  
  // Step 3: The body is a stream, we need to parse it
  return response.json()
})
.then(data => {
  // Step 4: Now we have the actual data
  console.log(data)
})
```

### 3. Show Output in Comments

```javascript
const greeting = "Hello"
console.log(typeof greeting)  // "string"

const numbers = [1, 2, 3]
console.log(numbers.length)   // 3
```

### 4. Use ❌ and ✓ for Wrong/Correct Patterns

```javascript
// ❌ WRONG - This misses HTTP errors!
try {
  const response = await fetch('/api/users/999')
  const data = await response.json()
} catch (error) {
  // Only catches NETWORK errors, not 404s!
}

// ✓ CORRECT - Check response.ok
try {
  const response = await fetch('/api/users/999')
  
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`)
  }
  
  const data = await response.json()
} catch (error) {
  // Now catches both network AND HTTP errors
}
```

### 5. Use Meaningful Variable Names

```javascript
// ❌ BAD
const x = [1, 2, 3]
const y = x.map(z => z * 2)

// ✓ GOOD
const numbers = [1, 2, 3]
const doubled = numbers.map(num => num * 2)
```

### 6. Progress from Simple to Complex

```javascript
// Level 1: Basic usage
fetch('/api/users')

// Level 2: With options
fetch('/api/users', {
  method: 'POST',
  body: JSON.stringify({ name: 'Alice' })
})

// Level 3: Full real-world pattern
async function createUser(userData) {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  })
  
  if (!response.ok) {
    throw new Error(`Failed to create user: ${response.status}`)
  }
  
  return response.json()
}
```

---

## Resource Curation Guidelines

External resources (articles, videos) are valuable, but must meet quality standards.

### Quality Standards

Only include resources that are:

1. **JavaScript-focused** — No resources primarily about other languages (C#, Python, Java, etc.), even if the concepts are similar
2. **Still accessible** — Verify all links work before publishing
3. **High quality** — From reputable sources (MDN, javascript.info, freeCodeCamp, well-known educators)
4. **Up to date** — Avoid outdated resources; check publication dates for time-sensitive topics
5. **Accurate** — Skim the content to verify it doesn't teach anti-patterns

### Writing Resource Descriptions

Each resource needs a **specific, engaging 2-sentence description** explaining what makes it unique. Generic descriptions waste the reader's time.

```mdx
<!-- ❌ Generic (bad) -->
<Card title="JavaScript Promises Tutorial" icon="newspaper" href="...">
  Learn about Promises in JavaScript.
</Card>

<!-- ❌ Generic (bad) -->
<Card title="Async/Await Explained" icon="newspaper" href="...">
  A comprehensive guide to async/await.
</Card>

<!-- ✓ Specific (good) -->
<Card title="JavaScript Async/Await Tutorial" icon="newspaper" href="https://javascript.info/async-await">
  The go-to reference for async/await fundamentals. Includes exercises at the end to test your understanding of rewriting promise chains.
</Card>

<!-- ✓ Specific (good) -->
<Card title="JavaScript Visualized: Promises & Async/Await" icon="newspaper" href="...">
  Animated GIFs showing the call stack, microtask queue, and event loop in action. This is how async/await finally "clicked" for thousands of developers.
</Card>

<!-- ✓ Specific (good) -->
<Card title="How to Escape Async/Await Hell" icon="newspaper" href="...">
  The pizza-and-drinks ordering example makes parallel vs sequential execution crystal clear. Essential reading once you know the basics.
</Card>
```

**Description Formula:**
1. **Sentence 1:** What makes this resource unique OR what it specifically covers
2. **Sentence 2:** Why a reader should click (what they'll gain, who it's best for, what stands out)

**Avoid in descriptions:**
- "Comprehensive guide to..." (vague)
- "Great tutorial on..." (vague)  
- "Learn all about..." (vague)
- "Everything you need to know about..." (cliché)

### Recommended Sources

**Articles (Prioritize):**

| Source | Why |
|--------|-----|
| javascript.info | Comprehensive, well-maintained, exercises included |
| MDN Web Docs | Official reference, always accurate |
| freeCodeCamp | Beginner-friendly, practical tutorials |
| dev.to (Lydia Hallie, etc.) | Visual explanations, community favorites |
| CSS-Tricks | DOM, browser APIs, visual topics |

**Videos (Prioritize):**

| Creator | Style |
|---------|-------|
| Web Dev Simplified | Clear, beginner-friendly, concise |
| Fireship | Fast-paced, modern, entertaining |
| Traversy Media | Comprehensive crash courses |
| Fun Fun Function | Deep-dives with personality |
| Wes Bos | Practical, real-world focused |

**Avoid:**
- Resources in other programming languages (C#, Python, Java) even if concepts overlap
- Outdated tutorials (pre-ES6 syntax for modern concepts)
- Paywalled content (unless there's a free tier)
- Low-quality Medium articles (check engagement and accuracy)
- Resources that teach anti-patterns
- Videos over 2 hours (link to specific timestamps if valuable)

### Verifying Resources

Before including any resource:

1. **Click the link** — Verify it loads and isn't behind a paywall
2. **Skim the content** — Ensure it's accurate and well-written
3. **Check the date** — For time-sensitive topics, prefer recent content
4. **Read comments/reactions** — Community feedback reveals quality issues
5. **Test code examples** — If they include code, verify it works

---

## ASCII Art Diagrams

Use ASCII art to visualize concepts. Make them boxed and labeled:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        THE REQUEST-RESPONSE CYCLE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│    YOU (Browser)                              KITCHEN (Server)           │
│    ┌──────────┐                               ┌──────────────┐           │
│    │          │  ──── "I'd like pasta" ────►  │              │           │
│    │    :)    │         (REQUEST)             │    [chef]    │           │
│    │          │                               │              │           │
│    │          │  ◄──── Here you go! ────────  │              │           │
│    │          │         (RESPONSE)            │              │           │
│    └──────────┘                               └──────────────┘           │
│                                                                          │
│    The waiter (HTTP) is the protocol that makes this exchange work!      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Mintlify Components Reference

| Component | When to Use |
|-----------|-------------|
| `<Info>` | "What you'll learn" boxes, Key Takeaways |
| `<Warning>` | Common mistakes, gotchas, prerequisites |
| `<Tip>` | Pro tips, rules of thumb, best practices |
| `<Note>` | Additional context, side notes |
| `<AccordionGroup>` | Expandable content, Q&A sections, optional deep-dives |
| `<Tabs>` | Comparing different approaches side-by-side |
| `<Steps>` | Sequential processes, numbered workflows |
| `<CardGroup>` | Resource links (articles, videos, references) |
| `<Card>` | Individual resource with icon and link |

### Card Icons Reference

| Content Type | Icon |
|--------------|------|
| MDN/Official Docs | `book` |
| Articles/Blog Posts | `newspaper` |
| Videos | `video` |
| Courses | `graduation-cap` |
| Related Concepts | Context-appropriate (`handshake`, `hourglass`, `arrows-spin`, `sitemap`, etc.) |

---

## Quality Checklist

Before finalizing a concept page, verify ALL of these:

### Structure
- [ ] Opens with engaging questions that hook the reader
- [ ] Shows a simple code example immediately after the opening
- [ ] Has "What you'll learn" Info box right after the opening
- [ ] Major sections are separated by `---` horizontal rules
- [ ] Has a real-world analogy with ASCII art diagram
- [ ] Has a "Common Mistakes" or "The #1 Mistake" section
- [ ] Has a "Key Takeaways" section summarizing 8-10 points
- [ ] Has a "Test Your Knowledge" section with 5-6 Q&As
- [ ] Ends with Related Concepts, Reference, Articles, Videos in that order

### Linking
- [ ] All new Web APIs/methods have inline MDN links on first mention
- [ ] All related concepts link to their concept pages (`/concepts/slug`)
- [ ] Reference section has multiple MDN links
- [ ] 4-6 quality articles with descriptions
- [ ] 3-4 quality videos with descriptions

### Code Examples
- [ ] First code example is dead simple
- [ ] Uses step-by-step comments for complex examples
- [ ] Shows output in comments (`// "result"`)
- [ ] Uses ❌ and ✓ for wrong/correct patterns
- [ ] Uses meaningful variable names
- [ ] Progresses from simple to complex

### Content Quality
- [ ] Written for someone who might be new to coding
- [ ] Prerequisites are noted with Warning component
- [ ] No assumptions about prior knowledge without links
- [ ] Tables used for quick reference information
- [ ] ASCII diagrams for visual concepts

### Language Quality
- [ ] Description starts with "Learn" or "Understand" (not "Master")
- [ ] No overuse of em dashes (fewer than 15 outside Key Takeaways and structured sections)
- [ ] No AI superlatives: "dramatically", "fundamentally", "incredibly", "extremely"
- [ ] No stiff phrases: "one of the most important", "essential points", "It should be noted"
- [ ] Emphasis patterns vary (not all "Key insight:" or "Best practice:")
- [ ] Playful touches are sparse (1-2 per major section maximum)
- [ ] No filler words: "basically", "essentially", "actually", "very", "really"
- [ ] Sentences are direct (no "In order to", "Due to the fact that")

### Resource Quality
- [ ] All article/video links are verified working
- [ ] All resources are JavaScript-focused (no C#, Python, Java resources)
- [ ] Each resource has a specific 2-sentence description (not generic)
- [ ] Resource descriptions explain what makes each unique
- [ ] No outdated resources (check dates for time-sensitive topics)
- [ ] 4-6 articles from reputable sources
- [ ] 3-4 videos from quality creators

---

## Writing Tests

When adding code examples, create corresponding tests in `/tests/`:

```javascript
// tests/{category}/{concept-name}/{concept-name}.test.js
import { describe, it, expect } from 'vitest'

describe('Concept Name', () => {
  describe('Basic Examples', () => {
    it('should demonstrate the core concept', () => {
      // Convert console.log examples to expect assertions
      expect(typeof "hello").toBe("string")
    })
  })
  
  describe('Common Mistakes', () => {
    it('should show the wrong behavior', () => {
      // Test the "wrong" example to prove it's actually wrong
    })
    
    it('should show the correct behavior', () => {
      // Test the "correct" example
    })
  })
})
```

---

## SEO Checklist

Verify these elements before publishing any concept page:

### Title & Meta Description
- [ ] **Title is 50-60 characters** — check with character counter
- [ ] **Title ends with "in JavaScript"** — SEO keyword at end
- [ ] **Title has a compelling hook** — tells reader what they'll understand
- [ ] **sidebarTitle matches title but without "in JavaScript"** — cleaner navigation
- [ ] **Description is 150-160 characters** — don't leave value on the table
- [ ] **Description includes primary keyword** in first sentence
- [ ] **Description includes 1-2 secondary keywords** naturally
- [ ] **Description starts with action word** (Learn, Understand, Discover — avoid "Master")
- [ ] **Description promises specific value** — what will they learn?

### Keyword Placement
- [ ] **Primary keyword in title**
- [ ] **Primary keyword in description**
- [ ] **Primary keyword in first paragraph** (within first 100 words)
- [ ] **Primary keyword in at least one H2 heading**
- [ ] **Secondary keywords in H2/H3 headings** where natural
- [ ] **Keywords in "What you'll learn" box items**
- [ ] **No keyword stuffing** — content reads naturally

### Content Structure
- [ ] **Opens with question hook** matching search intent
- [ ] **Shows code example in first 200 words**
- [ ] **First paragraph after H2s directly answers** the implied question
- [ ] **Content is 1,500+ words** (comprehensive coverage)
- [ ] **Short paragraphs** (2-4 sentences maximum)
- [ ] **Uses bullet lists** for 3+ related items
- [ ] **Uses numbered lists** for sequential processes
- [ ] **Uses tables** for comparisons and reference data
- [ ] **Key terms bolded** on first mention with MDN links

### Featured Snippet Optimization
- [ ] **"What is X" section has 40-60 word definition paragraph**
- [ ] **"How to" sections use numbered steps or `<Steps>` component**
- [ ] **Comparison sections use tables** with clear headers
- [ ] **At least one H2 is phrased as a question** matching search query

### Internal Linking
- [ ] **Links to 3-5 related concept pages** in body content
- [ ] **Uses descriptive anchor text** (not "click here" or "here")
- [ ] **Prerequisites linked in Warning component** at start
- [ ] **Related Concepts section has 4 cards** with relevant concepts
- [ ] **Links appear in natural context** — not forced

### Technical SEO
- [ ] **Slug is lowercase with hyphens**
- [ ] **Slug contains primary keyword**
- [ ] **Slug is 3-5 words maximum**
- [ ] **All external links use proper URLs** (no broken links)
- [ ] **MDN links are current** (check they resolve)
