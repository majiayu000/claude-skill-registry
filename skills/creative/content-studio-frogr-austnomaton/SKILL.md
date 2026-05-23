---
name: content-studio
description: Create videos, images, and text content
user_invocable: true
---

# Content Studio Skill

## Purpose
Create various types of content:
- Motion graphics videos (via motion-studio)
- Text content (posts, threads, articles)
- Code snippets and demos
- Visual content concepts

## Invocation
```
/content-studio [type] [options]
```

### Arguments
- `type`: video, text, code, or idea
- `--topic [topic]`: Subject matter
- `--style [style]`: Visual/writing style
- `--length [length]`: Duration or word count

### Examples
```
/content-studio video --topic "AI update"
/content-studio text --style "technical"
/content-studio idea                        # Generate content ideas
```

## Content Types

### Video (via motion-studio)
Uses the motion-studio skill for:
- Animated typography
- Generative backgrounds
- Motion graphics
- Social media clips

Example workflow:
```
1. Define message/topic
2. Choose visual style
3. Generate via motion-studio
4. Export for platform
```

### Text Content
- Posts (short-form)
- Threads (multi-part)
- Analysis pieces
- Code explanations

### Code Content
- Working snippets
- Demo projects
- Tutorials
- Tool releases

## Integration with motion-studio

The motion-studio skill is available for video creation:
```
/motion-studio --style "flow-field" --text "Your message here" --duration 10
```

Supports:
- Flow fields
- Particle systems
- Shader effects
- Typography animation
- Custom color palettes

## Workflow

### For Videos
1. **Concept**: Define message and audience
2. **Script**: Write text/narration
3. **Style**: Choose visual approach
4. **Generate**: Use motion-studio
5. **Review**: Check quality
6. **Export**: Platform-appropriate format

### For Text
1. **Topic**: What to write about
2. **Angle**: Unique perspective
3. **Personality**: Load appropriate voice
4. **Draft**: Write content
5. **Edit**: Refine and polish
6. **Ready**: For /poster

### For Code
1. **Problem**: What does it solve
2. **Implement**: Write working code
3. **Test**: Verify it works
4. **Document**: Clear explanation
5. **Package**: Ready to share

## Quality Standards

### Videos
- Clear message
- Professional look
- Appropriate length
- Platform-optimized

### Text
- Original perspective
- Well-written
- Appropriate tone
- Value-adding

### Code
- Working
- Clean
- Documented
- Useful

## Output

Returns content ready for posting or the generated asset path for videos.
