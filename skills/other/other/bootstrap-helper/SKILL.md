---
name: bootstrap-helper
description: Bootstrap Web 前端框架参考文档助手。在需要使用 Bootstrap 5.3 时自动触发：(1) 查找组件、工具类和布局，(2) 学习 Bootstrap 组件的正确用法和最佳实践，(3) 实现响应式设计、表单验证、模态框等交互，(4) 定制主题、颜色模式和配置，(5) 解决 Bootstrap 集成和兼容性问题。
---

# Bootstrap Helper

## 什么时候用
- 要使用 Bootstrap 5.3 构建 Web 前端 UI 或布局
- 需要查找特定组件（如 modal、navbar、card 等）的用法
- 实现表单、导航、下拉菜单等交互功能
- 定制 Bootstrap 主题、颜色或响应式断点
- 排查 Bootstrap 与其他库的集成问题

## 必须先看文档
1. **确定需求** - 明确你需要什么组件或功能（例如：按钮、模态框、表单验证）
2. **查阅文档分类** - 在下方的「文档目录索引」中找到对应类别的文档
3. **定位具体文件** - 根据分类中的文件名，在 `references/` 目录中找到对应文档
4. **阅读文档内容** - 使用 `read` 工具查看完整文档，理解后再实现
5. **参考示例代码** - 文档中包含完整的 HTML/CSS/JavaScript 示例

## Bootstrap 简介

Bootstrap 是最流行的 Web 前端开发框架，用于快速构建响应式、移动设备优先的网站和应用。它包含：

- **预构建组件** - 按钮、导航栏、卡片、模态框等
- **响应式网格系统** - 灵活的 12 列布局
- **强大的插件** - JavaScript 交互组件
- **样式和工具类** - 丰富的 CSS 样式和实用工具

## 文档分类速查

### 示例 1：使用 Modal 组件
1. 在「文档目录索引」里找到 `docs-5.3-components-modal.md`
2. 使用 `read` 工具阅读该文档
3. 理解 HTML 结构和 data 属性配置
4. 查看初始化代码和可用方法
5. 根据示例代码实现并修改内容和样式

### 示例 2：构建响应式导航栏
1. 在「文档目录索引」里找到 `docs-5.3-components-navbar.md`
2. 使用 `read` 工具阅读该文档
3. 理解不同响应式变体的实现方式
4. 如需网格布局，查阅 `docs-5.3-layout-grid.md`
5. 根据示例代码添加下拉菜单和折叠功能
6. 测试移动端和桌面端显示效果

## 文档目录索引

### ./references/docs-5.3-components-accordion.md

- JavaScript Initialization
- Collapse Methods
- Bootstrap Collapse Plugin Usage with Data Attributes
- Collapse Options
- Collapse Events

### ./references/docs-5.3-components-alerts.md

- Initialize Bootstrap Alerts with JavaScript
- HTML for Live Bootstrap Alert Demo
- Bootstrap Alerts with Multiple Icons using SVG Sprite (HTML)
- Bootstrap Alert with Single Icon (HTML)
- Display Bootstrap Alerts in HTML

### ./references/docs-5.3-components-badge.md

- Positioned Bootstrap Badges (HTML)
- Bootstrap Badge Background Colors (HTML)

### ./references/docs-5.3-components-breadcrumb.md

- Bootstrap Breadcrumb Examples (HTML)
- Customizing Breadcrumb Dividers with CSS and Sass (HTML & Sass)

### ./references/docs-5.3-components-button-group.md

- Button Group with Links (HTML)
- Create Button Toolbars with Bootstrap
- Integrate Input Groups with Button Toolbars in Bootstrap
- Radio Button Group (HTML)
- Vertical Radio Button Group HTML

### ./references/docs-5.3-components-buttons.md

- Toggle Button States
- Bootstrap Button JavaScript Methods
- Bootstrap Button Sizes
- Toggle Button States with HTML
- Custom Bootstrap Button Variant (SCSS)
- Responsive Block Buttons
- Bootstrap Button Tags and Roles
- Create Stacked Block Buttons

