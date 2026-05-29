---
name: publishing
description:
  Work on publishing features including EPUB generation, cover image generation,
  platform integration, and export functionality. Use when implementing eBook
  creation, platform exports, or distribution workflows.
---

# Publishing

## Quick Reference

- **[EPUB Generation](epub-generation.md)** - eBook creation and formatting
- **[Cover Generation](cover-generation.md)** - Image creation and styling
- **[Platform Integration](platform-integration.md)** - Amazon KDP, Google Play,
  etc.
- **[Export Workflows](export-workflows.md)** - Export and submission processes

## When to Use

- Implementing EPUB 3.0 generation
- Building cover image generation systems
- Creating platform-specific export workflows
- Working on metadata management
- Implementing submission automation
- Handling publishing standards compliance

## Core Methodology

- **Standards Compliance**: Follow EPUB 3.0, IDPF, and platform guidelines
- **Asset Management**: Handle images, fonts, and styles efficiently
- **Platform Rules**: Implement Amazon KDP, Google Play, and platform-specific
  requirements
- **Error Handling**: Validate exports before submission
- **User Experience**: Provide clear feedback and progress tracking

## Integration

- **tech-stack-specialist**: Manage EPUB libraries (JSZip, etc.)
- **qa-engineer**: Test export functionality and platform compliance
- **performance-engineer**: Optimize large file generation
- **architecture-guardian**: Maintain clean separation of publishing logic
- **domain-expert**: Model publishing domain concepts

## Best Practices

✓ Validate all exports before submission ✓ Support multiple output formats
(EPUB, PDF, etc.) ✓ Provide detailed error messages for failed exports ✓
Optimize image compression without quality loss ✓ Include comprehensive metadata

## Content Modules

See detailed modules:

- **[EPUB Generation](epub-generation.md)**: EPUB 3.0 creation, metadata, and
  styling
- **[Cover Generation](cover-generation.md)**: AI image generation and style
  presets
- **[Platform Integration](platform-integration.md)**: Platform-specific exports
  and submissions
- **[Export Workflows](export-workflows.md)**: Export pipelines and automation
- **[Publishing Standards](standards.md)**: Compliance and best practices
