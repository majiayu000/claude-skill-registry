---
name: slides
description: Generate high-quality, single-file HTML interactive slide decks. Use this skill when the user asks to create a presentation, slide deck, or PPT.
metadata:
  author: Yuga Sun
  version: "2026.01.29"
---

# Interactive HTML Slide Generator

## Instructions

Act as an expert Frontend Developer and Presentation Designer to generate a "Keynote-quality" single-file HTML presentation.

1.  **Analyze Content**: Transform user input into a logical slide outline (8-12 slides).
2.  **Apply Design**: Use the "Cyberpunk Professional" theme defined below.
3.  **Visual Assets**: If necessary, use **Nano Banana Pro** to generate high-quality images for slide content.
4.  **Generate Code**: Output a single `index.html` file containing all CSS, JS, and HTML.
5.  **Save Output**: Save the file to `slides/<ppt-name>/dist/index.html`.

## Design Philosophy & System
- **Theme**: "Cyberpunk Professional" / Dark Tech.
- **Background**: Deep dark background (`#030712`) with subtle animated grid or radial gradients.
- **Glassmorphism**: Slides use `rgba(17, 24, 39, 0.85)` with `backdrop-filter: blur(20px)` and thin borders.
- **Typography**:
  - Headings: 'Space Grotesk' (Google Fonts) - Tech/Modern feel.
  - Body: 'Inter' (Google Fonts) - Clean/Readable.
  - Code: 'JetBrains Mono' (Google Fonts) - Developer focus.
- **Color Palette**:
  - Background: `#030712` (`--bg-color`)
  - Primary Accent: Cyan `#06b6d4` (`--accent-primary`)
  - Secondary Accent: Violet `#8b5cf6` (`--accent-secondary`)
  - Warning/Highlight: Amber `#f59e0b` (`--accent-warning`)
  - Text: `#f8fafc` (Main, `--text-main`), `#94a3b8` (Muted, `--text-muted`)

## Technical Requirements
1. **Output Path & Format**: Output must be a single `index.html` file (containing all CSS/JS) located at `slides/<ppt-name>/dist/index.html`.
2. **External Assets**: Use CDNs for Fonts (Google Fonts) and Icons (FontAwesome). Images should be Unsplash URLs or placeholders.
3. **Responsiveness**: Implement the "Scale-to-Fit" logic for mobile devices.
   - **Desktop**: Single slide view, hidden overflow.
   - **Mobile (<768px)**: Vertical scrolling list of slides. Each slide is forced to 1280x720 but scaled down (using `transform: scale()`) to fit the screen width, with margin adjustments to remove gaps.

## Mobile Styling Specification
The generated CSS **must** include this exact media query block to handle the complex scaling logic:

```css
@media (max-width: 768px) {
    body {
        overflow-y: auto !important;
        height: auto !important;
        display: block !important;
        padding: 20px 0;
        background-attachment: scroll;
    }

    #deck {
        width: 100% !important;
        height: auto !important;
        max-width: none !important;
        max-height: none !important;
        aspect-ratio: auto !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 0; 
        padding: 0;
        align-items: center;
        overflow: hidden;
    }

    .slide-container {
        /* Force visible (Override JS) */
        position: relative !important;
        opacity: 1 !important;
        visibility: visible !important;
        transform: none !important;
        
        /* Force Desktop Dimensions */
        width: 1280px !important;
        height: 720px !important;
        min-height: 720px !important;
        flex-shrink: 0;
        
        /* Scale using JS-calculated variable */
        transform: scale(var(--scale, 0.3)) !important;
        transform-origin: top center !important;
        
        /* Layout Fix: Close the gap caused by scaling */
        margin-bottom: calc(720px * var(--scale, 0.3) - 720px + 20px) !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        left: auto !important;
        top: auto !important;
        
        border-radius: 24px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }

    .controls, .progress-bar { 
        display: none !important; 
    }
    
    .animate-in {
        opacity: 1 !important;
        animation: none !important;
        transform: none !important;
    }
}
```

