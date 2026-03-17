---
name: creating-wpf-flowdocument
description: Creates WPF FlowDocument for rich text display with Paragraph, Table, List elements. Use when building document viewers, rich text editors, or printable reports.
---

# WPF FlowDocument Patterns

Creating rich, paginated documents with flowing text content.

**Advanced Patterns:** See [ADVANCED.md](ADVANCED.md) for programmatic creation, printing, and file I/O.

## 1. FlowDocument Overview

```
FlowDocument
├── Block Elements (Paragraph, Section, List, Table, BlockUIContainer)
│   └── Inline Elements (Run, Bold, Italic, Hyperlink, InlineUIContainer)
├── Viewers
│   ├── FlowDocumentScrollViewer (continuous scroll)
│   ├── FlowDocumentPageViewer (page by page)
│   └── FlowDocumentReader (multiple viewing modes)
└── Features
    ├── Automatic pagination
    ├── Column layout
    ├── Figure/Floater positioning
    └── Print support
```

---

## 2. Basic FlowDocument

### 2.1 Simple Document

```xml
<FlowDocumentScrollViewer>
    <FlowDocument FontFamily="Segoe UI" FontSize="14">
        <Paragraph FontSize="24" FontWeight="Bold">
            Document Title
        </Paragraph>
        <Paragraph>
            This is a paragraph with <Bold>bold</Bold>,
            <Italic>italic</Italic>, and
            <Underline>underlined</Underline> text.
        </Paragraph>
        <Paragraph TextAlignment="Justify">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        </Paragraph>
    </FlowDocument>
</FlowDocumentScrollViewer>
```

### 2.2 Document Properties

```xml
<FlowDocument
    FontFamily="Georgia"
    FontSize="14"
    PageWidth="800"
    PageHeight="1100"
    PagePadding="50"
    ColumnWidth="350"
    ColumnGap="20"
    IsColumnWidthFlexible="True"
    IsOptimalParagraphEnabled="True"
    IsHyphenationEnabled="True">
    <!-- Content -->
</FlowDocument>
```

---

## 3. Block Elements

### 3.1 Paragraph

```xml
<Paragraph TextAlignment="Left"
           TextIndent="20"
           LineHeight="24"
           Margin="0,10,0,10">
    Regular paragraph text with indentation.
</Paragraph>

<Paragraph Background="#F0F0F0" Padding="10">
    Highlighted paragraph with background.
</Paragraph>
```

### 3.2 Section (Grouping)

```xml
<Section FontSize="12" Foreground="DarkGray">
    <Paragraph>First paragraph in section.</Paragraph>
    <Paragraph>Second paragraph in section.</Paragraph>
    <Paragraph>All paragraphs inherit section styling.</Paragraph>
</Section>
```

### 3.3 List

```xml
<!-- Bulleted list -->
<List MarkerStyle="Disc">
    <ListItem>
        <Paragraph>First item</Paragraph>
    </ListItem>
    <ListItem>
        <Paragraph>Second item</Paragraph>
        <List MarkerStyle="Circle">
            <ListItem><Paragraph>Nested item 1</Paragraph></ListItem>
            <ListItem><Paragraph>Nested item 2</Paragraph></ListItem>
        </List>
    </ListItem>
</List>

<!-- Numbered list -->
<List MarkerStyle="Decimal" StartIndex="1">
    <ListItem><Paragraph>Step one</Paragraph></ListItem>
    <ListItem><Paragraph>Step two</Paragraph></ListItem>
</List>
```

**MarkerStyle Options:** None, Disc, Circle, Square, Box, LowerRoman, UpperRoman, LowerLatin, UpperLatin, Decimal

### 3.4 Table

```xml
<Table CellSpacing="0">
    <Table.Columns>
        <TableColumn Width="100"/>
        <TableColumn Width="200"/>
        <TableColumn Width="100"/>
    </Table.Columns>

    <!-- Header row -->
    <TableRowGroup Background="#E0E0E0">
        <TableRow>
            <TableCell><Paragraph FontWeight="Bold">Name</Paragraph></TableCell>
            <TableCell><Paragraph FontWeight="Bold">Description</Paragraph></TableCell>
            <TableCell><Paragraph FontWeight="Bold">Price</Paragraph></TableCell>
        </TableRow>
    </TableRowGroup>

    <!-- Data rows -->
    <TableRowGroup>
        <TableRow>
            <TableCell><Paragraph>Item 1</Paragraph></TableCell>
            <TableCell><Paragraph>Description of item 1</Paragraph></TableCell>
            <TableCell><Paragraph>$10.00</Paragraph></TableCell>
        </TableRow>
    </TableRowGroup>
</Table>
```

