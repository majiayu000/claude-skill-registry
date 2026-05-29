---
name: requete-cph-licenciement-faute-grave-selim-brihi
description: Rédaction de requêtes devant le Conseil de prud'hommes pour contester un licenciement pour faute grave. Utiliser ce skill quand l'utilisateur demande de rédiger une requête CPH, contester un licenciement pour faute grave, préparer une saisine du CPH pour un litige lié à un licenciement, ou créer un document de contestation de licenciement en droit du travail français.
metadata:
  author: Sélim Brihi
  license: AGPL-3.0
  version: 2026.01.23
---

# Requête CPH - Contestation Licenciement pour Faute Grave

Ce skill guide la rédaction de requêtes devant le Conseil de prud'hommes (juridiction du travail français) pour un salarié contestant son licenciement pour faute grave et demandant la requalification en licenciement sans cause réelle et sérieuse.

## Informations à collecter AVANT de commencer la rédaction

Avant de rédiger la requête, impérativement collecter les informations suivantes auprès de l'utilisateur :

### 1. INFORMATIONS SUR LE SALARIÉ (Demandeur)
- Nom et prénom
- Date et lieu de naissance
- Nationalité
- Adresse complète
- Profession/poste occupé

### 2. INFORMATIONS SUR L'EMPLOYEUR (Défendeur)
- Dénomination sociale
- Forme juridique (SAS, SARL, SA, Association, etc.)
- Numéro SIRET
- Numéro RCS et ville d'immatriculation
- Adresse du siège social
- Effectif de l'entreprise (< ou > 11 salariés)
- Code APE
- Convention collective applicable (nom et numéro IDCC)

### 3. INFORMATIONS SUR LA RELATION DE TRAVAIL
- Date d'embauche
- Type de contrat (CDI écrit)
- Qualification/fonction
- Statut (Cadre ou Non-cadre)
- Salaire brut mensuel moyen (calculé sur les 3 ou 12 derniers mois)
- Ancienneté (calculée à la date du licenciement)
- Lieu de travail

### 4. INFORMATIONS SUR LA PROCÉDURE DE LICENCIEMENT
- Date de la convocation à l'entretien préalable
- Date de l'entretien préalable
- Date de notification du licenciement (date de la lettre)
- Motif invoqué par l'employeur dans la lettre de licenciement
- Contenu exact de la lettre de licenciement (si disponible)

### 5. INFORMATIONS SUR LES FAITS
- Historique de la relation de travail (durée, incidents éventuels, évaluations)
- Contexte du licenciement (événements ayant précédé le licenciement)
- Griefs invoqués par l'employeur
- Arguments du salarié contestant ces griefs
- Éléments de preuve disponibles (témoignages, emails, documents, etc.)
- Tentative de résolution amiable (si applicable)

### 6. INFORMATIONS SUR L'AVOCAT (si représenté)
- Nom et prénom
- Barreau
- Toque (si Barreau de Paris)
- Adresse du cabinet
- Téléphone et email

### 7. DEMANDES FINANCIÈRES SOUHAITÉES
Expliquer au salarié les différentes indemnités possibles et l'aider à les calculer :
- Indemnité pour licenciement sans cause réelle et sérieuse (minimum légal selon ancienneté et effectif)
- Indemnité légale de licenciement
- Indemnité compensatrice de préavis
- Congés payés afférents au préavis
- Rappel de salaire (si mise à pied conservatoire injustifiée)
- Dommages-intérêts pour préjudices distincts (si applicable)
- Remboursement des allocations chômage (si applicable)

## Workflow de Rédaction

### Phase 1 : Collecte des informations
Collecter toutes les informations listées ci-dessus de manière interactive avec l'utilisateur. Voir [conseils-variations.md](references/conseils-variations.md) pour un exemple de dialogue.

### Phase 2 : Calcul des indemnités
Calculer les montants des différentes indemnités. Consulter [calculs-indemnites.md](references/calculs-indemnites.md) pour les formules et barèmes.

### Phase 3 : Rédaction de la requête
Rédiger la requête en suivant la structure en 9 parties. Consulter [structure-requete.md](references/structure-requete.md) pour le template complet.

### Phase 4 : Vérification et finalisation
Vérifier la cohérence du document. Voir la section "Finalisation" dans [conseils-variations.md](references/conseils-variations.md).

### Phase 5 : Création du document
Créer le document final en format .docx et le présenter à l'utilisateur.

## Références Détaillées

- **Structure de la requête** : Voir [structure-requete.md](references/structure-requete.md) pour le template complet des 9 parties (en-tête, identification des parties, avertissements légaux, rappel des faits, exposé des motifs, demandes, par ces motifs, signature)

- **Calculs des indemnités** : Voir [calculs-indemnites.md](references/calculs-indemnites.md) pour les formules de calcul du salaire de référence, de l'ancienneté, de l'indemnité légale de licenciement, du préavis, et le barème des indemnités pour licenciement sans cause réelle et sérieuse

- **Conseils et variations** : Voir [conseils-variations.md](references/conseils-variations.md) pour la jurisprudence clé, les conseils de rédaction, les points de vigilance, les exemples de dialogue, les variations selon les situations, et la checklist de finalisation
