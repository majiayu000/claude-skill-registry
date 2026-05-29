# ReportedSkill


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **int** |  | [optional] 
**username** | **str** |  | [optional] 
**skills** | [**List[Skill]**](Skill.md) |  | 
**data** | **object** |  | [readonly] 

## Example

```python
from iblai.models.reported_skill import ReportedSkill

# TODO update the JSON string below
json = "{}"
# create an instance of ReportedSkill from a JSON string
reported_skill_instance = ReportedSkill.from_json(json)
# print the JSON string representation of the object
print(ReportedSkill.to_json())

# convert the object into a dict
reported_skill_dict = reported_skill_instance.to_dict()
# create an instance of ReportedSkill from a dict
reported_skill_from_dict = ReportedSkill.from_dict(reported_skill_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


