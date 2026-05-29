---
date: 2026-02-07
created: 2026-02-07
name: community-psychology
version: 1.0.0
description: "When the user wants to apply behavioral science, psychology, or mental models to community building. Also use when the user mentions 'community psychology,' 'behavioral science,' 'why people engage,' 'motivation,' 'belonging,' 'social dynamics,' 'group psychology,' or 'human behavior in communities.' This skill provides the scientific foundation that all other Tribalism skills build on."
tags:
  - community-psychology
  - skill
---

# Community Psychology

You are an expert in behavioral science, social psychology, and group dynamics applied to community building. Your goal is to help users understand the underlying human psychology that drives community engagement, belonging, and growth — and apply that understanding to build better communities.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the user's situation:
1. What community challenge are they facing? (engagement, retention, growth, culture)
2. What specific behavior do they want to encourage or discourage?
3. What have they tried that isn't working?

---

## How to Use This Skill

This is a **foundational skill.** Every other Tribalism skill implicitly draws on these principles. Use this skill when:

- You need to understand **why** something is or isn't working in a community
- You want to design an intervention grounded in behavioral science
- You're making a case to stakeholders about community investment
- You need the "why" behind a recommendation from another skill

## Quick Reference

| Challenge | Models to Apply |
|-----------|----------------|
| Members join but never engage | IKEA Effect, Activation Energy, BJ Fogg Behavior Model |
| Engagement drops over time | Variable Reward, Habit Loop, Hedonic Treadmill |
| Nobody creates content | Bystander Effect, Psychological Safety, 1% Rule |
| Community feels cliquey | Dunbar's Number, Weak Ties, In-Group/Out-Group |
| Members won't invite others | Social Proof, Identity Signaling, Network Effects |
| Toxic behavior persists | Broken Windows, Overton Window, Deindividuation |
| Paid community has high churn | Endowment Effect, Sunk Cost, Loss Aversion |
| Community feels lifeless | Social Facilitation, Mere Exposure, Reciprocity |
| Leaders burn out | Dunbar's Number, Diffusion of Responsibility, Volunteer's Dilemma |
| Growth stalls | Crossing the Chasm, Network Effects, Critical Mass |

---

## Belonging & Identity Models

### 1. Social Identity Theory (Tajfel & Turner, 1979)
People define themselves partly through group membership. When someone says "I'm a member of [community]," it becomes part of their identity.

**The psychology:** We categorize ourselves into in-groups and derive self-esteem from those groups. We favor in-group members and differentiate from out-groups.

**Community application:**
- Give your community a clear identity ("We are builders/operators/creators")
- Create visible markers of membership (badges, roles, titles, swag)
- Define what your community is NOT — exclusion sharpens identity
- Lenny Rachitsky's community thrives partly because members identify as "Lenny's Newsletter readers" — it's a professional identity signal

### 2. Maslow's Hierarchy of Needs
Belonging is the third level of human needs, after physiological and safety needs.

**The psychology:** People need to feel accepted and connected to a group before they can pursue esteem and self-actualization.

**Community application:**
- Before members can contribute (esteem), they need to feel they belong (safety/belonging)
- Onboarding must address safety first (will I be judged?) then belonging (am I welcome?)
- Status and recognition only work after belonging is established
- Figma's community succeeds because the design community already shares professional identity — belonging comes naturally

### 3. Dunbar's Number
Humans can maintain roughly 150 stable social relationships, with inner circles of ~5, ~15, and ~50.

**The psychology:** Our cognitive limits cap meaningful relationships. Beyond 150, people become strangers.

**Community application:**
- Communities >150 need sub-groups to maintain intimacy (channels, cohorts, pods)
- Your "campfire" model works because it respects Dunbar's limits
- Ambassador programs work because ambassadors each manage a Dunbar-sized group
- Slack communities fragment around 150-200 active members — design for this
- Discord servers use roles and channels to create sub-Dunbar groups within large communities

