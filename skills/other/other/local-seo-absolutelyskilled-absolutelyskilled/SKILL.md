---
name: local-seo
version: 0.1.0
description: >
  Use this skill when optimizing for local search results - Google Business Profile
  management, local citations, NAP consistency, local schema markup (LocalBusiness),
  review management, local pack optimization, and geo-targeted content. Triggers on
  any task involving local search visibility, map pack rankings, multi-location SEO,
  or local business online presence.
category: marketing
tags: [seo, local-seo, google-business-profile, citations, local-pack, reviews]
recommended_skills: [seo-mastery, link-building, geo-optimization, schema-markup]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Local SEO

Local SEO is the practice of optimizing a business's online presence to attract
customers from geographically relevant searches. Unlike traditional SEO, which
targets broad organic rankings, local SEO focuses on appearing in Google's Local
Pack (the map results block), Google Maps, and location-based organic results.
It is critical for any business serving customers in a physical location or a
defined service area - restaurants, law firms, plumbers, retail stores, medical
practices, and multi-location franchises all depend on local search visibility
to drive foot traffic and phone calls.

---

## When to use this skill

Trigger this skill when the user:
- Wants to set up or optimize a Google Business Profile (GBP)
- Needs to audit or fix NAP (Name, Address, Phone) consistency across the web
- Asks how to rank higher in Google Maps or the local pack
- Wants to implement LocalBusiness schema markup on a website
- Needs a review generation or reputation management strategy
- Is managing SEO for multiple business locations
- Wants to optimize for "near me" or service-area searches
- Asks about local citations - building, auditing, or cleaning up duplicates

Do NOT trigger this skill for:
- Broad keyword research or national/global SEO (use `seo-mastery` instead)
- Technical site performance issues like Core Web Vitals (use `technical-seo-engineering`)

---

## Key principles

1. **Google Business Profile is the foundation** - GBP is the single most impactful
   lever in local SEO. A fully optimized, actively managed profile outperforms a
   neglected one regardless of website quality.

2. **NAP consistency is non-negotiable** - Your business Name, Address, and Phone
   number must be identical across every citation, directory, and web property.
   Even minor variations (St. vs Street, Suite vs Ste) erode ranking signals.

3. **Reviews are both a ranking factor and a conversion driver** - The quantity,
   recency, and sentiment of reviews influence local pack rankings. A business with
   200 reviews at 4.3 stars beats one with 20 reviews at 5.0 stars in most queries.

4. **Relevance + proximity + prominence determine local pack rank** - Google weighs
   how relevant your business is to the search, how close you are to the searcher,
   and how well-known you are (links, reviews, citations). You can compensate for
   poor proximity with strong relevance and prominence signals.

5. **Local landing pages need unique, location-specific content** - A page for each
   location must go beyond swapping a city name. Include local addresses, phone
   numbers, staff, testimonials, service-area descriptions, and embedded maps.

---

## Core concepts

**The Local Pack vs organic results** - Local searches produce two types of results:
the Local Pack (a map widget with 3 business listings) and standard organic results
below it. GBP governs Local Pack rankings; your website governs organic local
rankings. A strong local SEO strategy targets both.

**Google's three local ranking factors** - Google evaluates local results on
relevance (does the business match what was searched?), distance (how close is it
to the searcher?), and prominence (how well-known and trusted is the business
online?). Prominence is the most controllable factor and is built through reviews,
citations, links, and an active GBP.

**GBP categories and attributes** - The primary category is the strongest relevance
signal Google uses. Choosing the wrong primary category (e.g. "Restaurant" vs
"Italian Restaurant") is a common high-cost mistake. Attributes (outdoor seating,
wheelchair accessible, accepts credit cards) improve relevance for filtered queries.

**Local citations** - Any online mention of your business NAP. Structured citations
are directory listings (Yelp, Yellow Pages, TripAdvisor). Unstructured citations are
mentions in blog posts or news articles. Both contribute to prominence signals.
See `references/local-citations-schema.md` for citation sources and schema.

**Review signals** - Google considers the total number of reviews, average rating,
recency (a business that got 10 reviews last month outperforms one that got 50 two
years ago), and review diversity across platforms (Google, Yelp, Facebook, industry
directories). Responding to reviews is also tracked as an engagement signal.

**Local link building** - Backlinks from locally relevant sites (local chambers of
commerce, local news outlets, community organizations) carry stronger local ranking
weight than equivalent links from generic national sites.