## Navigation Strategies
1. **Desktop**: 
   - Keyboard (Arrow keys, Space).
   - On-screen buttons (Next/Prev).
   - Progress bar at the bottom.
2. **Mobile**:
   - Native scroll interaction (Vertical list).
   - Hide controls and progress bar.

## Animations
Staggered entry animations (`.animate-in`, `.delay-1`, etc.) for elements within a slide.

## Slide Templates

### 1. Structure
All slides live inside a `#deck` container.
```html
<div class="slide-container" id="slideX">
  <div class="content-area">
    <!-- Content here -->
  </div>
</div>
```

### 2. Common Layouts
- **Cover Slide**: Large H1 with gradient text, subtitle, and call-to-action pill.
- **Split Layout**: `.grid-2` (Left Content / Right Image) for defining concepts.
- **Tiled Grid**: `.grid-tiled` (2-4 cards) for features/stat cards.
- **Timeline**: `.timeline` with `.timeline-item` and `.dot` for roadmaps.
- **Stats**: `.stat-grid` with `.stat-item` and `.num` for data visualization.
- **Comparison Table**: `.table-container` for pros/cons.

## Boilerplate Code
Always start with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {
            --bg-color: #030712;
            --slide-bg: rgba(17, 24, 39, 0.85);
            --accent-primary: #06b6d4;
            --accent-secondary: #8b5cf6;
            --accent-warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --glass-border: rgba(255, 255, 255, 0.08);
            --neon-glow: 0 0 20px rgba(6, 182, 212, 0.15);
        }

        * { box-sizing: border-box; }

        body {
            background-color: var(--bg-color);
            background-image:
                radial-gradient(circle at 15% 50%, rgba(139, 92, 246, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(6, 182, 212, 0.08), transparent 25%);
            margin: 0;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            color: var(--text-main);
        }

        #deck {
            width: 1280px;
            height: 720px;
            position: relative;
            transform: scale(var(--scale, 1));
            aspect-ratio: 16/9;
        }

        .slide-container {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background-color: var(--slide-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6), var(--neon-glow);
            border: 1px solid var(--glass-border);
            padding: 60px 80px;
            display: flex;
            flex-direction: column;
            opacity: 0;
            transform: scale(0.95);
            pointer-events: none;
            transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1), transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .slide-container.active {
            opacity: 1;
            transform: scale(1);
            pointer-events: auto;
            z-index: 10;
        }

        /* Typography */
        h1, h2, h3 {
            font-family: 'Space Grotesk', 'Noto Sans SC', sans-serif;
            margin: 0;
            color: var(--text-main);
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 72px;
            line-height: 1.1;
            font-weight: 700;
            background: linear-gradient(135deg, #fff 30%, var(--accent-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h2 { font-size: 48px; font-weight: 600; margin-bottom: 2rem; position: relative; }
        h2::after { 
            content: ''; display: block; width: 60px; height: 4px; 
            background: var(--accent-primary); margin-top: 16px; border-radius: 2px;
        }
        
        h3 { font-size: 24px; color: var(--accent-primary); margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
        
        p, li { font-size: 20px; line-height: 1.6; color: var(--text-muted); }
        .subtitle { font-size: 24px; font-weight: 300; margin-top: 1.5rem; max-width: 800px; }
        
        .mono-accent { font-family: 'JetBrains Mono', monospace; color: var(--accent-primary); }
        .text-gradient { background: linear-gradient(to right, var(--accent-primary), var(--accent-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        /* Animations */
        .animate-in { opacity: 0; transform: translateY(20px); }
        .active .animate-in { animation: fadeInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.2s; }
        .delay-3 { animation-delay: 0.3s; }
        .delay-4 { animation-delay: 0.4s; }

        @keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }

        /* Layout Utility Classes */
        .content-area { flex: 1; display: flex; flex-direction: column; justify-content: center; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; height: 100%; }
        .grid-tiled { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
        
        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            padding: 30px;
            border-radius: 16px;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); border-color: var(--accent-primary); background: rgba(255, 255, 255, 0.05); }

        .img-box {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }
        .img-box img { width: 100%; height: 100%; object-fit: cover; display: block; }

        /* Specific Components */
        .timeline { display: flex; justify-content: space-between; position: relative; margin-top: 40px; }
        .timeline::before { content: ''; position: absolute; top: 24px; left: 0; width: 100%; height: 2px; background: var(--glass-border); z-index: 0; }
        .timeline-item { position: relative; z-index: 1; text-align: center; flex: 1; }
        .dot { 
            width: 50px; height: 50px; background: rgba(3, 7, 18, 0.9); border: 2px solid var(--accent-primary); 
            border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;
            color: var(--accent-primary); font-family: 'Space Grotesk'; font-weight: 700;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }

        .stat-grid { display: flex; justify-content: space-around; gap: 40px; text-align: center; margin-top: 20px; }
        .stat-item .num { 
            font-size: 80px; font-weight: 700; font-family: 'Space Grotesk'; color: transparent;
            -webkit-text-stroke: 2px var(--accent-primary); line-height: 1; margin-bottom: 10px;
            position: relative;
        }
        .stat-item .num::after {
            content: attr(data-val); position: absolute; left: 0; top: 0; width: 100%;
            color: var(--accent-primary); opacity: 0.15; filter: blur(5px);
        }
        
        .table-container { 
            border: 1px solid var(--glass-border); border-radius: 12px; overflow: hidden; 
            background: rgba(255,255,255,0.02);
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 20px 30px; text-align: left; border-bottom: 1px solid var(--glass-border); }
        th { color: var(--accent-primary); font-weight: 600; text-transform: uppercase; font-size: 16px; letter-spacing: 1px; }
        tr:last-child td { border-bottom: none; }

        /* UI Controls */
        .progress-bar { position: fixed; bottom: 0; left: 0; width: 100%; height: 4px; background: rgba(255,255,255,0.1); z-index: 100; }
        .progress-fill { height: 100%; background: var(--accent-primary); width: 0%; transition: width 0.3s; box-shadow: 0 0 10px var(--accent-primary); }
        
        .controls { position: fixed; bottom: 30px; right: 30px; display: flex; gap: 15px; z-index: 100; }
        .btn-nav { 
            width: 48px; height: 48px; border-radius: 50%; background: rgba(255,255,255,0.05); 
            border: 1px solid var(--glass-border); color: var(--text-main); display: flex; 
            align-items: center; justify-content: center; cursor: pointer; transition: 0.2s;
            font-size: 18px; backdrop-filter: blur(10px);
        }
        .btn-nav:hover { background: var(--accent-primary); color: #000; border-color: var(--accent-primary); box-shadow: 0 0 20px rgba(6,182,212,0.4); }

        /* Helpers */
        .w-full { width: 100%; }
        .h-full { height: 100%; }
        .text-center { text-align: center; }
        .m-auto { margin: auto; }
        .pill { 
            display: inline-flex; align-items: center; gap: 8px; padding: 8px 20px; 
            border: 1px solid var(--accent-primary); border-radius: 50px; 
            color: var(--accent-primary); font-family: 'JetBrains Mono'; font-size: 14px; margin-top: 30px;
        }

        /* Responsive Mobile - Vertical Scroll */
        @media (max-width: 768px){
            body{overflow-y:auto!important;height:auto!important;display:block!important;padding:20px 0;background-attachment:scroll}#deck{width:100%!important;height:auto!important;max-width:none!important;max-height:none!important;aspect-ratio:auto!important;display:flex!important;flex-direction:column!important;gap:0;padding:0;align-items:center;overflow:hidden}.slide-container{position:relative!important;opacity:1!important;visibility:visible!important;transform:none!important;width:1280px!important;height:720px!important;flex-shrink:0;transform:scale(var(--scale,0.3))!important;transform-origin:top center!important;margin-bottom:calc(720px * var(--scale,0.3) - 720px + 20px)!important;left:auto!important;top:auto!important}.controls,.progress-bar{display:none!important}.active .animate-in{animation:none!important;opacity:1!important;transform:none!important}.animate-in{opacity:1!important;transform:none!important}
        }
    </style>
</head>
<body>
    <div id="deck">
        <!-- Slides go here -->
    </div>

    <!-- UI -->
    <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
    <div class="controls">
        <div class="btn-nav" onclick="prevSlide()"><i class="fa-solid fa-chevron-left"></i></div>
        <div class="btn-nav" onclick="nextSlide()"><i class="fa-solid fa-chevron-right"></i></div>
    </div>

    <script>
        // Scaling Logic
        function updateMobileScale() {
            if (window.innerWidth <= 1280) {
                const scale = Math.min((window.innerWidth - 40) / 1280, 1);
                document.documentElement.style.setProperty('--scale', scale);
            } else {
                document.documentElement.style.removeProperty('--scale');
            }
        }
        window.addEventListener('resize', updateMobileScale);
        updateMobileScale();

        // Navigation Logic
        let currentSlide = 1;
        const totalSlides = [TOTAL_SLIDES_COUNT];
        
        function updateUI() {
            document.querySelectorAll('.slide-container').forEach(s => s.classList.remove('active'));
            const active = document.getElementById('slide' + currentSlide);
            if(active) {
                active.classList.add('active');
                // Re-trigger animations
                active.querySelectorAll('.animate-in').forEach(el => {
                    el.style.animation = 'none';
                    el.offsetHeight; 
                    el.style.animation = '';
                });
            }
            document.getElementById('progressFill').style.width = ((currentSlide - 1) / (totalSlides - 1)) * 100 + '%';
        }
        
        function nextSlide() { if(currentSlide < totalSlides) { currentSlide++; updateUI(); } }
        function prevSlide() { if(currentSlide > 1) { currentSlide--; updateUI(); } }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === 'Space') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });
        
        updateUI();
    </script>
</body>
</html>
```

## Instruction
When generating slides:
1.  **Analyze Content**: Break down the user's topic into logical slides (approx 8-12 slides).
2.  **Select Layouts**: Choose the most appropriate visual layout for each point (e.g., Timeline for history, Tiles for features).
3.  **Refine Copy**: Use punchy, high-impact headings. Avoid walls of text. Use `span` with colors for emphasis.
4.  **Final Slide**: The last slide MUST use the specific "Q & A" layout with the author's contact info. Use the following HTML structure:
    ```html
    <div class="slide-container" id="slide[LAST_INDEX]">
        <div class="content-area" style="align-items: center; text-align: center;">
            <h2 class="animate-in" style="font-size: 60px; margin-bottom: 20px;">Q & A</h2>
            <p class="subtitle animate-in delay-1">Start building with /speckit today.</p>

            <div class="animate-in delay-2"
                style="margin-top: 60px; display: flex; flex-direction: column; gap: 20px; align-items: center;">
                <a href="mailto:yugasun.ai@gmail.com"
                    style="text-decoration: none; color: white; display: flex; align-items: center; gap: 10px; padding: 10px 20px; background: rgba(255,255,255,0.05); border-radius: 50px; border: 1px solid rgba(255,255,255,0.1); transition: all 0.2s;">
                    <i class="fa-solid fa-envelope" style="color: var(--accent-primary);"></i> yugasun.ai@gmail.com
                </a>
                <a href="https://github.com/yugasun" target="_blank"
                    style="text-decoration: none; color: white; display: flex; align-items: center; gap: 10px; padding: 10px 20px; background: rgba(255,255,255,0.05); border-radius: 50px; border: 1px solid rgba(255,255,255,0.1); transition: all 0.2s;">
                    <i class="fa-brands fa-github" style="color: var(--accent-secondary);"></i> github.com/yugasun
                </a>
            </div>
        </div>
    </div>
    ```
5.  **Code It**: Output the full HTML code.
