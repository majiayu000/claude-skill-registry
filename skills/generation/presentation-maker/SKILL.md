---
name: Presentation Maker
slug: presentation-maker
description: Generate PowerPoint presentations with slides, layouts, charts, and multimedia
category: document-creation
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create presentation"
  - "generate powerpoint"
  - "make slides"
  - "build pptx"
  - "create deck"
tags:
  - powerpoint
  - presentations
  - slides
  - pptx
  - keynote
---

# Presentation Maker

The Presentation Maker skill enables automated creation of professional PowerPoint presentations (.pptx) with custom layouts, themes, charts, images, and multimedia. Using libraries like `pptxgenjs`, this skill handles everything from simple slide decks to complex presentations with data visualizations and animations.

Create pitch decks, training materials, reports, project updates, and any presentation content programmatically. Support for master slides, themes, charts, tables, images, shapes, and speaker notes makes this a complete solution for presentation automation.

## Core Workflows

### Workflow 1: Create Basic Presentation
**Purpose:** Build a simple presentation with title and content slides

**Steps:**
1. Import `pptxgenjs` and create Presentation instance
2. Define presentation properties (title, author, company)
3. Add title slide with company branding
4. Add content slides with bullet points
5. Apply consistent theme and fonts
6. Add slide numbers
7. Export to .pptx file

**Implementation:**
```javascript
const PptxGenJS = require('pptxgenjs');

function createBasicPresentation(content, outputPath) {
  const pptx = new PptxGenJS();

  // Set presentation properties
  pptx.author = 'Company Name';
  pptx.company = 'Company Name';
  pptx.subject = content.subject;
  pptx.title = content.title;

  // Title slide
  let slide = pptx.addSlide();
  slide.background = { color: '2C3E50' };
  slide.addText(content.title, {
    x: 0.5,
    y: 2.5,
    w: '90%',
    h: 1.5,
    fontSize: 44,
    bold: true,
    color: 'FFFFFF',
    align: 'center'
  });
  slide.addText(content.subtitle, {
    x: 0.5,
    y: 4.0,
    w: '90%',
    fontSize: 24,
    color: 'BDC3C7',
    align: 'center'
  });

  // Content slides
  content.slides.forEach(slideData => {
    let slide = pptx.addSlide();

    // Title
    slide.addText(slideData.title, {
      x: 0.5,
      y: 0.5,
      w: '90%',
      h: 0.75,
      fontSize: 32,
      bold: true,
      color: '2C3E50'
    });

    // Bullet points
    slide.addText(slideData.bullets, {
      x: 0.5,
      y: 1.5,
      w: '90%',
      h: 4.0,
      fontSize: 18,
      bullet: true,
      color: '34495E'
    });

    // Slide number
    slide.addText(`${pptx.getSlideNumber()}`, {
      x: 9.0,
      y: 7.0,
      w: 0.5,
      h: 0.3,
      fontSize: 12,
      color: '95A5A6',
      align: 'right'
    });
  });

  pptx.writeFile({ fileName: outputPath });
}
```

### Workflow 2: Add Charts and Data Visualizations
**Purpose:** Create slides with embedded charts from data

**Steps:**
1. Create presentation
2. Prepare chart data (labels and values)
3. Add chart slide with title
4. Define chart type (bar, line, pie, scatter, etc.)
5. Configure chart options (colors, legend, axes)
6. Add data labels and formatting
7. Position chart on slide

