---
name: roslyn-analyzers
description: >
  USE FOR: Writing custom Roslyn diagnostic analyzers and code fix providers that report warnings
  and errors during compilation, and optionally provide automated code transformations.
  DO NOT USE FOR: Source generators that emit new files (use IIncrementalGenerator), post-compilation
  IL weaving (use Fody), or standalone static analysis tools (use NDepend or Semgrep).
license: MIT
metadata:
  displayName: Roslyn Analyzers
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Roslyn Analyzers Overview"
    url: "https://learn.microsoft.com/en-us/visualstudio/code-quality/roslyn-analyzers-overview"
  - title: "dotnet/roslyn-analyzers GitHub Repository"
    url: "https://github.com/dotnet/roslyn-analyzers"
  - title: "Microsoft.CodeAnalysis.NetAnalyzers NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.CodeAnalysis.NetAnalyzers"
---

# Roslyn Analyzers

## Overview

Roslyn analyzers are components that plug into the C# and VB.NET compilers to perform custom static analysis during compilation. They report diagnostics (errors, warnings, info messages) and can optionally provide code fix providers that offer automated refactorings through the IDE lightbulb menu. Analyzers are distributed as NuGet packages and run in both the IDE (real-time) and during `dotnet build` (batch).

The Roslyn analyzer API provides access to the syntax tree (textual structure), semantic model (type information and symbol resolution), and control/data flow analysis. Analyzers register callbacks for specific syntax nodes, symbols, operations, or compilation events.

## Project Setup

Analyzer projects target `netstandard2.0` and reference the Roslyn compiler APIs.

```xml
<!-- MyAnalyzers.csproj -->
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <EnforceExtendedAnalyzerRules>true</EnforceExtendedAnalyzerRules>
    <IsRoslynComponent>true</IsRoslynComponent>
    <GeneratePackageOnBuild>true</GeneratePackageOnBuild>
    <IncludeBuildOutput>false</IncludeBuildOutput>
    <DevelopmentDependency>true</DevelopmentDependency>
    <NoPackageAnalysis>true</NoPackageAnalysis>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.3.4"
                      PrivateAssets="all" />
    <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.8.0"
                      PrivateAssets="all" />
  </ItemGroup>

  <!-- Pack analyzer DLL into the analyzers/dotnet/cs folder -->
  <ItemGroup>
    <None Include="$(OutputPath)\$(AssemblyName).dll"
          Pack="true"
          PackagePath="analyzers/dotnet/cs"
          Visible="false" />
  </ItemGroup>
</Project>
```

## Writing a Diagnostic Analyzer

Analyzers inherit from `DiagnosticAnalyzer` and register analysis callbacks.

```csharp
using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;

namespace MyAnalyzers;

[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class AsyncMethodNamingAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "MA001";

    private static readonly DiagnosticDescriptor Rule = new(
        id: DiagnosticId,
        title: "Async method should end with 'Async'",
        messageFormat: "Method '{0}' returns Task but does not end with 'Async'",
        category: "Naming",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        helpLinkUri: "https://learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide1006");

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics =>
        ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        context.ConfigureGeneratedCodeAnalysis(
            GeneratedCodeAnalysisFlags.None);
        context.EnableConcurrentExecution();

        context.RegisterSymbolAction(AnalyzeMethod, SymbolKind.Method);
    }

    private static void AnalyzeMethod(SymbolAnalysisContext context)
    {
        var method = (IMethodSymbol)context.Symbol;

        // Skip if already ends with Async
        if (method.Name.EndsWith("Async"))
            return;

        // Skip special methods
        if (method.IsOverride || method.IsImplicitlyDeclared ||
            method.MethodKind != MethodKind.Ordinary)
            return;

        // Check if return type is Task or Task<T>
        INamedTypeSymbol? returnType = method.ReturnType as INamedTypeSymbol;
        if (returnType is null)
            return;

        string returnTypeName = returnType.ContainingNamespace?.ToDisplayString() + "." +
                                returnType.MetadataName;

        bool isTaskLike = returnTypeName is "System.Threading.Tasks.Task" or
                          "System.Threading.Tasks.Task`1" or
                          "System.Threading.Tasks.ValueTask" or
                          "System.Threading.Tasks.ValueTask`1";

        if (isTaskLike)
        {
            var diagnostic = Diagnostic.Create(Rule, method.Locations[0], method.Name);
            context.ReportDiagnostic(diagnostic);
        }
    }
}
```

## Writing a Code Fix Provider

Code fix providers offer automated fixes for diagnostics reported by analyzers.

```csharp
using System.Collections.Immutable;
using System.Composition;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CodeActions;
using Microsoft.CodeAnalysis.CodeFixes;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Rename;