### ./references/docs-5.3-components-card.md

- Bootstrap Card Styling Examples
- Basic Card Example with Image and Body (HTML)
- Bootstrap Card with Header and Body (HTML)
- Bootstrap Card with Blockquote (HTML)
- Bootstrap Card Basic Structure
- Bootstrap Card Header/Footer Styling
- Bootstrap Cards within Grid Columns (HTML)
- Bootstrap Card with Image, List, and Links (HTML)
- Bootstrap Card Text Alignment
- Bootstrap Card with Text Background Colors (HTML)
- Basic Bootstrap Card Layouts
- Card with Image and Text (HTML)
- Bootstrap Card with Image Overlay
- Bootstrap Card Background and Color Styles
- Card with Title, Subtitle, Text, and Links (HTML)
- Bootstrap Basic Card Layout
- Bootstrap Card with Tabbed Navigation
- Bootstrap Grid Cards Layout (HTML)
- Bootstrap Card with Footer Layout
- Card with Flush List Group and Footer (HTML)

### ./references/docs-5.3-components-carousel.md

- Bootstrap Carousel with Indicators HTML
- Bootstrap Carousel Basic Example HTML
- Bootstrap Carousel with Captions Example
- Initialize Bootstrap Carousel with Options
- Bootstrap Carousel: Autoplay on Page Load (HTML)
- Bootstrap Carousel with Crossfade Transition Example
- Bootstrap Carousel: Slides Only Autoplay (HTML)
- Bootstrap Carousel Dark Variant and Color Mode
- Usage

### ./references/docs-5.3-components-collapse.md

- Basic Collapse Example (HTML)
- Horizontal Collapse Example (HTML)
- Initialize Bootstrap Collapse via JavaScript
- Collapse Initialization and Usage
- Handle Bootstrap Collapse Hidden Event
- Collapse Methods
- Create Bootstrap Collapse Instance with Options

### ./references/docs-5.3-components-dropdowns.md

- Bootstrap Dropdown Alignment Examples
- Bootstrap Dropstart Dropdowns
- Bootstrap Dropdown Menu Text Example
- Bootstrap Dropend Dropdowns
- Bootstrap Dropdown Positioning with Offset and Reference
- Bootstrap Dropdown Menu Header Example
- Default and Split Dropup Buttons HTML
- Bootstrap Dropdown Menu Divider Example
- Bootstrap Dropdown Form Example
- Dark Dropdown in Navbar HTML
- Bootstrap Dropdown with Link Trigger (HTML)
- Bootstrap Dropdown Auto Close HTML Examples
- Bootstrap Large Split Button Dropdown (HTML)
- Bootstrap Dropdown Caret Sass Mixins
- Bootstrap Dropdown Menu Items
- Bootstrap Dropdown with Form Trigger
- Dropdown Options
- Configure Dropdown with popperConfig (JavaScript)
- Initialize Bootstrap Dropdowns with JavaScript

### ./references/docs-5.3-components-list-group.md

- Handle Tab Shown Event (JavaScript)
- Initialize Bootstrap Tab Instance (JavaScript)
- Bootstrap Horizontal List Group
- Bootstrap Numbered List Group
- Bootstrap List Group Tab Structure (HTML)
- Bootstrap List Group with Radio Buttons
- Bootstrap List Group Item Variants (HTML)
- Bootstrap List Group Action Variants (HTML)
- Basic List Group HTML
- Actionable List Group Items with Links HTML
- Bootstrap List Group with Actionable Items
- Bootstrap Responsive Horizontal List Groups
- Actionable List Group Items with Buttons HTML

### ./references/docs-5.3-components-modal.md

