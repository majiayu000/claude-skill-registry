---
name: seo-2025-expert
description: Modern Search Engine Optimization with GEO, AI Overviews optimization, and industry-specific strategies for E-commerce, SaaS, Healthcare, Real Estate, Restaurant, Law Firm, Finance, Travel, and Education industries
---

# SEO 2025: Modern Search Optimization & GEO Expert

## Skill Overview

This skill enables Claude to provide expert guidance on **modern SEO in 2025**, with specialized focus on **Generative Engine Optimization (GEO)**, **AI Overviews (AIO)**, and comprehensive search strategy across traditional and emerging platforms.

---

## When This Skill Should Be Invoked

Claude should automatically invoke this skill when the user asks about:

- **SEO Strategy & Planning**: roadmaps, action plans, quarterly planning, competitive analysis
- **GEO & AI Overviews (Primary Focus)**: optimizing for AI Overviews, LLM visibility, being cited
- **Content Strategy**: topic clusters, E-E-A-T, information gain, AI-assisted content
- **Technical SEO**: Core Web Vitals (INP, LCP, CLS), schema markup, site architecture
- **Entity SEO & Knowledge Graph**: entity optimization, brand recognition
- **Off-Page & Authority**: link building, digital PR, brand signals
- **Local SEO**: Google Business Profile, reviews, citations
- **Specialized SEO**: Video, Image, Voice, International, E-commerce, Programmatic
- **Social & Alternative Platforms**: TikTok, Reddit, LinkedIn, Pinterest SEO
- **Measurement & Analytics**: KPIs, AI visibility tracking, dashboards
- **AI, Automation & Compliance**: AI content guidelines, spam policies

---

## PART 1: STEP-BY-STEP SEO IMPLEMENTATION GUIDES

### 1.1 Complete GEO/AIO Optimization Guide

**Goal**: Get your content cited in AI Overviews and LLM responses

#### Step 1: Audit Current AI Visibility (Week 1)

**Actions:**
1. Search your top 20 target keywords in Google
2. Note which queries trigger AI Overviews
3. Check if your domain appears in AIO citations
4. Test your brand in ChatGPT, Perplexity, and Gemini
5. Document baseline metrics

**Tools:**
- Free: Manual SERP checks, Semrush AI Visibility Checker (free tier)
- Paid: SE Ranking AI Overviews Tracker, Ahrefs Brand Radar

**Example Prompt for Testing:**
```
Ask ChatGPT: "What are the best [your product category] in [your location]?"
Ask Perplexity: "Compare [your brand] vs [competitor]"
```

#### Step 2: Content Structure for AI Citation (Week 2-3)

**Actions:**
1. Identify your top 10 pages by traffic
2. Restructure each page with Q&A format
3. Add direct answer paragraphs (20-40 words) after each H2
4. Convert lists to HTML tables where comparing items
5. Add FAQ sections with natural-language questions

**Before/After Example:**

**Before (Poor for AIO):**
```html
<h2>Our Services</h2>
<p>We offer many services including web design, SEO, and content marketing. 
Our team has years of experience helping businesses grow online...</p>
```

**After (Optimized for AIO):**
```html
<h2>What SEO Services Do You Offer?</h2>
<p><strong>We offer technical SEO audits, content optimization, link building, 
and local SEO services for businesses in Bangkok.</strong></p>
<p>Our technical SEO audits identify crawlability issues, Core Web Vitals 
problems, and indexation gaps. Content optimization includes keyword research, 
topic cluster development, and E-E-A-T enhancement...</p>
```

#### Step 3: Schema Markup Implementation (Week 3-4)

**Actions:**
1. Implement Article or BlogPosting schema on all content pages
2. Add FAQPage schema to pages with Q&A sections
3. Add HowTo schema to tutorial/guide content
4. Validate with Google's Rich Results Test

