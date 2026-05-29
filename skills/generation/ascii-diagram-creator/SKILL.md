---
name: ascii-diagram-creator
description: Create ASCII diagrams from workflow definitions and save them as image files (PNG, SVG, etc.)
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: diagram-generation
---

## What I do

I create professional ASCII diagrams from user-defined workflow specifications and save them as image files:

1. **Parse Workflow Definition**: Analyze the user's workflow description to understand the diagram structure
2. **Generate ASCII Diagram**: Create a clean, well-formatted ASCII representation of the workflow
3. **Convert to Image**: Save the ASCII diagram as an image file (PNG, SVG, or other formats)
4. **Save to Disk**: Store the image file in the specified location (default: `./diagrams/`)

Supported diagram types:
- Flowcharts
- Process flows
- Sequence diagrams
- State machines
- System architecture diagrams
- Decision trees

## When to use me

Use this workflow when:
- You need to visualize a workflow, process, or system architecture
- You want a quick, text-based diagram that can be saved as an image
- You need to include diagrams in documentation or presentations
- You want to document code logic or system flows
- You need to communicate complex processes in a visual format

## Prerequisites

- ImageMagick or similar tool for ASCII to image conversion
- Write permissions to the output directory
- Valid workflow definition from user input

## Steps

### Step 1: Analyze the Workflow Request
- Parse the user's workflow definition
- Identify the diagram type needed (flowchart, sequence, etc.)
- Extract key elements:
  - Start/end points
  - Processes/actions
  - Decision points
  - Connections/flows
  - Labels and annotations

### Step 2: Design the ASCII Diagram
- Create a well-structured ASCII diagram using box-drawing characters
- Use consistent spacing and alignment
- Follow standard ASCII diagramming conventions:
  ```
  ┌─────────────┐
  │    Start    │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   Process   │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │    End      │
  └─────────────┘
  ```
- Ensure the diagram is readable and properly aligned

### Step 3: Create Output Directory
- Create a `diagrams/` directory if it doesn't exist:
  ```bash
  mkdir -p diagrams
  ```
- Use a custom directory if specified by the user

### Step 4: Save ASCII to Text File
- Save the ASCII diagram to a temporary text file:
  ```bash
  cat > /tmp/workflow.txt << 'EOF'
  [ASCII diagram content]
  EOF
  ```

### Step 5: Convert ASCII to Image
- Use ImageMagick to convert the ASCII text to an image:
  ```bash
  convert -font Courier -pointsize 12 -background white -fill black \
    -border 20 -bordercolor white /tmp/workflow.txt diagrams/workflow.png
  ```
- Or use `asciio` or other ASCII diagram tools if available
- Support multiple formats:
  - PNG (default)
  - SVG (for scalable graphics)
  - PDF (for documentation)

### Step 6: Verify and Report
- Verify the image file was created:
  ```bash
  ls -lh diagrams/workflow.png
  ```
- Display the ASCII diagram in the terminal
- Provide the image file path and format to the user
- Offer to open the image in a viewer if desired

## Examples

### Example 1: Simple Flowchart
**User Input**: "Create a flowchart showing a login process: start, check credentials, if valid show dashboard, else show error, end"

**ASCII Diagram Created**:
```
┌─────────────┐
│    Start    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Check Credentials│
└────────┬────────┘
         │
         ├────── Valid ────┐
         │                 │
         │                 ▼
         │    ┌───────────────┐
         │    │  Show Dashboard │
         │    └───────┬───────┘
         │           │
         │           │
Invalid  │           ▼
         │    ┌───────────────┐
         └───►│     End       │
              └───────────────┘
```

**Image Saved**: `diagrams/login-flow.png`

### Example 2: Decision Tree
**User Input**: "Create a decision tree for deployment: check if tests pass, if yes then deploy to staging, else fix bugs. After staging check if approved, if yes deploy to production, else make changes"

**ASCII Diagram Created**:
```
┌──────────────┐
│   Start      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Run Tests   │
└──────┬───────┘
       │
       ├──── Pass ────┐
       │              │
       │              ▼
       │    ┌─────────────────┐
       │    │ Deploy Staging  │
       │    └────────┬────────┘
       │             │
       │             ▼
       │    ┌─────────────────┐
       │    │   Get Approval  │
       │    └────────┬────────┘
       │             │
       │    Approved │
       │             │
       │             ▼
       │    ┌─────────────────┐
       │    │ Deploy Production│
       │    └────────┬────────┘
       │             │
       └──────┬──────┘
             │
             ▼
      ┌──────────────┐
      │     End      │
      └──────────────┘
```

**Image Saved**: `diagrams/deployment-flow.png`

### Example 3: Sequence Diagram
**User Input**: "Create a sequence diagram showing user interaction: user requests data, server processes it, database returns result, server responds to user"

**ASCII Diagram Created**:
```
User    ───────────────────────────────────────────────► Server
                              Request Data
Server  ───────────────────────────────────────────────► Database
                              Query Data
Database ──────────────────────────────────────────────► Server
                              Return Result
Server  ───────────────────────────────────────────────► User
                              Send Response
```

