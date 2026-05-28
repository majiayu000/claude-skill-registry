---
name: dotnet-cpp-localizer
description: Comprehensive internationalization (i18n) and localization (l10n) for .NET and C++ applications. Generate resource files, manage translations, and implement best practices for multi-language support.
---

# .NET & C++ Localizer Skill

.NETとC++アプリケーションの国際化（i18n）と地域化（l10n）を完全サポートするスキルです。

## 概要

このスキルは、**.NET**（.resx）と**C++**（gettext/ICU）の両方に対応した、エンタープライズレベルの国際化ソリューションを提供します。リソースファイル生成、翻訳管理、ベストプラクティス適用まで、国際化のすべてをカバーします。

## 主な機能

- **🎯 .NET サポート**: .resx、IStringLocalizer、ASP.NET Core localization
- **🎯 C++ サポート**: gettext (.po/.pot)、ICU、Boost.Locale
- **📦 リソース生成**: 自動リソースファイル作成
- **🔍 文字列抽出**: ハードコードされた文字列の自動検出
- **🌐 翻訳管理**: 複数言語の翻訳ファイル管理
- **✅ 品質チェック**: 翻訳漏れ、重複、フォーマットエラー検出
- **📊 進捗トラッキング**: 言語別の翻訳完了率
- **🔄 同期ツール**: コード変更への自動追従
- **🎨 複数形対応**: .NET plural rules、gettext ngettext
- **📱 文化対応**: 日付・通貨・数値のロケール別フォーマット

## サポート技術

### .NET ファミリー

