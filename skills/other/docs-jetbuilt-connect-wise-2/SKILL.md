# ConnectWise::MemberSkill

## Properties

| Name | Type | Description | Notes |
| ---- | ---- | ----------- | ----- |
| **skill** | [**SkillReference**](SkillReference.md) |  |  |
| **skill_level** | **String** |  |  |
| **id** | **Integer** |  | [optional] |
| **certified_flag** | **Boolean** |  | [optional] |
| **years_experience** | **Integer** |  | [optional] |
| **notes** | **String** |  | [optional] |
| **member** | [**MemberReference**](MemberReference.md) |  | [optional] |
| **_info** | **Hash&lt;String, String&gt;** |  | [optional] |

## Example

```ruby
require 'connect_wise'

instance = ConnectWise::MemberSkill.new(
  skill: null,
  skill_level: null,
  id: null,
  certified_flag: null,
  years_experience: null,
  notes: null,
  member: null,
  _info: null
)
```

