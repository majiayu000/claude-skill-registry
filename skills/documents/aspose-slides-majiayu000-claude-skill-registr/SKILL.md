---
name: aspose-slides
description: Comprehensive skill for manipulating Microsoft PowerPoint presentations using Aspose.Slides.NET library with modern C# patterns
---

# Aspose.Slides for .NET - PowerPoint Manipulation Skill

## Overview
This skill enables Claude Code to effectively manipulate Microsoft PowerPoint presentations using the Aspose.Slides.NET library. It provides comprehensive guidance for working with presentations programmatically without requiring Microsoft PowerPoint installation.

## Core Capabilities

### Presentation Structure
- **Creating presentations**: New presentations from scratch or from templates
- **Loading presentations**: PPT, PPTX, ODP, and other formats
- **Saving presentations**: Multiple format support (PPTX, PDF, HTML, images)
- **Slide management**: Add, remove, clone, reorder slides
- **Master slides and layouts**: Work with slide masters and apply layouts

### Content Manipulation
- **Text handling**: TextFrames, Paragraphs, Portions with formatting
- **Shapes**: AutoShapes, custom shapes, grouping, positioning
- **Tables**: Create, format, populate table data
- **Charts**: Create and customize various chart types
- **Images**: Add, replace, extract images and SVGs
- **Media**: Embed and configure audio/video

### Formatting and Styling
- **Text formatting**: Fonts, colors, alignment, spacing
- **Shape formatting**: Fill, line, effects, 3D properties
- **Themes and color schemes**: Apply and customize themes
- **Backgrounds**: Solid colors, gradients, patterns, images

### Advanced Features
- **Animations**: Timeline, effects, triggers
- **Transitions**: Slide transitions and timing
- **Comments**: Add and manage presentation comments
- **Properties**: Document properties (built-in and custom)
- **SmartArt**: Work with SmartArt graphics
- **VBA macros**: Access and manipulate VBA code

## Object Model Understanding

### Core Hierarchy
```
Presentation (IPresentation)
├── Slides (ISlideCollection)
│   ├── Slide (ISlide)
│   │   ├── Shapes (IShapeCollection)
│   │   │   ├── AutoShape (IAutoShape)
│   │   │   ├── Table (ITable)
│   │   │   ├── Chart (IChart)
│   │   │   ├── PictureFrame (IPictureFrame)
│   │   │   └── GroupShape (IGroupShape)
│   │   ├── Background (IBackground)
│   │   └── SlideShowTransition
│   └── NotesSlide (INotesSlide)
├── Masters (IMasterSlideCollection)
│   └── MasterSlide (IMasterSlide)
├── Layouts (ILayoutSlideCollection)
│   └── LayoutSlide (ILayoutSlide)
└── DocumentProperties (IDocumentProperties)
```

### Text Hierarchy
```
TextFrame (ITextFrame)
├── Paragraphs (IParagraphCollection)
│   └── Paragraph (IParagraph)
│       ├── Portions (IPortionCollection)
│       │   └── Portion (IPortion)
│       │       └── PortionFormat (IPortionFormat)
│       └── ParagraphFormat (IParagraphFormat)
└── TextFrameFormat (ITextFrameFormat)
```

## Modern C# Patterns

### Resource Management
Always use `using` statements for proper disposal:

```csharp
using Aspose.Slides;

// Single presentation
using var presentation = new Presentation("input.pptx");
// Work with presentation
presentation.Save("output.pptx", SaveFormat.Pptx);

// Multiple resources
using var sourcePresentation = new Presentation("source.pptx");
using var targetPresentation = new Presentation();
// Combine presentations
```

### Functional Collection Processing
Leverage LINQ and functional patterns:

```csharp
// Find shapes by type
var textShapes = slide.Shapes
    .OfType<IAutoShape>()
    .Where(s => s.TextFrame != null)
    .ToList();

// Process all text portions
var allText = slide.Shapes
    .OfType<IAutoShape>()
    .Where(s => s.TextFrame != null)
    .SelectMany(s => s.TextFrame.Paragraphs)
    .SelectMany(p => p.Portions)
    .Select(p => p.Text);

// Update text declaratively
slide.Shapes
    .OfType<IAutoShape>()
    .Where(s => s.Name == "Title")
    .Select(s => s.TextFrame)
    .Where(tf => tf != null)
    .ToList()
    .ForEach(tf => tf.Text = "New Title");
```

### Pattern Matching and Switch Expressions
Use modern C# features for shape handling:

```csharp
foreach (var shape in slide.Shapes)
{
    var result = shape switch
    {
        IAutoShape autoShape when autoShape.TextFrame != null 
            => ProcessTextShape(autoShape),
        ITable table 
            => ProcessTable(table),
        IChart chart 
            => ProcessChart(chart),
        IPictureFrame picture 
            => ProcessImage(picture),
        _ => null
    };
}
```

### Immutability and Builder Patterns
Create helper methods for declarative configuration:

```csharp
IAutoShape AddConfiguredShape(
    ISlide slide,
    ShapeType shapeType,
    float x, float y, float width, float height,
    Action<IAutoShape> configure)
{
    var shape = slide.Shapes.AddAutoShape(shapeType, x, y, width, height);
    configure(shape);
    return shape;
}

// Usage
var titleShape = AddConfiguredShape(
    slide, 
    ShapeType.Rectangle, 
    50, 50, 600, 100,
    shape =>
    {
        shape.TextFrame.Text = "Title";
        shape.FillFormat.FillType = FillType.Solid;
        shape.FillFormat.SolidFillColor.Color = Color.Blue;
    });
```

## Common Task Patterns

### Creating a Presentation from Template

```csharp
using var presentation = new Presentation("template.pptx");

// Populate placeholder text
foreach (var slide in presentation.Slides)
{
    foreach (var shape in slide.Shapes.OfType<IAutoShape>())
    {
        if (shape.Placeholder != null)
        {
            var placeholderType = shape.Placeholder.Type;
            shape.TextFrame.Text = placeholderType switch
            {
                PlaceholderType.Title => "Dynamic Title",
                PlaceholderType.Body => "Dynamic Content",
                _ => shape.TextFrame.Text
            };
        }
    }
}

presentation.Save("output.pptx", SaveFormat.Pptx);
```

### Adding a Table with Data

```csharp
// Define table dimensions
var columnWidths = new[] { 100.0, 150.0, 200.0 };
var rowHeights = new[] { 50.0, 40.0, 40.0, 40.0 };

var table = slide.Shapes.AddTable(
    x: 50, 
    y: 50, 
    columnWidths, 
    rowHeights);

// Populate headers
var headers = new[] { "Name", "Value", "Description" };
for (int col = 0; col < headers.Length; col++)
{
    table[col, 0].TextFrame.Text = headers[col];
    table[col, 0].CellFormat.FillFormat.FillType = FillType.Solid;
    table[col, 0].CellFormat.FillFormat.SolidFillColor.Color = 
        Color.FromArgb(68, 114, 196);
    table[col, 0].TextFrame.Paragraphs[0].Portions[0].PortionFormat
        .FillFormat.SolidFillColor.Color = Color.White;
}

// Populate data rows
var data = new[]
{
    new[] { "Item 1", "100", "First item" },
    new[] { "Item 2", "200", "Second item" },
    new[] { "Item 3", "300", "Third item" }
};

for (int row = 0; row < data.Length; row++)
{
    for (int col = 0; col < data[row].Length; col++)
    {
        table[col, row + 1].TextFrame.Text = data[row][col];
    }
}
```

### Creating a Chart

```csharp
// Add chart to slide
var chart = slide.Shapes.AddChart(
    ChartType.ClusteredColumn,
    x: 50,
    y: 50,
    width: 500,
    height: 400);

// Clear default data
chart.ChartData.Series.Clear();
chart.ChartData.Categories.Clear();

// Set categories
var categories = new[] { "Q1", "Q2", "Q3", "Q4" };
foreach (var category in categories)
{
    chart.ChartData.Categories.Add(
        chart.ChartData.ChartDataWorkbook.GetCell(0, 0, 0, category));
}

// Add data series
var series1 = chart.ChartData.Series.Add(
    chart.ChartData.ChartDataWorkbook.GetCell(0, 0, 1, "Sales"),
    chart.Type);

var salesData = new[] { 120, 150, 180, 160 };
for (int i = 0; i < salesData.Length; i++)
{
    series1.DataPoints.AddDataPointForBarSeries(
        chart.ChartData.ChartDataWorkbook.GetCell(0, i + 1, 1, salesData[i]));
}

// Style the chart
series1.Format.Fill.FillType = FillType.Solid;
series1.Format.Fill.SolidFillColor.Color = Color.FromArgb(68, 114, 196);
chart.HasTitle = true;
chart.ChartTitle.AddTextFrameForOverriding("Quarterly Sales");
```

### Text Replacement with Formatting Preservation

