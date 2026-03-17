---
name: "Landing Page Steal"
description: "Copies an existing landing page (from URL or image) into a specified page in the codebase using Playwright MCP. Iteratively refines the implementation until it matches the reference design and interactions as closely as possible. Use when the user wants to copy/reference/steal an existing landing page/url to replicate in their app"
version: "1.0.0"
dependencies: ["playwright-mcp"]
allowed-tools: ["playwright", "file_write", "file_read", "screenshot"]
---

# Landing Page Redesign

## Instructions

When requested to redesign a landing page based on a reference:

### 1. **User Interview**
   - If not provided in the initial request, ask the user for:
     - **Reference URL or Image**: The landing page or design to replicate (can be a live website URL or an image URL)
     - **Target Page**: Which file in the codebase should receive the design (e.g., `app/(tabs)/index.tsx`, `app/landing.tsx`)
   - If details are provided in the initial request, skip to step 2

### 2. **Capture Reference Design**
   - Use Playwright MCP to open the reference URL:
     - Navigate to the page
     - Take a full-page screenshot to understand structure
     - Interact with the website, mouse hover, click around
     - Analyze the page deeply
   - Analyze the landing page/image for:
     - Layout structure (header, hero, sections, footer)
     - Interactive elements
     - Color palette
     - Typography (fonts, sizes, weights)
     - Spacing and padding patterns
     - UI components (buttons, cards, forms, etc.)
     - Responsive design patterns

### 3. **Implement the Design**
   - Read the target page file to understand current structure
   - Implement the design following these principles:
     - **Match the layout**: Replicate section structure, grid layouts, flex patterns
      - **Match the intractions**: Replicate mouse and button interactions, whether clicks or hovers - on key elements
     - **Match colors**: Extract and use exact hex values from the reference
     - **Match typography**: Use similar fonts (adjust to available system fonts or suggest font imports)
     - **Match spacing**: Replicate padding, margins, and gaps
     - **Match components**: Build equivalent React Native components for buttons, cards, inputs, etc.
     - **Follow project patterns**: Use StyleSheet.create() as per CLAUDE.md guidelines
     - **Mobile-first**: Ensure the design works on mobile (Expo/React Native)
   - Write the implementation to the target file

### 4. **Compare Implementations**
   - If the reference is a live website:
     - Take a screenshot of the implemented page
     - Use Playwright to view your implementation
   - Visually compare:
     - Layout alignment and proportions
     - Color accuracy
     - Typography consistency
     - Spacing and padding
     - Component styling details
   - Document differences found

### 5. **Iterate and Refine**
   - Based on comparison, identify specific gaps:
     - Layout issues (alignment, sizing, positioning)
     - Color mismatches
     - Typography differences
     - Missing components or details
     - Spacing inconsistencies
   - Make targeted refinements to address each gap
   - Repeat steps 4-5 until:
     - The design matches as closely as technically possible
     - All major visual elements are replicated
     - User confirms satisfaction
   - **Aim for 3-5 iterations** minimum to achieve high fidelity

### 6. **Final Review**
   - Present the final implementation to the user
   - Summarize what was matched and any intentional differences
   - Suggest any follow-up improvements (e.g., animations, hover states, responsive tweaks)

## Best Practices

- **Be detail-oriented**: Small differences in spacing, colors, or typography can break the visual consistency
- **Extract exact values**: Use color pickers and measurement tools to get precise values from screenshots
- **Component reusability**: Extract repeated patterns into reusable components
- **Maintain project standards**: Follow the StyleSheet.create() pattern and existing architecture
- **Document trade-offs**: If React Native limitations prevent exact replication, document why

## Example Flow

**User request:** "Make our landing page look like https://stripe.com/payments"

1. **Interview**: Ask "Which file should receive this design?" → User: "app/(tabs)/index.tsx"
2. **Capture**:
   - Navigate to stripe.com/payments
   - Take full-page screenshot
   - Analyze deeply: Dark theme, gradient hero, feature grid, clean typography, button changes color upon hover/click
3. **Implement**:
   - Read app/(tabs)/index.tsx
   - Build based on reference
4. **Compare**:
   - Screenshot shows hero gradient is lighter than reference
   - Button border-radius is too sharp
   - Font weights don't match
   - Button doesn't change upon hover
5. **Iterate**:
   - Adjust gradient colors to match
   - Reduce border-radius on buttons
   - Increase font weights
   - button changes upon hover/click
   - Re-compare
6. **Iterate again**:
   - Fine-tune spacing between sections
   - Adjust icon sizes
   - Match exact color values
7. **Final review**: Present to user with summary of matched elements

## Technical Notes

- **React Native considerations**:
  - Web fonts may need to be loaded via expo-font or google fonts
  - Some web-specific effects (box-shadow) have React Native equivalents (shadowColor, shadowOffset)
  - Use Dimensions API for responsive layouts

- **Iteration targets**:
  - First iteration: Overall layout and structure
  - Second iteration: Colors and typography
  - Third iteration: Spacing and sizing refinement
  - Fourth+ iterations: Fine details and polish

## References

- [Playwright MCP Documentation](https://github.com/executeautomation/mcp-playwright)
- [Expo Style Guide](https://docs.expo.dev/develop/user-interface/style/)
- [React Native StyleSheet](https://reactnative.dev/docs/stylesheet)
