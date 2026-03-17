---
name: build-addin
description: TODO
---
---
description: Build the SolidLink C# Add-in
---
// turbo-all
1. Build the solution using MSBuild
```powershell
$roslynPath = "C:\Users\mattg\OneDrive\Documents\Projects\dev\antigravity_dev\SolidLink\packages\Microsoft.Net.Compilers.3.11.0\tools"
& "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe" SolidLink.sln /p:Configuration=Debug /p:Platform=x64 /p:CscToolPath=$roslynPath /p:CscToolExe="csc.exe" /v:minimal
```

