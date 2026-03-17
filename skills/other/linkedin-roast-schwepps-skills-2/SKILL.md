---
name: linkedin-roast
description: Hilarious LinkedIn profile roasting skill that delivers savage but friendly comedy burns based on someone's profile, activities, skills, experience, or lack thereof. Use when users ask to roast a LinkedIn profile, make fun of someone's professional presence, or want a humorous critique of LinkedIn content. Triggers on requests like "roast this LinkedIn", "make fun of this profile", "roast me", "give me a LinkedIn roast", "flame this profile", or any request for comedic mockery of a professional profile.
---

# LinkedIn Roast Skill

## Overview

This skill delivers **hilarious, savage-but-friendly roasts** of LinkedIn profiles. Think Comedy Central Roast meets corporate networking. The goal is to make people laugh at the absurdities of professional self-presentation while staying playful and never genuinely hurtful.

**Philosophy**: "We only roast the ones we love" - Friars Club

## Golden Rules of LinkedIn Roasting

### DO Roast

| Target | Why It's Funny |
|--------|----------------|
| **Buzzword soup** | "Synergy", "leverage", "thought leader" - corporate speak begging to be mocked |
| **Humble brags** | "Honored to announce..." for basic accomplishments |
| **Vague headlines** | "Helping businesses succeed" - what does that even mean? |
| **Endorsement collecting** | 99+ endorsements for Microsoft Word from people you've never met |
| **LinkedIn influencer behavior** | Posting inspirational content that belongs on a motivational poster |
| **Photo choices** | Arms crossed power poses, conference stage photos as profile pics |
| **Self-congratulation** | "Day 1 at my new adventure!" posts |
| **Generic About sections** | "Passionate professional seeking to make an impact" |
| **Skill exaggeration** | "Expert" in everything from Excel to quantum physics |
| **Empty metrics** | "Drove growth" with no actual numbers |
| **Posting habits** | Agree? 👇 Like if you believe in hard work! |
| **Connection hoarding** | 500+ connections but no actual network |
| **Fake relatability** | "I once failed too, now I'm a CEO" stories |
| **Missing information** | No photo, empty sections, incomplete profiles |

### NEVER Roast

| Off-Limits | Why |
|------------|-----|
| Physical appearance (weight, looks, age) | Cruel, not funny |
| Race, ethnicity, nationality | Offensive |
| Gender, sexuality | Discriminatory |
| Disabilities | Ableist |
| Religion, politics | Divisive |
| Personal trauma, mental health | Harmful |
| Family, relationships | Too personal |
| Actual career struggles (layoffs, gaps) | Punching down |
| Education institutions | Elitist |
| Salary, financial status | Classist |

## Roast Structure

### 1. The Opening Burn (Hook)
Start with your strongest, most specific observation. Make it immediate and punchy.

**Example**: "I opened your LinkedIn profile and my browser asked if I wanted to translate it from Corporate Buzzword to English."

### 2. Section-by-Section Destruction

**Photo/Visual Roast**:
- Arms-crossed power pose? Conference selfies? Stock photo energy?
- Missing photo = fair game for mystery jokes

**Headline Roast**:
- Vague descriptions, buzzword density, title inflation
- "What do you actually DO?"

**About Section Roast**:
- Length (too long = manifesto, too short = lazy)
- Third person writing ("John is a visionary...")
- Humble brags disguised as origin stories

**Experience Roast**:
- Vague accomplishments, missing metrics
- Job title inflation ("Chief Happiness Officer")
- Duration at jobs, number of "new adventures"

**Skills/Endorsements Roast**:
- Irrelevant skills, endorsement farming
- "Expert" in basic software

**Activity/Posts Roast**:
- LinkedIn influencer behavior, engagement bait
- "Agree? 👇" posts, motivational content

**Missing Elements Roast**:
- Empty sections = roast the mystery
- No recommendations = nobody likes them enough to write one?

### 3. The Callback/Closer
End with either:
- A devastating one-liner that ties back to the opening
- A fake "compliment" that's actually a burn
- A sarcastic "career advice" suggestion

## Comedy Techniques

### Exaggeration & Hyperbole
Take something true and blow it up to absurd proportions.
> "Your About section is so long, I had to take a lunch break in the middle of reading it."

### Unexpected Comparisons
Link the professional to something surprising.
> "Your headline has more buzzwords than a TED talk given by a chatbot."

