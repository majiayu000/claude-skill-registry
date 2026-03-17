---
name: jobs-to-be-done
description: "Understand why customers really buy by uncovering the \"job\" they're hiring your product to do Use when: **Understanding customer motivation** beyond demographics and feature requests; **Finding product-market fit** by identifying the real progress customers seek; **Discovering why customers switch** (or don't) between solutions; **Identifying true competition** that isn't obvious from industry categories; **Creating marketing messages** that resonate with real customer struggles"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Jobs to Be Done - Customer Motivation Framework

> Understand why customers really buy by uncovering the "job" they're hiring your product to do

## When to Use This Skill

- **Understanding customer motivation** beyond demographics and feature requests
- **Finding product-market fit** by identifying the real progress customers seek
- **Discovering why customers switch** (or don't) between solutions
- **Identifying true competition** that isn't obvious from industry categories
- **Creating marketing messages** that resonate with real customer struggles
- **Prioritizing features** based on unmet customer needs
- **Conducting customer research** that reveals actionable insights

## Methodology Foundation

| Aspect | Details |
|--------|---------|
| **Source** | Competing Against Luck (2016), The Innovator's Solution (2003) |
| **Expert** | Clayton Christensen (Harvard Business School), Tony Ulwick (Strategyn) |
| **Core Principle** | "People don't buy products; they hire them to get jobs done. Understanding the job—not the customer or the product—is the key to predictable innovation." |


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

This skill helps you shift from asking "Who is my customer?" to asking "What job is my customer trying to get done?"

The result is a fundamentally different understanding of why people buy:

1. **Uncover the real job** - The progress customers are trying to make in their lives
2. **See all three dimensions** - Functional, emotional, and social needs
3. **Understand the forces** - What pushes people to change and what holds them back
4. **Map the job** - Break it down into steps where you can add value
5. **Identify true competition** - Everyone solving the same job, regardless of category

This transforms feature-driven product development into progress-driven innovation.

## How to Use

### Prompt Examples

```
Help me identify the Job to Be Done for customers who buy [product/service].
Use the Christensen JTBD framework. Consider functional, emotional, and social dimensions.
```

```
I'm seeing customers use my product for [unexpected purpose]. Help me understand
what job they might be hiring it for using JTBD analysis.
```

```
Create a Job Map for [specific customer goal]. Break it into the 8 universal steps
and identify where customers might struggle most.
```

```
Analyze the forces of progress for someone switching from [current solution] to [my product].
What's pushing them, pulling them, causing anxiety, and creating habit inertia?
```

```
Write Job Stories (not user stories) for my [product]. Focus on situation,
motivation, and expected outcome rather than user type and action.
```

## Instructions

### The Core Framework

```
┌─────────────────────────────────────────────────────────────┐
│                  JOBS TO BE DONE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  "When [CIRCUMSTANCE], I want to [JOB], so I can [OUTCOME]" │
│                                                             │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐             │
│  │FUNCTIONAL │ + │ EMOTIONAL │ + │  SOCIAL   │             │
│  │    JOB    │   │    JOB    │   │    JOB    │             │
│  └───────────┘   └───────────┘   └───────────┘             │
│                                                             │
│  What they're    How they want   How they want              │
│  trying to DO    to FEEL         to be SEEN                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Step 1: Understand the Three Dimensions

Every job has three dimensions. Products that address all three are far more likely to be "hired."

| Dimension | Question | Example (Fitness App) |
|-----------|----------|-----------------------|
| **Functional** | What are they trying to accomplish? | Get exercise guidance and track workouts |
| **Emotional** | How do they want to feel? | Feel confident, accomplished, in control of health |
| **Social** | How do they want to be perceived? | Be seen as fit, disciplined, health-conscious |

**Key Insight**: Many products fail because they nail the functional job but ignore the emotional and social dimensions.

**Exercise**: For your product, fill in:
- "Customers hire us to **DO** _______________"
- "Customers hire us to **FEEL** _______________"
- "Customers hire us to **BE SEEN AS** _______________"

---

### Step 2: Identify the Forces of Progress

Four forces determine whether a customer will "switch" to your solution:

```
                    ┌─────────────┐
                    │    PUSH     │
                    │ Problems    │
                    │ with status │
                    │    quo      │
                    └──────┬──────┘
                           ↓
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   HABIT     │←────│   CUSTOMER   │────→│    PULL     │
│  Comfort    │     │   DECISION   │     │ Attraction  │
│  with old   │     └──────────────┘     │   of new    │
│   way       │                          │  solution   │
└─────────────┘            ↑              └─────────────┘
                    ┌──────┴──────┐
                    │   ANXIETY   │
                    │   Fear of   │
                    │   change    │
                    └─────────────┘
```

**Switch happens when**: Push + Pull > Habit + Anxiety

| Force | What to Ask | Example |
|-------|-------------|---------|
| **Push** | What's frustrating about their current situation? | "I keep losing track of my workouts in notebooks" |
| **Pull** | What's appealing about the new solution? | "The app shows my progress visually" |
| **Anxiety** | What fears do they have about changing? | "What if I can't figure out how to use it?" |
| **Habit** | What's comfortable about the status quo? | "I've always used notebooks, it's familiar" |

**Tactical Application**:
- **Increase Push**: Help customers see the true cost of their current solution
- **Increase Pull**: Demonstrate the progress they can make
- **Reduce Anxiety**: Provide guarantees, trials, social proof
- **Reduce Habit**: Make switching easy, offer migration tools

---

### Step 3: Map the Job

Break down any job into the universal 8-step Job Map:

| Step | Description | Questions to Ask |
|------|-------------|------------------|
| **1. Define** | Determine goals and plan | "What are you trying to accomplish?" |
| **2. Locate** | Gather inputs needed | "What do you need to get started?" |
| **3. Prepare** | Set up and organize | "How do you get ready?" |
| **4. Confirm** | Verify readiness | "How do you know you're ready?" |
| **5. Execute** | Perform the core job | "What are the key steps?" |
| **6. Monitor** | Check progress | "How do you know it's working?" |
| **7. Modify** | Make adjustments | "What do you change if needed?" |
| **8. Conclude** | Wrap up and clean up | "How do you finish up?" |

**Example: Job = "Prepare a nutritious dinner on a busy weeknight"**

| Step | Activity | Struggle Points |
|------|----------|-----------------|
| Define | Decide what to make | Too many options, dietary restrictions |
| Locate | Get ingredients | Missing items, trip to store |
| Prepare | Prep ingredients | Takes too long, messy |
| Confirm | Check recipe | Confusing instructions |
| Execute | Cook the meal | Timing multiple dishes |
| Monitor | Watch for doneness | Burning, undercooking |
| Modify | Adjust seasoning | Unsure how to fix mistakes |
| Conclude | Serve and clean | Pile of dishes |

**Innovation Opportunity**: Each struggle point is an opportunity to create value.

---

### Step 4: Discover Desired Outcomes

For each job step, identify what customers use to measure success:

**Format**: [Direction] + [Metric] + [Object]

**Examples**:
- "**Minimize** the **time** it takes to **find ingredients**"
- "**Minimize** the **likelihood** of **burning the food**"
- "**Increase** the **confidence** that **family will enjoy it**"
- "**Minimize** the **effort** required to **clean up**"

**Quantify Importance & Satisfaction**:
Survey customers on:
1. How important is this outcome? (1-10)
2. How satisfied are you with current solutions? (1-10)

**Opportunity Score** = Importance + (Importance - Satisfaction)

High opportunity = High importance, Low satisfaction

---

### Step 5: Redefine Your Competition

JTBD reveals that competition extends far beyond your industry.

**Traditional View**: Same product category
**JTBD View**: All solutions hired for the same job

**Example: Job = "Feel energized in the morning"**

| Solution | Category | Same Job? |
|----------|----------|-----------|
| Coffee | Beverage | ✓ |
| Energy drink | Beverage | ✓ |
| Morning jog | Fitness | ✓ |
| Cold shower | Personal care | ✓ |
| Meditation app | Wellness | ✓ |
| Upbeat playlist | Entertainment | ✓ |

**Strategic Implication**: You're not competing with similar products. You're competing with every way customers currently get the job done.

---

### Step 6: Write Job Stories

Replace user stories with Job Stories for better product decisions.

**User Story (Traditional)**:
> "As a [user type], I want [action], so that [benefit]."

**Job Story (JTBD)**:
> "When [situation/context], I want to [motivation], so I can [expected outcome]."

**Comparison**:

| User Story | Job Story |
|------------|-----------|
| "As a busy parent, I want a quick meal option" | "When I get home exhausted from work and the kids are hungry NOW, I want to put something nutritious on the table in under 20 minutes, so I can feed my family without guilt or stress" |
| "As a fitness enthusiast, I want to track workouts" | "When I finish a workout and want to see my progress, I want to quickly log what I did, so I can feel accomplished and know I'm improving" |

**Job Stories capture**:
- **Circumstance** (the trigger)
- **Motivation** (the real goal)
- **Outcome** (the definition of success)

---

## Examples

### Example 1: The Milkshake Story (Classic)

**Situation**: Fast-food chain wants to improve milkshake sales. Traditional research (focus groups, demographics) fails.

**JTBD Analysis**:

**Morning Customers (Commuters)**:
- **Job**: Make the boring commute more interesting and stay full until lunch
- **Functional**: One-hand consumption, filling, lasts the whole drive
- **Emotional**: Feel satisfied, not bored
- **Social**: N/A (alone in car)
- **Competition**: Bananas, bagels, donuts

**Afternoon Customers (Parents)**:
- **Job**: Be a good parent by treating the kids
- **Functional**: Quick, manageable for children
- **Emotional**: Feel like a caring parent
- **Social**: Be seen as fun/generous by the child
- **Competition**: Ice cream, candy, toys

**Implications**:
- Morning: Make it thicker (lasts longer), add texture (interest), self-serve kiosk (faster)
- Afternoon: Smaller size, quicker to consume, kid-friendly packaging

---

### Example 2: SaaS Product Discovery

**Situation**: A project management tool sees unexpected adoption by freelancers.

**JTBD Interview Findings**:

**The Job**: "Appear professional and organized to clients"

**Forces**:
- **Push**: "I was embarrassed when I lost a client email and missed a deadline"
- **Pull**: "This makes me look like I have my act together"
- **Anxiety**: "What if it's overkill? What if I can't figure it out?"
- **Habit**: "I've always just used sticky notes and Gmail"

**Three Dimensions**:
- **Functional**: Keep track of tasks and deadlines
- **Emotional**: Feel in control, confident
- **Social**: Appear professional, reliable to clients

**Job Stories**:
1. "When a client sends multiple emails about different projects, I want to quickly organize everything by project, so I can respond promptly without missing anything."

2. "When I'm on a call with a client asking for a status update, I want to instantly see where everything stands, so I can sound professional and knowledgeable."

**Product Decisions Based on This**:
- Add "client view" so freelancers can share professional-looking status updates
- Create quick-capture feature for emails
- Build "instant status" dashboard for calls

---

## Checklists & Templates

### JTBD Discovery Interview Guide

```markdown
## JTBD Interview for: [Product/Service]

### Opening
"I'd like to understand the story of how you came to use [product].
Walk me through what was happening in your life when you first started looking."

### Timeline Questions
1. "When did you first realize you needed something like this?"
2. "What was happening in your life at that moment?"
3. "What did you try first? How did that work out?"
4. "When did you first hear about [our product]?"
5. "What almost stopped you from trying it?"
6. "What was the moment you decided to actually use it?"
7. "What did you have to give up or change?"

### Forces Questions
**Push**: "What was frustrating about how you were doing it before?"
**Pull**: "What about [product] was appealing?"
**Anxiety**: "What were you worried about?"
**Habit**: "What was hard about changing?"

### Outcome Questions
"If [product] worked perfectly, what would be different in your life?"
"How do you know when you've succeeded at [the job]?"

### Wrap-Up
"If [product] disappeared tomorrow, what would you do instead?"
```

### Job Analysis Template

```markdown
## Job Analysis: [Customer Segment]

### The Job (One Sentence)
"Help me _________________ so I can _________________"

### Three Dimensions
| Dimension | The Job | Evidence |
|-----------|---------|----------|
| Functional | | |
| Emotional | | |
| Social | | |

### Forces of Progress
| Force | Description | Strength (H/M/L) |
|-------|-------------|------------------|
| Push | | |
| Pull | | |
| Anxiety | | |
| Habit | | |

### Job Map
| Step | What They Do | Struggle Points | Desired Outcomes |
|------|--------------|-----------------|------------------|
| Define | | | |
| Locate | | | |
| Prepare | | | |
| Confirm | | | |
| Execute | | | |
| Monitor | | | |
| Modify | | | |
| Conclude | | | |

### Competition (All Solutions for This Job)
1. [Solution] - How it gets the job done
2. [Solution] - How it gets the job done
3. [Solution] - How it gets the job done

### Key Insights
1.
2.
3.

### Opportunities
1.
2.
3.
```

### Job Story Template

```markdown
## Job Stories for: [Feature/Product]

### Job Story 1
**When** [situation/trigger]:

**I want to** [motivation]:

**So I can** [expected outcome]:

### Job Story 2
**When** [situation/trigger]:

**I want to** [motivation]:

**So I can** [expected outcome]:

### Job Story 3
**When** [situation/trigger]:

**I want to** [motivation]:

**So I can** [expected outcome]:

### Notes
- Key circumstance details:
- Emotional state:
- Social context:
```

---

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- **Books**: Competing Against Luck (Christensen), Jobs to be Done: Theory to Practice (Ulwick)
- **Institute**: Christensen Institute for Disruptive Innovation
- **Framework**: Outcome-Driven Innovation (Strategyn)
- **Source**: `sources/books/christensen-jobs-to-be-done.md`

## Related Skills

- **positioning-dunford** - Position your product for the job it does best
- **category-design** - Create categories around jobs that need solving
- **buyer-personas** - Complement JTBD with who has these jobs
- **grand-slam-offers** - Design offers that address the full job
- **conversion-copywriting** - Use job language in your copy