**FAQPage Schema Example:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is Generative Engine Optimization?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Generative Engine Optimization (GEO) is the practice of optimizing content so AI systems like Google AI Overviews, ChatGPT, and Perplexity can discover, understand, and cite your content in their responses."
    }
  }]
}
```

#### Step 4: Information Gain & E-E-A-T Enhancement (Week 4-6)

**Actions:**
1. Audit competitor content for your target keywords
2. Identify gaps—what information are they NOT providing?
3. Add unique data: surveys, case studies, expert quotes
4. Add author bios with credentials and photos
5. Include "Experience" signals: first-person narratives, process photos

**Information Gain Checklist:**
- [ ] Original data or statistics
- [ ] Expert quotes from named individuals
- [ ] Case studies with specific results
- [ ] Screenshots or process documentation
- [ ] Local/specific details competitors lack
- [ ] Updated information (dated within 6 months)

#### Step 5: Topic Cluster Development (Week 6-8)

**Actions:**
1. Choose 1 core topic for authority building
2. Create pillar page (3,000+ words, comprehensive)
3. Create 5-10 supporting articles (each targeting specific long-tail)
4. Internal link all spokes to hub with descriptive anchors
5. Update quarterly with fresh information

**Topic Cluster Example (Digital Marketing Agency):**

```
PILLAR: "Complete Guide to SEO in 2025" (3,500 words)
├── SPOKE 1: "How to Optimize for AI Overviews" (1,500 words)
├── SPOKE 2: "Core Web Vitals Optimization Guide" (1,800 words)
├── SPOKE 3: "E-E-A-T: Building Trust Signals" (1,200 words)
├── SPOKE 4: "Local SEO for Small Businesses" (1,500 words)
├── SPOKE 5: "Technical SEO Audit Checklist" (2,000 words)
├── SPOKE 6: "Link Building Strategies That Work" (1,400 words)
└── SPOKE 7: "SEO Tools Comparison 2025" (1,800 words)
```

---

### 1.2 Technical SEO Implementation Guide

**Goal**: Achieve "Good" Core Web Vitals and ensure crawlability

#### Step 1: Core Web Vitals Audit (Day 1-3)

**Actions:**
1. Run PageSpeed Insights on top 10 pages
2. Check Google Search Console Core Web Vitals report
3. Document current scores for INP, LCP, CLS
4. Identify pages failing thresholds

**2025 Thresholds:**
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| INP | < 200ms | 200-500ms | > 500ms |
| LCP | < 2.5s | 2.5-4.0s | > 4.0s |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |

#### Step 2: INP Optimization (Day 4-10)

**INP (Interaction to Next Paint)** measures responsiveness—how quickly the page responds to user interactions.

**Actions:**
1. Identify long tasks (> 50ms) in Chrome DevTools
2. Break up long JavaScript tasks
3. Defer non-critical JavaScript
4. Remove or optimize third-party scripts
5. Use web workers for heavy computations

**Quick Wins for INP:**
```javascript
// Before: Blocking script
<script src="analytics.js"></script>

// After: Deferred script
<script src="analytics.js" defer></script>
```

#### Step 3: LCP Optimization (Day 11-17)

**LCP (Largest Contentful Paint)** measures loading—when the main content becomes visible.

**Actions:**
1. Identify LCP element (usually hero image or H1)
2. Preload LCP image
3. Optimize image format (WebP/AVIF)
4. Use CDN for faster delivery
5. Minimize server response time (TTFB < 800ms)

**Preload LCP Image:**
```html
<head>
  <link rel="preload" as="image" href="hero-image.webp">
</head>
```

#### Step 4: CLS Optimization (Day 18-21)

**CLS (Cumulative Layout Shift)** measures visual stability—preventing unexpected layout jumps.

**Actions:**
1. Set explicit width/height on images and videos
2. Reserve space for ads and embeds
3. Avoid inserting content above existing content
4. Use font-display: swap for web fonts
5. Avoid animations that trigger layout changes

**Image with Dimensions:**
```html
<!-- Before: No dimensions (causes CLS) -->
<img src="product.jpg" alt="Product">

<!-- After: Explicit dimensions (prevents CLS) -->
<img src="product.jpg" alt="Product" width="800" height="600">
```

#### Step 5: Crawlability & Indexation (Day 22-30)

**Actions:**
1. Submit XML sitemap to Google Search Console
2. Check robots.txt for accidental blocks
3. Fix crawl errors in Search Console
4. Ensure internal links reach all important pages
5. Check for orphan pages (no internal links)

**Robots.txt Best Practice:**
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /checkout/
Sitemap: https://example.com/sitemap.xml
```

---

### 1.3 Local SEO Implementation Guide

**Goal**: Dominate local search and Google Maps

#### Step 1: Google Business Profile Setup (Day 1-3)

**Actions:**
1. Claim or create Google Business Profile
2. Verify ownership (postcard, phone, or email)
3. Select correct primary category
4. Add all secondary categories that apply
5. Complete every field in the profile

**GBP Completion Checklist:**
- [ ] Business name (exactly as on signage)
- [ ] Address (match website exactly)
- [ ] Phone number (local number preferred)
- [ ] Website URL
- [ ] Business hours (including special hours)
- [ ] Business description (750 characters, include keywords)
- [ ] Services/Products list
- [ ] Attributes (accessibility, amenities, etc.)
- [ ] Photos (exterior, interior, team, products)

#### Step 2: Photo & Media Optimization (Day 4-7)

**Actions:**
1. Upload 10+ high-quality photos
2. Add photos in each category (exterior, interior, team, products)
3. Geo-tag photos with location metadata
4. Add short videos (30-60 seconds)
5. Update photos monthly

**Photo Categories:**
- Exterior: 3+ photos from different angles
- Interior: 5+ photos showing atmosphere
- Team: Staff photos build trust
- Products/Services: Show what you offer
- Logo and cover photo

#### Step 3: Review Generation System (Ongoing)

**Actions:**
1. Create review request email/SMS template
2. Set up automated follow-up 24-48 hours post-service
3. Respond to ALL reviews within 24 hours
4. Address negative reviews professionally
5. Target 1-5 new reviews per month

