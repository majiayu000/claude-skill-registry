---
name: deploy-pipeline
description: >
  Feature tamamlandıktan sonra commit → push → deploy pipeline'ı.
  "/deploy" komutuyla veya implement-feature'ın son adımı olarak tetiklenir.
  Her adımda kullanıcı onayı zorunludur — onaysız aksiyon alınmaz.
---

# Deploy Pipeline

Bu skill, tamamlanmış kodu güvenli şekilde deploy eder.
Her adımda kullanıcı onayı **zorunludur** — onaysız ilerleme yapma.

## Pipeline Adımları

### Adım 1: Quality Gate
Aşağıdaki kontrolleri çalıştır:
```bash
npm test
npx tsc --noEmit
```

Tüm kontroller geçmeli. Herhangi biri başarısız olursa:
- Hatayı kullanıcıya göster
- Pipeline'ı durdur
- "Düzeltip tekrar deneyelim mi?" sor

### Adım 2: Git Durum Kontrolü
```bash
git status
git branch --show-current
git log --oneline -5
```

Kullanıcıya göster:
- Hangi branch'tesin
- Değişen dosya sayısı
- Son commit'ler

**Kural:** `main` branch'teysen uyar ve feature branch oluşturmayı öner.

### Adım 3: Commit (Onay Gerekli)
1. Değişen dosyaları listele
2. Anlamlı commit mesajı öner (conventional commits formatı)
3. **"Bu commit mesajı ile devam edeyim mi?" sor**
4. Onay gelirse: `git add <dosyalar>` + `git commit`
5. Onay gelmezse: Kullanıcının istediği mesajla commit at

### Adım 4: Push (Onay Gerekli)
1. Push edilecek branch'i göster
2. Remote durumunu kontrol et (`git remote -v`)
3. **"<branch> branch'ine push edeyim mi?" sor**
4. Onay gelirse: `git push -u origin <branch>`
5. Push sonucunu göster

### Adım 5: PR / Deploy Tetikleme (Onay Gerekli)
1. GitHub Actions CI workflow'un otomatik tetikleneceğini bildir
2. PR oluşturulup oluşturulmayacağını sor
3. **"PR oluşturayım mı? (main'e merge için)" sor**
4. Onay gelirse: `gh pr create` ile PR oluştur
5. CI durumunu kontrol et: `gh run list --limit 1`

### Adım 6: Sonuç Raporu
Pipeline tamamlandığında göster:
- Commit hash
- Branch adı
- PR URL (varsa)
- CI durumu
- Bir sonraki adım önerisi

## Önemli Kurallar
- **ASLA** kullanıcı onayı almadan commit, push veya PR oluşturma
- **ASLA** main branch'e direkt push yapma
- **ASLA** force push kullanma
- Her adımda ne olacağını ÖNCE açıkla, SONRA onay iste
- Hata durumunda pipeline'ı durdur, kullanıcıya raporla
