---
name: block-editor-components
description: React editor components for WordPress blocks in Oh My Brand! theme. useBlockProps, InspectorControls, MediaUpload, and attributes. Use when writing edit.tsx files.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# Block Editor Components

React editor components for WordPress blocks in the Oh My Brand! FSE theme.

---

## When to Use

- Creating editor UI for WordPress blocks
- Adding sidebar controls (InspectorControls)
- Implementing media selection (MediaUpload)
- Handling block attributes and state

---

## Reference Files

| File | Purpose |
|------|---------|
| [edit-gallery-example.tsx](references/edit-gallery-example.tsx) | Full gallery edit component (~155 lines) |
| [edit.tsx](../block-scaffolds/references/edit.tsx) | Edit component scaffold |

---

## Basic Edit Component

```tsx
import { __ } from '@wordpress/i18n';
import { useBlockProps, InspectorControls } from '@wordpress/block-editor';
import { PanelBody, RangeControl, ToggleControl } from '@wordpress/components';
import type { BlockEditProps } from '@wordpress/blocks';

interface BlockAttributes {
    count: number;
    isEnabled: boolean;
}

export default function Edit({
    attributes,
    setAttributes,
}: BlockEditProps<BlockAttributes>): JSX.Element {
    const { count, isEnabled } = attributes;
    const blockProps = useBlockProps();

    return (
        <>
            <InspectorControls>
                <PanelBody title={__('Settings', 'theme-oh-my-brand')}>
                    <RangeControl
                        label={__('Count', 'theme-oh-my-brand')}
                        value={count}
                        onChange={(value) => value !== undefined && setAttributes({ count: value })}
                        min={1}
                        max={10}
                    />
                    <ToggleControl
                        label={__('Enable Feature', 'theme-oh-my-brand')}
                        checked={isEnabled}
                        onChange={(value) => setAttributes({ isEnabled: value })}
                    />
                </PanelBody>
            </InspectorControls>
            <div {...blockProps}>
                {/* Block content */}
            </div>
        </>
    );
}
```

See [edit-gallery-example.tsx](references/edit-gallery-example.tsx) for a complete implementation with MediaUpload.

---

## useBlockProps

```tsx
// Basic usage
const blockProps = useBlockProps();

// With additional classes
const blockProps = useBlockProps({ className: 'custom-class' });

// With data attributes
const blockProps = useBlockProps({
    className: 'wp-block-theme-oh-my-brand-gallery',
    'data-visible': visibleImages,
});

// Apply to wrapper
return <div {...blockProps}>Content</div>;
```

---

## InspectorControls

Add sidebar panel controls:

```tsx
<InspectorControls>
    <PanelBody title={__('Settings', 'theme-oh-my-brand')} initialOpen={true}>
        <RangeControl
            label={__('Visible Items', 'theme-oh-my-brand')}
            value={visibleItems}
            onChange={(value) => setAttributes({ visibleItems: value })}
            min={1}
            max={6}
        />
        <ToggleControl
            label={__('Enable Feature', 'theme-oh-my-brand')}
            checked={enableFeature}
            onChange={(value) => setAttributes({ enableFeature: value })}
        />
        <SelectControl
            label={__('Layout', 'theme-oh-my-brand')}
            value={layout}
            onChange={(value) => setAttributes({ layout: value })}
            options={[
                { label: __('Grid', 'theme-oh-my-brand'), value: 'grid' },
                { label: __('Carousel', 'theme-oh-my-brand'), value: 'carousel' },
            ]}
        />
        <TextControl
            label={__('Caption', 'theme-oh-my-brand')}
            value={caption}
            onChange={(value) => setAttributes({ caption: value })}
        />
    </PanelBody>
</InspectorControls>
```

---

## MediaUpload

### Single Image

```tsx
<MediaUploadCheck>
    <MediaUpload
        onSelect={(media) => setAttributes({
            imageId: media.id,
            imageUrl: media.sizes?.large?.url || media.url,
            imageAlt: media.alt || '',
        })}
        allowedTypes={['image']}
        value={imageId}
        render={({ open }) => (
            <Button variant="primary" onClick={open}>
                {imageUrl ? __('Replace', 'theme-oh-my-brand') : __('Select', 'theme-oh-my-brand')}
            </Button>
        )}
    />
</MediaUploadCheck>
```

### Multiple Images (Gallery)

```tsx
<MediaUploadCheck>
    <MediaUpload
        onSelect={(media) => {
            const selected = media.map((item) => ({
                id: item.id,
                url: item.sizes?.large?.url || item.url,
                alt: item.alt || '',
            }));
            setAttributes({ images: selected });
        }}
        allowedTypes={['image']}
        multiple={true}
        gallery={true}
        value={images.map((img) => img.id)}
        render={({ open }) => (
            <Button variant="primary" onClick={open}>
                {hasImages ? __('Edit Gallery', 'theme-oh-my-brand') : __('Select', 'theme-oh-my-brand')}
            </Button>
        )}
    />
</MediaUploadCheck>
```

---

## Block Attributes

### Type Definitions

```tsx
interface BlockAttributes {
    title: string;
    count: number;
    isEnabled: boolean;
    images: ImageData[];
}

interface ImageData {
    id: number;
    url: string;
    alt: string;
}
```

### Setting Attributes

```tsx
// Single attribute
setAttributes({ title: 'New Title' });

// Multiple attributes
setAttributes({ title: 'New Title', count: 5 });

// Array attribute
setAttributes({ images: [...images, newImage] });
```

### Attribute Defaults (block.json)

```json
"attributes": {
    "title": { "type": "string", "default": "" },
    "count": { "type": "number", "default": 3 },
    "isEnabled": { "type": "boolean", "default": true },
    "images": { "type": "array", "default": [] }
}
```

---

## Common Patterns

### Placeholder State

```tsx
import { Placeholder } from '@wordpress/components';
import { gallery as blockIcon } from '@wordpress/icons';

{!hasContent && (
    <Placeholder
        icon={blockIcon}
        label={__('Block Name', 'theme-oh-my-brand')}
        instructions={__('Instructions for the user.', 'theme-oh-my-brand')}
    >
        <Button variant="primary" onClick={handleAdd}>
            {__('Add Content', 'theme-oh-my-brand')}
        </Button>
    </Placeholder>
)}
```

### Toolbar Controls

```tsx
import { BlockControls } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';

<BlockControls>
    <ToolbarGroup>
        <ToolbarButton icon={edit} label={__('Edit', 'theme-oh-my-brand')} onClick={handleEdit} />
        <ToolbarButton icon={trash} label={__('Remove', 'theme-oh-my-brand')} onClick={handleRemove} />
    </ToolbarGroup>
</BlockControls>
```

---

## Related Skills

- [typescript-standards](../typescript-standards/SKILL.md) - TypeScript conventions
- [native-block-development](../native-block-development/SKILL.md) - Block structure
- [block-scaffolds](../block-scaffolds/SKILL.md) - Edit component template

---

## References

- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [Component Reference](https://developer.wordpress.org/block-editor/reference-guides/components/)
- [@wordpress/block-editor](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-block-editor/)
