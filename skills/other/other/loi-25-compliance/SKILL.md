---
name: loi-25-compliance
description: >
  Base de connaissances sur la Loi 25 du Québec (protection des renseignements personnels) appliquée au développement logiciel.
  Ce skill doit être utilisé quand l'utilisateur demande "audit loi 25", "vérifier la conformité",
  "protection des données personnelles", "PII", "renseignements personnels", "vie privée",
  "chiffrement des données sensibles", "droit à l'effacement", "portabilité des données",
  "EFVP", "évaluation des facteurs relatifs à la vie privée", ou toute question sur la conformité
  d'un projet aux lois québécoises de protection de la vie privée.
version: 0.3.0
---

# Loi 25 — Conformité pour projets logiciels

Ce skill fournit les connaissances nécessaires pour auditer un projet Supabase/React/TypeScript selon les exigences de la Loi 25 du Québec. Toutes les références d'articles renvoient à la **Loi sur la protection des renseignements personnels dans le secteur privé (RLRQ, c. P-39.1)**, mise à jour au 11 décembre 2025.

## Structure du rapport — Deux volets

Le rapport d'audit est structuré en **deux volets** avec des scores séparés :

### Volet A — Technique (pondération 60 %)
Couvre tout ce qui touche au code et à l'infrastructure :
- **A1.** Inventaire des données personnelles (PII dans DB)
- **A2.** Constats — Base de données (chiffrement, RLS, audit trail, rétention)
- **A3.** Constats — API et Backend (exposition, logs, LLM, transfert international)
- **A4.** Constats — Frontend (masquage, localStorage, URL, confidentialité par défaut)

### Volet B — Gouvernance (pondération 40 %)
Couvre les processus organisationnels et la conformité administrative :
- **B1.** Responsable de la protection des données (art. 3.1)
- **B2.** Politiques et pratiques de gouvernance (art. 3.2)
- **B3.** EFVP — Évaluation des facteurs relatifs à la vie privée (art. 3.3, 17)
- **B4.** Consentement (art. 14)
- **B5.** Registre des incidents (art. 3.5 à 3.8)
- **B6.** Procédure de gestion des incidents (art. 3.5)
- **B7.** Formation des employés
- **B8.** Politique de confidentialité publiée (art. 3.2)
- **B9.** Droit d'accès et de rectification (art. 27, 28)

### Calcul des scores

Chaque volet démarre à 100 et décrémente selon les constats :
- -15 par constat CRITIQUE
- -8 par constat MAJEUR
- -3 par constat MODÉRÉ
- -1 par constat MINEUR
- Minimum 0

**Score global** = (Score Technique × 0.60) + (Score Gouvernance × 0.40)

## Contexte légal

La **Loi 25** (anciennement projet de loi 64) modernise la protection des renseignements personnels au Québec. Toutes ses dispositions sont en vigueur depuis le **22 septembre 2024**.

**Sanctions (art. 90.1 à 93.1) :**

- **Sanctions administratives pécuniaires (art. 90.1, 90.12)** : Personne physique — max 50 000 $; Autre personne — max 10 000 000 $ ou 2 % du chiffre d'affaires mondial
- **Sanctions pénales (art. 91)** : Personne physique — 5 000 $ à 100 000 $; Autre personne — 15 000 $ à 25 000 000 $ ou 4 % du chiffre d'affaires mondial
- **Récidive (art. 92.1)** : Les montants sont doublés
- **Dommages punitifs (art. 93.1)** : Minimum 1 000 $ en cas d'atteinte intentionnelle ou de faute lourde
- **Prescription pénale (art. 92.2)** : 5 ans à compter de la perpétration de l'infraction
- **Responsabilité des dirigeants (art. 93)** : Les administrateurs et dirigeants peuvent être personnellement poursuivis

## Obligations fondamentales de gouvernance

### Responsable de la protection (art. 3.1)

Toute personne exploitant une entreprise doit désigner un **responsable de la protection des renseignements personnels**. Par défaut, c'est la personne ayant la plus haute autorité dans l'entreprise. Les coordonnées du responsable doivent être publiées sur le site Web de l'entreprise.

