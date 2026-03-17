---
name: generate-product-shot
description: Generate product photography using the jocko-imagery MCP server
user-invocable: true
---

You are helping the marketing team generate product photography for Jocko Fuel products.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+jocko-imagery` to load the jocko-imagery MCP tools. All tools below are prefixed with `mcp__jocko-imagery__` (e.g., `mcp__jocko-imagery__generate_image`).

Follow these steps:

### Step 1: Identify the Product

Ask the user for:
- **Product name** or SKU (e.g., "Discipline GO", "Jocko Fuel Protein")
- **Flavor/variant** if applicable
- **Purpose** — what the image will be used for (website PDP, social media, email, ad creative)

### Step 2: Configure Shot Parameters

Ask the user about preferred style:
- **Background** — white/clean studio, gradient, lifestyle setting, or transparent
- **Angle** — front-facing, 3/4 angle, top-down, or hero shot
- **Composition** — single product, product group, or product with props
- **Lighting** — studio bright, dramatic/moody, or natural light
- **Format** — square (1:1), landscape (16:9), portrait (9:16), or custom

### Step 3: Generate the Image

Use the appropriate `mcp__jocko-imagery__` tool to generate the product shot with:
- Product details from Step 1
- Style parameters from Step 2
- Jocko Fuel brand aesthetics (bold, clean, military-inspired)

### Step 4: Review and Iterate

Present the generated image to the user. Offer:
- **Approve** — image is ready to use
- **Adjust** — modify specific parameters and regenerate
- **Variant** — generate additional angles or styles of the same product

### Error Handling

- If MCP tools are unavailable, inform the user that the jocko-imagery server may need reconnection
- If generation fails, suggest simplifying the prompt or adjusting parameters
- If the product is not recognized, ask the user for more specific details
