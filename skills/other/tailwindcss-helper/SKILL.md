---
name: tailwindcss-helper
description: Tailwind CSS 工具类参考和文档助手。提供 Tailwind CSS 文档的快速访问，用于查找工具类、理解 CSS 属性和查找代码示例。当 Claude 需要使用 Tailwind CSS 时使用此技能：（1）查找特定的工具类及其效果（2）理解如何在 Tailwind 中实现特定的 CSS 属性（3）查找布局、排版、颜色、间距等方面的代码示例和最佳实践（4）学习响应式设计模式、深色模式、悬停状态和其他变体
---

# Tailwind CSS Helper

## 何时使用此技能

当你需要以下情况时使用此技能：

- 查找特定的 Tailwind CSS 工具类
- 了解如何使用 Tailwind 实现 CSS 属性
- 查找代码示例和最佳实践
- 学习响应式设计、状态和变体
- 参考 Tailwind CSS 文档

## 如何使用

要查找 Tailwind CSS 文档：

1. **确定主题** - 确定你需要什么 CSS 属性或功能（例如：`flex-direction`、`font-weight`、`background-color`）
2. **找到相关文件** - 在 [文档目录索引] 中找到对应的参考文件
3. **阅读文档** - 每个文件包含：
   - 基本用法示例
   - 响应式变体
   - 自定义值选项
   - 状态变体（hover、focus、dark mode）
   - 最佳实践

## 必须先看文档

1. **确定需求** - 明确你需要什么组件或功能（例如：按钮、模态框、表单验证）
2. **查阅文档分类** - 在下方的「文档目录索引」中找到对应类别的文档
3. **定位具体文件** - 根据分类中的文件名，在 `references/` 目录中找到对应文档
4. **阅读文档内容** - 使用 `read` 工具查看完整文档，理解后再实现
5. **参考示例代码** - 文档中包含完整的 HTML/CSS/JavaScript 示例

## 文档目录索引

`references/` 目录包含 203 个涵盖所有 Tailwind CSS 功能的文档文件。

### ./references/docs-accent-color.md

- Apply Responsive Accent Color with Breakpoint Variant
- Use Custom Theme Color in Markup
- Customize Theme Colors with CSS Variables

### ./references/docs-adding-custom-styles.md

- Apply Arbitrary Values with Responsive Modifiers in Tailwind CSS HTML
- Use Simple Custom Utilities in HTML (HTML)
- Apply Arbitrary CSS Properties with Modifiers in Tailwind CSS HTML
- Combine Value Types with Multiple Arguments in CSS Utilities
- Use Simple Custom Utilities with Variants in HTML (HTML)
- Combine Value Types with Multiple Declarations in CSS Utilities
- Define Functional Custom Utilities with `@utility` and `--value()` (CSS)
- Define Simple Custom Utilities with `@utility` (CSS)
- Support Literal Utility Values in Tailwind CSS Utilities
- Define Custom Tailwind CSS Variants Using Shorthand Syntax
- Import Tailwind CSS and Add Custom Styles (CSS)
- Override Component Classes with Utility Classes (HTML)
- Define Complex Custom Utilities with Nesting (CSS)
- Support Fraction Values in CSS Utilities using `ratio` Data Type
- Apply Arbitrary Values for Direct Styling in Tailwind CSS HTML
- Support Negative Values in Tailwind CSS Utilities

### ./references/docs-align-content.md

- Align rows to the start of the cross axis using Tailwind CSS
- Apply responsive align-content utilities in Tailwind CSS
- Distribute rows with space between using Tailwind CSS
- Distribute rows with space around using Tailwind CSS
- Distribute rows with space evenly using Tailwind CSS
- Stretch rows to fill available space using Tailwind CSS
- Align rows to the end of the cross axis using Tailwind CSS
- Reset row alignment to normal using Tailwind CSS

### ./references/docs-align-items.md

- Apply responsive align-items utilities in Tailwind CSS HTML
- Align items to the cross-start with items-start in HTML
- Align items to the cross-end with items-end in HTML
- Apply items-stretch for cross-axis stretching in HTML
- Align items by text baseline with items-baseline in HTML

### ./references/docs-align-self.md

- Aligning Flex/Grid Item to Start of Cross Axis (self-start) in HTML
- Applying Responsive align-self Utilities in Tailwind CSS (HTML)

### ./references/docs-animation.md

- Responsive Animation with Breakpoint Variants
- Customize Animation Theme with CSS Variables
- Use Custom Themed Animation in Markup
- Custom Animation with Arbitrary Values
- Custom Animation with CSS Variables

### ./references/docs-appearance.md

- Apply Tailwind CSS `appearance` Utilities Responsively
- Remove Default Browser Styling with Tailwind CSS `appearance-none`

### ./references/docs-aspect-ratio.md

- Apply responsive aspect ratios using Tailwind CSS variants
- Use a custom aspect ratio utility defined in Tailwind CSS theme
- Define a custom aspect ratio utility in Tailwind CSS theme
- Set a custom aspect ratio with arbitrary values in Tailwind CSS
- Apply a custom aspect ratio using a CSS variable in Tailwind CSS
- Apply a specific aspect ratio to an element using Tailwind CSS
- Apply a 16:9 video aspect ratio to an iframe using Tailwind CSS

### ./references/docs-backdrop-filter.md

- Apply Basic Backdrop Filters with Tailwind CSS
- Remove Backdrop Filters with Tailwind CSS

### ./references/docs-backdrop-filter-brightness.md

- Apply Responsive Backdrop Brightness Filters in HTML with Tailwind CSS

### ./references/docs-backdrop-filter-contrast.md

- Apply responsive backdrop contrast with Tailwind CSS breakpoints
- Set custom backdrop contrast value with bracket notation

### ./references/docs-backdrop-filter-grayscale.md

- Apply responsive backdrop grayscale with Tailwind CSS
- Apply basic backdrop grayscale utilities in Tailwind CSS
- Set custom backdrop grayscale value with Tailwind CSS

### ./references/docs-backdrop-filter-invert.md

- Apply Basic Backdrop Invert Filters with Tailwind CSS
- Apply Backdrop Invert with CSS Variable in Tailwind CSS
- Apply Responsive Backdrop Invert Filters with Tailwind CSS

### ./references/docs-backdrop-filter-opacity.md

- Apply Responsive Backdrop Opacity with Tailwind CSS
- Apply Basic Backdrop Opacity Filters with Tailwind CSS

### ./references/docs-backdrop-filter-saturate.md

- Apply backdrop saturation with Tailwind CSS utilities
- Reference CSS custom properties for backdrop saturation

### ./references/docs-backdrop-filter-sepia.md

- Apply responsive backdrop sepia with breakpoint variants
- Apply backdrop sepia filter with Tailwind CSS utility classes
- Apply custom backdrop sepia value with arbitrary syntax

### ./references/docs-backface-visibility.md

- Apply Responsive backface-visibility Utility in HTML
- Apply backface-visibility Utilities in HTML

### ./references/docs-background-attachment.md

- Responsive background-attachment with breakpoint variants

### ./references/docs-background-blend-mode.md

- Responsive background blend mode with Tailwind CSS breakpoints

### ./references/docs-background-clip.md

