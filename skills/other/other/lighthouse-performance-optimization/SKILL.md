---
name: lighthouse-performance-optimization
description: "Use when optimizing website performance. Run Google Lighthouse audits via MCP to measure metrics, identify bottlenecks, and iterate on improvements."
---

# Lighthouse Performance Optimization

## Core Principle

**Measure, analyze, optimize, verify.** Use data-driven performance insights from Lighthouse to create fast, accessible, SEO-friendly websites.

## Overview

Lighthouse MCP enables AI-assisted performance auditing by running Google Lighthouse through Claude Code. Get comprehensive reports on performance, accessibility, best practices, and SEO without leaving your development environment.

## When to Use This Skill

- **Performance optimization** - Improving load times, Core Web Vitals
- **Pre-deployment quality checks** - Validate before going live
- **Regression testing** - Ensure updates don't degrade performance
- **Accessibility audits** - Find and fix a11y issues
- **SEO validation** - Check search engine optimization
- **Best practices verification** - Ensure standards compliance
- **Progressive Web App (PWA) validation** - Check PWA requirements
- **Performance benchmarking** - Compare before/after changes

## Prerequisites

**Required:**
- Lighthouse MCP server installed (see `.mcp.json`)
- Target website accessible (local dev server or live URL)

**Verify MCP is available:**
```
Ask Claude: "Can you run a Lighthouse audit?"
```

## The Iron Laws

### 1. ALWAYS ESTABLISH BASELINE FIRST

**Before making ANY performance changes:**
```
1. Run Lighthouse audit on current state
2. Document baseline metrics
3. Identify top 3-5 issues
4. Make changes
5. Run audit again to verify improvement
```

❌ **NEVER:**
- Make changes without baseline metrics
- Optimize blindly without measuring
- Skip verification after changes

✅ **ALWAYS:**
- Document baseline scores
- Compare before/after results
- Verify improvements with data

### 2. FOCUS ON CORE WEB VITALS

**Google's key metrics:**
- **LCP (Largest Contentful Paint)**: < 2.5s (good), 2.5-4s (needs improvement), > 4s (poor)
- **FID (First Input Delay)**: < 100ms (good), 100-300ms (needs improvement), > 300ms (poor)
- **CLS (Cumulative Layout Shift)**: < 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)

**Authority**: These metrics directly impact search rankings and user experience.

### 3. ITERATIVE OPTIMIZATION

**One change at a time:**
```
1. Identify highest-impact issue
2. Implement fix
3. Re-run Lighthouse
4. Verify improvement
5. Move to next issue
```

**Why**: Isolate impact of each change, understand what works.

## Performance Optimization Protocol

### Step 1: Run Baseline Audit

**Template:**
```
I'm using the lighthouse-performance-optimization skill to audit [URL].

Running baseline Lighthouse audit...
```

**Ask Claude:**
```
"Run a Lighthouse audit on http://localhost:3000"
"Run a Lighthouse audit on https://example.com"
```

**Document results:**
```
Baseline Metrics:
- Performance Score: [0-100]
- Accessibility Score: [0-100]
- Best Practices Score: [0-100]
- SEO Score: [0-100]

Core Web Vitals:
- LCP: [X.X]s
- FID: [X]ms
- CLS: [X.XX]

Top Issues:
1. [Issue description] - Impact: [High/Medium/Low]
2. [Issue description] - Impact: [High/Medium/Low]
3. [Issue description] - Impact: [High/Medium/Low]
```

### Step 2: Analyze Results

**Focus areas by score:**

**Performance (0-49 = Poor, 50-89 = Needs Improvement, 90-100 = Good):**
- Slow server response times (TTFB)
- Large JavaScript bundles
- Unoptimized images
- Render-blocking resources
- Large DOM size
- Inefficient cache policies

**Accessibility (aim for 90+):**
- Missing alt text on images
- Low contrast ratios
- Missing ARIA labels
- Keyboard navigation issues
- Missing form labels