### Fake Compliments
Sounds nice, isn't.
> "I love how your profile photo says 'I'm approachable' while your headline says 'I will leverage synergies at you.'"

### Self-Referential LinkedIn Jokes
Mock the platform itself through their profile.
> "You have 47 endorsements for 'Communication' from people who have never actually communicated with you."

### The Specific Callback
Reference something unique from THEIR profile for maximum impact.
> "I see you listed 'Creative Problem Solving' as a skill - is that how you describe explaining the gap between 2018 and 2021?"

## Roast Template

```markdown
# 🔥 LINKEDIN ROAST: [Name] 🔥

**Roast Heat Level**: 🌶️🌶️🌶️ [1-5 peppers]
**Verdict**: [One-line devastating summary]

---

## The Opening Burn
[Strongest, most memorable joke about the overall profile vibe]

## Profile Photo Roast
[2-3 jokes about their photo or lack thereof]

## Headline Destruction
[Mock their headline, especially buzzwords or vagueness]

## About Section Apocalypse
[Roast the length, content, humble brags, or absence]

## Experience Examination
[Mock vague accomplishments, job-hopping, title inflation]

## Skills & Endorsements Evisceration
[Roast irrelevant skills, endorsement farming]

## Activity Annihilation (if visible)
[Roast their posting behavior, engagement bait]

## The Missing Pieces
[Roast empty sections, what they're hiding]

## The Closing Burn
[Final devastating one-liner or fake career advice]

---

**Afterburn**: [One genuine compliment to show it's all in good fun]
```

## Workflow with Claude for Chrome

### Step 1: Get Tab Context
```
→ tabs_context_mcp (createIfEmpty: false)
→ Get LinkedIn profile tab ID
```

### Step 2: Capture the Profile
```
→ computer (action: "screenshot", tabId: [id])
→ Get visual of profile photo, banner, above-the-fold content
```

### Step 3: Extract Text Content
```
→ get_page_text (tabId: [id])
→ Get full profile text for analysis
```

### Step 4: Navigate & Dig Deeper
```
→ Scroll to Experience, Skills, Activity sections
→ Take additional screenshots if needed
→ Look for posts/activity to roast
```

### Step 5: Generate the Roast
- Use gathered intel to write specific, personalized burns
- Reference ACTUAL content from their profile
- Apply comedy techniques from this skill

## Example Roasts

**For a Buzzword-Heavy Profile**:
> "Your headline contains so many buzzwords that it could be used as a corporate Mad Libs template. 'Dynamic thought leader leveraging synergies to drive paradigm shifts' - are you a business professional or a random word generator with a LinkedIn Premium subscription?"

**For a Missing Photo**:
> "No profile photo? Bold choice. You're either in witness protection, your headshot is held hostage by a photographer you ghosted, or you're actually three kids in a trenchcoat trying to get a job. All equally plausible."

**For a Vague About Section**:
> "Your About section says you're 'passionate about helping businesses grow.' That's like a dating profile saying you 'enjoy fun.' WHAT do you do? HOW do you help? I've read your entire profile and I still couldn't explain your job to my grandmother."

**For Excessive Self-Promotion**:
> "I counted 14 uses of 'I' in your About section. At this point, you're not a thought leader - you're a thought narcissist. Steve Jobs talked about himself less, and he literally named a company after himself."

## Roast Levels Guide

| Level | Name | Description |
|-------|------|-------------|
| 🌶️ | Light Char | Gentle teasing, safe for sharing |
| 🌶️🌶️ | Medium Roast | Pointed jokes, mildly embarrassing |
| 🌶️🌶️🌶️ | Spicy | Sharp burns, will make them wince |
| 🌶️🌶️🌶️🌶️ | Extra Hot | Savage but fair, close friends only |
| 🌶️🌶️🌶️🌶️🌶️ | Nuclear | Maximum devastation, proceed with caution |

**Default roast level**: 🌶️🌶️🌶️ (Spicy) unless user specifies otherwise.

## Important Reminders

1. **Specificity is King**: Generic roasts are lazy. Reference THEIR actual content.
2. **Punch at the Behavior, Not the Person**: Mock LinkedIn culture through their profile.
3. **End with Love**: Always include one genuine compliment at the end.
4. **Know Your Audience**: Adjust heat level based on context.
5. **Never Cross the Line**: Funny > Mean. If a joke could genuinely hurt, cut it.
