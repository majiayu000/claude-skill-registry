---
name: build-ui
description: Build user interface. Clean, modern, works on all devices.
---

# Build UI

When building the visual interface:
1. Mobile-first — design for phone screens first, then scale up
2. Clean and simple — lots of white space, clear typography, obvious buttons
3. No framework unless needed — plain HTML/CSS handles 80% of cases
4. Test on narrow viewport (375px) and wide viewport (1440px)

Default style:
- White background, dark text
- System fonts (fast loading, familiar to users)
- Large tap targets for mobile (minimum 44px)
- One accent color, not a rainbow

Tell user: "页面做好了，手机和电脑都能用。你打开看看效果。"

If user says "不好看" — ask what they want changed specifically. Don't redesign everything.
