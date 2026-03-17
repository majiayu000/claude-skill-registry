---
name: google-seo-starter-guide
version: 1.0.0
author: Google Search Central (skill created from documentation)
created: 2026-01-22
last_updated: 2026-01-22
status: active
complexity: moderate
category: seo-web-development
tags: [google-search, seo, search-optimization, web-development, content-strategy, technical-seo, search-console]
source: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
---

# Google SEO Starter Guide

> **Skill Purpose**: Comprehensive guide for implementing Google's SEO best practices to improve website presence in Google Search results through user-focused content, technical optimization, and strategic site organization.

## When to Use This Skill

Use this skill when you need to:

- Implement SEO fundamentals for a new website or web application
- Improve an existing website's visibility in Google Search results
- Understand how Google discovers, crawls, and indexes web content
- Optimize page titles, meta descriptions, and URL structure
- Create search-friendly content that balances user needs and discoverability
- Organize website architecture for better crawlability
- Optimize images and videos for search visibility
- Diagnose why a website isn't appearing in Google search results
- Implement structured data and rich results
- Develop a sustainable content strategy aligned with search best practices
- Train team members on SEO fundamentals and best practices
- Audit existing SEO implementation against Google's official guidelines

## When NOT to Use This Skill

Do **not** use this skill for:

- Black-hat SEO tactics or search engine manipulation (explicitly prohibited)
- Competitive SEO analysis of other websites
- Paid search advertising (Google Ads)
- Social media marketing strategies (except promotion tactics)
- Advanced technical SEO beyond fundamentals (JavaScript SEO, international sites)
- E-commerce specific optimization (use dedicated e-commerce SEO guides)
- Local SEO strategies (use Google Business Profile guidance)
- Schema markup implementation details (use structured data documentation)
- Core Web Vitals optimization (use PageSpeed Insights guidance)
- Site migration planning (use dedicated migration guides)

## Prerequisites

Before using this skill, ensure you have:

1. **Website Access and Control**
   - Ability to modify HTML, CSS, and website structure
   - Or access to content management system (CMS) with SEO capabilities
   - FTP or hosting panel access for technical changes

2. **Google Search Console Setup**
   - Verified property ownership in Search Console
   - Understanding of Search Console basics
   - Access to URL Inspection Tool and performance reports

3. **Technical Knowledge**
   - Basic understanding of HTML structure and meta tags
   - Familiarity with URL structures and web hosting
   - Understanding of how search engines work (crawling, indexing, ranking)

4. **Content Strategy Foundation**
   - Clear understanding of target audience
   - Knowledge of user search intent and common queries
   - Ability to create original, valuable content

## Workflow Phases

### Phase 1: Initial Site Assessment

**Objective**: Verify Google can find and index your website content.

**Steps**:

1. **Check Indexing Status**
   - Use search operator: `site:yourdomain.com` in Google
   - Review number of indexed pages
   - Verify key pages appear in results

2. **Set Up Search Console**
   - Create Search Console account if not already done
   - Verify ownership via DNS, HTML file, or Google Tag Manager
   - Submit sitemap (optional but recommended)

3. **Run URL Inspection**
   - Use URL Inspection Tool for critical pages
   - Check crawl status, indexing status, and rendering
   - Identify any blocking issues (robots.txt, noindex tags)

4. **Verify Crawlability**
   - Ensure Google can render JavaScript (if applicable)
   - Check robots.txt doesn't block important resources
   - Verify no accidental noindex directives on important pages

**Common Issues**:
- **Not indexed**: Check robots.txt, noindex tags, or server access issues
- **Partial indexing**: May indicate duplicate content or low-quality pages
- **Rendering problems**: JavaScript, CSS, or image resources blocked

**Validation**:
- Key pages appear in `site:` search results
- Search Console shows pages as "Indexed" in Coverage report
- No critical crawl errors in Search Console

### Phase 2: URL Structure and Site Organization

**Objective**: Create logical, descriptive URL structure that helps both users and Google understand site organization.

**Steps**:

1. **Audit Existing URLs**
   - Review current URL patterns
   - Identify problematic URLs (random IDs, excessive parameters)
   - Document URL structure across site sections

