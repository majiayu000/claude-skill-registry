---
name: notification-licenciement-selim-brihi
description: Guide pour la rédaction de notifications de licenciement conformes au droit du travail français. Utiliser ce skill quand l'utilisateur demande de rédiger, préparer, créer ou éditer une lettre de notification de licenciement, notamment pour faute grave, faute lourde ou motif personnel. Le skill guide la collecte d'informations précises et la rédaction d'une notification juridiquement solide avec tous les éléments obligatoires du droit français.
metadata:
  author: Sélim Brihi
  license: AGPL-3.0
---

# Notification de Licenciement - Droit Français

Ce skill permet de rédiger des notifications de licenciement conformes au droit du travail français, en particulier pour les licenciements pour faute grave ou motif personnel.

## Principe Fondamental

**La motivation est CRITIQUE** : La lettre de notification de licenciement fixe définitivement les limites du litige en cas de contentieux. Le juge ne pourra examiner QUE les motifs mentionnés dans cette lettre. Il est donc ESSENTIEL de :

1. **Être exhaustif** : Mentionner TOUS les griefs que l'employeur souhaite invoquer
2. **Être précis** : Dater, circonstancier et détailler chaque fait reproché
3. **Être factuel** : S'appuyer sur des faits vérifiables et documentés
4. **Être cohérent** : Les griefs doivent justifier la qualification retenue (faute grave, etc.)

⚠️ **Plus la notification est détaillée et motivée, mieux l'employeur sera protégé en cas de contestation devant les tribunaux.**

## Workflow de Rédaction

### Phase 1 : Collecte des Informations Obligatoires

Avant de commencer la rédaction, collecter les informations suivantes en posant des questions à l'utilisateur :

#### A. Informations sur l'entreprise
- Raison sociale complète
- Forme juridique (SARL, SAS, SA, etc.)
- Adresse du siège social
- Capital social
- Numéro RCS et ville
- Code APE
- Téléphone, fax, email

#### B. Informations sur le salarié
- Civilité (M./Mme)
- Prénom et NOM
- Adresse complète du domicile

#### C. Informations sur le licenciement
- Date de la lettre
- Numéro de LRAR (si connu, sinon laisser à compléter)
- Numéro de référence interne (si applicable)
- **Type de licenciement** : Faute grave / Faute lourde / Motif personnel non disciplinaire
- Date de l'entretien préalable
- Présence ou absence du salarié à l'entretien
- Assistance éventuelle du salarié lors de l'entretien
- Date de la mise à pied conservatoire (si applicable)

#### D. Informations sur le contrat
- Date d'embauche
- Poste occupé / Qualification
- Type de contrat (CDI / CDD)
- Missions principales du poste (liste détaillée)
- Clauses particulières (mobilité, non-concurrence, confidentialité, etc.)

#### E. Les Griefs - ÉLÉMENTS CRITIQUES

**Pour CHAQUE grief, collecter :**

