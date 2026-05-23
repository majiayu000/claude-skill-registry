---
name: paper-writing
description: Scientific manuscript preparation for geoscience journals. Includes IMRAD structure, journal styles (Nature, EPSL, GSA), citation formatting, figure standards, and supplementary materials.
triggers:
  - write paper
  - draft manuscript
  - format citation
  - journal style
  - IMRAD
  - GSA style
  - bibliography
  - DOI
location: user
---

# Paper Writing for Geoscience Research

## When to Use This Skill

Invoke when:
- Drafting manuscript sections
- Formatting citations and bibliography
- Preparing figures and tables
- Adapting to journal-specific styles
- Organizing supplementary materials

## IMRAD Structure

Standard structure for geoscience papers:

### Introduction
- **Hook**: Why should anyone care? (1-2 paragraphs)
- **Context**: What's known? What's the gap?
- **Objective**: What question are we answering?
- **Approach**: Brief methodology preview
- **Findings preview**: "Here we show that..."

### Methods
- **Study sites**: Location, geology, relevance
- **Data collection**: What, when, how
- **Analytical methods**: Lab procedures, quality control
- **Statistical analysis**: Tests used, software
- **Reproducibility**: Data availability statement

### Results
- Present findings WITHOUT interpretation
- Lead with most important result
- One main finding per paragraph
- Reference all figures/tables
- Use past tense

### Discussion
- **Interpretation**: What do results mean?
- **Comparison**: How do they fit prior work?
- **Implications**: Why does this matter?
- **Limitations**: What could be wrong?
- **Future work**: What's next?

### Conclusions
- 3-5 key takeaways
- No new information
- Broader significance

## Journal-Specific Styles

### Nature Geoscience
- **Length**: 3,000 words main text
- **Abstract**: 150 words, no refs
- **Methods**: Separate section (online)
- **Refs**: Numbered, Nature style
- **Style**: High impact, accessible to broad audience

### EPSL (Earth and Planetary Science Letters)
- **Length**: 6,000-8,000 words
- **Abstract**: 300 words, structured OK
- **Keywords**: 5-6 required
- **Refs**: Author-year (Harvard style)
- **Style**: Technical, detailed methods OK

### GSA Bulletin
- **Length**: 8,000-12,000 words
- **Abstract**: 250 words
- **Refs**: Author-year, GSA style
- **Supplementary**: Encouraged for data
- **Style**: Regional focus, detailed stratigraphy

## Citation Formatting

### Author-Year (Harvard/GSA)
```
In-text: (Smith and Jones, 2020) or Smith and Jones (2020)
Multiple: (Smith, 2018; Jones, 2019; Chen et al., 2020)
Three+ authors: (Chen et al., 2020)

Reference list:
Smith, J.A., and Jones, B.C., 2020, Title of paper: Journal Name, v. 50, p. 100-120, doi:10.1234/example.
```

### Numbered (Nature)
```
In-text: Previous work¹⁻³ showed...

Reference list:
1. Smith, J.A. & Jones, B.C. Title of paper. J. Name 50, 100-120 (2020).
```

### Database Citations

**SISAL v3**:
> Comas-Bru, L., et al. (2020). SISALv2: A comprehensive speleothem isotope database with multiple age-depth models. Earth System Science Data, 12, 2579-2606.

**USGS Earthquake Catalog**:
> U.S. Geological Survey (2023). Earthquake Hazards Program. https://earthquake.usgs.gov

**DISS**:
> DISS Working Group (2021). Database of Individual Seismogenic Sources (DISS), Version 3.3.1: A compilation of potential sources for earthquakes larger than M 5.5 in Italy and surrounding areas. https://diss.ingv.it

## DOI Resolution

To get citation metadata from DOI:
1. Use CrossRef API: `https://api.crossref.org/works/{DOI}`
2. Extract: authors, title, journal, year, volume, pages
3. Format according to target journal style

**Example**:
```
DOI: 10.1038/ngeo2681
→ Toohey, M. & Sigl, M. Volcanic stratospheric sulfur injections and aerosol optical depth from 500 BCE to 1900 CE. Earth Syst. Sci. Data 9, 809-831 (2017).
```

## Figure Standards

### General Guidelines
- **Resolution**: 300+ DPI for publication
- **Width**: Single column (8.5 cm) or double (17.5 cm)
- **Font**: Sans-serif (Arial, Helvetica), 8-10 pt
- **Colors**: Colorblind-friendly palette
- **Labels**: A, B, C for panels (bold, upper left)

### Required Figures for Paleoseismic Paper
1. **Location map**: Study site with tectonic context
2. **Stratigraphic column**: Sample positions, ages
3. **Time series**: Main proxy data with anomalies marked
4. **Discrimination plot**: Seismic vs climatic signals
5. **Correlation figure**: Cross-validation evidence

### Figure Captions
- First sentence: What the figure SHOWS
- Subsequent: Methods, abbreviations, interpretation hints
- No conclusions in captions

## Table Standards

- Horizontal lines only (no vertical)
- Units in header, not cells
- Footnotes for exceptions (a, b, c)
- Round to appropriate precision

## Supplementary Materials

### What to Include
- Extended methods (lab protocols, code)
- Additional figures (supporting evidence)
- Data tables (raw measurements)
- Sensitivity analyses

### What to Keep in Main Text
- Key results
- Essential methods
- Most compelling figures

## Writing Tips

### Clarity
- One idea per sentence
- Active voice preferred
- Define acronyms on first use
- Avoid jargon when possible

### Hedging Language
- "We suggest that..." (uncertainty)
- "Our data are consistent with..." (not proof)
- "One interpretation is..." (alternatives exist)

### Transitions
- "Building on this..."
- "In contrast to X..."
- "These findings suggest..."
- "Taken together..."

## Checklist Before Submission

- [ ] Word count within limits
- [ ] All figures/tables referenced in text
- [ ] References formatted correctly
- [ ] Data availability statement included
- [ ] Author contributions listed
- [ ] Conflicts of interest declared
- [ ] Cover letter written
- [ ] Suggested reviewers listed
