# ConnectWise::Skill

## Properties

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **name** | **String** |  Max length: 50; |  |
| **category** | [**SkillCategoryReference**](SkillCategoryReference.md) |  |  |
| **id** | **Integer** |  | [optional] |
| **_info** | **Hash&lt;String, String&gt;** |  | [optional] |

## Example

```ruby
require 'connect_wise'

instance = ConnectWise::Skill.new(
  name: null,
  category: null,
  id: null,
  _info: null
)
```