---

## Common tasks

### Set up and optimize Google Business Profile

A complete GBP optimization covers these elements in priority order:

1. **Claim and verify** the listing (postcard, phone, or email verification)
2. **Primary category** - Choose the most specific category that accurately describes
   the business. This is the strongest GBP relevance signal.
3. **Business name** - Use the exact legal business name. Do not append keywords.
4. **Address and service area** - For service-area businesses, hide the address and
   define the service area by city, zip, or radius.
5. **Phone number** - Use a local number (not a toll-free 800 number) that matches
   the number on your website and citations.
6. **Website URL** - Link to the most relevant landing page, not always the homepage.
7. **Business description** - Write 250-750 characters covering what you do, who you
   serve, and what makes you different. Include relevant keywords naturally.
8. **Photos** - Upload at least 10 photos: exterior, interior, team, products/services.
   GBP listings with photos receive significantly more clicks and direction requests.
9. **Hours** - Keep hours accurate and update for holidays. Inaccurate hours increase
   abandonment and can trigger negative reviews.
10. **Posts** - Publish GBP posts (updates, offers, events) at least twice a month to
    signal active management.
11. **Q&A** - Seed the Q&A section with your own questions and answers for common
    customer queries.

See `references/google-business-profile.md` for the complete GBP optimization guide.

### Audit and fix NAP consistency

1. Export all existing citations (use tools like BrightLocal, Whitespark, or Moz Local)
2. Define the canonical NAP: the exact legal business name, full address format, and
   primary phone number
3. Compare each citation against the canonical NAP
4. Prioritize fixes on high-authority directories first: Google, Yelp, Facebook,
   Bing Places, Apple Maps, Foursquare, Yellow Pages
5. Claim and update each listing directly (preferred) or use a citation management
   tool (Yext, BrightLocal) to push updates in bulk
6. Delete or merge duplicate listings - duplicates split ranking signals and confuse
   customers

### Implement LocalBusiness schema markup

Add JSON-LD structured data to every location page. This helps Google understand and
display business information in search results (knowledge panels, rich results).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Acme Plumbing Services",
  "image": "https://www.acmeplumbing.com/images/logo.png",
  "@id": "https://www.acmeplumbing.com/#business",
  "url": "https://www.acmeplumbing.com",
  "telephone": "+1-555-867-5309",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street, Suite 100",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "14:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/acmeplumbing",
    "https://www.yelp.com/biz/acme-plumbing-austin"
  ]
}
</script>
```

Use a specific `@type` when applicable: `Plumber`, `Restaurant`, `LegalService`,
`MedicalBusiness`, `AutoRepair`. Specific types unlock additional schema properties
and can trigger richer search features.

See `references/local-citations-schema.md` for multi-location and review schema patterns.

### Build a review generation strategy

1. **Identify the right moment** - Ask for reviews at peak satisfaction: immediately
   after service completion, after a successful project delivery, or following a
   compliment from the customer.
2. **Make it easy** - Create a short review link using the Google Place ID generator
   (`https://search.google.com/local/writereview?placeid=PLACE_ID`) and shorten it.
3. **Ask directly** - Staff should verbally ask satisfied customers and follow up with
   a text or email containing the review link. Multi-step friction kills conversion.
4. **Diversify platforms** - Prioritize Google, then industry-specific platforms
   (TripAdvisor for restaurants, Avvo for lawyers, Healthgrades for doctors).
5. **Respond to every review** - Thank positive reviewers by name. Respond to negative
   reviews within 24 hours with empathy and a path to resolution. Never argue.
6. **Never buy or incentivize reviews** - Violates Google's terms of service and can
   result in listing suspension or review removal.

### Create location-specific landing pages

Each location page must have unique, substantive content - not a template with a
city name swapped in. Include:

- The full NAP for that location embedded in visible text and in LocalBusiness schema
- A Google Maps embed for that specific address
- Location-specific content: local staff bios, local community involvement,
  neighborhood descriptions, local testimonials
- Location-specific FAQs addressing local queries ("Do you serve the South Austin area?")
- Internal links to the main services pages
- An `<h1>` that includes the service and location (e.g. "Plumbing Services in Austin, TX")
- A unique page title and meta description referencing the location

### Manage multi-location SEO

For businesses with 2+ locations:

1. Create a `/locations/` hub page listing all locations with links to individual
   location pages
