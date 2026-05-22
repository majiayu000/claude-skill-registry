---
name: communitytoolkit-mvvm
description: "CommunityToolkit.Mvvm을 사용한 MVVM 패턴 구현 (ObservableProperty Attribute 스타일)"
---

# CommunityToolkit.Mvvm 코드 지침

WPF/AvaloniaUI에서 MVVM 패턴을 구현할 때 CommunityToolkit.Mvvm 사용 가이드입니다.

## 프로젝트 구조

templates 폴더에 .NET 9 WPF 프로젝트 예제가 포함되어 있습니다.

```
templates/
├── WpfMvvmSample.App/           ← WPF Application Project
│   ├── Views/
│   │   ├── MainWindow.xaml
│   │   └── MainWindow.xaml.cs
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── GlobalUsings.cs
│   └── WpfMvvmSample.App.csproj
└── WpfMvvmSample.ViewModels/    ← ViewModel Class Library (UI 프레임워크 독립)
    ├── UserViewModel.cs
    ├── GlobalUsings.cs
    └── WpfMvvmSample.ViewModels.csproj
```

## 기본 원칙

**MVVM을 구조로 잡을 때는 CommunityToolkit.Mvvm을 기본으로 사용**

## ObservableProperty Attribute 작성 규칙

### 단일 Attribute - Inline 작성

```csharp
// ✅ 좋은 예: Attribute가 1개일 경우 inline으로 작성
// Good: Single attribute written inline
[ObservableProperty] private string _userName = string.Empty;

[ObservableProperty] private int _age;

[ObservableProperty] private bool _isActive;
```

### 여러 Attribute - ObservableProperty는 항상 Inline

```csharp
// ✅ 좋은 예: Attribute가 여러 개일 경우, ObservableProperty는 항상 inline
// Good: Multiple attributes, ObservableProperty always inline
[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
[ObservableProperty] private string _email = string.Empty;

[NotifyDataErrorInfo]
[Required(ErrorMessage = "이름은 필수입니다.")]
[MinLength(2, ErrorMessage = "이름은 최소 2글자 이상이어야 합니다.")]
[ObservableProperty] private string _name = string.Empty;

[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
[NotifyCanExecuteChangedFor(nameof(UpdateCommand))]
[ObservableProperty] private User? _selectedUser;
```

### 잘못된 예

```csharp
// ❌ 나쁜 예: ObservableProperty를 별도 줄에 작성
// Bad: ObservableProperty on separate line
[NotifyPropertyChangedRecipients]
[NotifyCanExecuteChangedFor(nameof(SaveCommand))]
[ObservableProperty]
private string _email = string.Empty;
```

## 실제 ViewModel 예시

```csharp
namespace MyApp.ViewModels;

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public sealed partial class UserViewModel : ObservableObject
{
    // 단일 Attribute
    // Single attribute
    [ObservableProperty] private string _firstName = string.Empty;
    [ObservableProperty] private string _lastName = string.Empty;
    [ObservableProperty] private int _age;

    // 여러 Attribute - ObservableProperty는 inline
    // Multiple attributes - ObservableProperty inline
    [NotifyPropertyChangedRecipients]
    [NotifyCanExecuteChangedFor(nameof(SaveCommand))]
    [ObservableProperty] private string _email = string.Empty;

    [NotifyCanExecuteChangedFor(nameof(DeleteCommand))]
    [NotifyCanExecuteChangedFor(nameof(UpdateCommand))]
    [ObservableProperty] private User? _selectedUser;

    [RelayCommand(CanExecute = nameof(CanSave))]
    private async Task SaveAsync()
    {
        // 저장 로직
        // Save logic
    }

    private bool CanSave() => !string.IsNullOrWhiteSpace(Email);
}
```

## 핵심 규칙

- **Attribute가 1개**: `[ObservableProperty]` inline으로 필드 선언 바로 앞에 작성
- **Attribute가 여러 개**: 다른 Attribute들은 각 줄에 작성하되, `[ObservableProperty]`는 **항상 마지막에 inline**으로 작성
- **목적**: 코드 가독성 향상 및 일관된 코딩 스타일 유지