- **.NET Core / .NET 6/7/8/9**
- **ASP.NET Core** (MVC, Razor Pages, Blazor)
- **WPF** (Windows Presentation Foundation)
- **WinForms** (Windows Forms)
- **Xamarin** (iOS/Android)
- **.NET MAUI** (Multi-platform App UI)
- **Unity** (C# ゲームエンジン)

### C++ フレームワーク

- **gettext** - GNU翻訳システム（最も人気）
- **ICU** - International Components for Unicode
- **Boost.Locale** - C++標準ライブラリ風API
- **Qt Linguist** - Qt フレームワーク (.ts ファイル)
- **wxWidgets** - クロスプラットフォームGUI

## 使用方法

### .NET アプリケーションの国際化

#### 基本的なリソースファイル生成

```
.NET Coreプロジェクトに国際化を追加：

プロジェクトタイプ: ASP.NET Core MVC
言語: 英語（デフォルト）、日本語、中国語、スペイン語
リソース場所: Resources/
文化: ja-JP, zh-CN, es-ES

タスク:
1. .resx ファイル生成
2. IStringLocalizer 設定
3. Startup.cs 設定
4. ハードコード文字列の抽出と置き換え
```

#### WPF アプリケーション

```
WPF デスクトップアプリに多言語対応：

言語: 英語、日本語、ドイツ語
リソース: Properties/Resources.resx
UI更新: すべてのラベル、ボタン、メッセージボックス
言語切り替え: ランタイムで切り替え可能
```

---

### C++ アプリケーションの国際化

#### gettext 統合

```
C++ コンソールアプリケーションにgettextを統合：

ライブラリ: GNU gettext
言語: 英語、日本語、フランス語
ドメイン: myapp
出力: po/ja/myapp.po, po/fr/myapp.po

タスク:
1. gettext セットアップコード生成
2. 文字列抽出（xgettext）
3. .pot/.po ファイル生成
4. コード修正（_() マクロ）
```

#### ICU 統合

```
C++ プロジェクトにICUを統合：

機能:
- Unicode文字列処理
- 日付・時刻フォーマット（ロケール別）
- 数値・通貨フォーマット
- 複数形ルール
- ソート・検索（ロケール対応）
```

---

## .NET 実装パターン

### 1. ASP.NET Core MVC の国際化

**生成されるファイル構成**:

```
MyWebApp/
├── Resources/
│   ├── Controllers/
│   │   ├── HomeController.en.resx
│   │   ├── HomeController.ja.resx
│   │   └── HomeController.zh.resx
│   ├── Views/
│   │   ├── Home/
│   │   │   ├── Index.en.resx
│   │   │   ├── Index.ja.resx
│   │   │   └── Index.zh.resx
│   │   └── Shared/
│   │       ├── _Layout.en.resx
│   │       └── _Layout.ja.resx
│   └── SharedResources.resx
├── Program.cs (または Startup.cs)
└── appsettings.json
```

**Program.cs** (.NET 6+):

```csharp
using Microsoft.AspNetCore.Localization;
using Microsoft.Extensions.Options;
using System.Globalization;

var builder = WebApplication.CreateBuilder(args);

// Localization サービス追加
builder.Services.AddLocalization(options => options.ResourcesPath = "Resources");

builder.Services.AddControllersWithViews()
    .AddViewLocalization()
    .AddDataAnnotationsLocalization();

// サポートする文化を設定
var supportedCultures = new[]
{
    new CultureInfo("en"),
    new CultureInfo("ja"),
    new CultureInfo("zh"),
    new CultureInfo("es")
};

builder.Services.Configure<RequestLocalizationOptions>(options =>
{
    options.DefaultRequestCulture = new RequestCulture("en");
    options.SupportedCultures = supportedCultures;
    options.SupportedUICultures = supportedCultures;

    // クッキーベースの文化選択
    options.RequestCultureProviders.Insert(0, new CookieRequestCultureProvider());
});

var app = builder.Build();

// Localization ミドルウェア追加（重要: UseRouting より前）
app.UseRequestLocalization(
    app.Services.GetRequiredService<IOptions<RequestLocalizationOptions>>().Value
);

app.UseRouting();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
```

**Resources/Controllers/HomeController.ja.resx**:

```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <data name="Welcome" xml:space="preserve">
    <value>ようこそ</value>
  </data>
  <data name="HelloMessage" xml:space="preserve">
    <value>こんにちは、{0}さん！</value>
  </data>
  <data name="ItemCount" xml:space="preserve">
    <value>{0} 件のアイテム</value>
  </data>
</root>
```

**HomeController.cs**:

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Localization;

public class HomeController : Controller
{
    private readonly IStringLocalizer<HomeController> _localizer;

    public HomeController(IStringLocalizer<HomeController> localizer)
    {
        _localizer = localizer;
    }

    public IActionResult Index()
    {
        // リソースから文字列取得
        ViewData["Message"] = _localizer["Welcome"];

        // パラメータ付き
        var userName = "田中";
        ViewData["Greeting"] = _localizer["HelloMessage", userName];

        // 複数形対応
        var count = 5;
        ViewData["Items"] = _localizer["ItemCount", count];

        return View();
    }

    [HttpPost]
    public IActionResult SetLanguage(string culture, string returnUrl)
    {
        Response.Cookies.Append(
            CookieRequestCultureProvider.DefaultCookieName,
            CookieRequestCultureProvider.MakeCookieValue(new RequestCulture(culture)),
            new CookieOptions { Expires = DateTimeOffset.UtcNow.AddYears(1) }
        );

        return LocalRedirect(returnUrl);
    }
}
```

**Views/Home/Index.cshtml**:

```html
@using Microsoft.AspNetCore.Mvc.Localization
@inject IViewLocalizer Localizer

<h1>@Localizer["Welcome"]</h1>
<p>@ViewData["Greeting"]</p>
<p>@ViewData["Items"]</p>

<!-- 言語切り替え -->
<form asp-action="SetLanguage" asp-controller="Home" method="post">
    <input type="hidden" name="returnUrl" value="@Context.Request.Path" />
    <select name="culture" onchange="this.form.submit()">
        <option value="en">English</option>
        <option value="ja">日本語</option>
        <option value="zh">中文</option>
        <option value="es">Español</option>
    </select>
</form>
```

---

### 2. WPF デスクトップアプリケーション

**App.xaml.cs**:

```csharp
using System.Globalization;
using System.Threading;
using System.Windows;

public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // ユーザー設定から言語読み込み
        var cultureName = Properties.Settings.Default.Language ?? "en";
        SetLanguage(cultureName);
    }

    public static void SetLanguage(string cultureName)
    {
        var culture = new CultureInfo(cultureName);

        Thread.CurrentThread.CurrentCulture = culture;
        Thread.CurrentThread.CurrentUICulture = culture;

        // WPFのリソースディクショナリを更新
        CultureInfo.DefaultThreadCurrentCulture = culture;
        CultureInfo.DefaultThreadCurrentUICulture = culture;
    }
}
```

**MainWindow.xaml.cs**:

```csharp
using System.Windows;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        UpdateUI();
    }

    private void UpdateUI()
    {
        // リソースから文字列取得
        Title = Properties.Resources.AppTitle;
        WelcomeLabel.Content = Properties.Resources.Welcome;
        LoginButton.Content = Properties.Resources.Login;
    }

    private void LanguageComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (LanguageComboBox.SelectedItem is ComboBoxItem item)
        {
            var culture = item.Tag.ToString();
            App.SetLanguage(culture);

            // 設定を保存
            Properties.Settings.Default.Language = culture;
            Properties.Settings.Default.Save();

            // UIを更新（または再起動）
            UpdateUI();
        }
    }
}
```

**Properties/Resources.resx** (英語):

```xml
<data name="AppTitle" xml:space="preserve">
  <value>My Application</value>