- Apply responsive background-clip utilities in HTML (Tailwind CSS)
- Apply basic background-clip utilities in HTML (Tailwind CSS)
- Crop background to text shape in HTML (Tailwind CSS)

### ./references/docs-background-color.md

- Map Tailwind `bg-*` Classes to CSS Background Colors
- Apply Responsive Background Color using Tailwind CSS Breakpoint Variants

### ./references/docs-background-image.md

- Apply Responsive Gradient Utilities with Breakpoint Variants
- Create Conic Gradient Backgrounds with Tailwind CSS
- Create Radial Gradient Backgrounds with Tailwind CSS
- Create Linear Gradient Backgrounds with Tailwind CSS

### ./references/docs-background-origin.md

- Responsive background-origin with breakpoint variants

### ./references/docs-background-position.md

- Apply Tailwind CSS background-position utilities for basic positioning
- Apply background-position using CSS variables in Tailwind CSS
- Apply responsive background-position utilities in Tailwind CSS

### ./references/docs-background-repeat.md

- Responsive background-repeat with Tailwind CSS breakpoints

### ./references/docs-background-size.md

- Apply custom `background-size` value in Tailwind CSS
- Apply responsive `background-size` utilities in Tailwind CSS
- Apply `bg-cover` for background image fill in Tailwind CSS
- Apply custom CSS variable for `background-size` in Tailwind CSS
- Apply `bg-auto` for default background image size in Tailwind CSS
- Apply `bg-contain` for background image fill without cropping in Tailwind CSS

### ./references/docs-border-color.md

- Basic Border Color Example - HTML
- Apply Amber 400 Border Start Color with Tailwind CSS
- Apply Amber 600 Border Start Color with Tailwind CSS
- Apply Amber 500 Border Start Color with Tailwind CSS
- Apply Amber 300 Border Start Color with Tailwind CSS
- Apply Amber 200 Border Start Color with Tailwind CSS
- Apply Amber 100 Border Start Color with Tailwind CSS
- Apply Amber 50 Border Start Color with Tailwind CSS
- Apply Orange 950 Border Start Color with Tailwind CSS
- Apply Orange 400 Border Start Color with Tailwind CSS
- Apply Orange 700 Border Start Color with Tailwind CSS
- Apply Orange 600 Border Start Color with Tailwind CSS
- Apply Orange 900 Border Start Color with Tailwind CSS
- Apply Orange 800 Border Start Color with Tailwind CSS
- Apply Red 700 Border Start Color with Tailwind CSS
- Apply Orange 500 Border Start Color with Tailwind CSS
- Apply Orange 300 Border Start Color with Tailwind CSS
- Apply Red 900 Border Start Color with Tailwind CSS
- Apply Red 600 Border Start Color with Tailwind CSS
- Apply Red 950 Border Start Color with Tailwind CSS
- Apply Orange 100 Border Start Color with Tailwind CSS
- Apply Orange 200 Border Start Color with Tailwind CSS
- Apply Orange 50 Border Start Color with Tailwind CSS
- Apply Red 800 Border Start Color with Tailwind CSS
- Apply Red 500 Border Start Color with Tailwind CSS
- Apply Border Color on Focus State with Tailwind CSS
- Tailwind CSS Utilities for `border-inline-start-color`
- Apply Border Inline End Color with Tailwind CSS Utility Classes
- Set Border Block Color with Tailwind CSS Utilities
- Apply Border Inline Color with Tailwind CSS and CSS

### ./references/docs-border-radius.md

- Apply directional border radius (start) with Tailwind CSS

### ./references/docs-border-spacing.md

- Use CSS Custom Property for Border Spacing in HTML with Tailwind CSS
- Apply Basic Border Spacing to HTML Tables with Tailwind CSS
- Customize Tailwind CSS Spacing Theme Variable for Border Spacing
- Apply Responsive Border Spacing in HTML with Tailwind CSS

### ./references/docs-border-style.md

- Apply responsive border styles with breakpoint variants

### ./references/docs-border-width.md

- Apply responsive border width with breakpoint variants
- Set custom border width with bracket notation
- Add borders between child elements with divide utilities
- Logical property border-width utilities in Tailwind CSS
- Reverse divide direction for reversed flex layouts

### ./references/docs-box-decoration-break.md

- Responsive box-decoration-break with breakpoint variant
- Apply box-decoration-clone utility in HTML

### ./references/docs-box-shadow.md

- Apply Different Sized Box Shadows in HTML with Tailwind CSS
- Apply Responsive Box Shadows in Tailwind CSS
- Set Custom Box Shadow Colors in HTML with Tailwind CSS
- Apply Custom Box Shadow Values in Tailwind CSS
- Define Inset Ring Colors with Tailwind CSS Variables

### ./references/docs-box-sizing.md

- Apply responsive box-sizing with Tailwind CSS breakpoint variants
- Apply box-content utility in HTML with Tailwind CSS
- Apply box-border utility in HTML with Tailwind CSS

### ./references/docs-break-after.md

- break-after Basic Example with Columns
- break-after Responsive Design with Breakpoint Variant

### ./references/docs-break-before.md

- Control Column/Page Breaks with Tailwind CSS `break-before` Utilities
- Apply Responsive `break-before` Utilities in Tailwind CSS

### ./references/docs-break-inside.md

- Apply responsive break-inside utilities in HTML
- Apply break-inside utilities in HTML

### ./references/docs-caption-side.md

- Responsive caption-side with breakpoint variants

### ./references/docs-caret-color.md

- Apply Responsive Caret Colors with Tailwind CSS
- Set Custom Caret Color with Hex Value in Tailwind CSS

### ./references/docs-clear.md

- Apply Responsive Clears with Tailwind CSS Breakpoint Variants
- Disable Clears with Tailwind CSS `clear-none` Utility

### ./references/docs-color.md

- Apply predefined text color utilities in HTML
- Apply responsive text color with breakpoint variants in HTML

### ./references/docs-color-scheme.md

- Apply Tailwind CSS color scheme utilities conditionally in dark mode

### ./references/docs-colors.md

- Applying Tailwind CSS Color Utilities in a Notification Component (HTML)
- Using Arbitrary Opacity Values and CSS Variables with Tailwind CSS Colors (HTML)

### ./references/docs-columns.md

- Apply responsive column layouts with Tailwind CSS breakpoints
- Specify column gap with Tailwind CSS
- Use custom Tailwind CSS column utility in HTML
- Apply custom column width using arbitrary values in Tailwind CSS
- Customize Tailwind CSS column utilities in theme configuration
- Set ideal column width with Tailwind CSS
- Apply fixed number of columns with Tailwind CSS
- Apply custom column width using CSS variables in Tailwind CSS

### ./references/docs-compatibility.md

- Use CSS Variables in CSS Modules to Improve Tailwind Performance
- Apply color utilities with Tailwind hover states
- Reference Global Styles in CSS Modules for Tailwind @apply
- Reference Global Styles in Vue/Svelte/Astro Components for Tailwind @apply
- Bundle CSS imports with Tailwind
- Use native CSS variables in Tailwind
- Flatten nested CSS with Tailwind
- Use CSS Variables in Vue/Svelte/Astro Components for Better Tailwind Performance

### ./references/docs-content.md