- Pass Options via JavaScript (JavaScript)
- Add Popover and Tooltip in Bootstrap Modal
- Static Bootstrap Modal Structure (HTML)
- Create Scrollable Modal Body with Bootstrap
- Initialize Modal via JavaScript (JavaScript)
- Bootstrap Grid Layout in Modal Body
- Bootstrap Responsive Fullscreen Modals
- Live Bootstrap Modal Demo with Trigger Button (HTML)

### ./references/docs-5.3-components-navbar.md

- Bootstrap Navbar Example
- Bootstrap Navbar Brand Examples
- Default Navbar Placement (HTML)
- Bootstrap Navbar with Text and Navigation
- Bootstrap Navbar with Form Buttons
- Bootstrap Navbar with Brand and Search Form
- Navbar with Vertical Scrolling (HTML)
- Bootstrap Navbar with Hidden Brand Toggler
- Bootstrap Dark Navbar Color Scheme
- Navbar with Responsive Container (HTML)
- Sticky Top Navbar Placement (HTML)
- Bootstrap Navbar with Image
- Navbar with Container (HTML)
- Basic Offcanvas Navbar HTML Structure
- Bootstrap Navbar with Image and Text

### ./references/docs-5.3-components-navs-tabs.md

- Bootstrap Pills Example
- Bootstrap Tab Instance Methods
- Bootstrap Tabs Example
- Right-Aligned Horizontal Nav (HTML)
- Bootstrap Responsive Flex Nav HTML
- Centered Horizontal Nav (HTML)
- Bootstrap Underline Navigation HTML
- Bootstrap Nav Fill Justify HTML (NAV)
- Bootstrap Pills Navigation HTML
- Bootstrap Vertical Pills Example
- Base Nav with NAV Element (HTML)
- Bootstrap Tabs with Dropdown Example (HTML)
- Select Specific Bootstrap Tabs via JavaScript
- Bootstrap Nav Fill Justify HTML (UL)
- Bootstrap Pills with Dropdown Example (HTML)
- Activating Tabs via JavaScript
- Base Nav with UL Element (HTML)
- Using Data Attributes for Tabs
- Activate Bootstrap Tabs with Data Attributes (HTML)
- Activate Bootstrap Tabs Programmatically with JavaScript
- Listen for Bootstrap Tab Shown Event (JavaScript)

### ./references/docs-5.3-components-offcanvas.md

- Offcanvas Placement Examples (HTML)
- Bootstrap Offcanvas Live Demo with Triggers (HTML)
- Bootstrap Dark Offcanvas Example (Deprecated)
- Offcanvas Instance Creation
- Bootstrap Offcanvas Component Example (HTML)
- Create Bootstrap Offcanvas Instance (JavaScript)
- Initialize Bootstrap Offcanvas with JavaScript
- Bootstrap Offcanvas with Scrolling and Backdrop
- Bootstrap Offcanvas with Body Scrolling Example
- Offcanvas Methods
- Dismiss Offcanvas Button (Outside)
- Dismiss Offcanvas Button (Inside)
- Bootstrap Responsive Offcanvas Classes
- Responsive Offcanvas Toggle (HTML)

### ./references/docs-5.3-components-pagination.md

- Bootstrap Pagination with Icons and ARIA Attributes
- Large and Small Bootstrap Pagination Sizing
- Disabled Bootstrap Pagination Item
- Basic Bootstrap Pagination HTML Structure
- Center Align Pagination with HTML
- End Align Pagination with HTML

### ./references/docs-5.3-components-placeholders.md

- Bootstrap Placeholder Example: Card Component
- Bootstrap Placeholder Usage: Basic and Button
- Bootstrap Placeholder Animations
- Bootstrap Placeholder Width Customization

### ./references/docs-5.3-components-popovers.md