2. **Design Descriptive URL Structure**
   - Use words that describe page content
   - Group topically similar pages in directories
   - Keep URLs concise but meaningful
   - Use hyphens to separate words (not underscores)

**Examples**:

**Good URL Structure**:
```
example.com/pets/cats.html
example.com/products/running-shoes/nike-air-max
example.com/blog/2026/01/seo-best-practices
example.com/support/return-policy
```

**Bad URL Structure**:
```
example.com/2/6772756D707420636174  (random identifier)
example.com/index.php?id=45&cat=12   (excessive parameters)
example.com/page_1234                (non-descriptive)
```

3. **Implement Directory Hierarchy**
   - Create logical topical groupings
   - Use directories to show content relationships
   - Example hierarchy:
     ```
     /products/
       /clothing/
         /mens/
         /womens/
       /electronics/
         /phones/
         /laptops/
     /support/
       /faq/
       /returns/
     ```

4. **Handle Duplicate Content**
   - Identify pages with identical or very similar content
   - Implement canonical tags to specify preferred versions
   - Set up 301 redirects for permanently moved content
   - Use parameter handling in Search Console for URL parameters

**Best Practices**:
- Maintain consistency: Once URL structure is established, keep it stable
- Use HTTPS (secure protocol) for all pages
- Avoid excessive subdirectories (keep URLs reasonably short)
- Don't obsess over including keywords in domain name

**Validation**:
- URLs are human-readable and descriptive
- Site structure is logical when viewing in Search Console
- No duplicate content issues flagged

### Phase 3: Content Creation and Optimization

**Objective**: Create compelling, original content that serves user needs and ranks well in search results.

**Steps**:

1. **Identify Target Audience and Search Intent**
   - Define who you're writing for
   - Research common search queries (use Google Trends, Search Console)
   - Understand user intent: informational, navigational, or transactional
   - List keyword variations users might search

2. **Create High-Quality, Original Content**
   - Write naturally for humans, not search engines
   - Provide expert or experienced perspectives (E-E-A-T)
   - Make content well-written, error-free, and easy to follow
   - Keep information current and up-to-date

3. **Structure Content Effectively**
   - Use clear headings (H1, H2, H3) to organize content
   - Break content into logical sections
   - Use short paragraphs for readability
   - Include bulleted lists for scanability
   - Add relevant examples and explanations

