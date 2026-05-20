---
name: generate-lifestyle-shot
description: Generate lifestyle imagery using the jocko-imagery MCP server
user-invocable: true
---

You are helping the marketing team generate lifestyle imagery featuring Jocko Fuel products in real-world contexts.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+jocko-imagery` to load the jocko-imagery MCP tools. All tools below are prefixed with `mcp__jocko-imagery__` (e.g., `mcp__jocko-imagery__generate_image`).

Follow these steps:

### Step 1: Define the Scene

Ask the user for:
- **Product(s)** — which Jocko Fuel products to feature
- **Setting** — gym, kitchen, outdoor, office, pre-workout, post-workout, etc.
- **Mood** — energetic, focused, disciplined, recovery, community
- **Purpose** — blog hero image, social media post, email banner, ad creative

### Step 2: Configure Lifestyle Parameters

Discuss composition details:
- **Scene type** — product in environment, product in use, flat lay, action shot
- **Color palette** — brand colors (black, red, military green), warm tones, cool tones
- **People** — include person (silhouette/partial), hands-only, or product-only
- **Props** — gym equipment, water bottle, shaker, healthy food, etc.
- **Format** — square (1:1), landscape (16:9), portrait (9:16), or custom

### Step 3: Generate the Image

Use the appropriate `mcp__jocko-imagery__` tool to generate the lifestyle shot with:
- Scene and product details from Steps 1-2
- Jocko Fuel brand aesthetic (bold, authentic, military-inspired)

### Step 4: Review and Iterate

Present the generated image to the user. Offer:
- **Approve** — image is ready to use
- **Adjust** — modify scene, mood, or composition and regenerate
- **Series** — generate a set of related lifestyle shots for a campaign

### Error Handling

- If MCP tools are unavailable, inform the user that the jocko-imagery server may need reconnection
- If generation fails, suggest simplifying the scene or adjusting parameters
- If the scene is too complex, break it into simpler compositions
