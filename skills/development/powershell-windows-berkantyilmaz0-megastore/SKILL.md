---
name: powershell-windows
description: PowerShell Windows patterns. Critical pitfalls, operator syntax, error handling.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# PowerShell Windows Desenleri

> Windows PowerShell için kritik desenler ve tuzaklar.

---

## 1. Operatör Sözdizimi Kuralları

### KRİTİK: Parantez Gereklidir

| ❌ Yanlış | ✅ Doğru |
|----------|-----------|
| `if (Test-Path "a" -or Test-Path "b")` | `if ((Test-Path "a") -or (Test-Path "b"))` |
| `if (Get-Item $x -and $y -eq 5)` | `if ((Get-Item $x) -and ($y -eq 5))` |

**Kural:** Mantıksal operatörler kullanılırken her cmdlet çağrısı parantez içine ALINMALIDIR.

---

## 2. Unicode/Emoji Kısıtlaması

### KRİTİK: Scriptlerde Unicode Yok

| Amaç | ❌ Kullanma | ✅ Kullan |
|---------|-------------|--------|
| Başarı | ✅ ✓ | [OK] [+] |
| Hata | ❌ ✗ 🔴 | [!] [X] |
| Uyarı | ⚠️ 🟡 | [*] [WARN] |
| Bilgi | ℹ️ 🔵 | [i] [INFO] |
| İlerleme | ⏳ | [...] |

**Kural:** PowerShell scriptlerinde sadece ASCII karakterler kullanın.

---

## 3. Null Kontrol Desenleri

### Erişimden Önce Her Zaman Kontrol Et

| ❌ Yanlış | ✅ Doğru |
|----------|-----------|
| `$array.Count -gt 0` | `$array -and $array.Count -gt 0` |
| `$text.Length` | `if ($text) { $text.Length }` |

---

## 4. Dize Yerleştirme (String Interpolation)

### Karmaşık İfadeler

| ❌ Yanlış | ✅ Doğru |
|----------|-----------|
| `"Value: $($obj.prop.sub)"` | Önce değişkende sakla |

**Desen:**
```
$value = $obj.prop.sub
Write-Output "Value: $value"
```

---

## 5. Hata Yönetimi

### ErrorActionPreference

| Değer | Kullanım |
|-------|-----|
| Stop | Geliştirme (hızlı başarısız ol) |
| Continue | Üretim scriptleri |
| SilentlyContinue | Hataların beklendiği durumlar |

### Try/Catch Deseni

- Try bloğu içinde döndürme (return yapma)
- Temizlik için finally kullan
- try/catch sonrası döndür

---

## 6. Dosya Yolları

### Windows Yol Kuralları

| Desen | Kullanım |
|---------|-----|
| Değişmez (Literal) yol | `C:\Users\User\file.txt` |
| Değişken yol | `Join-Path $env:USERPROFILE "file.txt"` |
| Göreli | `Join-Path $ScriptDir "data"` |

**Kural:** Çapraz platform güvenliği için Join-Path kullanın.

---

## 7. Dizi İşlemleri

### Doğru Desenler

| İşlem | Sözdizimi |
|-----------|--------|
| Boş dizi | `$array = @()` |
| Öğe ekle | `$array += $item` |
| ArrayList ekle | `$list.Add($item) | Out-Null` |

---

## 8. JSON İşlemleri

### KRİTİK: Derinlik (Depth) Parametresi

| ❌ Yanlış | ✅ Doğru |
|----------|-----------|
| `ConvertTo-Json` | `ConvertTo-Json -Depth 10` |

**Kural:** İç içe geçmiş nesneler için her zaman `-Depth` belirtin.

### Dosya İşlemleri

| İşlem | Desen |
|-----------|---------|
| Oku | `Get-Content "file.json" -Raw | ConvertFrom-Json` |
| Yaz | `$data | ConvertTo-Json -Depth 10 | Out-File "file.json" -Encoding UTF8` |

---

## 9. Yaygın Hatalar

| Hata Mesajı | Neden | Düzeltme |
|---------------|-------|-----|
| "parameter 'or'" | Eksik parantez | Cmdlet'leri () içine al |
| "Unexpected token" | Unicode karakter | Sadece ASCII kullan |
| "Cannot find property" | Null nesne | Önce null kontrolü yap |
| "Cannot convert" | Tür uyuşmazlığı | .ToString() kullan |

---

## 10. Script Şablonu

```powershell
# Strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Main
try {
    # Logic here
    Write-Output "[OK] Done"
    exit 0
}
catch {
    Write-Warning "Error: $_"
    exit 1
}
```

---

> **Unutmayın:** PowerShell'in benzersiz sözdizimi kuralları vardır. Parantezler, sadece ASCII ve null kontrolleri pazarlık konusu değildir.