1. **Fait précis** : Qu'est-ce qui s'est passé exactement ?
2. **Date(s)** : Quand cela s'est-il produit ? (dates précises obligatoires)
3. **Contexte** : Dans quelles circonstances ?
4. **Preuves** : Comment a-t-on constaté le fait ? (badges, emails, témoignages, photos, rapports, etc.)
5. **Conséquences** : Quel impact pour l'entreprise ? (désorganisation, préjudice financier, d'image, risque juridique, etc.)
6. **Rappels antérieurs** : Le salarié a-t-il déjà été averti ? (avertissements, rappels à l'ordre, courriers, etc.)

**Types de griefs courants :**
- Absences injustifiées / Abandon de poste
- Insuffisance professionnelle grave
- Violation de règles de sécurité
- Insubordination / Refus d'exécuter des ordres
- Violation d'obligations contractuelles (mobilité, exclusivité, etc.)
- Fraude / Falsification / Vol
- Utilisation abusive de biens de l'entreprise
- Déloyauté / Concurrence déloyale
- Comportement inapproprié (violence, harcèlement, etc.)

**⚠️ INSISTER AUPRÈS DE L'UTILISATEUR :**
> "Il est essentiel de détailler au maximum les griefs avec des dates précises, des circonstances et des preuves. Plus la motivation est riche et circonstanciée, mieux vous serez protégé en cas de contestation devant le Conseil de Prud'hommes. Je vais vous guider pour chaque grief."

### Phase 2 : Consultation des Références

**Avant de rédiger, TOUJOURS consulter :**

1. **`references/mentions-obligatoires.md`** : Pour la structure complète et toutes les mentions légales obligatoires
2. **`references/exemples-griefs.md`** : Pour s'inspirer de formulations juridiquement solides

Utiliser l'outil `view` pour lire ces fichiers :
```
view references/mentions-obligatoires.md
view references/exemples-griefs.md
```

### Phase 3 : Rédaction de la Notification

#### Structure OBLIGATOIRE à respecter

```
[EN-TÊTE ENTREPRISE]
                                        [COORDONNÉES SALARIÉ]

[LIEU], LE [DATE]

Lettre recommandée avec avis de réception N° [NUMÉRO] + pli simple

Objet : Notification d'un licenciement pour [motif]
Pièce(s) jointe(s) : Portabilité des droits en matière de prévoyance
N° réf : [référence]

[Civilité],

[1. RÉFÉRENCE À L'ENTRETIEN PRÉALABLE]

[2. NOTIFICATION DE LA DÉCISION]

[3. EXPOSÉ DÉTAILLÉ DES MOTIFS - PARTIE CRITIQUE]

[4. CONSÉQUENCES DU LICENCIEMENT]

[5. DOCUMENTS DE FIN DE CONTRAT]

[6. RESTITUTION DU MATÉRIEL]

[7. PORTABILITÉ DE LA PRÉVOYANCE]

[8. CLAUSE DE NON-CONCURRENCE]

[9. DROIT À DEMANDE DE PRÉCISIONS]

[10. FORMULE DE POLITESSE]

[Signature]
```

#### Rédaction de l'Exposé des Motifs (Section Critique)

**Principes :**
- Commencer par une phrase d'introduction générale
- Présenter les griefs dans un ordre logique (chronologique ou par thème)
- Pour chaque grief : FAIT + DATE + CONTEXTE + PREUVE + CONSÉQUENCE
- Utiliser des transitions entre les griefs
- Conclure par une formule synthétisant la gravité

**Formulations à privilégier :**
- "Nous avons à déplorer [...]"
- "L'analyse des faits révèle [...]"
- "Nos vérifications ont établi que [...]"
- "Le [date précise], vous avez [fait précis] [...]"
- "Malgré nos demandes répétées [...]"
- "Cette situation a eu pour conséquence de [...]"
- "L'ensemble de ces faits constituent des fautes graves rendant impossible la poursuite de votre contrat de travail"

**Ce qu'il faut ÉVITER :**
- Formulations vagues : "Vous n'avez pas bien travaillé"
- Jugements de valeur : "Votre attitude déplorable"
- Faits non datés : "À plusieurs reprises" (toujours préciser les dates)
- Griefs non évoqués lors de l'entretien préalable
- Incohérences entre les faits et la qualification

### Phase 4 : Vérification Finale

Avant de présenter le document, vérifier la **CHECKLIST OBLIGATOIRE** :

- [ ] En-tête complet (entreprise + salarié)
- [ ] Mention LRAR + pli simple
- [ ] Référence à l'entretien préalable
- [ ] Motifs précis, datés et circonstanciés (AU MINIMUM 2-3 pages pour une faute grave)
- [ ] Chaque fait est daté avec précision
- [ ] Les preuves sont mentionnées
- [ ] Les conséquences sont expliquées
- [ ] Formule de gravité ("L'ensemble de ces faits constituent...")
- [ ] Conséquences du licenciement (rupture immédiate, pas d'indemnités)
- [ ] Documents de fin de contrat
- [ ] Restitution du matériel
- [ ] Portabilité de la prévoyance
- [ ] Clause de non-concurrence (position claire)
- [ ] Droit à demande de précisions (15 jours)
- [ ] Formule de politesse
- [ ] Signature

### Phase 5 : Création du Document

1. **Créer le document au format DOCX** en utilisant le skill `docx` 
2. Appliquer la mise en forme professionnelle :
   - Police : Arial ou Calibri 11pt
   - Interligne : 1.15 ou 1.5
   - Marges : normales
   - Alignement : justifié
   - En-tête en gras pour les coordonnées
   - Numéro de LRAR en italique

3. **Sauvegarder dans `/mnt/user-data/outputs/`**

4. **Présenter le fichier** à l'utilisateur avec l'outil `present_files`

## Conseils Juridiques Importants

### Distinction des Qualifications

**Faute grave :**
- Rend impossible le maintien du salarié dans l'entreprise, même pendant le préavis
- Rupture immédiate, sans préavis ni indemnité de licenciement
- Exemples : abandon de poste, insubordination grave, vol, violence

**Faute lourde :**
- Faute grave + intention de nuire à l'employeur
- Mêmes conséquences que faute grave + pas d'indemnité de CP
- Très difficile à prouver, éviter sauf cas évident

**Licenciement pour motif personnel non disciplinaire :**
- Insuffisance professionnelle, inaptitude
- Préavis et indemnités dus (sauf dispense de préavis)

### Erreurs à Éviter Absolument

1. **Motifs imprécis** : "Comportement inadapté" → Insuffisant
2. **Absence de dates** : "À plusieurs reprises" → Toujours dater
3. **Griefs nouveaux** : Ne jamais ajouter de faits non évoqués à l'entretien préalable
4. **Contradiction** : Entre les faits et la qualification (ex: licencier pour faute grave alors que les faits sont légers)
5. **Procédure non respectée** : Entretien préalable obligatoire, délai de 2 jours ouvrables minimum entre convocation et entretien

### Sécurisation Juridique

**Pour maximiser les chances de succès en cas de contentieux :**
- Accumuler un maximum de preuves documentées avant l'entretien
- Respecter scrupuleusement la procédure
- Rédiger une notification TRÈS détaillée (3-5 pages pour faute grave n'est pas excessif)
- Consulter un avocat spécialisé en droit du travail pour les cas complexes

## Interaction avec l'Utilisateur

### Ton à adopter :
- Professionnel et pédagogique
- Insister sur l'importance de la précision
- Poser des questions pour obtenir tous les détails nécessaires
- Ne pas hésiter à demander des précisions multiples

### Questions types à poser :
- "Pouvez-vous me donner la date EXACTE de ce fait ?"
- "Comment avez-vous constaté ce manquement ? Avez-vous des preuves (emails, témoignages, badges, etc.) ?"
- "Quelles ont été les conséquences concrètes de ce comportement pour l'entreprise ?"
- "Le salarié avait-il déjà été averti auparavant ? Si oui, quand et comment ?"
- "Y a-t-il d'autres faits similaires que vous souhaitez mentionner ?"

### Alertes à donner :
Si les informations fournies sont insuffisantes :
> "⚠️ ATTENTION : Les éléments fournis ne sont pas assez précis pour constituer une motivation solide. En cas de contestation, le juge pourrait considérer que le licenciement n'est pas justifié. Il est essentiel de [préciser ce qui manque]."

## Après la Rédaction

Une fois le document créé et présenté :

1. **Rappeler les étapes suivantes :**
   - Faire relire par un juriste/avocat (recommandé)
   - Envoyer en LRAR + pli simple
   - Conserver tous les justificatifs et preuves
   - Préparer les documents de fin de contrat

2. **Offrir de créer d'autres documents si nécessaire :**
   - Convocation à entretien préalable (si pas encore faite)
   - Lettre de mise à pied conservatoire
   - Note d'information portabilité prévoyance

## Ressources Intégrées

Ce skill inclut deux fichiers de référence essentiels dans le dossier `references/` :

- **`mentions-obligatoires.md`** : Structure complète avec toutes les mentions légales obligatoires et checklist
- **`exemples-griefs.md`** : Bibliothèque d'exemples de griefs bien rédigés, classés par type

Ces références doivent TOUJOURS être consultées avant de commencer la rédaction pour garantir la conformité juridique de la notification.
