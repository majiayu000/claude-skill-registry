---
name: academic-course-setup-automator
description: When the user needs to set up multiple academic courses in a learning management system (Canvas/LMS) from structured data sources. This skill automates the entire workflow extracting course schedules from emails/attachments, matching instructors from CSV files, creating courses, enrolling teachers, publishing announcements with class details, uploading syllabi, enabling resource sharing for instructors teaching multiple courses, and publishing all courses. Triggers include course schedule setup, Canvas/LMS administration, academic term preparation, instructor assignment, syllabus distribution, and multi-course management.
---
# Academic Course Setup Automator

## Purpose
Automate the creation and configuration of academic courses in Canvas (or similar LMS) from a master schedule and instructor list. This skill handles the end-to-end process from data extraction to final course publication.

## Primary Workflow

### 1. Initial Data Gathering
- **Search for schedule email**: Look for emails with subject "Course Schedule Notification" or similar
- **Download schedule attachment**: Extract the course schedule (typically markdown/CSV format)
- **Load instructor data**: Read teacher emails from CSV file in workspace
- **Verify admin identity**: Get current user profile to determine which courses to manage

### 2. Data Processing
- **Parse course schedule**: Extract courses for the current administrator
- **Map instructors**: Match instructor names to Canvas user IDs using email addresses
- **Identify multi-course instructors**: Flag instructors teaching multiple courses for resource sharing

### 3. Course Creation & Configuration
- **Create courses**: Generate all courses for the administrator
- **Enroll instructors**: Add teachers to their respective courses
- **Publish announcements**: Create course announcements with instructor name and class time
- **Upload syllabi**: Attach syllabus PDFs from workspace to corresponding courses
- **Update course settings**: Set public syllabus and publish courses

### 4. Resource Sharing Setup
- **Create resource sharing notices**: Add announcements indicating related courses for instructors teaching multiple sections
- **Cross-reference courses**: Provide course IDs for easy navigation between related courses

## Key Requirements Met
- ✅ Assign correct instructors as teachers using email mapping
- ✅ Publish announcements with instructor names and class times
- ✅ Set up resource sharing for instructors teaching multiple courses
- ✅ Publish syllabi for each course
- ✅ Publish all courses

## Critical Success Factors
1. **Email search precision**: Must find the correct schedule email
2. **Instructor mapping accuracy**: Email addresses must match Canvas user records
3. **Course naming consistency**: Course codes should follow institutional conventions
4. **File path accuracy**: Syllabus files must match course names in workspace

## Common Edge Cases
- Missing instructor records in Canvas
- Syllabus files not found in workspace
- Duplicate course names
- Large number of courses requiring batch processing

## Optimization Notes
- Batch course creation where possible
- Use consistent naming patterns for course codes
- Validate all operations before proceeding to next step
- Maintain clear logging of created resources for verification
