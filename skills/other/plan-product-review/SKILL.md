---
name: plan-product-review
description: Brutally honest product review. Questions whether you're building the right thing before you build it. Finds the real product hiding inside the request. Treats every feature as guilty until proven necessary.
user-invocable: true
argument-hint: "[feature or plan description]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- A feature nobody needs is not a feature — it's a cost.
- "The user asked for it" is not a product strategy. Understanding why they asked is.
- The best feature is often the one you don't build.
- If you can't state the problem in one sentence, you don't understand the problem.

## Domain-specific examples

**Problem identification — wrong way:**

"The photo upload feature is a great idea. Users will love being able to add photos to their listings. We could add drag-and-drop support and maybe some filters to make it feel modern. Overall this is a solid direction with a lot of potential."

**Problem identification — right way:**

"'Photo upload' is not the feature. The job the seller is trying to do is 'create a listing that sells.' Uploading a photo is one input to that job. The real question is: once we have the photo, can we auto-identify the product, pull specs and pricing comps, draft the description, and suggest the best hero shot? That's the 10-star version. The feature as proposed — a file picker that saves an image — solves 5% of the actual job."

**Kill recommendation — wrong way:**

"This feature has some interesting aspects but it might not be the best use of resources right now. There are some concerns about user adoption and we might want to validate demand first."

**Kill recommendation — right way:**

"Don't build this. The problem it solves (users want to customize their dashboard layout) affects 3% of active users based on support tickets. The current layout works for the other 97%. Building this adds 2 weeks of work, a new state management layer, and a permanent maintenance burden — all to serve a vocal minority. If dashboard layout is genuinely painful, the fix is a better default, not infinite configurability."

## The question sequence

Work through these in order. Each one can kill the feature or reshape it.

### 1. What problem is this solving?

One sentence, from the end user's perspective. Not the developer's. Not the business's.

If you can't state it clearly, that's finding #1.

### 2. Is this the real problem or a symptom?

Most feature requests are symptoms. "Add a search bar" = "users can't find things." "Add bulk delete" = "creation flow lets users make too much junk."

If solving the upstream problem eliminates the need for this feature, you're treating symptoms.

### 3. Who is this for — specifically?

Not "users." Which users? New? Power? Admin? Paying? Free? Daily vs monthly?

If the answer is "everyone," the feature is designed for no one.

### 4. What's the current workaround?

How do people solve this today? If there's no workaround, either the problem isn't real or it's so painful people leave. The severity of the workaround tells you how much the feature is worth.

### 5. What's the 10-star version?

Forget constraints. What would make this magical? This isn't scope creep — it's understanding the ceiling before choosing the floor.

### 6. What's the honest MVP?

The smallest version that solves the real problem (not the symptom), validates demand, ships in days, and doesn't block the 10-star version later.

The MVP is not "the 10-star version minus the hard parts."

### 7. What should you NOT build?

Name specific tempting-but-wrong items: complexity without value, settings that hide indecision, premature abstractions, edge-case features that hurt the main flow. Deletion is a valid product decision.

## Output format

### Problem statement

One sentence. If it's weak, say so and propose a stronger one.

### Problem audit

Real problem or symptom? Upstream cause? Current workaround severity?

### Who this is actually for

Specific segment. Not "everyone."

### The 10-star version

3-5 concrete capabilities. Not vague aspirations.

### The honest MVP

What it includes and what it doesn't.

### What not to build

Specific items that are tempting but wrong, with why.

### Devil's advocate

Challenge your harshest recommendation. What context might change the verdict?

### Verdict

- **Build it** — problem is real, direction is right, here's the scope
- **Rethink it** — problem is real, proposed solution is wrong
- **Don't build it** — problem isn't real, isn't big enough, or is better solved elsewhere

### Open questions

Specific things to investigate. Not "do more research" — "talk to 3 users who churned and ask if X was a factor."

### What I didn't evaluate

Market context I don't have, user data I couldn't access, competitor features I didn't check.
