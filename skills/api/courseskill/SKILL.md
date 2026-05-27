# CourseSkill


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**course_id** | **str** | The edX course ID string for the course. | 
**skills** | [**List[Skill]**](Skill.md) |  | 

## Example

```python
from iblai.models.course_skill import CourseSkill

# TODO update the JSON string below
json = "{}"
# create an instance of CourseSkill from a JSON string
course_skill_instance = CourseSkill.from_json(json)
# print the JSON string representation of the object
print(CourseSkill.to_json())

# convert the object into a dict
course_skill_dict = course_skill_instance.to_dict()
# create an instance of CourseSkill from a dict
course_skill_from_dict = CourseSkill.from_dict(course_skill_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