- Get or Create Bootstrap Popover Instance and Set Content (JavaScript)
- Using Popper.js Configuration
- Configuring Popover Options with JavaScript (Bootstrap)
- Popover Methods
- Initialize All Popovers with JavaScript
- Popover Configuration Options
- Initialize Bootstrap Popover with JavaScript
- Handle Bootstrap Popover Hidden Event (JavaScript)
- Popover Events
- Initialize Dismissible Popover with JavaScript
- Configure Popover with Popper.js Configuration Function (JavaScript)
- Initialize Popover with Custom Container (Body)
- Create Dismissible Popover on Next Click (HTML)
- Configuring Popover Options with Data Attributes (Bootstrap)
- Implement Custom Popover with HTML
- Bootstrap Popover HTML Structure
- Bootstrap Popover Sass Variables
- Initialize Popover within Modal with Custom Container
- Popover CSS Variables Definition (SCSS)
- Customize Popover Appearance with CSS Variables (SCSS)
- Bootstrap Popover Placement Options
- Enable Popover on Disabled Button (HTML)

### ./references/docs-5.3-components-progress.md

- Bootstrap Progress Bar Basic Structure and Examples
- Bootstrap Stacked Progress Bars

### ./references/docs-5.3-components-scrollspy.md

- Bootstrap Scrollspy Navigation Example
- Bootstrap Scrollspy with Simple Anchors
- Bootstrap Scrollspy HTML Structure

### ./references/docs-5.3-components-spinners.md

- Bootstrap Spinners in Buttons (HTML)
- Spinner with Text using Flexbox HTML

### ./references/docs-5.3-components-toasts.md

- Bootstrap Live Toast Example with JavaScript Initialization
- Get or Create Toast Instance with JavaScript
- Toast with Close Button and Autohide Disabled (HTML)
- Get Toast Instance with JavaScript
- Customizing Bootstrap Toasts: Simple Layout
- Customizing Bootstrap Toasts: With Actions
- Bootstrap Toasts: Color Schemes with Utilities
- Handle Toast Hidden Event with JavaScript
- Initialize Bootstrap Toasts with JavaScript
- Toast Options
- Stacking Toasts with Bootstrap Toast Container
- Toast Methods
- Toast Accessibility with aria-live and aria-atomic (HTML)
- Configure Toast Options via Data Attributes
- Configure Toast with JSON Data Attribute

### ./references/docs-5.3-components-tooltips.md

- Bootstrap Tooltip Placement Examples (HTML)
- Bootstrap Tooltip HTML Structure Example
- Get Tooltip Instance and Use setContent Method
- Configure Tooltip Options with JavaScript (JavaScript)
- Initialize Tooltip with Popper.js Configuration
- Initialize Bootstrap Tooltip via JavaScript
- Initialize All Tooltips with JavaScript
- Custom Tooltip Styling with CSS Variables
- Bootstrap Tooltip Event Handling in JavaScript
- Tooltip Configuration Options
- Configure Tooltip Options with Data Attributes (HTML)
- Bootstrap Tooltip Boundary Option (JavaScript)

### ./references/docs-5.3-content-figures.md

- Aligned Figure Caption (HTML)

### ./references/docs-5.3-content-images.md

- Bootstrap Responsive Images

### ./references/docs-5.3-content-reboot.md

- Example Link (HTML)
- Example Paragraph (HTML)
- Indicating Sample Output with `<samp>`
- HTML Example of Hidden Input Element
- Styling Tables with Bootstrap
- Horizontal Rules (HTML)
- Indicating User Input with `<kbd>`
- Displaying Code Blocks with `<pre>`
- Indicating Variables with `<var>`

### ./references/docs-5.3-content-tables.md

- Bootstrap Striped and Hoverable Table
- Bootstrap Bordered Table
- Bootstrap Table: Nesting Tables
- Bootstrap Table: Small Tables
- Bootstrap Table Variants and Row/Cell Coloring
- Bootstrap Responsive Table

### ./references/docs-5.3-content-typography.md

- Description List Alignment Example (HTML)
- Inline List Example (HTML)
- Unstyled List Example (HTML)
- Bootstrap Lead Paragraph HTML Example
- Implementing Basic Blockquotes
- Displaying Abbreviations with Tooltips
- Styling Inline Text Elements with HTML Tags
- Blockquotes with Attribution
- Styling Inline Text Elements with Bootstrap Classes

