---
name: dotnet-runfile
description: How to use the .NET 10 `dotnet run app.cs` feature. Use this skill when you need to run an existing single-file C# script, create a new C# script, run an ad-hoc C# script (e.g. to test the behavior of a C# snippet), or work on an existing C# script already in the repo. Covers how to run C# scripts and their syntax.
---

# dotnet run app.cs

Run C# files directly without `.csproj` project files. Requires .NET 10 (SpeedReader uses .NET 10, so this should already be installed).

```bash
dotnet run hello.cs
```

## Usage Examples

```csharp
#!/usr/bin/env dotnet run           // shebang (unix)
#:sdk Microsoft.NET.Sdk             // sdk (default; also .Web, .Worker)
#:package Humanizer@2.14.1          // nuget package (version required, wildcards ok)
#:property LangVersion=preview      // msbuild property
#:project ../src/MyLibrary          // project reference

Console.WriteLine("Hello, World!");
```

```bash
dotnet run hello.cs                   # run
dotnet run hello.cs -- arg1 arg2      # run with args
chmod +x hello.cs && ./hello.cs       # run via shebang
cat hello.cs | dotnet run -           # run from stdin
dotnet publish hello.cs -c Release    # publish
dotnet project convert hello.cs       # convert to full project w/ csproj
```

## Shared Configuration

Share settings across multiple single-file apps by placing a `Directory.Build.props` file in the same or parent directory:

```xml
<Project>
  <PropertyGroup>
    <LangVersion>preview</LangVersion>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  </ItemGroup>
</Project>
```

All `.cs` files in that directory tree inherit these settings.
