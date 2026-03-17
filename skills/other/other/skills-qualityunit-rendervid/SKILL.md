---
name: rendervid
description: "Generate videos and images from JSON templates using AI-powered video rendering"
version: "0.1.0"
tags: [video, rendering, animation, templates, social-media, mcp]
category: content-creation
author: QualityUnit
repository: https://github.com/QualityUnit/rendervid
license: FlowHunt Attribution License
---

# Rendervid MCP Skill

Generate professional videos and images from JSON templates using natural language. Rendervid provides a declarative, AI-friendly way to create animated content for social media, marketing, data visualization, and more.

## Overview

Rendervid is a Model Context Protocol (MCP) server that enables AI agents to:
- Generate videos in multiple formats (MP4, WebM, MOV, GIF)
- Create static images (PNG, JPEG, WebP)
- Access 50+ ready-to-use templates
- Validate templates before rendering
- Discover all available capabilities

**Key Features:**
- **Declarative JSON Templates** - Define videos/images as simple JSON structures
- **40+ Animation Presets** - Entrance, exit, and emphasis animations with easing functions
- **Rich Layer Types** - Text, images, video, shapes, audio, Lottie, custom React components
- **50+ Examples** - Ready-to-use templates across 10+ categories
- **Type-Safe** - Full TypeScript with Zod validation
- **Cross-Platform** - Works in Node.js and browsers

## When to Use This Skill

Use Rendervid when you need to:

### Content Creation
- Generate social media content (Instagram stories, TikTok videos, YouTube thumbnails)
- Create marketing videos (product showcases, sale announcements, testimonials)
- Build data visualizations (animated charts, graphs, dashboards)
- Produce educational content (course intros, lesson titles)

### Automation
- Batch generate videos from data
- Create personalized video content
- Generate thumbnails for video content
- Build video generation workflows

### Prototyping
- Quickly test video concepts
- Create animated mockups
- Generate placeholder content
- Explore animation styles

### AI-Driven Content
- Let AI agents create videos from text descriptions
- Generate videos based on user input
- Create dynamic content based on data
- Build video generation chatbots

## Available Tools

The Rendervid MCP server provides 6 tools:

### 1. render_video
Generate video files from JSON templates.

**Common uses:**
- Social media videos
- Marketing content
- Animated explainers
- Data visualizations

**Example prompt:**
```
"Create a 5-second Instagram story with text 'Summer Sale' and a blue gradient background"
```

### 2. render_image
Generate static images or single frames.

**Common uses:**
- Thumbnails
- Social media images
- Preview frames
- Static graphics

**Example prompt:**
```
"Generate a YouTube thumbnail with title 'Best Practices 2024'"
```

### 3. validate_template
Validate template JSON before rendering.

**Common uses:**
- Check template syntax
- Catch errors early
- Verify AI-generated templates
- Debug template issues

**Example prompt:**
```
"Validate this template: [paste JSON]"
```

### 4. get_capabilities
Discover all available features.

**Common uses:**
- Learn what's possible
- Find available animations
- Check supported formats
- Understand layer types

**Example prompt:**
```
"What animation presets are available?"
```

### 5. list_examples
Browse 50+ example templates.

**Common uses:**
- Find templates by category
- Discover use cases
- Get inspiration
- Learn template structure

**Example prompt:**
```
"Show me all social media templates"
```

### 6. get_example
Load a specific example template.

**Common uses:**
- Use ready-made templates
- Start from examples
- Learn template patterns
- Customize existing templates

**Example prompt:**
```
"Load the Instagram story template"
```

## Template Structure

Rendervid templates are JSON objects with three main sections:

```json
{
  "name": "My Video",
  "output": {
    "type": "video",
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "duration": 5
  },
  "inputs": [
    {
      "key": "title",
      "type": "string",
      "label": "Title",
      "default": "Hello"
    }
  ],
  "composition": {
    "scenes": [
      {
        "id": "main",
        "startFrame": 0,
        "endFrame": 150,
        "backgroundColor": "#1a1a2e",
        "layers": [
          {
            "id": "title",
            "type": "text",
            "position": { "x": 960, "y": 540 },
            "size": { "width": 1600, "height": 200 },
            "inputKey": "title",
            "props": {
              "fontSize": 120,
              "color": "#ffffff",
              "textAlign": "center"
            },
            "animations": [
              {
                "type": "entrance",
                "effect": "fadeInUp",
                "duration": 30,
                "easing": "easeOut"
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Key Concepts

**Output Configuration:**
- Defines video/image dimensions, FPS, duration
- Supports multiple formats and codecs

**Dynamic Inputs:**
- Variables that can be customized per render
- Support strings, numbers, booleans, colors, images, videos

**Composition:**
- Scenes with frame ranges
- Layers with types, positions, props
- Animations with presets and easing

## Common Patterns

### Pattern 1: Text Animation
```
User: "Create a video with animated text"

