---
name: thumbnail-generator
description: Generate prompts for dev.to blog thumbnail/cover images in hand-drawn infographic style. Use when creating cover images, thumbnails, or featured images for blog posts. Recommended size 1000x420 pixels.
license: MIT
metadata:
  author: nghi-danh-ai
  version: "1.0.0"
---

# 🎨 Thumbnail Generator for dev.to Blog

This skill helps generate prompts for AI image generators to create thumbnail/cover images for dev.to blog posts.

## 📐 Technical Specifications

- **Size**: 1000x420 pixels (aspect ratio 2.38:1 - optimized for dev.to)
- **Style**: Hand-drawn infographic on notebook/whiteboard
- **Output Format**: Text prompt for AI image generators (Midjourney, DALL-E, Stable Diffusion, etc.)

## 🎯 When to Use

- Creating cover images for new dev.to articles
- Maintaining consistent branding with "Nghi Danh AI Content Creator"
- Need professional hand-drawn style illustrations

## 📝 Standard Prompt Template

```
Generate one single image of a physical, hand-drawn infographic on a large white notebook page or whiteboard.

**Topic/Title**: [ARTICLE TITLE]

**Style & Medium (Very Important)**:
- The image must look like a real photograph of an actual notebook page or whiteboard
- All content must appear hand-drawn using colored marker pens (black, blue, red, green) and highlighters (yellow, orange)
- Lines should be slightly imperfect, wobbly, and show natural ink texture on the surface
- No digital or printed appearance

**Text Rules**:
- No digital fonts
- All text, titles, and bullet points must look handwritten or hand-printed with pencil
- Handwriting should be clear, large, and easy to read, but naturally imperfect

**Key Visual Elements**:
[LIST 3-5 ICONS/ILLUSTRATIONS FOR THE TOPIC]

**Layout & Resolution**:
- Image size: 1000x420
- Structure the layout like a well-organized infographic
- Use multiple colors to highlight key sections
- Overall style must feel organic, casual, and realistic, as if drawn by hand

**Final Mandatory Text (Bottom of the Page)**:
Include the following handwritten sentence at the bottom of the image, in the same hand-drawn marker style:
"Follow Nghi Danh AI Content Creator for more helpful content"
```

## 🔄 Thumbnail Creation Process

### Step 1: Analyze the Article
- Identify the main topic
- List 3-5 important keywords
- Choose 3-5 relevant icons/symbols

### Step 2: Choose Appropriate Colors
| Topic | Primary Color | Secondary Color |
|-------|---------------|-----------------|
| Tech/Code | Blue, Black | Green |
| AI/ML | Purple, Blue | Orange |
| Web Dev | Orange, Red | Blue |
| DevOps | Green, Blue | Black |
| Database | Green, Gray | Yellow |

### Step 3: Create Complete Prompt
Fill in the template with specific article information.

## 📋 Complete Prompt Example

**For article about "10 VS Code Extensions for Developers":**

```
Generate one single image of a physical, hand-drawn infographic on a large white notebook page or whiteboard.

**Topic/Title**: "10 Must-Have VS Code Extensions"

**Style & Medium (Very Important)**:
- The image must look like a real photograph of an actual notebook page or whiteboard
- All content must appear hand-drawn using colored marker pens (black, blue, red, green) and highlighters (yellow, orange)
- Lines should be slightly imperfect, wobbly, and show natural ink texture on the surface
- No digital or printed appearance

**Text Rules**:
- No digital fonts
- All text, titles, and bullet points must look handwritten or hand-printed with pencil
- Handwriting should be clear, large, and easy to read, but naturally imperfect

**Key Visual Elements**:
- VS Code logo (hand-drawn)
- Extension puzzle pieces
- Code brackets < / >
- Lightning bolt for productivity
- Checkmark list

**Layout & Resolution**:
- Image size: 1000x420
- Structure the layout like a well-organized infographic
- Use multiple colors to highlight key sections (blue for code, green for success, orange highlights)
- Overall style must feel organic, casual, and realistic, as if drawn by hand

**Final Mandatory Text (Bottom of the Page)**:
Include the following handwritten sentence at the bottom of the image, in the same hand-drawn marker style:
"Follow Nghi Danh AI Content Creator for more helpful content"
```

## ⚠️ Important Notes

1. **DO NOT** use digital fonts - everything must be hand-drawn
2. **MUST** include watermark/signature at the bottom
3. **CHECK** size is 1000x420 before export
4. **ENSURE** text in image is clear and readable

## 🔗 References

- [dev.to Cover Image Guidelines](https://dev.to/settings/customization)
- Aspect ratio: ~2.38:1 (1000x420)
- Maximum file size: 5MB
