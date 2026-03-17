---
name: matlab-live-script
description: Create MATLAB plain text Live Scripts (.m files) following specific formatting rules. Use when generating MATLAB scripts, educational MATLAB content, Live Scripts, or when the user requests .m files with rich text formatting.
license: MathWorks BSD-3-Clause (see LICENSE)
---

# MATLAB Plain Text Live Script Generator

This skill provides comprehensive guidelines for creating properly formatted MATLAB plain text Live Scripts. These scripts combine executable MATLAB code with rich text documentation in a single .m file.

## When to Use This Skill

- Creating new MATLAB Live Scripts in plain text format
- Generating educational MATLAB content with explanations
- When the user requests .m files with documentation
- Converting code examples into Live Script format
- Creating tutorial or example scripts

## Critical Rules

### File Format
- **ALWAYS** use the .m suffix for plain text Live Scripts
- **NEVER** create .mlx scripts (binary format)
- **MUST** close every script with the required appendix

### Required Appendix
Every Live Script must end with this exact formatting:

```matlab
%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
```

### Reading Live Scripts (Token Optimization)
When reading a Live Script file to pass back to the language model, you can save significant token count by ignoring everything below the appendix marker (which begins with `%[appendix]`). This optimization avoids passing large embedded images that are stored in the appendix section. All working code and text content appears before the appendix, so no functional information is lost.

## Formatting Rules

### Section Headers
**CORRECT format:**
```matlab
%%
%[text] ## Section Title
```

**INCORRECT format (DO NOT USE):**
```matlab
%% Section Title
```

### Rich Text
- Normal text uses `%[text]` prefix
- Text intended for a single paragraph should appear on a single line
- Use Markdown formatting after `%[text]`
- **DO NOT** leave blank lines in the file

### Bulleted Lists
Bulleted lists must have a backslash on the last item:

```matlab
%[text] - bullet 1
%[text] - bullet 2
%[text] - bullet 3 \
```


### Tables

```matlab
%[text:table]
%[text] | Column A | Column B |
%[text] | --- | --- |
%[text] | Value 1 | Value 2 |
%[text] | Value 3 | Value 4 |
%[text:table]
```


### LaTeX Equations
Format equations with double backslashes:

```matlab
%[text] $ e = \\sum_{\\alpha=0}^\\infty \\alpha^n/n! $
```

Note: All backslashes in LaTeX must be doubled.

### Comments for Readers
**DO NOT** use fprintf for reader comments:
```matlab
fprintf('This is a comment')  % WRONG
```

**Instead use rich text:**
```matlab
%[text] This is a comment  % CORRECT
```

## Code Guidelines

### Figures and Plots
- Use **implicit figure creation** (just call plot, histogram, etc.)
- **DO NOT** use the `figure` command to create new figures
- Put no more than one plot per section (unless using tiled layouts)
- Only use tiled plots when especially important to the illustration

### Script Initialization
- **DO NOT** start scripts with `close all` or `clear` commands
- Let MATLAB handle workspace management

## Complete Example

```matlab
%[text] # Sinusoidal Signals
%[text] Examples of sinusoidal signal in MATLAB.
%[text] - sine waves
%[text] - cosine waves \
x = linspace(0,8*pi);
%%
%[text] ## Sine Wave
plot(x,sin(x))
title('Sine Wave')
xlabel('x (radians)')
ylabel('sin(x)')
grid on
%%
%[text] ## Cosine Wave
plot(x,cos(x))
title('Cosine Wave')
xlabel('x (radians)')
ylabel('cos(x)')
grid on
%[text]

%[appendix]{"version":"1.0"}
%---
%[metadata:view]
%   data: {"layout":"inline"}
%---
```

## Structure Pattern

A typical Live Script follows this pattern:

1. **Title and Introduction**
   ```matlab
   %[text] # Main Title
   %[text] Brief description of what this script does.
   ```

2. **Setup Code** (if needed)
   ```matlab
   variable = value;
   data = load('file.mat');
   ```

3. **Sections with Explanations**
   ```matlab
   %%
   %[text] ## Section Name
   %[text] Explanation of what this section does.
   code_goes_here();
   plot(results)
   ```

4. **Required Appendix**
   ```matlab
   %[appendix]{"version":"1.0"}
   %---
   %[metadata:view]
   %   data: {"layout":"inline"}
   %---
   ```

## Common Patterns

### Mathematical Explanations with Equations
```matlab
%[text] ## Theory
%[text] The discrete Fourier transform is defined as:
%[text] $ X(k) = \\sum_{n=0}^{N-1} x(n)e^{-j2\\pi kn/N} $
```

### Code with Inline Comments
```matlab
%%
%[text] ## Data Processing
%[text] First, we load and filter the data.
data = load('measurements.mat');
filtered = lowpass(data, 0.5);  % Apply lowpass filter
%[text] Then we visualize the results.
plot(filtered)
title('Filtered Data')
```

### Multiple Related Plots (Tiled Layout)
Only when necessary for comparison:
```matlab
%%
%[text] ## Comparison of Methods
tiledlayout(1,2)
nexttile
plot(method1)
title('Method 1')
nexttile
plot(method2)
title('Method 2')
```

## Checklist

Before finishing a Live Script, verify:
- [ ] File has .m extension
- [ ] Sections use `%%` followed by `%[text] ##`
- [ ] No blank lines in the file
- [ ] Bulleted lists end with backslash
- [ ] LaTeX uses double backslashes
- [ ] No `figure` commands
- [ ] No `close all` or `clear` at start
- [ ] Appendix is present and correctly formatted
- [ ] No `fprintf` for comments (use `%[text]` instead)

## Troubleshooting

**Issue**: Script doesn't display rich text properly
- **Solution**: Ensure `%[text]` is at the start of each text line

**Issue**: Equations not rendering
- **Solution**: Check that all backslashes are doubled in LaTeX

**Issue**: Sections not appearing correctly
- **Solution**: Use `%%` on its own line, then `%[text] ##` on the next line

**Issue**: Script won't save with outputs
- **Solution**: Verify appendix is exactly as specified, with proper indentation