**Best Practices (aim for 90+):**
- Mixed HTTP/HTTPS content
- Deprecated APIs
- Browser errors in console
- Missing security headers
- Image aspect ratio issues

**SEO (aim for 90+):**
- Missing meta descriptions
- Non-crawlable links
- Missing structured data
- Mobile-unfriendly viewport
- Slow page speed

### Step 3: Prioritize Fixes

**Impact vs. Effort Matrix:**

**High Impact + Low Effort (DO FIRST):**
- Optimize images (compress, use WebP)
- Enable text compression (gzip/brotli)
- Add caching headers
- Defer non-critical JavaScript
- Add missing alt text

**High Impact + High Effort (DO SECOND):**
- Code splitting (reduce bundle size)
- Implement lazy loading
- Remove unused JavaScript
- Optimize third-party scripts
- Server-side rendering (SSR)

**Low Impact (DO LATER):**
- Minor accessibility improvements
- Non-critical best practices
- Small optimizations

### Step 4: Implement Fixes

**Common optimizations:**

#### Image Optimization
```bash
# Convert to WebP
npx @squoosh/cli --webp auto input.jpg

# Responsive images in HTML
<picture>
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

#### JavaScript Optimization
```javascript
// Code splitting with dynamic imports
const module = await import('./heavy-module.js');

// Defer non-critical scripts
<script src="analytics.js" defer></script>

// Lazy load components
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

#### CSS Optimization
```html
<!-- Inline critical CSS -->
<style>/* Critical above-fold CSS */</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

#### Caching Headers
```nginx
# Nginx example
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Step 5: Verify Improvements

**Re-run audit:**
```
Ask Claude: "Run another Lighthouse audit on [URL] to verify improvements"
```

**Compare results:**
```
Before → After:
- Performance: [X] → [Y] (+Z points)
- LCP: [X.X]s → [Y.Y]s (-Z.Z)s
- Bundle size: [X]kb → [Y]kb (-Z)kb

Improvements:
✅ [Fixed issue 1] - Score improved by X points
✅ [Fixed issue 2] - LCP reduced by X.Xs
⚠️  [Issue 3] - Still needs work

Next Steps:
- Address remaining issue 3
- Run audit again after fix
```

## Common Performance Patterns

### Pattern 1: Image-Heavy Site

**Symptoms:**
- Low performance score (< 50)
- High LCP (> 4s)
- Large transfer size

**Solution:**
```
1. Convert images to WebP/AVIF
2. Implement responsive images with srcset
3. Add lazy loading (loading="lazy")
4. Use modern image formats
5. Compress images (quality 80-85)
```

### Pattern 2: JavaScript-Heavy SPA

**Symptoms:**
- Large JavaScript bundle (> 500kb)
- Slow First Contentful Paint
- High Total Blocking Time

**Solution:**
```
1. Code splitting by route
2. Tree shaking (remove unused code)
3. Dynamic imports for heavy libraries
4. Defer non-critical JavaScript
5. Consider SSR/SSG for initial load
```

### Pattern 3: Third-Party Scripts

**Symptoms:**
- Slow TTFB
- Many external requests
- High Total Blocking Time

**Solution:**
```
1. Audit necessity of each third-party script
2. Load scripts asynchronously (async/defer)
3. Use facade pattern for heavy embeds (YouTube, maps)
4. Self-host critical third-party resources
5. Implement resource hints (preconnect, dns-prefetch)
```

### Pattern 4: Accessibility Issues

**Symptoms:**
- Accessibility score < 90
- Missing alt text
- Low contrast ratios

**Solution:**
```
1. Add alt text to all images
2. Ensure sufficient color contrast (WCAG AA: 4.5:1)
3. Add ARIA labels to interactive elements
4. Ensure keyboard navigation works
5. Add semantic HTML (header, nav, main, footer)
```

## Optimization Workflows

### Pre-Deployment Checklist

