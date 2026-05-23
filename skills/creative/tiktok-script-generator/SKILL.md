---
name: tiktok-script-generator
description: Generates 3 TikTok short video scripts (40–50s UGC ad style) in German with MANDATORY Chinese translation, plus a bilingual Campaign Summary. Uses official ElevenLabs v3 audio tags (every line MUST have 1-2 cues). References pre-existing analysis files (does NOT duplicate content). Outputs Obsidian-ready notes to product_list/YYYYMMDD/{product_id}/scripts/ with required frontmatter and sections. OPTIMIZED with batched Write calls.
version: 2.3.0
author: Claude
execution_agent: Claude Code (direct writing with parallel tool calls)
prerequisite: tiktok-product-analysis
---

# TikTok Script Generator Skill v2.3

**PURPOSE:** Generate production-ready UGC TikTok ad scripts with official ElevenLabs v3 audio tags (German VO + mandatory Chinese translation)
**EXECUTOR:** Claude Code (for quality creative writing)
**INPUT:** Analysis files from `tiktok-product-analysis` skill
**OUTPUT:** 3 scripts + Campaign Summary (references analysis, no duplication)
**STYLE:** Fast-paced UGC ads with mandatory emotion cues (1-2 per line), engaging delivery, dynamic performance
**OPTIMIZATION:** Batched Write calls (4 files per product in single message) ⭐ **2x faster**

⚠️ **CRITICAL FORMAT RULE - READ THIS FIRST:**
- **INLINE CUES ONLY:** `[emotion] Text here.` (cue + text on SAME LINE)
- **NEVER BROKEN LINES:** Do NOT write `[emotion]` on one line followed by text on the next line
- **EVERY LINE NEEDS CUES:** No orphan text without emotion tags
- See `templates/voiceover_format.md` for complete format specification

---

## Agent Responsibility

| Task | Agent | Why |
|:-----|:------|:----|
| Image/Video Analysis | Gemini MCP | Parallel processing, token-efficient |
| Script Writing | Claude Code | Better creative quality, detailed storyboards |
| Campaign Summary | Claude Code | Executive synthesis, proper references |

**Key Lesson:** Gemini produces generic placeholder scripts. Claude produces detailed, product-specific content with natural voiceovers.

---

## Workflow (4 Steps - OPTIMIZED)

```
[Step 0: Pre-Check] → GATE
        │
        ▼
[Step 1: Read Analysis Files in Parallel] → Extract key insights
        │                                     (5+ Read calls at once)
        ▼
[Step 2: Generate All Scripts + Summary] → Create all 4 files
        │                                    (in single response)
        ▼
[Step 3: Write All Files in Parallel] → 4 Write calls simultaneously
        │                                ⭐ 2x faster
        ▼
[Step 4: Quality Gate] → Verify completeness
```

**Key Optimization (v2.3.0):** Steps 2-3 now execute in ONE MESSAGE with parallel Write tool calls, eliminating sequential overhead.

---

## Step 0: Pre-Check Gate (MANDATORY)

**DO NOT PROCEED if analysis files are missing.**

```bash
product_id="{product_id}"
# Use the correct dated batch folder:
date="YYYYMMDD"
base="product_list/$date/$product_id"

echo "=== PRE-CHECK: $product_id ==="

# MANDATORY: Video synthesis must exist
if [ ! -f "$base/ref_video/video_synthesis.md" ]; then
    echo "❌ BLOCKED: video_synthesis.md missing"
    echo "Run tiktok-product-analysis skill first"
    exit 1
fi

lines=$(wc -l < "$base/ref_video/video_synthesis.md" | tr -d ' ')
if [ "$lines" -lt 150 ]; then
    echo "❌ BLOCKED: video_synthesis.md too short ($lines lines, need 150+)"
    exit 1
fi

# CRITICAL: Verify synthesis has properly flagged compliance risks
echo "Checking compliance flagging in analysis..."
if ! python3 scripts/validate_compliance_flags.py "$base/ref_video/video_synthesis.md" >/dev/null 2>&1; then
    echo "⚠️ WARNING: video_synthesis.md has compliance risks not properly flagged"
    echo "   Review and ensure risks are documented in 'Compliance & Trust Signals' section"
    echo "   Run: python3 scripts/validate_compliance_flags.py \"$base/ref_video/video_synthesis.md\""
    # Don't block, but warn - analysis files can have flagged risks
fi

echo "✅ Pre-check passed. Ready for script generation."
```

