---
name: nutrient-metabolism
description: Biochemical metabolism of macronutrients and key micronutrients — digestion, absorption, transport, utilization, and excretion — with emphasis on the pathways that matter for dietary-guideline debates (insulin response, lipoprotein metabolism, one-carbon metabolism, iron homeostasis). Use when a question asks what happens biochemically to a food after it is eaten, or when a claim about "metabolic effect" needs to be tested against mechanism.
type: skill
category: nutrition
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/nutrition/nutrient-metabolism/SKILL.md
superseded_by: null
---
# Nutrient Metabolism

Dietary claims that sound plausible at the food level sometimes collapse when examined at the metabolic level, and dietary claims that sound implausible at the food level sometimes turn out to have solid biochemical support. This skill grounds the department in the pathways that recur in nutrition debates: how macronutrients are digested and transported, what the lipoprotein system actually does, where insulin and glucagon fit, why iron is unlike other minerals, and what one-carbon metabolism has to do with folate recommendations. It is not a replacement for a biochemistry course; it is a working reference for the questions the department actually sees.

**Agent affinity:** atwater (macronutrient calorimetry), ancel-keys (lipid metabolism and the saturated-fat question)

**Concept IDs:** nutrition-biochemistry, nutrition-lipid-metabolism, nutrition-glucose-insulin

## Macronutrient digestion and absorption

### Carbohydrate

Complex carbohydrates are hydrolyzed stepwise. Salivary amylase begins starch digestion in the mouth; pancreatic amylase continues in the duodenum, producing maltose, maltotriose, and alpha-limit dextrins. Brush-border enzymes (maltase, sucrase, lactase, isomaltase) finish the job, producing monosaccharides: glucose, fructose, and galactose.

- **Glucose and galactose** are absorbed via SGLT1 (sodium-coupled) and enter the portal circulation.
- **Fructose** is absorbed via GLUT5 (sodium-independent) and enters the portal circulation. Hepatic fructose metabolism bypasses the phosphofructokinase regulatory step, which is one reason fructose loading differs metabolically from glucose loading.

Dietary fiber resists small-intestine hydrolysis and reaches the colon, where gut microbes ferment it to short-chain fatty acids (acetate, propionate, butyrate). SCFAs are absorbed by the colonocytes and contribute ~2 kcal/g of fiber, which is the basis for the reduced Atwater factor for fiber.

### Protein

Protein digestion begins with pepsin in the acidic stomach, continues with pancreatic proteases (trypsin, chymotrypsin, elastase, carboxypeptidases), and is finished by brush-border peptidases. The products — free amino acids and di/tripeptides — are absorbed through multiple transporters and enter the portal circulation.

The liver is the first stop for absorbed amino acids, and it exerts substantial control over systemic amino acid levels. A high-protein meal raises portal amino acids sharply but systemic amino acids more modestly because the liver is actively extracting and metabolizing them. This matters for interpreting "protein pulse" claims.

### Fat

Dietary fat is emulsified by bile salts, hydrolyzed by pancreatic lipase (and colipase) to monoglycerides and free fatty acids, packaged into mixed micelles, and absorbed at the enterocyte brush border. Long-chain fatty acids are re-esterified to triglycerides in the enterocyte and packaged into **chylomicrons** that enter the lymphatic system and bypass the portal circulation. Short- and medium-chain fatty acids are absorbed directly into the portal circulation.

This lymphatic-vs-portal split is not merely anatomical trivia. It means that long-chain dietary fat initially bypasses the liver, arriving instead at adipose tissue and muscle via peripheral circulation. The liver sees fat second, not first.

## The lipoprotein system

Almost every popular claim about "cholesterol" depends on the lipoprotein system, and almost every popular claim simplifies it into uselessness.

### The five lipoprotein classes

| Class | Density | Primary role | Primary apoprotein |
|---|---|---|---|
| Chylomicrons | lowest | Transport dietary fat from intestine to periphery | apoB-48 |
| VLDL | low | Transport hepatic TG to periphery | apoB-100 |
| IDL | intermediate | VLDL remnants | apoB-100 |
| LDL | low | Cholesterol delivery; VLDL/IDL terminus | apoB-100 |
| HDL | high | Reverse cholesterol transport | apoA-I |