**Implementation:**
```javascript
function createPresentationWithCharts(data, outputPath) {
  const pptx = new PptxGenJS();

  // Bar chart slide
  let slide = pptx.addSlide();
  slide.addText('Quarterly Revenue', {
    x: 0.5, y: 0.5, w: '90%', fontSize: 32, bold: true
  });

  const chartData = [
    {
      name: 'Revenue',
      labels: data.quarters,
      values: data.revenue
    }
  ];

  slide.addChart(pptx.ChartType.bar, chartData, {
    x: 1.0,
    y: 1.5,
    w: 8.0,
    h: 4.5,
    chartColors: ['2E74B5'],
    showTitle: false,
    showLegend: true,
    legendPos: 'b',
    valAxisMaxVal: Math.max(...data.revenue) * 1.2,
    dataLabelFormatCode: '$#,##0',
    showValue: true
  });

  // Pie chart slide
  slide = pptx.addSlide();
  slide.addText('Market Share', {
    x: 0.5, y: 0.5, w: '90%', fontSize: 32, bold: true
  });

  const pieData = [
    { name: 'Product A', labels: ['Share'], values: [35] },
    { name: 'Product B', labels: ['Share'], values: [28] },
    { name: 'Product C', labels: ['Share'], values: [22] },
    { name: 'Others', labels: ['Share'], values: [15] }
  ];

  slide.addChart(pptx.ChartType.pie, pieData, {
    x: 2.0,
    y: 1.5,
    w: 6.0,
    h: 4.5,
    showPercent: true,
    chartColors: ['2E74B5', '5DA5DA', '60BD68', 'F17CB0']
  });

  // Line chart for trends
  slide = pptx.addSlide();
  slide.addText('Growth Trend', {
    x: 0.5, y: 0.5, w: '90%', fontSize: 32, bold: true
  });

  const lineData = [
    {
      name: '2024',
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      values: [10, 15, 13, 18, 22, 25]
    },
    {
      name: '2025',
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      values: [12, 18, 16, 22, 27, 32]
    }
  ];

  slide.addChart(pptx.ChartType.line, lineData, {
    x: 1.0,
    y: 1.5,
    w: 8.0,
    h: 4.5,
    lineSmooth: true,
    chartColors: ['2E74B5', 'E74C3C']
  });

  pptx.writeFile({ fileName: outputPath });
}
```

### Workflow 3: Create Presentation from Template
**Purpose:** Use a master slide template for consistent branding

**Steps:**
1. Load or define master slide layouts
2. Set theme colors and fonts
3. Define slide layouts (title, content, two-column, etc.)
4. Create slides using predefined layouts
5. Apply company branding consistently
6. Add footer and logo to all slides
7. Export with template applied

**Implementation:**
```javascript
function createFromTemplate(content, outputPath) {
  const pptx = new PptxGenJS();

  // Define theme colors
  pptx.defineLayout({ name: 'CUSTOM', width: 10, height: 5.625 });
  pptx.layout = 'CUSTOM';

  // Define master slide
  const masterSlide = pptx.defineSlideMaster({
    title: 'MASTER_SLIDE',
    background: { color: 'FFFFFF' },
    objects: [
      // Company logo
      { image: { x: 0.5, y: 0.2, w: 1.0, h: 0.4, path: 'company-logo.png' } },
      // Footer
      { text: { text: 'Company Confidential', options: { x: 0.5, y: 5.0, fontSize: 10, color: '95A5A6' } } }
    ]
  });

  // Use master slide for content
  content.slides.forEach(slideData => {
    let slide = pptx.addSlide({ masterName: 'MASTER_SLIDE' });

    slide.addText(slideData.title, {
      x: 2.0, y: 0.5, w: 7.5, fontSize: 28, bold: true, color: '2C3E50'
    });

    slide.addText(slideData.content, {
      x: 2.0, y: 1.5, w: 7.5, fontSize: 16, color: '34495E'
    });
  });

  pptx.writeFile({ fileName: outputPath });
}
```

### Workflow 4: Add Images and Media
**Purpose:** Include images, shapes, and multimedia content

**Steps:**
1. Create presentation
2. Add image slides with captions
3. Resize and position images
4. Add shapes (rectangles, circles, arrows)
5. Layer elements with z-index
6. Add hyperlinks to images
7. Insert video placeholders (if supported)

