---
name: curriculum-package-lms
description: Generate LMS-ready packages in SCORM, Canvas, Moodle formats with proper structure, sequencing, and grade passback. Use when exporting to LMS, creating SCORM packages, or preparing Canvas/Moodle imports. Activates on "export to LMS", "create SCORM", "Canvas package", or "Moodle export".
---

# LMS Package Generation

Create distribution-ready Learning Management System packages with proper structure, navigation, assessments, and completion tracking.

## When to Use

- Export curriculum to LMS
- Create SCORM 1.2/2004 packages
- Generate Canvas course export
- Create Moodle backup
- Package for Blackboard/D2L

## Required Inputs

- **Curriculum Materials**: Lessons, assessments, resources
- **LMS Platform**: SCORM, Canvas, Moodle, Blackboard, D2L
- **Configuration**: Course settings, grading, prerequisites

## Workflow

### 1. Gather All Course Components

Collect:
- Syllabus and course info
- Learning objectives
- Lesson content
- Assessment items and rubrics
- Multimedia elements
- Resources and handouts

### 2. Generate SCORM Package

```bash
# SCORM 1.2 or 2004 structure
course-package/
├── imsmanifest.xml        # Package manifest
├── adlcp_rootv1p2.xsd     # Schema
├── index.html             # Launch file
├── content/
│   ├── lessons/
│   ├── assessments/
│   └── resources/
└── scripts/
    └── scorm-api.js       # SCORM communication
```

**Manifest Structure**:
```xml
<manifest identifier="COURSE_ID" version="1.0">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>2004 4th Edition</schemaversion>
  </metadata>
  <organizations default="ORG_ID">
    <organization identifier="ORG_ID">
      <title>Course Title</title>
      <item identifier="UNIT1" identifierref="RES_UNIT1">
        <title>Unit 1: Introduction</title>
        <item identifier="LESSON1" identifierref="RES_LESSON1">
          <title>Lesson 1.1</title>
        </item>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_LESSON1" type="webcontent" href="content/lesson1.html">
      <file href="content/lesson1.html"/>
    </resource>
  </resources>
</manifest>
```

### 3. Generate Canvas Export

```json
{
  "course": {
    "name": "Course Title",
    "course_code": "COURSE-101",
    "term": "Fall 2024",
    "modules": [
      {
        "id": 1,
        "name": "Unit 1: Introduction",
        "position": 1,
        "items": [
          {
            "type": "Page",
            "title": "Lesson 1.1",
            "content": "...",
            "position": 1
          },
          {
            "type": "Assignment",
            "title": "Unit 1 Assessment",
            "points_possible": 100,
            "rubric": {...}
          }
        ]
      }
    ],
    "assignments": [...],
    "quizzes": [...],
    "rubrics": [...]
  }
}
```

### 4. Generate Moodle Backup

```xml
<moodle_backup>
  <information>
    <name>Course Backup</name>
    <moodle_version>4.1</moodle_version>
    <backup_date>...</backup_date>
  </information>
  <contents>
    <activities>
      <activity id="1" moduleid="1" modulename="page">...</activity>
      <activity id="2" moduleid="2" modulename="quiz">...</activity>
    </activities>
  </contents>
</moodle_backup>
```

### 5. CLI Interface

```bash
# SCORM package
/curriculum.package-lms --format "scorm2004" --materials "curriculum-artifacts/" --output "course.zip"

# Canvas export
/curriculum.package-lms --format "canvas" --materials "curriculum-artifacts/" --course-code "BIO-101"

# Moodle backup
/curriculum.package-lms --format "moodle" --materials "curriculum-artifacts/"

# Help
/curriculum.package-lms --help
```

## Exit Codes

- **0**: Package created successfully
- **1**: Invalid LMS format
- **2**: Missing required materials
- **3**: Package generation failed
