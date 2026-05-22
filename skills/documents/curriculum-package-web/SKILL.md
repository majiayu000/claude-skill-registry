---
name: curriculum-package-web
description: Generate responsive HTML/CSS/JS web content with interactive elements, quizzes, navigation, and accessibility for self-paced or blended learning. Use when creating web content, interactive lessons, or online materials. Activates on "create website", "web content", "interactive web", or "HTML export".
---

# Web Content & Interactive Materials

Create responsive, accessible web-based learning content with interactivity, navigation, and engagement features.

## When to Use

- Create standalone websites
- Generate interactive lessons
- Build self-paced modules
- Develop online content
- Create web-based activities

## Required Inputs

- **Content**: Lessons, assessments, resources
- **Interactivity**: Quiz types, activities needed
- **Styling**: Theme, colors, branding
- **Features**: Navigation, progress tracking, etc.

## Workflow

### 1. Generate HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Course Title</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav><!-- Navigation menu --></nav>
  <main><!-- Content --></main>
  <footer><!-- Footer --></footer>
  <script src="interactive.js"></script>
</body>
</html>
```

### 2. Add Interactive Elements

- Quizzes with immediate feedback
- Drag-and-drop activities
- Expandable content sections
- Progress indicators
- Bookmarking
- Note-taking

### 3. Ensure Responsiveness

- Mobile-friendly (320px+)
- Tablet optimized
- Desktop enhanced
- Touch and keyboard accessible

### 4. CLI Interface

```bash
# Full course website
/curriculum.package-web --materials "curriculum-artifacts/" --output "course-website/"

# Single interactive lesson
/curriculum.package-web --lesson "lesson1.md" --interactive --quiz "quiz1.json"

# With custom theme
/curriculum.package-web --materials "curriculum-artifacts/" --theme "dark" --primary-color "#3498db"

# Help
/curriculum.package-web --help
```

## Exit Codes

- **0**: Website generated
- **1**: Invalid configuration
- **2**: Cannot load materials
- **3**: Build failed
