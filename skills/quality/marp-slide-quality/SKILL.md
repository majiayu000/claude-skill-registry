---
name: marp-slide-quality
description: Analyze and improve Marp markdown presentations using SlideGauge. Use when working with Marp presentations, slide decks, or when user asks to check, analyze, improve, or validate slide quality.
allowed-tools:
  - Read
  - Edit
  - Grep
  - Glob
  - Bash(uvx:*)
---

# Marp Slide Quality Skill

Analyze and improve Marp markdown presentations using the SlideGauge tool to create higher-quality, more effective slide decks.

## When This Skill Activates

This skill automatically activates when:
- Working with `.md` files containing `marp: true` frontmatter
- User mentions Marp presentations, slide quality, or slide analysis
- User asks to check, validate, improve, or fix presentation slides
- User wants to analyze slide quality metrics or scoring

## Main Workflow

Follow this 4-step process for analyzing and improving Marp presentations:

### Step 1: Analyze Baseline
First, install SlideGauge (if not already installed) and analyze the current state:

```bash
# Install SlideGauge using uvx
uvx --from git+https://github.com/kantord/SlideGauge slidegauge --version

# Analyze the presentation
uvx --from git+https://github.com/kantord/SlideGauge slidegauge analyze presentation.md

# Get detailed JSON output for deeper analysis
uvx --from git+https://github.com/kantord/SlideGauge slidegauge analyze --output json presentation.md | jq
```

### Step 2: Prioritize Fixes
Review the analysis and prioritize slides based on their scores:
- **Critical**: Slides scoring below 70 points (failing threshold)
- **Important**: Slides scoring 70-80 points (below good quality)
- **Good**: Slides scoring 80+ points (acceptable quality)

Focus on failing slides first, then work on improving the rest.

### Step 3: Apply Fixes
Use specific patterns and fixes from the reference documentation below. Common issues include:
- Too many bullet points or lines of content
- Missing slide titles or required elements
- Accessibility issues (low contrast, missing alt text)
- Code formatting problems
- Layout and visual design issues

### Step 4: Validate Improvements
After making changes, re-run the analysis to verify improvements:

```bash
uvx --from git+https://github.com/kantord/SlideGauge slidegauge analyze presentation.md
```

Compare before/after scores to ensure meaningful improvements.

## Requirements

- `uvx` available in the environment
- Network access to fetch SlideGauge from GitHub on first use
- Optional: `jq` if you want to pretty-print JSON output locally

## SlideGauge Rules Reference

### Scoring System
- **Starting Score**: 100 points per slide
- **Passing Threshold**: 70 points
- **Good Quality**: 80+ points
- **Excellent**: 90+ points

### Content Rules (Most Common Issues)

#### Too Many Bullets (-15 points)
**Rule**: Slides should have 6 or fewer bullet points
**Example Fix**:
```markdown
<!-- Before (8 bullets) -->
- First point
- Second point
- Third point
- Fourth point
- Fifth point
- Sixth point
- Seventh point
- Eighth point

<!-- After (split into 2 slides) -->
## Key Points
- First point
- Second point
- Third point
- Fourth point

## Additional Points
- Fifth point
- Sixth point
- Seventh point
- Eighth point
```

#### Too Many Lines (-15 points)
**Rule**: Slides should have 16 or fewer lines (including headers and code blocks)
**Strategy**: Split complex slides or use more concise phrasing

#### Missing Title (-30 points)
**Rule**: Every slide must have a title (H1 or H2)
**Fix**: Add appropriate headings to structure content

#### Missing Required Elements (-25 points)
**Rule**: Exercise/TODO slides need problem statement AND solution/activity
**Example**:
```markdown
## Exercise: Database Normalization

### Problem
Normalize the following unstructured data:
(Provide sample data)

### Solution Requirements
1. Identify entities and relationships
2. Create normalized tables
3. Define foreign key constraints
```

### Accessibility Rules

#### Low Contrast Text (-20 points)
**Rule**: Text must have sufficient contrast ratio
**Fix**: Ensure dark text on light backgrounds or use explicit contrast settings

#### Missing Alt Text (-10 points)
**Rule**: Images must have descriptive alt text
**Example**:
```markdown
![Diagram showing microservices architecture](./diagram.png)
```

### Color Rules

