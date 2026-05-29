# Skill
`toloka.client.skill.Skill` | [Source code](https://github.com/Toloka/toloka-kit/blob/v1.2.1/src/client/skill.py#L11)

```python
Skill(
    self,
    *,
    name: Optional[str] = None,
    private_comment: Optional[str] = None,
    hidden: Optional[bool] = None,
    skill_ttl_hours: Optional[int] = None,
    training: Optional[bool] = None,
    public_name: Optional[Dict[str, str]] = None,
    public_requester_description: Optional[Dict[str, str]] = None,
    owner: Optional[Owner] = None,
    id: Optional[str] = None,
    created: Optional[datetime] = None
)
```

Some characteristic of a Toloker described by a number from 0 to 100.


A `Skill` describes some characteristic, for example the percentage of correct responses.
Skills can be used to filter Tolokers.

Skill values are assigned to Tolokers by quality control rules, or manually. The values are accessed via the [UserSkill](toloka.client.user_skill.UserSkill.md) class.

Learn more about the [Toloker skills](https://toloka.ai/docs/guide/nav/).

## Parameters Description

| Parameters | Type | Description |
| :----------| :----| :-----------|
`name`|**Optional\[str\]**|<p>The skill name.</p>
`public_name`|**Optional\[Dict\[str, str\]\]**|<p>The skill name visible to Tolokers. The name can be provided in several languages.</p>
`public_requester_description`|**Optional\[Dict\[str, str\]\]**|<p>The skill description visible to Tolokers. The description can be provided in several languages.</p>
`private_comment`|**Optional\[str\]**|<p>Comments visible to a requester.</p>
`hidden`|**Optional\[bool\]**|<p>Visibility of the skill values to Tolokers:</p> <ul> <li>`True` — Tolokers don't see the information about the skill.</li> <li>`False` — Tolokers see the name and the value of the assigned skill.</li> </ul> <p>Default value: `True`.</p>
`skill_ttl_hours`|**Optional\[int\]**|<p>A lifetime in hours. If the skill value assigned to a Toloker is not updated for `skill_ttl_hours`, the skill is removed from a Toloker's profile.</p>
`training`|**Optional\[bool\]**|<p>Whether the skill is related to a training pool:</p> <ul> <li>`True` — The skill value is set after completing a training pool.</li> <li>`False` — The skill isn't related to a training pool.</li> </ul>
`owner`|**Optional\[[Owner](toloka.client.owner.Owner.md)\]**|<p>The skill owner.</p>
`id`|**Optional\[str\]**|<p>The skill ID. Read-only field.</p>
`created`|**Optional\[datetime\]**|<p>The UTC date and time when the skill was created. Read-only field.</p>

**Examples:**

Creating a new skill if it doesn't exist.

```python
segmentation_skill = next(toloka_client.get_skills(name='Road signs detection'), None)
if segmentation_skill:
    print(f'Skill exists. ID: {segmentation_skill.id}')
else:
    segmentation_skill = toloka_client.create_skill(
        name='Road signs detection',
        public_requester_description={
            'EN': 'The quality of selecting road signs on images',
            'RU': 'Качество выделения дорожных знаков на фотографиях',
        },
    )
    print(f'Skill created. ID: {segmentation_skill.id}')
```