AI flow:
1. get_capabilities() to understand animations
2. render_video() with fadeIn animation
```

### Pattern 2: Social Media Content
```
User: "Make an Instagram story for a product launch"

AI flow:
1. list_examples({ category: "social-media" })
2. get_example({ examplePath: "social-media/instagram-story" })
3. render_video() with custom inputs
```

### Pattern 3: Data Visualization
```
User: "Create an animated bar chart showing Q1 sales"

AI flow:
1. get_example({ examplePath: "data-visualization/animated-bar-chart" })
2. Modify template with data
3. render_video()
```

### Pattern 4: Batch Generation
```
User: "Create 10 videos with different titles"

AI flow:
1. Load template once
2. Call render_video() 10 times with different inputs
```

### Pattern 5: Template Validation
```
User: "Check if my custom template is valid"

AI flow:
1. validate_template() to check structure
2. Fix any errors
3. render_video() to generate
```

## Special Topics

### Animations

Rendervid supports 40+ animation presets organized by category:

**Entrance Animations:**
- fadeIn, fadeInUp, fadeInDown, fadeInLeft, fadeInRight
- slideInUp, slideInDown, slideInLeft, slideInRight
- scaleIn, zoomIn, rotateIn, bounceIn, flipInX, flipInY

**Exit Animations:**
- fadeOut, fadeOutUp, fadeOutDown, fadeOutLeft, fadeOutRight
- slideOutUp, slideOutDown, slideOutLeft, slideOutRight
- scaleOut, zoomOut, rotateOut, bounceOut

**Emphasis Animations:**
- pulse, shake, bounce, swing, wobble, flash, rubberBand
- heartbeat, float, spin, tada, jello, flip

**Easing Functions (30+):**
- Linear: linear
- Ease: ease, easeIn, easeOut, easeInOut
- Cubic: easeInQuad, easeOutQuad, easeInOutQuad
- And more: Cubic, Quart, Quint, Sine, Expo, Circ, Back, Elastic, Bounce

### Layer Types

**Text Layers:**
- Typography controls (font, size, weight, style)
- Alignment and spacing
- Color and effects
- Google Fonts support

**Image Layers:**
- Fit options (cover, contain, fill)
- Scaling and positioning
- Filters and blend modes

**Video Layers:**
- Playback controls
- Timing and trimming
- Audio control

**Shape Layers:**
- Rectangles, ellipses, polygons, stars, paths
- Fill and stroke
- Border radius and effects

**Audio Layers:**
- Background music
- Sound effects
- Volume and fade controls

**Lottie Layers:**
- Animated vector graphics
- JSON animation files

**Custom Layers:**
- React components
- Full CSS/Tailwind support
- Advanced use cases

### Output Formats

**Video Formats:**
- MP4 (H.264, H.265)
- WebM (VP8, VP9, AV1)
- MOV (ProRes, H.264)
- GIF

**Image Formats:**
- PNG (lossless)
- JPEG (lossy, quality control)
- WebP (modern, efficient)

**Quality Presets:**
- draft: Fast rendering, lower quality
- standard: Balanced quality/speed
- high: High quality, slower rendering
- lossless: Maximum quality, large files

### Template Categories

**Getting Started:**
- Hello World
- First Video
- First Image

**Social Media:**
- Instagram Story (1080x1920)
- Instagram Post (1080x1080)
- TikTok Video (1080x1920)
- YouTube Thumbnail (1280x720)
- Twitter Card (1200x630)
- LinkedIn Banner (1584x396)

**Marketing:**
- Product Showcase
- Sale Announcement
- Testimonial Video
- Before & After
- Logo Reveal

**Data Visualization:**
- Animated Bar Chart
- Line Graph
- Pie Chart
- Counter Animation
- Progress Dashboard

**Business:**
- Quote Card
- Stat Highlight
- Feature Announcement
- Team Introduction
- Company Update

**Education:**
- Lesson Title
- Quiz Question
- Course Intro
- Study Tip
- Progress Tracker

**Celebrations:**
- Birthday Card
- Holiday Greeting
- Congratulations
- Thank You
- Milestone

**E-commerce:**
- Product Launch
- Flash Sale
- New Arrival
- Customer Review
- Price Drop

**Event:**
- Event Announcement
- Countdown Timer
- Registration
- Thank You (Attendees)
- Highlight Reel

**Podcast:**
- Episode Intro
- Quote Card
- Guest Introduction
- Coming Soon
- Subscribe Reminder

**Real Estate:**
- Property Showcase
- Open House
- Sold Announcement
- Agent Introduction
- Virtual Tour Intro

## Best Practices

### Template Design

1. **Keep it Simple**
   - Start with examples
   - Build complexity gradually
   - Test frequently

2. **Use Dynamic Inputs**
   - Make values customizable
   - Provide sensible defaults
   - Document input purposes

3. **Optimize Frame Ranges**
   - Minimize total frames for faster rendering
   - Use appropriate FPS (24-30 for most content)
   - Consider file size vs quality tradeoffs

4. **Test Animations**
   - Preview before full render
   - Check timing and easing
   - Verify layer stacking

### Performance

1. **Draft Quality for Iteration**
   - Use draft quality during development
   - Switch to high quality for finals
   - Consider file size requirements

2. **Batch Rendering**
   - Reuse templates when possible
   - Queue multiple renders
   - Monitor resource usage

3. **Asset Optimization**
   - Compress images before use
   - Use appropriate video codecs
   - Optimize Lottie animations

### AI Integration

1. **Clear Descriptions**
   - Describe intent clearly
   - Specify dimensions and duration
   - Mention animation preferences

2. **Validate Templates**
   - Always validate AI-generated templates
   - Check for common errors
   - Test with sample data

3. **Iterate Progressively**
   - Start simple, add complexity
   - Test each change
   - Use examples as starting points

## Example Workflows

### Workflow 1: Quick Social Media Post

```
User: "Create an Instagram story announcing a flash sale"

