---
name: shownotes-generator
description: Generate comprehensive "Shownotes" summaries from longform articles, papers, transcripts, videos, or audio content. Use when users request shownotes, episode summaries, content summaries with takeaways, or when they reference the mdynotes.com format. Creates structured summaries with metadata, hooks, takeaways, quotes, and references.
---

<!--
Created by: mdy (https://mdynotes.com/)
Created: 2025-Oct-28
Version: 1.7 || Last Update: 2025-Nov-16
License: Creative Commons Attribution 4.0 International (CC BY 4.0)
Attribution Required: Yes - Include author name and link when sharing/modifying
For the latest version, check mdynotes.com/resources

CHANGELOG
v1.7: Added use of tables as alternative to bullets
v1.6: Improved instruction in the Quotes section 
v1.5: Strict adherence to Markdown for more consistent results 
v1.4: Restructured with top-level REFERENCE.md for examples; condensed main instructions; added inline examples
v1.3: Added conciseness guidelines to reduce verbosity while maintaining nuance with accompanying examples
v1.2: Added "this is AI-generated" disclaimer
v1.1: Added this metadata section
v1.0: Ported to Claude Skills format from prompt format
-->

# Shownotes Generator

Generate comprehensive, well-formatted shownotes from any longform content (articles, papers, transcripts, videos, audio). Shownotes follow a specific structure designed to provide value to target audiences through engaging hooks, detailed takeaways, memorable quotes, and proper attribution.

## When to Use

Invoke this skill when users:

- Explicitly request "shownotes" or "show notes" for content
- Ask for episode summaries with takeaways and quotes
- Reference the mdynotes.com format or style
- Request structured summaries that include:
  - Engaging hooks or key questions
  - Detailed takeaways with attribution
  - Memorable quotes from speakers/authors
  - Author/speaker references and links
- Provide longform content in these formats:
  - Podcast or video transcripts
  - Research papers or academic articles
  - Blog posts or long-form articles
  - Audio recordings (when transcribed)

**Do NOT use this skill when:**

- Users want a simple, brief summary (use standard summarization instead)
- Content is short-form (tweets, short posts, brief articles)
- Users only need key points without detailed structure
- No author/speaker attribution is needed

## Core Workflow

### Step 1: Infer Metadata

Analyze the content and infer these variables:

- **Original Content Type**: [Paper, Video, Blog post, Article, Audio, Transcript]
- **Original Source**: [URL if available]
- **Target Audience**: [Role interested in the topic]
- **Main Topic**: [Specific topic covered]
- **Date Published**: [Original publication date]
- **Shownotes Generated**: [Today's date]
- **Technical Terms**: [Key terminology used]
- **Model Used**: [Current LLM model]
- **Prompt Used**: shownotes-generator-skill-v# (where the version # is inferred based on comment block near the start of this skill file)

Ask the user to confirm the inferred metadata. Request corrections and update as needed before proceeding.

### Step 2: Generate Shownotes Structure

Create shownotes following this exact structure:

#### Header Section
Display the confirmed metadata as bullet points.

#### Disclaimer (include the following, including horizontal lines/separators)

CRITICAL: Format the disclaimer section exactly as shown below to ensure it renders in normal paragraph font, not heading font:

---

**Disclaimer:** These notes are AI-generated, may have errors, and are not a substitute for reading/watching/listening to the real thing.

---

#### The Hook
Craft an engaging question that:
- Frames the main topic
- Highlights the value proposition
- Makes readers want to explore further

**Example**: "How can trust and safety teams balance user protection with freedom of expression while scaling globally—and what lessons can we learn from those who've been in the trenches?"

#### The Summary
Format: "In this [content type] of [show/series name], [author introduction and credentials]. [Brief description of discussion format and collective expertise]."

CRITICAL: After the opening paragraph, include a "Topics discussed:" section formatted as a bulleted list:

Topics discussed:

- [Specific topic 1 with concrete details]
- [Specific topic 2 with concrete details]
- [Continue for 6-8 topics total]
- And much more!

**Example opening**: "In this research paper from MIT and Stanford, Dr. Sarah Chen (Director of Trust & Safety at TechCorp) and Professor James Williams (Digital Ethics researcher) explore the evolution of content moderation practices."

Key requirements:

- Use hyphens for bulletpoints to keep them markdown-compatible
- Each topic should be a complete phrase or sentence, not just keywords
- Ensure all authors/speakers are represented across the topics

#### Takeaways Section (4-10 takeaways)

**CRITICAL REQUIREMENT**: Before finalizing takeaways, verify that EACH takeaway directly addresses or supports the main question posed in the Episode Hook. Silently verify relevance but do not include verification process in output.

Format each takeaway as:

**[Number]. [Major insight with bold title].**

[Opening paragraph with key context and primary speaker quote in italics]

[Second paragraph with bulleted breakdown when appropriate:]

- [Point 1 with specific detail]
- [Point 2 with specific detail]
- [Point 3 with specific detail]
- [Point 4 with specific detail]

[Closing paragraph with implications or why this matters]

**Formatting Guidelines:**

- Use bold topic sentences to convey main points immediately
- Break long concepts into multiple paragraphs (NO walls of text)
- Add bullet points for lists, frameworks, advantages, or processes
- Use tables if the structure improves reading comprehension
- Takeaways must be easy to skim, with bullets and bolding/italics
- Include specific examples and quotes distributed across paragraphs
- If a takeaway doesn't directly support the hook question, reframe or replace it

**Conciseness Guidelines:**

- Eliminate redundant phrases ("in many cases," "it's important to note")
- Tighten bullet points by removing obvious explanations
- Cut transitional padding and combine related ideas
- Prefer active voice constructions
- Remove unnecessary qualifiers ("significantly," "particularly," "specifically")
- **Target length**: 130-170 words per takeaway (though okay to exceed if needed)
- Every word should earn its place

**Example**
```
**1. Trust and safety requires balancing competing values, not applying universal rules.**

Dr. Chen emphasizes that *"the hardest part of trust and safety isn't writing policies—it's making nuanced decisions when fundamental values like safety and expression come into conflict."* This insight challenges the perception that content moderation is simply enforcing clear rules.

**Four key principles** for navigating these tensions:
• **Context sensitivity**: The same content may be appropriate in one community but harmful in another, requiring local and cultural understanding
• **Stakeholder inclusion**: Effective policies emerge from ongoing dialogue with diverse user groups, not top-down mandates
• **Transparency with nuance**: Users deserve clear explanations of decisions while acknowledging that some contexts require confidentiality
• **Continuous evolution**: Policies must adapt as platform usage, cultural norms, and threat vectors change

The implications extend beyond social media. As Chen notes, any platform facilitating user interaction faces similar challenges, from gaming communities to professional networks. Organizations that recognize moderation as an ongoing balancing act rather than a solved problem maintain user trust more effectively.
```
**What makes this work:**

- Active voice throughout
- Combined related sentences naturally
- Removed filler words like "First," "Second," "Third," "Finally"
- No unnecessary transitions between paragraphs
- Every sentence adds new information

See **REFERENCE.md** for additional verbose vs. concise examples.

#### Interesting Quotes (if applicable)

**Process (silent - don't explain to user):**

1. Identify two to four sections most directly relevant to the episode hook
2. Pull multiple quotes from that specific section
3. Present quotes with context

Format:
**[Number]. [Topic/Theme]**

Here's how [Authors] summarized [framework/perspective]:

[Perspective 1]:

- [Point with title]. "[Quote with explanation]"
- [Additional points as relevant]

See **REFERENCE.md** for detailed quote formatting examples.

#### Related Content Links

Related resources mentioned:

- [Link to related content 1]

#### References

**Where to find the authors:**

**[Author/Speaker 1 Name]**:  

- X: [link]
- LinkedIn: [link]
- [Website/newsletter]: [description]

**[Author/Speaker 2 Name]**:  

- X: [link]
- LinkedIn: [link]
- [Website/newsletter]: [description]

[Add all notable authors/speakers]

**Mentions during the episode:**  

- [All tools, books, articles, companies mentioned with links]

## Content Analysis Guidelines

### Multi-Author Focus

- Identify author dynamics and expertise areas
- Extract major learnings with proper attribution
- Note areas of consensus vs. disagreement
- Show how different perspectives complement each other
- Ensure balanced representation of all major authors

### Writing Style

- Professional but conversational tone
- Well-structured takeaways with multiple paragraphs and strategic bullet points
- Clear author attribution for quotes and insights
- Use concrete examples and actionable advice
- Emphasize the value of multiple perspectives
- Concise without sacrificing nuance—every sentence adds value

See **REFERENCE.md** for common verbosity patterns to avoid.

### Quality Standards

- Each takeaway provides standalone value with improved readability
- All major authors represented in content
- Different viewpoints properly highlighted
- Resources and mentions comprehensively cataloged
- Quotes clearly attributed with context
- EVERY takeaway must directly support the episode hook question
- Efficient communication: 130-170 words per takeaway

See **REFERENCE.md** for formatting examples and conciseness principles.

## Examples

### Example: Podcast Transcript Request

**User provides:** Transcript from a 90-minute podcast interview with three AI researchers discussing alignment challenges.

**User asks:** "Can you create shownotes for this podcast transcript?"

**Skill output includes all sections:**

1. **Header** - Displays confirmed metadata (content type, source, audience, topic, dates, model, prompt version)
2. **Disclaimer** - AI-generated warning with horizontal separators
3. **The Hook** - "How can we ensure AI systems remain aligned with human values as they become more capable—and what are the hardest unsolved problems in alignment research?"
4. **The Summary** - Opening paragraph introducing the three researchers and their credentials, followed by "Topics discussed:" with 6-8 bulleted topics ending with "And much more!"
5. **Takeaways** - 6-8 detailed takeaways (130-170 words each) with quotes from all three researchers, strategic bullet points, and clear attribution
6. **Interesting Quotes** - Key quotes pulled from the most hook-relevant section with context
7. **Related Content Links** - Papers, tools, and resources mentioned during the episode
8. **References** - Author social links (X, LinkedIn, websites) plus all mentioned tools, books, articles, companies

## Final Checklist

Before delivering shownotes:

1. ✓ Metadata confirmed with user
2. ✓ Disclaimer placed immediately after metadata
3. ✓ Hook directly poses the central question
4. ✓ Summary introduces all key authors and topics
5. ✓ Each takeaway passes silent relevance check (supports hook)
6. ✓ Formatting uses paragraphs and strategic bullets (no walls of text)
7. ✓ Conciseness review completed (see REFERENCE.md for guidelines)
8. ✓ Quotes pulled from most hook-relevant section
9. ✓ All authors properly attributed throughout
10. ✓ References and links comprehensive

For detailed examples and formatting reference, see **REFERENCE.md**.
