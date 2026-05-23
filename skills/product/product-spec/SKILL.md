---
name: product-spec
description: Convert product briefs, websites, documents into structured product specs. Generates modular markdown files for landing pages, guides, marketing.
---

# Product Spec Generator

## Purpose

Transform unstructured product information into structured, modular specs that can generate:

- Landing pages
- Marketing copy
- User guides
- Sales materials

## Entry Points

```
/product-spec [url]         → Extract from website
/product-spec [brief]       → Convert brief to spec
/product-spec audit [slug]  → Audit existing spec
/product-spec update [slug] → Update specific module
```

## Data Location

- **Templates:** `data/products/_templates/`
- **Products:** `data/products/[slug]/`
- **Index:** `data/products/index.csv`

## Module Structure

| Module        | Purpose                         | Generates     |
| ------------- | ------------------------------- | ------------- |
| `core.md`     | Identity, problem, solution     | Hero, about   |
| `audience.md` | Personas, JTBD, pains           | Targeting     |
| `offer.md`    | Pricing, value stack, guarantee | Pricing cards |
| `copy.md`     | Headlines, hooks, CTAs          | Landing, ads  |
| `faq.md`      | Objections & responses          | FAQ sections  |
| `guide.md`    | How to use                      | User docs     |

---

## Process: Brief → Spec

### Phase 1: Extract Information

From input (brief, URL, document), identify:

```
IDENTITY
├── What is it? (type, name)
├── Who made it? (brand, creator)
└── What category? (workshop/course/membership/product)

PROBLEM
├── Surface pains (observable symptoms)
├── Root cause (deeper issue)
└── Cost of inaction (what happens if unsolved)

SOLUTION
├── Core approach (how you solve it)
├── Key mechanism (specific method)
└── Dream outcome (transformation)

AUDIENCE
├── Primary persona (who exactly)
├── Jobs to be done (functional/emotional/social)
├── Pains & gains (specific)
└── Triggers (when they buy)

OFFER
├── Price & model
├── What's included (value stack)
├── Delivery method
├── Guarantee
└── Scarcity/urgency

PROOF
├── Credentials
├── Results/metrics
└── Testimonials
```

### Phase 2: Ask Clarifying Questions

If information is missing, ask:

**Identity:**

- "Đây là loại gì? (workshop/course/membership/product)"
- "Target segment nào? (AI Office/Vibe Coder/both)"

**Problem:**

- "Vấn đề cụ thể họ đang gặp là gì?"
- "Nếu không giải quyết thì chuyện gì xảy ra?"

**Solution:**

- "Cách tiếp cận của bạn khác gì competitor?"
- "Kết quả cuối cùng (dream outcome) là gì?"

**Offer:**

- "Giá bao nhiêu? Model nào (one-time/monthly)?"
- "Có guarantee không? Loại nào?"

### Phase 3: Generate Modules

For each module, use template from `data/products/_templates/`

**Output:**

1. Create folder: `data/products/[slug]/`
2. Generate each module file
3. Update `data/products/index.csv`

---

## Process: URL → Spec

### Step 1: Fetch & Parse

```
WebFetch URL → Extract:
- Headlines, taglines
- Feature lists
- Pricing information
- Testimonials
- FAQ content
```

### Step 2: Map to Structure

```
Website Section → Module
─────────────────────────
Hero/Header    → core.md (one-liner, dream outcome)
About/Story    → core.md (problem, solution)
Features       → core.md (differentiators), offer.md (value stack)
Pricing        → offer.md (price, model, guarantee)
Testimonials   → copy.md (social proof)
FAQ            → faq.md
```

### Step 3: Fill Gaps

Ask user for missing information before generating.

---

## Quality Checklist

```
CORE.MD
□ One-liner is clear and benefit-focused?
□ Problem has surface + root + cost?
□ Solution has approach + mechanism + outcome?
□ Differentiators are specific, not generic?
□ Proof is verifiable?

AUDIENCE.MD
□ Persona is specific (not "everyone")?
□ JTBD covers functional/emotional/social?
□ Pains are real and ranked?
□ Triggers are actionable moments?
□ "Not for" is defined?

OFFER.MD
□ Value equation scored?
□ Value stack > 10x price perception?
□ Delivery method clear?
□ Guarantee matches product type?
□ Price anchoring included?

COPY.MD
□ Headlines are benefit-focused?
□ Hooks create tension/curiosity?
□ CTAs are action-oriented?
□ Social proof is specific?

FAQ.MD
□ Top objections addressed?
□ Root concerns identified?
□ Responses are conversational?
```

---

## Index CSV Format

```csv
slug,name,type,segment,price,currency,status,tagline,updated
premium-membership,Premium Membership,membership,ai-office,199000,VND/mo,active,"AI làm việc CHO bạn",2026-01-26
vip-membership,VIP Membership,membership,vibe-coder,349000,VND/mo,active,"Ship production products",2026-01-26
```

---

## Example: Brief → Spec

**Input:**

```
Tôi muốn tạo spec cho workshop AI Office Masterclass.
- 3 giờ, live
- Giá 399K
- Dành cho AI Office segment
- Học cách build AI workflow đầu tiên
- Có recording, templates, Q&A
```

**Output:**

Creates `data/products/ai-office-masterclass/`:

- `core.md` - Workshop identity, problem (manual AI usage), solution (workflow approach)
- `audience.md` - AI Office persona, pains (time wasted, no scaling)
- `offer.md` - 399K pricing, value stack (workshop + recording + templates)
- `copy.md` - Headlines, hooks for landing page
- `faq.md` - Common workshop objections

Updates `data/products/index.csv` with new row.

---

## Integration with Other Skills

**offer-creation:** Uses offer.md structure
**landing-page:** Pulls from all modules to generate page
**content-repurposing:** Uses copy.md for content variations

---

## Voice & Tone

When generating copy modules, follow brand voice:

- Personal (mình/bạn)
- Direct (no fluff)
- Practical (actionable)
- Mix Anh-Việt naturally

Avoid:

- Corporate speak
- Hype words
- Empty promises
