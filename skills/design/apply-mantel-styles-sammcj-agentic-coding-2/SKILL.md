---
name: apply-mantel-styles
description: Provides guidelines for applying Mantel's brand styles to diagrams and frontend components. Use when asked to create visuals that need to align with Mantel's branding.
---

# Rules For Applying Mantel Brand Styles

When creating visual diagrams or frontend components, you can apply the following style guidelines to ensure consistency with the Mantel brand identity.

## Colour Scheme

- You should aim to use the following primary colours from the Mantel brand palette.
- You _may_ also use tints and shades of these colours as needed, but avoid introducing non-brand colours.

<PALETTE>
   Ocean:       #1E5E82 | rgb(30, 94, 130)
   Flamingo:    #D86E89 | rgb(216, 110, 137)
   Deep Ocean:  #002A41 | rgb(0, 42, 65)
   Sky Blue:    #81CCEA | rgb(129, 204, 234)
   Cloud:       #EEF9FD | rgb(238, 249, 253)
</PALETTE>

---

## General Design Principles

<GENERAL_PRINCIPLES>
   <COLOUR_HIERARCHY>
     1. Primary Actions/Elements: Ocean (#1E5E82)
     2. Secondary/Supporting: Sky Blue (#81CCEA)
     3. Emphasis/Accent: Flamingo (#D86E89)
     4. Foundation/Authority: Deep Ocean (#002A41)
     5. Background/Neutral: Cloud (#EEF9FD)
   </COLOUR_HIERARCHY>

   <SEMANTIC_USAGE>
      - Use Ocean for primary actions, main navigation, success states
      - Use Sky Blue for interactive elements, information, secondary actions
      - Use Flamingo sparingly for CTAs, warnings, important highlights
      - Use Deep Ocean for text, borders, authoritative elements
      - Use Cloud for backgrounds, subtle dividers, inactive states
   </SEMANTIC_USAGE>

   <CONSISTENCY_RULES>
      - Avoid mixing colour schemes from other brands
      - Maintain consistent colour meanings across all diagrams in a project
      - When transparency is needed, use rgba values of the brand colours
      - For hover states, darken by 10-15% or lighten by 10-15% staying within brand
   </CONSISTENCY_RULES>
</GENERAL_PRINCIPLES>

---

## Mermaid Styles

Example Mermaid class definitions to apply Mantel brand styles to diagrams

<MERMAID_THEME>
   <!-- Primary elements using Ocean with Cloud fill for readability -->
   classDef process fill:#EEF9FD,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef components fill:#EEF9FD,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef subprocess fill:#EEF9FD,stroke:#1E5E82,stroke-width:1px,color:#002A41,stroke-dasharray:5 5

   <!-- Interactive/Input elements using Sky Blue -->
   classDef inputOutput fill:#81CCEA,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef api fill:#81CCEA,stroke:#002A41,stroke-width:2px,color:#002A41
   classDef user fill:#81CCEA,stroke:#002A41,stroke-width:2px,color:#002A41
   classDef external fill:#81CCEA,stroke:#002A41,stroke-width:2px,color:#002A41,stroke-dasharray:3 3

   <!-- Decision points and important elements using Flamingo -->
   classDef decision fill:#D86E89,stroke:#002A41,stroke-width:2px,color:#FFFFFF
   classDef critical fill:#D86E89,stroke:#002A41,stroke-width:2px,color:#FFFFFF
   classDef error fill:#D86E89,stroke:#002A41,stroke-width:3px,color:#FFFFFF
   classDef warning fill:#D86E8955,stroke:#D86E89,stroke-width:2px,color:#002A41
   classDef security fill:#D86E89,stroke:#002A41,stroke-width:3px,color:#FFFFFF,stroke-dasharray:2 1

   <!-- Data and storage using Deep Ocean -->
   classDef data fill:#002A41,stroke:#1E5E82,stroke-width:2px,color:#EEF9FD
   classDef storage fill:#002A41,stroke:#1E5E82,stroke-width:2px,color:#EEF9FD
   classDef database fill:#002A41,stroke:#1E5E82,stroke-width:2px,color:#EEF9FD
   classDef cache fill:#002A4166,stroke:#1E5E82,stroke-width:2px,color:#002A41

   <!-- State classes -->
   classDef start fill:#1E5E82,stroke:#002A41,stroke-width:3px,color:#EEF9FD
   classDef end fill:#002A41,stroke:#1E5E82,stroke-width:3px,color:#EEF9FD
   classDef success fill:#1E5E8233,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef pending fill:#81CCEA55,stroke:#81CCEA,stroke-width:2px,color:#002A41,stroke-dasharray:5 5
   classDef active fill:#1E5E82,stroke:#002A41,stroke-width:2px,color:#EEF9FD
   classDef complete fill:#1E5E8255,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef disabled fill:#EEF9FD,stroke:#81CCEA66,stroke-width:1px,color:#81CCEA
   classDef inactive fill:#EEF9FD,stroke:#81CCEA66,stroke-width:1px,color:#81CCEA

   <!-- Process types -->
   classDef manual fill:#EEF9FD,stroke:#D86E89,stroke-width:2px,color:#002A41
   classDef automated fill:#EEF9FD,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef async fill:#81CCEA33,stroke:#81CCEA,stroke-width:2px,color:#002A41,stroke-dasharray:8 3
   classDef sync fill:#EEF9FD,stroke:#1E5E82,stroke-width:2px,color:#002A41

   <!-- System elements -->
   classDef system fill:#002A4133,stroke:#002A41,stroke-width:2px,color:#002A41
   classDef network fill:#81CCEA33,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef queue fill:#81CCEA55,stroke:#1E5E82,stroke-width:2px,color:#002A41
   classDef monitoring fill:#EEF9FD,stroke:#81CCEA,stroke-width:2px,color:#002A41,stroke-dasharray:1 1

   <!-- Emphasis and highlights -->
   classDef highlight fill:#D86E8922,stroke:#D86E89,stroke-width:3px,color:#002A41
   classDef focus fill:#1E5E8244,stroke:#1E5E82,stroke-width:3px,color:#002A41
   classDef selected fill:#81CCEA44,stroke:#002A41,stroke-width:3px,color:#002A41

   <!-- Secondary elements -->
   classDef secondary fill:#EEF9FD,stroke:#81CCEA,stroke-width:2px,color:#002A41
   classDef note fill:#EEF9FD,stroke:#81CCEA,stroke-width:1px,color:#1E5E82
   classDef comment fill:#EEF9FD,stroke:#81CCEA,stroke-width:1px,color:#1E5E82,stroke-dasharray:3 3
   classDef optional fill:#EEF9FD,stroke:#81CCEA,stroke-width:1px,color:#002A41,stroke-dasharray:5 5

   <!-- Default styling -->
   classDef default fill:#EEF9FD,stroke:#1E5E82,stroke-width:2px,color:#002A41
</MERMAID_THEME>

<MERMAID_USAGE_GUIDE>
<!-- Core Process Elements -->
- Use 'process' for standard workflow steps
- Use 'subprocess' for nested or child processes
- Use 'components' for system components or modules

<!-- Interactive Elements -->
- Use 'inputOutput' for user interactions or system I/O
- Use 'user' for user/actor specific elements
- Use 'api' for external service connections
- Use 'external' for third-party systems or external dependencies

<!-- Decision and Alert Elements -->
- Use 'decision' for branching logic or critical choices
- Use 'critical' for important warnings or highlights
- Use 'error' for error states or failure conditions
- Use 'warning' for caution states (less severe than errors)
- Use 'security' for security-related checkpoints or processes

<!-- Data Elements -->
- Use 'data' for data objects or data flow
- Use 'storage' or 'database' for persistent storage
- Use 'cache' for temporary storage or caching layers

<!-- State Elements -->
- Use 'start' for process start points
- Use 'end' for process end points
- Use 'success' for successful completion states
- Use 'pending' for waiting or queued states
- Use 'active' for currently running processes
- Use 'complete' for finished processes
- Use 'disabled' or 'inactive' for unavailable elements

<!-- Process Types -->
- Use 'manual' for human/manual processes
- Use 'automated' for automatic processes
- Use 'async' for asynchronous operations
- Use 'sync' for synchronous operations

<!-- System Elements -->
- Use 'system' for internal system components
- Use 'network' for network-related elements
- Use 'queue' for message queues or buffers
- Use 'monitoring' for logging or monitoring components

<!-- Emphasis Elements -->
- Use 'highlight' for temporarily emphasised elements
- Use 'focus' for elements requiring attention
- Use 'selected' for user-selected items

<!-- Supporting Elements -->
- Use 'secondary' for supporting or auxiliary elements
- Use 'note' for annotations or explanatory text
- Use 'comment' for inline comments or documentation
- Use 'optional' for optional steps or components
</MERMAID_USAGE_GUIDE>

<TRANSPARENCY_NOTE>
Note: Some classes use transparency via hex alpha values (e.g., #81CCEA55)
- Last 2 digits represent opacity: FF=100%, CC=80%, 99=60%, 66=40%, 55=33%, 33=20%, 22=13%
- Used for: warning, cache, pending, disabled, system, network, queue, highlight states
- This creates visual hierarchy without introducing non-brand colours
</TRANSPARENCY_NOTE>

<MERMAID_RULES>
- Use <br> instead of \n for line breaks
- Apply standard colour theme unless specified otherwise
- Do NOT use round brackets ( ) within item labels or descriptions
- Mermaid does not support unordered lists within item labels
</MERMAID_RULES>

---

## PlantUML Styles

Apply these colour definitions at the start of PlantUML diagrams

<PLANTUML_RULES>
   !define OCEAN #1E5E82
   !define FLAMINGO #D86E89
   !define DEEP_OCEAN #002A41
   !define SKY_BLUE #81CCEA
   !define CLOUD #EEF9FD

   skinparam backgroundColor CLOUD
   skinparam defaultFontColor DEEP_OCEAN

   ' Activity Diagrams
   skinparam activity {
      BackgroundColor CLOUD
      BorderColor OCEAN
      FontColor DEEP_OCEAN
      StartColor OCEAN
      EndColor DEEP_OCEAN
      BarColor FLAMINGO
      DiamondBackgroundColor SKY_BLUE
      DiamondBorderColor OCEAN
   }

   ' Class Diagrams
   skinparam class {
      BackgroundColor CLOUD
      BorderColor OCEAN
      FontColor DEEP_OCEAN
      AttributeFontColor OCEAN
      StereotypeFontColor SKY_BLUE
      ArrowColor OCEAN
      HeaderBackgroundColor SKY_BLUE
   }

   ' Sequence Diagrams
   skinparam sequence {
      ParticipantBackgroundColor SKY_BLUE
      ParticipantBorderColor OCEAN
      ActorBackgroundColor CLOUD
      ActorBorderColor DEEP_OCEAN
      LifeLineBorderColor OCEAN
      ArrowColor OCEAN
      GroupBackgroundColor CLOUD
      GroupBorderColor SKY_BLUE
      NoteBackgroundColor CLOUD
      NoteBorderColor FLAMINGO
   }

   ' Component Diagrams
   skinparam component {
      BackgroundColor CLOUD
      BorderColor OCEAN
      FontColor DEEP_OCEAN
      InterfaceBackgroundColor SKY_BLUE
      InterfaceBorderColor DEEP_OCEAN
   }

   ' State Diagrams
   skinparam state {
      BackgroundColor CLOUD
      BorderColor OCEAN
      FontColor DEEP_OCEAN
      StartColor OCEAN
      EndColor DEEP_OCEAN
      AttributeFontColor OCEAN
   }

   ' Use Case Diagrams
   skinparam usecase {
      BackgroundColor CLOUD
      BorderColor OCEAN
      FontColor DEEP_OCEAN
      ActorBackgroundColor SKY_BLUE
      ActorBorderColor DEEP_OCEAN
   }

   ' Error/Warning States
   skinparam note {
      BackgroundColor<<warning>> FLAMINGO
      BorderColor<<warning>> DEEP_OCEAN
      FontColor<<warning>> CLOUD
   }
</PLANTUML_RULES>

---

## Frontend Component Styles

<CSS_VARIABLES>
   :root {
      /* Primary Colours */
      --brand-ocean: #1E5E82;
      --brand-flamingo: #D86E89;
      --brand-deep-ocean: #002A41;
      --brand-sky-blue: #81CCEA;
      --brand-cloud: #EEF9FD;

      /* Semantic Mappings */
      --colour-primary: var(--brand-ocean);
      --colour-primary-dark: var(--brand-deep-ocean);
      --colour-secondary: var(--brand-sky-blue);
      --colour-accent: var(--brand-flamingo);
      --colour-background: var(--brand-cloud);
      --colour-surface: #FFFFFF;

      /* Text Colours */
      --text-primary: var(--brand-deep-ocean);
      --text-secondary: var(--brand-ocean);
      --text-on-primary: var(--brand-cloud);
      --text-on-accent: #FFFFFF;

      /* State Colours */
      --colour-error: var(--brand-flamingo);
      --colour-warning: var(--brand-flamingo);
      --colour-success: var(--brand-ocean);
      --colour-info: var(--brand-sky-blue);

      /* Shadows and Overlays */
      --shadow-colour: rgba(0, 42, 65, 0.1);
      --overlay-light: rgba(238, 249, 253, 0.9);
      --overlay-dark: rgba(0, 42, 65, 0.8);
   }
</CSS_VARIABLES>

<COMPONENT_GUIDELINES>
   <BUTTONS>
   Primary:
      - Background: Ocean (#1E5E82)
      - Text: Cloud (#EEF9FD)
      - Hover: Deep Ocean (#002A41)
      - Border: none or Ocean

   Secondary:
      - Background: Sky Blue (#81CCEA)
      - Text: Deep Ocean (#002A41)
      - Hover: Ocean (#1E5E82) with Cloud text
      - Border: Ocean (#1E5E82)

   Accent/CTA:
      - Background: Flamingo (#D86E89)
      - Text: White (#FFFFFF)
      - Hover: Darker Flamingo (darken by 10%)
      - Border: none

   Ghost/Outline:
      - Background: transparent
      - Text: Ocean (#1E5E82)
      - Hover: Cloud (#EEF9FD) background
      - Border: Ocean (#1E5E82)
   </BUTTONS>

   <NAVIGATION>
   Header:
      - Background: Deep Ocean (#002A41)
      - Text: Cloud (#EEF9FD)
      - Active: Sky Blue (#81CCEA)
      - Hover: Ocean (#1E5E82) background

   Sidebar:
      - Background: Cloud (#EEF9FD)
      - Text: Deep Ocean (#002A41)
      - Active: Ocean (#1E5E82) with Cloud text
      - Hover: Sky Blue (#81CCEA) background
   </NAVIGATION>

   <FORMS>
   Input Fields:
      - Background: White (#FFFFFF)
      - Border: Sky Blue (#81CCEA)
      - Focus Border: Ocean (#1E5E82)
      - Text: Deep Ocean (#002A41)
      - Placeholder: Sky Blue (#81CCEA)
      - Error Border: Flamingo (#D86E89)

   Labels:
      - Colour: Ocean (#1E5E82)
      - Required Indicator: Flamingo (#D86E89)
   </FORMS>

   <!-- Cards and Surfaces -->
   <CARDS>
   Standard Card:
      - Background: White (#FFFFFF)
      - Border: Cloud (#EEF9FD)
      - Shadow: rgba(0, 42, 65, 0.1)

   Highlighted Card:
      - Background: Cloud (#EEF9FD)
      - Border: Sky Blue (#81CCEA)
      - Shadow: rgba(30, 94, 130, 0.15)
   </CARDS>

   <!-- Alerts and Messages -->
   <ALERTS>
   Error:
      - Background: Flamingo (#D86E89) at 10% opacity
      - Border: Flamingo (#D86E89)
      - Text: Deep Ocean (#002A41)
      - Icon: Flamingo (#D86E89)

   Warning:
      - Background: Flamingo (#D86E89) at 5% opacity
      - Border: Flamingo (#D86E89) at 50%
      - Text: Deep Ocean (#002A41)
      - Icon: Flamingo (#D86E89)

   Success:
      - Background: Ocean (#1E5E82) at 10% opacity
      - Border: Ocean (#1E5E82)
      - Text: Deep Ocean (#002A41)
      - Icon: Ocean (#1E5E82)

   Info:
      - Background: Sky Blue (#81CCEA) at 10% opacity
      - Border: Sky Blue (#81CCEA)
      - Text: Deep Ocean (#002A41)
      - Icon: Sky Blue (#81CCEA)
   </ALERTS>

   <!-- Data Visualisation -->
   <CHARTS>
      Primary Series: Ocean (#1E5E82)
      Secondary Series: Sky Blue (#81CCEA)
      Tertiary Series: Deep Ocean (#002A41)
      Highlight/Accent: Flamingo (#D86E89)
      Background: Cloud (#EEF9FD)
      Grid Lines: Sky Blue (#81CCEA) at 20% opacity
      Text: Deep Ocean (#002A41)
   </CHARTS>

</COMPONENT_GUIDELINES>

<!-- Tailwind Configuration -->
<TAILWIND_CONFIG>
   module.exports = {
      theme: {
         extend: {
         colours: {
            'brand': {
               'ocean': '#1E5E82',
               'flamingo': '#D86E89',
               'deep-ocean': '#002A41',
               'sky-blue': '#81CCEA',
               'cloud': '#EEF9FD',
            }
         }
         }
      }
   }
</TAILWIND_CONFIG>

---

## Fonts & Typography

<TYPOGRAPHY>
  - Where applicable use the 'Inter' typeface is utilised for headlines, subheadings, and body copy.
  - Favour bundling the font for offline use over relying on CDNs.
  <INTER_CDN note="If bundling is not possible, you may use this CDN">
    <!-- HTML in your document's head -->
    <link rel="preconnect" href="https://rsms.me/">
    <link rel="stylesheet" href="https://rsms.me/inter/inter.css">

    /* CSS */
    :root {
      font-family: Inter, sans-serif;
      font-feature-settings: 'liga' 1, 'calt' 1; /* fix for Chrome */
    }
    @supports (font-variation-settings: normal) {
      :root { font-family: InterVariable, sans-serif; }
    }
  </INTER_CDN>
</TYPOGRAPHY>

---

This information should help you maintain visual consistency with the Mantel brand across diagrams and frontend components.
