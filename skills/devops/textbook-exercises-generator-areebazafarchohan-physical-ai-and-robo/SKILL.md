---
name: textbook-exercises-generator
description: Skill from AreebaZafarChohan/physical-ai-and-robotics
---

# Textbook Exercises & Capstone Generator

A skill for generating exercises, mini-projects, and capstone checkpoints for textbook chapters in Physical AI & Humanoid Robotics.

## Description

This skill generates educational content for textbook chapters including:
- 3 exercises (conceptual + practical)
- 1 mini project using real tools (ROS 2, Gazebo, Isaac)
- 1 capstone checkpoint connecting to the final humanoid robot

## Parameters

- `chapter_title`: The title of the textbook chapter
- `chapter_summary`: A brief summary of the chapter content
- `difficulty_level`: The difficulty level (Beginner / Intermediate / Advanced)

## Output Format

The skill outputs content in Markdown format with the heading "Exercises & Capstone Checkpoints" containing:
- 3 exercises (mix of conceptual and practical)
- 1 mini project with specific tool usage
- 1 capstone checkpoint connecting to humanoid robotics

## Example Usage

```
skill: "textbook_exercises_generator"
chapter_title: "Introduction to ROS 2"
chapter_summary: "Basic concepts of ROS 2 including nodes, topics, services"
difficulty_level: "Beginner"
```

## Implementation

This skill will generate:
1. Three exercises that combine conceptual understanding with practical application
2. A mini-project that uses ROS 2, Gazebo, or Isaac Sim tools
3. A capstone checkpoint that connects to the broader humanoid robot concept
4. All content formatted in Markdown under appropriate headings