**If blocked:** Run `tiktok-product-analysis` skill first.

### Recommended (Repo Verifier)

```bash
bash scripts/verify_gate.sh --date YYYYMMDD --csv scripts/products.csv --phase analysis
```

---

## Step 1: Read Analysis Files (PARALLEL v2.3.0)

**CRITICAL OPTIMIZATION:** Use parallel Read tool calls to fetch ALL files in ONE MESSAGE.

**Files to read (make 4-5 parallel Read calls):**

1. **`ref_video/video_synthesis.md`** (CRITICAL)
   - Hook patterns, selling points, replication strategy
   - Target audience, production patterns
   - DO's and DON'Ts

2. **`product_images/image_analysis.md`** (if exists)
   - Visual hooks (Section 10)
   - German text from packaging
   - Color/variant recommendations

3. **`tabcut_data.json`** (product metadata)
   - Product name, price, shop
   - Sales data, conversion rate

4. **`fastmoss_data.json`** (fallback if tabcut data is missing/unknown)
   - Use if product_name is "Unknown Product" or key sales metrics are null

5. **Individual `video_N_analysis.md` files** (optional, for deep dive)
   - Use if video_synthesis.md lacks detail

**Example parallel execution:**
```
<Read file_path="product_list/YYYYMMDD/{product_id}/ref_video/video_synthesis.md" />
<Read file_path="product_list/YYYYMMDD/{product_id}/product_images/image_analysis.md" />
<Read file_path="product_list/YYYYMMDD/{product_id}/tabcut_data.json" />
```
All 3 files read simultaneously in ~2-3 seconds (was 6-9 seconds sequential).

**Extract these key elements:**
- Top 3 hook patterns from synthesis
- Top 5 selling points (ranked)
- 3 recommended script angles
- German terminology from packaging
- Visual filming instructions

---

## Step 2-3: Generate and Write All Scripts (BATCHED v2.3.0)

**CRITICAL OPTIMIZATION:** Generate all 3 scripts + Campaign Summary in ONE response, then make 4 parallel Write tool calls.

**Old workflow (sequential - SLOW):**
```
Generate Script 1 → Write Script 1 → Generate Script 2 → Write Script 2 → Generate Script 3 → Write Script 3 → Generate Summary → Write Summary
Total: ~5-8 minutes per product
```

**New workflow (batched - FAST):**
```
Generate all 4 files (Scripts 1-3 + Summary) → Write all 4 in parallel
Total: ~2-3 minutes per product ⭐ 2x faster
```

**Implementation:**
1. After reading analysis files, generate complete content for all 4 files
2. In a SINGLE MESSAGE, make 4 Write tool calls in parallel:
   - Write Script 1
   - Write Script 2
   - Write Script 3
   - Write Campaign Summary

**Each script must have:**

### Required YAML Frontmatter (Obsidian)

**See `templates/frontmatter_template.md` for complete specification.**

**Quick reference:**
- `duration` target: 00:40–00:50
- `tags` max 5 and meaningful for commerce/interest
- `caption` uses YAML block scalar `caption: >-` with hashtags appended (space-separated)
- Always include `source_notes` to exact files used

### TikTok Policy Compliance (DE Market) - ENHANCED v2.0

**CRITICAL:** These rules prevent TikTok ad rejection and "false advertising" complaints in the German market. All scripts MUST pass compliance validation before publication.

---

#### **POLICY 1: No Exact Low Price Bait** 🚫

**Prohibited:** Specific € amounts combined with urgency, comparison, or scarcity framing.

| ❌ VIOLATION | ✅ COMPLIANT ALTERNATIVE |
|:-------------|:------------------------|
| "Nur 9€!" | "Super günstig!" / "Tolles Preis-Leistungs-Verhältnis" |
| "€9.99 statt €50" | "Fraktioniert vom Markenpreis" / "Für kleines Geld" |
| "Nur noch 3 Stück!" | "Jetzt verfügbar" / "Schnell bestellen" |
| "Warum 150€ zahlen?" | "Markengeräte oft teurer" / "Ohne Aufpreis" |
| "50% Rabatt" | "Top Angebot" / "Aktionspreis" |
| "Jetzt nur €29,99" | "Aktuell besonders günstig" |

