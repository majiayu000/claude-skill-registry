---
name: schema
description: '- CoolDown string[]'
---

## TOSSkill :: TOSEntity

#### Properties
- CoolDown `string[]`
- Effect `string`
- Effect_SkillFactor `string`
- Effect_CaptionRatio `string`
- Effect_CaptionRatio2 `string`
- Effect_CaptionRatio3 `string`
- Element `TOSElement`
- IsBunsin `boolean`
- IsSimony `boolean`
- LevelMax `int`
- LevelPerCircle `int`
- OverHeat `int`
- Prop_BasicCoolDown `int`
- Prop_BasicPoison `number`
- Prop_BasicSP `int`
- Prop_LvUpSpendPoison `number`
- Prop_SklAtkAdd `number`
- Prop_SklAtkAddByLevel `number`
- Prop_SklFactor `number`
- Prop_SklFactorByLevel `number`
- Prop_SklSR `number`
- Prop_SpendItemBaseCount `number`
- RequiredCircle `int`
- RequiredStance `TOSSkillRequiredStance[]`
- RequiredStanceCompanion `TOSSkillRequiredStanceCompanion`
- RequiredSubWeapon `boolean`
- SP `string[]`
- SPPerLevel `int`
- TypeAttack `TOSAttackType`

#### Links
- Link_Attributes `TOSEntityLink[]`
- Link_Gem `TOSEntityLink`
- Link_Job `TOSEntityLink`

### TOSSkillRequiredStanceCompanion
- BOTH
- NO
- YES

## TOSSkillRequiredStance
#### Properties
- Icon `Icon`
- Name `string`
