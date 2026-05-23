---
name: influencer-analyzer
description: "Track and analyze cardiology content creators (Topol, Attia, York Cardiology, Indian channels). Discovers content patterns, topics, engagement, and gap opportunities for your Hinglish content strategy."
---
# Influencer Analyzer

**Know what's working, find where to differentiate.** This skill tracks cardiology content creators and identifies opportunities for your content.

---

## WHAT IT DOES

| Step | Action | Output |
|------|--------|--------|
| 1 | Find influencer content via Perplexity/DuckDuckGo | URLs, articles, videos |
| 2 | Scrape and extract content patterns | Topics, formats, frequency |
| 3 | Analyze engagement signals | What resonates with audience |
| 4 | Generate gap analysis | Where you can differentiate |

---

## TRIGGERS

Use this skill when you say:
- "What is [Topol/Attia/competitor] posting about?"
- "Find gaps in cardiology content"
- "Analyze my competition"
- "What topics should I cover?"
- "Track cardiology influencers"

---

## TARGET INFLUENCERS

### International (English)
| Name | Platform | Focus | Why Track |
|------|----------|-------|-----------|
| @EricTopol | Twitter, Substack | Trials, digital health | Voice model, Ground Truths style |
| Peter Attia | Podcast, YouTube | Longevity, CVD prevention | Deep-dive style |
| York Cardiology | YouTube | Patient education | Clear explanations |
| Dr. Sanjay Gupta (York) | YouTube | ECG, clinical cases | Educational format |

### Indian (Hindi/English)
| Name | Platform | Focus | Why Track |
|------|----------|-------|-----------|
| Dr Navin Agrawal | YouTube | Patient education | Competition |
| Cardiac Second Opinion | YouTube | Second opinions | Competition |
| Dr. Devi Shetty | Videos | Affordable care | Authority |

### Anti-Patterns (What NOT to do)
| Name | Platform | Why Track |
|------|----------|-----------|
| SAAOL | YouTube | Misinformation to counter |
| Dr Biswaroop Roy Chowdhury | YouTube | Dangerous claims to debunk |

---

## USAGE

### In Claude Code (Recommended)

```
"Analyze what Eric Topol is posting about this week"

"Find gaps between Topol's content and Indian cardiology YouTube"

"What cardiology topics are trending that I haven't covered?"

"Compare my content strategy with Peter Attia"
```

### CLI Mode

```bash
# Analyze single influencer
python scripts/analyze_influencer.py --name "Eric Topol" --platform twitter

# Compare multiple influencers
python scripts/analyze_influencer.py --compare "Topol,Attia,York Cardiology"

# Find content gaps
python scripts/analyze_influencer.py --gaps --domain "Cardiology"

# Track specific topic
python scripts/analyze_influencer.py --topic "GLP-1" --influencers "Topol,Attia"
```

---

## OUTPUT FORMATS

### 1. Influencer Profile
```markdown
## Eric Topol (@EricTopol)

**Recent Focus (Last 30 days):**
- Clinical trials: 45%
- Digital health/AI: 30%
- COVID updates: 15%
- Book promotion: 10%

**Top Performing Topics:**
1. REDUCE-IT controversy (high engagement)
2. Apple Watch AFib detection (viral)
3. AI in diagnosis (consistent interest)

**Posting Patterns:**
- Frequency: 5-10 tweets/day
- Best times: 6AM, 12PM, 6PM PST
- Thread usage: Weekly deep-dives

**Style Notes:**
- Links to primary sources (PubMed, NEJM)
- Quotes key statistics
- Engages with critics
- Retweets junior researchers
```

### 2. Gap Analysis Report
```markdown
## CONTENT GAP ANALYSIS

**What Topol Covers That You Don't:**
- [ ] Weekly trial breakdowns
- [ ] Digital health intersection
- [ ] International guideline comparisons

**What You Cover That Topol Doesn't:**
- [x] Hinglish explanations
- [x] Indian patient context
- [x] Cost-conscious alternatives
- [x] Cultural nuances (vegetarian diets, family dynamics)

**OPPORTUNITY ZONES:**
1. **Translate English trials for Indian context**
   - Topol covers REDUCE-IT → You explain what it means for Indian patients

2. **Bridge the gap**
   - International guidelines → Indian applicability

3. **Underserved topics in English space**
   - Rheumatic heart disease (rare topic in US)
   - Tropical cardiology
   - Resource-limited settings
```

