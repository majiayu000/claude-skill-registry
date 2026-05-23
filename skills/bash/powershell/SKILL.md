---
name: powershell
description: Cheat sheet for PowerShell commands and scripts.
---

```ps1
Get-ChildItem Env:
$env:Path = "C:\Users\leo.yen\.local\bin;$env:Path"
(Get-PSReadlineOption).HistorySavePath
```

```ps1
# https://1fichier.com/?123&af=3957104&token=cHRfalB%2BWVBCD3BzWjhQZ15TQRlwdF1w
# https://1fichier.com/?123

$ErrorActionPreference = "STOP"
# URL of the file you want to download https://1fichier.com/?123
$url = "http://a-33.1fichier.com/456?inline"

$file = "E:\download.zip"
if (!(Test-Path $file)) {
    # 若檔案不存在，用單純 Invoke-WebRequest 或 WebClient.DownloadFile 就好
    # (New-Object System.Net.WebClient).DownloadFile($url, $file)
    Invoke-WebRequest -Uri $url -OutFile $file
}
else {
    # .NET 工作目錄與 PowerShell 可能不用，取得完整路徑供 .NET 使用
    $fileFullPath = (Resolve-Path $file).Path    
    # 若檔案存在，查現有檔案大小，使用 Range Header 續傳
    # 取得現有檔案大小，由後面續傳
    # PowerShell 7 Invoke-WebRequest 直接加 -Resume 即可
    $currLength = (Get-Item $file).Length
    # Invoke-WebRequest -Uri $url -Headers @{"Range"="bytes=$currLength-"} -OutFile "$file.resume"
    # 以上寫法不 Work -> The 'RANGE' header must be modified using the appropriate property or method.
    # 用 HttpWebRequest 實現
    [System.Net.HttpWebRequest] $req = [System.Net.WebRequest]::Create($url)
    $req.Method = "GET"
    $req.AddRange($currLength)
    try {
        $resp = $req.GetResponse()
    }
    catch [System.Net.WebException] {
        # 若檔案先前已下載完成，伺服器會由 Range 已到檔案結尾回傳 HTTP 416，此時不需續傳，直接結束
        if ($_.Exception.Response.StatusCode -eq [System.Net.HttpStatusCode]::RequestedRangeNotSatisfiable) {
            Write-Host "檔案已完成"
            return
        }
        else {
            $_.Exception
        }
    }
    Write-Host "從 $currLength 開始續傳"
    $respStream = $resp.GetResponseStream()
    $contRange = $resp.Headers['Content-Range'] # ex: Content-Range: bytes 0-50/1270
    if (!$contRange) { throw "無法續傳" }
    $totalLen = $contRange.Split('/')[1]
    $fileStream = New-Object System.IO.FileStream($fileFullPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Write, [System.IO.FileShare]::Read)
    try {
        $fileStream.Seek($currLength, [System.IO.SeekOrigin]::Begin) | Out-Null
        # 以 8K 為單位從 Response Stream 讀取 byte[] 寫入 FileStream
        [byte[]]$buff = [byte[]]::CreateInstance([byte], 8192)
        do {
            $bytesRead = $respStream.Read($buff, 0, $buff.Length)
            $fileStream.Write($buff, 0, $bytesRead)
            Write-Progress -Activity "續傳下載中" -Status "$($fileStream.Position)/$totalLen" -PercentComplete ($fileStream.Position * 100 / $totalLen)
        } while ($bytesRead -gt 0)
        $fileStream.Close()
    }
    finally {
        $fileStream.Dispose()
    }
    $respStream.Close()
}

```



```ps1
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

Get-CimInstance Win32_Process |
    Where-Object { $_.Name -like "python*" } |
    Select-Object ProcessId, Name, CommandLine

```



```ps1
function Get-ParentChain {
    param(
        [int]$ProcessId
    )

    $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $ProcessId"

    if (-not $proc) {
        return @()
    }

    if ($proc.ParentProcessId -eq 0) {
        return @($proc)
    }

    return @($proc) + (Get-ParentChain -ProcessId $proc.ParentProcessId)
}


Get-CimInstance Win32_Process |
    Where-Object { $_.Name -like "python*" } |
    ForEach-Object {
        $chain = Get-ParentChain -ProcessId $_.ProcessId

        [PSCustomObject]@{
            PID          = $_.ProcessId
            Name         = $_.Name
            ParentChain  = ($chain | Select-Object -ExpandProperty Name) -join " -> "
        }
    }

```