**Review Request Template:**
```
Hi [Name],

Thank you for choosing [Business Name]! We hope you had a great experience.

If you have a moment, we'd love to hear your feedback on Google. Your review 
helps us serve you better and helps others find us.

[Direct Google Review Link]

Thank you!
[Your Name]
```

**Review Response Template (Positive):**
```
Thank you so much, [Name]! We're thrilled you enjoyed your [service/product]. 
Your support means the world to our team. We look forward to seeing you again soon!
```

**Review Response Template (Negative):**
```
Hi [Name], thank you for your feedback. We're sorry your experience didn't 
meet expectations. We'd love to make this right—please contact us at 
[email/phone] so we can discuss how to resolve this.
```

#### Step 4: Local Content Strategy (Week 2-4)

**Actions:**
1. Create location-specific landing pages
2. Write neighborhood guides
3. Cover local events and news
4. Create "Best of [Location]" content
5. Add LocalBusiness schema to all local pages

**Local Page Template:**
```
URL: /services/[service]-[city]/

H1: [Service] in [City] | [Business Name]

Content Structure:
- Service overview (200 words)
- Why choose us in [City] (150 words)
- Service area map
- Local testimonials
- FAQ specific to location
- Contact info with embedded map
```

---

### 1.4 Content Creation Workflow

**Goal**: Create SEO content that ranks AND gets cited by AI

#### Step 1: Keyword Research (Day 1-2)

**Actions:**
1. Brainstorm seed keywords
2. Expand with tools (Ahrefs, Semrush, or free: Ubersuggest)
3. Analyze search intent for each keyword
4. Check keyword difficulty vs domain authority
5. Prioritize by business value × achievability

**Keyword Prioritization Matrix:**
| Priority | Criteria |
|----------|----------|
| P1 (High) | High intent + Low difficulty + High volume |
| P2 (Medium) | High intent + Medium difficulty |
| P3 (Lower) | Low intent OR High difficulty |

#### Step 2: SERP Analysis (Day 2-3)

**Actions:**
1. Search target keyword in incognito
2. Note if AI Overview appears
3. Analyze top 5 results for content structure
4. Identify content gaps (what's missing?)
5. Note featured snippets and PAA questions

**SERP Analysis Checklist:**
- [ ] AI Overview present? What sources cited?
- [ ] Featured snippet format (paragraph, list, table)?
- [ ] People Also Ask questions (note top 5)
- [ ] Top results word count (estimate)
- [ ] Top results content structure (H2s, H3s)
- [ ] What's missing from all top results?

#### Step 3: Content Brief Creation (Day 3-4)

**Content Brief Template:**
```
TARGET KEYWORD: [Primary keyword]
SECONDARY KEYWORDS: [3-5 related terms]
SEARCH INTENT: [Informational/Commercial/Transactional]
WORD COUNT TARGET: [Based on SERP analysis]
CONTENT TYPE: [Guide/Comparison/How-to/List]

OUTLINE:
H1: [Include primary keyword]
  - Introduction (answer query in first 100 words)
  
H2: [Section 1 - target secondary keyword]
  - Direct answer paragraph (20-40 words)
  - Supporting details
  
H2: [Section 2]
  ...

H2: FAQ Section
  - Q: [PAA question 1]
  - Q: [PAA question 2]
  - Q: [PAA question 3]

REQUIRED ELEMENTS:
- [ ] Original data/statistic
- [ ] Expert quote
- [ ] Comparison table
- [ ] Internal links to: [list pages]
- [ ] External links to: [authoritative sources]
- [ ] Images with alt text
- [ ] Schema markup type: [Article/HowTo/FAQ]

E-E-A-T REQUIREMENTS:
- Author: [Name with credentials]
- Experience signal: [First-person narrative/case study]
- Sources to cite: [List authoritative sources]
```

#### Step 4: Content Writing (Day 4-7)

**Writing Guidelines:**
1. Answer the query in the first 100 words
2. Use the "inverted pyramid" structure
3. Write at 8th-grade reading level
4. Break up text with headers every 300 words
5. Use bullet points and tables for scanability
6. Include original insights, not just summarized SERP content

**AI-Assisted Writing Best Practice:**
```
DO:
- Use AI for research and outline creation
- Use AI to generate first drafts
- Always edit for accuracy and voice
- Add personal experience and examples
- Fact-check all AI-generated claims

DON'T:
- Publish unedited AI content
- Use AI for YMYL topics without expert review
- Scale content without quality control
- Copy AI output verbatim
```

#### Step 5: On-Page Optimization (Day 7-8)

**On-Page Checklist:**
- [ ] Title tag: Primary keyword + compelling hook (50-60 chars)
- [ ] Meta description: Include keyword + CTA (150-160 chars)
- [ ] URL: Short, keyword-rich, hyphen-separated
- [ ] H1: Matches title tag intent, includes keyword
- [ ] H2s: Include secondary keywords naturally
- [ ] First paragraph: Answer query directly
- [ ] Images: Compressed, WebP format, descriptive alt text
- [ ] Internal links: 3-5 relevant internal links
- [ ] External links: 2-3 authoritative sources
- [ ] Schema: Implement appropriate structured data

---

## PART 2: INDUSTRY-SPECIFIC SEO BEST PRACTICES

### 2.1 E-Commerce SEO

**Unique Challenges:**
- Large number of product pages
- Duplicate content from manufacturer descriptions
- Faceted navigation creating crawl bloat
- Out-of-stock page management

**Priority Actions:**

**Product Page Optimization:**
```
Title: [Brand] [Product Name] - [Key Feature] | [Store Name]
Example: Nike Air Max 90 - Men's Running Shoes | SneakerStore

URL: /category/brand-product-name/
Example: /mens-shoes/nike-air-max-90/

Required Elements:
- Unique product description (150+ words)
- High-quality images (multiple angles)
- Product schema with price, availability, reviews
- Customer reviews section
- Related products internal links
- Clear CTA button
```

**Category Page Strategy:**
- Add 200-300 words of unique content above or below product grid
- Include FAQ section targeting long-tail queries
- Implement breadcrumb navigation
- Use canonical tags for filtered views
- Target category-level keywords (higher volume)

**Schema Markup (Product):**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Nike Air Max 90",
  "image": "https://example.com/nike-air-max-90.jpg",
  "description": "Classic Nike Air Max 90 running shoes...",
  "brand": {"@type": "Brand", "name": "Nike"},
  "offers": {
    "@type": "Offer",
    "price": "129.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "127"
  }
}
```

**E-Commerce KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Organic revenue | +20% YoY | GA4 |
| Category page rankings | Top 10 | Rank tracker |
| Product rich results | 80%+ eligible | GSC |
| Crawl efficiency | < 5% crawl waste | Log analysis |

---

### 2.2 B2B SaaS SEO

**Unique Challenges:**
- Long sales cycles (multiple stakeholders)
- Technical topics requiring expertise
- Competition from well-funded competitors
- Need to capture leads, not just traffic

**Priority Actions:**

**Content Strategy by Funnel Stage:**

```
TOP OF FUNNEL (Awareness):
- "What is [problem]?" educational content
- Industry trend reports
- Beginner guides
- Glossary pages
Target: High-volume, informational keywords