- Set Content for Pseudo-elements with Tailwind CSS
- Apply Responsive Content Utilities with Tailwind CSS
- Control Tailwind CSS Content with CSS Variables

### ./references/docs-cursor.md

- Apply Responsive Cursor Styles with Tailwind CSS
- Apply Basic Cursor Styles with Tailwind CSS

### ./references/docs-dark-mode.md

- Activate Tailwind CSS Dark Mode Manually with HTML Class

### ./references/docs-detecting-classes-in-source-files.md

- Correct Prop Mapping for Static Class Names in JSX
- Advanced Prop Mapping for Varied Class Names in JSX
- Setting Tailwind's Base Path for Source Detection in CSS
- Safelist Utilities with Variants in Tailwind CSS
- Correct Dynamic Class Name Usage in HTML
- Safelist Utilities with Ranges in Tailwind CSS
- Explicitly Exclude Classes in Tailwind CSS
- Incorrect Dynamic Class Name Construction in HTML
- Example JSX Component with Tailwind Classes
- Incorrect Dynamic Class Name Construction with Props in JSX
- Registering Additional Tailwind Source Paths in CSS

### ./references/docs-display.md

- Create Inline Grid Containers with Tailwind CSS Inline-Grid Utility
- Create Block Formatting Contexts with Tailwind CSS Flow Root Utility
- Create Inline Flex Containers with Tailwind CSS Inline-Flex Utility
- Implement Tailwind CSS Table Layouts with Utility Classes
- Apply Responsive Display Utilities in Tailwind CSS
- Create Block-Level Flex Containers with Tailwind CSS Flex Utility
- Create Grid Containers with Tailwind CSS Grid Utility

### ./references/docs-editor-setup.md

- Sort Tailwind CSS Classes with Prettier Plugin (HTML)

### ./references/docs-field-sizing.md

- Apply responsive field sizing with Tailwind CSS
- Apply content-based field sizing with Tailwind CSS
- Apply fixed field sizing with Tailwind CSS

### ./references/docs-fill.md

- Apply Tailwind CSS fill-cyan-300 utility
- Customize Tailwind CSS Theme for Fill Colors
- Apply Responsive Fill Colors to SVG in Tailwind CSS

### ./references/docs-filter.md

- Apply responsive filter utilities with breakpoints
- Remove all filters with filter-none utility
- Apply filter utilities on hover state
- Apply custom CSS variable filters
- Apply blur and grayscale filters with Tailwind CSS
- Apply custom filter values with bracket notation

### ./references/docs-filter-blur.md

- Apply responsive blur filters in Tailwind CSS

### ./references/docs-filter-brightness.md

- Apply Brightness Filters with Tailwind CSS and CSS Variables
- Apply Basic Brightness Filters with Tailwind CSS
- Apply Responsive Brightness Filters with Tailwind CSS
- Apply Custom Brightness Filters with Tailwind CSS Arbitrary Values

### ./references/docs-filter-contrast.md

- Apply custom contrast value with bracket notation
- Apply responsive contrast filter with breakpoint variants
- Apply contrast filter using CSS custom properties
- Apply contrast filter with predefined Tailwind utilities

### ./references/docs-filter-drop-shadow.md

- Remove Drop Shadow with Tailwind CSS Utility
- Adjust Drop Shadow Opacity with Tailwind CSS Modifiers
- Set Drop Shadow Color with Tailwind CSS Color Utilities
- Apply Drop Shadow with Tailwind CSS Classes

### ./references/docs-filter-grayscale.md

- Apply Custom Grayscale Values and CSS Variables with Tailwind CSS
- Apply Basic Grayscale Filters to Images using Tailwind CSS

### ./references/docs-filter-hue-rotate.md

- Apply responsive hue-rotate utilities in HTML
- Apply custom hue-rotate values with bracket notation in HTML
- Apply negative hue-rotate values in HTML
- Apply hue-rotate filter with predefined values in HTML

### ./references/docs-filter-invert.md

- Apply Responsive Invert Filter with Tailwind CSS Breakpoints

### ./references/docs-filter-saturate.md

- Apply Basic Saturation Filters with Tailwind CSS
- Use CSS Variables for Saturation with Tailwind CSS
- Apply Responsive Saturation Filters with Tailwind CSS
- Apply Custom Saturation Values with Tailwind CSS

### ./references/docs-filter-sepia.md

- Apply responsive sepia filters to images with Tailwind CSS breakpoints
- Apply basic sepia filters to images with Tailwind CSS
- Apply custom sepia filter values using Tailwind CSS arbitrary values
- Apply sepia filter using CSS custom properties in Tailwind CSS

### ./references/docs-flex.md

- flex-initial Utility Example
- Basic flex-1 Utility Example
- flex-auto Utility Example
- flex-none Utility Example
- Custom flex Value with Bracket Notation
- Responsive flex Utility with Breakpoint Variant
- Custom flex Property with CSS Variable

### ./references/docs-flex-basis.md

- Apply flex-basis using percentage fractions in Tailwind CSS
- Apply flex-basis using spacing scale in Tailwind CSS
- Apply flex-basis using container scale in Tailwind CSS
- Apply responsive flex-basis utilities in Tailwind CSS
- Apply flex-basis with custom arbitrary values in Tailwind CSS
- Use custom container basis utility in Tailwind CSS
- Apply flex-basis with custom CSS variables in Tailwind CSS

### ./references/docs-flex-direction.md

- Apply responsive `flex-direction` with Tailwind CSS variants
- Apply `flex-col` for vertical flex items in Tailwind CSS
- Apply `flex-row` for horizontal flex items in Tailwind CSS
- Apply `flex-col-reverse` for reversed vertical flex items in Tailwind CSS
- Apply `flex-row-reverse` for reversed horizontal flex items in Tailwind CSS

### ./references/docs-flex-grow.md

- Applying Responsive Flex Grow Utilities with Tailwind CSS Breakpoints
- Setting Custom Flex Grow Values with Tailwind CSS `grow-[<value>]` Syntax
- Allowing Flex Items to Grow with Tailwind CSS `grow` Utility
- Proportionally Growing Flex Items with Tailwind CSS `grow-<number>` Utilities
- Applying CSS Variables for Flex Grow with Tailwind CSS `grow-(<custom-property>)`
- Preventing Flex Items from Growing with Tailwind CSS `grow-0` Utility

### ./references/docs-flex-shrink.md

- Applying Responsive Shrink Utilities with Tailwind CSS
- Using Custom Shrink Values with Tailwind CSS
- Using CSS Variables for Shrink Values in Tailwind CSS
- Allowing Flex Items to Shrink with Tailwind CSS

### ./references/docs-flex-wrap.md

- Apply Responsive Flex Wrap Utilities with Tailwind CSS

### ./references/docs-float.md

- Apply Logical Float Properties with Tailwind CSS
- Apply Responsive Float with Tailwind CSS Breakpoints

### ./references/docs-font-size.md

- Set font-size with line-height modifiers in HTML
- Define Custom Font Size Utility in Tailwind CSS Theme
- Apply responsive font-size utilities in HTML

### ./references/docs-font-smoothing.md

- Responsive font-smoothing with Tailwind CSS breakpoints

### ./references/docs-font-stretch.md