**Safe Price Language:**
- German: `"preiswert"`, `"erschwinglich"`, `"für kleines Geld"`, `"fairer Preis"`, `"gutes Preis-Leistungs-Verhältnis"`
- Chinese: `"价格很友好"`, `"很划算"`, `"性价比高"`, `"不贵"`

**Rule:** Avoid exact €, comparison math ("statt/vs"), or urgency tied to price.

---

#### **POLICY 2: No Absolute Effect Claims** 🚫

**Prohibited:** "100%", "pure", "perfect", "genauso gut", "never", "always", "instant" without qualification.

| ❌ VIOLATION | ✅ COMPLIANT ALTERNATIVE |
|:-------------|:------------------------|
| "100% wasserdicht" | "Wasserabweisend" / "Spritzwassergeschützt" |
| "Pure Freude" | "Richtig schön" / "Tolles Gefühl" |
| "Perfektes Geschenk" | "Schöne Geschenkidee" / "Praktisches Geschenk" |
| "Genauso gut wie [Brand]" | "Vergleichbare Qualität" / "Gute Alternative" |
| "Besser als [Brand]" | "Stark genug" / "Für [use case] geeignet" |
| "Nie wieder [problem]" | "Reduziert [problem]" / "Hilft bei [problem]" |
| "Sofort [result]" | "Schnell [result]" / "In kürzester Zeit" |
| "Komplett schützt" | "Bietet Schutz" / "Schützt vor [specific]" |

**Safe Comparison Language:**
- German: `"hilft bei"`, `"unterstützt"`, `"kann"`, `"für... geeignet"`, `"stark genug"`
- Chinese: `"有助于"`, `"支持"`, `"适合"`, `"功能强大"`, `"能满足需求"`

**Rule:** Use qualified claims with "hilft bei", "unterstützt", or specific context instead of absolutes.

---

#### **POLICY 3: No Exaggerated Promotions** 🚫

**Prohibited:** Unverifiable superlatives, false urgency, hyperbolic claims without proof.

| ❌ VIOLATION | ✅ COMPLIANT ALTERNATIVE |
|:-------------|:------------------------|
| "Unbezahlbar!" | "Unersetzlich" / "Wertvoll" / "Besonders" |
| "Genial!" | "Clevere Lösung" / "Praktisch" / "Wirklich gut" |
| "Unglaublich!" | "Beeindruckend" / "Überzeugend" |
| "Bevor es weg ist!" | "Mehr entdecken" / "Jetzt bestellen" |
| "Letzte Chance!" | "Verfügbar" / "Aktuell auf Lager" |
| "Nur noch 3 Stück!" | "Guter Lagerbestand" / "Jetzt verfügbar" |
| "Sie müssen das haben!" | "Lohnt sich" / "Praktisch für" |
| "Das beste Produkt!" | "Eine gute Wahl" / "Empfehlenswert" |
| "100% empfohlen" | "Wir empfehlen" / "Top Bewertungen" |

**Safe Promotion Language:**
- German: `"praktisch"`, `"clever"`, `"hilfreich"`, `"empfehlenswert"`, `"wertvoll"`, `"besonders"`
- Chinese: `"实用"`, `"方便"`, `"值得推荐"`, `"有价值"`, `"特别"`

**Rule:** Avoid hyperboles without proof. Use descriptive, specific benefits instead.

---

#### **POLICY 4: Medical & Health Claims** 🚫

**Prohibited:** Therapy, healing, pain relief, medical treatment framing.

| ❌ VIOLATION | ✅ COMPLIANT ALTERNATIVE |
|:-------------|:------------------------|
| "Heilt [condition]" | "Unterstützt bei [condition]" / "Hilft bei [condition]" |
| "Schmerzlinderung" | "Entspannung" / "Wohlbefinden" / "Angenehm" |
| "Schmerzfreiheit" | "Lindert" / "Besseres Gefühl" |
| "Physiotherapie" | "Massage-Funktion" / "Entspannungsmodus" |
| "Tiefengewebe-Behandlung" | "Intensive Massage" / "Tiefe Entspannung" |
| "Medizinisch bewährt" | "Beliebt bei" / "Viele nutzen" |

