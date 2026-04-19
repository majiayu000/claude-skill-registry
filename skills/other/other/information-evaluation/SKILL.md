---
name: information-evaluation
description: Evaluating online information for credibility, accuracy, and context. Covers the SIFT method (Stop, Investigate, Find, Trace), lateral reading, reverse image search, primary source verification, and common misinformation tactics. Use when assessing the trustworthiness of a web page, article, video, social media post, or any digital claim before relying on it or sharing it.
type: skill
category: digital-literacy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/digital-literacy/information-evaluation/SKILL.md
superseded_by: null
---
# Information Evaluation

Information evaluation is the discipline of deciding whether a piece of online information deserves your belief, your share, or your further attention. On the open web there is no gatekeeper: anyone can publish, anyone can amplify, and anything can look professional. The practical question is never "is this true?" in the abstract but "how much weight should I put on this before I act?" This skill catalogs the evaluation techniques that produce reliable answers quickly, grounded in the work of Mike Caulfield (SIFT), Sam Wineburg and Sarah McGrew (lateral reading), and the fact-checking community.

**Agent affinity:** rheingold (crap detection, net smart), palfrey (source analysis), noble (algorithmic framing of what you find)

**Concept IDs:** diglit-source-credibility, diglit-fact-checking, diglit-misinformation-tactics, diglit-search-strategies

## The SIFT Method

Mike Caulfield's SIFT method is the most important evaluation framework taught in undergraduate information literacy courses. It is designed to take 30-90 seconds per claim, which is the only time budget most users actually have.

| Step | Action | What it replaces |
|---|---|---|
| **Stop** | Recognize the claim and pause before reacting or sharing | Reflexive engagement |
| **Investigate** | Check who is making the claim and their track record | Trusting the surface presentation |
| **Find** | Look for better coverage of the same claim | Reading only the first result |
| **Trace** | Trace claims, quotes, and media back to their original context | Accepting mediated or stripped versions |

### Stop

The first move is not analysis -- it is a pause. Your emotional reaction to a headline or image is evidence about you, not about the claim. If a post makes you furious, delighted, or indignant, that is precisely when you should slow down. Strong emotion is the signature of content optimized to spread, and optimization for spread is not the same as optimization for truth.

**Practical gesture:** Before engaging, ask "do I know enough about this source to evaluate this claim right now?" If no, you proceed to Investigate. If yes, you proceed to Find.

### Investigate the source

Do not trust a source because its site looks professional. Modern web templates make any blog look like a newspaper. Instead, ask what others say about this source.

**The lateral reading move.** Open a new tab. Search the source's name (not the content of the article). Read what independent sources say about them. Wikipedia, MediaBiasFactCheck, NewsGuard, and established fact-checking organizations are better starting points than the source's own About page.

### Find better coverage

Your goal is not to decide whether this specific article is true. Your goal is to decide whether this claim is true. Search the core claim in a search engine and see who else is reporting it. If no established sources are reporting it, that is evidence against -- not proof against, but a strong signal.

### Trace claims, quotes, and media

Online content is almost always mediated: a screenshot of a tweet, a clip of a video, a summary of a study. Find the original. Then ask: (a) does the original say what the summary claims? (b) is the original in context?

## Lateral Reading

Sam Wineburg and Sarah McGrew's 2017 Stanford study compared how professional fact-checkers, historians, and undergraduates evaluated a set of web claims. Fact-checkers were vastly better -- not because they knew more, but because they used a different movement pattern.

**Vertical reading** (what students did): Open the page, read it carefully, look for internal signals of credibility (author bio, site design, citations).

**Lateral reading** (what fact-checkers did): Open the page, glance at it, open five other tabs to check what independent sources say about this source and this claim.

Vertical reading assumes the document is honest. Lateral reading assumes you need external context. Lateral reading is faster and produces dramatically more accurate judgments.

**The rule of thumb:** Never evaluate a site using only the site itself.

## Reverse Image Search

Images are among the most common vectors for misinformation because they feel like evidence. They are usually not what they claim to be. A flood photo from 2011 gets recirculated as a 2023 hurricane. A protest image from Turkey is labeled as being in France.

**Tools:** Google Images (reverse search by URL or upload), TinEye, Yandex Images. Yandex in particular is strong on faces and non-Western content.

**The workflow:**

1. Right-click the suspect image, "copy image address," or save it locally.
2. Paste or upload to a reverse image search engine.
3. Sort results by date (oldest first).
4. The earliest appearance usually reveals the real origin.

