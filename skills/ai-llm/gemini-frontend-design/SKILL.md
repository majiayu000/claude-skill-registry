---
name: gemini-frontend-design
description: Create distinctive, production-grade frontend interfaces using Gemini 3 Pro for design ideation. Use this skill when you want Gemini's creative perspective on web components, pages, or applications. Generates bold, polished code that avoids generic AI aesthetics.
license: MIT
---

This skill leverages Gemini 3 Pro's creative capabilities to generate distinctive, production-grade frontend interfaces. It uses a multi-step workflow: Gemini provides creative direction and initial implementation, then Claude refines and polishes the output.

## Workflow

### Step 1: Parse User Requirements

Extract from user input:
- **Component/Page Type**: What are we building? (landing page, dashboard, form, card, etc.)
- **Purpose**: What problem does it solve? Who uses it?
- **Technical Constraints**: Framework (React, Vue, vanilla), styling (Tailwind, CSS), etc.
- **Aesthetic Hints**: Any mentioned preferences (dark mode, minimal, playful, etc.)

### Step 2: Call Gemini 3 Pro for Design Generation

**CRITICAL**: Use the Bash tool to execute this Python command. Replace `{REQUIREMENTS}` with the parsed user requirements.

```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

requirements = '''
{REQUIREMENTS}
'''

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=f'''You are an elite frontend designer known for creating distinctive, memorable interfaces that avoid generic \"AI slop\" aesthetics.

REQUIREMENTS:
{requirements}

DESIGN THINKING PROCESS:

1. **Purpose Analysis**: What problem does this solve? Who uses it?

2. **Aesthetic Direction**: Choose ONE bold direction and commit fully:
   - Brutally minimal (precision, negative space, restraint)
   - Maximalist chaos (layered, textured, overwhelming)
   - Retro-futuristic (CRT vibes, neon, chrome)
   - Organic/natural (flowing shapes, earth tones, textures)
   - Luxury/refined (gold accents, serif fonts, dark themes)
   - Playful/toy-like (rounded corners, bright colors, bouncy animations)
   - Editorial/magazine (dramatic typography, asymmetric layouts)
   - Brutalist/raw (exposed structure, unconventional, harsh)
   - Art deco/geometric (patterns, gold, symmetry)
   - Industrial/utilitarian (monospace, yellow/black, functional)

3. **Typography**: Choose distinctive fonts - NEVER use Inter, Roboto, Arial, or generic system fonts. Pick characterful display fonts paired with refined body fonts.

4. **Color Palette**: Commit to a cohesive scheme. Dominant colors with sharp accents beat timid, evenly-distributed palettes.

5. **Signature Element**: What ONE thing will make this unforgettable?

OUTPUT FORMAT:

## Design Direction
[Explain your chosen aesthetic in 2-3 sentences]

## Signature Element
[The ONE memorable thing about this design]

## Color Palette
- Primary: [hex]
- Secondary: [hex]
- Accent: [hex]
- Background: [hex]
- Text: [hex]

## Typography
- Display Font: [font name from Google Fonts]
- Body Font: [font name from Google Fonts]

## Code

```[html/jsx/vue based on requirements]
[Complete, production-ready code with:
- All CSS included (inline styles, styled-components, or Tailwind based on context)
- Animations and micro-interactions
- Responsive design
- Semantic HTML
- Accessibility attributes
- Google Fonts import if needed]
```

CRITICAL RULES:
- NO purple gradients on white backgrounds
- NO generic card layouts
- NO cookie-cutter component patterns
- NEVER use overused fonts (Inter, Space Grotesk, Roboto)
- MAKE IT MEMORABLE - someone should remember this design
- COMMIT to your aesthetic direction - half-measures fail
- INCLUDE working animations and hover states
- USE unexpected layouts: asymmetry, overlap, diagonal flow, grid-breaking
''',
    config=types.GenerateContentConfig(
        system_instruction='You are an elite frontend designer and developer. You create distinctive, production-grade interfaces with bold aesthetic choices. Your code is always complete, functional, and ready for production. You never produce generic or templated designs.',
        temperature=0.9
    )
)
print(response.text)
"
```

### Step 3: Review and Refine Gemini's Output

After Gemini returns the design:

1. **Validate the code** - Ensure it's complete and functional
2. **Check aesthetic commitment** - Is the direction bold enough?
3. **Verify typography** - No generic fonts slipped through?
4. **Enhance animations** - Add more polish if needed
5. **Fix any issues** - Syntax errors, missing imports, etc.

Use Edit/Write tools to save the refined code to appropriate files.

### Step 4: Present Final Design

Display to user:
- Design direction and rationale
- The signature element
- Color palette and typography choices
- Complete, working code

---

## Alternative: Multi-Shot Design Exploration

For more complex projects, spawn multiple Gemini calls with different aesthetic directions:

```bash
# Call 1: Minimal direction
python -c "... aesthetic='brutally minimal' ..."

# Call 2: Maximalist direction
python -c "... aesthetic='maximalist chaos' ..."

# Call 3: User's hinted direction
python -c "... aesthetic='{user_preference}' ..."
```

Then present all options and let user choose, or synthesize the best elements.

---

## Gemini 3 Pro Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Model | `gemini-3-pro-preview` | Best creative reasoning |
| Temperature | `0.9` | High creativity for design |
| Max Tokens | (omitted) | Uses model's maximum - no artificial limit |

---

## Design Quality Checklist

Before presenting to user, verify:

- [ ] **Typography**: Distinctive fonts (not Inter/Roboto/Arial)
- [ ] **Color**: Cohesive palette with clear hierarchy
- [ ] **Layout**: Unexpected/interesting composition
- [ ] **Motion**: Animations on load, hover, and interactions
- [ ] **Details**: Textures, shadows, gradients, or other depth
- [ ] **Accessibility**: Semantic HTML, ARIA labels, contrast
- [ ] **Responsive**: Works on mobile and desktop
- [ ] **Complete**: All code included, no placeholders

---

## Example Usage

**User**: "Build me a pricing page for a SaaS product"

**Workflow**:
1. Parse: Pricing page, SaaS context, likely needs 3 tiers
2. Call Gemini 3 Pro with full prompt
3. Gemini returns: Art deco direction, geometric patterns, gold accents
4. Claude refines: Fixes any code issues, enhances animations
5. Present: Complete pricing page with distinctive aesthetic

---

## Why Gemini 3 Pro?

- **Extended thinking**: Deep reasoning about design choices
- **Creative temperature**: High temperature (0.9) for bold choices
- **Fresh perspective**: Different training data = different aesthetics
- **Complementary**: Gemini ideates, Claude refines

This combination produces designs that neither model would create alone.