MIDDLE OF FUNNEL (Consideration):
- "How to solve [problem]" guides
- Comparison pages ([Your Product] vs [Competitor])
- Use case pages
- ROI calculators
Target: Commercial investigation keywords

BOTTOM OF FUNNEL (Decision):
- Pricing pages
- Case studies with specific results
- Demo/trial landing pages
- Integration pages
Target: High-intent, transactional keywords
```

**Comparison Page Template:**
```
URL: /compare/[your-product]-vs-[competitor]/

H1: [Your Product] vs [Competitor]: Complete 2025 Comparison

Structure:
- Quick verdict summary (50 words)
- Comparison table (features, pricing, ratings)
- Detailed feature-by-feature breakdown
- Use case recommendations
- FAQ section
- CTA to free trial

Best Practice:
- Be honest about competitor strengths
- Include real pricing (if public)
- Update quarterly
```

**B2B SaaS Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Your SaaS Product",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "offers": {
    "@type": "Offer",
    "price": "49",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "523"
  }
}
```

**B2B SaaS KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Demo requests from organic | Track monthly | CRM + GA4 |
| Comparison page rankings | Position 1-3 | Rank tracker |
| Feature snippet wins | 20%+ of targets | Semrush |
| Pipeline from organic | Track attribution | CRM |

---

### 2.3 Healthcare & Medical SEO (YMYL)

**Unique Challenges:**
- Extremely high E-E-A-T requirements
- YMYL (Your Money Your Life) scrutiny
- Medical accuracy requirements
- HIPAA compliance considerations
- Competition from WebMD, Mayo Clinic, etc.

**Priority Actions:**

**E-E-A-T Implementation for Healthcare:**

```
REQUIRED AUTHOR CREDENTIALS:
- Medical degree (MD, DO, NP, PA)
- Current license and practice location
- Professional headshot
- Bio with credentials and experience
- Links to medical board verification

CONTENT REVIEW PROCESS:
1. Medical professional writes or reviews
2. Include medical disclaimer
3. Cite peer-reviewed sources
4. Update with latest guidelines
5. Include "Last reviewed by [Doctor] on [Date]"

PAGE ELEMENTS:
- Author box with credentials
- Medical reviewer box
- Last updated/reviewed date
- Citations to medical journals
- Medical disclaimer
- Emergency contact information (if relevant)
```

**Medical Content Template:**
```
H1: [Condition/Treatment]: Symptoms, Causes, and Treatment Options

Medical Disclaimer Box:
"This information is for educational purposes only and is not a substitute 
for professional medical advice. Always consult your healthcare provider."

Author Box:
Written by: [Name], [Credentials]
Medically reviewed by: Dr. [Name], [Specialty]
Last updated: [Date]

Content Structure:
- Overview (what is this condition?)
- Symptoms (bullet list)
- Causes and risk factors
- Diagnosis
- Treatment options
- When to see a doctor
- FAQ
- Sources (peer-reviewed journals)
```

