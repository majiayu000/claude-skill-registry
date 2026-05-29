---
name: book-ideation
description: Develop raw book ideas into structured nonfiction book concepts. Use when the user wants to develop a book idea, has brainstorm documents to refine into a book concept, wants to articulate a book's thesis/promise/reader/transformation, or needs to prepare a book concept for validation and market research. Nonfiction only. Produces a Book Concept Document with all elements needed for downstream skills (idea-validator, market-research, book-architect).
---

# Book Ideation

Transform raw ideas into structured nonfiction book concepts through guided multi-session development.

## Core Philosophy

**Every decision serves the reader.** The question is never "what do I want to say?" but "what transformation does the reader need, and how can this book deliver it?"

This skill sits between generic brainstorming and book architecture. Its job is to refine raw material into a structured concept that can be validated, market-tested, and architected.

**The goal is not a book outline.** The goal is clarity on eight fundamental elements that determine whether a book should exist and what it must accomplish.

## Input Types

This skill accepts:

- Raw idea (one sentence or paragraph)
- Brainstorm document from the `brainstorm` skill
- Zettelkasten notes or research collection
- Existing partial concept needing refinement
- "Shower thought" worth exploring

## Session Flow

### Session Start

Begin every session with:

1. **New or continuing?**
   - If continuing: Request the latest Book Concept Document version
   - If new: Proceed to initialization

2. **What do we have?**
   - Ask user to share their raw material (brainstorm doc, notes, idea)
   - Read and identify what's already clear vs. underdeveloped

3. **Session goal**
   - Which elements need development today?
   - Deep exploration or quick progress?

### The Eight Elements

Develop these through conversation, not interrogation. Surface insights; don't extract data.

#### 1. The Reader

_Who specifically is this for?_

Go beyond demographics. Understand:

- Their current situation (what's happening in their life/work)
- What they currently believe that isn't serving them
- What they've already tried that hasn't worked
- What's blocking them from solving this themselves
- Why they would pick up THIS book (the trigger moment)

**Probe:** "If your ideal reader walked into a bookstore, what section would they be in? What would they be feeling? What search would they have just done on Amazon?"

#### 2. The Transformation

_Where will they be after reading?_

The reader starts at Point A and ends at Point B. Define both clearly:

- What will they believe differently?
- What will they be able to do?
- How will they feel?
- What will they stop doing?

**The gap between A and B is the book's reason for existence.**

#### 3. The Core Thesis

_What's the one big idea?_

This is not a topic—it's a claim. A thesis takes a position. Test it:

- Can someone disagree with this? (If not, it's too obvious)
- Does it challenge conventional wisdom? (Contrarian theses are more compelling)
- Can you state it in one sentence?

**Template:** "Most people believe [conventional wisdom], but actually [your thesis], because [key insight]."

#### 4. The Author Angle

_Why are you the one to write this?_

Credibility comes from:

- Experience (you've lived this)
- Expertise (you've studied/practiced this)
- Access (you have information others don't)
- Perspective (you see what others miss)

**You don't need all four. You need at least one that's compelling.**

#### 5. The Stakes

_Why does this matter? Why now?_

Articulate:

- What's the cost of NOT reading this book?
- Why is this moment in time right for this message?
- What's at risk for the reader if they continue as they are?

Stakes create urgency. Without stakes, the book is a "nice to have."

#### 6. The Key Concepts

_What are the 3-7 major ideas that support the thesis?_

These are the building blocks—the frameworks, principles, stories, or insights that make the thesis credible and actionable. They'll become chapters or sections.

Don't list 20 ideas. Force prioritization. What's essential vs. nice-to-have?

#### 7. The Enemy

_What is this book arguing against?_

Every great nonfiction book has a villain:

- A mindset ("hustle culture")
- A practice ("inbox zero")
- Conventional wisdom ("more information = better decisions")
- A competing approach ("digital note-taking")

**The enemy clarifies the thesis by contrast.**

#### 8. The Promise

_In one sentence, what does the reader get?_

This is the book's value proposition. It should:

- Be specific (not "improve your life")
- Be believable (not "become a millionaire in 30 days")
- Connect transformation to method

**Template:** "This book will help [reader] achieve [transformation] by [method/insight]."

### During Session

**Collaboration behaviors:**

- Surface what's implicit: "It sounds like you're really saying..."
- Challenge weak elements: "I'm not convinced this thesis is contrarian enough. Here's why..."
- Connect elements: "Your enemy suggests your reader might be someone who..."
- Push for specificity: "Can you give me an example of this reader?"

**When stuck on an element:**

- Skip it and return later (other elements may clarify it)
- Use the "Ideal Reader Interview" technique (imagine interviewing your reader)
- Try the "Anti-Book" technique (what's the opposite book? who's it for?)

### Session End

Always conclude with:

1. **Element status** — Which elements are solid, developing, or still raw?
2. **Key insight** — What did we discover this session?
3. **Overnight question** — What should the user sit with?
4. **Version creation** — Generate the next version of the Book Concept Document

## Quick Capture Mode

For rapid concept capture when time is short:

1. User shares raw idea
2. Extract: Reader (rough), Transformation (rough), Thesis (rough), Promise (one sentence)
3. Create minimal v1 document
4. Note: "Quick capture—expand in future session"

## Readiness Criteria

A Book Concept Document is ready for validation when:

| Element        | Readiness Test                                             |
| -------------- | ---------------------------------------------------------- |
| Reader         | Can describe them as a specific person, not a category     |
| Transformation | Clear before/after with emotional and practical dimensions |
| Thesis         | One sentence, contrarian, defensible                       |
| Author Angle   | At least one compelling credibility source                 |
| Stakes         | Urgency is clear—reader feels cost of inaction             |
| Key Concepts   | 3-7 prioritized, each clearly supporting the thesis        |
| Enemy          | Named and specific                                         |
| Promise        | One sentence that a reader would find compelling           |

## Output

Use the template at `assets/templates/book-concept-template.md` for all Book Concept Documents.

The document is versioned (v1, v2, etc.) and includes:

- All eight elements with current development status
- Session log tracking progress
- Open questions for future sessions
- Readiness assessment for downstream skills

## Structural Frameworks Reference

When discussing Key Concepts, it often helps to preview potential book structures. See `references/nonfiction-frameworks.md` for framework options to share with the user. This is for orientation only—structural decisions belong to `book-architect`.

## Handoff to Downstream Skills

When the Book Concept Document is ready:

→ **idea-validator**: Will stress-test the thesis and key concepts against existing research
→ **market-research**: Will assess KDP viability, competition, and positioning
→ **book-architect**: Will use reader/transformation/key concepts to design the structure