- Apply responsive font-stretch utilities in HTML with Tailwind CSS
- Apply percentage-based font-stretch in HTML with Tailwind CSS
- Apply basic font-stretch utilities in HTML with Tailwind CSS
- Apply CSS variable for font-stretch in HTML with Tailwind CSS
- Apply custom font-stretch values in HTML with Tailwind CSS

### ./references/docs-font-style.md

- Responsive font-style with Tailwind CSS breakpoints

### ./references/docs-font-variant-numeric.md

- Combine Multiple Numeric Font Variants with Tailwind CSS

### ./references/docs-font-weight.md

- Apply responsive font-weight with breakpoint variants

### ./references/docs-forced-color-adjust.md

- Restoring forced colors with Tailwind CSS
- Applying forced-color-adjust responsively with Tailwind CSS
- Opting out of forced colors with Tailwind CSS

### ./references/docs-functions-and-directives.md

- Load Legacy Tailwind CSS Plugin with @plugin Directive (CSS)
- Access Tailwind Theme Values with theme() Function (CSS)
- Generate spacing values with --spacing() function

### ./references/docs-gap.md

- Apply responsive gap in Tailwind CSS
- Apply custom gap value in Tailwind CSS
- Apply uniform gap in Tailwind CSS Grid
- Apply custom gap using CSS variable in Tailwind CSS

### ./references/docs-grid-auto-columns.md

- Apply responsive grid-auto-columns utilities in Tailwind CSS
- Apply basic grid-auto-columns utilities in Tailwind CSS
- Set custom grid-auto-columns value in Tailwind CSS
- Apply grid-auto-columns with CSS variables in Tailwind CSS

### ./references/docs-grid-auto-flow.md

- Basic grid-auto-flow Example - Tailwind HTML
- Responsive grid-auto-flow Design - Tailwind HTML

### ./references/docs-grid-auto-rows.md

- Implement responsive `grid-auto-rows` with Tailwind CSS breakpoints
- Apply basic `grid-auto-rows` utilities in Tailwind CSS

### ./references/docs-grid-column.md

- Control Grid Column Start/End with Tailwind CSS `col-start`/`col-end`
- Implement Responsive Grid Column Spanning with Tailwind CSS Breakpoints
- Span Columns with Tailwind CSS `col-span-<number>`

### ./references/docs-grid-row.md

- Starting and ending grid lines with row-start and row-end
- Spanning rows with row-span utilities
- Custom grid-row values with bracket notation
- CSS custom properties with row utilities

### ./references/docs-grid-template-columns.md

- Apply responsive grid column utilities with Tailwind CSS breakpoints
- Define grid columns with Tailwind CSS `grid-cols-<number>` utility
- Implement a subgrid using Tailwind CSS `grid-cols-subgrid`

### ./references/docs-grid-template-rows.md

- Apply Responsive Grid Row Utilities with Tailwind CSS
- Implement Subgrid with Tailwind CSS `grid-rows-subgrid`
- Specify Grid Rows with Tailwind CSS `grid-rows-<number>`
- Set Custom Grid Row Values with Tailwind CSS `grid-rows-[<value>]`
- Set Grid Rows with CSS Variables using Tailwind CSS `grid-rows-(<custom-property>)`

### ./references/docs-height.md

- Apply Responsive Height with Tailwind CSS Breakpoint Variants
- Set Both Width and Height with Tailwind CSS size-* Utilities
- Set Percentage-Based Height with Tailwind CSS h-full and h-<fraction> Utilities

### ./references/docs-hover-focus-and-other-states.md

- Apply Styles for Element Initial Render or Display Transition (Tailwind CSS HTML)
- Style Popovers in Open State
- Applying Tailwind CSS Arbitrary Variants with Space Selectors
- Conditional Styling for Print Media (Tailwind CSS HTML)
- Use Custom Data Variants in HTML
- Create visual effects with ::before pseudo-element
- Stacking Tailwind CSS Arbitrary and Built-in Variants
- Style Details Elements in Open State
- Style Elements Based on Data Attribute Existence
- Replace pseudo-elements with real HTML elements for simplicity
- Style ::before and ::after pseudo-elements
- Style Elements Based on Data Attribute Values
- Apply Styles Based on CSS Property Support Shorthand (Tailwind CSS HTML)
- Create Custom Data Attribute Variants
- Use Arbitrary ARIA Variants with Square Brackets
- Apply Container Queries with Tailwind CSS `@md` Variant
- Apply Directional Styles with RTL and LTR Variants
- Style Dialog Backdrops with Tailwind CSS `backdrop` Variant
- Using Tailwind CSS Arbitrary Variants for Custom Selectors
- Differentiate multiple peers with named peer variants
- Target Parent Elements with Group ARIA Variants
- Apply Tailwind CSS `odd` and `even` variants to table rows
- Style File Input Buttons with Tailwind CSS `file` Variant
- Create Custom ARIA Variants in Tailwind CSS
- Tailwind CSS Special State Variants
- Conditional Styling Based on Viewport Orientation (Tailwind CSS HTML)
- Style Active Text Selection with Tailwind CSS `selection` Variant
- Style element based on sibling state with peer variant
- Apply Tailwind CSS `disabled` and `invalid` variants to form inputs
- Create arbitrary peer variants with custom selectors
- Apply Tailwind CSS `group-has-*` variant for styling based on descendant state
- Style interactive states with hover, focus, and active variants
- Using Tailwind CSS Arbitrary Variants for At-Rules
- Apply Responsive Grid Layouts with Tailwind CSS Breakpoints
- Apply Styles Based on Pointing Device Accuracy (Tailwind CSS HTML)
- Tailwind CSS Container Query Variants

### ./references/docs-hyphens.md

- Responsive hyphens utility with breakpoint variant

### ./references/docs-index.md

- Create a new Vite project using npm
- Configure Tailwind CSS Vite plugin in vite.config.ts
- Basic HTML structure with Tailwind CSS classes

### ./references/docs-installation.md

- HTML Template with Tailwind CSS Utilities

### ./references/docs-installation-framework-guides-adonisjs.md

- Start Development Server
- Create AdonisJS Project
- Install Tailwind CSS and Vite Plugin
- Use Tailwind CSS in AdonisJS Edge Template
- Configure Tailwind CSS Vite Plugin
- Import Tailwind CSS and Configure Source Scanning

### ./references/docs-installation-framework-guides-angular.md

- Start Angular development server
- Create new Angular project using Angular CLI
- Install Tailwind CSS and PostCSS dependencies via npm
- Configure PostCSS to use Tailwind CSS plugin
- Apply Tailwind CSS utility classes in Angular component template

### ./references/docs-installation-framework-guides-astro.md

- Start Development Server
- Create Astro Project with npm
- Use Tailwind CSS Utility Classes in Astro Component
- Install Tailwind CSS and Vite Plugin
- Import Tailwind CSS in Global Stylesheet
- Configure Tailwind CSS Vite Plugin in Astro

### ./references/docs-installation-framework-guides-emberjs.md

- Create a new Ember.js project
- Import application CSS file into Ember.js main application file
- Apply Tailwind CSS classes in an Ember.js Handlebars template
- Install Tailwind CSS and PostCSS dependencies via npm
- Add Tailwind CSS PostCSS plugin configuration
- Enable PostCSS support in Ember CLI build configuration

