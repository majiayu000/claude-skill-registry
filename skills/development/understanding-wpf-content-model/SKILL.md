---
name: understanding-wpf-content-model
description: "Explains WPF content model hierarchy including ContentControl, ItemsControl, and Headered variants. Use when selecting base classes for custom controls or understanding content/items properties."
---

# WPF Content Model Patterns

WPF controls are classified into 4 main models based on how they contain content.

## 1. Content Model Hierarchy

```
Control
├── ContentControl          (Single Content)
│   ├── Button
│   ├── Label
│   ├── CheckBox
│   ├── RadioButton
│   ├── ToolTip
│   ├── ScrollViewer
│   ├── UserControl
│   ├── Window
│   └── HeaderedContentControl  (Content + Header)
│       ├── Expander
│       ├── GroupBox
│       └── TabItem
│
└── ItemsControl            (Multiple Items)
    ├── ListBox
    ├── ComboBox
    ├── ListView
    ├── TreeView
    ├── Menu
    ├── TabControl
    └── HeaderedItemsControl    (Items + Header)
        ├── MenuItem
        ├── TreeViewItem
        └── ToolBar
```

---

## 2. ContentControl

### 2.1 Characteristics

- **Single Content property**: Holds only one child element
- **Content type**: object (allows all types)
- **ContentTemplate**: Specifies how Content is rendered

### 2.2 Basic Usage

```xml
<!-- String content -->
<Button Content="Click Me"/>

<!-- Complex content -->
<Button>
    <StackPanel Orientation="Horizontal">
        <Image Source="/icon.png" Width="16"/>
        <TextBlock Text="Save" Margin="5,0,0,0"/>
    </StackPanel>
</Button>
```

### 2.3 Using ContentTemplate

```xml
<Button Content="Download">
    <Button.ContentTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <Path Data="M12,2L12,14L8,10L12,14L16,10L12,14"
                      Fill="White" Width="16"/>
                <TextBlock Text="{Binding}" Margin="5,0,0,0"/>
            </StackPanel>
        </DataTemplate>
    </Button.ContentTemplate>
</Button>
```

### 2.4 Creating ContentControl-Derived Controls

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;

/// <summary>
/// Card control that displays single content
/// </summary>
public sealed class CardControl : ContentControl
{
    static CardControl()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof(CardControl),
            new FrameworkPropertyMetadata(typeof(CardControl)));
    }

    public static readonly DependencyProperty CornerRadiusProperty =
        DependencyProperty.Register(
            nameof(CornerRadius),
            typeof(CornerRadius),
            typeof(CardControl),
            new PropertyMetadata(new CornerRadius(8)));

    public CornerRadius CornerRadius
    {
        get => (CornerRadius)GetValue(CornerRadiusProperty);
        set => SetValue(CornerRadiusProperty, value);
    }
}
```

---

## 3. ItemsControl

### 3.1 Characteristics

- **Items collection**: Holds multiple child elements
- **ItemsSource**: Source for data binding
- **ItemTemplate**: Rendering method for each item
- **ItemsPanel**: Specifies the panel for item layout

### 3.2 Basic Usage

```xml
<!-- Direct item addition -->
<ListBox>
    <ListBoxItem Content="Item 1"/>
    <ListBoxItem Content="Item 2"/>
    <ListBoxItem Content="Item 3"/>
</ListBox>

<!-- Data binding -->
<ListBox ItemsSource="{Binding Products}">
    <ListBox.ItemTemplate>
        <DataTemplate>
            <StackPanel>
                <TextBlock Text="{Binding Name}" FontWeight="Bold"/>
                <TextBlock Text="{Binding Price, StringFormat=${0:N2}}"/>
            </StackPanel>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

### 3.3 Customizing ItemsPanel

```xml
<!-- Horizontal list layout -->
<ListBox ItemsSource="{Binding Items}">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <StackPanel Orientation="Horizontal"/>
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
</ListBox>

<!-- Grid layout -->
<ItemsControl ItemsSource="{Binding Items}">
    <ItemsControl.ItemsPanel>
        <ItemsPanelTemplate>
            <WrapPanel/>
        </ItemsPanelTemplate>
    </ItemsControl.ItemsPanel>
</ItemsControl>

<!-- Virtualized panel (large data) -->
<ListBox ItemsSource="{Binding LargeCollection}"
         VirtualizingPanel.IsVirtualizing="True"
         VirtualizingPanel.VirtualizationMode="Recycling">
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <VirtualizingStackPanel/>
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
</ListBox>
```

### 3.4 Creating ItemsControl-Derived Controls

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;

/// <summary>
/// Control that displays a list of tags
/// </summary>
public sealed class TagListControl : ItemsControl
{
    static TagListControl()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof(TagListControl),
            new FrameworkPropertyMetadata(typeof(TagListControl)));
    }

    protected override DependencyObject GetContainerForItemOverride()
    {
        // Specify container that wraps each item
        return new TagItem();
    }

    protected override bool IsItemItsOwnContainerOverride(object item)
    {
        return item is TagItem;
    }
}