</data>
<data name="Welcome" xml:space="preserve">
  <value>Welcome!</value>
</data>
<data name="Login" xml:space="preserve">
  <value>Login</value>
</data>
```

**Properties/Resources.ja.resx** (日本語):

```xml
<data name="AppTitle" xml:space="preserve">
  <value>私のアプリケーション</value>
</data>
<data name="Welcome" xml:space="preserve">
  <value>ようこそ！</value>
</data>
<data name="Login" xml:space="preserve">
  <value>ログイン</value>
</data>
```

---

### 3. .NET MAUI (マルチプラットフォーム)

**MauiProgram.cs**:

```csharp
using Microsoft.Extensions.Localization;
using System.Globalization;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            });

        // Localization追加
        builder.Services.AddLocalization();

        return builder.Build();
    }
}
```

**Resources/Strings/AppResources.ja.resx**:

```xml
<data name="Welcome" xml:space="preserve">
  <value>ようこそ</value>
</data>
```

**MainPage.xaml.cs**:

```csharp
using Microsoft.Extensions.Localization;

public partial class MainPage : ContentPage
{
    private readonly IStringLocalizer<AppResources> _localizer;

    public MainPage(IStringLocalizer<AppResources> localizer)
    {
        InitializeComponent();
        _localizer = localizer;

        WelcomeLabel.Text = _localizer["Welcome"];
    }
}
```

---

## C++ 実装パターン

### 1. gettext による国際化

**ファイル構成**:

```
myapp/
├── src/
│   ├── main.cpp
│   └── i18n.h
├── po/
│   ├── myapp.pot          # テンプレート
│   ├── ja/
│   │   └── myapp.po       # 日本語翻訳
│   ├── fr/
│   │   └── myapp.po       # フランス語翻訳
│   └── de/
│       └── myapp.po       # ドイツ語翻訳
├── locale/                 # コンパイル済み .mo ファイル
│   ├── ja/
│   │   └── LC_MESSAGES/
│   │       └── myapp.mo
│   └── fr/
│       └── LC_MESSAGES/
│           └── myapp.mo
└── CMakeLists.txt
```

**i18n.h** (ヘッダー):

```cpp
#ifndef I18N_H
#define I18N_H