### ./references/docs-5.3-customize-color.md

- Sass Example: Using Color Variables
- Apply Subtle Primary Background and Border with Text Emphasis

### ./references/docs-5.3-customize-color-modes.md

- Enable Dark Mode with HTML Data Attribute

### ./references/docs-5.3-customize-css-variables.md

- Bootstrap CSS Variables for Page Styles

### ./references/docs-5.3-customize-sass.md

- Importing Specific Bootstrap Sass Parts
- Compiling Sass with the Sass CLI
- Bootstrap Sass File Structure Example (Manual Download)
- Bootstrap Sass File Structure Example
- Importing All of Bootstrap Sass

### ./references/docs-5.3-examples-masonry.md

- Integrate Masonry with Bootstrap Grid and Cards
- Include Masonry JavaScript Plugin via CDN

### ./references/docs-5.3-forms-checks-radios.md

- Bootstrap Checkbox Examples (HTML)
- Bootstrap Radio Examples (HTML)
- Bootstrap Default Stacked Checkboxes
- Bootstrap Disabled Radio Examples (HTML)
- Bootstrap Default Stacked Radios
- Bootstrap Disabled Checkbox Examples (HTML)
- Bootstrap Outlined Styles HTML
- Bootstrap Radio Toggle Buttons HTML
- Bootstrap Switch Checkbox Markup
- Bootstrap Checkbox Toggle Buttons
- Inline Checkboxes and Radios with Bootstrap
- Reversed Form Controls with Bootstrap

### ./references/docs-5.3-forms-floating-labels.md

- Bootstrap Floating Input Group HTML
- Floating Labels for Textareas in Bootstrap HTML
- Bootstrap Floating Form Layout HTML
- Bootstrap Floating Plaintext Input HTML

### ./references/docs-5.3-forms-form-control.md

- Bootstrap File Input Examples
- Bootstrap Datalist Example
- Basic Form Controls Example (HTML)
- Inline Form Text Example (HTML)
- Disabled Form Controls (HTML)
- Form Control Sizing (HTML)
- Form Text with Help Block (HTML)

### ./references/docs-5.3-forms-input-group.md

- Bootstrap Input Group Basic Examples
- Bootstrap Input Group Sizing Examples
- Bootstrap Input Group with Multiple Addons
- Bootstrap Input Group Border Radius Example
- Bootstrap Input Group Wrapping Example
- Bootstrap Input Group with Dropdown Button (HTML)
- Bootstrap Segmented Button Group with Dropdown (HTML)
- Bootstrap Input Group with Button Addons

### ./references/docs-5.3-forms-layout.md

- Bootstrap Grid Column Sizing Examples
- Complex Form Layout with Grid System (HTML)
- Bootstrap Auto-Sizing Form Example (HTML)
- Bootstrap Size-Specific Column Form (HTML)
- Bootstrap Inline Form Example (HTML)
- Basic Form Layout with Margin Utilities (HTML)

### ./references/docs-5.3-forms-overview.md

- Basic Form Example with Bootstrap
- Form Accessibility Techniques in HTML

### ./references/docs-5.3-forms-range.md

- Range Input with Output Value Display (HTML & JS)

### ./references/docs-5.3-forms-select.md

- Bootstrap Select SCSS Variables

### ./references/docs-5.3-forms-validation.md

- Bootstrap Form Validation Tooltips Example (HTML)
- Bootstrap Server-Side Form Validation Example (HTML)
- Bootstrap Form Validation Example (HTML)

### ./references/docs-5.3-getting-started-download.md

- Install Bootstrap with NuGet
- Install Bootstrap with Bun
- Install Bootstrap with RubyGems
- Install Bootstrap with Yarn
- Install Bootstrap with Composer
- Install Bootstrap via npm
- Generate SRI Hash for Bootstrap JS
- Import Bootstrap in JavaScript (CommonJS/ES Modules)
- Include Bootstrap and Popper via CDN
- Include Bootstrap via jsDelivr CDN