**Healthcare Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "MedicalWebPage",
  "about": {
    "@type": "MedicalCondition",
    "name": "Type 2 Diabetes"
  },
  "lastReviewed": "2025-01-15",
  "reviewedBy": {
    "@type": "Person",
    "name": "Dr. Jane Smith",
    "jobTitle": "Endocrinologist"
  }
}
```

**Healthcare KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Medical accuracy | 100% (mandatory) | Expert review |
| E-E-A-T signals | All pages compliant | Manual audit |
| Patient appointment requests | Track by page | Call tracking |
| Local pack visibility | Top 3 | Local rank tracker |

---

### 2.4 Real Estate SEO

**Unique Challenges:**
- Competition from Zillow, Realtor.com, Redfin
- Hyper-local targeting needs
- Rapidly changing inventory
- IDX/MLS duplicate content issues

**Priority Actions:**

**Neighborhood Page Strategy:**
```
URL: /neighborhoods/[neighborhood-name]/

H1: [Neighborhood] Real Estate | Homes for Sale in [Neighborhood]

Content Structure:
- Neighborhood overview (200 words)
- Current market stats (median price, days on market)
- Schools information
- Amenities and lifestyle
- Transportation/commute info
- Featured listings (dynamic)
- Agent CTA

Unique Content Ideas:
- Local restaurant recommendations
- Best streets to live on
- Hidden gems only locals know
- Market trend analysis
- Video neighborhood tour
```

**Property Listing Optimization:**
```
Title: [Address] - [Beds]BR/[Baths]BA [Type] for Sale in [Neighborhood]
Example: 123 Oak Street - 4BR/3BA Single Family Home for Sale in Westwood

Description Guidelines:
- UNIQUE description (not MLS copy-paste)
- 200+ words per listing
- Highlight unique features
- Include neighborhood benefits
- Natural keyword usage

Image Optimization:
- High-quality photos (compressed)
- Alt text: "Living room at 123 Oak Street, Westwood"
- Image sitemap submission
```

**Real Estate Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateListing",
  "name": "4BR Home in Westwood",
  "url": "https://example.com/listings/123-oak-street",
  "datePosted": "2025-01-15",
  "offers": {
    "@type": "Offer",
    "price": "850000",
    "priceCurrency": "USD"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Oak Street",
    "addressLocality": "Los Angeles",
    "addressRegion": "CA"
  }
}
```

**Real Estate KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Neighborhood page rankings | Top 5 | Rank tracker |
| Lead form submissions | Track by page | GA4 |
| Listing page indexation | 95%+ | GSC |
| Local pack visibility | Top 3 | Local tracker |

---

### 2.5 Restaurant & Hospitality SEO

**Unique Challenges:**
- Extreme local competition
- Review dependency
- Mobile-first audience
- Seasonal fluctuations

**Priority Actions:**

**Google Business Profile Optimization:**
```
CRITICAL FIELDS:
- Primary category: Be specific (e.g., "Thai Restaurant" not "Restaurant")
- Menu link: Direct link to online menu
- Reservation link: Direct booking URL
- Order link: Online ordering URL
- Attributes: Dine-in, takeout, delivery, outdoor seating

PHOTO STRATEGY:
- Food photos: 20+ high-quality dish photos
- Interior: 5+ atmosphere photos
- Exterior: 3+ photos (helps customers find you)
- Team: Staff photos build trust
- Update monthly with new photos

POSTS:
- Post 2-3x per week
- Promote specials, events, new menu items
- Include photos and CTAs
```

**Menu SEO:**
```
URL: /menu/

On-Page Optimization:
- HTML text menu (not just PDF/image)
- Schema markup for each item
- Prices included
- Descriptions with keywords
- Dietary labels (vegan, gluten-free)

Menu Schema:
{
  "@type": "Menu",
  "hasMenuSection": [{
    "@type": "MenuSection",
    "name": "Appetizers",
    "hasMenuItem": [{
      "@type": "MenuItem",
      "name": "Spring Rolls",
      "description": "Crispy vegetable spring rolls with sweet chili sauce",
      "offers": {
        "@type": "Offer",
        "price": "8.95"
      }
    }]
  }]
}
```

**Review Strategy:**
```
REVIEW ACQUISITION:
- Table tent with QR code to Google review
- Follow-up email 2 hours after reservation
- Train staff to mention reviews
- Target: 5-10 new reviews per month

REVIEW RESPONSE TEMPLATES:

5-Star:
"Thank you, [Name]! We're so glad you enjoyed the [dish mentioned]. 
Our chef puts so much love into every plate. See you again soon!"

3-Star:
"Hi [Name], thank you for your honest feedback. We'd love to hear more 
about how we can improve. Please reach out to [email] so we can make 
your next visit exceptional."

1-Star:
"We're sorry your experience didn't meet expectations, [Name]. This 
isn't the standard we hold ourselves to. Please contact our manager 
at [phone] so we can make this right."
```

**Restaurant KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Google Maps views | +30% YoY | GBP Insights |
| Direction requests | Track weekly | GBP Insights |
| Review rating | 4.5+ stars | GBP |
| Review velocity | 5-10/month | GBP |

