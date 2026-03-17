---
name: when-creating-presentations-use-pptx-generation
version: 1.0.0
description: Enterprise-grade PowerPoint deck generation using evidence-based prompting, workflow enforcement, constraint-based design
category: utilities
tags: [presentation, pptx, slides, enterprise, documentation]
agents: [coder, researcher]
difficulty: intermediate
estimated_duration: 25-40min
success_criteria:
  - Presentation generated with proper structure
  - All slides follow design constraints
  - Accessibility standards met (WCAG 2.1 AA)
  - Data visualization effective
validation_method: accessibility_scan
dependencies:
  - claude-flow@alpha
  - pptxgenjs
  - html2pptx (optional)
outputs:
  - PowerPoint file (.pptx)
  - Slide notes
  - Accessibility report
triggers:
  - Need professional presentation
  - Board deck required
  - Report generation
  - Data visualization needed
---

# PPTX Generation - Enterprise Presentation Creator

## Overview

Enterprise-grade PowerPoint deck generation system using evidence-based prompting techniques, workflow enforcement, and constraint-based design for professional presentations (board decks, reports, analyses). Supports 30+ slide decks with consistent visual quality and accessibility compliance.

## When to Use

- Creating board-level presentations
- Quarterly business reviews
- Technical documentation slides
- Data-heavy reports
- Executive summaries
- Client proposals
- Training materials

## Phase 1: Research Content (8 min)

### Objective
Gather and structure presentation information

### Agent: Researcher

**Step 1.1: Content Gathering**
```javascript
const contentStructure = {
  metadata: {
    title: 'Presentation Title',
    subtitle: 'Subtitle',
    author: 'Author Name',
    date: new Date(),
    audience: 'executive|technical|general',
    purpose: 'inform|persuade|instruct'
  },
  outline: [
    {
      section: 'Introduction',
      slides: ['Title', 'Agenda', 'Executive Summary']
    },
    {
      section: 'Main Content',
      slides: ['Key Points', 'Data Analysis', 'Recommendations']
    },
    {
      section: 'Conclusion',
      slides: ['Summary', 'Next Steps', 'Q&A']
    }
  ],
  dataPoints: extractDataPoints(),
  visualizations: identifyVisualizations()
};

await memory.store('pptx/content-structure', contentStructure);
```

**Step 1.2: Data Analysis**
```javascript
async function analyzeData(data) {
  return {
    tables: extractTables(data),
    charts: identifyChartOpportunities(data),
    trends: analyzeTrends(data),
    insights: generateInsights(data)
  };
}
```

### Validation Criteria
- [ ] Content structure defined
- [ ] Data points extracted
- [ ] Visualization types identified
- [ ] Outline complete

## Phase 2: Design Layout (7 min)

### Objective
Create presentation design following constraints

### Agent: Coder

**Step 2.1: Define Design System**
```javascript
const designSystem = {
  colors: {
    primary: '#2C3E50',
    secondary: '#3498DB',
    accent: '#E74C3C',
    text: '#2C3E50',
    background: '#FFFFFF'
  },
  fonts: {
    heading: { face: 'Calibri', size: 32, bold: true },
    subheading: { face: 'Calibri', size: 24, bold: true },
    body: { face: 'Calibri', size: 18 },
    caption: { face: 'Calibri', size: 14, italic: true }
  },
  layout: {
    marginX: 0.5,
    marginY: 0.5,
    titleY: 0.5,
    contentY: 1.5,
    spacing: 0.3
  },
  accessibility: {
    contrastRatio: 4.5, // WCAG 2.1 AA
    altText: true,
    readingOrder: true
  }
};

await memory.store('pptx/design-system', designSystem);
```