### 4. Sense of Community Theory (McMillan & Chavis, 1986)
Four elements create a sense of community: **membership**, **influence**, **integration/fulfillment of needs**, and **shared emotional connection**.

**The psychology:**
- Membership: Boundaries define who's in and who's out
- Influence: Members feel they matter to the group AND the group matters to them
- Integration: Members' needs are met through community participation
- Shared emotional connection: Shared history, events, and experiences

**Community application:**
- Membership: Application-based or invite-only communities score higher on belonging
- Influence: Feature requests, voting, and governance give members influence
- Integration: Programming must deliver tangible value (knowledge, connections, opportunities)
- Shared emotional connection: Inside jokes, rituals, and shared stories create this — you can't shortcut it

### 5. Common Knowledge Effect
People are more likely to discuss information that everyone already knows rather than unique information that only they possess.

**The psychology:** In groups, shared knowledge dominates discussion because it's easier and safer to discuss.

**Community application:**
- Deliberately prompt for unique knowledge: "What's something YOU know that most people in [field] don't?"
- Structured formats (AMAs, hot seats, show-and-tell) surface unique information
- Avoid discussion prompts that invite obvious answers

---

## Motivation & Engagement Models

### 6. Self-Determination Theory (Deci & Ryan, 1985)
Three innate psychological needs drive intrinsic motivation: **autonomy**, **competence**, and **relatedness**.

**The psychology:** When these three needs are met, people are intrinsically motivated. When they're undermined, motivation collapses — even if external rewards are present.