### Politiques et pratiques de gouvernance (art. 3.2)

L'entreprise doit établir et mettre en œuvre des **politiques et des pratiques** encadrant sa gouvernance des renseignements personnels. Ces politiques doivent :
- Être proportionnelles à la nature et à l'importance des activités
- Être publiées en termes simples sur le site Web de l'entreprise

### EFVP — Évaluation des facteurs relatifs à la vie privée (art. 3.3)

Une EFVP doit être réalisée pour tout projet d'acquisition, de développement ou de refonte d'un système d'information impliquant des renseignements personnels. Elle doit aussi être réalisée avant de communiquer des renseignements à l'extérieur du Québec (art. 17 al. 2).

### Incidents de confidentialité (art. 3.5 à 3.8)

Un **incident de confidentialité** est : tout accès non autorisé, toute utilisation non autorisée, toute communication non autorisée, ou toute perte de renseignements personnels (art. 3.6).

**Obligations en cas d'incident :**
1. **Prendre les mesures raisonnables** pour diminuer les risques et prévenir de nouveaux incidents (art. 3.5 al. 1)
2. **Aviser la CAI et les personnes concernées** si l'incident présente un risque sérieux de préjudice (art. 3.5 al. 2)
3. **Évaluer le risque de préjudice** en considérant la sensibilité des renseignements, les conséquences appréhendées, et la probabilité d'utilisation préjudiciable (art. 3.7)
4. **Tenir un registre des incidents** qui doit être communiqué à la CAI sur demande (art. 3.8)

## Consentement (art. 14)

Le consentement à la collecte, communication ou utilisation de renseignements personnels doit être :
- **Manifeste** — clairement exprimé
- **Libre** — sans pression
- **Éclairé** — la personne doit être informée des finalités, des personnes qui y auront accès, du lieu de conservation, de ses droits
- **Donné à des fins spécifiques** — un consentement distinct pour chaque finalité
- **Demandé pour chaque finalité** de façon distincte
- **Consentement séparé pour les données sensibles (art. 12 al. 3)** — le consentement pour les données sensibles doit être expressément donné

## Confidentialité par défaut (art. 9.1)

Les paramètres d'un produit ou service technologique offert au public doivent assurer, **par défaut**, le plus haut niveau de confidentialité, sans aucune intervention de la personne concernée. Exception : les témoins de connexion (cookies).

**Implication technique :** Les paramètres de partage, de visibilité et de collecte doivent être désactivés par défaut. L'utilisateur doit activer manuellement tout partage de ses données.

## Décisions automatisées (art. 12.1)

Lorsqu'un renseignement personnel est utilisé pour rendre une **décision fondée exclusivement sur un traitement automatisé** :
1. **Informer la personne** au moment de la décision ou avant
2. **Informer de ses droits** : la personne peut demander que la décision soit révisée par un humain, et elle peut soumettre ses observations
3. **Communiquer les renseignements utilisés** et les raisons/facteurs principaux ayant mené à la décision, sur demande

**Implication pour les chatbots :** Si un chatbot RH prend ou recommande des décisions (approbation de congés, évaluations, etc.), le système doit informer l'employé que la décision est automatisée et offrir un recours humain.

## Classification des renseignements personnels

### Définition de « renseignement sensible » (art. 12 al. 2)

Un renseignement personnel est sensible s'il est de nature **médicale, biométrique ou autrement intime**, ou s'il suscite, par sa nature ou en raison du contexte de son utilisation ou de sa communication, un **degré élevé d'attente raisonnable en matière de vie privée**.

### Catégorie 1 — Données sensibles (protection maximale requise)

Réf : art. 10, 12 al. 2-3. Chiffrement au repos obligatoire + contrôle d'accès strict + consentement exprès.

- Données de santé : allergies, conditions médicales, handicaps, médicaments
- Données financières : salaire, type de rémunération, % REER, % avantages sociaux, numéro de compte bancaire
- Numéro d'assurance sociale (NAS)
- Données biométriques
- Orientation sexuelle, origine ethnique, opinions politiques, croyances religieuses
- Antécédents judiciaires

