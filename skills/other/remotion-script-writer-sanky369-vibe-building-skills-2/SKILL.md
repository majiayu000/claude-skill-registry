---
name: remotion-script-writer
description: Writes detailed video scripts for Remotion based on input requirements and codebase analysis
metadata:
  tags: remotion, video, script, animation, tutorial, demo, product
---

## When to use

Use this skill whenever you need to generate a comprehensive video script for creating a Remotion video. This skill is particularly useful for:

- **Product demo videos** that showcase features of a web application or software product
- **Coding tutorials** that explain a codebase or specific technical concepts with animated code
- **Animated videos** with complex sequences, transitions, and visual effects
- **Data visualization videos** that present statistics, charts, and dynamic data
- **Social media content** with captions, effects, and platform-specific optimizations

This skill analyzes your codebase, understands your requirements, and generates a detailed JSON script that can be directly used by Remotion's agent skills to create the final video.

## How to use

Read individual rule files for detailed explanations and examples:

- [rules/prompt-structure.md](rules/prompt-structure.md) - Defines the input structure and requirements for the skill
- [rules/script-generation.md](rules/script-generation.md) - The core prompt for generating detailed video scripts
- [rules/animation-patterns.md](rules/animation-patterns.md) - Common animation patterns and timing guidelines
- [rules/scene-templates.md](rules/scene-templates.md) - Reusable scene templates for common video scenarios

## Quick Start

### 1. Prepare Your Input

Create a JSON object with your video requirements:

```json
{
  "goal": "Create a product demo video for our new task management app",
  "targetAudience": "Project managers and teams looking for productivity tools",
  "code": "/path/to/your/codebase",
  "language": "TypeScript",
  "videoType": "product-demo",
  "duration": 60,
  "style": "modern",
  "animations": ["fade", "slide", "typewriter"],
  "transitions": ["wipe", "fade"]
}
```

### 2. Generate the Script

Pass your input to the `remotion-script-writer` skill. The skill will:

1. Analyze your codebase to identify key features and functionality
2. Structure the video into logical scenes with appropriate timing
3. Design visual elements, animations, and transitions for each scene
4. Generate voiceover scripts synchronized with visuals
5. List all required assets (images, fonts, audio, etc.)
6. Specify technical requirements (Remotion packages, libraries)

### 3. Use the Output

The skill generates a comprehensive JSON script that includes:

- **Video metadata**: Title, duration, dimensions, fps, video type
- **Scene breakdown**: Detailed specifications for each scene
- **Visual elements**: Text, images, code, animations, transitions
- **Audio**: Voiceover scripts and background music
- **Assets**: Complete list of required images, fonts, icons, etc.
- **Technical requirements**: Remotion packages and third-party libraries

### 4. Create the Video

Pass the generated script to Remotion's agent skills to:

1. Generate React components for each scene
2. Implement animations and transitions
3. Set up the composition structure
4. Preview the video in Remotion Studio
5. Render the final video

## Example Output

See [examples/product-demo-example.json](examples/product-demo-example.json) for a complete example of a generated video script.

## Supported Video Types

- **`product-demo`**: Feature showcases, UI walkthroughs, product announcements
- **`coding-tutorial`**: Code explanations, technical concepts, programming tutorials
- **`animation`**: Creative animations, motion graphics, visual effects
- **`data-visualization`**: Charts, graphs, statistics, animated data
- **`social-media`**: Short-form content, viral videos, platform-optimized content

## Best Practices

The skill incorporates Remotion best practices:

- All animations use `useCurrentFrame()` hook for frame-based timing
- Spring animations with natural motion (`damping: 200`) for smooth reveals
- Proper sequencing with `<Sequence>`, `<Series>`, and `<TransitionSeries>`
- Typewriter effects using string slicing (not per-character opacity)
- Deterministic animations (no `Math.random()`, use `random()` from remotion)
- Premounting sequences with `premountFor` prop for better performance
- Accurate duration calculation accounting for transition overlaps

## Customization

Modify the rule files to customize the skill:

- **`prompt-structure.md`**: Add new input fields or validation rules
- **`script-generation.md`**: Adjust the generation prompt or output format
- **`animation-patterns.md`**: Add custom animation patterns and effects
- **`scene-templates.md`**: Create new scene templates for specific use cases

## Advanced Features

### Codebase Analysis

The skill can analyze codebases from:

- Local file paths
- GitHub repositories (public or private)
- Code snippets provided directly

It identifies:

- Key functions and components
- Data structures and APIs
- User interactions and workflows
- Technical architecture and patterns

### Dynamic Content

Generate scripts with dynamic content:

- Fetch data from APIs for real-time information
- Calculate video duration based on content length
- Adjust scene timing based on voiceover length
- Parameterize content for multiple video variations

### Branding Integration

Apply consistent branding:

- Custom color schemes
- Company logos and icons
- Brand-specific fonts
- Visual style guidelines

## Limitations

- Maximum recommended video duration: 5 minutes (for performance)
- Code analysis works best with well-documented, structured code
- Voiceover scripts are auto-generated and may require manual refinement
- Asset generation (images, icons) is not included - assets must be provided or described
- Complex 3D animations may require additional manual setup

## Support

For questions, issues, or feature requests:

- Consult the [README.md](README.md) for detailed documentation
- Check the [examples](examples/) directory for sample scripts
- Visit [remotion.dev](https://www.remotion.dev) for Remotion documentation
- Join the Remotion Discord community for help and discussions

## Version

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Created by**: Manus AI
