---
name: managing-wpf-collectionview-mvvm
description: "Encapsulates CollectionView in Service Layer to maintain MVVM principles in WPF. Use when implementing filtering, sorting, or grouping while keeping ViewModels free of WPF dependencies."
---

# 5.6 MVVM Pattern with CollectionView

## Project Structure

The templates folder contains a WPF project example (use latest .NET per version mapping).

```
templates/
├── WpfCollectionViewSample.Core/           ← Pure C# models and interfaces
│   ├── Member.cs
│   ├── IMemberCollectionService.cs
│   └── WpfCollectionViewSample.Core.csproj
├── WpfCollectionViewSample.ViewModels/     ← ViewModel (no WPF references)
│   ├── MainViewModel.cs
│   ├── GlobalUsings.cs
│   └── WpfCollectionViewSample.ViewModels.csproj
├── WpfCollectionViewSample.WpfServices/    ← WPF Service Layer
│   ├── MemberCollectionService.cs
│   ├── GlobalUsings.cs
│   └── WpfCollectionViewSample.WpfServices.csproj
└── WpfCollectionViewSample.App/            ← WPF Application
    ├── Views/
    │   ├── MainWindow.xaml
    │   └── MainWindow.xaml.cs
    ├── App.xaml
    ├── App.xaml.cs
    ├── GlobalUsings.cs
    └── WpfCollectionViewSample.App.csproj
```

#### 5.6.1 Problem Scenario

When a single source collection needs to be filtered with different conditions across multiple Views while adhering to MVVM principles

#### 5.6.2 Core Principles

- **ViewModel must not reference WPF-related assemblies** (MVVM violation)
- **Encapsulate `CollectionViewSource` access through Service Layer**
- **ViewModel uses only `IEnumerable` or pure BCL types**

#### 5.6.3 Architecture Layer Structure

```
View (XAML)
    ↓ DataBinding
ViewModel Layer (uses IEnumerable, no WPF assembly reference)
    ↓ IEnumerable interface
Service Layer (uses CollectionViewSource directly)
    ↓
Data Layer (ObservableCollection<T>)
```

#### 5.6.4 Implementation Pattern

**1. Service Layer (CollectionViewFactory/Store)**

```csharp
// Services/MemberCollectionService.cs
// This class can reference PresentationFramework
namespace MyApp.Services;

public sealed class MemberCollectionService
{
    private ObservableCollection<Member> Source { get; } = [];

    // Factory Method: Create filtered view
    // Returns IEnumerable so ViewModel doesn't know WPF types
    public IEnumerable CreateView(Predicate<object>? filter = null)
    {
        var viewSource = new CollectionViewSource { Source = Source };
        var view = viewSource.View;

        if (filter is not null)
        {
            view.Filter = filter;
        }

        return view; // ICollectionView inherits IEnumerable
    }

    public void Add(Member item) => Source.Add(item);

    public void Remove(Member? item)
    {
        if (item is not null)
            Source.Remove(item);
    }

    public void Clear() => Source.Clear();
}
```

**2. ViewModel Layer**

```csharp
// ViewModel uses only IEnumerable (pure BCL type)
namespace MyApp.ViewModels;

public abstract class BaseFilteredViewModel
{
    public IEnumerable? Members { get; }

    protected BaseFilteredViewModel(Predicate<object> filter)
    {
        // Receives IEnumerable from Service
        Members = memberService.CreateView(filter);
    }
}

// Each filtered ViewModel
public sealed class WalkerViewModel : BaseFilteredViewModel
{
    public WalkerViewModel()
        : base(item => (item as Member)?.Type == DeviceTypes.Walker)
    {
    }
}

// Or use with direct type casting
public sealed class AppViewModel : ObservableObject
{
    public IEnumerable? Members { get; }

    public AppViewModel()
    {
        Members = memberService.CreateView();
    }

    // Manipulate collection with LINQ when needed
    private void ProcessMembers()
    {
        var memberList = Members?.Cast<Member>().ToList();
        // Processing logic...
    }
}
```

**3. Initialize CollectionView from View (Alternative Approach)**

This approach keeps ViewModel completely independent from WPF, but requires initialization logic in View's Code-Behind.

