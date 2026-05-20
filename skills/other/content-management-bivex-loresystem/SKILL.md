---
name: content-management
description: Extract content management entities from narrative text. Use when analyzing mods, custom maps, user scenarios, localization, translations, subtitles, dubbing, and workshop content.
---
# content-management

Domain skill for Content Creator. Specific extraction rules and expertise.

## Domain Expertise

- **Modding**: User modifications, custom content
- **Maps**: Custom levels, world design
- **UGC platforms**: Workshops, sharing systems
- **Localization**: Translating content for different regions
- **Audio/visual**: Subtitles, dubbing, voice over
- **Content pipelines**: Creation, testing, distribution

## Entity Types (10 total)

- **mod** - Mods and modifications
- **custom_map** - Custom maps
- **user_scenario** - User-created scenarios
- **share_code** - Share codes
- **workshop_entry** - Workshop entries
- **localization** - Localization settings
- **translation** - Translations
- **subtitle** - Subtitles
- **dubbing** - Dubbing tracks
- **voice_over** - Voice over

## Processing Guidelines

When extracting content entities from chapter text:

1. **Identify content elements**:
   - Mods or custom content mentioned
   - Custom maps or user scenarios
   - Workshop or sharing platforms
   - Localization needs (different languages)
   - Audio/visual requirements (subtitles, dubbing)

2. **Extract content details**:
   - Mod types and features
   - Map designs and objectives
   - Sharing mechanisms and codes
   - Translation requirements
   - Audio/visual specifications

3. **Analyze content context**:
   - Platform compatibility
   - Content rating/approval
   - Community standards
   - Technical constraints

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Platform differences**: Content may work differently on different platforms
- **Community standards**: Mods may be rejected for violations
- **Translation quality**: Direct translations may miss cultural context
- **Technical constraints**: File sizes, compatibility, performance