### 3. Competitive Comparison Table
```markdown
| Aspect | Eric Topol | Peter Attia | York Cardiology | You |
|--------|------------|-------------|-----------------|-----|
| Platform | Twitter/Substack | Podcast/YouTube | YouTube | YouTube |
| Language | English | English | English | Hinglish |
| Depth | Expert-level | Deep-dive | Patient-friendly | Expert→Patient |
| Frequency | Daily | Weekly | 2-3x/week | ? |
| Unique Angle | Trials/Digital | Longevity | ECG teaching | Indian context |
```

---

## INTEGRATION WITH YOUR SYSTEM

### Feeds Into:
- `research-engine/data/target_channels.json` - Channel tracking
- `youtube-script-master` - Topic selection
- `viral-content-predictor` - Content scoring
- `content-repurposer` - Multi-platform adaptation

### Data Flow:
```
influencer-analyzer
       ↓
[Gap Analysis Report]
       ↓
research-engine (topic prioritization)
       ↓
youtube-script-master (script creation)
       ↓
YOUR CONTENT (unique angle)
```

---

## HOW CLAUDE SHOULD USE THIS SKILL

When the user asks about competitors or content strategy:

### Step 1: Identify Target
```
User: "What is Topol posting about?"
→ Target: Eric Topol
→ Platforms: Twitter, Substack
```

### Step 2: Research with Perplexity
Use Perplexity MCP or web search to find:
- Recent posts/articles
- Engagement metrics
- Topic distribution

### Step 3: Analyze Patterns
- What topics repeat?
- What gets most engagement?
- What's the posting frequency?

### Step 4: Generate Gap Analysis
Compare with user's existing content:
- What's covered vs. uncovered?
- Where can user differentiate?
- What's the unique angle?

### Step 5: Actionable Recommendations
- Specific topics to cover
- Formats to try
- Timing suggestions

---

## SAMPLE WORKFLOW

```
User: "Find content gaps in cardiology YouTube"

Claude:
1. Uses Perplexity to search:
   - "Eric Topol recent tweets cardiology 2025"
   - "Peter Attia podcast topics 2025"
   - "York Cardiology recent videos"
   - "Indian cardiology YouTube channels"

2. Analyzes results:
   - Topic frequency
   - Engagement patterns
   - Content gaps

3. Cross-references with user's content:
   - What has user covered?
   - What's missing?
   - What's unique to user?

4. Outputs:
   - Gap analysis report
   - Priority topics list
   - Differentiation strategy
```

---

## DEPENDENCIES

```python
# Already have
anthropic>=0.18.0
python-dotenv>=1.0.0
rich>=13.0.0

# For web scraping (optional)
requests>=2.31.0
beautifulsoup4>=4.12.0
```

---

## API KEYS NEEDED

| Key | Purpose | Status |
|-----|---------|--------|
| PERPLEXITY_API_KEY | Web search | Already have (via OpenRouter) |
| ANTHROPIC_API_KEY | Analysis | Already have |

---

## PRE-CONFIGURED INFLUENCER PROFILES

Located in `data/influencers.json`:

```json
{
  "influencers": [
    {
      "name": "Eric Topol",
      "handle": "@EricTopol",
      "platforms": ["twitter", "substack"],
      "focus": ["clinical_trials", "digital_health", "AI_medicine"],
      "style": "expert_commentary",
      "track_for": "voice_model"
    },
    {
      "name": "Peter Attia",
      "handle": "peterattiamd",
      "platforms": ["podcast", "youtube", "newsletter"],
      "focus": ["longevity", "metabolic_health", "CVD_prevention"],
      "style": "deep_dive",
      "track_for": "format_inspiration"
    },
    {
      "name": "York Cardiology",
      "handle": "@YorkCardiology",
      "platforms": ["youtube"],
      "focus": ["ECG", "patient_education", "clinical_cases"],
      "style": "educational",
      "track_for": "competitor"
    },
    {
      "name": "Dr Navin Agrawal",
      "handle": null,
      "platforms": ["youtube"],
      "focus": ["patient_education", "hindi"],
      "style": "simple_explanations",
      "track_for": "competitor"
    }
  ]
}
```

---

## NOTES

- **Privacy**: Only analyze public content
- **Frequency**: Run weekly for trend tracking
- **Focus**: Gap analysis, not copying
- **Goal**: Find YOUR unique angle, not imitate others

---

*This skill helps you understand the competitive landscape so you can differentiate, not duplicate.*