---

### 2.6 Law Firm SEO (YMYL)

**Unique Challenges:**
- Extremely competitive keywords
- High E-E-A-T requirements
- Location-specific targeting
- Strict advertising regulations
- Long-tail, question-based searches

**Priority Actions:**

**Practice Area Page Template:**
```
URL: /practice-areas/[practice-area]/

H1: [Practice Area] Lawyer in [City] | [Firm Name]
Example: Personal Injury Lawyer in Houston | Smith & Associates

Content Structure (2,000+ words):
- Overview of practice area
- Types of cases handled
- Legal process explained
- Why choose our firm
- Attorney profiles for this practice
- Case results (if permitted)
- FAQ section
- Contact CTA

Required Elements:
- Attorney credentials and bar numbers
- Case results disclaimer
- Consultation CTA
- Location-specific content
- Client testimonials (with permission)
```

**Legal Content E-E-A-T:**
```
AUTHOR REQUIREMENTS:
- Licensed attorney in relevant jurisdiction
- Bar number and status link
- Professional headshot
- Detailed bio with experience
- Speaking/publication credentials

CONTENT STANDARDS:
- Cite relevant statutes and case law
- Include jurisdiction-specific information
- Add legal disclaimer
- Update when laws change
- Include "This is not legal advice" disclaimer
```

**Legal Services Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "name": "Smith & Associates Personal Injury Law",
  "priceRange": "Free Consultation",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "Houston",
    "addressRegion": "TX"
  },
  "areaServed": {
    "@type": "City",
    "name": "Houston"
  }
}
```

**Law Firm KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Consultation requests | Track by practice area | Call tracking |
| Practice area rankings | Top 5 local | Rank tracker |
| Featured snippet wins | 30%+ of FAQ queries | Semrush |
| GBP conversion actions | Track weekly | GBP Insights |

---

### 2.7 Finance & Fintech SEO (YMYL)

**Unique Challenges:**
- Highest E-E-A-T scrutiny (YMYL)
- Regulatory compliance requirements
- Trust is paramount
- Competition from established banks

**Priority Actions:**

**Financial Content E-E-A-T:**
```
AUTHOR REQUIREMENTS:
- Certified financial professional (CFP, CFA, CPA)
- Credentials verifiable via official registries
- Professional experience in finance
- Disclosure of any conflicts of interest

CONTENT STANDARDS:
- Cite official sources (SEC, IRS, Federal Reserve)
- Include risk disclaimers
- Update with regulatory changes
- Fact-check all financial data
- Include publication and update dates
```

**Financial Services Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "FinancialService",
  "name": "XYZ Investment Advisors",
  "description": "SEC-registered investment advisory firm...",
  "areaServed": "United States",
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "SEC Registered Investment Advisor"
  }
}
```

**Fintech Landing Page Template:**
```
URL: /solutions/[solution-type]/

H1: [Solution] for [Target Audience] | [Company Name]

Trust Signals Required:
- Security certifications (SOC 2, PCI-DSS)
- Regulatory compliance badges
- Partner logos (banks, payment processors)
- Customer testimonials from known companies
- Press mentions from financial publications

Content Structure:
- Problem statement
- Solution overview
- How it works (with visuals)
- Security and compliance
- Pricing transparency
- Customer success stories
- FAQ
- Demo CTA
```

**Finance KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Compliance accuracy | 100% | Legal review |
| Trust signals per page | 5+ elements | Manual audit |
| Lead quality score | Track MQL rate | CRM |
| Organic conversion rate | Benchmark vs paid | GA4 |

---

### 2.8 Travel & Tourism SEO

**Unique Challenges:**
- Seasonal search patterns
- Competition from OTAs (Booking.com, Expedia)
- Visual content importance
- Voice search for travel queries

**Priority Actions:**

**Destination Page Template:**
```
URL: /destinations/[destination]/

H1: [Destination] Travel Guide: Things to Do & Best Time to Visit

Content Structure:
- Destination overview (300 words)
- Best time to visit
- Top attractions (with schema)
- Where to stay
- Getting around
- Local food guide
- Insider tips
- Interactive map
- Related tours/experiences

Visual Requirements:
- Hero video or image
- Photo gallery (10+ images)
- Interactive map
- Infographic (best times, costs)
```

**Tour/Experience Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "TouristTrip",
  "name": "Bangkok Street Food Tour",
  "description": "4-hour guided tour of Bangkok's best street food...",
  "touristType": "Food & Drink",
  "itinerary": {
    "@type": "ItemList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Chinatown Market"},
      {"@type": "ListItem", "position": 2, "name": "Flower Market"}
    ]
  },
  "offers": {
    "@type": "Offer",
    "price": "75",
    "priceCurrency": "USD"
  }
}
```

**Voice Search Optimization:**
```
Target conversational queries:
- "What's the best time to visit [destination]?"
- "How do I get from [airport] to [city center]?"
- "What are the top restaurants near [attraction]?"

