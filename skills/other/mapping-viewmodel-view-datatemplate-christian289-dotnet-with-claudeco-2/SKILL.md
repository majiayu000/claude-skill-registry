---
name: mapping-viewmodel-view-datatemplate
description: "Implements automatic ViewModel-View mapping using DataTemplate for navigation scenarios. Use when building dynamic content display or implementing navigation between views in WPF."
---

# 5.8 Automatic View-ViewModel Mapping Using DataTemplate

In WPF, DataTemplate allows automatic mapping between ViewModel types and Views. This pattern is very useful for navigation scenarios and dynamic content display.

## Project Structure

The templates folder contains a WPF project example (use latest .NET per version mapping).

```
templates/
├── WpfDataTemplateSample.App/           ← WPF Application Project
│   ├── Views/
│   │   ├── HomeView.xaml
│   │   ├── HomeView.xaml.cs
│   │   ├── SettingsView.xaml
│   │   └── SettingsView.xaml.cs
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── MainWindow.xaml
│   ├── MainWindow.xaml.cs
│   ├── Mappings.xaml                    ← DataTemplate mapping definitions
│   ├── GlobalUsings.cs
│   └── WpfDataTemplateSample.App.csproj
└── WpfDataTemplateSample.ViewModels/    ← ViewModel Class Library
    ├── MainWindowViewModel.cs
    ├── HomeViewModel.cs
    ├── SettingsViewModel.cs
    ├── GlobalUsings.cs
    └── WpfDataTemplateSample.ViewModels.csproj
```

#### 5.8.1 Core Concept

**When you bind a ViewModel instance to ContentControl's Content, WPF automatically finds the corresponding DataTemplate for that ViewModel type and renders the View.**

Key points of this pattern:
1. Define DataTemplates for each ViewModel type in `Mappings.xaml`
2. Bind ViewModel instances to `ContentControl.Content`
3. WPF automatically matches types and renders the corresponding View

#### 5.8.2 Mappings.xaml Pattern

**Mappings.xaml - Define ViewModel and View mappings:**

```xml
<!-- Mappings.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:viewmodels="clr-namespace:WpfDataTemplateSample.ViewModels"
                    xmlns:views="clr-namespace:WpfDataTemplateSample.Views">

    <!--  DataTemplate definitions that automatically map ViewModel to View  -->
    <!--  Setting ViewModel to ContentControl's Content automatically renders the corresponding View  -->

    <DataTemplate DataType="{x:Type viewmodels:HomeViewModel}">
        <views:HomeView />
    </DataTemplate>

    <DataTemplate DataType="{x:Type viewmodels:SettingsViewModel}">
        <views:SettingsView />
    </DataTemplate>

    <DataTemplate DataType="{x:Type viewmodels:UserProfileViewModel}">
        <views:UserProfileView />
    </DataTemplate>

</ResourceDictionary>
```

**App.xaml - Merge Mappings.xaml into Application Resources:**

```xml
<!-- App.xaml -->
<Application x:Class="WpfDataTemplateSample.App"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             StartupUri="MainWindow.xaml">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <ResourceDictionary Source="Mappings.xaml" />
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
```

#### 5.8.3 Navigation Pattern Implementation

**MainWindowViewModel - Screen navigation via CurrentViewModel property:**

```csharp
// ViewModels/MainWindowViewModel.cs
namespace WpfDataTemplateSample.ViewModels;

public sealed partial class MainWindowViewModel : ObservableObject
{
    [ObservableProperty] private object? _currentViewModel;

    public MainWindowViewModel()
    {
        CurrentViewModel = new HomeViewModel();
    }

    [RelayCommand]
    private void NavigateToHome()
    {
        CurrentViewModel = new HomeViewModel();
    }

    [RelayCommand]
    private void NavigateToSettings()
    {
        CurrentViewModel = new SettingsViewModel();
    }

    [RelayCommand]
    private void NavigateToUserProfile()
    {
        CurrentViewModel = new UserProfileViewModel();
    }
}
```

**MainWindow.xaml - Display dynamic content with ContentControl:**

