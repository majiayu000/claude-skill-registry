---
name: product-led-onboarding-design
description: Design a self-serve onboarding flow that enables users to reach "Day Zero" value without a salesperson or manual training. Use this skill when launching a bottoms-up product, diagnostic work for low activation rates, or transitioning from white-glove to self-serve motions.
---

# Product-Led Onboarding Design

Product-led onboarding is not a "plug-and-play" veneer; it is a native experience where the product teaches the user how to use the product through action. This framework applies game design principles to help users clear the "fog of war" and reach immediate value.

## Core Principles

### 1. Identify "Day Zero" Value
Onboarding must provide value in the first session. If the product requires months of data or long-term transcripts to be useful, it is likely not a product-led candidate.
- **Criteria**: Can an individual (IC) use this without "the keys to the Porsche" (HR-level PII access or executive buy-in)?
- **Target**: Find the "Atomic Unit" of value (e.g., sending the first message, creating the first task).

### 2. The "Product as Teacher" Model
Avoid carousels and instructional overlays that users instinctively dismiss. Instead, use the core mechanics of the product to onboard.
- **Example**: In a to-do list app, the first task in the list should be "Click the square next to this task to mark it as complete."
- **Avoid**: "Magic Wand" solutions—don't assume users will have an NLP-driven conversation with a bot to set up their workspace. Keep it grounded in the actual UI.

### 3. Clear the "Fog of War"
Treat the user's first experience like a game map. 
- Start with a constrained view of the product.
- Reveal features as the user completes foundational steps.
- Ensure someone is there to "greet" them (e.g., in a collaboration tool, push notifications to get teammates online simultaneously are a high-leverage trigger).

## Implementation Workflow

### Step 1: Friction Audit
Map every step between the user's signup and their "Aha!" moment.
- Identify "Dad’s Porsche" blockers: Does the user need an API key they don't have? Do they need to ask a boss for permission?
- Remove "Information Panes": Delete any carousel that isn't native to the product's core modality.

### Step 2: Determine Activation Benchmarks
Use regression analysis to find the "Activation" tipping point, but keep the numbers small.
- **Slack's Benchmark**: 3 people (real humans, not bots) and 50 messages.
- **Goal**: Find the lowest number where the product dynamics "break" or become necessary (e.g., email works fine for 1:1, but breaks at 3+ people).

### Step 3: Design "Social" Triggers
For collaboration products, the first user's job is to invite others. 
- **Include Invites Early and Often**: Even if user research says "I wouldn't invite someone yet," provide the option. Social "connectors" will use it immediately.
- **Synchronicity**: Build triggers (like mobile push notifications) that encourage teammates to join the app at the exact same time to minimize "empty room" syndrome.

### Step 4: Validate via "Embarrassing" Research
Stop looking at anonymized data piles and watch real humans.
- **Frequency**: Once a month, recruit users from your target demographic.
- **The Test**: Watch them sign up without saying a word. Observe where they hesitate, where they look annoyed, and which "instructional" text they skip.

## Examples

**Example 1: B2B Messaging Tool**
- **Context**: Low day-one retention in a new team communication app.
- **Application**: Instead of a "Welcome" video, the app opens to a single channel with a prompt: "Type @teammate to see if they're online."
- **Outcome**: The user experiences the core "sync" value immediately, reaching the 3-person/50-message threshold faster.

**Example 2: Data Visualization Dashboard**
- **Context**: Users sign up but never connect a data source.
- **Application**: Provide a "Play with Sample Data" button on the first screen. Let the user build a chart using the sample data *before* asking them to connect their sensitive production database.
- **Outcome**: The user learns the UI value ("I can make charts easily") before facing the high-friction task of data integration.

## Common Pitfalls

- **Copying the "Throbbers"**: Don't copy UI elements from competitors (like Slack's old animated onboarding circles) just because they exist. Often, the company you're copying knows those features aren't working and is planning to delete them.
- **Overestimating Investment**: Users do not care about your product as much as you do. If your onboarding requires reading more than one sentence at a time, it’s too complex.
- **The Carousel Trap**: If you are using a carousel to explain "7 power features," you have failed to make the product intuitive. If the carousel is built to be dismissed, it shouldn't exist.
- **Ignoring the Persona**: Forcing a "non-social" user to invite 10 people to proceed is a dark pattern. Make invitations available for "connectors" but skippable for others.