2. Each location page gets its own GBP listing - never use one listing for multiple
   addresses
3. Use `sameAs` in schema to connect each location's GBP URL, Yelp page, and Facebook
   page to the corresponding location landing page
4. Build citations separately for each location - each location needs its own NAP
5. Manage review responses per-location - assign a team member per location
6. Use UTM parameters on GBP website links to track traffic and conversions per location

### Optimize for "near me" and service-area searches

"Near me" queries are handled almost entirely by GBP proximity and prominence - the
words "near me" do not need to appear on your website. To rank for them:

1. Ensure GBP service area is accurately defined
2. Maximize review count and recency (the strongest prominence signal)
3. Build local citations to strengthen the prominence score
4. On-page: use city/neighborhood names naturally in content, titles, and headings
5. Embed a Google Map on the contact page - it reinforces the location association

---

## Anti-patterns / common mistakes

| Mistake | Why it's wrong | What to do instead |
|---|---|---|
| Keyword stuffing in GBP business name | Violates Google guidelines and risks listing suspension | Use the exact legal business name only |
| Duplicate GBP listings | Splits ranking signals and confuses customers | Find and merge or remove duplicates using the GBP dashboard or contacting Google support |
| Inconsistent NAP across directories | Dilutes citation signals and reduces Google's confidence in the data | Audit all citations against canonical NAP and correct them |
| Buying or incentivizing reviews | Violates Google's Terms of Service; can result in review removal or suspension | Earn reviews organically by asking at moments of peak satisfaction |
| Thin location pages (city-swap templates) | Google detects near-duplicate content and ranks these poorly | Write unique content for each location page with local specifics |
| Using a toll-free 800 number on GBP | Signals a national operation, not a local business; weakens local relevance | Use the local phone number for GBP and citations |
| Ignoring or deleting negative reviews | Unresponded negative reviews signal poor customer service | Respond to every negative review professionally and offer resolution |
| Setting GBP address for a virtual office or UPS Store | Violates GBP guidelines and risks suspension | Only use addresses where customers can physically visit during listed hours |
| Neglecting GBP after initial setup | Active listings with recent posts, photos, and review responses outperform stale ones | Schedule monthly GBP maintenance: new photos, posts, and review responses |

---

## Gotchas

1. **GBP suspensions happen silently and without clear reasons** - Google can suspend a listing for guideline violations (keyword-stuffed name, virtual office address, duplicate listing) without email notice. The listing simply stops showing. Monitor GBP health weekly and always check the "Issues" tab. Recovery requires a reinstatement request through Google Business Profile support, which can take 2-6 weeks.

2. **NAP inconsistencies from data aggregators propagate indefinitely** - The four major data aggregators (Neustar Localeze, Foursquare, Data Axle, Acxiom) feed hundreds of directories automatically. A wrong address they have on file will keep repopulating corrected listings unless you fix it at the aggregator level. Tools like Yext or BrightLocal push updates to aggregators directly; manual directory fixes alone are insufficient.

3. **Keyword stuffing in the business name is a high-risk tactic that works short-term** - "Joe's Plumbing - Austin Emergency Plumber" may rank better temporarily, but it violates GBP guidelines and competitors can report it. Google processes reports and the listing name gets reverted or the listing suspended. Use the exact legal name.

4. **Review gating violates Google's terms and triggers penalties** - "Review gating" is asking customers to rate satisfaction before deciding whether to send them to Google reviews, filtering out unhappy customers. Google explicitly prohibits this. Only direct customers to review platforms without pre-screening.

5. **Multi-location businesses that share a phone number confuse Google's signals** - Using a single tracking or call center number across multiple locations makes it impossible for Google to associate each location with a unique NAP. Use unique local numbers per location, even if you route them centrally. Use call tracking at the subdomain/campaign level, not by replacing the primary GBP number.

---

## References

For detailed content on specific topics, read the relevant file from `references/`:

- `references/google-business-profile.md` - Complete GBP optimization guide: categories,
  attributes, posts, photos, Q&A, products/services, verification, insights, and
  multi-location management. Load when doing deep GBP work.

- `references/local-citations-schema.md` - Citation building strategy, top citation
  sources by industry, NAP audit process, and complete LocalBusiness JSON-LD schema
  patterns including multi-location, review, and service-area variants. Load when
  implementing schema or managing citations at scale.

Only load a references file if the current task requires deep detail on that topic.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