### Catégorie 2 — Données personnelles (protection standard requise)

Réf : art. 2, 10, 20. Contrôle d'accès basé sur le rôle + masquage à l'affichage.

- Nom complet, prénom, nom de famille
- Date de naissance, année de naissance, genre
- Adresse postale complète (rue, ville, province, code postal)
- Numéro de téléphone (personnel, travail, secondaire)
- Email personnel (distinct de l'email professionnel)
- Contact d'urgence (nom + téléphone)
- Photo / avatar

### Catégorie 3 — Données professionnelles (protection de base)

Réf : art. 2. Contrôle d'accès par rôle suffisant.

- Email professionnel
- Poste, département, date d'embauche
- Numéro d'employé
- Équipement assigné (camion, cellulaire, ordinateur, iPad)

## Exigences techniques par couche

### Base de données (Supabase/PostgreSQL)

**Chiffrement au repos — Catégorie 1 obligatoire (art. 10) :**

Art. 10 : « Une personne qui exploite une entreprise doit prendre les **mesures de sécurité** propres à assurer la protection des renseignements personnels [...] contre l'accès, l'utilisation, la communication, la modification ou la destruction non autorisés. »

```sql
-- Activer pgcrypto
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Chiffrer un champ sensible
UPDATE employees SET allergies_encrypted = pgp_sym_encrypt(allergies, current_setting('app.encryption_key'));

-- Déchiffrer à la lecture (dans une fonction RLS-protégée)
SELECT pgp_sym_decrypt(allergies_encrypted, current_setting('app.encryption_key')) as allergies;
```

**Politiques RLS obligatoires (art. 20) :**

Art. 20 : « L'accès [...] aux renseignements personnels détenus par une personne qui exploite une entreprise est réservé à ses employés ou mandataires qui ont **qualité pour les connaître** dans l'exercice de leurs fonctions. »

- Chaque table contenant des PII DOIT avoir RLS activé
- Principe du moindre privilège : un employé ne voit que ses propres données
- Un gestionnaire ne voit que les données de son équipe directe
- Les données de Catégorie 1 nécessitent un accès restreint aux RH et admin

**Audit trail obligatoire (art. 3.5, 3.8) :**

La capacité de retracer les accès aux données est essentielle pour :
- Détecter les incidents de confidentialité (art. 3.5)
- Alimenter le registre des incidents (art. 3.8)
- Évaluer le risque de préjudice (art. 3.7)
- Journaliser : user_id, table accédée, champs consultés, timestamp, IP

**Exactitude et conservation (art. 11) :**

Art. 11 : Les renseignements personnels utilisés pour prendre une décision relative à la personne concernée doivent être **à jour et exacts**. Ils doivent être conservés aussi longtemps que nécessaire pour la prise de décision et au **minimum pendant la durée prévue par règlement** pour permettre à la personne d'exercer son droit d'accès.

### API / Backend

**Exposition minimale (art. 4, 20) :**

Art. 4 : La collecte doit se limiter à ce qui est **nécessaire à l'objet du dossier**. Art. 20 : Seuls ceux qui ont « qualité pour connaître » y ont accès.

- Ne jamais retourner tous les champs d'un profil dans une seule requête
- Séparer les endpoints par niveau de sensibilité
- Les champs de Catégorie 1 nécessitent une authentification renforcée

**Logging sécuritaire (art. 10) :**

Les mesures de sécurité incluent la protection contre la divulgation accidentelle dans les logs.

- JAMAIS de PII dans les logs (noms, emails, téléphones, adresses)
- Utiliser des identifiants anonymisés (user_id UUID) dans les logs
- Filtrer les champs sensibles avant la sérialisation des logs

**Transfert hors Québec (art. 17) :**

Art. 17 al. 1 : Avant de communiquer un renseignement personnel à l'extérieur du Québec, l'entreprise doit s'assurer que le renseignement bénéficiera d'une **protection équivalente**. Al. 2 : Une **EFVP** doit être réalisée avant la communication, tenant compte de la sensibilité du renseignement, de la finalité, et du régime juridique applicable dans l'État concerné.

**Obligations des mandataires/sous-traitants (art. 18.3) :**

Art. 18.3 : Le mandataire ou la personne à qui des renseignements sont communiqués doit **n'utiliser les renseignements que pour les fins prévues au contrat** et ne pas les conserver après l'expiration du contrat. Un contrat écrit est requis.

### Frontend (React/TypeScript)

**Masquage à l'affichage (art. 10, 20) :**
- Téléphone : afficher `514-***-1234` (premiers 3 + derniers 4)
- Email personnel : afficher `j***@gmail.com`
- Adresse : afficher seulement la ville et province
- NAS : JAMAIS affiché, même masqué
- Date de naissance : afficher seulement l'année ou l'âge

**Confidentialité par défaut (art. 9.1) :**
- Les paramètres de partage et de visibilité doivent être désactivés par défaut
- L'utilisateur doit activer manuellement tout partage de ses données

**Contrôle d'accès UI (art. 20) :**
- Les onglets contenant des PII de Catégorie 1 doivent vérifier le rôle côté client ET serveur
- Afficher un message « Accès restreint » plutôt que masquer silencieusement

### Politique de rétention et suppression (art. 23, 27)

**Destruction/Anonymisation (art. 23) :**

Art. 23 al. 1 : Lorsque les fins auxquelles un renseignement personnel a été recueilli sont accomplies, l'entreprise doit le **détruire** ou l'**anonymiser**. Al. 3 : L'anonymisation doit se faire selon les **meilleures pratiques généralement reconnues** et selon les critères et modalités déterminés par règlement. L'anonymisation doit être **irréversible** — il ne doit plus être raisonnablement possible d'identifier directement ou indirectement la personne.

**Portabilité (art. 27 al. 3) :**

Art. 27 al. 3 : La personne peut demander que les renseignements recueillis auprès d'elle lui soient communiqués dans un **format technologique structuré et couramment utilisé**, ou qu'ils soient communiqués à une personne ou un organisme autorisé par la loi à recueillir ce renseignement.

## Patterns de détection dans le code

### Noms de colonnes typiques contenant des PII

```
# Catégorie 1 (sensibles — art. 12 al. 2)
allergies, medical_*, health_*, salary*, wage*, pay_*, rrsp*, benefit*,
sin, nas, social_insurance, biometric*, orientation*, ethnicity*, religion*

# Catégorie 2 (personnelles)
birth_date, birth_year, date_of_birth, gender, sex,
phone, telephone, mobile, cell, personal_email,
address, street, city, postal_code, zip_code,
emergency_contact*, next_of_kin*,
first_name, last_name, full_name (quand combinés avec d'autres PII)

# Catégorie 3 (professionnelles)
email (professionnel), position, department, hire_date, employee_number
```

### Patterns de code à risque

```typescript
// RISQUE (art. 4, 20): Select * expose tous les champs PII
.select('*')

// RISQUE (art. 20): Pas de filtrage RLS visible
.from('employees').select('phone, address, birth_date')

// RISQUE (art. 10): PII dans les logs
console.log('User data:', userData)
logger.info({ email, phone }, 'Profile updated')

// RISQUE (art. 10): PII dans les URL params
navigate(`/profile?email=${email}&phone=${phone}`)

// RISQUE (art. 10): PII stockée dans localStorage
localStorage.setItem('userProfile', JSON.stringify(profile))

// RISQUE (art. 12.1): Décision automatisée sans transparence
if (chatbot.recommend('deny_leave', employeeData)) { ... }

// RISQUE (art. 9.1): Partage activé par défaut
const defaultSettings = { shareProfile: true, publicDirectory: true }
```

## Ressources détaillées

Pour les règles d'audit détaillées par composant, consulter :
- `references/regles-audit-db.md` — Règles spécifiques base de données
- `references/regles-audit-frontend.md` — Règles spécifiques frontend
- `references/regles-audit-api.md` — Règles spécifiques API et logs
- `references/modele-rapport.md` — Template du rapport d'audit
