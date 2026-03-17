---
name: youtube-script-master
description: "Unified YouTube script creation for cardiology channels in Hinglish. Uses the COMPLETE research-engine pipeline (channel scraping, comment analysis, narrative monitoring, gap finding, view prediction) combined with RAG + PubMed for evidence. Data-driven topic selection, 15-30 min educational videos with 6-point voice check."
---

# YouTube Script Master

Unified skill for creating **data-driven**, evidence-based cardiology YouTube scripts in Hinglish.

**This skill CONSUMES data from the research-engine Python pipeline.** It does NOT replace that pipeline with manual web searches.

---

## CRITICAL: Run Research Pipeline First

Before writing ANY script, the research-engine should have been run to generate:
- Content calendar with prioritized topics
- Demand analysis (what people want)
- Gap analysis (where opportunities are)
- Narrative analysis (what misinformation to address)

```bash
cd "/Users/shaileshsingh/cowriting system/research-engine"
python run_pipeline.py --quick    # Quick mode (~10 min)
python run_pipeline.py            # Full mode (~30 min)
```

---

## Complete Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 1: DATA COLLECTION (Weekly - Python Pipeline)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  channel_scraper.py ──► Scrapes 35+ channels (no API needed)   │
│                         Competition, inspiration, belief-seeders│
│                                                                  │
│  comment_scraper.py ──► Downloads comments from top videos      │
│                         Extracts questions and pain points      │
│                                                                  │
│  OUTPUT: /data/scraped/latest_scrape.json                       │
│          /data/scraped/latest_comments.json                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 2: ANALYSIS (Python Pipeline)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  demand_signals.py ──► What topics get views/engagement         │
│                        Question themes, demand scoring           │
│                                                                  │
│  narrative_monitor.py ──► Tracks 8 dangerous narratives:        │
│                           1. LDL skepticism                      │
│                           2. Statin fear                         │
│                           3. Insulin primacy                     │
│                           4. Fasting absolutism                  │
│                           5. Supplement superiority              │
│                           6. Seed oil villain                    │
│                           7. Exercise compensation               │
│                           8. Fear mongering                      │
│                                                                  │
│  gap_finder.py ──► Content opportunities                        │
│                    CORRECTION_OPPORTUNITY (misinformation)       │
│                    LANGUAGE_GAP (English→Hindi needed)           │
│                    DEMAND_GAP (questions but no videos)          │
│                    PROVEN_TOPIC (high views in English)          │
│                                                                  │
│  view_predictor.py ──► ML prediction of video performance       │
│                        Ridge regression + TF-IDF on title        │
│                                                                  │
│  OUTPUT: /output/demand_analysis_*.json                          │
│          /output/narrative_analysis_*.json                       │
│          /output/content_gaps_*.json                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 3: PLANNING (Python Pipeline)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  idea_combinator.py ──► Seed ideas (300+) × Modifiers (215+)   │
│                         Filters by pillar, archetype, compat    │
│                         Prioritizes by demand + gap scores       │
│                                                                  │
│  calendar_generator.py ──► 100-day content calendar             │
│                            Mon/Wed/Fri schedule                  │
│                            Balanced by pillar and audience       │
│                                                                  │
│  OUTPUT: /output/calendar.json                                   │
│          /output/100-day-calendar.md (Obsidian-ready)           │
│          /output/idea-briefs/*.md (per-video briefs)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 4: KNOWLEDGE BUILDING (Per Video)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  knowledge_pipeline.py ──► RAG + PubMed in parallel             │
│    ├─► RAG: Your textbooks/guidelines (AstraDB)                 │
│    └─► PubMed: Latest research (NCBI API)                       │
│                                                                  │
│  OUTPUT: Knowledge brief with citations                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 5: SCRIPT WRITING (This Skill - Opus)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUTS:                                                         │
│  - calendar.json (which topic, why now)                         │
│  - content_gaps.json (opportunity type)                         │
│  - narrative_analysis.json (if debunk: which narrative)         │
│  - knowledge_brief (evidence for claims)                        │
│                                                                  │
│  APPLY:                                                          │
│  - Hinglish rules (70% Hindi / 30% English)                     │
│  - Script structure (hook → body → CTA)                         │
│  - Debunk protocol (if correction opportunity)                  │
│  - 6-point voice check                                          │
│                                                                  │
│  OUTPUT: Complete 15-30 min script in Hinglish                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Using Research Engine Outputs

### Step 1: Check the Content Calendar

```bash
# See next 5 topics to create
python calendar_generator.py --show-next 5

# Or read directly
cat /output/calendar.json | head -100
```

Each calendar entry includes:
- `seed_idea` - The topic
- `modifier` - The angle
- `gap_score` - Why this is an opportunity
- `recommended_date` - When to publish

### Step 2: Check If Debunk Needed

```bash
# Get threat ranking of narratives
python analyzer/narrative_monitor.py --threats

# Generate debunk ideas
python analyzer/narrative_monitor.py --debunk

# Get response video ideas for high-reach misinformation
python analyzer/narrative_monitor.py --response
```

**Output includes:**
- Which channels are promoting which narratives
- View counts of misinformation videos
- Pre-generated Hinglish hooks for debunk content
- Matched seed ideas for counter-content

### Step 3: Check Correction Opportunities

```bash
python analyzer/gap_finder.py --corrections
```

Returns high-reach misinformation videos with:
- Video title and views
- Narratives detected
- Suggested correction format (direct_response, evidence_synthesis, gentle_correction, indian_context)

### Step 4: Build Knowledge for Selected Topic

```python
from rag_pipeline.src.knowledge_pipeline import KnowledgePipeline

pipeline = KnowledgePipeline(verbose=True)
brief = pipeline.synthesize_knowledge("Your selected topic")
```

### Step 5: Write Script Using This Skill

With all data ready, apply the rules below.

---

## 35+ Tracked Channels (Data Source)

The research-engine tracks these channels in `target_channels.json`:

### Competition (Hindi) - Differentiate/Monitor
- Dr Navin Agrawal CARDIO CARE (300K+)
- Cardiac Second Opinion (100K+)
- SAAOL Heart Center (3.4M) - ANTI-PATTERN

### Indian Mega Channels - Monitor/Differentiate
- Fit Tuber (7M+)
- Dr Vikas Bangar (1M+)
- Satvic Movement (1M+)
- Dr Biswaroop Roy Chowdhury (4M+) - CRITICAL ANTI-PATTERN

### Inspiration (English) - Absorb Techniques
- **Peter Attia MD (1.5M+) - PRIMARY MODEL**
- York Cardiology (1M+)
- Nutrition Made Simple (1.2M+)
- The Proof with Simon Hill (1M+)
- Dr Ford Brewer (700K+)
- Medlife Crisis (1.5M+)

### Belief Seeders - HIGH DEBUNK PRIORITY
- **Dr Eric Berg (11M+) - Keto, insulin primacy, statin fear**
- **Dr Sten Ekberg (3.5M+) - Insulin, fasting**
- **Dr Ken Berry (2.5M+) - Carnivore, LDL skepticism**
- Dr Mark Hyman (3M+) - Functional medicine
- Dr Jason Fung (1M+) - Fasting
- Dr Pradip Jamnadas (1M+) - Popular in Indian diaspora

---

## 8 Tracked Narratives (For Debunk Content)

The narrative_monitor.py tracks these dangerous beliefs:

| Narrative | What They Claim | Key Channels |
|-----------|-----------------|--------------|
| ldl_skepticism | "LDL doesn't cause heart disease" | Berg, Ekberg, Berry, Low Carb Down Under |
| statin_fear | "Statins are dangerous/unnecessary" | Berg, Berry, SAAOL, Satvic |
| insulin_primacy | "Only insulin matters, not LDL" | Ekberg, Fung, Jamnadas, Hyman |
| fasting_absolutism | "Fasting cures/reverses everything" | Fung, Jamnadas, DeLauer |
| supplement_superiority | "Supplements > medications" | Berg, Hyman, Huberman |
| seed_oil_villain | "Seed oils cause heart disease" | Berry, Saladino |
| exercise_compensation | "Exercise reverses plaque" | Various |
| fear_mongering | "Doctors/pharma hide cures" | Dr Biswaroop, SAAOL |

When writing debunk content, use the **Steelman-Then-Correct Protocol** below.

---

## Hinglish Language Rules

### Word Choice Matrix

| Context | Use Hindi | Use English |
|---------|-----------|-------------|
| Emotions | Dil, zindagi, takleef | - |
| Medical terms | - | Cholesterol, BP, diabetes, LDL, HDL |
| Actions | Samjhiye, dekhiye, sochiye | - |
| Data | - | 80%, studies show, evidence |
| Body parts | - | Heart, arteries, blood |
| Severity | Khatarnak, serious | Critical, emergency |

**Ratio**: 70% Hindi / 30% English (technical terms only)

### Sentence Patterns

**Explanation:**
> "Cholesterol do type ka hota hai - LDL jo 'bad cholesterol' hai, aur HDL jo 'good cholesterol' hai. LDL zyada ho toh arteries mein jam jaata hai..."

**Evidence citation:**
> "2023 ki ek study, jisme 50,000 Indians the, usme paya gaya ki..."

**Practical advice:**
> "Toh aap kya karein? Simple hai - daily 30 minute walk, dinner 8 baje se pehle, aur sodium kam..."

### Transitions (Hindi)

- Point to point: "Ab doosri baat...", "Teen number...", "Sabse zaroori baat..."
- Contrast: "Lekin...", "Haan, magar...", "Yahan twist hai..."
- Emphasis: "Dhyan se suniye...", "Yeh important hai...", "Yeh mat bhooliye..."
- Story: "Ek patient ka case batata hoon...", "Mere saath kya hua..."

---

## Script Structure (15-30 min videos)

### HOOK (0:00 - 0:30)
Stop the scroll, create curiosity gap.

**Patterns:**
- Surprising statistic: "80% Indians jo yeh karte hain, unhe heart disease ka risk double hai..."
- Myth challenge: "Aapne suna hoga ki [belief]. Yeh galat hai. Main batata hoon kyun..."
- Story open: "Ek patient aaye mere paas, 42 saal ke. Unka case aapki aankhen khol dega..."
- Direct question: "Kya aap [common thing] karte ho? Yeh aapke dil ke liye kya kar raha hai?"

**Rules:**
- NO "Namaste dosto" (boring, skippable)
- First 5 seconds = most critical
- Create information gap that MUST be filled

**For Debunk Videos**, narrative_monitor.py generates Hinglish hooks like:
- "YouTube pe dekha ki LDL kharab nahi hai? Ek cardiologist ki sachai suniye..."
- "Statin se darr lagta hai? Main aapka darr samajhta hoon. Ab evidence dekhte hain..."

### INTRO + CREDIBILITY (0:30 - 2:00)
Establish authority, set expectations.

> "Main Dr. Shailesh, interventional cardiologist. Pichhle 15 saalon mein hazaaron patients dekhe hain. Aaj main aapko woh bataunga jo main apne patients ko clinic mein batata hoon..."

### BODY - Main Content (2:00 - 25:00)

**Structure Options:**

**A. Listicle (3-5 points)**
```
Point 1: [Setup → Evidence → Practical takeaway]
Transition: "Ab doosri baat..."
Point 2: [Setup → Evidence → Practical takeaway]
...
```

**B. Story-driven**
```
Patient case introduction
What happened (tension)
Medical explanation (education)
Resolution
Lessons learned
```

**C. Myth-busting (Debunk Format)**
```
State the myth clearly
Steelman: Why people believe it (from narrative_monitor data)
Evidence: What studies actually show (from knowledge_brief)
Nuance: The complete picture
What to do instead
```

**Engagement Beats (every 3-4 minutes):**
- Question to viewer: "Aapko kya lagta hai?"
- Surprising reveal: "Lekin yahan twist hai..."
- Relatable moment: "Aap bhi soch rahe honge..."
- Pattern interrupt: Change pace, tone, or visual cue

### SUMMARY + CTA (25:00 - 30:00)

**Summary:**
- Recap 3 key points (brief)
- One sentence takeaway
- "Agar sirf ek cheez yaad rakhni ho..."

**CTA (choose one primary):**
- Subscribe: "Is channel pe aisi videos regularly aati hain..."
- Comment: "Apna sawaal neeche likhiye, main jawab dunga..."
- Share: "Kisi apne ko bhejiye jinke kaam aa sake..."

---

## Steelman-Then-Correct Protocol (For Debunk Content)

### Step 1: Find the Kernel of Truth
Every popular health belief contains something true. Find it.

| Belief | Kernel of Truth |
|--------|-----------------|
| "LDL doesn't matter" | LDL alone isn't full picture; particle count, inflammation matter |
| "Statins are poison" | Statins do have side effects; not everyone needs them |
| "Fasting cures everything" | Fasting has metabolic benefits; caloric restriction helps |
| "Insulin is the real problem" | Insulin resistance IS important; metabolic health matters |

### Step 2: Acknowledge Explicitly

**Wrong:**
> "Yeh log galat hain. LDL clearly causes heart disease."

**Right:**
> "Yeh belief kahan se aayi? Actually, ek valid point hai. LDL alone se poori picture nahi milti. ApoB, particle count, inflammation - sab matter karta hai. Lekin iska matlab yeh nahi ki LDL matter hi nahi karta..."

### Step 3: Show the Logical Error

- **Oversimplification**: "It's not that simple..."
- **Cherry-picking studies**: "Jab hum ALL studies dekhte hain..."
- **Anecdote vs evidence**: "Kuch logon ka experience aisa hai, but population level pe..."

### Tone: Never Say / Instead Say

| Never Say | Instead Say |
|-----------|-------------|
| "Yeh log galat hain" | "Is approach mein ek problem hai" |
| "Bakwaas" | "Story itni simple nahi hai" |
| "Aap fool ban rahe ho" | "Partial truth hai, but..." |
| "Dangerous misinformation" | "Evidence kuch aur kehti hai" |

---

## 6-Point Voice Check

Before delivering ANY script, verify all 6:

| # | Check | Question |
|---|-------|----------|
| 1 | Authority | Would Topol/Attia/Huberman say this in Hinglish? |
| 2 | Domain Expert | Sounds like cardiologist, NOT wellness guru? |
| 3 | Rigor | Would pass as journal review (in English)? |
| 4 | Accessibility | 7th grader in Delhi can follow? |
| 5 | Non-Preachy | Explaining, NOT sermonizing? |
| 6 | Non-Judgmental | Evidence, NOT lifestyle shaming? |

See [voice-check.md](references/voice-check.md) for detailed criteria.

---

## Evidence Citation Protocol

### For Studies
> "2023 mein European Heart Journal mein ek meta-analysis aayi - 200 studies, 20 lakh logon pe. Finding? [specific finding]..."

### For Guidelines
> "ESC guidelines - Europe ke top cardiologists - recommend karte hain ki [specific recommendation]. Kyun? Because evidence shows..."

### For Clinical Experience
> "Mere practice mein pichhle 15 saal mein, maine [X] cases dekhe hain jahan [observation]..."

---

## Quick Reference: Data Files

| File | Location | Contains |
|------|----------|----------|
| Content calendar | `/output/calendar.json` | What to create and when |
| Demand analysis | `/output/demand_analysis_*.json` | What audience wants |
| Gap analysis | `/output/content_gaps_*.json` | Where opportunities are |
| Narrative threats | `/output/narrative_analysis_*.json` | What to debunk |
| Seed ideas | `/data/seed-ideas.json` | 300+ topic seeds |
| Modifiers | `/data/modifiers.json` | 215+ content angles |
| Target channels | `/data/target_channels.json` | 35+ tracked channels |

---

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/research-and-script [topic]` | Full workflow: data → knowledge → script |
| `/show-calendar` | View content calendar |
| `/debunk-script [narrative]` | Write correction video |
| `/idea-details [idea-id]` | Full research on specific idea |

---

## Deprecated Skills

This skill supersedes:
- `/.claude/skills/youtube-script-hinglish/skill.md` - DEPRECATED
- `/.claude/skills/debunk-script-writer/skill.md` - DEPRECATED
- `/.claude/skills/cardiology-youtube-scriptwriter/SKILL.md` - DEPRECATED

Use this unified skill instead.

---

*This skill ensures every YouTube script is DATA-DRIVEN (from research-engine) + EVIDENCE-BASED (from RAG+PubMed) + AUTHENTIC (Hinglish voice with 6-point check).*