```csharp
void ReplaceTextPreservingFormat(
    IPresentation presentation, 
    string searchText, 
    string replacementText)
{
    foreach (var slide in presentation.Slides)
    {
        foreach (var shape in slide.Shapes.OfType<IAutoShape>())
        {
            if (shape.TextFrame == null) continue;

            foreach (var paragraph in shape.TextFrame.Paragraphs)
            {
                foreach (var portion in paragraph.Portions)
                {
                    if (portion.Text.Contains(searchText))
                    {
                        portion.Text = portion.Text.Replace(
                            searchText, 
                            replacementText);
                    }
                }
            }
        }
    }
}
```

### Working with Images

```csharp
// Add image from file
using var image = Image.FromFile("logo.png");
var ppImage = presentation.Images.AddImage(image);

var pictureFrame = slide.Shapes.AddPictureFrame(
    ShapeType.Rectangle,
    x: 100,
    y: 100,
    width: 200,
    height: 150,
    ppImage);

// Extract all images from presentation
var imageIndex = 0;
foreach (var slide in presentation.Slides)
{
    foreach (var shape in slide.Shapes.OfType<IPictureFrame>())
    {
        var image = shape.PictureFormat.Picture.Image.SystemImage;
        image.Save($"extracted_image_{imageIndex++}.png");
    }
}
```

## JSON Data Population Pattern

For data-driven presentations, use a declarative approach:

```csharp
public class SlideDataModel
{
    public string Title { get; set; }
    public List<BulletPoint> BulletPoints { get; set; }
    public TableData TableData { get; set; }
    public ChartData ChartData { get; set; }
}

void PopulateSlideFromJson(ISlide slide, SlideDataModel data)
{
    // Update title
    var titleShape = slide.Shapes
        .OfType<IAutoShape>()
        .FirstOrDefault(s => s.Placeholder?.Type == PlaceholderType.Title);
    
    if (titleShape != null && data.Title != null)
    {
        titleShape.TextFrame.Text = data.Title;
    }

    // Update bullet points
    var bodyShape = slide.Shapes
        .OfType<IAutoShape>()
        .FirstOrDefault(s => s.Placeholder?.Type == PlaceholderType.Body);
    
    if (bodyShape != null && data.BulletPoints != null)
    {
        bodyShape.TextFrame.Paragraphs.Clear();
        
        foreach (var bullet in data.BulletPoints)
        {
            var paragraph = new Paragraph();
            paragraph.Text = bullet.Text;
            paragraph.ParagraphFormat.Bullet.Type = BulletType.Symbol;
            bodyShape.TextFrame.Paragraphs.Add(paragraph);
        }
    }

    // Populate table if present
    if (data.TableData != null)
    {
        PopulateTable(slide, data.TableData);
    }

    // Populate chart if present
    if (data.ChartData != null)
    {
        PopulateChart(slide, data.ChartData);
    }
}
```

## Performance Considerations

### Memory Management for Large Presentations

```csharp
// Use BlobManagementOptions for large presentations
var blobOptions = new BlobManagementOptions
{
    PresentationLockingBehavior = PresentationLockingBehavior.KeepLocked,
    IsTemporaryFilesAllowed = true,
    TempFilesRootPath = Path.GetTempPath()
};

var loadOptions = new LoadOptions { BlobManagementOptions = blobOptions };
using var presentation = new Presentation("large.pptx", loadOptions);
```

### Efficient Batch Processing

```csharp
async Task ProcessPresentationsAsync(IEnumerable<string> files)
{
    var processingTasks = files.Select(async file =>
    {
        using var presentation = new Presentation(file);
        
        // Process presentation
        await Task.Run(() => ProcessSlides(presentation));
        
        var outputPath = Path.ChangeExtension(file, ".processed.pptx");
        presentation.Save(outputPath, SaveFormat.Pptx);
    });

    await Task.WhenAll(processingTasks);
}
```

## Error Handling Patterns

### Robust Presentation Processing

```csharp
Result<Presentation> LoadPresentationSafely(string path)
{
    try
    {
        var presentation = new Presentation(path);
        return Result<Presentation>.Success(presentation);
    }
    catch (Exception ex) when (ex is InvalidOperationException or IOException)
    {
        return Result<Presentation>.Failure($"Failed to load presentation: {ex.Message}");
    }
}

// Usage with pattern matching
var result = LoadPresentationSafely("presentation.pptx");

result switch
{
    { IsSuccess: true } => ProcessPresentation(result.Value),
    { IsSuccess: false } => LogError(result.Error)
};
```

## Export and Conversion

### PDF Export with Options

```csharp
var pdfOptions = new PdfOptions
{
    Compliance = PdfCompliance.Pdf15,
    JpegQuality = 90,
    TextCompression = PdfTextCompression.Flate,
    EmbedFullFonts = true,
    DrawSlidesFrame = false
};

// Include notes in PDF
pdfOptions.NotesCommentsLayouting.NotesPosition = NotesPositions.BottomFull;

presentation.Save("output.pdf", SaveFormat.Pdf, pdfOptions);
```