**Safe Wellness Language:**
- German: `"Entspannung"`, `"Wohlbefinden"`, `"lockert Verspannungen"`, `"angenehm"`, `"komfortabel"`, `"entspannend"`
- Chinese: `"放松"`, `"舒适"`, `"缓解紧绷感"`, `"享受"`

**Rule:** Never promise medical outcomes. Use wellness/comfort framing only.

---

#### **POLICY 5: Waterproof & Tech Specs** 🚫

**Prohibited:** Absolutes without IP rating proof, ambiguous tech claims.

| ❌ VIOLATION | ✅ COMPLIANT ALTERNATIVE |
|:-------------|:------------------------|
| "100% wasserdicht" | "Spritzwassergeschützt" (IPX4) / "Wasserabweisend" |
| "Komplett wasserdicht" | "Für Regen geeignet" / "Schützt vor Spritzwasser" |
| "4K Support" (ambiguous) | "Unterstützt 4K Dekodierung" / "4K-kompatibel" |
| "Zero Lag" / "Keine Verzögerung" | "Flüssige Wiedergabe" / "Schnelle Reaktion" |
| "Instant [result]" | "Schnell [result]" / "Kurze Ladezeit" |

**Safe Tech Language:**
- Waterproof: Use IP rating ONLY if sourced (e.g., "IP67" from packaging)
- Performance: Use qualified terms ("flüssig", "schnell", "zuverlässig")
- Avoid: "instant", "zero", "100%", "komplett", "total"

---

#### **Compliance Validation Checklist**

Before finalizing scripts, verify:

```bash
# Run compliance validator on generated scripts
for script in product_list/YYYYMMDD/{product_id}/scripts/*.md; do
  [[ "$(basename "$script")" == "Campaign_Summary.md" ]] && continue
  python3 scripts/validate_compliance_flags.py "$script"
done
```

**Manual Review Points:**
- [ ] No € symbols in captions or voiceovers
- [ ] No "100%", "pure", "perfect", "genauso gut", "besser als"
- [ ] No "unbezahlbar", "genial", false urgency ("weg ist", "letzte Chance")
- [ ] Medical terms replaced with wellness language
- [ ] Tech specs qualified (not absolute)

**If validation fails:**
1. Check the specific violation flagged
2. Find the compliant alternative in the table above
3. Replace and re-validate
4. Never bypass compliance checks

---

### Required Sections

```markdown
## Scripts

[1–2 sentence concept description]

### Structure (35s)
- Hook: [Description] (0-3s)
- Problem/Reveal: [Description] (3-8s)
- Solution/Demo: [Description] (8-20s)
- Benefits: [Description] (20-30s)
- CTA: [Description] (30-35s)

### Visual Strategy - ENHANCED TEMPLATE

**Required format:** Seconds | Visual | Purpose (psychological function)

**Sample-quality example:**

| Seconds | Visual | Purpose |
|:--------|:-------|:--------|
| 00-03 | Screenshot of negative comment: "Breaks after 1 day" with creator looking annoyed | Hook: Relatable objection creates curiosity |
| 03-07 | Hands dropping LARGE ice cubes + frozen berries into transparent cup | Build tension: "Can it really handle this?" |
| 07-10 | Close-up: LED display showing battery at 95% before starting | Trust: Tech credibility with real data |
| 10-15 | Blender upside down, ice crushing visible through transparent cup | Proof: Visual confirmation of power |
| 20-25 | Final smoothie texture shot (creamy, no chunks) | Result proof: Delivers on promise |

**Purpose categories (choose 1 per shot):**
- **Hook:** Attention/Relatability/Pattern Interrupt
- **Problem:** Pain amplification/Anchoring
- **Proof:** Evidence/Trust building/Demonstration
- **Objection Handling:** Removes barrier (noise, battery, cleaning)
- **Social Proof:** FOMO/Aspiration
- **Conversion:** CTA/Urgency

**Minimum:** 8-10 shots for 40-50s, each with clear psychological purpose
```

