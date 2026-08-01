---
name: license-checker
description: ตรวจสอบ licenses ของ dependencies เพื่อความถูกต้องตามกฎหมายและนโยบายบริษัท
---

# ⚖️ License Checker Skill

---
name: license-checker
description: Check and validate licenses of project dependencies for legal compliance
---

## 🎯 Purpose

ตรวจสอบ licenses ของ dependencies เพื่อความถูกต้องตามกฎหมายและนโยบายบริษัท

## 📋 When to Use

- Before releasing software
- Adding new dependencies
- Compliance audits
- Open source contributions
- Enterprise projects

## 🔧 License Types

### Permissive (Safe for commercial)
| License | Can | Cannot |
|---------|-----|--------|
| **MIT** | Commercial use, modify, distribute | Liability |
| **Apache 2.0** | Commercial, patents, modify | Liability, trademark |
| **BSD** | Commercial, modify, distribute | Liability |

### Copyleft (Careful)
| License | Risk |
|---------|------|
| **GPL** | Must open source derivative works |
| **LGPL** | OK if dynamically linked |
| **AGPL** | Network use = distribution |

### Commercial
| License | Description |
|---------|-------------|
| **Proprietary** | Requires license purchase |
| **Dual-licensed** | Choose open or commercial |

## 📝 Check Commands

```bash
# NPM - license-checker
npx license-checker --summary
npx license-checker --production --csv > licenses.csv

# NPM - license-report
npx license-report

# Python
pip-licenses --format=markdown
```

## 📊 Output Example

```
├─ package-a@1.0.0
│  ├─ licenses: MIT
│  ├─ repository: https://github.com/...
│  └─ publisher: Author Name
├─ package-b@2.0.0
│  ├─ licenses: Apache-2.0
│  ├─ repository: https://github.com/...
│  └─ publisher: Company Inc
```

## 🚨 License Policy Template

```markdown
## Allowed Licenses
- MIT
- Apache-2.0
- BSD-2-Clause
- BSD-3-Clause
- ISC
- CC0-1.0

## Requires Review
- LGPL-3.0
- MPL-2.0

## Not Allowed
- GPL-3.0
- AGPL-3.0
- Unlicensed
```

## ✅ Compliance Checklist

- [ ] All deps have licenses
- [ ] No GPL in commercial
- [ ] Attribution included
- [ ] License files copied
- [ ] NOTICE file updated
- [ ] Legal approved

## 🔗 Related Skills

- `security-audit` - Security compliance
- `dependency-management` - Manage deps
- `documentation` - License docs