#### Too Many Colors (-10 points)
**Rule**: Slides should use consistent, limited color schemes
**Fix**: Use Marp's theme colors or define a limited palette

### Code Rules

#### Long Code Blocks (-10 points)
**Rule**: Code blocks over 30 lines should be split or simplified
**Strategy**: Show key concepts, move detailed code to separate files

#### Unclear Code Purpose (-10 points)
**Rule**: Code examples should clearly demonstrate their purpose
**Fix**: Add explanatory comments or use more illustrative examples

## Common Fix Patterns

### For Content Overload:
1. **Split slides** - Break complex topics into multiple focused slides
2. **Use groups** - Organize related content under subheadings
3. **Summarize** - Replace lengthy explanations with key points

### For Missing Elements:
1. **Add titles** - Every slide needs clear H1/H2 headings
2. **Complete exercises** - Ensure problem + solution/activity structure
3. **Add context** - Include brief explanations for code examples

### For Accessibility:
1. **Check contrast** - Use tools or built-in Marp themes
2. **Add alt text** - Describe image content and purpose
3. **Use semantic structure** - Proper heading hierarchy

## Practical Examples

### Example 1: Too Many Bullets Fix
**Before**: 8 bullet points on a single slide (Score: 70)
**After**: 2 slides with 4 bullets each (Score: 95)

### Example 2: Missing Title Fix
**Before**: Slide starts directly with content (Score: 65)
**After**: Added "## Database Design Overview" header (Score: 95)

### Example 3: Code Block Optimization
**Before**: 45-line code block (Score: 75)
**After**: 20-line key example + "See full implementation in: src/database.py" (Score: 90)

## Working with Users

### Best Practices:
1. **Show analysis first** - Always display current scores before making changes
2. **Get approval for major changes** - Ask before splitting content or restructuring slides
3. **Explain the reasoning** - Help users understand why specific changes improve quality
4. **Preserve technical accuracy** - Focus on presentation quality, not content changes
5. **Offer alternatives** - When multiple solutions exist, present options

### Sample Interaction:
```
I've analyzed your presentation and found 3 slides scoring below 70:

Slide 3: "Architecture Overview" - Score: 65 (missing title)
Slide 7: "Code Implementation" - Score: 55 (35-line code block)
Slide 12: "Database Design" - Score: 60 (8 bullet points)

Would you like me to fix these issues? I'll:
- Add proper titles
- Split the long code example
- Break down the complex bullet slide

Should I proceed with these improvements?
```

## Usage Tips

### Configuration Options:
```bash
# Custom passing threshold
uvx slidegauge analyze --threshold 75 presentation.md

# Only analyze specific slides
uvx slidegauge analyze --slides "1,3,5-7" presentation.md

# Verbose output with detailed explanations
uvx slidegauge analyze --verbose presentation.md
```

### Integration with Workflow:
- Run analysis after major content changes
- Use before presentations or reviews
- Include in CI/CD for documentation quality
- Great for team collaboration and standards

### Team Usage:
- Share scoring thresholds for consistency
- Use common fix patterns across presentations
- Document team-specific SlideGauge configurations
- Include quality checks in presentation templates

## Troubleshooting

### Common Issues:
1. **SlideGauge installation fails**: Ensure uvx is available and network connectivity
2. **No analysis results**: Check that file contains `marp: true` frontmatter
3. **Unexpected low scores**: Review rule documentation - some rules are strict by design
4. **Code analysis issues**: Ensure code blocks are properly formatted with language markers

### Getting Help:
- Check the complete SlideGauge documentation at https://github.com/kantord/SlideGauge
- Review rule reference for detailed explanations
- Test with simple presentations to understand baseline behavior
- Use `--verbose` flag for detailed analysis output

## Quality Checklist

Before finalizing a presentation, ensure:
- [ ] All slides have titles (H1/H2)
- [ ] No slide exceeds 6 bullet points
- [ ] No slide exceeds 16 lines total
- [ ] Code blocks are 30 lines or less
- [ ] Images have descriptive alt text
- [ ] Color contrast is sufficient
- [ ] Exercise slides have problem + solution
- [ ] Overall presentation scores 70+ on all slides

Following these guidelines will help create professional, accessible, and effective Marp presentations that communicate your ideas clearly and effectively.
