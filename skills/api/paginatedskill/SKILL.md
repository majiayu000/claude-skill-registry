# PaginatedSkill


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_page** | **str** |  | 
**previous_page** | **str** |  | 
**results** | [**List[Skill]**](Skill.md) |  | [readonly] 
**count** | **int** |  | [readonly] 

## Example

```python
from iblai.models.paginated_skill import PaginatedSkill

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedSkill from a JSON string
paginated_skill_instance = PaginatedSkill.from_json(json)
# print the JSON string representation of the object
print(PaginatedSkill.to_json())

# convert the object into a dict
paginated_skill_dict = paginated_skill_instance.to_dict()
# create an instance of PaginatedSkill from a dict
paginated_skill_from_dict = PaginatedSkill.from_dict(paginated_skill_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