**Implementation:**
```javascript
function createWithMedia(content, outputPath) {
  const pptx = new PptxGenJS();

  // Image slide
  let slide = pptx.addSlide();
  slide.addText(content.title, {
    x: 0.5, y: 0.5, fontSize: 32, bold: true
  });

  // Add image
  slide.addImage({
    path: content.imagePath,
    x: 1.5,
    y: 1.5,
    w: 7.0,
    h: 4.0,
    sizing: { type: 'contain', w: 7.0, h: 4.0 }
  });

  // Add caption
  slide.addText(content.caption, {
    x: 1.5,
    y: 5.7,
    w: 7.0,
    fontSize: 14,
    italic: true,
    align: 'center',
    color: '7F8C8D'
  });

  // Slide with shapes
  slide = pptx.addSlide();

  // Background shape
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.5,
    y: 1.5,
    w: 9.0,
    h: 4.5,
    fill: { color: 'ECF0F1' },
    line: { color: '3498DB', width: 2 }
  });

  // Arrow shapes for process flow
  slide.addShape(pptx.ShapeType.rightArrow, {
    x: 1.0,
    y: 3.0,
    w: 2.0,
    h: 1.0,
    fill: { color: '3498DB' }
  });

  slide.addText('Step 1', {
    x: 1.3, y: 3.3, w: 1.4, fontSize: 16, color: 'FFFFFF', bold: true, align: 'center'
  });

  pptx.writeFile({ fileName: outputPath });
}
```

### Workflow 5: Add Tables and Data
**Purpose:** Display structured data in table format

**Steps:**
1. Create slide
2. Define table structure (rows and columns)
3. Add header row with styling
4. Populate data rows
5. Apply cell formatting (colors, borders, alignment)
6. Set column widths
7. Add table title

**Implementation:**
```javascript
function createWithTables(data, outputPath) {
  const pptx = new PptxGenJS();

  let slide = pptx.addSlide();
  slide.addText('Project Status', {
    x: 0.5, y: 0.5, fontSize: 32, bold: true
  });

  // Define table rows
  const tableData = [
    [
      { text: 'Task', options: { bold: true, fill: '2C3E50', color: 'FFFFFF' } },
      { text: 'Owner', options: { bold: true, fill: '2C3E50', color: 'FFFFFF' } },
      { text: 'Status', options: { bold: true, fill: '2C3E50', color: 'FFFFFF' } },
      { text: 'Due Date', options: { bold: true, fill: '2C3E50', color: 'FFFFFF' } }
    ]
  ];

  // Add data rows
  data.tasks.forEach(task => {
    const statusColor = task.status === 'Complete' ? '27AE60' :
                       task.status === 'In Progress' ? 'F39C12' : 'E74C3C';

    tableData.push([
      { text: task.name },
      { text: task.owner },
      { text: task.status, options: { fill: statusColor, color: 'FFFFFF' } },
      { text: task.dueDate }
    ]);
  });

  slide.addTable(tableData, {
    x: 0.5,
    y: 1.5,
    w: 9.0,
    colW: [3.0, 2.0, 2.0, 2.0],
    border: { pt: 1, color: 'BDC3C7' },
    fontSize: 14,
    align: 'center',
    valign: 'middle'
  });

  pptx.writeFile({ fileName: outputPath });
}
```

### Workflow 6: Add Speaker Notes
**Purpose:** Include presenter notes for each slide

**Steps:**
1. Create slides with content
2. Add speaker notes to each slide
3. Format notes with key talking points
4. Include timing suggestions
5. Add references and sources
6. Export with notes included

**Implementation:**
```javascript
content.slides.forEach(slideData => {
  let slide = pptx.addSlide();

  slide.addText(slideData.title, {
    x: 0.5, y: 0.5, fontSize: 32, bold: true
  });

  slide.addText(slideData.content, {
    x: 0.5, y: 1.5, fontSize: 18, bullet: true
  });

  // Add speaker notes
  slide.addNotes(`
    Key Points:
    - ${slideData.notes.keyPoints.join('\n    - ')}

    Timing: ${slideData.notes.timing}

    Additional Context:
    ${slideData.notes.context}
  `);
});
```

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create presentation | "create powerpoint with [slides]" |
| Add chart slide | "add chart to presentation" |
| Insert image | "add image [file] to slide" |
| Create table | "add table with [data]" |
| From template | "use template for presentation" |
| Add shapes | "add shapes to slide" |
| Speaker notes | "add notes to slides" |
| Export | "save presentation as [name]" |