**Step 2.2: Create Slide Layouts**
```javascript
const slideLayouts = {
  title: {
    type: 'title',
    elements: [
      { type: 'text', content: '{title}', style: 'heading', position: { x: 1, y: 2.5 } },
      { type: 'text', content: '{subtitle}', style: 'subheading', position: { x: 1, y: 3.5 } }
    ]
  },
  content: {
    type: 'content',
    elements: [
      { type: 'text', content: '{title}', style: 'heading', position: { x: 0.5, y: 0.5 } },
      { type: 'text', content: '{body}', style: 'body', position: { x: 0.5, y: 1.5 } }
    ]
  },
  twoColumn: {
    type: 'two-column',
    elements: [
      { type: 'text', content: '{left}', position: { x: 0.5, y: 1.5, w: 4.5 } },
      { type: 'text', content: '{right}', position: { x: 5.5, y: 1.5, w: 4.5 } }
    ]
  },
  dataVisualization: {
    type: 'chart',
    elements: [
      { type: 'text', content: '{title}', style: 'heading', position: { x: 0.5, y: 0.5 } },
      { type: 'chart', chartData: '{data}', position: { x: 1, y: 1.5, w: 8, h: 4 } }
    ]
  }
};

await memory.store('pptx/layouts', slideLayouts);
```

### Validation Criteria
- [ ] Design system defined
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Layouts created
- [ ] Accessibility constraints applied

## Phase 3: Generate Slides (12 min)

### Objective
Create PowerPoint file with all slides

### Agent: Coder

**Step 3.1: Initialize Presentation**
```javascript
const pptxgen = require('pptxgenjs');
const pres = new pptxgen();

// Apply design system
pres.layout = 'LAYOUT_WIDE';
pres.author = contentStructure.metadata.author;
pres.title = contentStructure.metadata.title;
pres.subject = contentStructure.metadata.purpose;
```

**Step 3.2: Generate Slides**
```javascript
async function generateSlides(outline, designSystem, layouts) {
  for (const section of outline) {
    for (const slideData of section.slides) {
      const layout = selectLayout(slideData.type, layouts);
      const slide = pres.addSlide();

      // Add title
      slide.addText(slideData.title, {
        x: layout.title.x,
        y: layout.title.y,
        w: layout.title.w || 9,
        h: layout.title.h || 0.75,
        fontSize: designSystem.fonts.heading.size,
        bold: designSystem.fonts.heading.bold,
        color: designSystem.colors.text
      });

      // Add content based on slide type
      if (slideData.type === 'content') {
        slide.addText(slideData.content, {
          x: layout.content.x,
          y: layout.content.y,
          w: layout.content.w || 9,
          h: layout.content.h || 4,
          fontSize: designSystem.fonts.body.size,
          color: designSystem.colors.text,
          bullet: slideData.bullet || false
        });
      }

      // Add visualizations
      if (slideData.chart) {
        slide.addChart(slideData.chart.type, slideData.chart.data, {
          x: layout.chart.x,
          y: layout.chart.y,
          w: layout.chart.w,
          h: layout.chart.h,
          showTitle: true,
          showLegend: true
        });
      }

      // Add accessibility
      if (slideData.altText) {
        slide.addNotes(slideData.altText); // Alt text for screen readers
      }
    }
  }

  return pres;
}
```

**Step 3.3: Add Data Visualizations**
```javascript
function addChart(slide, chartData, position, designSystem) {
  const chartConfig = {
    x: position.x,
    y: position.y,
    w: position.w,
    h: position.h,
    chartColors: [
      designSystem.colors.primary,
      designSystem.colors.secondary,
      designSystem.colors.accent
    ],
    showLabel: true,
    showValue: true,
    showLegend: true,
    legendPos: 'r',
    valAxisMaxVal: Math.max(...chartData.values) * 1.2
  };

  slide.addChart(chartData.type, chartData.data, chartConfig);
}
```

### Validation Criteria
- [ ] All slides generated
- [ ] Design system applied consistently
- [ ] Charts and visuals rendered
- [ ] Alt text added for accessibility