Content Format:
- Direct answer in first sentence
- Structured with headers
- FAQ schema markup
- Speakable schema for voice assistants
```

**Travel KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Destination page rankings | Top 10 | Rank tracker |
| Booking conversions | Track by page | GA4 |
| Featured snippets | 40%+ of travel queries | Semrush |
| Video views | Track YouTube analytics | YouTube Studio |

---

### 2.9 Education & Online Courses SEO

**Unique Challenges:**
- Competition from Coursera, Udemy, etc.
- Trust requirements for educators
- Long-tail keyword opportunities
- Course discovery challenges

**Priority Actions:**

**Course Page Template:**
```
URL: /courses/[course-name]/

H1: [Course Name]: [Key Outcome] | [Platform/Instructor]
Example: Python for Data Science: Master Analytics in 8 Weeks | DataMasters

Required Elements:
- Course description (unique, 300+ words)
- Learning outcomes (bullet list)
- Curriculum/syllabus (expandable sections)
- Instructor bio with credentials
- Student testimonials
- Course preview (video)
- FAQs
- Enrollment CTA

Trust Signals:
- Instructor credentials and experience
- Number of students enrolled
- Completion rate
- Average rating and review count
- Certification details
```

**Course Schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Python for Data Science",
  "description": "Comprehensive 8-week course covering...",
  "provider": {
    "@type": "Organization",
    "name": "DataMasters"
  },
  "instructor": {
    "@type": "Person",
    "name": "Dr. Jane Smith",
    "jobTitle": "Senior Data Scientist"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "online",
    "courseWorkload": "PT8W"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "2341"
  }
}
```

**Educational Blog Strategy:**
```
Content Funnel:

AWARENESS (Target beginners):
- "What is [topic]?"
- "[Topic] for beginners"
- "How to get started with [skill]"

CONSIDERATION (Target learners):
- "Best [topic] courses 2025"
- "[Course A] vs [Course B]"
- "How long to learn [skill]?"

DECISION (Target enrollers):
- "[Your Course] review"
- "[Your Course] syllabus"
- "Is [Your Course] worth it?"
```

**Education KPIs:**
| Metric | Target | Tool |
|--------|--------|------|
| Course page rankings | Top 10 | Rank tracker |
| Enrollment from organic | Track monthly | GA4 |
| Course rich results | 80%+ eligible | GSC |
| Student testimonials | 10+ per course | Manual |

---

## PART 3: MEASUREMENT FRAMEWORKS

### 3.1 Weekly SEO Dashboard Metrics

**Track Every Week:**
| Metric | Tool | Action Threshold |
|--------|------|------------------|
| Organic sessions | GA4 | < 10% WoW decline |
| AI referral traffic | GA4 (custom) | Track trend |
| Impressions | GSC | < 15% WoW decline |
| Average position | GSC | Track movement |
| Core Web Vitals status | GSC | Any "Poor" pages |
| Index coverage issues | GSC | Any new errors |

### 3.2 Monthly SEO Report Metrics

**Track Monthly:**
| Metric | Tool | Target |
|--------|------|--------|
| Organic conversions | GA4 | +10% MoM |
| Keyword rankings (top 10) | Rank tracker | +5 keywords |
| AIO Share of Voice | AI tracker | Improving trend |
| Backlinks acquired | Ahrefs/Semrush | 10+ quality |
| Brand search volume | Keyword tool | +5% MoM |
| Review count/rating | GBP | 5+ new reviews |

### 3.3 Quarterly SEO Review Metrics

**Track Quarterly:**
| Metric | Tool | Target |
|--------|------|--------|
| Organic traffic YoY | GA4 | +20% |
| Revenue from organic | GA4 | +20% |
| Domain authority | Ahrefs/Moz | +2 points |
| Content published | CMS | vs plan |
| Technical debt | Audit tool | Decreasing |

---

## PART 4: QUICK REFERENCE CHECKLISTS

### 4.1 New Page Launch Checklist

- [ ] Keyword research completed
- [ ] SERP analysis completed
- [ ] Content brief created
- [ ] Content written and edited
- [ ] Title tag optimized (50-60 chars)
- [ ] Meta description written (150-160 chars)
- [ ] URL is short and keyword-rich
- [ ] H1 includes primary keyword
- [ ] Images compressed and alt text added
- [ ] Internal links added (3-5)
- [ ] External links to authoritative sources (2-3)
- [ ] Schema markup implemented
- [ ] Mobile preview checked
- [ ] Page speed tested
- [ ] Published and submitted to GSC

### 4.2 Monthly SEO Maintenance Checklist

- [ ] Check GSC for new crawl errors
- [ ] Review Core Web Vitals report
- [ ] Check for index coverage issues
- [ ] Review top declining pages
- [ ] Update 2-3 older articles
- [ ] Respond to all new reviews
- [ ] Post to Google Business Profile
- [ ] Check for broken links
- [ ] Review competitor rankings
- [ ] Document wins and learnings

### 4.3 Content Refresh Checklist

