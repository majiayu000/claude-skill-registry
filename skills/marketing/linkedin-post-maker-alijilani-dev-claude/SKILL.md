---
name: linkedin-post-maker
description: Creates engaging LinkedIn posts on any topic with proper formatting, hooks, and CTAs. Use when the user asks to create, generate, or write a LinkedIn post, social media content for LinkedIn, or professional social content. Asks clarifying questions to ensure quality and relevance.
allowed-tools: Read, Write, AskUserQuestion, Grep, Glob
---

# LinkedIn Post Maker

## Purpose
This skill generates high-quality, engaging LinkedIn posts on any topic while maintaining professional standards and best practices for the platform.

## Supporting Resources
- [BEST-PRACTICES.md](BEST-PRACTICES.md) - Comprehensive LinkedIn best practices, hook formulas, and engagement strategies
- [POST-TEMPLATE.md](POST-TEMPLATE.md) - Quick reference templates for different post types

## Instructions

### 1. Gather Information and Clarify Requirements

Before generating the post, assess if you have enough information. If any of the following are unclear or missing, use AskUserQuestion to clarify:

**Required Clarifications:**
- **Topic Depth**: If the topic is vague or too broad, ask for specific angles, key points, or main message
- **Target Audience**: Who is this post for? (e.g., software developers, entrepreneurs, HR professionals, general business audience)
- **Post Tone**: What style should the post have?
  - Professional/Corporate
  - Casual/Conversational
  - Thought Leadership
  - Educational/Tutorial
  - Inspirational/Motivational
  - Story-driven/Personal
- **Post Length**: What length is preferred?
  - Short (150-300 words) - Quick insights
  - Medium (300-600 words) - Standard engagement
  - Long (600-1000 words) - In-depth analysis
- **Key Message**: What's the main takeaway readers should have?
- **Call to Action**: What should readers do after reading? (e.g., comment, share experience, visit link, engage in discussion)

**Use AskUserQuestion strategically:**
- If topic is clear and specific: Ask 1-2 questions maximum (audience + tone)
- If topic is vague: Ask about topic specifics, target audience, and desired message
- If user provides detailed context: Proceed without questions

### 2. LinkedIn Post Structure

Every post should follow this proven structure:

**A. Hook (First 1-2 lines)**
- Grab attention immediately
- Make readers want to click "see more"
- Use patterns like:
  - Surprising statement
  - Relatable pain point
  - Bold claim or question
  - Personal story opening
  - Contrarian viewpoint

**B. Value/Body (Main content)**
- Deliver on the hook's promise
- Use short paragraphs (1-3 lines each)
- Include white space for readability
- Use formatting:
  - → Bullet points with arrows
  - ✓ Checkmarks for lists
  - Numbers for sequences
  - Line breaks between sections

**C. Key Takeaways (Optional for longer posts)**
- Summarize main points
- Use bullet format
- Make them actionable

**D. Call to Action**
- Ask engaging question
- Invite discussion
- Request shares or comments
- Encourage connection

**E. Hashtags (3-5 relevant tags)**
- Mix of popular and niche hashtags
- Industry-specific terms
- Topic-related keywords

### 3. Writing Best Practices

**Tone and Style:**
- Write conversationally (use "you", "I", "we")
- Keep sentences short and punchy
- Avoid jargon unless audience-appropriate
- Use active voice
- Show personality and authenticity

**Formatting:**
- Short paragraphs (1-3 lines)
- Blank lines between paragraphs
- Use emojis sparingly (1-3 max, only if tone-appropriate)
- Bold key phrases with asterisks: **like this**
- Create visual hierarchy

**Engagement Optimization:**
- Start with a hook that stops scrolling
- Provide genuine value or insight
- Make it relatable to target audience
- End with clear CTA
- Spark conversation in comments

### 4. Generate and Save the Post

**File Naming Convention:**
```
LinkedIn-Posts/YYYY-MM-DD_topic-keywords.md
```

Example: `LinkedIn-Posts/2025-12-21_ai-product-development.md`

**File Content Structure:**
```markdown
# LinkedIn Post: [Topic Title]

**Date Created:** YYYY-MM-DD
**Target Audience:** [audience]
**Tone:** [tone style]
**Length:** [word count] words

---

## Post Content

[The actual LinkedIn post goes here with proper formatting]

---

## Metadata
- **Main Topic:** [topic]
- **Key Themes:** [theme1, theme2, theme3]
- **Hashtags:** #hashtag1 #hashtag2 #hashtag3
- **Estimated Reading Time:** [X] seconds
```