## Phase 4: Validate Quality (8 min)

### Objective
Ensure accessibility and quality standards

### Agent: Coder

**Step 4.1: Accessibility Scan**
```javascript
async function scanAccessibility(pres) {
  const issues = [];

  for (const slide of pres.slides) {
    // Check color contrast
    for (const element of slide.elements) {
      if (element.color && element.background) {
        const contrast = calculateContrastRatio(element.color, element.background);
        if (contrast < 4.5) {
          issues.push({
            slide: slide.index,
            type: 'COLOR_CONTRAST',
            severity: 'HIGH',
            message: `Contrast ratio ${contrast} < 4.5 (WCAG 2.1 AA)`
          });
        }
      }
    }

    // Check alt text
    if (slide.hasImages() && !slide.hasAltText()) {
      issues.push({
        slide: slide.index,
        type: 'MISSING_ALT_TEXT',
        severity: 'HIGH',
        message: 'Images missing alt text for screen readers'
      });
    }

    // Check reading order
    if (!slide.hasReadingOrder()) {
      issues.push({
        slide: slide.index,
        type: 'READING_ORDER',
        severity: 'MEDIUM',
        message: 'Reading order not defined'
      });
    }
  }

  await memory.store('pptx/accessibility-issues', issues);
  return issues;
}
```

**Step 4.2: Quality Checks**
```javascript
const qualityChecks = {
  consistency: checkDesignConsistency(pres),
  readability: checkTextReadability(pres),
  dataIntegrity: validateChartData(pres),
  fileSize: checkFileSize(pres),
  slideCount: pres.slides.length <= 40 // Optimal for attention
};

const passed = Object.values(qualityChecks).every(check => check.passed);
```

### Validation Criteria
- [ ] WCAG 2.1 AA compliance
- [ ] No critical accessibility issues
- [ ] Quality checks passed
- [ ] File size reasonable

## Phase 5: Export Final (5 min)

### Objective
Generate final presentation file

### Agent: Coder

**Step 5.1: Generate PPTX File**
```javascript
async function exportPresentation(pres, filename) {
  await pres.writeFile({ fileName: filename });
  console.log(`✅ Presentation saved: ${filename}`);

  // Generate accessibility report
  const report = {
    filename,
    slides: pres.slides.length,
    accessibilityIssues: await memory.retrieve('pptx/accessibility-issues'),
    qualityScore: calculateQualityScore(pres),
    wcagCompliance: 'AA',
    generatedAt: new Date()
  };

  await fs.writeFile(
    filename.replace('.pptx', '-accessibility-report.json'),
    JSON.stringify(report, null, 2)
  );
}
```

**Step 5.2: Generate Documentation**
```markdown
# Presentation Documentation

## Metadata
- Title: ${metadata.title}
- Slides: ${slideCount}
- Generated: ${timestamp}

## Design System
- Colors: ${colors}
- Fonts: ${fonts}
- Accessibility: WCAG 2.1 AA

## Slide Breakdown
${outline.map(section => `
### ${section.name}
${section.slides.map(slide => `- ${slide.title}`).join('\n')}
`).join('\n')}

## Quality Metrics
- Accessibility Score: ${accessibilityScore}/100
- Readability Score: ${readabilityScore}/100
- Design Consistency: ${consistencyScore}/100
```

### Validation Criteria
- [ ] PPTX file generated
- [ ] Accessibility report created
- [ ] Documentation complete
- [ ] Ready for distribution

## Success Metrics

- All slides generated successfully
- WCAG 2.1 AA compliance achieved
- Quality score > 85/100
- File size < 50MB

## Skill Completion

Outputs:
1. **presentation.pptx**: Final PowerPoint file
2. **accessibility-report.json**: Compliance analysis
3. **presentation-doc.md**: Generation documentation
4. **slide-notes.txt**: Speaker notes

Complete when PPTX generated with WCAG 2.1 AA compliance.
