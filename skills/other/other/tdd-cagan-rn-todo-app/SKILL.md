---
name: tdd
description: >
  Test-Driven Development workflow'u için kullan. "/tdd" komutuyla veya
  "test yaz", "tdd ile yap" ifadesi geçtiğinde devreye gir.
  Mevcut bir component/hook/service için test yazmak istendiğinde de kullan.
---

# TDD Workflow

## Kullanım
Bu skill, mevcut veya yeni kod için TDD döngüsünü uygular.

## Adımlar

### 1. Hedefi Belirle
- Hangi dosya/component test edilecek?
- Mevcut test dosyası var mı? (kontrol et)

### 2. Test Dosyası Oluştur (yoksa)
`src/{component|hook|service}/__tests__/FileName.test.tsx`

### 3. Test Senaryolarını Belirle
rules/testing-standards.md'ye göre:
- Happy path
- Error path  
- Edge case'ler (empty, null, max length vb.)

### 4. Testleri Yaz (RED)
Önce failing testleri yaz.
`npm test -- --testPathPattern=FileName` ile confirm et — fail olması beklenen.

### 5. Implementation (GREEN)
Testleri geçirecek minimum kodu yaz.
`npm test` çalıştır — GREEN olana kadar iterate et.

### 6. Refactor
Testler GREEN iken kodu temizle.
`npm test` tekrar çalıştır — GREEN'de kaldığını doğrula.

### 7. Coverage Raporu
`npm test -- --coverage --testPathPattern=FileName`
Raporu kullanıcıya göster.

## @tdd-guide Subagent ile Fark
- Bu skill: Hızlı, interaktif TDD — mevcut component'ler için
- @tdd-guide subagent: implement-feature pipeline içinde izole context'te çalışır