```xml
<!-- MainWindow.xaml -->
<Window x:Class="WpfDataTemplateSample.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:viewmodels="clr-namespace:WpfDataTemplateSample.ViewModels"
        Title="DataTemplate Auto-Mapping Sample"
        Width="800"
        Height="500"
        WindowStartupLocation="CenterScreen">

    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
        </Grid.RowDefinitions>

        <!--  Navigation button area  -->
        <StackPanel Grid.Row="0"
                    Margin="10"
                    HorizontalAlignment="Center"
                    Orientation="Horizontal">
            <Button Width="100"
                    Height="35"
                    Margin="5"
                    Command="{Binding NavigateToHomeCommand}"
                    Content="Home" />
            <Button Width="100"
                    Height="35"
                    Margin="5"
                    Command="{Binding NavigateToSettingsCommand}"
                    Content="Settings" />
            <Button Width="100"
                    Height="35"
                    Margin="5"
                    Command="{Binding NavigateToUserProfileCommand}"
                    Content="User Profile" />
        </StackPanel>

        <!--  Binding ViewModel to ContentControl renders the View automatically via DataTemplate in Mappings.xaml  -->
        <!--  Key point: Setting a ViewModel type to Content automatically displays the corresponding View  -->
        <Border Grid.Row="1"
                Margin="10"
                BorderBrush="Gray"
                BorderThickness="1">
            <ContentControl Content="{Binding CurrentViewModel}" />
        </Border>

    </Grid>
</Window>
```

```csharp
// MainWindow.xaml.cs
using WpfDataTemplateSample.ViewModels;

namespace WpfDataTemplateSample;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        DataContext = new MainWindowViewModel();
    }
}
```

#### 5.8.4 ViewModel and View Implementation Examples

**HomeViewModel:**

```csharp
// ViewModels/HomeViewModel.cs
namespace WpfDataTemplateSample.ViewModels;

public sealed partial class HomeViewModel : ObservableObject
{
    [ObservableProperty] private string _welcomeMessage = "Welcome to Home Page!";
    [ObservableProperty] private string _description = "This is the home page content. DataTemplate automatically maps this ViewModel to HomeView.";
}
```

**HomeView:**

```xml
<!-- Views/HomeView.xaml -->
<UserControl x:Class="WpfDataTemplateSample.Views.HomeView"
             xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
             xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
             xmlns:viewmodels="clr-namespace:WpfDataTemplateSample.ViewModels"
             d:DataContext="{d:DesignInstance Type=viewmodels:HomeViewModel}">

    <Grid Background="#F0F8FF">
        <StackPanel HorizontalAlignment="Center"
                    VerticalAlignment="Center">
            <TextBlock Margin="0,0,0,20"
                       HorizontalAlignment="Center"
                       FontSize="32"
                       FontWeight="Bold"
                       Foreground="#2C3E50"
                       Text="{Binding WelcomeMessage}" />

            <Border MaxWidth="600"
                    Padding="30"
                    Background="White"
                    BorderBrush="#3498DB"
                    BorderThickness="2"
                    CornerRadius="10">
                <TextBlock FontSize="16"
                           Foreground="#34495E"
                           LineHeight="24"
                           Text="{Binding Description}"
                           TextAlignment="Center"
                           TextWrapping="Wrap" />
            </Border>
        </StackPanel>
    </Grid>
</UserControl>
```

```csharp
// Views/HomeView.xaml.cs
namespace WpfDataTemplateSample.Views;

public partial class HomeView : UserControl
{
    public HomeView()
    {
        InitializeComponent();
    }
}
```

#### 5.8.5 Core Principles

1. **DataTemplate's DataType attribute**: Specifies ViewModel type for automatic mapping
2. **Define without x:Key**: When only DataType is specified, WPF automatically searches by type
3. **Use ContentControl**: Bind ViewModel instance to the Content property
4. **Register in Application Resources**: Merge Mappings.xaml via MergedDictionaries in App.xaml
5. **Views as UserControls**: Define Views as reusable UserControls

#### 5.8.6 Advantages

1. **Reduced View-ViewModel coupling**: No direct View creation in Code-Behind
2. **Declarative mapping**: Explicitly define mapping relationships in XAML
3. **Simplified navigation**: Automatic screen transitions by simply replacing ViewModel instances
4. **Testability**: Logic can be tested with ViewModel alone
5. **Design-time support**: Designer preview support via `d:DataContext`

#### 5.8.7 Important Notes

