# DesiredSkill


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **int** |  | [optional] 
**username** | **str** |  | [optional] 
**skills** | [**List[Skill]**](Skill.md) |  | 
**data** | **object** |  | [readonly] 

## Example

```python
from iblai.models.desired_skill import DesiredSkill

# TODO update the JSON string below
json = "{}"
# create an instance of DesiredSkill from a JSON string
desired_skill_instance = DesiredSkill.from_json(json)
# print the JSON string representation of the object
print(DesiredSkill.to_json())

# convert the object into a dict
desired_skill_dict = desired_skill_instance.to_dict()
# create an instance of DesiredSkill from a dict
desired_skill_from_dict = DesiredSkill.from_dict(desired_skill_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


