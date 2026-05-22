---
name: wpf-mvvm-collectionview
description: 'WPF에서 CollectionView를 Service Layer로 캡슐화하여 MVVM 원칙을 준수하는 패턴'
---

# 5.6 CollectionView를 사용한 MVVM 패턴

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

```
templates/
├── WpfCollectionViewSample.Core/           ← 순수 C# 모델 및 인터페이스
│   ├── Member.cs
│   ├── IMemberCollectionService.cs
│   └── WpfCollectionViewSample.Core.csproj
├── WpfCollectionViewSample.ViewModels/     ← ViewModel (WPF 참조 없음)
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

#### 5.6.1 문제 상황

하나의 원본 컬렉션을 여러 View에서 각각 다른 조건으로 필터링하여 사용하면서도 MVVM 원칙을 준수해야 하는 경우

#### 5.6.2 핵심 원칙

- **ViewModel은 WPF 관련 어셈블리를 참조하면 안 됨** (MVVM 위반)
- **Service Layer를 통해 `CollectionViewSource` 접근을 캡슐화**
- **ViewModel은 `IEnumerable` 또는 순수 BCL 타입만 사용**

#### 5.6.3 아키텍처 계층 구조

```
View (XAML)
    ↓ DataBinding
ViewModel Layer (IEnumerable 사용, WPF 어셈블리 참조 X)
    ↓ IEnumerable 인터페이스
Service Layer (CollectionViewSource 직접 사용)
    ↓
Data Layer (ObservableCollection<T>)
```

#### 5.6.4 구현 패턴

**1. Service Layer (CollectionViewFactory/Store)**

```csharp
// Services/MemberCollectionService.cs
// 이 클래스는 PresentationFramework 참조 가능
// This class can reference PresentationFramework
namespace MyApp.Services;

public sealed class MemberCollectionService
{
    private ObservableCollection<Member> Source { get; } = [];

    // Factory Method: 필터링된 뷰 생성
    // IEnumerable로 반환하여 ViewModel이 WPF 타입을 모르게 함
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

        return view; // ICollectionView는 IEnumerable을 상속
                     // ICollectionView inherits IEnumerable
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
// ViewModel은 IEnumerable만 사용 (순수 BCL 타입)
// ViewModel uses only IEnumerable (pure BCL type)
namespace MyApp.ViewModels;

public abstract class BaseFilteredViewModel
{
    public IEnumerable? Members { get; }

    protected BaseFilteredViewModel(Predicate<object> filter)
    {
        // Service에서 IEnumerable로 받음
        // Receives IEnumerable from Service
        Members = memberService.CreateView(filter);
    }
}

// 각 필터링된 ViewModel
// Each filtered ViewModel
public sealed class WalkerViewModel : BaseFilteredViewModel
{
    public WalkerViewModel()
        : base(item => (item as Member)?.Type == DeviceTypes.Walker)
    {
    }
}

// 또는 직접 타입 캐스팅하여 사용
// Or use with direct type casting
public sealed class AppViewModel : ObservableObject
{
    public IEnumerable? Members { get; }

    public AppViewModel()
    {
        Members = memberService.CreateView();
    }

    // 필요시 LINQ로 컬렉션 조작
    // Manipulate collection with LINQ when needed
    private void ProcessMembers()
    {
        var memberList = Members?.Cast<Member>().ToList();
        // 처리 로직...
        // Processing logic...
    }
}
```

**3. View에서 CollectionView 초기화 (대안 방법)**

이 방법은 ViewModel이 완전히 WPF로부터 독립적이지만, View의 Code-Behind에서 초기화 로직이 필요합니다.

```csharp
// ViewModel - 순수 BCL만 사용
// ViewModel - Uses pure BCL only
namespace MyApp.ViewModels;

public sealed partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private ObservableCollection<Person> people = [];

    private ICollectionView? _peopleView;

    // View에서 주입받음
    // Injected from View
    public void InitializeCollectionView(ICollectionView collectionView)
    {
        _peopleView = collectionView;
        _peopleView.Filter = FilterPerson;
    }

    private bool FilterPerson(object item)
    {
        // 필터링 로직
        // Filtering logic
        return true;
    }
}

