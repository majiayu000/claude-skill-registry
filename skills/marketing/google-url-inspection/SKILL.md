---
name: google-url-inspection
version: 1.0.0
author: Google Search Central (skill created from documentation)
created: 2026-01-22
last_updated: 2026-01-22
status: active
complexity: basic
category: seo-webmaster-tools
tags: [google-search-console, url-inspection, seo, indexing, crawl-analysis, technical-seo, webmaster-tools]
source: https://support.google.com/webmasters/answer/9012289
---

# Google URL Inspection Tool

> **Skill Purpose**: Comprehensive guide for using Google's URL Inspection Tool in Search Console to verify indexing status, diagnose crawl issues, and request re-indexing for specific URLs.

## When to Use This Skill

Use this skill when you need to:

- Verify if a specific URL is indexed by Google
- Diagnose why a page is not appearing in Google search results
- Check how Google crawls and renders a specific page
- Request indexing or re-indexing after making page updates
- Troubleshoot crawl errors preventing page discovery
- Verify JavaScript rendering and content visibility
- Check mobile vs. desktop indexing differences
- Investigate robots.txt or meta robots restrictions
- Validate fixes after resolving technical SEO issues
- Understand Google's view of a specific URL before site-wide audits

## When NOT to Use This Skill

Do **not** use this skill for:

- Analyzing site-wide indexing issues (use Coverage reports instead)
- Bulk URL inspection (tool is designed for individual URLs)
- Keyword ranking analysis (use Search Performance reports)
- Competitive analysis of other websites
- Sitemap validation (use Sitemaps tool)
- Mobile usability testing (use Mobile Usability reports)
- Core Web Vitals analysis (use Page Experience reports)
- Backlink analysis (use Links reports)

## Prerequisites

Before using this skill, ensure you have:

1. **Google Search Console Account**
   - Verified ownership of the website property
   - Appropriate access level (Owner, Full User, or Restricted User)

2. **Technical Knowledge**
   - Basic understanding of HTML and web page structure
   - Familiarity with HTTP status codes
   - Understanding of crawling and indexing concepts

3. **Access Requirements**
   - URL must belong to a verified Search Console property
   - Property must be verified via DNS, HTML file, Google Tag Manager, or other method

## Workflow Phases

### Phase 1: Access the URL Inspection Tool

**Objective**: Navigate to the URL Inspection Tool in Google Search Console.

**Steps**:

1. **Log into Google Search Console**
   - Navigate to https://search.google.com/search-console
   - Sign in with your Google account

2. **Select Your Property**
   - Choose the website property you want to inspect
   - Ensure the property is verified and active

3. **Open URL Inspection Tool**
   - Click on the magnifying glass icon at the top of any Search Console page
   - Or select "URL Inspection" from the left-hand navigation menu

**Validation**:
- Tool interface loads successfully
- Search bar is visible and active

### Phase 2: Inspect a Specific URL

**Objective**: Submit a URL for inspection and review the results.

**Steps**:

