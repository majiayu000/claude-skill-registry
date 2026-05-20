---
name: family-history
description: Generate FamilyMemberHistory resources with family relationships, heritable conditions, age of onset, and deceased status. Use when user mentions family history, hereditary, genetic risk, family member, parent, sibling, cancer history, heart disease in family, or FamilyMemberHistory.
keywords: [family history, hereditary, genetic, familial, family member, parent, mother, father, sibling, brother, sister, grandparent, cancer history, heart disease family, diabetes family, BRCA, Lynch syndrome, inherited, predisposition, consanguinity]
resource_types: [FamilyMemberHistory]
always: false
---

# Family Member History

Generate FamilyMemberHistory resources linking patients to heritable conditions in relatives.

## Relationship Codes

Use http://terminology.hl7.org/CodeSystem/v3-RoleCode:
- **Parents**: FTH (father), MTH (mother), NFTH (natural father), NMTH (natural mother),
  STPFTH (stepfather), STPMTH (stepmother), ADOPTF (adoptive father), ADOPTM (adoptive mother).
- **Siblings**: BRO (brother), SIS (sister), HBRO (half-brother), HSIS (half-sister),
  TWIN (twin), TWINBRO (twin brother), TWINSIS (twin sister).
- **Grandparents**: GRFTH (grandfather), GRMTH (grandmother),
  PGRFTH (paternal grandfather), MGRMTH (maternal grandmother).
- **Children**: SON, DAU, NCHILD (natural child), STPSON, STPDAU.
- **Extended**: UNCLE, AUNT, COUSN (cousin), NEPHEW, NIECE.

## Common Heritable Conditions

Include realistic condition codes (SNOMED CT / ICD-10):
- **Cardiovascular**: Coronary artery disease (53741008), Hypertension (38341003),
  Stroke (230690007), Cardiomyopathy (85898001).
- **Oncology**: Breast cancer (254837009), Colon cancer (93761005),
  Prostate cancer (399068003), Lung cancer (93880001), Ovarian cancer (363443007),
  Melanoma (372244006).
- **Metabolic**: Type 2 diabetes (44054006), Hyperlipidemia (55822004),
  Obesity (414916001).
- **Neurological**: Alzheimer's (26929004), Parkinson's (49049000),
  Huntington's (58756001), Epilepsy (84757009).
- **Genetic syndromes**: BRCA1/BRCA2 positive (412734009), Lynch syndrome (315058005),
  Sickle cell trait (16402000), Cystic fibrosis carrier (401150006),
  Hemophilia carrier (50536004).
- **Mental health**: Major depression (73867007), Bipolar disorder (13746004),
  Schizophrenia (58214004), Alcohol use disorder (7200002).
- **Autoimmune**: Rheumatoid arthritis (69896004), Lupus (55464009),
  Type 1 diabetes (46635009), Celiac disease (396331005).

## Status

- partial, completed, entered-in-error, health-unknown.
- Use **health-unknown** for adopted patients or unknown family members.

## Age and Deceased

- **age**: Use Age data type (e.g., onset at age 55) or ageRange.
- **deceasedBoolean** / **deceasedAge** / **deceasedDate**: Include for deceased relatives.
  Common pattern: father deceased at age 62 from MI.
- **bornDate**: Include approximate birth year when relevant.

## Clinical Patterns

- **Three-generation history**: Include parents + grandparents + siblings minimum.
- **Cancer clustering**: Multiple first-degree relatives with same cancer type →
  suggest genetic testing referral.
- **Cardiovascular family**: Father MI at 55, paternal grandfather stroke at 60,
  brother hypertension at 40.
- **Diabetes family**: Mother T2DM, maternal grandmother T2DM, sibling pre-diabetes.
- **Unknown history**: Adopted patients — use status "health-unknown".

## References

- FamilyMemberHistory.patient → Reference(Patient/{id}) — required.
- FamilyMemberHistory.reasonReference → Reference(Condition/{id}) — why documented.