// MainWindow.xaml.cs - View의 Code-Behind
// MainWindow.xaml.cs - View's Code-Behind
namespace MyApp.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        var viewModel = new MainViewModel();
        DataContext = viewModel;

        // View 레이어에서 CollectionViewSource 생성
        // Create CollectionViewSource in View layer
        ICollectionView collectionView =
            CollectionViewSource.GetDefaultView(viewModel.People);

        // ViewModel에 주입
        // Inject into ViewModel
        viewModel.InitializeCollectionView(collectionView);
    }
}
```

**주의**: 이 방법은 ViewModel이 `ICollectionView` 타입을 알게 되므로, WindowsBase.dll 참조가 필요합니다. 완전한 독립을 원한다면 Service Layer 방식을 사용하세요.

#### 5.6.5 프로젝트 구조 (엄격한 MVVM)

```
MyApp.Models/              // 순수 C# 모델, BCL만 사용
                          // Pure C# models, BCL only

MyApp.ViewModels/         // 순수 C# ViewModel
                          // Pure C# ViewModel
                          // WPF 어셈블리 참조 X
                          // No WPF assembly references
                          // IEnumerable만 사용
                          // Uses IEnumerable only

MyApp.Services/           // PresentationFramework 참조 O
                          // PresentationFramework reference: YES
                          // WindowsBase 참조 O
                          // WindowsBase reference: YES
                          // CollectionViewSource 사용
                          // Uses CollectionViewSource

MyApp.Views/              // 모든 WPF 어셈블리 참조
                          // References all WPF assemblies
```

#### 5.6.6 참조 어셈블리 규칙

**ViewModel 프로젝트가 참조하면 안 되는 어셈블리:**

- ❌ `WindowsBase.dll` (ICollectionView 포함)
- ❌ `PresentationFramework.dll` (CollectionViewSource 포함)
- ❌ `PresentationCore.dll`

**ViewModel 프로젝트가 참조 가능한 어셈블리:**

- ✅ BCL (Base Class Library) 타입만 사용
- ✅ `System.Collections.IEnumerable`
- ✅ `System.Collections.ObjectModel.ObservableCollection<T>`
- ✅ `System.ComponentModel.INotifyPropertyChanged`

**Service 프로젝트가 참조 가능한 어셈블리:**

- ✅ `WindowsBase.dll`
- ✅ `PresentationFramework.dll`
- ✅ 모든 WPF 관련 어셈블리

#### 5.6.7 핵심 장점

1. **단일 원본 유지**: 모든 View가 하나의 `ObservableCollection` 공유
2. **자동 동기화**: 원본 변경 시 모든 필터링된 View에 자동 반영
3. **MVVM 준수**: ViewModel이 UI 프레임워크에 완전 독립적
4. **재사용성**: 다양한 필터 조건으로 여러 View 생성 가능
5. **테스트 용이성**: ViewModel을 WPF 없이 단위 테스트 가능

#### 5.6.8 Service Layer에서 CollectionView 기능 활용

Service Layer에서 CollectionView의 다양한 기능을 캡슐화하여 제공할 수 있습니다.

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

    // 정렬된 뷰 생성
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

    // 그룹화된 뷰 생성
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

#### 5.6.9 DI/IoC 적용 시

```csharp
// Interface 정의 (순수 BCL 타입만 사용)
// Interface definition (uses pure BCL types only)
namespace MyApp.Services;

public interface IMemberCollectionService
{
    IEnumerable CreateView(Predicate<object>? filter = null);
    void Add(Member member);
    void Remove(Member? member);
    void Clear();
}

// DI 컨테이너 등록
// DI container registration
services.AddSingleton<IMemberCollectionService, MemberCollectionService>();

// ViewModel 생성자 주입
// ViewModel constructor injection
namespace MyApp.ViewModels;

public sealed partial class AppViewModel(IMemberCollectionService memberService)
    : ObservableObject
{
    public IEnumerable? Members { get; } = memberService.CreateView();
}
```

#### 5.6.10 실무 적용 시 권장사항

1. **프로젝트 분리**: ViewModel과 Service를 별도 프로젝트로 분리
2. **Interface 활용**: Service는 인터페이스로 정의하여 테스트 용이성 확보
3. **Singleton 또는 DI**: Service는 Singleton 또는 DI 컨테이너로 관리
4. **명명 규칙**:
   - `MemberCollectionService` (Service 접미사)
   - `MemberViewFactory` (Factory 접미사)
   - `MemberStore` (Store 접미사)

#### 5.6.11 Microsoft 공식 문서

- [CollectionViewSource Class](https://learn.microsoft.com/en-us/dotnet/api/system.windows.data.collectionviewsource?view=windowsdesktop-10.0)
- [Data Binding Overview - Collection Views](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/#binding-to-collections)
- [How to: Filter Data in a View](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/how-to-filter-data-in-a-view)
- [Service Layer Pattern](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions-1/models-data/validating-with-a-service-layer-cs#creating-a-service-layer)
