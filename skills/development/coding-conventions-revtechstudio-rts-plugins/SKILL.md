---
name: coding-conventions
description: .NET/C#のコーディング規約、命名規則、レイアウト、C# 12/13/14の最新機能活用ガイドラインを定義する。C#/.NETコード作成時、クラス・メソッド命名時、コードフォーマット時、またはユーザーがコーディング規約、命名規則、C#ベストプラクティス、Primary Constructors、Collection Expressions、field キーワードに言及した際に使用する。
---

# Coding Conventions

## 概要

このSkillは、開発されるすべての.NETプロジェクトに適用されるコーディング規約を定義する。.NET 8以降の最新機能（C# 12/13/14、.NET 8/9/10）を積極的に活用し、可読性、保守性、パフォーマンスの高いコードを実現することを目的とする。

## 責任範囲

このSkillは以下の範囲をカバーする:

- .NET/C#の最新機能（C# 12/13/14、.NET 8/9/10）の活用方針
- 命名規則（型、メンバー、変数、パラメータ）
- コードレイアウトとフォーマット
- 言語機能の使用方針（型推論、コレクション、例外処理）
- LINQとラムダ式のベストプラクティス
- モダンC#構文の推奨パターン

## 基本方針

- .NET 8以降の最新機能を積極的に使用する（C# 12/13/14、.NET 8/9/10）
- 古いバージョンとの互換性が必要な場合を除き、常に最新機能を優先する
- 古い言語構文は避ける
- **重要: アンダースコアプレフィックス（`_field`）の使用は絶対に禁止する**
- **重要: 中括弧の省略は絶対に禁止する（1行で記述できる場合でも省略不可）**
- Microsoftの公式コーディング規約に従う
- 一貫性を保ち、チーム全体で同じスタイルを適用する

## .NET/C#の最新機能（バージョン別）

.NET 8以降の各バージョンで導入された主要機能を積極的に活用する。古いバージョンとの互換性が必要な場合を除き、常に最新の機能を優先的に使用する。

### C# 12 (.NET 8) - 2023年11月リリース

#### Primary Constructors

- クラスやstructの宣言でパラメータを定義し、クラス全体で使用できる
- 明示的なフィールド宣言を削減し、初期化を簡潔にする

良い例:

```csharp
public class Person(string name, int age)
{
    public string Name => name;
    public int Age => age;

    public void Display()
    {
        Console.WriteLine($"{name} is {age} years old");
    }
}
```

悪い例:

```csharp
public class Person
{
    private string name;
    private int age;

    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
    }

    public string Name => name;
    public int Age => age;
}
```

#### Collection Expressions

- 括弧とスプレッド演算子を使用してコレクションを簡潔に作成する
- 複数のコレクションを結合する際に便利

良い例:

```csharp
int[] array = [1, 2, 3, 4, 5];
List<string> list = ["one", "two", "three"];

int[] row0 = [1, 2, 3];
int[] row1 = [4, 5, 6];

// スプレッド演算子で結合
int[] combined = [..row0, ..row1];
```

#### Default Lambda Parameters

- ラムダ式にデフォルトパラメータ値を指定できる

良い例:

```csharp
var incrementBy = (int source, int increment = 1) => source + increment;

Console.WriteLine(incrementBy(5));
Console.WriteLine(incrementBy(5, 3));
```

#### Alias Any Type

- using ディレクティブで複雑な型に別名を付けられる

良い例:

```csharp
using Point = (int x, int y);
using ProductList = System.Collections.Generic.List<(string Name, decimal Price)>;

Point origin = (0, 0);
ProductList products = [("Product1", 100m), ("Product2", 200m)];
```

### C# 13 (.NET 9) - 2024年11月リリース

#### Params Collections

- `params`修飾子が配列以外のコレクション型でも使用可能になった
- `List<T>`, `Span<T>`, `ReadOnlySpan<T>`, `IEnumerable<T>`などで使用できる

良い例:

```csharp
public void ProcessItems(params List<string> items)
{
    foreach (var item in items)
    {
        Console.WriteLine(item);
    }
}

// メモリ効率が重要な場合
public void ProcessData(params ReadOnlySpan<int> data)
{
    foreach (var value in data)
    {
        Process(value);
    }
}
```

#### New Lock Type

- `System.Threading.Lock`型を使用して、より高速なスレッド同期を実現する
- 従来の`Monitor`ベースのロックより高速

良い例:

```csharp
private readonly Lock lockObject = new();

public void UpdateData()
{
    lock (lockObject)
    {
        // クリティカルセクション
    }
}
```

悪い例:

```csharp
// 従来のobjectベースのロック（C# 13では推奨されない）
private readonly object lockObject = new();

public void UpdateData()
{
    lock (lockObject)
    {
        // クリティカルセクション
    }
}
```

#### Partial Properties and Indexers

- partial プロパティとインデクサーが使用可能になった
- 定義と実装を分離できる

良い例:

```csharp
// 定義部分
public partial class DataModel
{
    public partial string Name { get; set; }
}

// 実装部分
public partial class DataModel
{
    private string name;

    public partial string Name
    {
        get => name;
        set => name = value ?? throw new ArgumentNullException(nameof(value));
    }
}
```

#### Implicit Index Access

- オブジェクト初期化子で`^`演算子が使用可能になった

良い例:

```csharp
var countdown = new TimerBuffer
{
    buffer =
    {
        [^1] = 0,
        [^2] = 1,
        [^3] = 2
    }
};
```

#### Ref Struct Enhancements

- `ref struct`型がインターフェースを実装できるようになった
- ジェネリック型で`ref struct`を使用できるようになった（`allows ref struct`制約）

良い例:

```csharp
public ref struct SpanWrapper<T> : IEnumerable<T>
{
    private Span<T> span;

    public IEnumerator<T> GetEnumerator()
    {
        foreach (var item in span)
        {
            yield return item;
        }
    }
}
```

### C# 14 (.NET 10) - 2025年11月リリース

#### Extension Members

- Extension Membersを活用してクリーンなAPI拡張を実現する
- 元の型を汚染せずに機能を追加できる

良い例:

```csharp
extension<TSource>(IEnumerable<TSource> source)
{
    public bool IsEmpty => !source.Any();
    public int Count => source.Count();
}
```

### Field-Backed Properties

- `field`キーワードを使用して明示的なバッキングフィールドを削減する
- バリデーションロジックを簡潔に記述できる
- **アンダースコアプレフィックスを使用した明示的なバッキングフィールドは絶対に禁止**

良い例:

```csharp
// C# 14のfieldキーワードを使用
public string Name
{
    get;
    set => field = value ?? throw new ArgumentNullException(nameof(value));
}

// やむを得ず明示的なバッキングフィールドが必要な場合もアンダースコアなし
private string name;

public string Name
{
    get => name;
    set => name = value ?? throw new ArgumentNullException(nameof(value));
}
```

悪い例:

```csharp
// アンダースコアプレフィックスは絶対に禁止
private string _name;

public string Name
{
    get => _name;
    set => _name = value ?? throw new ArgumentNullException(nameof(value));
}
```

### Null-Conditional Assignment

- `?.`を使用してnullチェックを簡潔に記述する
- 冗長なnullチェックを削減する

良い例:

```csharp
customer?.Order = GetCurrentOrder();
```

悪い例:

```csharp
if (customer != null)
{
    customer.Order = GetCurrentOrder();
}
```

### Implicit Span Conversions

- パフォーマンス重視のコードでは`Span<T>`と`ReadOnlySpan<T>`を活用する
- 配列とスパン型の間の自動変換を利用する

## 命名規則

### Pascal Casing

- 型名（class, record, struct, interface, enum）
- パブリックメンバー（プロパティ、メソッド、イベント）
- 名前空間

良い例:

```csharp
public class CustomerOrder
{
    public string OrderId { get; set; }
    public void ProcessOrder() { }
}
```

### Camel Casing

- ローカル変数
- メソッドパラメータ
- プライベートフィールド（**アンダースコアプレフィックスは絶対に使用しない**）

良い例:

```csharp
public class OrderProcessor
{
    // アンダースコアなし
    private string customerName;

    // アンダースコアなし
    private int orderCount;

    public void ProcessOrder(string orderId)
    {
        var customerName = GetCustomerName(orderId);
        string processedResult = Process(customerName);
    }
}
```

悪い例:

```csharp
public class OrderProcessor
{
    // アンダースコアプレフィックスは絶対に禁止
    private string _customerName;

    // アンダースコアプレフィックスは絶対に禁止
    private int _orderCount;
}
```

### Interface命名

- 接頭辞`I`を使用する

良い例:

```csharp
public interface IOrderProcessor
{
    void Process(Order order);
}
```

### 型パラメータ命名

- 接頭辞`T`を使用する
- 意味のある名前を付ける

良い例:

```csharp
public class Repository<TEntity> where TEntity : class
{
    public void Add(TEntity entity) { }
}
```

## コードレイアウト

### インデント

- スペース4個を使用する
- タブは使用しない

### 波括弧