1. **Enter the URL**
   - Paste or type the full URL you want to inspect
   - Include protocol (https:// or http://)
   - Ensure URL matches the property exactly (www vs. non-www)

2. **Submit for Inspection**
   - Press Enter or click the search icon
   - Wait for Google to fetch inspection data (5-10 seconds)

3. **Review Indexing Status**
   - Check the primary status indicator:
     - **"URL is on Google"**: Successfully indexed
     - **"URL is not on Google"**: Not indexed (review reasons)
     - **"URL has issues"**: Indexed but with warnings

**Common Status Messages**:
- ✅ **"URL is on Google"**: Page is indexed and eligible to appear in search results
- ❌ **"URL is not on Google"**: Page is not indexed (see error details)
- ⚠️ **"Coverage: Excluded"**: Page was crawled but not indexed (check exclusion reason)
- 🔒 **"Blocked by robots.txt"**: Crawlers are blocked from accessing the page

**Validation**:
- Inspection results appear within 15 seconds
- Status message is clear and actionable

### Phase 3: Analyze Crawl and Indexing Details

**Objective**: Review detailed information about how Google crawls and indexes the URL.

**Key Sections to Review**:

1. **Coverage**
   - Indexing status and eligibility
   - Sitemaps that reference this URL
   - Referring page (how Google discovered the URL)

2. **Crawl**
   - Last crawl date and time
   - Crawl allowed/disallowed status
   - Fetch status (success, error codes)
   - Page fetch details (user-agent, response code)

3. **Indexing**
   - Whether the page can be indexed
   - Canonical URL detected by Google
   - User-declared canonical URL

4. **Enhancements**
   - Mobile usability issues
   - Structured data detection
   - AMP validity (if applicable)

**Critical Checks**:
- **Last Crawl Date**: Verify it's recent (within expected timeframe)
- **Crawl Allowed**: Must be "Yes" for indexing
- **Indexing Allowed**: Check for robots meta tags or X-Robots-Tag headers
- **Canonical URL**: Verify it matches your intent

**Validation**:
- All sections display data without errors
- Crawl date is within expected range for your site

### Phase 4: Test Live URL (Optional)

**Objective**: Fetch the current live version of the URL to see how Google crawls it now.

**Steps**:

1. **Click "Test Live URL"**
   - Located in the top-right corner of the inspection results
   - This fetches the URL in real-time (not from Google's index)

2. **Wait for Live Test Results**
   - Takes 10-30 seconds to complete
   - Google crawls the URL as Googlebot would now

3. **Review Live Test Results**
   - Compare live status with indexed version
   - Check for differences in crawlability or rendering

**Use Cases for Live Testing**:
- After fixing crawl errors on the page
- After updating robots.txt or meta robots tags
- After implementing JavaScript changes that affect rendering
- Before requesting indexing to verify fixes

**Validation**:
- Live test completes without errors
- Results show improvements over indexed version

### Phase 5: View Rendered Page

**Objective**: See how Google renders the page after executing JavaScript.

**Steps**:

1. **Click "View Crawled Page"**
   - Located in the Coverage or Indexing section
   - Opens a modal with three tabs

2. **Review HTML Tab**
   - Shows the raw HTML received by Googlebot
   - Check for critical content presence

3. **Review Screenshot Tab**
   - Visual representation of how Google renders the page
   - Verify that key content is visible

4. **Review More Info Tab**
   - HTTP response details
   - Page resources loaded/blocked
   - JavaScript console errors

**Critical Checks**:
- Primary content appears in the HTML (not just JavaScript-rendered)
- Screenshot shows key elements (navigation, main content, footer)
- No critical JavaScript errors in console

**Common Issues**:
- Content only visible in screenshot but missing from HTML (JavaScript-dependent)
- Blocked resources preventing full rendering
- JavaScript errors causing content to fail loading

**Validation**:
- All three tabs load successfully
- Rendered page matches user expectations

### Phase 6: Request Indexing (If Needed)

**Objective**: Request Google to crawl and index the URL (or re-index after updates).

**Steps**:

1. **Verify Page is Ready**
   - All crawl errors resolved
   - Robots.txt allows crawling
   - No noindex directives present
   - Content is valuable and unique

2. **Click "Request Indexing"**
   - Button appears at top of inspection results
   - Only available if URL is not blocked

3. **Wait for Confirmation**
   - Takes 5-10 seconds to submit request
   - Confirmation message appears

4. **Understand the Process**
   - Request is added to Google's crawl queue
   - No guaranteed timeline (minutes to days)
   - Actual indexing depends on quality signals

**Important Notes**:
- ⚠️ **Rate Limits**: Limited number of indexing requests per day per property
- ⚠️ **Not a Guarantee**: Request doesn't guarantee indexing, only prioritizes crawling
- ⚠️ **Quality Matters**: Low-quality pages may still be excluded after crawling

**Best Practices**:
- Only request indexing for important updates or new high-value content
- Fix all errors before requesting indexing
- Don't request indexing repeatedly for the same URL
- Use sitemaps for bulk URL discovery instead of individual requests

**Validation**:
- Confirmation message: "Indexing requested"
- No errors during submission

### Phase 7: Troubleshoot Common Issues

**Objective**: Diagnose and resolve common crawl and indexing problems.

**Issue 1: "URL is not on Google" - Blocked by robots.txt**

**Diagnosis**:
- Crawl section shows "Blocked by robots.txt: Yes"
- Robots.txt file is disallowing Googlebot

**Solution**:
1. Review your robots.txt file at https://yoursite.com/robots.txt
2. Remove or modify the disallow directive blocking the URL
3. Test changes using robots.txt Tester in Search Console
4. Wait for Google to re-crawl robots.txt (or request crawl)
5. Use "Test Live URL" to verify access
6. Request indexing once confirmed

**Issue 2: "URL is not on Google" - Soft 404 or noindex**

**Diagnosis**:
- Page returns 200 status but has little content
- Or page has `<meta name="robots" content="noindex">` tag

**Solution**:
1. Review the "Indexing" section for noindex directives
2. Check HTML source for meta robots tags or X-Robots-Tag headers
3. Remove noindex if indexing is desired
4. For soft 404s, add substantial unique content
5. Test live URL to verify changes
6. Request indexing

**Issue 3: "URL is on Google" but with rendering issues**

**Diagnosis**:
- Screenshot shows missing content
- JavaScript console shows errors
- Resources are blocked

**Solution**:
1. Review "View Crawled Page" → "More Info" tab
2. Check for blocked JavaScript/CSS resources
3. Update robots.txt to allow critical resources
4. Fix JavaScript errors preventing content rendering
5. Test with "Test Live URL" to verify improvements
6. Request indexing to update indexed version

**Issue 4: Canonical mismatch**

**Diagnosis**:
- User-declared canonical differs from Google-selected canonical
- May indicate duplicate content issues

**Solution**:
1. Review the "Indexing" section for canonical URLs
2. Verify your canonical tags are correct
3. Ensure all duplicate versions point to preferred URL
4. Check for conflicting signals (canonical vs. sitemap vs. internal links)
5. Request indexing for preferred canonical URL

**Issue 5: "Crawled - currently not indexed"**

**Diagnosis**:
- Google crawled the page but chose not to index it
- Usually indicates quality or duplication issues

**Solution**:
1. Improve content quality and uniqueness
2. Add more substantial content (aim for 300+ words)
3. Ensure page provides value beyond existing indexed pages
4. Check for thin content, doorway pages, or duplication
5. Wait for natural re-crawl (Google may index later)
6. Consider consolidating with similar pages

## Examples

### Example 1: Verifying New Blog Post Indexing

**Scenario**: You published a new blog post and want to verify Google has indexed it.

**Steps**:
1. Access URL Inspection Tool in Search Console
2. Enter the full blog post URL: `https://yoursite.com/blog/new-post-title`
3. Review inspection results:
   - **If "URL is on Google"**: Post is indexed and may appear in search results
   - **If "URL is not on Google"**: Check for errors or request indexing
4. If not indexed, click "Test Live URL" to verify current crawlability
5. Review rendered page to ensure content is visible
6. Click "Request Indexing" if page is ready
7. Wait 24-48 hours and re-inspect to verify indexing

**Expected Outcome**: Blog post appears in Google search results within 1-7 days.

### Example 2: Diagnosing Missing Product Page

**Scenario**: An important product page isn't appearing in search results despite being live for weeks.

**Steps**:
1. Open URL Inspection Tool
2. Enter product page URL: `https://yoursite.com/products/product-name`
3. Review status message:
   - If blocked by robots.txt, update robots.txt file
   - If soft 404, add more product details and unique content
   - If noindex, remove meta robots noindex tag
4. Click "View Crawled Page" to see how Google renders it
5. Check screenshot for visible product info (title, image, description, price)
6. Review "More Info" for JavaScript errors or blocked resources
7. Fix identified issues on the live page
8. Click "Test Live URL" to verify fixes work
9. Request indexing once all issues resolved
10. Re-inspect in 3-7 days to verify indexing

**Expected Outcome**: Product page gets indexed and appears in search results.

### Example 3: Verifying JavaScript Rendering

**Scenario**: Your site uses client-side JavaScript to render content, and you want to ensure Google can see it.

**Steps**:
1. Access URL Inspection Tool
2. Enter a key page URL that relies on JavaScript: `https://yoursite.com/interactive-tool`
3. Click "View Crawled Page"
4. Compare HTML tab vs. Screenshot tab:
   - **HTML tab**: Shows initial HTML before JavaScript execution
   - **Screenshot tab**: Shows final rendered page after JavaScript runs
5. Verify critical content appears in screenshot
6. Check "More Info" tab for JavaScript console errors
7. If content missing from screenshot:
   - Fix JavaScript errors shown in console
   - Ensure critical resources aren't blocked by robots.txt
   - Consider server-side rendering or pre-rendering for critical content
8. Test Live URL after fixes
9. Request indexing

**Expected Outcome**: Google successfully renders JavaScript content and indexes the page with full content visible.

## Common Pitfalls

### 1. Requesting Indexing Too Frequently

**Problem**: Submitting multiple indexing requests for the same URL within a short period.

**Why It's Bad**:
- Rate limits may block further requests
- Wastes crawl budget
- Doesn't speed up indexing

**Solution**:
- Request indexing once per URL per major update
- Use sitemaps for bulk URL discovery
- Wait at least 1-2 weeks before re-requesting

### 2. Assuming "Not Indexed" Means Permanent Rejection

**Problem**: Thinking "URL is not on Google" means the page will never be indexed.

**Why It's Bad**:
- Many not-indexed pages are simply awaiting crawl
- Status can change as Google re-crawls

**Solution**:
- Review the specific reason for non-indexing
- Fix any errors or quality issues
- Allow time for natural crawling (submit sitemap)
- Request indexing only for high-priority pages

### 3. Ignoring Rendering Issues

**Problem**: Not checking the "View Crawled Page" screenshot and assuming Google sees the page correctly.

**Why It's Bad**:
- JavaScript errors may hide critical content
- Blocked resources prevent proper rendering
- Content may be invisible to Google even if visible to users

**Solution**:
- Always review the screenshot for important pages
- Check for JavaScript console errors
- Unblock critical CSS/JS resources in robots.txt
- Test with "Test Live URL" after making changes

### 4. Mixing Up www vs. non-www Versions

**Problem**: Inspecting the wrong URL variant (www.example.com vs. example.com) when only one is indexed.

**Why It's Bad**:
- Different variants are separate properties in Search Console
- Inspection results won't match your site's actual indexing

**Solution**:
- Verify which URL variant is your canonical version
- Inspect the canonical variant in Search Console
- Ensure proper 301 redirects from non-canonical to canonical
- Set preferred domain in Search Console (or use canonical tags)

### 5. Not Fixing Issues Before Requesting Indexing

**Problem**: Requesting indexing while crawl errors or noindex tags are still present.

**Why It's Bad**:
- Request will fail or be ignored
- Wastes one of your limited daily requests
- Delays actual indexing

**Solution**:
- Always use "Test Live URL" to verify fixes before requesting indexing
- Check for noindex tags, robots.txt blocks, and errors
- Ensure page is fully ready for indexing
- Only request indexing after confirming all issues are resolved

## Troubleshooting

### Problem: "Indexing request failed"

**Symptoms**: Error message when clicking "Request Indexing" button.

**Possible Causes**:
- Daily rate limit reached for your property
- URL is blocked by robots.txt
- URL has noindex directive
- Network connectivity issue

**Resolution**:
1. Check if you've exceeded daily request quota (wait 24 hours)
2. Verify URL is not blocked by robots.txt
3. Remove any noindex meta tags or headers
4. Try again later if network issue
5. Submit URL via sitemap as alternative method

### Problem: "Test Live URL" shows different results than indexed version

**Symptoms**: Live test passes but indexed version shows errors.

**Possible Causes**:
- Recent fixes haven't been re-crawled yet
- Cached version in Google's index is outdated
- Intermittent server issues during original crawl

**Resolution**:
1. This is actually a good sign - your fixes are working
2. Request indexing to update Google's cached version
3. Wait 1-7 days for re-crawl and re-indexing
4. Re-inspect to verify updated version is indexed

### Problem: Canonical URL doesn't match expectation

**Symptoms**: Google selects a different canonical URL than you specified.

**Possible Causes**:
- Conflicting canonical signals (tags, redirects, sitemaps)
- Duplicate or near-duplicate content
- Stronger signals pointing to alternate URL

**Resolution**:
1. Review all canonical tags on the page and duplicates
2. Ensure consistent canonical signals across:
   - `<link rel="canonical">` tags
   - Sitemap submissions
   - Internal linking patterns
   - 301 redirects
3. Consolidate duplicate content to single canonical version
4. Request indexing for preferred canonical URL
5. Monitor over 2-4 weeks to see if Google respects your signal

### Problem: Page shows as indexed but doesn't appear in search

**Symptoms**: "URL is on Google" status but page isn't in search results.

**Possible Causes**:
- Low-quality content signals
- Strong competition for target keywords
- Recent indexing (not yet ranking)
- Manual action or algorithmic filter

**Resolution**:
1. Check for Manual Actions in Search Console
2. Improve content quality and uniqueness
3. Build relevant backlinks to the page
4. Optimize title and meta description for target keywords
5. Be patient - indexing doesn't guarantee immediate ranking
6. Use site:yoururl.com search to verify page is in index

## Integration Notes

This skill integrates with other SEO and Search Console workflows:

- **After fixing crawl errors**: Use this tool to verify fixes before requesting re-indexing
- **Before site migrations**: Inspect key URLs on old site to understand current indexing state
- **After migrations**: Verify new URLs are being indexed correctly
- **With sitemap submissions**: Inspect URLs from submitted sitemaps to ensure proper indexing
- **For technical SEO audits**: Validate that key pages are crawlable and indexable
- **With structured data testing**: Verify structured data is detected after implementation

## Quality Standards

When using this skill, ensure:

- ✅ All URLs inspected belong to verified Search Console properties
- ✅ Fixes are tested with "Test Live URL" before requesting indexing
- ✅ Rendered page screenshot is reviewed for important pages
- ✅ Indexing requests are limited to high-priority pages only
- ✅ Issues are fully resolved before requesting re-indexing
- ✅ Both mobile and desktop versions are checked for responsive sites
- ✅ Canonical URLs match intended site structure
- ✅ Documentation of inspection results for important pages

## Version History

- **1.0.0** (2026-01-22): Initial skill creation from Google Search Central documentation

## Additional Resources

- [Google Search Console Help](https://support.google.com/webmasters)
- [URL Inspection Tool Official Documentation](https://support.google.com/webmasters/answer/9012289)
- [How Google Search Works](https://www.google.com/search/howsearchworks/)
- [Robots.txt Tester](https://support.google.com/webmasters/answer/6062598)
- [Rich Results Test](https://search.google.com/test/rich-results)