#include <libintl.h>
#include <locale.h>

// 翻訳マクロ
#define _(STRING) gettext(STRING)
#define N_(STRING) STRING

// 複数形対応
#define _n(SINGULAR, PLURAL, N) ngettext(SINGULAR, PLURAL, N)

// 初期化関数
inline void initI18n(const char* domain, const char* locale_dir) {
    // ロケール設定
    setlocale(LC_ALL, "");

    // gettext設定
    bindtextdomain(domain, locale_dir);
    bind_textdomain_codeset(domain, "UTF-8");
    textdomain(domain);
}

#endif // I18N_H
```

**main.cpp**:

```cpp
#include <iostream>
#include <string>
#include "i18n.h"

int main(int argc, char* argv[]) {
    // 国際化初期化
    initI18n("myapp", "./locale");

    // 翻訳された文字列を使用
    std::cout << _("Welcome to My Application!") << std::endl;
    std::cout << _("Please enter your name: ");

    std::string name;
    std::getline(std::cin, name);

    // パラメータ付き（printfスタイル）
    printf(_("Hello, %s!\n"), name.c_str());

    // 複数形対応
    int count = 5;
    printf(_n("You have %d new message",
              "You have %d new messages",
              count),
           count);
    std::cout << std::endl;

    // メニュー表示
    std::cout << "\n" << _("Menu:") << std::endl;
    std::cout << "1. " << _("View Profile") << std::endl;
    std::cout << "2. " << _("Settings") << std::endl;
    std::cout << "3. " << _("Exit") << std::endl;

    return 0;
}
```

**翻訳ファイル生成手順**:

```bash
# 1. 翻訳可能な文字列を抽出 (.pot ファイル生成)
xgettext --keyword=_ --keyword=_n:1,2 --language=C++ \
         --add-comments --sort-output \
         --output=po/myapp.pot \
         src/*.cpp

# 2. 各言語の .po ファイル作成（初回のみ）
msginit --input=po/myapp.pot --locale=ja_JP --output=po/ja/myapp.po
msginit --input=po/myapp.pot --locale=fr_FR --output=po/fr/myapp.po

# 3. .po ファイルを編集（翻訳者が実施）
# 例: po/ja/myapp.po

# 4. 既存の .po ファイルを更新（コード変更時）
msgmerge --update po/ja/myapp.po po/myapp.pot

# 5. .mo ファイルにコンパイル
msgfmt --output-file=locale/ja/LC_MESSAGES/myapp.mo po/ja/myapp.po
msgfmt --output-file=locale/fr/LC_MESSAGES/myapp.mo po/fr/myapp.po
```

**po/ja/myapp.po** (日本語翻訳例):

```po
# Japanese translation for myapp
msgid ""
msgstr ""
"Project-Id-Version: myapp 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Language: ja\n"

msgid "Welcome to My Application!"
msgstr "私のアプリケーションへようこそ！"

msgid "Please enter your name: "
msgstr "お名前を入力してください: "

msgid "Hello, %s!\n"
msgstr "こんにちは、%sさん！\n"

# 複数形
msgid "You have %d new message"
msgid_plural "You have %d new messages"
msgstr[0] "%d 件の新しいメッセージがあります"

msgid "Menu:"
msgstr "メニュー:"

msgid "View Profile"
msgstr "プロフィールを表示"

msgid "Settings"
msgstr "設定"

msgid "Exit"
msgstr "終了"
```

**CMakeLists.txt** (ビルド統合):

```cmake
cmake_minimum_required(VERSION 3.10)
project(myapp)

set(CMAKE_CXX_STANDARD 17)

# gettext ライブラリを探す
find_package(Gettext REQUIRED)
find_package(Intl REQUIRED)

# 実行ファイル
add_executable(myapp src/main.cpp)

# インクルードディレクトリ
target_include_directories(myapp PRIVATE ${Intl_INCLUDE_DIRS})

# ライブラリリンク
target_link_libraries(myapp PRIVATE ${Intl_LIBRARIES})

# .po ファイルから .mo ファイルを生成
set(LANGUAGES ja fr de)
set(PO_DIR ${CMAKE_SOURCE_DIR}/po)
set(LOCALE_DIR ${CMAKE_BINARY_DIR}/locale)

foreach(LANG ${LANGUAGES})
    set(PO_FILE ${PO_DIR}/${LANG}/myapp.po)
    set(MO_DIR ${LOCALE_DIR}/${LANG}/LC_MESSAGES)
    set(MO_FILE ${MO_DIR}/myapp.mo)

    # ディレクトリ作成
    file(MAKE_DIRECTORY ${MO_DIR})

    # カスタムコマンド: .po → .mo
    add_custom_command(
        OUTPUT ${MO_FILE}
        COMMAND ${GETTEXT_MSGFMT_EXECUTABLE} -o ${MO_FILE} ${PO_FILE}
        DEPENDS ${PO_FILE}
        COMMENT "Compiling ${LANG} translation"
    )

    list(APPEND MO_FILES ${MO_FILE})
endforeach()

# すべての .mo ファイルをビルド
add_custom_target(translations ALL DEPENDS ${MO_FILES})
add_dependencies(myapp translations)

# インストール
install(DIRECTORY ${LOCALE_DIR}/ DESTINATION share/locale)
```

---

### 2. ICU による高度な国際化

**ICU 使用例**:

```cpp
#include <iostream>
#include <unicode/ucnv.h>
#include <unicode/unistr.h>
#include <unicode/datefmt.h>
#include <unicode/numfmt.h>
#include <unicode/plurrule.h>
#include <unicode/msgfmt.h>

using namespace icu;

int main() {
    UErrorCode status = U_ZERO_ERROR;

    // 1. Unicode文字列処理
    UnicodeString text("Hello, 世界! 你好!");
    std::cout << "Length: " << text.length() << " characters" << std::endl;

    // 2. 日付フォーマット（ロケール別）
    Locale localeJa("ja_JP");
    Locale localeEn("en_US");

    DateFormat* dateFormatJa = DateFormat::createDateInstance(
        DateFormat::kFull, localeJa);
    DateFormat* dateFormatEn = DateFormat::createDateInstance(
        DateFormat::kFull, localeEn);

    UDate now = Calendar::getNow();
    UnicodeString dateJa, dateEn;

    dateFormatJa->format(now, dateJa);
    dateFormatEn->format(now, dateEn);

    std::string dateJaUtf8, dateEnUtf8;
    dateJa.toUTF8String(dateJaUtf8);
    dateEn.toUTF8String(dateEnUtf8);

    std::cout << "Date (ja): " << dateJaUtf8 << std::endl;
    std::cout << "Date (en): " << dateEnUtf8 << std::endl;

    // 3. 数値フォーマット（通貨）
    NumberFormat* currencyJa = NumberFormat::createCurrencyInstance(
        localeJa, status);
    NumberFormat* currencyEn = NumberFormat::createCurrencyInstance(
        localeEn, status);

    double amount = 1234567.89;
    UnicodeString currencyJaStr, currencyEnStr;

    currencyJa->format(amount, currencyJaStr);
    currencyEn->format(amount, currencyEnStr);

    std::string currencyJaUtf8, currencyEnUtf8;
    currencyJaStr.toUTF8String(currencyJaUtf8);
    currencyEnStr.toUTF8String(currencyEnUtf8);

    std::cout << "Currency (ja): " << currencyJaUtf8 << std::endl;
    std::cout << "Currency (en): " << currencyEnUtf8 << std::endl;

    // 4. 複数形ルール
    PluralRules* pluralRulesEn = PluralRules::forLocale(localeEn, status);

    for (int i = 0; i <= 5; i++) {
        UnicodeString keyword = pluralRulesEn->select(i);
        std::string keywordUtf8;
        keyword.toUTF8String(keywordUtf8);
        std::cout << i << " -> " << keywordUtf8 << std::endl;
    }

    // 5. MessageFormat (パラメータ付きメッセージ)
    UnicodeString pattern("{0} has {1, plural, "
                          "one {# apple} "
                          "other {# apples}}.");

    MessageFormat msgFormat(pattern, localeEn, status);

    UnicodeString name("Alice");
    int appleCount = 3;

    Formattable args[] = { name, appleCount };
    UnicodeString result;
    msgFormat.format(args, 2, result, status);

    std::string resultUtf8;
    result.toUTF8String(resultUtf8);
    std::cout << "Message: " << resultUtf8 << std::endl;

    // クリーンアップ
    delete dateFormatJa;
    delete dateFormatEn;
    delete currencyJa;
    delete currencyEn;
    delete pluralRulesEn;

    return 0;
}
```

**CMakeLists.txt** (ICU):

```cmake
cmake_minimum_required(VERSION 3.10)
project(icu_example)

set(CMAKE_CXX_STANDARD 17)

# ICU を探す
find_package(ICU REQUIRED COMPONENTS uc i18n)

add_executable(icu_example main.cpp)

target_include_directories(icu_example PRIVATE ${ICU_INCLUDE_DIRS})
target_link_libraries(icu_example PRIVATE ${ICU_LIBRARIES})
```

---

### 3. Boost.Locale (C++標準風API)

```cpp
#include <boost/locale.hpp>
#include <iostream>

using namespace boost::locale;

int main() {
    // ロケールジェネレーター
    generator gen;

    // サポートロケール追加
    gen.add_messages_path("./locale");
    gen.add_messages_domain("myapp");

    // ロケール設定
    std::locale::global(gen("ja_JP.UTF-8"));
    std::cout.imbue(std::locale());

    // 翻訳
    std::cout << translate("Welcome!") << std::endl;
    std::cout << translate("Hello, {1}!").str("田中") << std::endl;

    // 複数形
    std::cout << format(translate("You have {1} message",
                                  "You have {1} messages",
                                  5)) % 5
              << std::endl;

    // 日付フォーマット
    auto now = std::time(nullptr);
    std::cout << as::date << std::put_time(std::localtime(&now), "%x")
              << std::endl;

    // 通貨
    std::cout << as::currency << 1234.56 << std::endl;

    return 0;
}
```

---

## ベストプラクティス

### .NET

1. **IStringLocalizer 使用**: ResourceManager より推奨
2. **リソース配置**: コントローラー/ビュー別に整理
3. **ハードコード回避**: すべての文字列をリソース化
4. **文化フォールバック**: `ja-JP` → `ja` → デフォルト
5. **キャッシング**: パフォーマンス向上
6. **データアノテーション**: バリデーションメッセージも国際化

### C++

1. **gettext 優先**: 翻訳管理に最適
2. **ICU 併用**: 日付・通貨・複数形はICU
3. **UTF-8 統一**: すべての文字列をUTF-8
4. **マクロ使用**: `_()` でシンプルに
5. **コンテキスト**: pgettext でキー重複回避
6. **自動抽出**: xgettext で翻訳文字列抽出

---

## 翻訳ワークフロー

### 1. 文字列抽出

**.NET**:
```bash
# カスタムツールで .resx から未翻訳キーを抽出
dotnet run --project LocalizationTool extract --output missing.csv
```

**C++**:
```bash
# xgettext で翻訳可能文字列を抽出
xgettext --keyword=_ --output=messages.pot src/**/*.cpp
```

### 2. 翻訳

- **手動翻訳**: Poedit、Lokalize などのGUIツール
- **機械翻訳**: DeepL/Google Translate API統合
- **翻訳サービス**: Crowdin、Lokalise、Phrase

### 3. 品質チェック

```bash
# .NET: 重複キー検出
dotnet run --project LocalizationTool validate

