---
name: dns-zonefile-config
description: "Configurez correctement vos zones DNS pour l'email deliverability (SPF, DKIM, DMARC), la sécurité (DNSSEC, CAA), et l'automatisation (OVH API, Cloudflare, Terraform), basé sur les best practices 2024-2025. Use when: **Configurer l'authentification email** - SPF, DKIM, DMARC pour éviter le spam folder; **Sécuriser un domaine** - DNSSEC, CAA records, protection contre le spoofing; **Automatiser la gestion DNS** - OVH API, Cloudflare API, Terraform; **Débugger des problèmes DNS** - dig, nslookup..."
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# DNS Zonefile Configuration

> Configurez correctement vos zones DNS pour l'email deliverability (SPF, DKIM, DMARC), la sécurité (DNSSEC, CAA), et l'automatisation (OVH API, Cloudflare, Terraform), basé sur les best practices 2024-2025.

## When to Use This Skill

- **Configurer l'authentification email** - SPF, DKIM, DMARC pour éviter le spam folder
- **Sécuriser un domaine** - DNSSEC, CAA records, protection contre le spoofing
- **Automatiser la gestion DNS** - OVH API, Cloudflare API, Terraform
- **Débugger des problèmes DNS** - dig, nslookup, MXToolbox
- **Migrer ou configurer un nouveau domaine** - Setup complet from scratch

## Methodology Foundation