### ./references/docs-5.3-getting-started-introduction.md

- Include Bootstrap CSS and JS via CDN
- Basic HTML Structure for Bootstrap
- Include Bootstrap JS and Popper Separately
- Viewport Meta Tag for Responsive Design in Bootstrap
- HTML5 Doctype Declaration for Bootstrap
- Overriding Box-sizing for Specific Selectors in Bootstrap

### ./references/docs-5.3-getting-started-javascript.md

- Initialize Bootstrap tooltips with jQuery
- Initialize Bootstrap Modal with Default and Custom Options
- Execute Action After Bootstrap Collapse Transition Completes
- Plugin Instance Methods
- Get Bootstrap Plugin Instance using getInstance
- Get or Create Bootstrap Plugin Instance using getOrCreateInstance
- Using Bootstrap as an ES Module in the Browser
- Modify default plugin settings in Bootstrap
- Bootstrap Carousel Slide Transition and Ignored Calls
- Initialize Bootstrap Components with CSS Selectors
- Modal Plugin - Dispose Method
- Plugin Static Properties
- Initializing Bootstrap Toasts with ES Modules
- Sanitizer Configuration
- Correctly dispose of Bootstrap modal instance
- Trigger Bootstrap tooltip method with jQuery
- Plugin Default Settings

### ./references/docs-5.3-getting-started-parcel.md

- Start Parcel Development Server
- Add Parcel npm Start Script
- Create Project Structure
- Install Bootstrap and Popper.js
- Create Project Folder and Initialize npm
- Install Parcel Development Dependency
- Configure Parcel HTML Entry Point
- Import Individual Bootstrap JS Plugins
- Import Bootstrap JavaScript in JS
- Configure Sass Deprecation Warnings
- Import Bootstrap CSS in Sass

### ./references/docs-5.3-getting-started-rtl.md

- RTLCSS Output Example
- RTL Bootstrap Starter Template
- Simultaneous LTR and RTL Imports with RTLCSS (Sass)

### ./references/docs-5.3-getting-started-vite.md

- Add npm Start Script (package.json)
- Vite HTML Entry Point (src/index.html)
- Configure Vite (vite.config.js)
- Import Bootstrap JS and CSS (src/js/main.js)
- Import Bootstrap CSS (src/scss/styles.scss)

### ./references/docs-5.3-getting-started-webpack.md

- Start Webpack Development Server (npm)
- Install Webpack Development Dependencies
- Install Bootstrap and Popper
- Initialize npm Project
- Create Project Structure
- Install Sass and Webpack Loaders
- Install mini-css-extract-plugin for Webpack
- Define npm Scripts for Webpack (package.json)
- Import Bootstrap JavaScript
- Create HTML Template (src/index.html)
- Configure Webpack Settings (webpack.config.js)
- Include Extracted CSS in HTML
- Configure Webpack to Extract CSS with mini-css-extract-plugin
- Configure Webpack Loaders for Bootstrap
- Configure Webpack to Extract SVG Files

### ./references/docs-5.3-helpers-clearfix.md

- Bootstrap Clearfix Example with Floated Buttons

### ./references/docs-5.3-helpers-color-background.md

- Apply Color and Background Utilities to Cards (HTML)
- Use Color and Background Utilities on Badges (HTML)
- Apply Text and Background Colors with Contrast (HTML)

### ./references/docs-5.3-helpers-colored-links.md

- Bootstrap Link Utilities for Customization (HTML)
- Bootstrap Link Colors with Hover States (HTML)

### ./references/docs-5.3-helpers-focus-ring.md

- Basic Focus Ring Example (HTML)
- Themed Focus Ring Utilities (HTML)
- Customizing Focus Ring Offset and Blur (HTML)

### ./references/docs-5.3-helpers-icon-link.md

