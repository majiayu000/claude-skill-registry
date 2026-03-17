---
name: localizing-wpf-applications
description: Localizes WPF applications using resource files, x:Uid, and BAML localization. Use when building multi-language applications or supporting right-to-left layouts.
---

# WPF Localization Patterns

Implementing multi-language support in WPF applications.

## 1. Localization Overview

```
Localization Approaches
├── Resource Files (.resx)
│   ├── Simple string lookup
│   └── Strongly-typed access
├── BAML Localization
│   ├── x:Uid attributes
│   └── LocBaml tool
└── Runtime Features
    ├── FlowDirection (RTL support)
    ├── Culture-aware formatting
    └── Dynamic language switching
```

---

## 2. Resource File Approach

### 2.1 Creating Resource Files

```
Project Structure:
├── Properties/
│   └── Resources.resx          (default/fallback)
├── Resources/
│   ├── Strings.resx            (default English)
│   ├── Strings.ko-KR.resx      (Korean)
│   ├── Strings.ja-JP.resx      (Japanese)
│   └── Strings.de-DE.resx      (German)
```

### 2.2 Resource File Content

**Strings.resx (English - default):**
```xml
<data name="AppTitle" xml:space="preserve">
    <value>My Application</value>
</data>
<data name="WelcomeMessage" xml:space="preserve">
    <value>Welcome, {0}!</value>
</data>
<data name="SaveButton" xml:space="preserve">
    <value>Save</value>
</data>
<data name="CancelButton" xml:space="preserve">
    <value>Cancel</value>
</data>
```

**Strings.ko-KR.resx (Korean):**
```xml
<data name="AppTitle" xml:space="preserve">
    <value>My Application (Korean translation)</value>
</data>
<data name="WelcomeMessage" xml:space="preserve">
    <value>Welcome, {0}! (Korean translation)</value>
</data>
<data name="SaveButton" xml:space="preserve">
    <value>Save (Korean translation)</value>
</data>
<data name="CancelButton" xml:space="preserve">
    <value>Cancel (Korean translation)</value>
</data>
```

### 2.3 Using Resources in XAML

```xml
<Window xmlns:p="clr-namespace:MyApp.Resources">
    <Window.Title>
        <Binding Source="{x:Static p:Strings.AppTitle}"/>
    </Window.Title>

    <StackPanel>
        <TextBlock Text="{x:Static p:Strings.WelcomeMessage}"/>
        <Button Content="{x:Static p:Strings.SaveButton}"/>
        <Button Content="{x:Static p:Strings.CancelButton}"/>
    </StackPanel>
</Window>
```

### 2.4 Using Resources in Code

```csharp
using MyApp.Resources;

// Direct access
var title = Strings.AppTitle;

// Formatted string
var welcome = string.Format(Strings.WelcomeMessage, userName);

// Access by key (for dynamic keys)
var value = Strings.ResourceManager.GetString("SaveButton");
```

---

## 3. Setting Culture

### 3.1 At Application Startup

```csharp
namespace MyApp;

using System.Globalization;
using System.Threading;
using System.Windows;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Set culture from user settings or system
        var cultureName = GetSavedCulture() ?? CultureInfo.CurrentCulture.Name;
        SetCulture(cultureName);
    }

    public static void SetCulture(string cultureName)
    {
        var culture = new CultureInfo(cultureName);

        // Set for current thread
        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;

        // Set for new threads (.NET 4.6+)
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;
    }

    private string? GetSavedCulture()
    {
        return Properties.Settings.Default.Culture;
    }
}
```

### 3.2 Dynamic Language Switching

```csharp
namespace MyApp.Services;

using System.Globalization;
using System.Threading;
using System.Windows;

public sealed class LocalizationService
{
    public event EventHandler? CultureChanged;

    public CultureInfo CurrentCulture => Thread.CurrentThread.CurrentUICulture;

    public void ChangeCulture(string cultureName)
    {
        var culture = new CultureInfo(cultureName);

        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;

        // Save preference
        Properties.Settings.Default.Culture = cultureName;
        Properties.Settings.Default.Save();

        // Notify subscribers
        CultureChanged?.Invoke(this, EventArgs.Empty);

        // Restart required for full XAML update
        RestartApplication();
    }

    private void RestartApplication()
    {
        var result = MessageBox.Show(
            "Application needs to restart to apply language change. Restart now?",
            "Language Changed",
            MessageBoxButton.YesNo);

        if (result == MessageBoxResult.Yes)
        {
            System.Diagnostics.Process.Start(Application.ResourceAssembly.Location);
            Application.Current.Shutdown();
        }
    }
}
```

---

## 4. Related Skills

| Skill | Description |
|-------|-------------|
| `/localizing-wpf-with-baml` | BAML localization with x:Uid and LocBaml tool |
| `/implementing-wpf-rtl-support` | RTL layout support for Arabic, Hebrew |
| `/formatting-culture-aware-data` | Date, number, currency formatting + converters |

---

## 5. Language Selection UI

```xml
<ComboBox x:Name="LanguageSelector"
          SelectionChanged="LanguageSelector_SelectionChanged">
    <ComboBoxItem Tag="en-US" Content="English"/>
    <ComboBoxItem Tag="ko-KR" Content="Korean"/>
    <ComboBoxItem Tag="ja-JP" Content="Japanese"/>
    <ComboBoxItem Tag="de-DE" Content="German"/>
</ComboBox>
```

```csharp
private void LanguageSelector_SelectionChanged(object sender, SelectionChangedEventArgs e)
{
    if (LanguageSelector.SelectedItem is ComboBoxItem item)
    {
        var cultureName = item.Tag?.ToString();

        if (!string.IsNullOrEmpty(cultureName))
        {
            _localizationService.ChangeCulture(cultureName);
        }
    }
}
```

---

## 6. References

- [WPF Globalization and Localization Overview - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/wpf-globalization-and-localization-overview)
- [Localizing XAML - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/how-to-localize-an-application)
- [CultureInfo Class - Microsoft Docs](https://learn.microsoft.com/en-us/dotnet/api/system.globalization.cultureinfo)