4. **Optimize Content Length Naturally**
   - Don't target specific word counts
   - Cover topics comprehensively without artificial padding
   - Vary terminology (don't repeat same phrases excessively)
   - Focus on answering user questions thoroughly

5. **Implement Strategic Linking**
   - Link to relevant internal pages for additional context
   - Use descriptive anchor text that explains linked content
   - Add external links to authoritative sources when helpful
   - Add `nofollow` attribute to untrusted external links
   - Automatically add `nofollow` to user-generated content links

**Content Quality Checklist**:
- [ ] Original content (not duplicated from elsewhere)
- [ ] Free of spelling and grammatical errors
- [ ] Well-structured with clear headings
- [ ] Answers user questions comprehensively
- [ ] Includes relevant, authoritative sources
- [ ] Updated regularly to maintain accuracy
- [ ] Written naturally without keyword stuffing

**Common Mistakes to Avoid**:
- ❌ Keyword stuffing (excessively repeating same words)
- ❌ Duplicating content from other sites
- ❌ Creating multiple pages with identical information
- ❌ Neglecting to update outdated content
- ❌ Writing only for search engines, not users
- ❌ Ignoring spelling and grammar quality

**Validation**:
- Content reads naturally and provides value
- No duplicate content flags in Search Console
- Users spend time on page (check analytics)

### Phase 4: Title Links and Meta Descriptions

**Objective**: Optimize how pages appear in Google search results with compelling titles and descriptions.

**Steps**:

1. **Craft Unique Page Titles**
   - Create unique title for every page
   - Make titles clear, concise, and descriptive
   - Include business name, location, or key information if relevant
   - Keep titles readable at typical display width (avoid truncation)

**Title Best Practices**:

**Good Titles**:
```html
<title>Best Running Shoes for Marathon Training | Nike Air Max Review</title>
<title>Return Policy - Free Returns Within 30 Days | Example Store</title>
<title>How to Train Your Cat: Complete Guide for New Cat Owners</title>
```

**Bad Titles**:
```html
<title>Page 1</title>  (non-descriptive)
<title>Buy shoes running marathon Nike Adidas cheap best</title>  (keyword stuffing)
<title>Home</title>  (too generic, not unique)
```

2. **Write Compelling Meta Descriptions**
   - Create unique description for each important page
   - Write as "succinct, one- or two-sentence summary of the page"
   - Include relevant information users would find helpful
   - Don't worry about length limits (Google may rewrite anyway)

**Meta Description Examples**:

**Good**:
```html
<meta name="description" content="Comprehensive guide to training your new cat, including litter box training, socialization tips, and behavior management strategies from certified cat trainers.">
```

**Bad**:
```html
<meta name="description" content="cats training guide tips">  (too brief)
<meta name="description" content="This page is about cats and training and everything you need to know about training cats and cat behavior">  (repetitive)
```

3. **Implement Structured Data (Optional)**
   - Add structured data markup for rich results eligibility
   - Use Rich Results Test to validate implementation
   - Consider: Articles, Products, Recipes, Events, FAQs, etc.
   - Follow structured data guidelines carefully

**What NOT to Optimize**:
- ⚠️ **Keyword meta tags** - Ignored by Google, don't waste time
- ⚠️ **Exact word counts** - No magic number, write naturally
- ⚠️ **Heading order semantics** - H1 before H2 order doesn't directly matter

**Validation**:
- All important pages have unique titles and descriptions
- Titles display properly in search results (not truncated mid-word)
- Meta descriptions are informative and compelling

### Phase 5: Image and Video Optimization

**Objective**: Make visual content discoverable and understandable to search engines.

**Steps for Images**:

1. **Use High-Quality Images**
   - Use sharp, clear images (avoid blurry or pixelated)
   - Optimize file size for fast loading without quality loss
   - Use modern formats (WebP) where supported

2. **Position Images Strategically**
   - Place images near contextually relevant text
   - Use images to enhance understanding of content
   - Ensure images add value, not just decoration

3. **Write Descriptive Alt Text**
   - Describe what's in the image concisely
   - Explain relationship between image and page content
   - Keep alt text short but descriptive (don't keyword stuff)

**Alt Text Examples**:

**Good Alt Text**:
```html
<img src="golden-retriever-puppy.jpg" alt="Golden retriever puppy playing with red ball in backyard">
<img src="chocolate-chip-cookies.jpg" alt="Stack of freshly baked chocolate chip cookies on white plate">
```

**Bad Alt Text**:
```html
<img src="img123.jpg" alt="image">  (non-descriptive)
<img src="product.jpg" alt="buy cheap best quality product online store">  (keyword stuffing)
```

4. **Implement Image Best Practices**
   - Use descriptive filenames (not IMG_1234.jpg)
   - Provide image context through surrounding text
   - Consider lazy loading for below-the-fold images
   - Ensure images are crawlable (not blocked by robots.txt)

**Steps for Videos**:

1. **Create Standalone Video Pages**
   - Give each video its own dedicated page
   - Don't embed multiple videos on one page
   - Include video on page where users would logically find it

2. **Add Video Context**
   - Write descriptive title for the video
   - Create comprehensive description explaining video content
   - Add relevant text content around the video
   - Include transcript if possible (helps accessibility and SEO)

3. **Implement Video Structured Data**
   - Add VideoObject schema markup
   - Include thumbnail URL, upload date, duration
   - Provide accurate video description in markup

**Validation**:
- All images have descriptive alt text
- Images appear in Google Image Search
- Videos appear in video search results
- No broken image or video links

### Phase 6: Promotion and Audience Building

**Objective**: Build genuine audience through authentic engagement and strategic promotion.

**Steps**:

1. **Leverage Social Media Strategically**
   - Share content on relevant social platforms
   - Engage with your community authentically
   - Respond to comments and questions
   - Don't overdo promotion (avoid user fatigue)

2. **Participate in Relevant Communities**
   - Engage in online forums and discussion groups
   - Provide valuable insights without excessive self-promotion
   - Build reputation as helpful expert in your field
   - Follow community guidelines strictly

3. **Implement Offline Promotion**
   - Include website URL in offline marketing materials
   - Add to business cards, packaging, signage
   - Mention in presentations or events
   - Word-of-mouth marketing

4. **Build Natural Backlinks**
   - Create linkable assets (comprehensive guides, original research)
   - Reach out to relevant websites for genuine collaborations
   - Don't participate in link schemes or buying links
   - Focus on earning links through quality content

5. **Manage Advertisements Responsibly**
   - Ensure ads don't distract from main content
   - Avoid intrusive popups or interstitials
   - Don't let ads push content below fold on mobile
   - Follow Better Ads Standards

**Promotion Red Flags to Avoid**:
- ❌ Spamming forums with links
- ❌ Participating in link exchange schemes
- ❌ Buying backlinks
- ❌ Creating doorway pages for manipulation
- ❌ Cloaking (showing different content to Google vs. users)

**Validation**:
- Growing organic traffic in Search Console
- Increasing backlinks from quality sources
- Social engagement metrics improving
- Brand searches increasing

### Phase 7: Monitoring and Continuous Improvement

**Objective**: Track performance, identify issues, and continuously optimize based on data.

**Steps**:

1. **Monitor Search Console Regularly**
   - Check Performance report for traffic trends
   - Review Coverage report for indexing issues
   - Inspect Core Web Vitals for user experience metrics
   - Address any manual actions immediately

2. **Use Analytics for Insights**
   - Track user behavior and engagement metrics
   - Identify top-performing content
   - Find high-bounce pages needing improvement
   - Monitor conversion goals

3. **Conduct Regular Content Audits**
   - Update outdated information
   - Improve underperforming pages
   - Consolidate or remove low-value content
   - Refresh content with new insights

4. **Test and Iterate**
   - Try different title and description variations
   - A/B test content approaches
   - Experiment with content formats (videos, infographics)
   - Learn from what works for your audience

5. **Stay Informed on Updates**
   - Follow Google Search Central blog
   - Monitor for algorithm updates
   - Adapt to new features (e.g., AI Overviews)
   - Update practices based on official guidance

**Timeline Expectations**:
- **Hours to days**: Simple HTML changes (titles, meta descriptions)
- **Weeks to months**: New content indexing and ranking
- **Months**: Significant traffic improvements from optimization
- **Ongoing**: Continuous improvement and maintenance

**Validation**:
- Regular monitoring cadence established
- Proactive issue resolution
- Continuous traffic growth trends
- Decreasing bounce rates and increasing engagement

## Examples

### Example 1: Optimizing a New Blog Post for Search

**Scenario**: You've written a comprehensive guide on "How to Start a Podcast" and want to optimize it for Google Search.

**Implementation**:

1. **URL Structure**:
   ```
   yourblog.com/guides/how-to-start-a-podcast
   ```
   (Descriptive, includes topic, in logical directory)

2. **Page Title**:
   ```html
   <title>How to Start a Podcast: Complete Beginner's Guide (2026) | Your Blog Name</title>
   ```
   (Unique, descriptive, includes year for freshness, brand)

3. **Meta Description**:
   ```html
   <meta name="description" content="Step-by-step guide to starting your first podcast, covering equipment selection, recording software, hosting platforms, and promotion strategies. Perfect for beginners with no technical experience.">
   ```
   (Compelling summary, includes key topics, targets beginners)

4. **Content Structure**:
   ```markdown
   # How to Start a Podcast: Complete Beginner's Guide

   [Introduction paragraph explaining what podcast is and why start one]

   ## What You'll Need to Start a Podcast
   - Equipment (microphone, headphones)
   - Recording software
   - Hosting platform
   - Cover art

   ## Step 1: Choose Your Podcast Topic and Format
   [Detailed content with examples]

   ## Step 2: Select Recording Equipment
   [Detailed content with product recommendations]

   [Continue with more sections...]

   ## Common Mistakes When Starting a Podcast
   [Avoid these pitfalls...]

   ## Conclusion and Next Steps
   ```

5. **Images**:
   ```html
   <img src="podcast-microphone-setup.jpg" alt="Professional podcast microphone setup with boom arm and pop filter on desk">
   <img src="recording-software-screenshot.jpg" alt="Audacity recording software interface showing waveform and editing tools">
   ```
   (Descriptive alt text, positioned near relevant content)

6. **Internal Linking**:
   ```markdown
   For more tips on audio editing, check out our [Audio Editing for Beginners guide](/guides/audio-editing-basics).

   Once your podcast is live, learn how to [promote your podcast effectively](/guides/podcast-promotion-strategies).
   ```
   (Descriptive anchor text, relevant internal links)

7. **External Linking**:
   ```markdown
   According to [Edison Research's 2025 Podcast Report](https://example.com), 42% of Americans listen to podcasts monthly.
   ```
   (Authoritative source, adds credibility)

**Expected Outcome**: Blog post indexes within days, begins appearing in search results for "how to start a podcast" and related queries within weeks. Comprehensive content and good structure lead to sustained rankings.

### Example 2: Fixing an E-commerce Product Page Not Ranking

**Scenario**: Your product page for "Organic Dog Food" exists but isn't appearing in search results despite being indexed.

**Diagnosis**:
- Generic title: "Product - Page 142"
- No meta description
- Thin content (only product specs, no context)
- Generic URLs: `example.com/products?id=142`
- No images or poorly labeled images

**Solution**:

1. **Update URL Structure**:
   ```
   Before: example.com/products?id=142
   After: example.com/products/organic-dog-food-grain-free
   ```
   (Implement 301 redirect from old URL)

2. **Optimize Title**:
   ```html
   Before: <title>Product - Page 142</title>
   After: <title>Organic Grain-Free Dog Food - High Protein Formula | PetStore</title>
   ```

3. **Add Meta Description**:
   ```html
   <meta name="description" content="Premium organic dog food made with grass-fed beef and fresh vegetables. Grain-free, high-protein formula perfect for active dogs. Free shipping on orders over $50.">
   ```

4. **Expand Product Content**:
   ```html
   <h1>Organic Grain-Free Dog Food - High Protein Formula</h1>

   <p>Give your dog the nutrition they deserve with our premium organic dog food. Made with 80% grass-fed beef and 20% fresh vegetables, this grain-free formula provides complete nutrition for active dogs of all sizes.</p>

   <h2>Key Features</h2>
   <ul>
     <li>100% organic, human-grade ingredients</li>
     <li>Grain-free and gluten-free</li>
     <li>High protein (32%) for muscle development</li>
     <li>No artificial preservatives or fillers</li>
     <li>Made in USA with locally sourced ingredients</li>
   </ul>

   <h2>Ingredients</h2>
   [Detailed ingredients list]

   <h2>Feeding Guidelines</h2>
   [Weight-based feeding chart]

   <h2>Why Choose Organic Dog Food?</h2>
   [Educational content about benefits]
   ```

5. **Optimize Images**:
   ```html
   Before: <img src="img_142.jpg" alt="product">

   After:
   <img src="organic-dog-food-bag.jpg" alt="5-pound bag of organic grain-free dog food with grass-fed beef">
   <img src="dog-eating-organic-food.jpg" alt="Happy golden retriever eating organic dog food from stainless steel bowl">
   ```

6. **Add Product Schema**:
   ```json
   {
     "@context": "https://schema.org/",
     "@type": "Product",
     "name": "Organic Grain-Free Dog Food",
     "image": "https://example.com/images/organic-dog-food-bag.jpg",
     "description": "Premium organic dog food made with grass-fed beef",
     "brand": {
       "@type": "Brand",
       "name": "PetStore"
     },
     "offers": {
       "@type": "Offer",
       "price": "49.99",
       "priceCurrency": "USD",
       "availability": "https://schema.org/InStock"
     }
   }
   ```

**Expected Outcome**: Within 2-4 weeks, product page begins appearing for relevant searches like "organic dog food," "grain-free dog food," and related queries. Enhanced content and proper optimization lead to improved rankings and conversions.

### Example 3: Launching a New Website with SEO Fundamentals

**Scenario**: You're launching a new website for a local bakery and want to implement SEO best practices from the start.

**Implementation Checklist**:

1. **Pre-Launch Setup**:
   - [x] Register Google Search Console account
   - [x] Verify ownership (DNS verification)
   - [x] Create XML sitemap
   - [x] Configure robots.txt properly
   - [x] Set up Google Analytics 4
   - [x] Ensure HTTPS is properly configured

2. **URL Structure**:
   ```
   bakery.com/about
   bakery.com/menu/cakes
   bakery.com/menu/pastries
   bakery.com/menu/breads
   bakery.com/catering
   bakery.com/locations
   bakery.com/contact
   bakery.com/blog/wedding-cake-tips
   ```

3. **Core Pages with Optimized Titles**:
   ```html
   Home: <title>Sweet Delights Bakery - Fresh Pastries & Custom Cakes | Boston, MA</title>
   Menu: <title>Bakery Menu - Cakes, Pastries, Breads | Sweet Delights</title>
   Catering: <title>Catering Services - Wedding Cakes & Event Desserts | Sweet Delights Bakery</title>
   ```

4. **Content Strategy**:
   - Homepage: Business overview, location, hours, featured products
   - Menu pages: Detailed descriptions of offerings with pricing
   - Blog: SEO-friendly content ("How to Choose Wedding Cake," "Gluten-Free Baking Tips")
   - Location page: Address, map, directions, parking info

5. **Image Optimization**:
   ```html
   <img src="chocolate-wedding-cake.jpg" alt="Three-tier chocolate wedding cake with fresh raspberry decoration">
   <img src="fresh-croissants.jpg" alt="Basket of fresh-baked butter croissants">
   <img src="bakery-interior.jpg" alt="Sweet Delights Bakery interior with display case of pastries">
   ```

6. **Local SEO Elements**:
   - Google Business Profile setup and optimization
   - NAP (Name, Address, Phone) consistency across site
   - Local business schema markup
   - Location-specific content

7. **Post-Launch Monitoring**:
   - Submit sitemap to Search Console
   - Monitor indexing progress in Coverage report
   - Check for any crawl errors
   - Verify mobile-friendliness
   - Monitor Core Web Vitals

**Timeline**:
- **Week 1**: Site goes live, sitemap submitted
- **Week 2-4**: Google discovers and indexes pages
- **Month 2**: Begin seeing organic traffic
- **Month 3+**: Rankings stabilize, ongoing optimization

**Expected Outcome**: Website launches with solid SEO foundation, indexes properly within weeks, begins attracting local search traffic for relevant queries like "bakery Boston," "wedding cakes Boston," "fresh pastries near me."

## Common Pitfalls

### 1. Keyword Stuffing

**Problem**: Excessively repeating keywords thinking it will improve rankings.

**Why It's Bad**:
- Creates unnatural, hard-to-read content
- May trigger spam filters or manual actions
- Poor user experience leads to high bounce rates
- Wastes time on outdated tactic

**Example**:
```
Bad: "Our bakery in Boston is the best Boston bakery for Boston residents
looking for a bakery in Boston. Visit our Boston bakery today!"

Good: "Sweet Delights Bakery serves fresh pastries and custom cakes to
Boston residents and visitors. Stop by our downtown location for
handcrafted baked goods."
```

**Solution**:
- Write naturally for human readers
- Use varied terminology and synonyms
- Focus on comprehensive coverage, not repetition
- Read content aloud to check if it sounds natural

### 2. Ignoring Mobile Experience

**Problem**: Optimizing only for desktop while most searches happen on mobile.

**Why It's Bad**:
- Google uses mobile-first indexing
- Poor mobile experience leads to lower rankings
- Intrusive popups or ads frustrate mobile users
- Slow loading times increase bounce rates

**Solution**:
- Use responsive design that adapts to all screen sizes
- Test mobile usability in Search Console
- Optimize page speed for mobile connections
- Avoid intrusive interstitials on mobile
- Ensure buttons and links are tap-friendly

### 3. Duplicate Content

**Problem**: Creating multiple pages with identical or very similar content.

**Why It's Bad**:
- Google must choose which version to index
- Wastes crawl budget
- Dilutes ranking signals across multiple URLs
- Confuses users with redundant pages

**Common Causes**:
- HTTP vs HTTPS versions both accessible
- WWW vs non-WWW versions both active
- Multiple URL parameters leading to same content
- Printer-friendly versions without canonicalization

**Solution**:
- Implement canonical tags pointing to preferred version
- Set up 301 redirects for duplicate URLs
- Use parameter handling in Search Console
- Consolidate similar pages into single comprehensive page

### 4. Neglecting Search Console

**Problem**: Not monitoring Search Console or ignoring warnings and errors.

**Why It's Bad**:
- Miss critical indexing issues
- Don't see coverage errors or manual actions
- Lack visibility into search performance
- Can't diagnose ranking drops or traffic changes

**Solution**:
- Check Search Console at least weekly
- Set up email alerts for critical issues
- Address coverage errors promptly
- Monitor performance trends regularly
- Use URL Inspection Tool for troubleshooting

### 5. Over-Optimizing Anchor Text

**Problem**: Using exact-match keywords in all internal link anchor text.

**Why It's Bad**:
- Looks unnatural and manipulative
- May trigger over-optimization penalties
- Poor user experience with repetitive links
- Doesn't provide context about linked content

**Example**:
```
Bad (all internal links):
- "Click here to see our best dog food products"
- "Dog food for sale"
- "Buy dog food online"

Good (varied, natural):
- "Check out our selection of organic dog food"
- "Learn about grain-free options"
- "See our customer reviews"
```

**Solution**:
- Use varied, natural anchor text
- Make anchor text descriptive of linked content
- Don't force keywords into every link
- Think about what helps users understand the link destination

## Troubleshooting

### Problem: Site not appearing in Google search results

**Symptoms**: `site:yourdomain.com` returns no results or very few pages.

**Diagnosis Steps**:

1. **Check Search Console Coverage Report**
   - Go to Search Console → Coverage
   - Look for "Excluded" or "Error" status on important pages

2. **Common Causes**:
   - Robots.txt blocking crawlers
   - Noindex meta tags accidentally left on pages
   - Site not yet discovered by Google (very new)
   - Manual action or algorithmic filter
   - Server returning wrong status codes (404, 500)

**Resolution**:

1. **For robots.txt issues**:
   - Check robots.txt file at `yourdomain.com/robots.txt`
   - Remove `Disallow: /` if blocking everything
   - Ensure important sections aren't blocked
   - Test with robots.txt Tester in Search Console

2. **For noindex tags**:
   - Inspect page source for `<meta name="robots" content="noindex">`
   - Check for X-Robots-Tag HTTP headers
   - Remove noindex directives from pages you want indexed
   - Use URL Inspection Tool to verify "Indexing allowed: Yes"

3. **For new sites**:
   - Submit sitemap in Search Console
   - Request indexing for key pages via URL Inspection Tool
   - Create backlinks from established sites
   - Be patient (can take days to weeks)

4. **For manual actions**:
   - Check Search Console → Manual Actions
   - Follow guidance to fix violations
   - Submit reconsideration request after fixes

**Validation**: Within days to weeks, pages should appear in search results.

### Problem: Rankings dropped suddenly

**Symptoms**: Significant traffic decrease, pages no longer ranking for target keywords.

**Diagnosis Steps**:

1. **Check for Algorithm Updates**
   - Search for recent Google algorithm updates
   - Review Search Central blog for announcements
   - Check SEO news sources for update reports

2. **Review Search Console**
   - Check for new manual actions
   - Look for coverage errors or indexing issues
   - Review Core Web Vitals for performance problems

3. **Audit Recent Changes**
   - Did you recently update content?
   - Were there technical changes (CMS update, server migration)?
   - Any new backlinks from questionable sources?

**Common Causes**:
- Helpful Content Update impact (low-quality content)
- Core Web Vitals issues (page experience)
- Mobile usability problems
- Unnatural backlinks or link schemes
- Technical errors breaking site

**Resolution**:

1. **For content quality issues**:
   - Review and improve thin or low-value content
   - Remove or consolidate duplicate pages
   - Update outdated information
   - Focus on expertise, experience, authoritativeness

2. **For technical issues**:
   - Fix broken links and 404 errors
   - Improve page load speed
   - Resolve mobile usability issues
   - Ensure proper canonicalization

3. **For Core Web Vitals**:
   - Use PageSpeed Insights to identify issues
   - Optimize images and defer non-critical JavaScript
   - Improve server response times
   - Address layout shifts and interactivity delays

**Validation**: Recovery can take weeks to months depending on issue severity.

### Problem: Pages indexed but not ranking

**Symptoms**: Pages appear in `site:` search but don't rank for target queries.

**Possible Causes**:
- Intense competition for target keywords
- Content doesn't match search intent
- Low-quality or thin content
- Poor page experience metrics
- Lack of backlinks or authority

**Resolution**:

1. **Analyze Search Intent**:
   - Search for target keyword
   - Review what currently ranks (format, depth, angle)
   - Ensure your content matches user expectations
   - Consider if your page truly answers the query

2. **Improve Content Quality**:
   - Make content more comprehensive than competitors
   - Add unique insights or perspectives
   - Include examples, images, and multimedia
   - Update with fresh, current information

3. **Build Authority**:
   - Create linkable assets (original research, tools, guides)
   - Reach out for genuine backlinks from relevant sites
   - Improve internal linking structure
   - Build brand recognition through promotion

4. **Optimize On-Page Elements**:
   - Review title and description optimization
   - Improve heading structure
   - Enhance content formatting and readability
   - Add relevant structured data

**Validation**: Improvements may take weeks to months to show in rankings.

### Problem: Duplicate content issues

**Symptoms**: Search Console shows "Duplicate, submitted URL not selected as canonical."

**Possible Causes**:
- Multiple URLs serving same content
- HTTP vs HTTPS versions both accessible
- WWW vs non-WWW versions both indexed
- URL parameters creating duplicate pages

**Resolution**:

1. **Identify Preferred Version**:
   - Decide which URL should be canonical
   - Check which version has more backlinks
   - Choose most user-friendly URL

2. **Implement Canonical Tags**:
   ```html
   <link rel="canonical" href="https://www.example.com/preferred-url">
   ```
   Add to all duplicate versions pointing to preferred URL

3. **Set Up 301 Redirects**:
   ```
   Redirect 301 /old-url https://www.example.com/new-url
   ```
   For permanently moved content or consolidation

4. **Configure Server/CMS**:
   - Set preferred domain (www vs non-www)
   - Force HTTPS redirect
   - Use parameter handling in Search Console

**Validation**: Within weeks, Google should consolidate signals to canonical version.

## Integration Notes

This skill integrates with other SEO and web development workflows:

- **After site development**: Use this skill to implement SEO fundamentals before launch
- **With content strategy**: Align content creation with SEO best practices from this guide
- **Before site migrations**: Review guidelines to preserve SEO value during transitions
- **With technical SEO audits**: Use as baseline for identifying fundamental issues
- **For ongoing optimization**: Reference continuously as part of content and technical maintenance
- **With analytics tools**: Combine Search Console data with analytics for comprehensive insights
- **During redesigns**: Ensure new design maintains or improves SEO fundamentals

## Quality Standards

When implementing this skill, ensure:

- ✅ All pages have unique, descriptive titles and meta descriptions
- ✅ URL structure is logical, descriptive, and consistent
- ✅ Content is original, well-written, and serves user needs
- ✅ Images have descriptive alt text and are optimized for performance
- ✅ Internal linking uses varied, descriptive anchor text
- ✅ External links to untrusted sources include `nofollow` attribute
- ✅ Site is fully accessible to Google's crawlers (no blocking issues)
- ✅ Mobile experience is optimized and user-friendly
- ✅ Search Console is set up and monitored regularly
- ✅ Changes are tracked and measured for effectiveness
- ✅ No manipulative tactics or policy violations present
- ✅ Content is kept current with regular updates

## Version History

- **1.0.0** (2026-01-22): Initial skill creation from Google Search Central SEO Starter Guide documentation

## Additional Resources

- [Google Search Central](https://developers.google.com/search)
- [Search Essentials (formerly Webmaster Guidelines)](https://developers.google.com/search/docs/essentials)
- [How Google Search Works](https://www.google.com/search/howsearchworks/)
- [Creating Helpful Content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [JavaScript SEO Basics](https://developers.google.com/search/docs/javascript)
- [Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data)
- [Mobile-First Indexing](https://developers.google.com/search/mobile-sites/mobile-first-indexing)
- [International and Multilingual Sites](https://developers.google.com/search/docs/specialty/international)
- [E-commerce SEO](https://developers.google.com/search/docs/specialty/ecommerce)
- [Core Web Vitals](https://web.dev/vitals/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Google Trends](https://trends.google.com/)
