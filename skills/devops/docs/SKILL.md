---
name: docs
description: Name | Type | Description | Notes
---

# UserRoutingSkill

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | Option<**String**> | The globally unique identifier for the object. | [optional][readonly]
**name** | Option<**String**> |  | [optional]
**proficiency** | Option<**f64**> | A rating from 0.0 to 5.0 that indicates how adept an agent is at a particular skill. When \"Best available skills\" is enabled for a queue in Genesys Cloud, ACD interactions in that queue are routed to agents with higher proficiency ratings. | [optional]
**state** | Option<**String**> | Activate or deactivate this routing skill. | [optional]
**skill_uri** | Option<**String**> | URI to the organization skill used by this user skill. | [optional][readonly]
**self_uri** | Option<**String**> | The URI for this object | [optional][readonly]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