### 5. Quality Checklist

Before finalizing, ensure:
- [ ] Hook is compelling and makes reader want more
- [ ] Content delivers value (insight, education, inspiration, or entertainment)
- [ ] Paragraphs are short and scannable
- [ ] Message is clear and focused
- [ ] Tone matches audience and purpose
- [ ] CTA encourages engagement
- [ ] 3-5 relevant hashtags included
- [ ] Proper formatting with white space
- [ ] No spelling or grammar errors
- [ ] File saved to LinkedIn-Posts directory

## Examples

### Example 1: Tech Topic - Short Casual Post

**User Request:** "Create a LinkedIn post about clean code"

**Clarifying Questions:** (if needed)
- Target audience: software developers, tech leads
- Tone: casual/conversational
- Length: short

**Generated Post:**
```
Your code might work perfectly.

But that doesn't mean it's good code.

Here's the difference:

Working code = solves the problem
Good code = solves the problem AND is easy to maintain

3 signs your code needs cleanup:

→ You can't explain what it does in 1 sentence
→ You need comments to understand your own logic
→ Making a small change breaks 3 other things

Clean code isn't about being fancy.
It's about being kind to your future self.

What's your #1 rule for writing clean code?

#SoftwareDevelopment #CleanCode #Programming #CodingBestPractices
```

### Example 2: Business Topic - Professional Tone

**User Request:** "Write about leadership and delegation"

**Generated Post:**
```
The hardest lesson I learned as a leader:

Delegation isn't about offloading work.
It's about multiplying impact.

Early in my career, I thought being a good leader meant:
- Being the smartest person in the room
- Having all the answers
- Doing the important work myself

I was wrong.

**Real delegation means:**

→ Trusting your team with meaningful work
→ Providing context, not just tasks
→ Creating space for others to grow
→ Being okay with different approaches

The result?
Your team becomes more capable. You create future leaders. And you free yourself to focus on what only you can do.

**The question isn't: "Can I do this better?"
The question is: "Who can I develop by giving this opportunity?"**

What's been your biggest challenge with delegation?

#Leadership #Management #TeamDevelopment #GrowthMindset #ProfessionalGrowth
```

### Example 3: Personal Story - Inspirational

**User Request:** "Post about overcoming failure in startup"

**Generated Post:**
```
Two years ago, I shut down my startup.

$200K invested. 18 months of work. Zero revenue.

I felt like a complete failure.

Today? I'm grateful it happened.

Here's what that "failure" taught me:

**About Product:**
→ Building what users want > building what you think is cool
→ Talk to customers BEFORE writing code
→ MVPs should be embarrassingly simple

**About Business:**
→ Revenue isn't optional—it's oxygen
→ Funding doesn't validate your idea
→ Burn rate kills dreams faster than bad products

**About Myself:**
→ I'm more resilient than I thought
→ Failure is data, not identity
→ Every setback teaches something valuable

The startup died. But I didn't.

Now I'm building again—smarter, humbler, and more focused.

Sometimes you need to fail at the wrong thing to succeed at the right thing.

Have you had a "failure" that became your best teacher?

#Entrepreneurship #StartupJourney #FailureIsPartOfSuccess #GrowthMindset #StartupLessons
```

## Advanced Tips

### When Topic Requires Research:
1. Use Grep/Glob to search existing posts for similar topics
2. Check for previous content to avoid repetition
3. Build on previous insights

### Hashtag Strategy:
- **Popular (100K+ posts):** 1-2 max (#Leadership, #Technology)
- **Medium (10K-100K):** 2-3 tags (#CleanCode, #ProductManagement)
- **Niche (Under 10K):** 1-2 tags (specific to topic)

### Engagement Patterns:
- Posts with questions get 50% more comments
- Posts with personal stories get higher engagement
- Lists and frameworks are highly shareable
- Contrarian takes spark discussion

## Common Mistakes to Avoid

❌ Starting with generic statements ("In today's fast-paced world...")
❌ Writing long paragraphs (makes readers scroll away)
❌ Using too much corporate jargon
❌ No clear takeaway or CTA
❌ Overusing hashtags (more than 5)
❌ Writing without considering target audience
❌ Being too salesy or promotional

## Version History
- v1.0.0 (2025-12-21): Initial release with core functionality