- [ ] Update statistics and data
- [ ] Check all links still work
- [ ] Add new sections if needed
- [ ] Update screenshots/images
- [ ] Refresh publish date
- [ ] Re-optimize for new keywords
- [ ] Add FAQ if missing
- [ ] Check schema is still valid
- [ ] Submit updated URL to GSC
- [ ] Promote refreshed content

---

## PART 5: EXAMPLE SCENARIOS

### Scenario 1: New E-commerce Store Launch

**Situation:** Launching a new online store selling sustainable fashion

**90-Day Action Plan:**

**Month 1: Foundation**
- Week 1-2: Technical setup (sitemap, schema, speed optimization)
- Week 3: Category page optimization (top 5 categories)
- Week 4: Product page template optimization

**Month 2: Content**
- Week 5-6: Launch blog with 4 pillar articles
- Week 7: Create size guide and sustainability pages
- Week 8: Build FAQ pages for top product categories

**Month 3: Authority**
- Week 9-10: Digital PR outreach (sustainable fashion angle)
- Week 11: Guest posts on fashion blogs
- Week 12: Review and optimize based on data

**Expected Results:**
- 50+ pages indexed
- 10+ keywords in top 50
- 500+ organic sessions/month by month 3

---

### Scenario 2: Local Business Struggling with Reviews

**Situation:** Restaurant with 3.8 star rating, only 23 reviews

**60-Day Action Plan:**

**Week 1-2: Audit**
- Respond to ALL existing reviews
- Analyze negative review themes
- Set up review monitoring

**Week 3-4: Systems**
- Create review request email sequence
- Train staff on review process
- Set up table tent QR codes

**Week 5-8: Execution**
- Email past customers (last 6 months)
- Follow up 24 hours after reservations
- Track weekly progress

**Expected Results:**
- 30+ new reviews in 60 days
- Rating improved to 4.3+
- Local pack visibility improved

---

### Scenario 3: B2B SaaS Not Appearing in AI Overviews

**Situation:** Project management SaaS not cited in AI responses for target queries

**90-Day GEO Action Plan:**

**Month 1: Audit & Structure**
- Identify 20 queries that trigger AIO
- Restructure top pages with Q&A format
- Implement Article and FAQ schema

**Month 2: Content Depth**
- Create comprehensive comparison pages
- Add original data (user survey)
- Build topic cluster around core feature

**Month 3: Authority**
- Digital PR for data study
- Guest posts on productivity blogs
- Update all competitor comparison pages

**Expected Results:**
- AIO citations for 3-5 target queries
- Brand mentioned in ChatGPT/Perplexity
- 20%+ increase in branded search

---

## PART 6: KEY SEO FRAMEWORKS

### Four Core Pillars of Modern SEO
1. **GEO/AIO Readiness**: Optimize to be discovered and cited by AI
2. **On-Page & Content**: Information-dense, E-E-A-T-strong content
3. **Technical & UX**: Fast, accessible, crawlable sites
4. **Authority & Trust**: Links, brand signals, and reputation

### Three Strategic Tracks (90-Day Action Plan)
1. **Track 1**: "Be the Answer" (GEO & Content)
2. **Track 2**: "Speed & Access" (Technical & UX)
3. **Track 3**: "Verify Expertise" (E-E-A-T & Trust)

### 2025 Success Metrics Framework
- **AI Visibility Metrics**: AIO Share of Voice, AI Referral Traffic, Brand Mentions
- **Zero-Click Metrics**: SERP Feature Share, Impression-to-Click Ratio
- **Brand Authority**: Brand Search Volume, Share of Search
- **Technical**: Core Web Vitals (INP < 200ms)
- **Traditional**: Organic Traffic, Rankings, CTR, Backlinks
- **Local**: GBP Performance, Review Metrics

### Quick Reference: Key 2025 SEO Shifts

| Old (Pre-2024) | New (2025) |
|---|---|
| "How do I rank #1?" | "How do I get cited in AI Overviews?" |
| "Keywords are king" | "Entities and intent are king" |
| "More content wins" | "Better information gain wins" |
| "Links are the only authority signal" | "Links + brand mentions + E-E-A-T win" |
| "Google-only focus" | "Multi-platform visibility (6+ platforms)" |
| "Track rankings" | "Track AI visibility, zero-click share, brand search" |
| "SEO for websites" | "SEO for AI discovery + websites + social + apps" |
| "Thin content scales" | "Quality content scales; thin content is spam" |

---

## PART 7: VERSION & UPDATES

**Skill Version:** 2.0 (December 2025)
**Last Updated:** December 04, 2025
**SEO Standards:** 2025 Best Practices
**Reference Base:** 200+ current sources
**Next Review:** Q2 2026

### Changelog

**v2.0 (December 2025):**
- Added step-by-step implementation guides
- Added 9 industry-specific best practice sections
- Added detailed checklists and templates
- Added example scenarios with action plans
- Added schema markup examples for each industry
- Added measurement frameworks by timeframe

**v1.0 (December 2025):**
- Initial skill creation
- Core GEO/AIO guidance
- Basic framework structures

---

**End of SKILL.md**