**Community application:**
- Autonomy: Let members choose how they participate (don't mandate activities)
- Competence: Create skill-building opportunities and visible progress markers
- Relatedness: Facilitate genuine relationships, not just transactions
- This is why gamification alone fails — badges without autonomy and relatedness feel hollow
- Stack Overflow works because it fulfills competence (reputation) and autonomy (answer what you want)

### 7. BJ Fogg Behavior Model
Behavior = Motivation × Ability × Prompt. All three must be present for action.

**The psychology:** Even highly motivated people won't act if it's too hard. Even easy actions don't happen without a trigger.

**Community application:**
- **Motivation:** Make participation meaningful (not "post because we need content")
- **Ability:** Reduce friction at every step (one-click reactions, pre-filled templates, mobile-friendly)
- **Prompt:** Notifications, @-mentions, scheduled reminders, email digests
- When engagement is low, diagnose which factor is missing: motivation, ability, or prompt?
- Discord's reaction system works because ability is extremely low (one click) and the prompt is seeing others' reactions

### 8. Variable Reward (Skinner, 1957)
Unpredictable rewards are more engaging than predictable ones.

**The psychology:** Slot machines, social media feeds, and email refreshing all exploit variable reward schedules. The unpredictability of "what will I find?" creates compulsive engagement.

**Community application:**
- Mix content types and formats so the feed is never monotonous
- Surprise recognition (unexpected shoutouts, random gifts to active members)
- Guest appearances, special events, and "drop" content create unpredictability
- Reddit's upvote system is a variable reward — you never know which comment will blow up
- Warning: Don't manufacture this cynically. Variable reward should come from genuine community dynamism, not manipulation

### 9. The Habit Loop (Duhigg, 2012)
Habits form through a loop: **Cue → Routine → Reward**.

**The psychology:** Habits become automatic when the cue-routine-reward cycle is repeated consistently.

**Community application:**
- Cue: "Every Monday morning, a new discussion thread drops"
- Routine: "I read and respond to the thread"
- Reward: "I get valuable insights and peer recognition"
- Consistent timing is essential — erratic programming prevents habit formation
- Industry data: Communities with consistent weekly rituals see 40-60% higher weekly retention than those without

### 10. Flow State (Csikszentmihalyi, 1990)
People are most engaged when challenge matches skill level.

**The psychology:** Too easy = boredom. Too hard = anxiety. The sweet spot is "flow" — complete absorption.

**Community application:**
- Progressive complexity: Start new members with easy wins (introduce yourself, react to a post), then increase challenge (share your work, give feedback, lead a discussion)
- This is why member progression systems work — they calibrate challenge to skill
- Hackathons create flow because the time pressure + creative challenge hits the sweet spot

### 11. IKEA Effect (Norton et al., 2012)
People value things more when they've invested effort in creating them.

**The psychology:** We overvalue our own creations relative to identical pre-made items.

**Community application:**
- Members who contribute to the community value it more than those who only consume
- Getting members to invest early (write an intro, answer a question, share a resource) increases retention
- Co-creation of community guidelines, events, and content increases ownership
- "Help us name this program" or "Vote on our next event topic" creates investment
- Wikipedia thrives on this — contributors defend and return to articles they've edited

### 12. Hedonic Treadmill
People quickly adapt to positive changes and return to baseline satisfaction.

**The psychology:** The excitement of a new thing fades. What was delightful becomes expected.

**Community application:**
- A community that relies on one value proposition will experience declining engagement
- Refresh programming every 6-12 weeks (new formats, new guests, new challenges)
- Introduce new layers of value as members progress (advanced channels, leadership opportunities, exclusive access)
- This is why "launch energy" always fades — it's not failure, it's adaptation

---

## Social Dynamics Models

### 13. Social Proof (Cialdini, 1984)
People follow the behavior of others, especially in uncertain situations.

**The psychology:** "If others are doing it, it must be correct." We look to others for cues on how to behave.

**Community application:**
- Show member count, active discussions, and testimonials to attract new members
- When someone posts an introduction and gets 10 welcome responses, new members see that's the norm
- Highlight engagement: "This week's discussion had 47 contributions from 23 members"
- Notion grew partly through community members sharing templates publicly — visible social proof of an active ecosystem
- Empty communities repel because they lack social proof — this is the "empty room problem"

### 14. The 1% Rule (Nielsen, 2006)
In most online communities: 1% create content, 9% contribute occasionally, 90% lurk.

**The psychology:** Most people are consumers, not creators. Creating content requires more effort and social risk.

**Community application:**
- Don't design for 100% participation — design for 1/9/90
- Make lurking valuable (curated content, accessible archives, search)
- Create ladders from lurking → reacting → commenting → posting → leading
- Lowering the barrier to contribute shifts the ratio (polls, reactions, one-line responses)
- GitHub Discussions has a contribution rate closer to 5-10% because the audience self-selects for technical engagement

### 15. Bystander Effect (Darley & Latané, 1968)
The more people present, the less likely any individual is to act.

**The psychology:** Responsibility diffuses across the group. "Someone else will do it."

**Community application:**
- Don't post open questions to large channels ("Does anyone want to...?") — ask specific people
- Tag members directly: "@name, you've dealt with this — any thoughts?"
- Small group formats (5-8 people) eliminate the bystander effect
- Assign clear roles: "This week's discussion host is @name"
- This is why large Slack channels go quiet — 500 people all assume someone else will answer

### 16. Reciprocity (Gouldner, 1960)
When someone does something for us, we feel compelled to return the favor.

**The psychology:** Reciprocity is one of the most powerful social forces. Gifts, help, and generosity create obligations.

**Community application:**
- Help new members first (answer questions, make introductions) — they'll reciprocate
- Community managers who give generously create a culture of reciprocity
- "Pay it forward" norms: "I got help here, so I'll help someone else"
- Surprise gifts to active members trigger reciprocity
- Open source communities run on reciprocity — contributors give code because they've received the project's value

### 17. Psychological Safety (Edmondson, 1999)
People participate more when they believe they won't be punished for mistakes, questions, or disagreement.

**The psychology:** In psychologically safe environments, people take interpersonal risks — sharing ideas, admitting mistakes, asking questions.

**Community application:**
- Celebrate vulnerability ("Thanks for sharing that — it takes courage")
- Never ridicule questions, even basic ones
- Leaders should model vulnerability first (share their failures, ask for help)
- Google's Project Aristotle found psychological safety was the #1 predictor of effective teams — same applies to communities
- "No stupid questions" channels work because they explicitly lower the social risk

### 18. Mere Exposure Effect (Zajonc, 1968)
People develop preference for things they're repeatedly exposed to.

**The psychology:** Familiarity breeds fondness. The more we see something, the more we like it.

**Community application:**
- Consistent presence builds trust (regular posts, always responding, showing up at events)
- Weekly email digests keep the community top-of-mind even for inactive members
- Members who see the same community name 5-10 times before joining have higher activation rates
- This is why multi-touch marketing works for community growth — the 4th mention converts

### 19. In-Group Favoritism / Out-Group Bias
People prefer members of their own group and view outsiders with suspicion.

**The psychology:** We give in-group members the benefit of the doubt and judge out-group members more harshly.

**Community application:**
- New members are "out-group" until they're accepted — onboarding must bridge this gap
- Shared language, rituals, and identity markers create in-group bonds
- Danger: Cliques form naturally. Design cross-group interactions (random pairings, cross-channel events)
- When communities have sub-groups (beginners/advanced, different use cases), in-group bias can create friction between them

### 20. Broken Windows Theory (Wilson & Kelling, 1982)
Visible signs of disorder encourage more disorder.

**The psychology:** If a building has broken windows, more windows get broken. Small violations signal that nobody cares.

**Community application:**
- Unanswered questions signal "nobody's home" — always respond
- Off-topic spam left unchecked invites more spam
- Low-effort posts that get no moderation lower the quality bar for everyone
- Respond to the first violation quickly — it sets the standard
- Well-maintained communities (active moderation, clean channels, current content) attract quality members

---

## Growth & Network Models

### 21. Network Effects (Metcalfe's Law)
The value of a network grows proportionally to the square of the number of connected users.

**The psychology:** Each new member adds value for all existing members. This creates exponential value growth.

**Community application:**
- Early communities must manually create value because network effects haven't kicked in
- Critical mass for network effects: typically 50-150 active members
- Two-sided network effects are strongest: content creators attract consumers, consumers attract creators
- LinkedIn's early growth strategy: invite everyone you know → network effects kick in → network becomes the moat

### 22. Crossing the Chasm (Moore, 1991)
New products (and communities) must cross the gap between early adopters and early majority.

**The psychology:** Early adopters tolerate rough edges. The early majority wants proven, polished experiences.

**Community application:**
- Founding members (innovators/early adopters) join for the potential
- To cross the chasm, you need: social proof, clear onboarding, consistent value, and reduced risk
- Communities stall at 200-500 members when they fail to cross the chasm
- Signal that you've crossed: new members say "I heard about this from multiple sources"

### 23. Critical Mass Theory
A community needs a minimum number of active participants before it becomes self-sustaining.

**The psychology:** Below critical mass, the community requires constant effort from organizers. Above it, members sustain engagement themselves.

**Community application:**
- Critical mass for most communities: 30-50 consistently active members (not total members — active ones)
- Before critical mass: seed every discussion, respond to every post, DM inactive members
- After critical mass: shift to facilitation and curation, members drive engagement
- Benchmark: When >50% of discussions are started by members (not staff), you've hit critical mass

### 24. Diffusion of Innovation (Rogers, 1962)
Adoption follows a predictable curve: Innovators (2.5%) → Early Adopters (13.5%) → Early Majority (34%) → Late Majority (34%) → Laggards (16%).

**The psychology:** Different people adopt for different reasons at different speeds.

**Community application:**
- Innovators and early adopters want access and influence — give them founding member status
- Early majority wants proven value — show testimonials and case studies
- Late majority wants safety — emphasize community size, notable members, established reputation
- Tailor your messaging to the adoption stage you're targeting

---

## Decision & Cognitive Models

### 25. Loss Aversion (Kahneman & Tversky, 1979)
Losses feel roughly 2x as painful as equivalent gains feel good.

**The psychology:** People are more motivated to avoid losing something than to gain something equivalent.

**Community application:**
- "Don't miss this week's discussion" > "Join this week's discussion"
- For paid communities: free trials create ownership, cancellation feels like loss
- Streak mechanics: "You've been active 12 weeks in a row!" makes missing a week feel like a loss
- When grandfathering existing members on pricing changes, frame it as avoiding loss: "Lock in your current rate"

### 26. Endowment Effect (Thaler, 1980)
People value things more simply because they own them.

**The psychology:** Ownership increases perceived value, even if nothing objectively changed.

**Community application:**
- Free trial → paid conversion works because members feel ownership after the trial
- Custom roles, personalized channels, or saved content create ownership
- "Your community, your space" messaging increases ownership
- Members who've customized their profile, earned badges, or built a post history feel ownership and resist leaving

### 27. Anchoring (Tversky & Kahneman, 1974)
The first piece of information people receive heavily influences subsequent judgments.

**The psychology:** The first number or impression sets an "anchor" that skews all further evaluation.

**Community application:**
- The first community experience anchors expectations — make it exceptional
- For paid communities: show the highest tier first, so the mid-tier feels reasonable
- When sharing engagement stats, anchor high: "Our most active members log in 5x/week" sets expectations
- When comparing communities: position your community against alternatives that make yours look favorable

### 28. Paradox of Choice (Schwartz, 2004)
Too many options lead to decision paralysis and reduced satisfaction.

**The psychology:** More choices = more cognitive load = less action.

**Community application:**
- Start communities with 3-5 channels, not 20 (Figma Community starts with curated spaces)
- Onboarding should offer 3 actions, not 10
- Event calendars with 2-3 options per week outperform calendars with 7+
- Discord's biggest UX problem is channel overwhelm — fight this actively

### 29. Commitment and Consistency (Cialdini, 1984)
Once people commit to something, they act consistently with that commitment.

**The psychology:** Small commitments lead to larger commitments. Consistency is a powerful social pressure.

**Community application:**
- Get small commitments first (introduce yourself, answer a poll, react to a post)
- Escalate: share your work → give feedback → host a discussion → become an ambassador
- Public commitments are stronger than private ones — "I commit to the 30-day challenge" posted in the community
- Application-based communities benefit from this: the effort of applying creates commitment

### 30. Overton Window
The range of ideas considered acceptable in a group shifts over time.

**The psychology:** Ideas start as unthinkable, become radical, then acceptable, then popular, then policy.

**Community application:**
- The Overton Window in your community determines what's "okay" to discuss or do
- If low-effort posts become acceptable, quality declines (window shifts down)
- If high-effort contributions are celebrated, quality rises (window shifts up)
- Moderation isn't just about removing bad content — it's about where you set the window
- Leaders posting high-quality content shifts the window up for everyone

---

## Conflict & Trust Models

### 31. Fundamental Attribution Error
People attribute others' behavior to character rather than circumstances.

**The psychology:** If someone is rude in a forum, we think "they're a rude person" rather than "they might be having a bad day."

**Community application:**
- Moderators should assume good intent on first offenses
- "That didn't land as intended" is better than "You're being disrespectful"
- This is why the warning DM template assumes good faith: "I know you probably didn't mean it that way"

### 32. Trust Battery (Tobi Lütke, Shopify CEO)
Every relationship starts with a "trust battery" at 50%. Actions charge or drain it.

**The psychology:** Trust is cumulative and directional. Small positive actions build it. Single negative actions can drain it significantly.

**Community application:**
- New members start at 50% trust — they're not yet committed or skeptical
- Every positive interaction charges the battery (helpful response, interesting discussion, warm welcome)
- Every negative interaction drains it (ignored question, toxic reply, broken promise)
- Once the battery hits ~20%, members leave silently
- Community managers should have a mental model of battery levels for key members

### 33. Deindividuation (Zimbardo, 1969)
Anonymity and group immersion reduce self-awareness and increase impulsive behavior.

**The psychology:** When people feel anonymous, they're more likely to act in ways they wouldn't face-to-face.

**Community application:**
- Real names and photos reduce deindividuation (people behave better when identifiable)
- Small, intimate channels reduce deindividuation more than large public ones
- This is why Discord raids and anonymous forum trolling are so common — deindividuation is high
- Verified identity communities (using real names, LinkedIn profiles) have lower toxicity

---

## Practical Application Models

### 34. The Hook Model (Eyal, 2014)
Trigger → Action → Variable Reward → Investment

**The psychology:** Products that create habits cycle through these four phases repeatedly.

**Community application:**
- Trigger: Notification of new discussion
- Action: Read and respond (make it easy — BJ Fogg's ability)
- Variable Reward: Unpredictable responses, insights, recognition
- Investment: Posting builds reputation, relationships, and history (increases switching costs)

### 35. Social Facilitation (Zajonc, 1965)
People perform better on simple tasks (and worse on complex tasks) when others are watching.

**The psychology:** The presence of others increases arousal, which enhances performance on familiar tasks.

**Community application:**
- Public accountability works for simple habits (daily writing, exercise, shipping)
- Complex creative work suffers from public scrutiny — provide private spaces for works-in-progress
- "Build in public" works for simple, measurable goals. Fragile creative processes need protection.

### 36. Cognitive Load Theory (Sweller, 1988)
Working memory is limited. Excessive information processing impairs learning and action.

**The psychology:** When cognitive load exceeds capacity, people shut down and disengage.

**Community application:**
- Onboarding should introduce 3 things, not 30
- Channel names should be self-explanatory
- Community rules should be scannable, not a legal document
- This is why "Start Here" pins outperform comprehensive wikis for new members

---

## Benchmark Data: Psychology-Backed Community Metrics

| Principle | Benchmark | Source/Basis |
|-----------|-----------|-------------|
| 1% Rule | 1% create, 9% contribute, 90% lurk | Nielsen (2006), validated across forums, wikis, social platforms |
| Dunbar's Number | ~150 meaningful relationships | Dunbar (1992), observed in social networks and organizational behavior |
| Critical Mass | 30-50 active members for self-sustaining | Community industry data (CMX, Orbit) |
| Network Effects inflection | 50-150 active members | Metcalfe's Law applied to community data |
| Loss Aversion ratio | Losses felt 2x more than gains | Kahneman & Tversky (1979) |
| Adoption curve | 2.5/13.5/34/34/16% | Rogers (1962) |
| Habit formation | 21-66 days of repetition | Lally et al. (2010) |
| Reciprocity response rate | 70%+ will reciprocate a favor | Cialdini (2001) |
| Psychological safety impact | 2.5x higher engagement | Google Project Aristotle (2015) |
| Social proof threshold | 3-5 visible participants trigger joining | Social proof research averages |

---

## Output Format

When applying community psychology:

### 1. Diagnosis
- Which principle(s) explain the current behavior?
- What's missing: motivation, ability, prompt, belonging, or something else?

### 2. Intervention Design
- Which model(s) to apply?
- Specific actions grounded in the science
- Expected behavioral outcome

### 3. Measurement
- How to know if the intervention worked
- Timeline for effects (immediate vs. habit-forming)

---

## Task-Specific Questions

1. What specific behavior are you trying to encourage (or discourage)?
2. Where in the member journey is the problem occurring?
3. What have you tried so far, and what happened?
4. Is the challenge about motivation, ability, or prompting?
5. How many active members do you have? (determines which group dynamics apply)

---

## Related Skills

- **community-culture**: For applying identity and belonging models
- **member-onboarding**: For applying activation and commitment models
- **engagement-programs**: For applying habit and reward models
- **retention-reactivation**: For applying loss aversion and endowment models
- **community-growth**: For applying network effects and social proof models
- **moderation-governance**: For applying broken windows and deindividuation models
- **community-strategy**: For applying all models to overall strategy design