### ./references/docs-installation-framework-guides-gatsby.md

- Start Gatsby Development Server
- Create Gatsby Project with CLI
- Import Tailwind CSS in Global Styles
- Use Tailwind Utility Classes in React Components
- Configure PostCSS Plugins
- Install Tailwind CSS and Dependencies
- Import Global CSS in Gatsby Browser
- Enable Gatsby PostCSS Plugin

### ./references/docs-installation-framework-guides-laravel-mix.md

- Start Laravel Mix build process with watch mode
- Install Tailwind CSS npm dependencies
- Use Tailwind CSS utility classes in Laravel Blade template
- Configure Tailwind CSS in Laravel Mix webpack.mix.js
- Import Tailwind CSS and configure content scanning

### ./references/docs-installation-framework-guides-laravel-vite.md

- Start Development Build Process
- Create New Laravel Project
- Install Tailwind CSS and Vite Plugin
- Configure Vite Plugin for Tailwind CSS

### ./references/docs-installation-framework-guides-meteor.md

- Start Meteor Development Server
- Create Meteor Project with CLI
- Use Tailwind Utility Classes in React Component
- Install Tailwind CSS and Dependencies via npm
- Configure PostCSS Plugins for Tailwind

### ./references/docs-installation-framework-guides-nextjs.md

- Create a New Next.js Project with TypeScript and ESLint
- Configure PostCSS for Tailwind CSS in Next.js
- Apply Tailwind CSS Classes in a Next.js React Component

### ./references/docs-installation-framework-guides-nuxt.md

- Create a new Nuxt.js project using npm
- Apply Tailwind CSS classes in a Vue component template
- Globally link main.css in nuxt.config.ts for Nuxt
- Configure Tailwind CSS Vite Plugin in nuxt.config.ts

### ./references/docs-installation-framework-guides-parcel.md

- Start Parcel development server
- Create Parcel project with npm
- Create HTML template with Tailwind CSS
- Install Tailwind CSS and PostCSS dependencies
- Configure PostCSS for Tailwind CSS

### ./references/docs-installation-framework-guides-phoenix.md

- Start Phoenix server with Tailwind CSS build
- Create a new Phoenix project
- Install Tailwind CSS standalone CLI
- Apply Tailwind CSS utility classes in Phoenix template
- Configure Tailwind CSS plugin in Phoenix
- Enable Tailwind CSS watcher in Phoenix development
- Update Phoenix deployment script for Tailwind CSS
- Add Tailwind plugin dependency in Phoenix
- Remove default CSS import from Phoenix JavaScript

### ./references/docs-installation-framework-guides-qwik.md

- Create a new Qwik project using npm
- Apply Tailwind CSS classes in a Qwik component
- Configure Tailwind CSS Vite plugin in vite.config.ts

### ./references/docs-installation-framework-guides-react-router.md

- Create a new React Router project using npx
- Configure Vite to use Tailwind CSS and React Router plugins

### ./references/docs-installation-framework-guides-rspack-react.md

- Example React Component Using Tailwind CSS Classes
- Create Rspack Project using npm CLI
- Install Tailwind CSS and PostCSS Dependencies
- Configure PostCSS to Use Tailwind CSS Plugin
- Configure Rspack to Use PostCSS Loader for CSS

### ./references/docs-installation-framework-guides-rspack-vue.md

- Use Tailwind Utility Classes in Vue Component

### ./references/docs-installation-framework-guides-ruby-on-rails.md

- Start Development Build Process
- Create New Rails Project
- Apply Tailwind Utility Classes in ERB Template
- Install Tailwind CSS Rails Gem

### ./references/docs-installation-framework-guides-solidjs.md

- Create new SolidJS project with Vite template
- Apply Tailwind CSS utility classes in SolidJS `App.jsx` component
- Configure Vite plugin for Tailwind CSS in SolidJS `vite.config.ts`

### ./references/docs-installation-framework-guides-sveltekit.md

- Create SvelteKit Project
- Use Tailwind CSS Utility Classes
- Import CSS in SvelteKit Layout
- Configure Tailwind CSS Vite Plugin

### ./references/docs-installation-framework-guides-symfony.md

- Create a new Symfony web application project
- Install Webpack Encore for asset management in Symfony
- Integrate compiled CSS and use Tailwind classes in Twig template
- Configure PostCSS plugins with Tailwind CSS in postcss.config.mjs
- Enable PostCSS Loader in webpack.config.js for Symfony Encore
- Import Tailwind CSS and configure source in app.css

### ./references/docs-installation-framework-guides-tanstack-start.md

- Create TanStack Start Project
- Link CSS File in Root Route
- Configure Vite Plugin for Tailwind CSS
- Use Tailwind CSS Utility Classes in Components

### ./references/docs-installation-play-cdn.md

- Add Play CDN Script to HTML
- Configure Custom Tailwind CSS Theme with Play CDN

### ./references/docs-installation-tailwind-cli.md

- Include compiled Tailwind CSS in HTML and use utility classes
- Install Tailwind CSS and CLI via npm
- Run Tailwind CLI to build CSS with watch mode

### ./references/docs-installation-using-postcss.md

- Basic HTML structure with Tailwind CSS styling
- Configure Tailwind CSS PostCSS plugin in JavaScript

### ./references/docs-installation-using-vite.md

- Create Vite Project with npm
- Use Tailwind CSS Utility Classes in HTML
- Configure Tailwind CSS Vite Plugin

### ./references/docs-isolation.md

- Apply responsive isolation utility with breakpoint variant
- Apply isolation utility to create stacking context

### ./references/docs-justify-content.md

- Align items to start of main axis with Tailwind CSS `justify-start`
- Distribute items with space between using Tailwind CSS `justify-between`
- Apply responsive justify-content with Tailwind CSS breakpoint variants
- Align items to end of main axis with Tailwind CSS `justify-end` and `justify-end-safe`
- Distribute items with space around using Tailwind CSS `justify-around`
- Stretch items to fill space with Tailwind CSS `justify-stretch`
- Distribute items with space evenly using Tailwind CSS `justify-evenly`
- Reset justify-content to normal with Tailwind CSS `justify-normal`
- Center items along main axis with Tailwind CSS `justify-center` and `justify-center-safe`

### ./references/docs-justify-items.md

- Apply justify-items-end and justify-items-end-safe to grid items in HTML
- Apply justify-items-center and justify-items-center-safe to grid items in HTML
- Apply responsive justify-items utilities in HTML
- Apply justify-items-start to grid items in HTML

### ./references/docs-justify-self.md

- justify-self with responsive breakpoints
- justify-self-start - Align grid item to inline start
- justify-self-center - Center grid item on inline axis
- justify-self-end - Align grid item to inline end

### ./references/docs-line-clamp.md

- Responsive line-clamp with breakpoint variants
- Undo line clamping with line-clamp-none
- Basic line-clamp HTML example
- Custom line-clamp value with bracket notation
- Custom line-clamp with CSS custom property

### ./references/docs-line-height.md

- Custom line-height values with bracket notation in Tailwind CSS
- Responsive line-height with breakpoint variants in Tailwind CSS
- Combined font-size and line-height with Tailwind CSS
- Independent line-height with leading utilities in Tailwind CSS

### ./references/docs-list-style-image.md