- Allmanスタイル（開始括弧と終了括弧を別の行に配置）
- **中括弧の省略は絶対に禁止する（1行で記述できる場合でも必ず中括弧を使用）**

良い例:

```csharp
public void ProcessOrder(Order order)
{
    if (order != null)
    {
        order.Process();
    }
}

// 1行でも中括弧を使用する
if (isValid)
{
    Execute();
}

for (int i = 0; i < 10; i++)
{
    Process(i);
}
```

悪い例:

```csharp
// 中括弧の省略は禁止
if (isValid)
    Execute();

// 中括弧の省略は禁止
for (int i = 0; i < 10; i++)
    Process(i);

// 中括弧の省略は禁止
if (order != null) order.Process();
```

### 行の記述

- 1行に1つのステートメントのみ記述する
- 1行に1つの宣言のみ記述する
- メソッド定義とプロパティ定義の間に空行を1行入れる

良い例:

```csharp
public class Order
{
    public string OrderId { get; set; }

    public void Process()
    {
        var result = Validate();
        Execute(result);
    }

    private bool Validate()
    {
        return OrderId != null;
    }
}
```

### 名前空間

- ファイルスコープ名前空間を使用する

良い例:

```csharp
namespace YourProject.Orders;

public class OrderProcessor
{
    // 実装
}
```

悪い例:

```csharp
namespace YourProject.Orders
{
    public class OrderProcessor
    {
        // 実装
    }
}
```

### using ディレクティブ

- 名前空間宣言の外側に配置する
- アルファベット順に並べる

良い例:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace YourProject.Orders;
```

## 型と変数

### 型指定

- 言語キーワード（`string`, `int`, `bool`）を使用する
- ランタイム型（`System.String`, `System.Int32`）は使用しない

良い例:

```csharp
string name = "John";
int count = 10;
bool isValid = true;
```

悪い例:

```csharp
String name = "John";
Int32 count = 10;
Boolean isValid = true;
```

### 型推論（var）

- 型が代入から明白な場合のみ`var`を使用する
- 組み込み型は明示的に型を記述する

良い例:

```csharp
// 明白
var orders = new List<Order>();

// 明白
var customer = GetCustomer();

// 組み込み型は明示
int count = 10;

// 組み込み型は明示
string name = "John";
```

悪い例:

```csharp
// 組み込み型でvarは避ける
var count = 10;

// 組み込み型でvarは避ける
var name = "John";
```

## 文字列

### 文字列補間

- 短い文字列の連結には文字列補間を使用する

良い例:

```csharp
string message = $"Order {orderId} processed successfully";
```

悪い例:

```csharp
string message = "Order " + orderId + " processed successfully";
```

### StringBuilder

- ループ内で大量のテキストを追加する場合は`StringBuilder`を使用する

良い例:

```csharp
var builder = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    builder.Append($"Line {i}\n");
}
```

### Raw String Literals

- エスケープシーケンスよりもRaw String Literalsを優先する

良い例:

```csharp
string json = """
{
    "name": "John",
    "age": 30
}
""";
```

## コレクションとオブジェクト初期化

### コレクションの初期化

- C# 12以降のCollection Expressionsを使用する（前述の「C# 12の最新機能」を参照）

### オブジェクト初期化子

- オブジェクト初期化子を使用して生成を簡潔にする

良い例:

```csharp
var customer = new Customer
{
    Name = "John",
    Email = "john@example.com"
};
```

## 例外処理

### 具体的な例外のキャッチ

- 一般的な`System.Exception`ではなく具体的な例外をキャッチする

良い例:

```csharp
try
{
    ProcessOrder(order);
}
catch (ArgumentNullException ex)
{
    Logger.Error("Order is null", ex);
}
```

悪い例:

```csharp
try
{
    ProcessOrder(order);
}
catch (Exception ex) // 一般的すぎる
{
    Logger.Error("Error", ex);
}
```

### usingステートメント

- try-finallyの代わりに`using`ステートメントを使用する

良い例:

```csharp
using var connection = new SqlConnection(connectionString);
connection.Open();
// 処理
```

悪い例:

```csharp
SqlConnection connection = null;
try
{
    connection = new SqlConnection(connectionString);
    connection.Open();
    // 処理
}
finally
{
    connection?.Dispose();
}
```

## LINQ

### 意味のある変数名

- クエリ変数には意味のある名前を使用する

良い例:

```csharp
var activeCustomers = from customer in customers
                      where customer.IsActive
                      select customer;
```

### 早期フィルタリング

- `where`句を使用して早期にデータをフィルタリングする

良い例:

```csharp
var result = customers
    .Where(c => c.IsActive)
    .Select(c => c.Name)
    .ToList();