Chylomicrons carry dietary fat; VLDL carries hepatic fat. Both lose triglyceride at peripheral tissues (lipoprotein lipase hydrolyzes TG to FFA for tissue uptake) and shrink, becoming remnants. VLDL remnants are further processed into LDL. LDL particles circulate longer and deliver cholesterol to peripheral tissues via the LDL receptor. HDL moves cholesterol from tissues back toward the liver.

### The apoB-containing particles

The cardiovascular risk literature has been converging for two decades on the finding that **apoB particle count** — essentially, the number of atherogenic particles in circulation — is a better predictor of atherosclerosis than total LDL cholesterol. Every LDL particle carries one apoB; small dense LDL particles have less cholesterol per particle than large buoyant ones, so a person with many small dense LDL has a higher apoB count than their LDL-C would suggest.

This matters for dietary debates because the metabolic effect of different diets on LDL particle *count* and *size* is not identical to their effect on LDL-C. A diet that lowers LDL-C while shifting particles toward small dense forms is not necessarily lowering cardiovascular risk.

### The saturated-fat question, biochemically

The Ancel Keys hypothesis — that saturated fat raises LDL-C and cardiovascular risk — remains contested in the popular literature but is supported by the following biochemical observations:

1. Saturated fatty acids suppress LDL receptor expression, slowing LDL clearance.
2. Slowed LDL clearance raises LDL particle count in circulation.
3. Higher LDL particle count correlates with atherosclerosis across multiple study designs.

The challenges to this story do not typically dispute the biochemistry; they dispute the magnitude of effect, the relevance of the intermediate biomarker (LDL-C) to the clinical outcome, and the appropriate comparator (what replaces the saturated fat matters). See the contested-claims-in-nutrition skill for the full debate.

## Glucose, insulin, and the beta-cell

Postprandial glucose is sensed by pancreatic beta cells, which release insulin in proportion to blood glucose. Insulin signals three major responses:

1. **Skeletal muscle and adipose** increase glucose uptake via GLUT4 translocation.
2. **Liver** stops gluconeogenesis and glycogenolysis, and begins glycogen synthesis.
3. **Adipose** increases triglyceride storage and decreases lipolysis.

In type 2 diabetes, peripheral tissues become insulin-resistant, requiring more insulin to achieve the same glucose response. Over time, beta cells fail to keep up and fasting glucose rises. The condition is characterized by insulin resistance plus beta-cell insufficiency.

The glycemic index of a carbohydrate food reflects its postprandial glucose response relative to a reference food (usually pure glucose or white bread). Low-GI foods produce slower, lower glucose peaks and correspondingly lower insulin peaks. Whether this matters clinically is a live debate — in people with normal glucose tolerance, the difference is often metabolically irrelevant; in people with diabetes or pre-diabetes, it matters substantially more.

## Iron — the unusual mineral

Most minerals are regulated by excretion: intake is absorbed freely, and excess is excreted. Iron is the exception. Humans have no regulated excretion pathway for iron; homeostasis is achieved at the absorption step.

- **Heme iron** (from animal sources) is absorbed via a dedicated heme transporter at roughly 15–35% efficiency regardless of body stores.
- **Non-heme iron** (from plant sources) is absorbed via DMT1 at highly variable efficiency — 2–20% depending on body stores, ascorbate co-ingestion, phytate and tannin content, and calcium co-ingestion.

**Hepcidin** is the master regulator. Produced by the liver in proportion to iron stores and inflammation, hepcidin binds ferroportin on enterocytes and macrophages and triggers its degradation, effectively closing the absorption gate. High body iron or active inflammation raises hepcidin and suppresses absorption.

This matters for dietary assessment: a person with depleted stores will absorb non-heme iron two to four times more efficiently than a replete person. Static absorption estimates are misleading.

## One-carbon metabolism and folate

Folate is a cofactor in one-carbon transfer reactions that produce methyl groups for DNA, protein, and lipid methylation, and that supply methionine from homocysteine. Inadequate folate (or inadequate B12, which works in the same pathway) disrupts methylation and raises homocysteine.

