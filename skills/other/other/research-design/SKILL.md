---
name: research-design
description: Extract research and education entities from narrative text. Use when analyzing academies, universities, schools, libraries, archives, museums, and research centers.
---
# research-design

Domain skill for Research Education Specialist. Specific extraction rules and expertise.

## Domain Expertise

- **Education systems**: Schools, academies, universities
- **Research institutions**: Labs, observatories, research centers
- **Knowledge preservation**: Libraries, archives, museums
- **Academic structure**: Degrees, specializations, admission
- **Funding and support**: Patronage, grants, royal backing

## Entity Types (7 total)

- **academy** - Academies
- **university** - Universities
- **school** - Schools
- **library** - Libraries
- **research_center** - Research centers
- **archive** - Archives
- **museum** - Museums

## Processing Guidelines

When extracting research and education entities from chapter text:

1. **Identify education/research elements**:
   - Schools, academies, universities mentioned
   - Libraries or archives
   - Museums or research centers
   - Scholars or researchers
   - Research projects or discoveries
   - Educational systems or degrees

2. **Extract education/research details**:
   - Institution types and focuses
   - Libraries' collections and sizes
   - Museum exhibits and themes
   - Research projects and specializations
   - Academic programs and degrees

3. **Analyze education/research context**:
   - Knowledge accessibility (open vs restricted)
   - Research funding and support
   - Preservation of ancient knowledge
   - Educational quality and equality

4. **Create schema-compliant entities** with proper JSON structure

## Key Considerations

- **Access inequality**: Some knowledge is restricted to elite
- **Funding issues**: Research depends on patronage or government support
- **Preservation vs access**: Libraries may restrict ancient or dangerous texts
- **Educational hierarchy**: Different levels (primary, academy, university)
- **Knowledge loss**: War or disaster can destroy institutions
