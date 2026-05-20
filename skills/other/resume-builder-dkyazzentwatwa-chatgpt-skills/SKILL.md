---
name: resume-builder
description: Generate professional PDF resumes from structured data or JSON. Multiple templates, ATS-friendly output, and customizable sections.
---

# Resume Builder

Create professional PDF resumes from structured data with multiple template styles. Supports JSON input, customizable sections, and ATS-friendly formatting.

## Quick Start

```python
from scripts.resume_builder import ResumeBuilder

# Build resume programmatically
resume = ResumeBuilder()
resume.set_contact("John Smith", "john@email.com", "555-123-4567", "San Francisco, CA")
resume.set_summary("Experienced software engineer with 5+ years...")
resume.add_experience("Software Engineer", "Tech Corp", "2020-Present", [
    "Led development of microservices architecture",
    "Improved system performance by 40%"
])
resume.add_education("B.S. Computer Science", "State University", "2019")
resume.add_skills(["Python", "JavaScript", "AWS", "Docker"])
resume.generate().save("resume.pdf")

# From JSON
resume = ResumeBuilder.from_json("resume_data.json")
resume.generate().save("resume.pdf")
```

## Features

- **Multiple Templates**: Modern, classic, minimal, executive styles
- **ATS-Friendly**: Clean formatting that passes applicant tracking systems
- **Customizable Sections**: Experience, education, skills, projects, certifications
- **Flexible Input**: Python API or JSON data
- **Professional Output**: Clean PDF with proper typography
- **Links**: Clickable URLs for portfolio, LinkedIn, GitHub

## API Reference

### Initialization

```python
resume = ResumeBuilder()
resume = ResumeBuilder(template="modern")
resume = ResumeBuilder.from_json("data.json")
resume = ResumeBuilder.from_dict(data)
```

### Contact Information

```python
# Basic contact
resume.set_contact(
    name="John Smith",
    email="john@email.com",
    phone="555-123-4567",
    location="San Francisco, CA"
)

# With links
resume.set_contact(
    name="John Smith",
    email="john@email.com",
    phone="555-123-4567",
    location="San Francisco, CA",
    linkedin="linkedin.com/in/johnsmith",
    github="github.com/johnsmith",
    website="johnsmith.dev"
)
```

### Summary/Objective

```python
# Professional summary
resume.set_summary(
    "Experienced software engineer with 5+ years building scalable "
    "web applications. Passionate about clean code and mentoring."
)

# Or objective statement
resume.set_objective(
    "Seeking a senior engineering role where I can leverage my "
    "expertise in distributed systems and cloud architecture."
)
```

### Work Experience

```python
# Add experience entry
resume.add_experience(
    title="Senior Software Engineer",
    company="Tech Corporation",
    dates="Jan 2020 - Present",
    bullets=[
        "Led team of 5 engineers in developing microservices architecture",
        "Reduced API response time by 60% through optimization",
        "Implemented CI/CD pipeline reducing deployment time by 80%"
    ],
    location="San Francisco, CA"  # Optional
)

# Multiple entries
resume.add_experience("Software Engineer", "Startup Inc", "2018-2020", [
    "Built real-time notification system serving 1M+ users",
    "Developed RESTful APIs using Python and FastAPI"
])
```

### Education

```python
# Add education
resume.add_education(
    degree="Bachelor of Science in Computer Science",
    school="State University",
    year="2018",
    gpa="3.8",  # Optional
    honors="Magna Cum Laude"  # Optional
)

# With coursework
resume.add_education(
    degree="M.S. Data Science",
    school="Tech University",
    year="2020",
    coursework=["Machine Learning", "Statistical Analysis", "Big Data"]
)
```

### Skills

```python
# Simple skills list
resume.add_skills(["Python", "JavaScript", "React", "AWS", "Docker"])

# Categorized skills
resume.add_skills({
    "Languages": ["Python", "JavaScript", "Go", "SQL"],
    "Frameworks": ["React", "Django", "FastAPI"],
    "Tools": ["Docker", "Kubernetes", "AWS", "Git"]
})
```

### Projects