```csharp
// ViewModel - Uses pure BCL only
namespace MyApp.ViewModels;

public sealed partial class MainViewModel : ObservableObject
{
    [ObservableProperty] private ObservableCollection<Person> _people = [];

    private ICollectionView? _peopleView;

    // Injected from View
    public void InitializeCollectionView(ICollectionView collectionView)
    {
        _peopleView = collectionView;
        _peopleView.Filter = FilterPerson;
    }

    private bool FilterPerson(object item)
    {
        // Filtering logic
        return true;
    }
}

// MainWindow.xaml.cs - View's Code-Behind
namespace MyApp.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        var viewModel = new MainViewModel();
        DataContext = viewModel;

        // Create CollectionViewSource in View layer
        ICollectionView collectionView =
            CollectionViewSource.GetDefaultView(viewModel.People);

        // Inject into ViewModel
        viewModel.InitializeCollectionView(collectionView);
    }
}
```

**Note**: This approach requires ViewModel to know the `ICollectionView` type, so WindowsBase.dll reference is needed. For complete independence, use the Service Layer approach.

#### 5.6.5 Project Structure (Strict MVVM)

```
MyApp.Models/              // Pure C# models, BCL only

MyApp.ViewModels/         // Pure C# ViewModel
                          // No WPF assembly references
                          // Uses IEnumerable only

MyApp.Services/           // PresentationFramework reference: YES
                          // WindowsBase reference: YES
                          // Uses CollectionViewSource

MyApp.Views/              // References all WPF assemblies
```

#### 5.6.6 Assembly Reference Rules

**Assemblies that ViewModel project must NOT reference:**

- ❌ `WindowsBase.dll` (contains ICollectionView)
- ❌ `PresentationFramework.dll` (contains CollectionViewSource)
- ❌ `PresentationCore.dll`

**Assemblies that ViewModel project CAN reference:**

- ✅ BCL (Base Class Library) types only
- ✅ `System.Collections.IEnumerable`
- ✅ `System.Collections.ObjectModel.ObservableCollection<T>`
- ✅ `System.ComponentModel.INotifyPropertyChanged`

**Assemblies that Service project CAN reference:**

- ✅ `WindowsBase.dll`
- ✅ `PresentationFramework.dll`
- ✅ All WPF-related assemblies

#### 5.6.7 Key Advantages

1. **Single source maintenance**: All Views share one `ObservableCollection`
2. **Automatic synchronization**: Source changes automatically reflect in all filtered Views
3. **MVVM compliance**: ViewModel is completely independent from UI framework
4. **Reusability**: Multiple Views can be created with various filter conditions
5. **Testability**: ViewModel can be unit tested without WPF

#### 5.6.8 Utilizing CollectionView Features in Service Layer

Service Layer can encapsulate various CollectionView features.

```csharp
// Services/MemberCollectionService.cs
namespace MyApp.Services;

public sealed class MemberCollectionService
{
    private ObservableCollection<Member> Source { get; } = [];

    public IEnumerable CreateView(Predicate<object>? filter = null)
    {
        var viewSource = new CollectionViewSource { Source = Source };
        var view = viewSource.View;

        if (filter is not null)
        {
            view.Filter = filter;
        }

        return view;
    }

    // Create sorted view
    public IEnumerable CreateSortedView(
        string propertyName,
        ListSortDirection direction = ListSortDirection.Ascending)
    {
        var viewSource = new CollectionViewSource { Source = Source };
        var view = viewSource.View;

        view.SortDescriptions.Add(
            new SortDescription(propertyName, direction)
        );

        return view;
    }

    // Create grouped view
    public IEnumerable CreateGroupedView(string groupPropertyName)
    {
        var viewSource = new CollectionViewSource { Source = Source };
        var view = viewSource.View;

        view.GroupDescriptions.Add(
            new PropertyGroupDescription(groupPropertyName)
        );

        return view;
    }

    public void Add(Member item) => Source.Add(item);
    public void Remove(Member? item) { if (item is not null) Source.Remove(item); }
    public void Clear() => Source.Clear();
}
```

#### 5.6.9 When Applying DI/IoC

```csharp
// Interface definition (uses pure BCL types only)
namespace MyApp.Services;

public interface IMemberCollectionService
{
    IEnumerable CreateView(Predicate<object>? filter = null);
    void Add(Member member);
    void Remove(Member? member);
    void Clear();
}

// DI container registration
services.AddSingleton<IMemberCollectionService, MemberCollectionService>();

// ViewModel constructor injection
namespace MyApp.ViewModels;

public sealed partial class AppViewModel(IMemberCollectionService memberService)
    : ObservableObject
{
    public IEnumerable? Members { get; } = memberService.CreateView();
}
```