- Icon Link with Bootstrap Utilities (HTML)
- Customizing Icon Link Color on Hover (HTML/CSS)

### ./references/docs-5.3-helpers-position.md

- Responsive Sticky Top Positioning with Bootstrap
- Responsive Sticky Bottom Positioning with Bootstrap

### ./references/docs-5.3-helpers-ratio.md

- Basic Ratio Example (HTML)
- Responsive Custom Aspect Ratio (SCSS)
- Predefined Aspect Ratios (HTML)

### ./references/docs-5.3-helpers-stacks.md

- Bootstrap Stack Example: Inline Form
- Bootstrap Stack Example: Vertical Buttons
- Bootstrap Vertical Stack (.vstack) Example
- Bootstrap Horizontal Stack (.hstack) Example
- Bootstrap Horizontal Stack with Margin Spacer

### ./references/docs-5.3-helpers-stretched-link.md

- Card with Stretched Links (Positioning Issues) - Bootstrap HTML

### ./references/docs-5.3-helpers-vertical-rule.md

- Basic Vertical Rule HTML

### ./references/docs-5.3-helpers-visually-hidden.md

- SCSS: Use visually hidden mixins

### ./references/docs-5.3-layout-breakpoints.md

- Bootstrap Sass Media Query Mixins for Responsive Layouts

### ./references/docs-5.3-layout-columns.md

- Bootstrap Column Wrapping Example
- Customizing Bootstrap Order Utilities with Sass
- Bootstrap Responsive Column Break with d-none d-md-block
- Bootstrap Order Classes for Visual Reordering
- Bootstrap Margin Utilities for Spacing
- Bootstrap Order-First and Order-Last Classes
- Bootstrap Responsive Floated Images with Clearfix

### ./references/docs-5.3-layout-containers.md

- Bootstrap Sass Mixin for Creating Custom Containers

### ./references/docs-5.3-layout-css-grid.md

- Column Start Alignment with CSS Grid
- Bootstrap Grid: Adding Rows and Customizing Placement
- Bootstrap Grid: Customizing Columns and Gaps
- Bootstrap Grid: Customizing Columns with CSS Variables
- Bootstrap Grid: Auto Columns Example
- Bootstrap Grid: Modifying Vertical Gaps
- Bootstrap Grid: Customizing Columns and Gaps (Mixed Widths)
- Customize Bootstrap Sass Grid with HTML Example
- Two Column Layout with CSS Grid
- Bootstrap Grid: Customizing Horizontal and Vertical Gaps
- Responsive Columns with CSS Grid

### ./references/docs-5.3-layout-grid.md

- Bootstrap Row Columns Examples (HTML)
- Basic Grid Layout Example (HTML)
- Bootstrap Grid Nesting Example (HTML)
- Bootstrap: Responsive Grid Classes - Mix and Match
- Bootstrap Grid Layout HTML Structure
- Bootstrap: Variable Width Content Columns
- Bootstrap: Responsive Grid Classes - All Breakpoints
- Bootstrap: Create Equal-Width Columns
- Bootstrap: Responsive Grid Classes - Stacked to Horizontal
- Bootstrap Grid Layout with Mixins (Sass)
- Customizing Bootstrap Grid Tiers (Sass)

### ./references/docs-5.3-layout-gutters.md

- Bootstrap Horizontal Gutters Example (HTML)
- Bootstrap Vertical Gutters Example (HTML)
- Bootstrap Row Columns with Responsive Gutters (HTML)
- Bootstrap Combined Horizontal & Vertical Gutters (HTML)

### ./references/docs-5.3-migration.md

- Instantiate Bootstrap Plugins with CSS Selectors (JavaScript)
- Customize Bootstrap Text and Background Colors with Opacity Utilities
- Create Layouts with Bootstrap Stack and Vertical Rule Helpers
- Implement Bootstrap's New Placeholder Component
- Add Offcanvas Drawers to Bootstrap Navbars
- Customizing Sass Maps in Bootstrap Build
- Bootstrap 5.0.0 Dependencies and Compiler Changes

