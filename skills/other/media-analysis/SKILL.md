---
name: media-analysis
description: Extract media entities from narrative text. Use when analyzing newspapers, radio, television, internet, social media platforms, propaganda, and rumor systems.
---
# media-analysis

Domain skill for Media Analyst. Specific extraction rules and expertise.

## Domain Expertise

- **Media types**: Newspapers, radio, TV, internet, social platforms
- **Information channels**: How news and information spread
- **Propaganda systems**: Manipulation, censorship, state media
- **Social media**: Platforms, virality, influence campaigns
- **Rumors**: Unofficial information, gossip, underground channels

## Entity Types (7 total)

- **newspaper** - Newspapers and printed news
- **radio** - Radio broadcasts
- **television** - Television broadcasts
- **internet** - Internet systems and networks
- **social_media** - Social media platforms
- **propaganda** - Propaganda and state messaging
- **rumor** - Rumors and unofficial information

## Processing Guidelines

When extracting media entities from chapter text:

1. **Identify media elements**:
   - Newspapers or printed news mentioned
   - Radio or TV broadcasts
   - Internet or network references
   - Social media or communication platforms
   - Propaganda or state messaging
   - Rumors or unofficial information

2. **Extract media details**:
   - Publication names, frequency, reach
   - Broadcast channels, frequencies, programming
   - Internet platforms, websites, connectivity
   - Social media platforms, viral content
   - Propaganda techniques and targets
   - Rumor sources and reliability

3. **Analyze media context**:
   - Information control and censorship
   - Official vs unofficial channels
   - Media bias and manipulation
   - Communication technology level

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Media bias**: All media has perspective or bias
- **Censorship**: Information may be controlled or restricted
- **Underground channels**: Rumors and unofficial info flow differently
- **Technology level**: Media reflects world's tech advancement
- **Social impact**: Media shapes public opinion