## Best Practices

- **Consistency:** Use templates and master slides for uniform appearance
- **Simplicity:** Keep slides clean with minimal text (6x6 rule: max 6 bullets, 6 words each)
- **Visuals:** Use charts and images to convey information effectively
- **Color Scheme:** Stick to 2-3 primary colors aligned with brand
- **Font Size:** Minimum 18pt for body text, 28pt+ for headings
- **Contrast:** Ensure text is readable against backgrounds
- **Slide Count:** Aim for one slide per minute of presentation time
- **Data Visualization:** Choose appropriate chart types for data
- **White Space:** Don't overcrowd slides; use white space effectively
- **Animations:** Use sparingly and only when they add value (not supported in pptxgenjs)
- **File Size:** Compress images before embedding
- **Accessibility:** Include alt text for images when possible

## Common Patterns

**Pitch Deck:**
```javascript
const pitchSlides = [
  { type: 'title', title: 'Company Name', subtitle: 'Investor Pitch' },
  { type: 'content', title: 'Problem', bullets: ['Pain point 1', 'Pain point 2'] },
  { type: 'content', title: 'Solution', bullets: ['Our approach', 'Key benefits'] },
  { type: 'chart', title: 'Market Size', chartType: 'bar' },
  { type: 'content', title: 'Business Model', bullets: ['Revenue streams'] },
  { type: 'chart', title: 'Financial Projections', chartType: 'line' },
  { type: 'content', title: 'Team', image: 'team-photos.png' },
  { type: 'content', title: 'Ask', bullets: ['Funding amount', 'Use of funds'] }
];
```

**Training Presentation:**
```javascript
slides.forEach((slide, idx) => {
  let s = pptx.addSlide();
  s.addText(slide.title, { x: 0.5, y: 0.5, fontSize: 28, bold: true });
  s.addText(slide.content, { x: 0.5, y: 1.5, fontSize: 16 });
  if (slide.example) {
    s.addText('Example:', { x: 0.5, y: 4.0, fontSize: 14, italic: true });
    s.addText(slide.example, { x: 0.5, y: 4.4, fontSize: 14 });
  }
  s.addNotes(slide.trainerNotes);
});
```

## Dependencies

Install required packages:
```bash
npm install pptxgenjs
```

Alternative libraries:
```bash
npm install officegen  # Legacy option
npm install node-pptx  # Another alternative
```

## Error Handling

- **File Paths:** Verify image paths exist before adding to slides
- **Data Validation:** Ensure chart data is properly formatted
- **Memory:** For presentations with many high-res images, monitor memory usage
- **Compatibility:** Test output in PowerPoint, Google Slides, and Keynote
- **Chart Limits:** Some chart types have data point limitations
- **Text Overflow:** Monitor text length to prevent overflow on slides

## Performance Tips

- Compress images before adding to presentation
- Reuse image objects when same image appears on multiple slides
- Batch slide creation operations
- Use web-optimized images (72-96 DPI sufficient for screens)
- Limit number of slides in a single file (<100 slides)

## Advanced Features

**Custom Layouts:**
```javascript
const layout = pptx.defineSlideMaster({
  title: 'TWO_COLUMN',
  background: { color: 'FFFFFF' },
  objects: [
    { rect: { x: 0, y: 0, w: 5, h: 5.625, fill: 'F0F0F0' } },
    { rect: { x: 5, y: 0, w: 5, h: 5.625, fill: 'FFFFFF' } }
  ]
});
```

**Hyperlinks:**
```javascript
slide.addText('Visit Website', {
  x: 1, y: 3, fontSize: 18,
  hyperlink: { url: 'https://example.com', tooltip: 'Click to visit' },
  color: '0000FF',
  underline: true
});
```

**Gradients:**
```javascript
slide.background = {
  fill: { type: 'solid', color: '2C3E50' },
  transparency: 0
};
```