# C++: .po ファイル検証
msgfmt --check-format --check-header ja.po
```

### 4. 進捗レポート

```
Translation Progress
====================
Japanese (ja):   100% ✅ (250/250)
Chinese (zh):     85% ⚠️  (213/250)
Spanish (es):     60% ❌ (150/250)

Missing in Chinese:
  - Settings.Privacy.DeleteAccount
  - Checkout.Payment.ApplePay
  ...
```

---

## 高度な機能

### 複数形ルール

**.NET** (.resx):
```xml
<data name="ItemCount" xml:space="preserve">
  <value>{0} items</value>
</data>
```

**C++** (gettext):
```po
msgid "%d item"
msgid_plural "%d items"
msgstr[0] "%d 個のアイテム"  # 日本語は単複同形
```

### 日付・通貨フォーマット

**.NET**:
```csharp
var date = DateTime.Now;
var formattedDate = date.ToString("D", CultureInfo.CurrentCulture);

var price = 1234.56m;
var formattedPrice = price.ToString("C", CultureInfo.CurrentCulture);
// ja-JP: ¥1,235
// en-US: $1,234.56
```

**C++** (ICU):
```cpp
NumberFormat* fmt = NumberFormat::createCurrencyInstance(Locale("ja_JP"), status);
UnicodeString result;
fmt->format(1234.56, result);
// ¥1,235
```

---

## ツールとユーティリティ

### .NET ツール

- **ResXManager** - Visual Studio拡張
- **Zeta Resource Editor** - スタンドアロンエディター
- **Lokalise.NET** - APIクライアント

### C++ ツール

- **Poedit** - .po ファイルエディター（GUI）
- **gettext utilities** - xgettext, msgfmt, msgmerge
- **translate-toolkit** - Pythonベース変換ツール

---

## 統合例

### 例1: ASP.NET Core Web API

```
ASP.NET Core Web APIに多言語対応:
- API レスポンスメッセージ
- バリデーションエラー
- Accept-Language ヘッダー対応
言語: 英語、日本語、中国語
```

### 例2: WPF デスクトップアプリ

```
WPF 在庫管理アプリを多言語化:
- すべてのUI要素
- メッセージボックス
- レポート出力
- ランタイム言語切り替え
言語: 英語、日本語、ドイツ語、スペイン語
```

### 例3: C++ クロスプラットフォームCLI

```
C++ コマンドラインツールにgettext統合:
- ヘルプメッセージ
- エラーメッセージ
- 進捗表示
- 環境変数でロケール切り替え
言語: 英語、日本語、フランス語
```

---

## 制限事項

- **.NET**: リソースファイルはコンパイル時埋め込み（動的追加不可）
- **C++**: gettext はランタイムで .mo ファイル必要
- **ICU**: ライブラリサイズが大きい（30MB+）
- **複数形**: 言語により複数形ルールが異なる

## バージョン情報

- スキルバージョン: 1.0.0
- 対応 .NET: .NET Core 3.1+, .NET 6/7/8/9
- 対応 C++: C++11 以上
- 最終更新: 2025-11-22

---

**使用例**:

```
ASP.NET Core MVC プロジェクトに国際化を追加：

言語: 英語（デフォルト）、日本語、中国語
リソース配置: Resources/
機能:
- すべてのビュー、コントローラー
- データアノテーション
- クッキーベース言語切り替え
- 日付・通貨のロケール別フォーマット

完全な実装コード、設定ファイル、リソースファイルを生成してください。
```

または

```
C++ デスクトップアプリケーションにgettextを統合：

ライブラリ: gettext
言語: 英語、日本語、ドイツ語
機能:
- すべてのUI文字列
- エラーメッセージ
- 複数形対応
- CMake ビルド統合

セットアップコード、翻訳ファイル、ビルドスクリプトを生成してください。
```

エンタープライズレベルの国際化が実装されます！