```

### 暗黙的型指定

- LINQ宣言では暗黙的型指定を使用する

良い例:

```csharp
var query = from customer in customers
            where customer.IsActive
            select customer;
```

## ラムダ式

### イベントハンドラ

- 削除が不要なハンドラにはラムダ式を使用する

良い例:

```csharp
button.Click += (s, e) => ProcessClick();
```

### パラメータ修飾子

- C# 14の機能を活用して型推論を維持しながら修飾子を使用する

良い例:

```csharp
TryParse<int> parse = (text, out result) => int.TryParse(text, out result);
```

## コメント

### 単一行コメント

- 簡潔な説明には`//`を使用する
- コメント区切り文字の後にスペースを1つ入れる
- **コメントは必ず単独の行に記述する（コードと同じ行には記述しない）**
- コメントの前には空行を1行入れる

良い例:

```csharp
// 顧客の注文を処理する
ProcessOrder(order);

var processor = new OrderProcessor();

// 注文を実行する
var result = processor.ProcessOrder(order);
```

悪い例:

```csharp
ProcessOrder(order); // 顧客の注文を処理する（コードと同じ行は禁止）
var result = processor.ProcessOrder(order); // 注文を実行する（コードと同じ行は禁止）
var processor = new OrderProcessor();
// この行の前に空行がない（悪い例）
var result = processor.ProcessOrder(order);
```

### XMLドキュメント

- パブリックメンバーにはXMLドキュメントを使用する

良い例:

```csharp
/// <summary>
/// 指定された注文を処理する
/// </summary>
/// <param name="order">処理する注文</param>
/// <returns>処理結果</returns>
public bool ProcessOrder(Order order)
{
    // 実装
}
```

## 静的メンバー

### クラス名による呼び出し

- 静的メンバーはクラス名を介して呼び出す

良い例:

```csharp
var result = OrderProcessor.ProcessOrder(order);
```

悪い例:

```csharp
var processor = new OrderProcessor();

// 静的メソッドをインスタンス経由で呼び出すのは誤解を招く
var result = processor.ProcessOrder(order);
```

## チェックリスト

### コード作成前

- [ ] .NET/C#の最新機能（C# 12/13/14）を把握している
- [ ] プロジェクトのターゲットフレームワークが.NET 8以降に設定されている
- [ ] 命名規則を理解している

### コード作成中

**必須ルール:**

- [ ] **アンダースコアプレフィックスを絶対に使用していない**
- [ ] **中括弧を省略していない（1行でも必ず使用している）**
- [ ] **コメントは必ず単独の行に記述している（コードと同じ行に記述していない）**
- [ ] **コメントの前に空行を1行入れている**

**C# 12以降の機能:**

- [ ] Primary Constructorsを使用している（該当する場合）
- [ ] Collection Expressionsを使用している
- [ ] Default Lambda Parametersを活用している（該当する場合）
- [ ] Alias Any Typeで複雑な型に別名を付けている（該当する場合）

**C# 13以降の機能:**

- [ ] Params Collectionsを使用している（該当する場合）
- [ ] New Lock Typeを使用している（スレッド同期が必要な場合）
- [ ] Partial Properties and Indexersを活用している（該当する場合）
- [ ] Implicit Index Accessをオブジェクト初期化子で使用している（該当する場合）

**C# 14以降の機能:**

- [ ] `field`キーワードを使用してバッキングフィールドを簡潔に記述している
- [ ] Extension Membersを活用している（該当する場合）
- [ ] Null-Conditional Assignmentを活用している
- [ ] Lambda Parameters with Modifiersを使用している（該当する場合）

**基本規則:**

- [ ] ファイルスコープ名前空間を使用している
- [ ] 言語キーワード（`string`, `int`）を使用している
- [ ] `var`を適切に使用している（型が明白な場合のみ）
- [ ] 文字列補間を使用している
- [ ] Raw String Literalsを使用している（該当する場合）
- [ ] Object Initializersを使用している
- [ ] `using`ステートメントを使用している
- [ ] 具体的な例外をキャッチしている
- [ ] LINQ式で早期フィルタリングを実施している
- [ ] 意味のある変数名を使用している
- [ ] コメントが簡潔で明確である
- [ ] パブリックメンバーにXMLドキュメントを記述している
- [ ] Allmanスタイルで波括弧を配置している
- [ ] インデントにスペース4個を使用している

### コード作成後

- [ ] コードが一貫したスタイルで記述されている
- [ ] .NET 8以降の最新機能（C# 12/13/14）を活用している
- [ ] 命名規則に従っている
- [ ] 可読性が高く保守しやすいコードである