namespace MyAnalyzers;

[ExportCodeFixProvider(LanguageNames.CSharp, Name = nameof(AsyncMethodNamingCodeFix))]
[Shared]
public sealed class AsyncMethodNamingCodeFix : CodeFixProvider
{
    public override ImmutableArray<string> FixableDiagnosticIds =>
        ImmutableArray.Create(AsyncMethodNamingAnalyzer.DiagnosticId);

    public override FixAllProvider GetFixAllProvider() =>
        WellKnownFixAllProviders.BatchFixer;

    public override async Task RegisterCodeFixesAsync(CodeFixContext context)
    {
        var root = await context.Document.GetSyntaxRootAsync(context.CancellationToken);
        if (root is null) return;

        var diagnostic = context.Diagnostics[0];
        var diagnosticSpan = diagnostic.Location.SourceSpan;

        var declaration = root.FindToken(diagnosticSpan.Start)
            .Parent?
            .AncestorsAndSelf()
            .OfType<MethodDeclarationSyntax>()
            .First();

        if (declaration is null) return;

        string newName = declaration.Identifier.Text + "Async";

        context.RegisterCodeFix(
            CodeAction.Create(
                title: $"Rename to '{newName}'",
                createChangedSolution: ct => RenameMethodAsync(
                    context.Document, declaration, newName, ct),
                equivalenceKey: DiagnosticId),
            diagnostic);
    }

    private static async Task<Solution> RenameMethodAsync(
        Document document,
        MethodDeclarationSyntax declaration,
        string newName,
        CancellationToken cancellationToken)
    {
        var semanticModel = await document.GetSemanticModelAsync(cancellationToken);
        if (semanticModel is null) return document.Project.Solution;

        var symbol = semanticModel.GetDeclaredSymbol(declaration, cancellationToken);
        if (symbol is null) return document.Project.Solution;

        return await Renamer.RenameSymbolAsync(
            document.Project.Solution,
            symbol,
            new SymbolRenameOptions(),
            newName,
            cancellationToken);
    }

    private const string DiagnosticId = AsyncMethodNamingAnalyzer.DiagnosticId;
}
```

## Syntax-Based Analyzer

Analyzers can also register for specific syntax node types for pattern detection.

```csharp
using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;

namespace MyAnalyzers;

[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class EmptyCatchBlockAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "MA002";

    private static readonly DiagnosticDescriptor Rule = new(
        id: DiagnosticId,
        title: "Empty catch block swallows exceptions",
        messageFormat: "Catch block is empty; exceptions will be silently swallowed",
        category: "Reliability",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true);

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics =>
        ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        context.EnableConcurrentExecution();
        context.RegisterSyntaxNodeAction(AnalyzeCatchClause, SyntaxKind.CatchClause);
    }

    private static void AnalyzeCatchClause(SyntaxNodeAnalysisContext context)
    {
        var catchClause = (CatchClauseSyntax)context.Node;

        // Check if catch block has no statements and no comments
        if (catchClause.Block.Statements.Count == 0 &&
            !catchClause.Block.DescendantTrivia()
                .Any(t => t.IsKind(SyntaxKind.SingleLineCommentTrivia) ||
                          t.IsKind(SyntaxKind.MultiLineCommentTrivia)))
        {
            context.ReportDiagnostic(
                Diagnostic.Create(Rule, catchClause.CatchKeyword.GetLocation()));
        }
    }
}
```

## Registration Method Comparison

| Registration Method                    | Scope                        | Use Case                                |
|----------------------------------------|------------------------------|-----------------------------------------|
| `RegisterSymbolAction`                 | Named symbols                | Naming conventions, accessibility checks |
| `RegisterSyntaxNodeAction`             | Specific syntax node kinds   | Pattern detection, anti-patterns        |
| `RegisterOperationAction`              | IOperation (semantic ops)    | Data flow, assignment analysis          |
| `RegisterCompilationStartAction`       | Full compilation scope       | Cross-file analysis, type collection     |
| `RegisterSyntaxTreeAction`             | Per syntax tree              | File-level checks (line count, etc.)    |
| `RegisterCodeBlockAction`              | Method/property bodies       | Control flow within a single member     |
| `RegisterAdditionalFileAction`         | Non-C# files in project     | Configuration file validation           |

## Unit Testing Analyzers

```csharp
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Testing;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using VerifyCS = Microsoft.CodeAnalysis.CSharp.Testing.CSharpAnalyzerVerifier<
    MyAnalyzers.AsyncMethodNamingAnalyzer,
    Microsoft.CodeAnalysis.Testing.DefaultVerifier>;