**⚠️ Important:**
- DataTemplate must be defined without `x:Key` for automatic mapping to work
- Mappings.xaml must be merged into Application.Resources
- ViewModel types must match exactly (inheritance relationships are not considered)
- Bind ViewModel instances (not types) to ContentControl.Content
- Views automatically receive DataContext (no separate configuration needed)

#### 5.8.8 Project Structure Example

```
WpfDataTemplateSample/
├── ViewModels/
│   ├── MainWindowViewModel.cs
│   ├── HomeViewModel.cs
│   ├── SettingsViewModel.cs
│   └── UserProfileViewModel.cs
├── Views/
│   ├── HomeView.xaml
│   ├── HomeView.xaml.cs
│   ├── SettingsView.xaml
│   ├── SettingsView.xaml.cs
│   ├── UserProfileView.xaml
│   └── UserProfileView.xaml.cs
├── App.xaml
├── App.xaml.cs
├── MainWindow.xaml
├── MainWindow.xaml.cs
├── Mappings.xaml              ← DataTemplate mapping definitions
└── GlobalUsings.cs
```

---

#### 5.8.9 HierarchicalDataTemplate for TreeView

For hierarchical data structures (e.g., folder trees, organization charts), use `HierarchicalDataTemplate`.

**ViewModel with Hierarchical Data:**

```csharp
// ViewModels/FolderViewModel.cs
namespace MyApp.ViewModels;

public sealed partial class FolderViewModel : ObservableObject
{
    [ObservableProperty] private string _name = string.Empty;
    [ObservableProperty] private ObservableCollection<FolderViewModel> _children = [];
    [ObservableProperty] private bool _isExpanded;
    [ObservableProperty] private bool _isSelected;

    public FolderViewModel(string name)
    {
        Name = name;
    }

    public FolderViewModel(string name, IEnumerable<FolderViewModel> children)
        : this(name)
    {
        foreach (var child in children)
        {
            Children.Add(child);
        }
    }
}
```

**HierarchicalDataTemplate in XAML:**

```xml
<!-- Mappings.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:viewmodels="clr-namespace:MyApp.ViewModels">

    <!-- HierarchicalDataTemplate for recursive tree structure -->
    <HierarchicalDataTemplate DataType="{x:Type viewmodels:FolderViewModel}"
                              ItemsSource="{Binding Children}">
        <StackPanel Orientation="Horizontal">
            <Image Source="/Icons/folder.png" Width="16" Height="16" Margin="0,0,5,0"/>
            <TextBlock Text="{Binding Name}" VerticalAlignment="Center"/>
        </StackPanel>
    </HierarchicalDataTemplate>

</ResourceDictionary>
```

**TreeView Usage:**

```xml
<TreeView ItemsSource="{Binding RootFolders}">
    <!-- HierarchicalDataTemplate from resources is automatically applied -->
    <TreeView.ItemContainerStyle>
        <Style TargetType="{x:Type TreeViewItem}">
            <Setter Property="IsExpanded" Value="{Binding IsExpanded, Mode=TwoWay}"/>
            <Setter Property="IsSelected" Value="{Binding IsSelected, Mode=TwoWay}"/>
        </Style>
    </TreeView.ItemContainerStyle>
</TreeView>
```

**Multiple ViewModel Types in Tree:**

```xml
<!-- Different templates for different node types -->
<HierarchicalDataTemplate DataType="{x:Type viewmodels:FolderViewModel}"
                          ItemsSource="{Binding Children}">
    <StackPanel Orientation="Horizontal">
        <Image Source="/Icons/folder.png" Width="16" Height="16"/>
        <TextBlock Text="{Binding Name}" Margin="5,0"/>
    </StackPanel>
</HierarchicalDataTemplate>

<DataTemplate DataType="{x:Type viewmodels:FileViewModel}">
    <StackPanel Orientation="Horizontal">
        <Image Source="/Icons/file.png" Width="16" Height="16"/>
        <TextBlock Text="{Binding FileName}" Margin="5,0"/>
    </StackPanel>
</DataTemplate>
```

**Key Differences:**

| DataTemplate | HierarchicalDataTemplate |
|--------------|-------------------------|
| Flat data | Hierarchical/nested data |
| No children | Has ItemsSource for children |
| ContentControl | TreeView, Menu, MenuItem |

---

