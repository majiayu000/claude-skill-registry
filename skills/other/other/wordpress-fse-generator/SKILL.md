---
name: generating-wordpress-fse-blocks
description: Generates WordPress Full Site Editing blocks and theme files. Use when the user asks about block.json, Gutenberg blocks, FSE themes, WordPress block development, or theme.json configuration.
---

# WordPress FSE Theme Code Generator

## When to use this skill

- User asks to create a Gutenberg block
- User mentions Full Site Editing or FSE
- User wants to scaffold block.json files
- User asks about WordPress theme.json
- User needs block templates or patterns

## Workflow

- [ ] Identify block or theme requirement
- [ ] Generate block.json with attributes
- [ ] Create edit component (React/JSX)
- [ ] Create save component
- [ ] Add block styles
- [ ] Register in PHP
- [ ] Update theme.json if needed

## Instructions

### Step 1: Identify Block Type

| Block Type   | Use Case                      | Complexity |
| ------------ | ----------------------------- | ---------- |
| Static       | Content display only          | Low        |
| Dynamic      | Server-rendered, PHP callback | Medium     |
| Interactive  | Client-side JS behavior       | High       |
| Inner Blocks | Container with nested blocks  | Medium     |

### Step 2: Create Block Structure

```bash
mkdir -p src/blocks/my-block
touch src/blocks/my-block/{block.json,edit.tsx,save.tsx,index.ts,style.scss,editor.scss}
```

### Step 3: Generate Block Files

See [examples/block-templates.md](examples/block-templates.md) for complete templates:

- block.json with attributes and supports
- Edit component with InspectorControls and MediaUpload
- Save component (static) and render.php (dynamic)
- Block registration (JS and PHP)
- Block styles (frontend and editor)

### Step 4: Configure theme.json

See [examples/theme-json.md](examples/theme-json.md) for:

- Color palette and typography settings
- Spacing scale configuration
- Layout settings (content/wide)
- Custom font registration
- Block-specific styles
- Template parts and custom templates

### Step 5: Setup functions.php

See [examples/functions-php.md](examples/functions-php.md) for:

- Block registration hooks
- Asset enqueueing
- Block category registration
- Block patterns
- Theme support setup

### Quick Reference: block.json Attributes

```json
{
  "attributes": {
    "text": { "type": "string", "default": "" },
    "number": { "type": "number", "default": 0 },
    "boolean": { "type": "boolean", "default": false },
    "array": { "type": "array", "default": [] },
    "object": { "type": "object", "default": {} }
  }
}
```

### Quick Reference: Block Supports

```json
{
  "supports": {
    "html": false,
    "align": ["wide", "full"],
    "color": { "background": true, "text": true },
    "spacing": { "margin": true, "padding": true },
    "typography": { "fontSize": true }
  }
}
```

## Validation

Before completing:

- [ ] block.json schema validates
- [ ] Block appears in inserter
- [ ] Edit component renders in editor
- [ ] Save outputs valid HTML
- [ ] Styles apply correctly
- [ ] PHP render works (if dynamic)

```bash
npm run build
npm run lint:js
npm run lint:css
```

## Error Handling

- **Block not appearing**: Check block.json name matches registration and category exists.
- **Validation error**: Ensure save output matches stored content exactly.
- **Styles not loading**: Verify file paths in block.json are correct.
- **PHP render not working**: Check render.php exists and block.json has `render` key.
- **TypeScript errors**: Install @wordpress/blocks types: `npm i -D @types/wordpress__blocks`.

## Resources

- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [block.json Schema](https://schemas.wp.org/trunk/block.json)
- [theme.json Reference](https://developer.wordpress.org/block-editor/reference-guides/theme-json-reference/)
- [@wordpress/scripts](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-scripts/)