**Image Saved**: `diagrams/sequence-user-data.png`

## ASCII Diagram Conventions

### Box Drawing Characters
Use Unicode box-drawing characters for professional-looking diagrams:
- Horizontal: `─`, `═`, `━`
- Vertical: `│`, `║`, `┃`
- Corners: `┌`, `┐`, `└`, `┘`
- Crosses: `┼`, `╪`, `╬`
- T-junctions: `├`, `┤`, `┬`, `┴`

### Spacing Guidelines
- Maintain consistent spacing between elements
- Use single spaces for readability
- Align boxes and text properly
- Leave margins around the diagram

### Color and Styling (when converting to image)
- Use Courier or monospace fonts for ASCII
- Set appropriate font size (10-14pt)
- Use white background for clarity
- Add borders for presentation-ready output

## Image Conversion Options

### Using ImageMagick
```bash
# Convert to PNG
convert -font Courier -pointsize 12 -background white -fill black \
  -border 20 -bordercolor white input.txt output.png

# Convert to SVG
convert -font Courier -pointsize 12 input.txt output.svg

# Convert with custom dimensions
convert -font Courier -pointsize 14 -size 800x600 -background white \
  -fill black input.txt output.png
```

### Using ASCIIO (if available)
```bash
# Generate ASCII diagram and convert
echo "[diagram definition]" | asciio -o output.png
```

### Using Python PIL
```python
from PIL import Image, ImageDraw, ImageFont

# Create image from ASCII text
img = Image.new('RGB', (800, 400), color='white')
d = ImageDraw.Draw(img)
font = ImageFont.truetype('Courier.ttf', 12)

# Draw ASCII text
d.text((10, 10), ascii_text, font=font, fill='black')
img.save('diagrams/output.png')
```

## Best Practices

- Keep ASCII diagrams simple and readable
- Use consistent spacing and alignment
- Limit diagram width to terminal width (usually 80-120 characters)
- Add descriptive labels and annotations
- Save images in standard formats (PNG, SVG)
- Organize diagrams in a dedicated directory
- Use descriptive filenames (`login-flow.png`, not `diagram1.png`)
- Provide both ASCII and image output for flexibility

## Common Issues

### ImageMagick Not Installed
**Issue**: `convert: command not found`

**Solution**:
```bash
# macOS
brew install imagemagick

# Ubuntu/Debian
sudo apt-get install imagemagick

# Fedora/CentOS
sudo dnf install imagemagick
```

### Font Not Found
**Issue**: `convert: unable to read font`

**Solution**:
```bash
# List available fonts
convert -list font

# Use system font
convert -font /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf input.txt output.png
```

### Diagram Too Wide
**Issue**: ASCII diagram exceeds terminal width

**Solution**:
- Simplify the workflow
- Use shorter labels
- Break complex diagrams into smaller parts
- Increase canvas size when converting to image

### Special Characters Not Rendering
**Issue**: Box-drawing characters display incorrectly

**Solution**:
- Use UTF-8 encoding
- Check terminal character set support
- Use ASCII alternatives if needed:
  - `|` instead of `│`
  - `-` instead of `─`
  - `+` instead of `┼`

## Workflow Diagram Types Reference

### Flowchart
```
┌─────┐    ┌─────┐    ┌─────┐
│Start│───►│Process│───►│ End │
└─────┘    └─────┘    └─────┘
```

### Decision Tree
```
     ┌──────┐
     │Start │
     └──┬───┘
        │
        ├── Yes ──► Option A
        │
        └── No ───► Option B
```

### Sequence Diagram
```
A ─────────────► B
     Message 1
B ─────────────► C
     Message 2
```

### State Machine
```
     ┌──────┐
     │ Idle │
     └──┬───┘
        │ Event
        ▼
     ┌──────┐
     │Active│
     └──────┘
```

## Troubleshooting Checklist

Before creating the diagram:
- [ ] Workflow definition is clear and complete
- [ ] Output directory exists or can be created
- [ ] ImageMagick or conversion tool is installed
- [ ] Font files are available

After creating the diagram:
- [ ] ASCII diagram is properly formatted
- [ ] Image file was created successfully
- [ ] Image file is readable and displays correctly
- [ ] File path is reported to the user

## Related Commands

```bash
# Check ImageMagick version
convert --version

# List available fonts
convert -list font

# View image file
file diagrams/workflow.png
display diagrams/workflow.png

# Convert to different formats
convert diagrams/workflow.png diagrams/workflow.svg
convert diagrams/workflow.png diagrams/workflow.pdf

# Resize image
convert diagrams/workflow.png -resize 800x600 diagrams/workflow-thumb.png
```

## Related Skills

- `diagram-creator`: For creating Draw.io diagrams
- `nextjs-pr-workflow`: For creating PRs with diagram attachments
- `git-pr-creator`: For PR creation with JIRA integration