### 3.5 BlockUIContainer (Embedding UI)

```xml
<BlockUIContainer>
    <Image Source="/Images/diagram.png" Width="400" Stretch="Uniform"/>
</BlockUIContainer>

<BlockUIContainer>
    <Button Content="Click Me" Width="100" Height="30"/>
</BlockUIContainer>
```

---

## 4. Inline Elements

### 4.1 Text Formatting

```xml
<Paragraph>
    <Run>Normal text</Run>
    <Bold>Bold text</Bold>
    <Italic>Italic text</Italic>
    <Underline>Underlined text</Underline>
    <Run FontFamily="Consolas" Background="#F0F0F0">Code text</Run>
    <Run Foreground="Red">Colored text</Run>
    <Span BaselineAlignment="Superscript" FontSize="10">superscript</Span>
</Paragraph>
```

### 4.2 Hyperlink

```xml
<Paragraph>
    Visit <Hyperlink NavigateUri="https://example.com"
                     RequestNavigate="Hyperlink_RequestNavigate">
        Example.com
    </Hyperlink> for more info.
</Paragraph>
```

```csharp
private void Hyperlink_RequestNavigate(object sender, RequestNavigateEventArgs e)
{
    System.Diagnostics.Process.Start(new ProcessStartInfo
    {
        FileName = e.Uri.AbsoluteUri,
        UseShellExecute = true
    });
    e.Handled = true;
}
```

### 4.3 InlineUIContainer

```xml
<Paragraph>
    Status:
    <InlineUIContainer>
        <Ellipse Width="12" Height="12" Fill="Green"/>
    </InlineUIContainer>
    Online
</Paragraph>
```

---

## 5. Figures and Floaters

### 5.1 Figure (Positioned Content)

```xml
<Paragraph>
    <Figure HorizontalAnchor="PageRight"
            VerticalAnchor="PageTop"
            Width="200"
            Padding="10"
            BorderBrush="Gray"
            BorderThickness="1">
        <Paragraph FontStyle="Italic">
            This figure appears at the top-right of the page.
        </Paragraph>
    </Figure>
    Main document text continues here...
</Paragraph>
```

**HorizontalAnchor:** ContentLeft, ContentCenter, ContentRight, PageLeft, PageCenter, PageRight

**VerticalAnchor:** PageTop, PageCenter, PageBottom, ContentTop, ContentCenter, ContentBottom

### 5.2 Floater (Floating Content)

```xml
<Paragraph>
    <Floater HorizontalAlignment="Right" Width="150">
        <Paragraph Background="#F0F8FF" Padding="10">
            This floater appears inline and text wraps around it.
        </Paragraph>
    </Floater>
    Main paragraph text that wraps around the floater content...
</Paragraph>
```

---

## 6. Document Viewers

### 6.1 FlowDocumentScrollViewer

```xml
<!-- Continuous scroll, single page -->
<FlowDocumentScrollViewer VerticalScrollBarVisibility="Auto" IsToolBarVisible="True">
    <FlowDocument><!-- Content --></FlowDocument>
</FlowDocumentScrollViewer>
```

### 6.2 FlowDocumentPageViewer

```xml
<!-- Page by page viewing -->
<FlowDocumentPageViewer>
    <FlowDocument><!-- Content --></FlowDocument>
</FlowDocumentPageViewer>
```

### 6.3 FlowDocumentReader

```xml
<!-- Multiple viewing modes (Page, TwoPage, Scroll) -->
<FlowDocumentReader ViewingMode="TwoPage" IsFindEnabled="True" IsPrintEnabled="True">
    <FlowDocument><!-- Content --></FlowDocument>
</FlowDocumentReader>
```

---

## 7. References

- [FlowDocument Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/flow-document-overview)
- [Flow Content Elements - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/flow-content-elements-how-to-topics)
- [Documents in WPF - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/documents-in-wpf)
