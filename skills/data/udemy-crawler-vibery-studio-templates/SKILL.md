---
name: udemy-crawler
description: Extract Udemy course content to markdown. Use when user asks to scrape/crawl Udemy course pages.
---

# Udemy Course Crawler

Extract Udemy course data using Chrome DevTools skill.

## Prerequisites

- Chrome DevTools skill installed and working
- `cd .claude/skills/chrome-devtools/scripts && npm install`

## Strategy

- **Visible browser required** - Cloudflare blocks headless
- **networkidle2** - Dynamic page load
- **Scroll + expand** - Lazy-loaded curriculum
- **Text parsing** - CSS selectors obfuscated

## Usage

```bash
cd .claude/skills/chrome-devtools/scripts
```

### Step 1: Basic Info

```bash
node evaluate.js \
  --url "https://www.udemy.com/course/COURSE-SLUG/" \
  --headless false \
  --timeout 60000 \
  --wait-until networkidle2 \
  --script '(function() {
    return {
      title: document.querySelector("h1")?.textContent?.trim() || "",
      headline: document.querySelector("[data-purpose=\"lead-headline\"]")?.textContent?.trim() || "",
      rating: document.querySelector("[data-purpose=\"rating-number\"]")?.textContent?.trim() || "",
      students: document.querySelector("[data-purpose=\"enrollment\"]")?.textContent?.trim() || "",
      instructor: document.querySelector("[data-purpose=\"instructor-name-top\"] a")?.textContent?.trim() || "",
      price: document.querySelector("[data-purpose=\"course-price-text\"] span span")?.textContent?.trim() || "",
      lastUpdated: document.querySelector("[data-purpose=\"last-update-date\"]")?.textContent?.trim() || "",
      language: document.querySelector("[data-purpose=\"lead-course-locale\"]")?.textContent?.trim() || "",
      whatYouWillLearn: Array.from(document.querySelectorAll("[data-purpose=\"objective\"] span")).map(el => el.textContent?.trim()).filter(Boolean),
      targetAudience: Array.from(document.querySelectorAll("[data-purpose=\"target-audience\"] li")).map(el => el.textContent?.trim()).filter(Boolean)
    };
  })()'
```

### Step 2: Curriculum + Details

```bash
node evaluate.js \
  --url "https://www.udemy.com/course/COURSE-SLUG/" \
  --headless false \
  --timeout 120000 \
  --wait-until networkidle2 \
  --script '(async function() {
    window.scrollTo(0, 1200);
    await new Promise(r => setTimeout(r, 1000));
    const expandAll = Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Expand all"));
    if (expandAll) { expandAll.click(); await new Promise(r => setTimeout(r, 3000)); }
    window.scrollTo(0, 5000);
    await new Promise(r => setTimeout(r, 1000));
    const mainContent = document.getElementById("main-content-anchor");
    const parent = mainContent ? mainContent.closest("div") : document.body;
    const fullText = parent.textContent;
    const currStart = fullText.indexOf("Course content");
    const currEnd = fullText.indexOf("Requirements") > currStart ? fullText.indexOf("Requirements") : fullText.indexOf("Who this course");
    const descStart = fullText.indexOf("Description");
    const descEnd = fullText.indexOf("Who this course");
    const reqStart = fullText.indexOf("Requirements");
    const reqEnd = fullText.indexOf("Description");
    const targetStart = fullText.indexOf("Who this course is for");
    return {
      curriculum: fullText.substring(currStart, currEnd).replace(/\s+/g, " ").trim(),
      requirements: fullText.substring(reqStart, reqEnd).replace(/\s+/g, " ").trim(),
      description: fullText.substring(descStart, descEnd).replace(/\s+/g, " ").substring(0, 3000).trim(),
      targetAudience: fullText.substring(targetStart, targetStart + 1500).replace(/\s+/g, " ").trim()
    };
  })()'
```

## Output Template

```markdown
# {title}

**URL:** {url}

## Course Info

- **Instructor:** {instructor}
- **Rating:** {rating} ({students})
- **Language:** {language}
- **Price:** {price}
- **Last Updated:** {lastUpdated}

## What You'll Learn

{whatYouWillLearn as bullets}

## Course Content

{curriculum parsed into sections}

## Requirements

{requirements as bullets}

## Description

{description}

## Target Audience

{targetAudience as bullets}
```

## Key Notes

- `data-purpose` attributes stable for: rating, enrollment, objectives
- Curriculum uses dynamic class names - text parsing only
- 3s delay after expanding sections
- Scroll required to load lazy content