### ./references/docs-5.3-utilities-api.md

- Add, Remove, and Modify Utilities with map-merge()
- Rename Bootstrap Utility Classes with Sass
- Enable Responsive Variations for Bootstrap Utilities with Sass
- Add Custom Bootstrap Utilities with Sass
- Override Bootstrap Utilities with Sass
- Generate Visibility Utilities with Sass (Null Class)
- Generate Responsive Utilities Across Breakpoints
- Generate Local CSS Variables for Utility Rulesets
- Generate Print-Specific Utility Classes
- Utility API Configuration
- Generate Pseudo-Class Variations with States Option

### ./references/docs-5.3-utilities-background.md

- Bootstrap: Apply Background Opacity with Utility Classes

### ./references/docs-5.3-utilities-borders.md

- Set Border Width using Bootstrap Utilities
- Add or Remove Borders using Bootstrap Utilities
- Control Border Opacity with Bootstrap Utilities
- Apply Border Radius with Sass Mixins (SCSS)

### ./references/docs-5.3-utilities-colors.md

- Bootstrap Text Color CSS Variable Example (CSS)
- Bootstrap Text Opacity Utilities (HTML)

### ./references/docs-5.3-utilities-display.md

- Bootstrap HTML: Inline Display Example
- Bootstrap HTML: Responsive Hiding Example
- Bootstrap HTML: Print Display Examples
- Bootstrap HTML: Block Display Example
- Bootstrap SCSS: Display Utilities API Configuration

### ./references/docs-5.3-utilities-flex.md

- Control Flex Item Growth with flex-grow Utilities (HTML)
- Control Flex Item Shrinking with flex-shrink Utilities (HTML)
- Align Flex Items with align-self Utilities (HTML)
- Control Flex Item Spacing with Auto Margins (HTML)
- Align Items with Bootstrap Flexbox Utilities
- Justify Content with Bootstrap Flexbox Utilities
- Bootstrap Media Object Component
- Enable Flexbox Container (HTML)
- Flex Item Wrapping with flex-wrap Utilities
- Enable Inline Flexbox Container (HTML)

### ./references/docs-5.3-utilities-float.md

- Sass Utilities API for Floats
- Responsive Float Utilities (HTML)
- Basic Float Utilities (HTML)

### ./references/docs-5.3-utilities-link.md

- Link Underline Hover Variants (HTML)
- Link Underline Color Utilities (HTML)
- Link Opacity Utilities (HTML)
- Link Underline Opacity Utilities (HTML)

### ./references/docs-5.3-utilities-object-fit.md

- Responsive Object Fit Utilities (HTML)
- Object Fit Utilities for Video (HTML)

### ./references/docs-5.3-utilities-opacity.md

- Apply Opacity Utilities in HTML

### ./references/docs-5.3-utilities-overflow.md

- Bootstrap Overflow Utilities (HTML)

### ./references/docs-5.3-utilities-position.md

- Bootstrap Position Utility Examples
- Bootstrap Edge Positioning Utilities
- Bootstrap Sass Position Utilities API
- Bootstrap Sass Position Values

### ./references/docs-5.3-utilities-shadows.md

- Bootstrap Shadow Utility Classes (HTML)

### ./references/docs-5.3-utilities-sizing.md

- Bootstrap Viewport Sizing Utilities (HTML)
- Bootstrap Sizing Utilities SCSS Configuration
- Bootstrap Width Utilities (HTML)

### ./references/docs-5.3-utilities-spacing.md

- HTML Example: Using column-gap Utility
- Row Gap Utility for Grid Layout (HTML)

### ./references/docs-5.3-utilities-vertical-align.md

- Bootstrap Vertical Alignment CSS Classes for Table Cells

### ./references/docs-5.3-utilities-z-index.md

- HTML Example for Z-index Utilities