The US and Canada fortified grain products with folic acid starting in 1998 specifically to reduce the risk of neural tube defects, which are known to be reduced by periconceptional folate supplementation. The fortification program is one of the clearest nutrition-policy success stories — neural tube defect rates fell substantially after implementation — and is a worked example of what a well-targeted population nutrition intervention can accomplish when the science is solid.

## Worked example — why replacing saturated fat with sugar does not help

A 1970s dietary guideline told people to reduce saturated fat. Many people replaced saturated fat calories with refined carbohydrates (sugary foods became abundant precisely because they were "low fat"). The biochemical consequence:

1. The refined carbohydrate is rapidly digested to glucose and fructose.
2. Elevated insulin drives hepatic de novo lipogenesis, producing VLDL.
3. VLDL elevation lowers HDL and raises small dense LDL.
4. The apoB particle count does not improve, and may worsen.

This is the mechanistic explanation for why "low fat" public-health guidance paired with refined-carbohydrate consumption did not deliver the expected cardiovascular benefit. The lesson is not "saturated fat was fine" — it is "the comparator matters." Replacing saturated fat with unsaturated fat or with whole-food carbohydrate produces a very different outcome than replacing it with refined carbohydrate.

## Worked example — why glutamine supplementation is oversold

Glutamine is the most abundant free amino acid in plasma and is a major fuel for enterocytes and immune cells. A wave of popular nutrition claims in the 1990s promoted glutamine supplementation for gut health, immune function, and athletic recovery.

Biochemically, glutamine is **conditionally essential** — synthesized endogenously except in severe catabolic stress (burns, sepsis, major trauma). In those contexts, IV glutamine has shown clinical benefit. In healthy free-living people, oral glutamine supplementation produces almost no change in plasma glutamine because the gut and liver metabolize most of the dose on first pass. The mechanism that makes glutamine important in burn units is the mechanism that makes oral supplementation in healthy people mostly pointless.

## Assessment protocol for a metabolic claim

When a user presents a "metabolic effect" claim, the skill provides a check:

1. **Name the biochemistry.** What pathway is the claim touching? Lipid metabolism? Glucose-insulin? One-carbon? Micronutrient absorption?
2. **Check plausibility at the molecular level.** Does the proposed effect require a transporter, receptor, or enzyme that does not exist in humans? Does it require a concentration that is physiologically impossible?
3. **Distinguish mechanism from magnitude.** A plausible mechanism can have a clinically irrelevant magnitude. "This food contains X, which in vitro affects pathway Y" is not evidence that eating the food matters clinically.
4. **Check for first-pass and homeostatic corrections.** Many nutrients are extensively metabolized by the gut and liver before reaching systemic circulation; many have homeostatic feedback loops that damp supplementation effects.
5. **Route to the appropriate specialist.** Atwater for energy/macronutrient accounting, ancel-keys for lipid-CV questions, marion-nestle for the food-politics angle, adelle-davis (with transparency) for examples of historical mechanism claims that did not replicate.

## Routing heuristics

- Mechanism of macronutrient energy → atwater
- Mechanism of lipids and cardiovascular biomarkers → ancel-keys
- Mechanism of a claim tied to a specific food or supplement the user is considering → contested-claims-in-nutrition skill
- Pediatric metabolism and growth → satter

## Common failure modes

- **In vitro to in vivo extrapolation** without checking physiological concentration.
- **Ignoring first-pass hepatic metabolism** for orally consumed nutrients.
- **Treating single-biomarker endpoints as clinical outcomes** (LDL-C is not cardiovascular death; hemoglobin A1c is not diabetic retinopathy).
- **Conflating pharmacological and dietary doses** — IV glutamine in sepsis is not oral glutamine in a shake.

## Further reading

- Gropper and Smith, *Advanced Nutrition and Human Metabolism* (textbook reference)
- Sniderman et al. on apoB and cardiovascular risk
- Ganz, *Hepcidin and iron regulation*, NEJM review
- Institute of Medicine, DRI volume on folate and B-vitamins