```
Before deploying to production:

[ ] Run Lighthouse audit on staging
[ ] Performance score > 90
[ ] Accessibility score > 90
[ ] Core Web Vitals all "Good"
[ ] No console errors
[ ] Mobile responsive (test mobile viewport)
[ ] All images have alt text
[ ] Meta descriptions present
[ ] Security headers configured
```

### Performance Budget Workflow

**Establish budgets:**
```
Performance Budget:
- Total page size: < 2MB
- JavaScript bundle: < 300kb
- Images total: < 1MB
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- Performance score: > 90
```

**Monitor with Lighthouse:**
```
1. Run audit weekly
2. Alert if metrics exceed budget
3. Investigate regressions immediately
4. Block merges that degrade performance
```

### A/B Testing Performance Changes

```
1. Run Lighthouse on current version (variant A)
2. Deploy change (variant B)
3. Run Lighthouse on new version
4. Compare metrics statistically
5. Keep change if improvement > 5%
6. Rollback if degradation detected
```

## Advanced Usage

### Lighthouse CI Integration

**For automated testing:**
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Lighthouse
        run: |
          npm install -g @lhci/cli
          lhci autorun
```

### Custom Lighthouse Config

**Ask Claude to use specific settings:**
```
"Run a Lighthouse audit with mobile emulation"
"Run a Lighthouse audit checking only performance and accessibility"
"Run a desktop Lighthouse audit"
```

### Performance Regression Detection

**Compare audits over time:**
```
Weekly Audit Log:
Week 1: Performance 92, LCP 2.1s
Week 2: Performance 89, LCP 2.4s ⚠️ REGRESSION
Week 3: Performance 94, LCP 1.8s ✅ IMPROVED
```

## Troubleshooting

### Audit Fails or Errors

**Common issues:**
- Site not accessible (check dev server running)
- Authentication required (use public staging URL)
- Timeout errors (site too slow, need to optimize first)

**Solutions:**
```
1. Verify URL is accessible
2. Check server is running
3. Try different URL (staging vs. production)
4. Increase timeout if very slow site
```

### Inconsistent Scores

**Scores vary between runs:**
- Network conditions change
- Server load varies
- Third-party scripts have latency

**Solutions:**
```
1. Run multiple audits (3-5)
2. Take average of scores
3. Focus on trends, not single values
4. Use controlled environment (local dev)
```

### Low Scores Despite Optimizations

**Still poor performance:**
```
1. Check server response time (TTFB)
2. Review hosting infrastructure
3. Enable CDN for static assets
4. Implement edge caching
5. Consider upgrading server resources
```

## Best Practices

1. **Run audits regularly** - Weekly or per major change
2. **Document baseline** - Always know your starting point
3. **Iterate incrementally** - One optimization at a time
4. **Verify improvements** - Re-run audit after each change
5. **Focus on Core Web Vitals** - These impact search rankings
6. **Test on real devices** - Desktop AND mobile
7. **Monitor production** - Audit live site, not just staging
8. **Set performance budgets** - Prevent regressions
9. **Automate in CI/CD** - Catch regressions early
10. **Share results with team** - Collective responsibility

## Integration with Other Skills

**Before optimizing:**
- `brainstorming` - Understand performance goals
- `writing-plans` - Plan optimization strategy

**During optimization:**
- `test-driven-development` - Write performance tests
- `code-review` - Review optimization code

**After optimization:**
- `verification-before-completion` - Verify improvements
- `git-workflow` - Commit with performance metrics

## Remember

**Performance is a feature, not an afterthought.**

- Users abandon slow sites (53% leave if load > 3s)
- Google penalizes slow sites in search rankings
- Fast sites have higher conversion rates
- Accessibility benefits everyone

Use Lighthouse MCP to make data-driven optimization decisions and create blazing-fast experiences.

---

**Resources:**
- [Web Vitals](https://web.dev/vitals/)
- [Lighthouse Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