- Apply responsive marker image with breakpoint variant

### ./references/docs-list-style-position.md

- Applying responsive list-style-position utilities in HTML
- Applying list-style-position utilities in HTML

### ./references/docs-list-style-type.md

- Apply responsive list-style-type utilities with breakpoint variants

### ./references/docs-margin.md

- Responsive Margin Utility HTML Example
- Logical Properties Margin Utilities HTML Example
- Space Reverse Direction Utility HTML Example
- Custom CSS Property Margin HTML Example
- Basic Margin Utility HTML Example
- Vertical Margin Utility HTML Example
- Horizontal Margin Utility HTML Example
- Custom Margin Value HTML Example
- Space Between Children Utility HTML Example
- Directional Margin Utilities HTML Example
- Negative Margin Utility HTML Example
- Space Y Arbitrary Value Margin CSS Implementation
- Space X Reverse Direction CSS Implementation
- Space Y Custom Property Margin CSS Implementation

### ./references/docs-mask-clip.md

- Apply responsive mask-clip utilities with breakpoint variants

### ./references/docs-mask-composite.md

- Apply responsive mask-composite utilities in HTML with Tailwind CSS

### ./references/docs-mask-image.md

- Add Radial Mask with Gradient and Position in Tailwind CSS
- Customize Conic Gradient Mask Start Color
- Remove Mask Image with Tailwind CSS `mask-none` Utility
- Apply Image Mask with Tailwind CSS
- Bottom Mask Gradient From Utilities - Tailwind CSS
- Use Custom Theme Color in Tailwind CSS Mask Utility
- Mask Radial From Gradient - Tailwind CSS
- Left Mask Gradient From Utilities - Tailwind CSS
- Apply Custom CSS Variable for Linear Mask in Tailwind CSS
- Mask X-Axis From Gradient - Tailwind CSS
- Set Radial Gradient Position with Tailwind CSS Utilities

### ./references/docs-mask-mode.md

- Apply basic mask-mode utilities in HTML
- Apply responsive mask-mode utilities in HTML

### ./references/docs-mask-origin.md

- Apply responsive mask-origin with breakpoint variants

### ./references/docs-mask-position.md

- Apply responsive Tailwind CSS mask-position utilities
- Apply Tailwind CSS mask-position utilities for basic positioning
- Set Tailwind CSS mask-position with custom arbitrary values

### ./references/docs-mask-size.md

- Apply responsive mask-size utilities in HTML
- Apply mask-cover utility in HTML
- Apply mask-auto utility in HTML
- Apply custom mask-size value in HTML
- Apply mask-contain utility in HTML

### ./references/docs-max-height.md

- Set Percentage-Based Maximum Height with Tailwind CSS
- Apply Custom CSS Variable Maximum Height with Tailwind CSS
- Implement Responsive Maximum Height with Tailwind CSS

### ./references/docs-max-width.md

- Container utility with responsive breakpoints in HTML
- Basic max-width with spacing scale in HTML
- Custom max-width values with bracket notation in HTML
- Percentage-based max-width with fractions in HTML
- Responsive max-width with breakpoint variants in HTML
- Custom max-width with CSS variables in HTML

### ./references/docs-min-height.md

- Apply responsive min-height utilities in HTML
- Apply min-height with percentage-based utilities in HTML
- Apply min-height with custom arbitrary values in HTML
- Apply min-height with custom CSS properties in HTML
- Apply min-height with spacing scale utilities in HTML

### ./references/docs-min-width.md

- Apply Percentage-Based Minimum Width with Tailwind CSS `min-w-<fraction>` Utilities
- Apply Custom CSS Variable for Minimum Width with Tailwind CSS
- Set Fixed Minimum Width with Tailwind CSS `min-w-<number>` Utilities
- Set Minimum Width with Tailwind CSS Container Scale Utilities
- Apply Responsive Minimum Width with Tailwind CSS Breakpoint Variants
- Apply Custom Minimum Width with Tailwind CSS `min-w-[<value>]` Syntax

### ./references/docs-mix-blend-mode.md

- Apply responsive mix-blend-mode utilities in Tailwind CSS
- Apply basic mix-blend-mode utilities in Tailwind CSS
- Isolate mix-blend-mode effects in Tailwind CSS

### ./references/docs-object-fit.md

- Applying responsive `object-fit` utilities with Tailwind CSS
- Resizing to cover using Tailwind CSS `object-cover`
- Stretching content to fit container using Tailwind CSS `object-fill`
- Scaling down content with Tailwind CSS `object-scale-down`
- Displaying content at original size using Tailwind CSS `object-none`
- Containing content within its container using Tailwind CSS `object-contain`

### ./references/docs-object-position.md

- Apply object-position utilities in HTML with Tailwind CSS
- Set object-position using CSS variable in HTML with Tailwind CSS
- Apply responsive object-position in HTML with Tailwind CSS

### ./references/docs-opacity.md

- Apply Tailwind CSS Opacity Responsively with Breakpoint Variants
- Set Tailwind CSS Opacity with Custom CSS Variables
- Apply Tailwind CSS Opacity Conditionally with Variants
- Set Tailwind CSS Opacity with Custom Numeric Values
- Apply Tailwind CSS Opacity Utilities for Basic Elements

### ./references/docs-order.md

- Explicitly setting sort order with numeric classes
- Responsive order utility with breakpoint variants
- Ordering items first or last with utility classes
- Using custom arbitrary values for order
- Using CSS custom properties with order utility
- Using negative order values

### ./references/docs-outline-offset.md

- Apply Responsive Outline Offset in Tailwind CSS
- Apply Outline Offset using CSS Variables in Tailwind CSS
- Set Custom Outline Offset Values in Tailwind CSS

### ./references/docs-outline-style.md

- Apply outline styles to buttons with Tailwind CSS
- Responsive outline-style with breakpoint variant in Tailwind CSS

### ./references/docs-outline-width.md

- Custom outline-width value with bracket notation in HTML
- Basic outline-width utilities in HTML

### ./references/docs-overflow.md

- Applying Responsive Overflow Utilities with Tailwind CSS

### ./references/docs-overflow-wrap.md

- Apply responsive `overflow-wrap` utilities in HTML with Tailwind CSS

### ./references/docs-padding.md

- Basic Padding Utility - Tailwind CSS
- Responsive Padding Design - Tailwind CSS
- Logical Padding Properties - Tailwind CSS

### ./references/docs-perspective.md

- Responsive Perspective Design with Breakpoint Variants
- Basic Perspective Transform with Tailwind CSS
- Use Custom Perspective Theme Utility in Markup
- Custom Perspective with CSS Variables
- Custom Perspective Value with Arbitrary Values

### ./references/docs-perspective-origin.md

- Apply responsive perspective-origin utilities in Tailwind CSS
- Apply Tailwind CSS perspective-origin utilities for basic positioning

### ./references/docs-place-content.md

- place-content-start - Align Grid Content to Start
- place-content with Responsive Breakpoints - Tailwind CSS

### ./references/docs-place-items.md

- Apply place-items-start utility in Tailwind CSS
- Apply responsive place-items utilities in Tailwind CSS
- Apply place-items-stretch utility in Tailwind CSS
- Apply place-items-center utility in Tailwind CSS
- Apply place-items-end utility in Tailwind CSS