**Sources**:
- [Cisco Email Authentication Best Practices](https://www.cisco.com/c/en/us/support/docs/security/email-security-appliance/215360-best-practice-for-email-authentication.html)
- [DMARCLY Definitive Guide](https://dmarcly.com/blog/how-to-implement-dmarc-dkim-spf-to-stop-email-spoofing-phishing-the-definitive-guide)
- [Cloudflare Terraform Best Practices](https://developers.cloudflare.com/terraform/advanced-topics/best-practices/)
- [OVH Python API](https://github.com/ovh/python-ovh)

**Why This Matters**: Depuis février 2024, Google et Yahoo exigent SPF, DKIM et DMARC pour les envois bulk. Sans configuration correcte, vos emails finissent en spam. Les expéditeurs authentifiés ont **2.7x plus de chances** d'atteindre l'inbox.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures sales frameworks | Deal strategy |
| Suggests discovery questions | Relationship approach |
| Creates proposal templates | Pricing decisions |
| Identifies objection patterns | Negotiation tactics |
| Analyzes deal dynamics | Final deal terms |

## What This Skill Does

1. **Configure l'authentification email** - SPF, DKIM, DMARC avec les bonnes valeurs
2. **Sécurise le domaine** - DNSSEC, CAA, protection certificats
3. **Optimise les TTL** - Valeurs recommandées par type de record
4. **Automatise via API** - OVH, Cloudflare, Terraform
5. **Diagnostique les problèmes** - Outils et troubleshooting

## Instructions

### Step 1: Comprendre la Structure de Zone

```
## Anatomie d'un Fichier de Zone

$ORIGIN example.com.     ; Le domaine de base
$TTL 3600                ; TTL par défaut (1 heure)

; SOA Record (Start of Authority)
@   IN  SOA   ns1.example.com. admin.example.com. (
            2024012801  ; Serial (YYYYMMDDNN)
            7200        ; Refresh (2h)
            3600        ; Retry (1h)
            1209600     ; Expire (2 semaines)
            3600        ; Minimum TTL (1h)
)

; Nameservers
@       IN  NS      ns1.example.com.
@       IN  NS      ns2.example.com.

; A Records
@       IN  A       203.0.113.10
www     IN  A       203.0.113.10
mail    IN  A       203.0.113.20

; CNAME Records
blog    IN  CNAME   www.example.com.

; MX Records (priorité croissante = préférence décroissante)
@       IN  MX  10  mail.example.com.
@       IN  MX  20  mail-backup.example.com.

; TXT Records (SPF, DKIM, DMARC, etc.)
@       IN  TXT     "v=spf1 ..."
```

---

### Step 2: Email Authentication - SPF

**SPF (Sender Policy Framework)** - Déclare quels serveurs peuvent envoyer des emails pour votre domaine.

```
## SPF Record Syntax

v=spf1 [mechanisms] [qualifier]all

Mechanisms:
- ip4:203.0.113.0/24    ; Autoriser une plage IP
- ip6:2001:db8::/32     ; IPv6
- a                      ; Autoriser l'IP du record A du domaine
- mx                     ; Autoriser les serveurs MX
- include:_spf.google.com  ; Inclure le SPF d'un autre domaine
- exists:%{i}.spf.example.com  ; Macro avancée

Qualifiers:
- +all  ; PASS (dangereux, jamais utiliser)
- -all  ; FAIL (hard fail)
- ~all  ; SOFTFAIL (recommandé)
- ?all  ; NEUTRAL
```

**Best Practices SPF:**

```
## SPF - Règles Critiques

1. UN SEUL record SPF par domaine
   ❌ Plusieurs records = tous invalides

2. Utiliser ~all (softfail), pas -all (hardfail)
   → Permet à DMARC d'évaluer aussi DKIM

3. Maximum 10 DNS lookups
   → include:, a, mx, ptr comptent comme lookups
   → ip4/ip6 ne comptent pas
   → Utiliser des macros SPF si limite atteinte

4. Éviter les gros blocs CIDR
   → Préférer des IPs spécifiques aux /16 ou /8
```

**Exemples SPF courants:**

```
## SPF pour Google Workspace
v=spf1 include:_spf.google.com ~all

## SPF pour Microsoft 365
v=spf1 include:spf.protection.outlook.com ~all

## SPF pour OVH Mail
v=spf1 include:mx.ovh.com ~all

## SPF multi-services (Google + Mailchimp + Sendgrid)
v=spf1 include:_spf.google.com include:servers.mcsv.net include:sendgrid.net ~all

## SPF avec IP dédiée
v=spf1 ip4:203.0.113.10 include:_spf.google.com ~all
```

---

### Step 3: Email Authentication - DKIM

**DKIM (DomainKeys Identified Mail)** - Signature cryptographique des emails.

```
## Structure DKIM

Record Name: [selector]._domainkey.example.com
Record Type: TXT
Value: v=DKIM1; k=rsa; p=[public_key]

Exemple:
google._domainkey.example.com  TXT  "v=DKIM1; k=rsa; p=MIIBIjANBgkq..."
```

**Best Practices DKIM:**

```
## DKIM - Règles Critiques

1. Un sélecteur différent par service
   → google._domainkey pour Google Workspace
   → mailchimp._domainkey pour Mailchimp
   → sendgrid._domainkey pour Sendgrid

2. Rotation des clés tous les 6 mois
   → Réduit le risque de compromission

3. Clé RSA 2048 bits minimum
   → 1024 bits est obsolète

4. Un sélecteur par tiers
   → Permet de révoquer sans impacter la production
```

**Génération DKIM par service:**

| Service | Où trouver la clé DKIM |
|---------|------------------------|
| Google Workspace | Admin Console → Apps → Google Workspace → Gmail → Authenticate email |
| Microsoft 365 | Microsoft 365 Defender → Email → DKIM |
| Mailchimp | Settings → Domain → View Setup Instructions |
| Sendgrid | Settings → Sender Authentication → Domain Authentication |
| Brevo | Settings → Senders & IP → Domains |

---

### Step 4: Email Authentication - DMARC

**DMARC (Domain-based Message Authentication)** - Politique qui dit aux serveurs quoi faire si SPF/DKIM échouent.

```
## Structure DMARC

Record Name: _dmarc.example.com
Record Type: TXT
Value: v=DMARC1; p=[policy]; [options]

Policies:
- p=none      ; Monitoring only (étape 1)
- p=quarantine ; Mettre en spam si échec
- p=reject    ; Rejeter si échec (étape finale)

Options courantes:
- rua=mailto:dmarc@example.com  ; Rapports agrégés (XML)
- ruf=mailto:dmarc@example.com  ; Rapports forensics (détaillés)
- pct=100     ; Pourcentage d'emails concernés
- sp=reject   ; Politique pour sous-domaines
- adkim=r     ; Alignement DKIM (r=relaxed, s=strict)
- aspf=r      ; Alignement SPF (r=relaxed, s=strict)
```

**Progression DMARC recommandée:**

```
## Étape 1: Monitoring (2-4 semaines)
v=DMARC1; p=none; rua=mailto:dmarc-reports@example.com

→ Collecter les rapports, identifier tous les expéditeurs légitimes

## Étape 2: Quarantine (2-4 semaines)
v=DMARC1; p=quarantine; pct=10; rua=mailto:dmarc-reports@example.com

→ Tester sur 10% des emails, augmenter progressivement

## Étape 3: Quarantine 100%
v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@example.com

## Étape 4: Reject (objectif final)
v=DMARC1; p=reject; rua=mailto:dmarc-reports@example.com; sp=reject
```

**Services de monitoring DMARC:**
- [DMARC Analyzer](https://www.dmarcanalyzer.com) (freemium)
- [Postmark DMARC](https://dmarc.postmarkapp.com) (gratuit)
- [EasyDMARC](https://easydmarc.com) (freemium)

---

### Step 5: Security - DNSSEC & CAA

**DNSSEC** - Signe cryptographiquement les réponses DNS pour éviter le spoofing.

```
## Activer DNSSEC

Chez OVH:
1. Manager → Domaine → Zone DNS → DNSSEC
2. Activer → OVH génère les clés automatiquement

Chez Cloudflare:
1. DNS → Settings → DNSSEC
2. Enable DNSSEC → Copier le DS record
3. Ajouter le DS record chez le registrar

Vérification:
$ dig +dnssec example.com
→ Doit montrer RRSIG records
```

**CAA Records** - Limite quelles CA peuvent émettre des certificats SSL.

```
## Structure CAA

Record Type: CAA
Flags: 0
Tag: issue | issuewild | iodef
Value: "ca-domain" ou "mailto:..."

Exemples:

# Autoriser uniquement Let's Encrypt
example.com.  CAA  0 issue "letsencrypt.org"
example.com.  CAA  0 issuewild "letsencrypt.org"

# Autoriser Let's Encrypt + Sectigo
example.com.  CAA  0 issue "letsencrypt.org"
example.com.  CAA  0 issue "sectigo.com"

# Reporter les violations
example.com.  CAA  0 iodef "mailto:security@example.com"

# Bloquer tous les wildcards
example.com.  CAA  0 issuewild ";"
```

**Best Practice CAA:**
- Toujours combiner avec DNSSEC (sinon vulnérable au spoofing)
- Lister uniquement les CA que vous utilisez vraiment
- Ajouter un iodef pour être alerté des tentatives

---

### Step 6: TTL Best Practices

```
## TTL Recommandés par Type de Record

| Record Type | Usage | TTL Recommandé | Rationale |
|-------------|-------|----------------|-----------|
| A / AAAA | Serveur web stable | 3600-86400 (1h-24h) | Rarement changé |
| A (failover) | Avec health check | 60-300 (1-5min) | Failover rapide |
| CNAME | Alias stable | 3600-86400 | Suit le TTL de la cible |
| MX | Mail servers | 3600-21600 (1h-6h) | Failover via priorité MX |
| TXT (SPF/DKIM) | Email auth | 3600-86400 | Rarement changé |
| TXT (DMARC) | Email policy | 3600 | Peut nécessiter ajustements |
| NS | Nameservers | 86400-172800 (1-2j) | Très stable |
| CAA | Cert authority | 3600-86400 | Rarement changé |

## Règles Générales

1. Jamais TTL = 0 (non défini dans le standard)
2. Minimum recommandé: 300 (5 min)
3. Avant migration: baisser TTL 24-48h avant
4. Après migration stable: remonter le TTL
```

---

### Step 7: Automatisation - OVH API

```python
## Installation
# pip install ovh

## Configuration (ovh.conf)
[default]
endpoint=ovh-eu

[ovh-eu]
application_key=YOUR_APP_KEY
application_secret=YOUR_APP_SECRET
consumer_key=YOUR_CONSUMER_KEY

## Obtenir les clés
# https://eu.api.ovh.com/createToken/
# Permissions nécessaires:
# GET /domain/zone/*
# POST /domain/zone/*
# PUT /domain/zone/*
# DELETE /domain/zone/*
```

```python
## Script Python - Gestion DNS OVH

import ovh

client = ovh.Client()

# Lister tous les domaines
domains = client.get('/domain/zone')
print(domains)

# Lister les records d'une zone
records = client.get(f'/domain/zone/{domain}/record')

# Obtenir un record spécifique
record = client.get(f'/domain/zone/{domain}/record/{record_id}')

# Créer un record TXT (ex: SPF)
result = client.post(
    f'/domain/zone/{domain}/record',
    fieldType='TXT',
    subDomain='',  # @ = racine
    target='v=spf1 include:_spf.google.com ~all',
    ttl=3600
)

# Créer un record DMARC
result = client.post(
    f'/domain/zone/{domain}/record',
    fieldType='TXT',
    subDomain='_dmarc',
    target='v=DMARC1; p=none; rua=mailto:dmarc@example.com',
    ttl=3600
)

# Modifier un record
client.put(
    f'/domain/zone/{domain}/record/{record_id}',
    target='nouvelle_valeur',
    ttl=3600
)

# Supprimer un record
client.delete(f'/domain/zone/{domain}/record/{record_id}')

# IMPORTANT: Rafraîchir la zone après modifications
client.post(f'/domain/zone/{domain}/refresh')
```

---

### Step 8: Automatisation - Cloudflare

```hcl
## Terraform - Cloudflare DNS

provider "cloudflare" {
  api_token = var.cloudflare_api_token  # Jamais en dur!
}

# Zone data
data "cloudflare_zone" "example" {
  name = "example.com"
}

# A Record
resource "cloudflare_record" "www" {
  zone_id = data.cloudflare_zone.example.id
  name    = "www"
  value   = "203.0.113.10"
  type    = "A"
  ttl     = 3600
  proxied = true  # Cloudflare proxy
}

# SPF Record
resource "cloudflare_record" "spf" {
  zone_id = data.cloudflare_zone.example.id
  name    = "@"
  value   = "v=spf1 include:_spf.google.com ~all"
  type    = "TXT"
  ttl     = 3600
}

# DMARC Record
resource "cloudflare_record" "dmarc" {
  zone_id = data.cloudflare_zone.example.id
  name    = "_dmarc"
  value   = "v=DMARC1; p=reject; rua=mailto:dmarc@example.com"
  type    = "TXT"
  ttl     = 3600
}

# MX Records
resource "cloudflare_record" "mx_primary" {
  zone_id  = data.cloudflare_zone.example.id
  name     = "@"
  value    = "aspmx.l.google.com"
  type     = "MX"
  ttl      = 3600
  priority = 1
}

# CAA Record
resource "cloudflare_record" "caa" {
  zone_id = data.cloudflare_zone.example.id
  name    = "@"
  type    = "CAA"
  ttl     = 3600
  data {
    flags = 0
    tag   = "issue"
    value = "letsencrypt.org"
  }
}
```

**Best Practices Terraform/Cloudflare:**
- Ne jamais stocker les credentials en clair
- Utiliser des variables d'environnement ou un secret manager
- State remote (S3, GCS) pour la collaboration
- Un workspace par environnement (staging/prod)

---

### Step 9: Diagnostic & Troubleshooting

```bash
## Outils CLI

# Vérifier un record spécifique
dig example.com TXT +short
dig _dmarc.example.com TXT +short
dig google._domainkey.example.com TXT +short

# Vérifier les MX
dig example.com MX +short

# Vérifier DNSSEC
dig example.com +dnssec

# Tracer la résolution
dig example.com +trace

# Vérifier la propagation (multiple resolvers)
dig @8.8.8.8 example.com TXT    # Google
dig @1.1.1.1 example.com TXT    # Cloudflare
dig @9.9.9.9 example.com TXT    # Quad9
```

**Outils en ligne:**

| Outil | URL | Usage |
|-------|-----|-------|
| MXToolbox | [mxtoolbox.com](https://mxtoolbox.com) | SPF, DKIM, DMARC, blacklist |
| DMARC Analyzer | [dmarcanalyzer.com](https://dmarcanalyzer.com/dmarc/dmarc-record-check/) | Validation DMARC |
| DNSViz | [dnsviz.net](https://dnsviz.net) | Debug DNSSEC |
| Mail-Tester | [mail-tester.com](https://www.mail-tester.com) | Score email complet |
| Google Postmaster | [postmaster.google.com](https://postmaster.google.com) | Réputation domaine |

**Erreurs courantes:**

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| SPF permerror | Multiple SPF records | Fusionner en un seul |
| SPF permerror | >10 DNS lookups | Utiliser ip4/ip6, macros SPF |
| DKIM fail | Clé mal copiée | Vérifier pas de retour à la ligne |
| DMARC none | Policy p=none | Normal en monitoring, escalader après |
| Emails en spam | SPF/DKIM OK mais pas alignés | Vérifier alignement DMARC (From: header) |
| SERVFAIL | DNSSEC mal configuré | Debugger sur dnsviz.net |

---

## Templates Complets

### Template: Nouveau Domaine (Google Workspace)

```
## Records à créer

# MX (mail)
@       MX  1   aspmx.l.google.com.
@       MX  5   alt1.aspmx.l.google.com.
@       MX  5   alt2.aspmx.l.google.com.
@       MX  10  alt3.aspmx.l.google.com.
@       MX  10  alt4.aspmx.l.google.com.

# SPF
@       TXT     "v=spf1 include:_spf.google.com ~all"

# DKIM (obtenir la clé dans Google Admin Console)
google._domainkey   TXT     "v=DKIM1; k=rsa; p=MIIBIjANBgkq..."

# DMARC (commencer en monitoring)
_dmarc  TXT     "v=DMARC1; p=none; rua=mailto:dmarc@example.com"

# CAA (si Let's Encrypt pour SSL)
@       CAA     0 issue "letsencrypt.org"
@       CAA     0 iodef "mailto:security@example.com"
```

### Template: Domaine Parké (protection anti-spoofing)

```
## Domaine qui n'envoie JAMAIS d'email

# SPF - Rejeter tout
@       TXT     "v=spf1 -all"

# DMARC - Rejeter tout
_dmarc  TXT     "v=DMARC1; p=reject; sp=reject; rua=mailto:dmarc@example.com"

# Pas de MX = pas de réception
# (ou MX vers null: @  MX  0  .)
```

### Template: Multi-Services (SaaS stack)

```
## SPF avec plusieurs services
@       TXT     "v=spf1 include:_spf.google.com include:servers.mcsv.net include:sendgrid.net ~all"

## DKIM - Un par service
google._domainkey       TXT     "v=DKIM1; k=rsa; p=..."
k1._domainkey           TXT     "v=DKIM1; k=rsa; p=..."  # Mailchimp
s1._domainkey           TXT     "v=DKIM1; k=rsa; p=..."  # Sendgrid

## DMARC
_dmarc  TXT     "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"
```

## Checklist Configuration DNS

```
## Setup Initial

[ ] A/AAAA records pour web
[ ] CNAME pour www et autres alias
[ ] MX records configurés (avec priorités)
[ ] SPF record (un seul, ~all)
[ ] DKIM configuré pour chaque service d'envoi
[ ] DMARC en mode monitoring (p=none)
[ ] CAA records (limiter les CA autorisées)
[ ] DNSSEC activé chez le registrar

## Après 2-4 semaines de monitoring

[ ] Analyser les rapports DMARC
[ ] Identifier les expéditeurs non authentifiés
[ ] Corriger ou ajouter les sources légitimes
[ ] Escalader DMARC vers p=quarantine
[ ] Puis vers p=reject

## Maintenance

[ ] Rotation DKIM tous les 6 mois
[ ] Review des rapports DMARC mensuellement
[ ] Vérifier le score sur mail-tester.com
[ ] Monitorer la réputation sur Google Postmaster
```

## Skill Boundaries

### What This Skill Does Well
- Structuring sales conversations
- Creating discovery frameworks
- Analyzing deal dynamics
- Suggesting negotiation approaches

### What This Skill Cannot Do
- Replace relationship building
- Guarantee closed deals
- Know specific buyer psychology
- Make pricing decisions

## References

### Email Authentication
- [Cisco Best Practices](https://www.cisco.com/c/en/us/support/docs/security/email-security-appliance/215360-best-practice-for-email-authentication.html)
- [DMARCLY Guide](https://dmarcly.com/blog/how-to-implement-dmarc-dkim-spf-to-stop-email-spoofing-phishing-the-definitive-guide)
- [EasyDMARC Best Practices](https://easydmarc.com/blog/dmarc-dkim-spf-email-authentication-best-practices/)
- [SalesHive 2025 Guide](https://saleshive.com/blog/dkim-dmarc-spf-best-practices-email-security-deliverability/)

### DNS Security
- [Let's Encrypt CAA](https://letsencrypt.org/docs/caa/)
- [CAA Records Guide 2025](https://domaindetails.com/kb/technical-guides/caa-records-ssl-certificates)
- [DNSSEC Best Practices](https://vercara.digicert.com/resources/understanding-dnssec-best-practices-and-implementation-challenges)

### TTL
- [Catchpoint TTL Guide](https://www.catchpoint.com/dns-monitoring/dns-ttl)
- [Varonis TTL Best Practices](https://www.varonis.com/blog/dns-ttl)
- [AWS Route 53 Best Practices](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/best-practices-dns.html)

### Automation
- [OVH Python Library](https://github.com/ovh/python-ovh)
- [Cloudflare Terraform Best Practices](https://developers.cloudflare.com/terraform/advanced-topics/best-practices/)
- [cf-terraforming](https://developers.cloudflare.com/terraform/advanced-topics/import-cloudflare-resources/)

### Tools
- [MXToolbox](https://mxtoolbox.com)
- [DNSViz](https://dnsviz.net)
- [Mail-Tester](https://www.mail-tester.com)
- [Google Postmaster Tools](https://postmaster.google.com)

## Related Skills

- `nurture-sequences/` - Email deliverability impacte le nurturing
- `distribution-engine/` - Infrastructure pour le marketing automation

---

*Skill version: 1.0*
*Last updated: 2026-01-28*
*Category: devops*