### Voiceover Sections

**See `templates/voiceover_format.md` for complete specification and all audio tags.**

**Critical requirements:**
- INLINE cues: `[emotion] Text.` on SAME LINE
- 1-2 audio tags per line (MANDATORY)
- Both German (DE) and Chinese (ZH) sections required
- Target length: 40-50s (100-150 German words, 130-180 Chinese characters)

### Script Naming Convention
```
Product_Model_KeyAngle.md   # e.g., HTC_NE20_AI_Uebersetzer_Earbuds.md
```

---

## Campaign Summary (Reference-Based - Included in Step 2-3)

**See `templates/campaign_summary_structure.md` for complete template.**

**Key Change from v1:** DO NOT duplicate content from analysis files. REFERENCE them.

**MANDATORY:** Use inline Chinese throughout (English text (中文翻译))

**Required sections:**
1. Product Overview | 产品概述
2. Campaign Strategy | 活动策略
3. Key Selling Points | 核心卖点
4. Target Audience | 目标受众
5. Scripts Summary | 脚本摘要
6. Production Notes | 制作说明
7. Source Files | 源文件

---

## Step 4: Quality Gate (Post-Write Validation)

```bash
product_id="{product_id}"
date="YYYYMMDD"
scripts_dir="product_list/$date/$product_id/scripts"

echo "=== QUALITY GATE: $product_id ==="

# Check script count (exclude Campaign_Summary.md)
script_count=$(ls -1 "$scripts_dir"/*.md 2>/dev/null | grep -v 'Campaign_Summary.md' | wc -l | tr -d ' ')
if [ "$script_count" -lt 3 ]; then
    echo "❌ FAIL: Only $script_count scripts (need 3)"
    exit 1
fi
echo "✅ Scripts: $script_count"

# Check Campaign Summary
if [ ! -f "$scripts_dir/Campaign_Summary.md" ]; then
    echo "❌ FAIL: Campaign_Summary.md missing"
    exit 1
fi
echo "✅ Campaign Summary exists"

# Check script quality (not stubs)
for script in "$scripts_dir"/*.md; do
    if [ "$(basename "$script")" = "Campaign_Summary.md" ]; then
        continue
    fi
    lines=$(wc -l < "$script" | tr -d ' ')
    if [ "$lines" -lt 40 ]; then
        echo "⚠️ WARNING: $(basename $script) may be a stub ($lines lines)"
    fi

    # Check for placeholder content
    if grep -q 'product: "Product"' "$script"; then
        echo "❌ FAIL: $(basename $script) has placeholder product name"
        exit 1
    fi
    if ! grep -q '### ZH' "$script"; then
        echo "❌ FAIL: $(basename $script) missing Chinese translation section"
        exit 1
    fi

    # Caption should use YAML block scalar so hashtags don't break YAML parsing
    if ! awk 'BEGIN{in=0} /^---$/{in=!in} in && /^caption: >-/{ok=1} END{exit !ok}' "$script"; then
        echo "⚠️ WARNING: $(basename $script) caption is not using 'caption: >-' (hashtags may break YAML)"
    fi
done
echo "✅ Script quality verified"

# CRITICAL: TikTok Policy Compliance Validation
echo ""
echo "=== TIKTOK POLICY COMPLIANCE CHECK ==="
echo "Validating scripts against TikTok advertising policies..."
compliance_fail=0
for script in "$scripts_dir"/*.md; do
    [[ "$(basename "$script")" == "Campaign_Summary.md" ]] && continue
    [[ -e "$script" ]] || continue

    if ! python3 scripts/validate_compliance_flags.py "$script" >/dev/null 2>&1; then
        echo "❌ FAIL: $(basename "$script") has compliance violations"
        echo "   Run: python3 scripts/validate_compliance_flags.py \"$script\""
        compliance_fail=1
    fi
done

if [ "$compliance_fail" -eq 1 ]; then
    echo ""
    echo "⚠️ COMPLIANCE VIOLATIONS DETECTED"
    echo "Fix violations before proceeding. See 'TikTok Policy Compliance' section for safe alternatives."
    exit 1
fi
echo "✅ All scripts pass TikTok policy compliance"

echo ""
echo "=== QUALITY GATE PASSED ==="
```