### ./references/docs-place-self.md

- place-self-start - Align item to start on both axes

### ./references/docs-pointer-events.md

- Controlling pointer events for elements in HTML with Tailwind CSS
- Conditionally restoring pointer events in HTML with Tailwind CSS

### ./references/docs-position.md

- Apply Absolute Positioning in Tailwind CSS
- Apply Fixed Positioning in Tailwind CSS
- Apply Responsive Positioning in Tailwind CSS

### ./references/docs-preflight.md

- Styling Unstyled Lists with Tailwind CSS Utilities
- Overriding Block Display for Images with Tailwind CSS Utility
- Overriding Image Width Constraint with Tailwind CSS Utility
- Resetting Default Margins and Padding with Preflight CSS
- Apply source() Modifier to Tailwind CSS Utilities Import (CSS)
- Apply prefix(tw) Modifier to Tailwind CSS Theme and Utilities Imports (CSS)
- Overriding Preflight Border Reset for Third-Party Libraries in CSS
- Unstyling Default List Elements with Preflight CSS
- Constraining Images and Videos to Parent Width with Preflight CSS

### ./references/docs-resize.md

- Responsive resize utilities with Tailwind CSS breakpoints

### ./references/docs-responsive-design.md

- Apply Responsive Utility Variants with Breakpoint Prefixes
- Build Responsive Marketing Component with Tailwind CSS
- Apply Tailwind CSS utilities at a single breakpoint
- Implement basic Tailwind CSS container queries
- Correct Mobile-First Responsive Styling Pattern
- Apply custom Tailwind CSS breakpoints in HTML
- Remove all default Tailwind CSS breakpoints and define custom ones
- Target specific ranges with Tailwind CSS container queries
- Incorrect Mobile-First Responsive Styling Pattern
- Apply Arbitrary Container Query Values in HTML

### ./references/docs-rotate.md

- Apply 3D Rotations with Tailwind CSS
- Apply Basic 2D Rotations with Tailwind CSS
- Apply Responsive Rotations with Tailwind CSS
- Apply Custom Rotation with CSS Variables in Tailwind CSS
- Apply Custom Rotation Values with Tailwind CSS
- Apply Negative 2D Rotations with Tailwind CSS

### ./references/docs-scale.md

- Apply Negative Scale Transforms with Tailwind CSS
- Apply Basic Scale Transforms with Tailwind CSS
- Apply Custom Scale Values with Tailwind CSS

### ./references/docs-scroll-margin.md

- Apply Responsive Scroll Margin with Breakpoint Variants
- Apply Basic Scroll Margin in HTML with Tailwind CSS
- Apply Logical Scroll Margin Properties in HTML with Tailwind CSS
- Apply Negative Scroll Margin in HTML with Tailwind CSS

### ./references/docs-scroll-padding.md

- Using logical scroll-padding properties in HTML
- Basic scroll-padding with directional utilities in HTML
- Apply scroll-padding with responsive breakpoint variant in Tailwind CSS
- Custom scroll-padding values in HTML
- Negative scroll-padding values in HTML

### ./references/docs-scroll-snap-align.md

- Snap Start Alignment with Tailwind CSS
- Responsive Scroll Snap Alignment with Tailwind CSS
- Snap Center Alignment with Tailwind CSS
- Snap End Alignment with Tailwind CSS

### ./references/docs-scroll-snap-stop.md

- Apply `snap-normal` for skipping scroll snap stops in Tailwind CSS
- Apply `snap-always` for forced scroll snap stops in Tailwind CSS

### ./references/docs-scroll-snap-type.md

- Responsive scroll-snap-type with breakpoint variant

### ./references/docs-skew.md

- Responsive skew transform with breakpoint variants
- Basic skew transform on both axes

### ./references/docs-stroke.md

- Use Custom Theme Stroke Color in Tailwind CSS Markup
- Apply Neutral Stroke Colors in Tailwind CSS
- Apply Custom CSS Variable Stroke Color to SVG in Tailwind CSS
- Set SVG Stroke Color to Current Text Color with Tailwind CSS

### ./references/docs-stroke-width.md

- Apply Responsive Stroke Width with Tailwind CSS Breakpoints

### ./references/docs-styling-with-utility-classes.md

- Creating a responsive profile card with Tailwind CSS
- Complex Arbitrary Grid Values in Tailwind CSS
- Generated CSS for Tailwind CSS Arbitrary Variants
- Apply responsive styles with Tailwind breakpoint prefixes
- Example React Component Using Tailwind CSS Classes (JSX)
- Apply Multiple Tailwind CSS Variants for Complex Styling (HTML)
- Generated CSS for Multiple Tailwind CSS Variants
- CSS stylesheet demonstrating utility class conflict resolution
- Generated CSS for Tailwind CSS `group-hover` Variant
- Define Custom Grid Columns with Tailwind CSS Arbitrary Values (HTML)
- Styling a basic card component with Tailwind CSS
- Repeated Avatar List with Utility Classes in HTML
- Tailwind important modifier for forcing utility class precedence
- Multi-cursor editing for duplicated Tailwind classes in HTML
- Custom CSS button component with Tailwind theme variables
- Dynamic Button Styling with Inline Styles in React
- Apply Arbitrary Background Color with Tailwind CSS (HTML)
- Avatar List with Loop to Eliminate Duplication in Svelte
- Use CSS `calc()` with Tailwind CSS Arbitrary Values (HTML)
- CSS Variables with Dynamic Values and Tailwind Utilities
- React conditional styling to avoid conflicting Tailwind classes
- Prefix all Tailwind CSS classes and variables (CSS)
- Stack multiple Tailwind variants for combined conditions
- Set Custom CSS Variables with Tailwind CSS Arbitrary Values (HTML)
- React component with Tailwind CSS for reusable card styling

### ./references/docs-table-layout.md

- Apply automatic table column sizing with Tailwind CSS `table-auto`
- Apply responsive table layout with Tailwind CSS breakpoints
- Apply fixed table column widths with Tailwind CSS `table-fixed`

### ./references/docs-text-align.md

- Logical text alignment with text-start and text-end utilities
- Responsive text alignment with breakpoint variants

### ./references/docs-text-decoration-color.md

- Implement Responsive Text Decoration Colors with Tailwind CSS
- Apply Basic Text Decoration Colors with Tailwind CSS
- Apply Text Decoration Color on Hover State with Tailwind CSS
- Utilize Custom Theme Color for Text Decoration in Tailwind CSS
- Set Custom Hex Text Decoration Color in Tailwind CSS

### ./references/docs-text-decoration-style.md

- Apply Basic Text Decoration Styles with Tailwind CSS
- Apply Responsive Text Decoration Styles with Tailwind CSS

### ./references/docs-text-decoration-thickness.md

- Apply Numeric Text Decoration Thickness with Tailwind CSS
- Apply CSS Variable for Text Decoration Thickness in Tailwind CSS
- Apply Responsive Text Decoration Thickness with Tailwind CSS

### ./references/docs-text-indent.md

- Apply responsive text indentation with breakpoint variants
- Apply custom text indentation values with bracket notation
- Apply text indentation with indent utility classes
- Apply custom text indentation with CSS variables

### ./references/docs-text-overflow.md

