---
name: content-brief
description: Content brief template and creation methodology for SEO-optimized content. Use when preparing briefs for writers or planning new content pieces.
---

# Content Brief

## When to Use

- Preparing briefs for content writers
- Planning new content pieces
- Documenting SEO requirements for articles
- Aligning content with keyword research

## Brief Creation Methodology

### Step 1: Keyword Research
1. Identify primary keyword (highest priority)
2. Identify 3-5 secondary keywords
3. Extract People Also Ask questions
4. Note search intent (informational/commercial/transactional)

### Step 2: SERP Analysis
1. Analyze top 10 ranking pages
2. Note average word count
3. Identify common content format (listicle, guide, etc.)
4. Find content gaps (topics competitors miss)

### Step 3: Outline Creation
1. Create H1 with primary keyword
2. Plan H2s to cover required topics
3. Plan H3s for detailed sections
4. Map keywords to specific sections

### Step 4: Requirements Definition
1. Set word count target (based on competitors + 20%)
2. Define E-E-A-T requirements
3. Specify internal linking targets
4. Set readability target (Flesch 60-70)

## Brief Template

```markdown
---
type: content-brief
created_by: {agent_or_command}
created_at: {timestamp}
keyword: "{keyword}"
session_id: {session_id}
session_path: {session_path}
status: complete
---

# Content Brief: {Title}

## Target Keyword
- **Primary**: {keyword}
- **Secondary**: {keyword2}, {keyword3}, {keyword4}
- **Questions to Answer**:
  1. {PAA question 1}
  2. {PAA question 2}
  3. {PAA question 3}

## Search Intent
- **Type**: Informational | Commercial | Transactional
- **User Goal**: {what user wants to accomplish}

## Content Specifications
- **Word Count**: {min}-{max} words
- **Format**: {article, listicle, guide, comparison}
- **Tone**: {professional, conversational, technical}
- **Target Audience**: {description}

## Required Sections
1. **{H2: Section topic}** - {brief description of what to cover}
2. **{H2: Section topic}** - {brief description}
3. **{H2: Section topic}** - {brief description}
4. **{H2: Section topic}** - {brief description}

## Featured Snippet Opportunity
- **Type**: {paragraph, list, table}
- **Target Query**: {question to answer}
- **Format**: {how to structure the answer}

## Competitor Analysis
| Competitor | Word Count | Unique Angle | Gap |
|------------|------------|--------------|-----|
| {site1} | {count} | {angle} | {what they miss} |
| {site2} | {count} | {angle} | {what they miss} |
| {site3} | {count} | {angle} | {what they miss} |

## E-E-A-T Requirements
- **Experience**: {specific examples to include from first-hand experience}
- **Expertise**: {depth of coverage required, technical accuracy needs}
- **Authority**: {sources to cite, data to include}
- **Trust**: {claims to verify, transparency requirements}

## Internal Linking
- Link to: {list of existing content to link}
- Anchor text suggestions: {list}

## SEO Requirements Checklist
- [ ] Keyword in title and H1
- [ ] Keyword in first 100 words
- [ ] 1-2% keyword density
- [ ] Minimum 3 internal links
- [ ] At least 1 external authoritative link
- [ ] Meta title: 50-60 characters
- [ ] Meta description: 150-160 characters with CTA
- [ ] Flesch Reading Ease: 60-70
```

## Quality Checklist

Before finalizing a brief, verify:

- [ ] Primary keyword clearly defined
- [ ] Search intent identified and explained
- [ ] Word count based on competitor analysis
- [ ] All PAA questions captured
- [ ] Required sections cover all topics
- [ ] E-E-A-T requirements specific and actionable
- [ ] Internal linking targets identified
- [ ] Featured snippet opportunity noted (if any)