If the earliest appearance is from a stock photo site, a different event, or a year before the claimed date, the caption is lying about the image.

## Primary Source Verification

Many claims are attributed to "a study," "experts say," or "research shows" without naming the study. Your job is to find the actual source.

**Workflow:**

1. Search for the specific claim plus the word "study."
2. If a study is named or linked, open the actual paper (not a press release).
3. Read the abstract and the conclusion. Often the paper says something different, narrower, or more tentative than the coverage claims.
4. Check the methodology section for obvious red flags: tiny sample size, no control group, self-reported data, industry funding without disclosure.

A surprising fraction of viral science coverage misrepresents its own underlying research. This is usually not malicious -- it is the compression step from paper to headline, and compression loses caveats.

## Common Misinformation Tactics

Knowing the tactics makes them easier to see.

### False context

A real image or video is presented with a false caption. The content is authentic but the framing is wrong. Reverse image search is the primary defense.

### Manipulated content

Real content is edited: a quote is trimmed to reverse its meaning, a video is sped up to make a speaker look intoxicated, an image is photoshopped. Cross-check with unaltered versions.

### Impostor content

A fake version of a legitimate source is created (fake BBC domain, fake university press release). Check the URL carefully. Real news sites do not use URLs like "bbc-news-today.com" or "cnn-breaking.net."

### Fabricated content

Content made from nothing, designed to look authentic. Deepfakes are the most dramatic form. Cross-reference with primary sources is the only reliable defense.

### Emotional amplification

Content that is technically true but selected and framed to produce a specific emotional reaction. This is harder to detect because there is no falsehood to point to. The test is whether the framing generalizes: if the same logic applied to a different group produced an outrageous conclusion, the framing is doing most of the work.

### Fake engagement

Bot networks, paid engagement, and coordinated amplification make content appear more popular and consensus-supported than it is. Do not use "everyone is sharing this" as evidence for anything.

## When to Evaluate (And When Not To)

You cannot SIFT every claim you encounter -- that would be all you did. Reserve deep evaluation for:

- **High-stakes decisions.** Anything affecting your health, finances, legal status, or major life choices.
- **Claims you are considering sharing.** Sharing amplifies; amplifying a false claim makes you a vector.
- **Claims that surprise you.** If a claim changes your model of the world, verify before updating.
- **Claims that confirm what you already believe.** Confirmation bias is the sharpest hook. Verify *especially* when something feels obviously right.

For low-stakes content (a cute video, a restaurant recommendation, a celebrity gossip item), a quick Investigate glance is usually enough.

## When NOT to Use This Skill

- **Technical computer problems.** Use `computational-literacy` instead -- understanding how systems work is a different discipline.
- **Privacy decisions.** Use `data-privacy` -- evaluating what a service collects is not the same as evaluating a news claim.
- **Creative media production.** Use `media-creation` -- making media is upstream of evaluating it.

## Decision Guidance

When deciding whether to trust a claim, walk this short tree:

1. **Is the source recognized and independent?** If yes, trust conditionally. If no, proceed.
2. **Can I verify the claim in another independent source?** If yes, raise confidence. If no, lower it.
3. **Is the primary source available?** If yes, check it. If it says something different, trust the primary.
4. **Is media (image, video) attached?** Reverse-search it before treating it as evidence.
5. **Am I feeling emotionally charged?** Add a deliberate delay before sharing.

If any step fails, do not share. Sharing is the most consequential decision a reader makes online.

## Cross-References

- **rheingold agent:** Crap detection, "Net Smart" framework, community-based verification
- **palfrey agent:** Source analysis, institutional credibility, Berkman Klein framework
- **noble agent:** How search algorithms privilege certain sources and suppress others
- **digital-citizenship skill:** What to do once you have evaluated a claim -- sharing responsibly
- **algorithmic-awareness skill:** Why some claims reach you at all

## References

- Caulfield, M. (2019). *SIFT (The Four Moves)*. Hapgood (Open Resource).
- Wineburg, S., & McGrew, S. (2017). "Lateral Reading: Reading Less and Learning More When Evaluating Digital Information." Stanford History Education Group Working Paper.
- Rheingold, H. (2012). *Net Smart: How to Thrive Online*. MIT Press.
- Wardle, C., & Derakhshan, H. (2017). *Information Disorder*. Council of Europe Report.
- boyd, d. (2017). "Did Media Literacy Backfire?" *Data & Society*.