namespace MyAnalyzers.Tests;

[TestClass]
public class AsyncMethodNamingAnalyzerTests
{
    [TestMethod]
    public async Task Method_ReturningTask_WithoutAsyncSuffix_ReportsDiagnostic()
    {
        string source = """
            using System.Threading.Tasks;

            public class MyClass
            {
                public Task {|#0:GetData|}()
                {
                    return Task.CompletedTask;
                }
            }
            """;

        var expected = VerifyCS.Diagnostic(AsyncMethodNamingAnalyzer.DiagnosticId)
            .WithLocation(0)
            .WithArguments("GetData");

        await VerifyCS.VerifyAnalyzerAsync(source, expected);
    }

    [TestMethod]
    public async Task Method_ReturningTask_WithAsyncSuffix_NoDiagnostic()
    {
        string source = """
            using System.Threading.Tasks;

            public class MyClass
            {
                public Task GetDataAsync()
                {
                    return Task.CompletedTask;
                }
            }
            """;

        await VerifyCS.VerifyAnalyzerAsync(source);
    }
}
```

## Best Practices

1. **Always call `context.EnableConcurrentExecution()` and `context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None)` in `Initialize`** to allow the compiler to run your analyzer in parallel and skip generated code, both of which are required for good IDE performance.

2. **Define diagnostic IDs with a consistent prefix (e.g., `MA001`) and maintain a public constants class** so that consumers can reference diagnostic IDs in `.editorconfig` severity overrides and `SuppressMessage` attributes.

3. **Provide a `helpLinkUri` in every `DiagnosticDescriptor`** that points to documentation explaining why the diagnostic is reported and how to fix it, so developers can understand the rule without reading analyzer source code.

4. **Use `RegisterSymbolAction` for naming and accessibility rules, `RegisterSyntaxNodeAction` for pattern detection, and `RegisterOperationAction` for semantic analysis** to match the right level of abstraction to the analysis task.

5. **Implement `GetFixAllProvider()` returning `WellKnownFixAllProviders.BatchFixer` in code fix providers** so that users can fix all instances of a diagnostic across a document, project, or solution in a single action.

6. **Target `netstandard2.0` and set `EnforceExtendedAnalyzerRules` to `true`** because the compiler loads analyzers in a restricted context; this setting surfaces violations of analyzer design rules at build time.

7. **Pack the analyzer DLL into `analyzers/dotnet/cs` in the NuGet package** using the `None` item with `PackagePath` so that consuming projects automatically load the analyzer without explicit project references.

8. **Use the `Microsoft.CodeAnalysis.Testing` framework for unit tests with the `VerifyAnalyzerAsync` pattern** which handles compilation setup, reference resolution, and diagnostic location matching automatically.

9. **Skip compiler-generated symbols by checking `IsImplicitlyDeclared` and filter out `MethodKind.PropertyGet`, `MethodKind.PropertySet`, etc.** to avoid reporting diagnostics on auto-generated backing methods that developers cannot fix.

10. **Test both positive cases (diagnostic reported) and negative cases (no diagnostic) for every rule** to prevent false positives, which erode developer trust and lead to teams disabling the analyzer entirely.
