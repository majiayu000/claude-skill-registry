---
name: datatemplate-mapping
description: "DataTemplate을 사용한 ViewModel-View 자동 매핑 및 네비게이션 패턴"
---

# 5.8 DataTemplate을 사용한 View-ViewModel 자동 매핑

WPF에서 DataTemplate을 사용하면 ViewModel 타입과 View를 자동으로 매핑할 수 있습니다. 이 패턴은 네비게이션 시나리오나 동적 콘텐츠 표시에 매우 유용합니다.

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

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
│   ├── Mappings.xaml                    ← DataTemplate 매핑 정의
│   ├── GlobalUsings.cs
│   └── WpfDataTemplateSample.App.csproj
└── WpfDataTemplateSample.ViewModels/    ← ViewModel Class Library
    ├── MainWindowViewModel.cs
    ├── HomeViewModel.cs
    ├── SettingsViewModel.cs
    ├── GlobalUsings.cs
    └── WpfDataTemplateSample.ViewModels.csproj
```

#### 5.8.1 핵심 개념

**ContentControl의 Content에 ViewModel 인스턴스를 바인딩하면, WPF가 자동으로 해당 ViewModel 타입에 맞는 DataTemplate을 찾아서 View를 렌더링합니다.**

이 패턴의 핵심:
1. `Mappings.xaml`에 ViewModel 타입별 DataTemplate 정의
2. `ContentControl.Content`에 ViewModel 인스턴스 바인딩
3. WPF가 자동으로 타입을 매칭하여 해당 View 렌더링

#### 5.8.2 Mappings.xaml 패턴

**Mappings.xaml - ViewModel과 View 매핑 정의:**

```xml
<!-- Mappings.xaml -->
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:viewmodels="clr-namespace:WpfDataTemplateSample.ViewModels"
                    xmlns:views="clr-namespace:WpfDataTemplateSample.Views">

    <!--  ViewModel과 View를 자동으로 매핑하는 DataTemplate 정의  -->
    <!--  ContentControl의 Content에 ViewModel을 설정하면 자동으로 해당 View가 렌더링됨  -->

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

**App.xaml - Mappings.xaml을 Application Resources에 병합:**

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

#### 5.8.3 네비게이션 패턴 구현

**MainWindowViewModel - CurrentViewModel 속성으로 화면 전환:**

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

**MainWindow.xaml - ContentControl로 동적 콘텐츠 표시:**

```xml
<!-- MainWindow.xaml -->
<Window x:Class="WpfDataTemplateSample.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:viewmodels="clr-namespace:WpfDataTemplateSample.ViewModels"
        Title="DataTemplate 자동 매핑 Sample"
        Width="800"
        Height="500"
        WindowStartupLocation="CenterScreen">

    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
        </Grid.RowDefinitions>

        <!--  Navigation 버튼 영역  -->
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

        <!--  ContentControl에 ViewModel을 바인딩하면 Mappings.xaml의 DataTemplate에 의해 자동으로 View가 렌더링됨  -->
        <!--  핵심: Content에 ViewModel 타입을 설정하면 자동으로 해당 View가 표시됨  -->
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

#### 5.8.4 ViewModel 및 View 구현 예시

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

#### 5.8.5 핵심 원칙

1. **DataTemplate의 DataType 속성**: ViewModel 타입을 지정하여 자동 매핑
2. **x:Key 없이 정의**: DataType만 지정하면 WPF가 타입으로 자동 검색
3. **ContentControl 사용**: Content 속성에 ViewModel 인스턴스 바인딩
4. **Application Resources에 등록**: Mappings.xaml을 App.xaml에서 MergedDictionaries로 병합
5. **View는 UserControl**: 재사용 가능한 UserControl로 View 정의

#### 5.8.6 장점

1. **View-ViewModel 결합도 감소**: Code-Behind에서 View를 직접 생성하지 않음
2. **선언적 매핑**: XAML에서 명시적으로 매핑 관계 정의
3. **네비게이션 간소화**: ViewModel 인스턴스만 교체하면 자동으로 화면 전환
4. **테스트 용이성**: ViewModel만으로 로직 테스트 가능
5. **디자인 타임 지원**: `d:DataContext`를 통한 디자이너 미리보기 지원

#### 5.8.7 주의사항

**⚠️ 중요:**
- DataTemplate은 `x:Key` 없이 정의해야 자동 매핑 동작
- Mappings.xaml은 반드시 Application.Resources에 병합 필요
- ViewModel 타입은 정확히 일치해야 함 (상속 관계 고려 안 됨)
- ContentControl.Content에는 ViewModel 인스턴스를 바인딩 (타입이 아닌 인스턴스)
- View는 DataContext를 자동으로 받음 (별도 설정 불필요)

#### 5.8.8 프로젝트 구조 예시

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
├── Mappings.xaml              ← DataTemplate 매핑 정의
└── GlobalUsings.cs
```

---