AI Agent:
1. list_examples({ category: "social-media" })
2. get_example({ examplePath: "social-media/instagram-story" })
3. render_video({
     template: {...},
     inputs: {
       title: "Flash Sale",
       subtitle: "50% Off Everything",
       backgroundColor: "#FF6B6B"
     },
     format: "mp4",
     quality: "high"
   })

Result: Instagram-ready 1080x1920 video
```

### Workflow 2: Data Visualization

```
User: "Create an animated chart showing Q1 revenue growth"

AI Agent:
1. get_example({ examplePath: "data-visualization/animated-bar-chart" })
2. Modify template with revenue data
3. validate_template({ template })
4. render_video({
     template,
     inputs: { data: [...], title: "Q1 Revenue" },
     format: "mp4",
     quality: "high"
   })

Result: Animated bar chart video
```

### Workflow 3: Custom Template Creation

```
User: "Create a custom video with my brand colors and logo"

AI Agent:
1. get_capabilities() to understand options
2. Start with example template
3. Customize colors, fonts, layout
4. validate_template() to check
5. render_video() with draft quality
6. Iterate based on preview
7. Final render with high quality

Result: Custom branded video
```

### Workflow 4: Batch Video Generation

```
User: "Create welcome videos for 100 new users"

AI Agent:
1. get_example({ examplePath: "business/team-introduction" })
2. Loop through user list:
   - render_video({
       template,
       inputs: { name: user.name },
       outputPath: `welcome-${user.id}.mp4`
     })

Result: 100 personalized welcome videos
```

## Troubleshooting

### Common Issues

**Issue: Server not connecting**
- Check absolute path in MCP config
- Verify Node.js version (20+)
- Check server builds: `pnpm build`
- Review logs in AI editor

**Issue: FFmpeg not found**
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu
choco install ffmpeg  # Windows
```

**Issue: Template validation fails**
- Check JSON syntax
- Verify required fields
- Review error messages
- Use validate_template tool

**Issue: Slow rendering**
- Use draft quality for iteration
- Reduce video duration/FPS
- Optimize asset sizes
- Check system resources

**Issue: Node version errors**
- Update to Node.js 20+
- Use full Node.js path in config
- Verify with: `node --version`

### Getting Help

- **Documentation**: [MCP Server README](../mcp/README.md)
- **Examples**: Browse `/examples/` directory
- **Issues**: [GitHub Issues](https://github.com/QualityUnit/rendervid/issues)
- **Discussions**: [GitHub Discussions](https://github.com/QualityUnit/rendervid/discussions)

## Resources

### Documentation
- [MCP Server Documentation](../mcp/README.md)
- [Installation Guide](../mcp/INSTALL.md)
- [Quick Start Guide](../mcp/QUICKSTART.md)
- [API Reference](./README.md)

### Templates
- [50+ Example Templates](../examples/)
- [Skills Registry](./skills-registry.json)
- [Individual Tool Docs](./README.md#available-skills)

### External Links
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Specification](https://modelcontextprotocol.io/specification)
- [Rendervid Repository](https://github.com/QualityUnit/rendervid)

## Version History

### 0.1.0 (Initial Release)
- 6 MCP tools (render_video, render_image, validate_template, get_capabilities, list_examples, get_example)
- 50+ example templates across 10 categories
- 40+ animation presets with 30+ easing functions
- Support for MP4, WebM, MOV, GIF, PNG, JPEG, WebP
- Full TypeScript with Zod validation
- Stdio transport for maximum compatibility
- Comprehensive documentation

## License

FlowHunt Attribution License - Free for commercial and personal use with attribution

## Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Credits

Developed by QualityUnit

Built with:
- TypeScript
- Model Context Protocol SDK
- Zod for validation
- Puppeteer for rendering
- FFmpeg for video encoding