- Responsive text-overflow with breakpoint variants - HTML

### ./references/docs-text-shadow.md

- Apply Text Shadow Color Utilities - Tailwind CSS HTML
- Apply Custom Text Shadow Utility in Markup
- Apply Responsive Text Shadow with Breakpoint Variant

### ./references/docs-text-transform.md

- Responsive text-transform with Tailwind CSS breakpoints

### ./references/docs-text-underline-offset.md

- Apply Responsive Underline Offset in Tailwind CSS
- Apply Basic Underline Offset in Tailwind CSS
- Apply Custom Underline Offset Value in Tailwind CSS
- Apply Underline Offset with CSS Variable in Tailwind CSS

### ./references/docs-text-wrap.md

- Implementing responsive text wrapping with Tailwind CSS
- Balancing text wrapping with Tailwind CSS `text-balance`
- Allowing text to wrap with Tailwind CSS `text-wrap`

### ./references/docs-theme.md

- Override default theme variable value
- Define Breakpoint Theme Variable
- Share Theme Variables Across Projects in Tailwind CSS
- Utilize Tailwind CSS Theme Variables in HTML Arbitrary Values
- Retrieve Resolved Tailwind CSS Theme Variable Values in JavaScript

### ./references/docs-top-right-bottom-left.md

- Tailwind CSS `start` Utilities for Inline Start Placement
- Apply Responsive Positioning with Breakpoint Variants in Tailwind CSS
- Use Logical Properties for Directional Positioning in Tailwind CSS
- Tailwind CSS `inset` Utilities for All Sides
- Set Custom Position Values in Tailwind CSS
- Position Elements with Top, Right, Bottom, Left Utilities in Tailwind CSS

### ./references/docs-touch-action.md

- Responsive touch-action with Breakpoint Variants HTML
- Basic touch-action Utilities HTML

### ./references/docs-transform.md

- Apply Hardware Accelerated Transforms with Tailwind CSS

### ./references/docs-transform-origin.md

- Apply Responsive Transform Origin in Tailwind CSS
- Apply Transform Origin with CSS Variable in Tailwind CSS

### ./references/docs-transform-style.md

- Responsive transform-style with breakpoint variant
- transform-3d and transform-flat HTML classes

### ./references/docs-transition-behavior.md

- Responsive transition-behavior with Breakpoint Variant
- Basic transition-behavior HTML Example

### ./references/docs-transition-delay.md

- transition-delay with motion-reduce variant
- transition-delay with custom CSS property
- transition-delay with custom arbitrary value
- transition-delay with responsive breakpoint variant
- Basic transition-delay HTML markup with Tailwind classes

### ./references/docs-transition-duration.md

- Apply predefined transition durations with Tailwind CSS
- Apply responsive transition durations with Tailwind CSS breakpoints
- Set custom transition duration values with Tailwind CSS arbitrary values

### ./references/docs-transition-property.md

- Custom transition-property with bracket notation
- Responsive transition-property with breakpoint variant

### ./references/docs-transition-timing-function.md

- Apply responsive transition timing functions with Tailwind CSS
- Use custom theme transition timing function utility in HTML
- Set custom transition timing function values in Tailwind CSS
- Apply custom CSS variable for transition timing function in Tailwind CSS
- Apply basic transition timing functions with Tailwind CSS
- Customize Tailwind CSS transition timing function theme variables

### ./references/docs-translate.md

- Apply 2D Translation with Percentage Values in Tailwind CSS
- Apply Y-axis Translation in Tailwind CSS
- Apply X-axis Translation in Tailwind CSS
- Apply 2D Translation with Spacing Scale in Tailwind CSS
- Apply Responsive Translation with Tailwind CSS Breakpoint Variants

### ./references/docs-upgrade-guide.md

- Update Tailwind CLI Commands for v4 Package
- Configure PostCSS for Tailwind CSS v4 Migration
- Apply Prefixed Tailwind CSS Classes in HTML
- Apply Important Modifier in Tailwind CSS v4.0 HTML
- Customize Tailwind CSS v4 `container` utility with `@utility` directive
- Retrieve Resolved CSS Variable Value in JavaScript
- Define Custom Component Utilities with Tailwind CSS v4.0 `@utility` API
- Update Tailwind CSS v3 `ring` utility to `ring-3` in v4
- Animate with Tailwind CSS Variables in React using Motion
- Update Tailwind CSS v3 shadow, radius, and blur scales to v4
- Tailwind CSS v4 `space-x/y` selector change and `gap` migration
- Tailwind CSS v4 gradient variant behavior and `via-none` usage
- Handle Outline-Color Transitions - HTML
- Update Grid and Object-Position Arbitrary Values - HTML
- Update Transform Transitions - HTML
- Upgrade Tailwind CSS Project using `npx @tailwindcss/upgrade`
- Reset Individual Transform Properties - HTML
- Update CSS Variables in Arbitrary Values - HTML
- Update Variant Stacking Order - HTML
- Use CSS Variables Instead of theme() Function - CSS
- Hover Variant Device Detection - CSS
- Restore Tailwind CSS v3 Dialog Margins in Preflight
- Integrate Tailwind CSS v4 with Vite using Dedicated Plugin
- Import Tailwind CSS Definitions with @reference in Vue/Svelte
- Apply Tailwind CSS Theme Variables Directly in Vue/Svelte
- Configure Tailwind CSS Theme Variables with Prefix
- Define Custom Utilities with Tailwind CSS v4.0 `@utility` API
- Preserve Tailwind CSS v3 Placeholder Color in Preflight
- Migrate Tailwind CSS v3 `outline` and `outline-none` utilities to v4
- Understand Generated CSS Variables with Tailwind CSS Prefix
- Update Tailwind CSS Ring Utility for v4.0
- Restore Tailwind CSS v3 Button Cursor Behavior in Preflight
- Preserve Tailwind CSS v3 Ring Behavior with CSS Theme Variables
- Replace `@tailwind` Directives with `@import` in CSS for v4
- Tailwind CSS v4 `divide-x/y` utility selector change
- Manage Tailwind CSS v4 default border color for `border` and `divide` utilities

### ./references/docs-user-select.md

- Responsive user-select with breakpoint variants

### ./references/docs-visibility.md

- Apply Responsive Visibility with Tailwind CSS Breakpoints
- Collapse Table Row with Tailwind CSS `collapse` Utility

### ./references/docs-white-space.md

- Use responsive white-space utility with breakpoint prefix
- Apply whitespace-pre utility in HTML
- Apply whitespace-pre-line utility in HTML
- Apply whitespace-pre-wrap utility in HTML

### ./references/docs-width.md

- Apply Percentage-Based Widths with Tailwind CSS `w-<fraction>` Utilities
- Set Widths Based on Container Scale with Tailwind CSS Utilities
- Match Viewport Width with Tailwind CSS `w-screen` Utility
- Set Fixed Width with Tailwind CSS `w-<number>` Utilities
- Reset Element Width Conditionally with Tailwind CSS `w-auto`
- Apply Responsive Width Utilities in Tailwind CSS

### ./references/docs-word-break.md

- Apply responsive word breaking with Tailwind CSS

### ./references/docs-z-index.md

- Responsive z-index with Tailwind CSS breakpoints
