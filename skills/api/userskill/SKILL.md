# UserSkill


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**skill** | [**Skill**](Skill.md) |  | 
**courses** | [**List[CoursePoint]**](CoursePoint.md) | Courses with skill and associated points | 
**resources** | [**List[ResourcePoint]**](ResourcePoint.md) | Resources with skill and associated points | 
**total_points** | **int** | Total points for skill | [readonly] 
**percentile** | **float** | Percentile of points for user. | [optional] 

## Example

```python
from iblai.models.user_skill import UserSkill

# TODO update the JSON string below
json = "{}"
# create an instance of UserSkill from a JSON string
user_skill_instance = UserSkill.from_json(json)
# print the JSON string representation of the object
print(UserSkill.to_json())

# convert the object into a dict
user_skill_dict = user_skill_instance.to_dict()
# create an instance of UserSkill from a dict
user_skill_from_dict = UserSkill.from_dict(user_skill_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


