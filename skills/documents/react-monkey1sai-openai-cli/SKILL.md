---
name: react_docs
description: Use when working with react_docs
---

# React_Docs Skill

Use when working with react_docs, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with react_docs
- Asking about react_docs features or APIs
- Implementing react_docs solutions
- Debugging react_docs code
- Learning react_docs best practices

## Quick Reference

### Common Patterns

**Pattern 1:** API ReferenceComponents<Activity><Activity> lets you hide and restore the UI and internal state of its children

```
<Activity>
```

**Pattern 2:** Posts was able to prepare itself for a faster render, thanks to the hidden Activity boundary

```
Posts
```

**Pattern 3:** Learn ReactInstallationAdd React to an Existing ProjectIf you want to add some interactivity to your existing project, you don’t have to rewrite it...

```
example.com
```

**Pattern 4:** If the entire content of your page was replaced by a “Hello, world!”, everything worked! Keep reading

```
import { createRoot } from 'react-dom/client';// Clear the existing HTML contentdocument.body.innerHTML = '<div id="app"></div>';// Render your React component insteadconst root = createRoot(document.getElementById('app'));root.render(<h1>Hello, world</h1>);
```

**Pattern 5:** Instead, you probably want to render your React components in specific places in your HTML

```
id
```

**Pattern 6:** API ReferenceLegacy React APIsChildrenPitfallUsing Children is uncommon and can lead to fragile code

```
Children
```

**Pattern 7:** Deep DiveWhy is the children prop not always an array? Show DetailsIn React, the children prop is considered an opaque data structure

```
children
```

**Pattern 8:** Learn ReactManaging StateChoosing the State StructureStructuring state well can make a difference between a component that is pleasant to modify an...

```
const [x, setX] = useState(0);const [y, setY] = useState(0);
```

### Example Code Patterns

**Example 1** (jsx):
```jsx
const [index, setIndex] = useState(0);const [showMore, setShowMore] = useState(false);
```

**Example 2** (javascript):
```javascript
console.log(count);  // 0setCount(count + 1); // Request a re-render with 1console.log(count);  // Still 0!
```

**Example 3** (python):
```python
npm create vite@latest my-app -- --template react-ts
```

**Example 4** (jsx):
```jsx
<Activity mode={visibility}>  <Sidebar /></Activity>
```

**Example 5** (jsx):
```jsx
<Activity mode={isShowingSidebar ? "visible" : "hidden"}>  <Sidebar /></Activity>
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **components.md** - Components documentation
- **getting_started.md** - Getting Started documentation
- **hooks.md** - Hooks documentation
- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