---

## Batch Processing (v2.3.0 Optimized)

**For multiple products, process sequentially with batched writes:**

```
Product A: [Read all files in parallel] → [Generate + Write 4 files in parallel] → [Gate] = 2-3 min
Product B: [Read all files in parallel] → [Generate + Write 4 files in parallel] → [Gate] = 2-3 min
Product C: [Read all files in parallel] → [Generate + Write 4 files in parallel] → [Gate] = 2-3 min
```

**Performance Improvement:**
- **Old (sequential writes):** 5-8 min per product × 8 products = 40-64 min
- **New (batched writes):** 2-3 min per product × 8 products = 16-24 min
- **Savings:** ~25-40 minutes for 8-product batch ⭐ **2x faster**

**Why sequential across products (not parallel)?**
- Claude Code produces better quality with focused attention
- Each product needs full context window for analysis
- Quality over speed for creative content
- BUT: We optimize WITHIN each product via batched writes

**Time estimate (v2.3.0):** ~2-3 minutes per product for script generation

---

## Common Mistakes to Avoid

### ❌ Mistake 1: **BROKEN LINE FORMAT (Most Common Error)**
**Symptoms:** Writing emotion cues on separate lines from text
```
[frustrated]
Du kennst das?
```
**Why it fails:** Validation script expects `[cue] Text.` on SAME LINE. Separate lines create "orphan" text without cues.
**Fix:** ALWAYS write inline: `[frustrated] Du kennst das?`
**Validation Error:** "Low cue density" / "No German voiceover section found"

### ❌ Mistake 2: Starting before analysis complete
**Fix:** Always run Step 0 Pre-Check first

### ❌ Mistake 3: Generic placeholder content
**Symptoms:** "You won't believe...", product="Product"
**Fix:** Read analysis files, use specific product details

### ❌ Mistake 4: Duplicating analysis content in Campaign Summary
**Fix:** Reference files with quotes, don't copy-paste

### ❌ Mistake 5: Missing ElevenLabs v3 markers
**Fix:** Every VO line needs [tone] marker at start (inline format)

### ❌ Mistake 6: Skipping Chinese translations
**Fix:** Chinese translation is mandatory for every script (DE + ZH sections required)

---

## File Structure After Completion

```
product_list/YYYYMMDD/{product_id}/
├── tabcut_data.json                    # From scraper
├── product_images/
│   ├── *.webp
│   └── image_analysis.md               # From analysis skill
├── ref_video/
│   ├── video_*.mp4
│   ├── video_*_analysis.md             # From analysis skill
│   └── video_synthesis.md              # From analysis skill (CRITICAL)
└── scripts/                            # FROM THIS SKILL (new workflow)
    ├── Product_Model_KeyAngle.md
    ├── Product_Model_KeyAngle.md
    ├── Product_Model_KeyAngle.md
    └── Campaign_Summary.md
```

---

## Integration with Other Skills

**Workflow order:**
1. `tiktok-product-scraper` → Product data + videos
2. `tiktok-product-analysis` → Image + video analysis (Gemini)
3. **`tiktok-script-generator`** → Scripts + summary (THIS SKILL - Claude)

**Handoff verification:**
```bash
# Before running this skill, verify:
date="YYYYMMDD"
ls product_list/$date/$product_id/ref_video/video_synthesis.md  # Must exist
```

---

**Version:** 2.3.0
**Last Updated:** 2026-01-31
**Changes from v2.2:**
- **MAJOR PERFORMANCE OPTIMIZATION:** Batched Write calls ⭐ **2x faster**
- Parallel Read tool calls (all analysis files fetched at once)
- Parallel Write tool calls (4 files written simultaneously in one message)
- Workflow reduced from 5 steps to 4 steps (Steps 2-3 merged)
- Time per product: 2-3 min (was 5-8 min)
- 8 products: 16-24 min (was 40-64 min)
- **Template extraction:** Moved frontmatter, voiceover format, and campaign summary to separate template files
- Added template references throughout skill for better maintainability