### HTML Export

```csharp
var htmlOptions = new HtmlOptions
{
    EmbedImages = true,
    HtmlFormatter = HtmlFormatter.CreateDocumentFormatter(string.Empty, false)
};

presentation.Save("output.html", SaveFormat.Html, htmlOptions);
```

### Image Export for Each Slide

```csharp
foreach (var slide in presentation.Slides)
{
    using var bitmap = slide.GetThumbnail(2.0f, 2.0f); // 2x scale
    bitmap.Save(
        $"slide_{slide.SlideNumber}.png", 
        System.Drawing.Imaging.ImageFormat.Png);
}
```

## Best Practices

### 1. Fitness for Purpose
- Use templates when possible to maintain consistent design
- Prefer placeholder manipulation over direct shape creation
- Consider export format requirements when designing slides
- Balance visual quality with file size constraints

### 2. Declarative Configuration
- Extract repeated configuration into helper methods
- Use object initializers and collection initializers
- Leverage LINQ for collection transformations
- Prefer expression-bodied members for simple operations

### 3. Type Safety
- Use strongly-typed enumerations (ShapeType, PlaceholderType, etc.)
- Avoid magic numbers and strings
- Create domain-specific value objects for measurements
- Use records for immutable data transfer objects

### 4. Maintainability
- Separate data from presentation logic
- Create reusable components for common slide patterns
- Use consistent naming conventions for shapes
- Document complex shape hierarchies

### 5. Testing
- Create minimal test presentations for validation
- Use presentation properties to verify changes
- Extract testable pure functions
- Consider round-trip testing (save/load/verify)

## Troubleshooting Common Issues

### Issue: Shape positioning inconsistent
**Solution**: Use slide dimensions as reference
```csharp
var slideWidth = presentation.SlideSize.Size.Width;
var slideHeight = presentation.SlideSize.Size.Height;

// Center shape
var shape = slide.Shapes.AddAutoShape(
    ShapeType.Rectangle,
    x: (slideWidth - shapeWidth) / 2,
    y: (slideHeight - shapeHeight) / 2,
    width: shapeWidth,
    height: shapeHeight);
```

### Issue: Text overflow in shapes
**Solution**: Enable auto-fit or adjust shape size
```csharp
var textFrame = shape.TextFrame;
textFrame.TextFrameFormat.AutofitType = TextAutofitType.Shape;
// or
textFrame.TextFrameFormat.AutofitType = TextAutofitType.Normal;
```

### Issue: Font not embedded
**Solution**: Embed fonts explicitly
```csharp
var fontData = File.ReadAllBytes("customfont.ttf");
presentation.FontsManager.AddEmbeddedFont(fontData, EmbedFontCharacters.All);
```

### Issue: Chart data not updating
**Solution**: Refresh chart data workbook
```csharp
chart.ChartData.ChartDataWorkbook.Clear(0);
// Re-populate data
```

## Resource Discovery Strategy

When implementing Aspose.Slides functionality:

1. **Check the namespace hierarchy** - Aspose.Slides types are organized logically by domain
2. **Explore interface contracts** - Most functionality is exposed through interfaces (IPresentation, ISlide, etc.)
3. **Review enumerations** - Aspose uses comprehensive enums for options and types
4. **Consult XML documentation** - IntelliSense provides detailed API documentation
5. **Reference GitHub examples** - Real-world usage patterns for specific scenarios
6. **Leverage type inference** - Let the compiler guide you through valid operations

## Example-Driven Development

Start with the desired outcome and work backward:

```csharp
// Goal: Create a data-driven presentation from JSON

// 1. Define the data structure
var slideData = JsonSerializer.Deserialize<PresentationData>(jsonContent);

// 2. Load or create presentation
using var presentation = LoadTemplate("template.pptx") 
    ?? CreateNewPresentation();

// 3. Apply data to slides
foreach (var (slide, data) in presentation.Slides.Zip(slideData.Slides))
{
    ApplyDataToSlide(slide, data);
}

// 4. Save with appropriate options
SavePresentation(presentation, "output.pptx", slideData.ExportOptions);
```

## Summary

This skill enables Claude Code to manipulate PowerPoint presentations using modern C# patterns with Aspose.Slides. Focus on:
- Declarative, functional approaches to slide manipulation
- Proper resource management with `using` statements
- Type-safe operations using the comprehensive object model
- Data-driven presentation generation
- Efficient processing of large presentations

When tackling a new task, understand the object hierarchy, leverage LINQ for collection operations, and prefer composition over complex imperative code.