#### 5.6.10 Practical Recommendations

1. **Project separation**: Separate ViewModel and Service into different projects
2. **Interface usage**: Define Services with interfaces for testability
3. **Singleton or DI**: Manage Services as Singleton or through DI container
4. **Naming conventions**:
   - `MemberCollectionService` (Service suffix)
   - `MemberViewFactory` (Factory suffix)
   - `MemberStore` (Store suffix)

#### 5.6.11 Grouping UI in XAML

When using grouped CollectionView, display groups using `GroupStyle` in ListBox or ItemsControl.

**XAML - Grouped ListBox:**

```xml
<ListBox ItemsSource="{Binding GroupedMembers}">
    <!-- Group header template -->
    <ListBox.GroupStyle>
        <GroupStyle>
            <GroupStyle.HeaderTemplate>
                <DataTemplate>
                    <Border Background="#E0E0E0" Padding="5">
                        <StackPanel Orientation="Horizontal">
                            <TextBlock Text="{Binding Name}"
                                       FontWeight="Bold"
                                       FontSize="14"/>
                            <TextBlock Text=" ("
                                       Foreground="Gray"/>
                            <TextBlock Text="{Binding ItemCount}"
                                       Foreground="Gray"/>
                            <TextBlock Text=" items)"
                                       Foreground="Gray"/>
                        </StackPanel>
                    </Border>
                </DataTemplate>
            </GroupStyle.HeaderTemplate>
            <!-- Optional: Group container style -->
            <GroupStyle.ContainerStyle>
                <Style TargetType="{x:Type GroupItem}">
                    <Setter Property="Margin" Value="0,0,0,10"/>
                </Style>
            </GroupStyle.ContainerStyle>
        </GroupStyle>
    </ListBox.GroupStyle>

    <!-- Item template -->
    <ListBox.ItemTemplate>
        <DataTemplate>
            <TextBlock Text="{Binding Name}" Padding="10,5"/>
        </DataTemplate>
    </ListBox.ItemTemplate>
</ListBox>
```

**XAML - Expander Style Grouping:**

```xml
<ListBox ItemsSource="{Binding GroupedMembers}">
    <ListBox.GroupStyle>
        <GroupStyle>
            <GroupStyle.ContainerStyle>
                <Style TargetType="{x:Type GroupItem}">
                    <Setter Property="Template">
                        <Setter.Value>
                            <ControlTemplate TargetType="{x:Type GroupItem}">
                                <Expander IsExpanded="True">
                                    <Expander.Header>
                                        <StackPanel Orientation="Horizontal">
                                            <TextBlock Text="{Binding Name}"
                                                       FontWeight="Bold"/>
                                            <TextBlock Text="{Binding ItemCount,
                                                       StringFormat=' ({0})'}"
                                                       Foreground="Gray"/>
                                        </StackPanel>
                                    </Expander.Header>
                                    <ItemsPresenter/>
                                </Expander>
                            </ControlTemplate>
                        </Setter.Value>
                    </Setter>
                </Style>
            </GroupStyle.ContainerStyle>
        </GroupStyle>
    </ListBox.GroupStyle>
</ListBox>
```

**Service Layer - Multiple Sort and Group:**

```csharp
// Create view with sorting and grouping combined
public IEnumerable CreateSortedGroupedView(
    string sortProperty,
    ListSortDirection sortDirection,
    string groupProperty)
{
    var viewSource = new CollectionViewSource { Source = Source };
    var view = viewSource.View;

    // Apply sort first, then group
    view.SortDescriptions.Add(new SortDescription(sortProperty, sortDirection));
    view.GroupDescriptions.Add(new PropertyGroupDescription(groupProperty));

    return view;
}
```

#### 5.6.12 Microsoft Official Documentation

- [CollectionViewSource Class](https://learn.microsoft.com/en-us/dotnet/api/system.windows.data.collectionviewsource?view=windowsdesktop-10.0)
- [Data Binding Overview - Collection Views](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/#binding-to-collections)
- [How to: Filter Data in a View](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/how-to-filter-data-in-a-view)
- [Service Layer Pattern](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/models-data/validating-with-a-service-layer-cs#creating-a-service-layer)

