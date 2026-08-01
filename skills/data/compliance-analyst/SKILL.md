---
name: compliance-analyst
description: '> Sertifikasyon ve uyumluluk araştırma rehberi.'
---

---
name: compliance_analyst
router_kit: SecurityKit
description: Sertifikasyon, uyumluluk gereksinimleri ve regulatory pathway araştırma rehberi.
metadata:
  skillport:
    category: research
    tags: [architecture, automation, best practices, clean code, coding, collaboration, compliance, compliance analyst, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - standards
---

# 📋 Compliance Analyst

> Sertifikasyon ve uyumluluk araştırma rehberi.

---

## 📋 Compliance Areas

| Area | Standards | Examples |
|------|-----------|----------|
| **Security** | ISO 27001, SOC 2 | Data protection |
| **Privacy** | GDPR, KVKK, CCPA | Personal data |
| **Accessibility** | WCAG, ADA | Web access |
| **Industry** | HIPAA, PCI-DSS | Healthcare, payments |

---

## 🔧 Compliance Checklist

### GDPR
```checklist
- [ ] Consent management
- [ ] Right to deletion
- [ ] Data portability
- [ ] Privacy policy
- [ ] DPO appointed
- [ ] Breach notification
```

### SOC 2
```checklist
- [ ] Security controls
- [ ] Availability SLA
- [ ] Processing integrity
- [ ] Confidentiality
- [ ] Privacy practices
```

---

## 📊 Gap Analysis Template

```markdown
# Compliance Gap Analysis: [Standard]

## Current State
| Control | Required | Current | Gap |
|---------|----------|---------|-----|
| Access Control | Yes | Partial | ⚠️ |
| Encryption | Yes | Yes | ✅ |
| Logging | Yes | No | ❌ |

## Remediation Plan
| Gap | Action | Owner | Deadline |
|-----|--------|-------|----------|
| Logging | Implement audit logs | DevOps | Q1 |

## Timeline to Compliance
- Gap remediation: 3 months
- Audit prep: 1 month
- Certification: 2 months
```

---

## 🎯 Certification Path

```
Assessment → Gap Analysis → Remediation → Audit → Certification
    └─────────────────────────────────────────────┘
                      6-12 months
```

## 🔄 Workflow

> **Kaynak:** [Compliance-As-Code (SCAP)](https://github.com/ComplianceAsCode/content) & [EU AI Act Compliance Framework](https://artificialintelligenceact.eu/)

### Aşama 1: Regulatory Scoping & DORA/AI Act
- [ ] **Inventory**: Sistemin hangi düzenlemelere (DORA, NIS2, EU AI Act) tabi olduğunu belirle.
- [ ] **Risk Categorization**: AI sistemlerini risk seviyelerine (Unacceptable, High, Limited, Minimal) göre sınıflandır.
- [ ] **Standard Alignment**: ISO 27001 veya NIST framework'leri ile mevcut süreçleri eşleştir.

### Aşama 2: Audit & Gap Assessment
- [ ] **Evidence Collection**: Politika belgeleri, log kayıtları ve sistem konfigürasyonlarını topla.
- [ ] **Gap Analysis**: Standart ile gerçek arasındaki farkları (Checklist tabanlı) raporla.
- [ ] **Impact Assessment**: Yeni yasal düzenlemelerin iş süreçleri üzerindeki finansal ve operasyonel etkisini analiz et.

### Aşama 3: Remediation & Continuous Compliance
- [ ] **Mitigation Plan**: Eksikleri gidermek için aksiyon planı oluştur (Örn: MFA zorunluluğu).
- [ ] **Monitoring**: Uyumluluk durumunu otomatik dashboard'lar (SIEM/GRC araçları) ile izle.
- [ ] **Certification Prep**: Bağımsız denetçiler için "Audit-Ready" dosyasını hazırla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Yeni çıkan "EU AI Act" kriterleri göz önünde bulunduruldu mu? |
| 2 | Veri işleme envanteri (ROPA) güncel mi? |
| 3 | Tedarikçi (Third-party) riski analiz edildi mi? |

---
*Compliance Analyst v1.5 - With Workflow*