public sealed class TagItem : ContentControl
{
    static TagItem()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof(TagItem),
            new FrameworkPropertyMetadata(typeof(TagItem)));
    }
}
```

---

## 4. HeaderedContentControl

### 4.1 Characteristics

- **Header + Content**: Two separate regions
- **HeaderTemplate**: Header rendering method
- **ContentTemplate**: Content rendering method

### 4.2 Representative Controls

```xml
<!-- GroupBox -->
<GroupBox Header="Settings">
    <StackPanel>
        <CheckBox Content="Option 1"/>
        <CheckBox Content="Option 2"/>
    </StackPanel>
</GroupBox>

<!-- Expander -->
<Expander Header="Details" IsExpanded="False">
    <TextBlock Text="Content not visible when collapsed"/>
</Expander>

<!-- TabItem -->
<TabControl>
    <TabItem Header="Tab 1">
        <TextBlock Text="Tab 1 content"/>
    </TabItem>
    <TabItem>
        <TabItem.Header>
            <StackPanel Orientation="Horizontal">
                <Ellipse Width="8" Height="8" Fill="Green"/>
                <TextBlock Text="Status" Margin="5,0,0,0"/>
            </StackPanel>
        </TabItem.Header>
        <TextBlock Text="Tab 2 content"/>
    </TabItem>
</TabControl>
```

### 4.3 Creating HeaderedContentControl-Derived Controls

```csharp
namespace MyApp.Controls;

using System.Windows;
using System.Windows.Controls;

/// <summary>
/// Collapsible section control
/// </summary>
public sealed class CollapsibleSection : HeaderedContentControl
{
    static CollapsibleSection()
    {
        DefaultStyleKeyProperty.OverrideMetadata(
            typeof(CollapsibleSection),
            new FrameworkPropertyMetadata(typeof(CollapsibleSection)));
    }

    public static readonly DependencyProperty IsExpandedProperty =
        DependencyProperty.Register(
            nameof(IsExpanded),
            typeof(bool),
            typeof(CollapsibleSection),
            new PropertyMetadata(true));

    public bool IsExpanded
    {
        get => (bool)GetValue(IsExpandedProperty);
        set => SetValue(IsExpandedProperty, value);
    }
}
```

---

## 5. HeaderedItemsControl

### 5.1 Characteristics

- **Header + Items**: Header and multiple items
- Suitable for representing **hierarchical structures**

### 5.2 Representative Controls

```xml
<!-- TreeViewItem -->
<TreeView>
    <TreeViewItem Header="Folder 1">
        <TreeViewItem Header="File 1.txt"/>
        <TreeViewItem Header="File 2.txt"/>
        <TreeViewItem Header="Subfolder">
            <TreeViewItem Header="File 3.txt"/>
        </TreeViewItem>
    </TreeViewItem>
</TreeView>

<!-- MenuItem -->
<Menu>
    <MenuItem Header="File">
        <MenuItem Header="New"/>
        <MenuItem Header="Open"/>
        <Separator/>
        <MenuItem Header="Recent Files">
            <MenuItem Header="file1.txt"/>
            <MenuItem Header="file2.txt"/>
        </MenuItem>
    </MenuItem>
</Menu>
```

### 5.3 HierarchicalDataTemplate (Hierarchical Data Binding)

```xml
<TreeView ItemsSource="{Binding RootNodes}">
    <TreeView.ItemTemplate>
        <HierarchicalDataTemplate ItemsSource="{Binding Children}">
            <StackPanel Orientation="Horizontal">
                <Image Source="{Binding Icon}" Width="16"/>
                <TextBlock Text="{Binding Name}" Margin="5,0,0,0"/>
            </StackPanel>
        </HierarchicalDataTemplate>
    </TreeView.ItemTemplate>
</TreeView>
```

---

## 6. Control Selection Guide

| Scenario | Recommended Base Class |
|----------|------------------------|
| Display single content | ContentControl |
| Single content + title | HeaderedContentControl |
| Display list/collection | ItemsControl |
| Selectable list | Selector (ListBox, ComboBox) |
| Hierarchical data | HeaderedItemsControl |
| Input field | TextBoxBase |
| Range value selection | RangeBase |

---

## 7. Content Property Processing Flow

```
Content Set
    ↓
ContentTemplate exists?
    ├── Yes → Render with DataTemplate
    └── No → Check Content type
                ├── UIElement → Render directly
                ├── String → Render with TextBlock
                └── Other → ToString() then TextBlock
```

---

## 8. References

- [WPF Content Model - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/wpf-content-model)
- [ItemsControl Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.windows.controls.itemscontrol)