```python
# Add project
resume.add_project(
    name="Open Source Library",
    description="Data validation library with 1000+ GitHub stars",
    technologies=["Python", "PyPI"],
    url="github.com/user/project"  # Optional
)
```

### Certifications

```python
resume.add_certification("AWS Solutions Architect", "Amazon", "2023")
resume.add_certification("Professional Scrum Master", "Scrum.org", "2022")
```

### Additional Sections

```python
# Languages
resume.add_languages(["English (Native)", "Spanish (Fluent)", "French (Basic)"])

# Volunteer experience
resume.add_volunteer(
    role="Tech Mentor",
    organization="Code for Good",
    dates="2021 - Present",
    description="Mentor underrepresented students in programming"
)

# Publications
resume.add_publication(
    title="Scaling Microservices",
    venue="Tech Blog",
    year="2023",
    url="blog.com/article"
)

# Custom section
resume.add_custom_section("Awards", [
    "Employee of the Year 2022",
    "Hackathon Winner - Best Innovation"
])
```

### Templates and Styling

```python
# Set template
resume.set_template("modern")    # Clean, contemporary
resume.set_template("classic")   # Traditional, formal
resume.set_template("minimal")   # Simple, ATS-optimized
resume.set_template("executive") # Premium, senior roles

# Custom colors
resume.set_colors(
    primary="#2563eb",   # Headers
    text="#333333"       # Body text
)

# Margins
resume.set_margins(top=0.5, bottom=0.5, left=0.6, right=0.6)
```

### Generation

```python
# Generate and save
resume.generate().save("resume.pdf")

# Get PDF bytes
pdf_bytes = resume.to_bytes()
```

## Data Formats

### JSON Format

```json
{
  "contact": {
    "name": "John Smith",
    "email": "john@email.com",
    "phone": "555-123-4567",
    "location": "San Francisco, CA",
    "linkedin": "linkedin.com/in/johnsmith",
    "github": "github.com/johnsmith"
  },
  "summary": "Experienced software engineer...",
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "Tech Corp",
      "dates": "2020 - Present",
      "location": "San Francisco, CA",
      "bullets": [
        "Led development of microservices",
        "Improved performance by 40%"
      ]
    }
  ],
  "education": [
    {
      "degree": "B.S. Computer Science",
      "school": "State University",
      "year": "2018",
      "gpa": "3.8"
    }
  ],
  "skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["React", "Django"]
  },
  "projects": [
    {
      "name": "Open Source Tool",
      "description": "Description here",
      "technologies": ["Python"],
      "url": "github.com/project"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified",
      "issuer": "Amazon",
      "year": "2023"
    }
  ]
}
```

## CLI Usage

```bash
# From JSON file
python resume_builder.py --input resume.json --output resume.pdf

# With template
python resume_builder.py --input data.json --template modern --output resume.pdf

# Quick resume (interactive prompts)
python resume_builder.py --quick --output resume.pdf
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input JSON file | Required |
| `--output` | Output PDF path | `resume.pdf` |
| `--template` | Template style | `modern` |

## Templates

### Modern
- Clean sans-serif typography
- Blue accent color
- Clear section headers
- Good for tech roles

### Classic
- Traditional serif fonts
- Black and gray colors
- Formal layout
- Good for traditional industries

### Minimal
- Maximum ATS compatibility
- Simple formatting
- No colors or graphics
- Best for online applications

### Executive
- Premium appearance
- Elegant typography
- Subtle accents
- Good for senior roles

## Best Practices

1. **Keep it concise**: 1 page for <10 years experience, 2 pages max
2. **Use action verbs**: "Led", "Developed", "Improved", "Achieved"
3. **Quantify achievements**: "Increased sales by 25%", "Managed team of 8"
4. **Tailor to job**: Customize skills and summary for each application
5. **ATS-friendly**: Use standard section headers, avoid tables/graphics

## Dependencies

```
reportlab>=4.0.0
Pillow>=10.0.0
```

## Limitations

- PDF output only
- English language optimized
- Maximum 2 pages
- No photo support (ATS best practice)
