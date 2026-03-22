# Skill

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**Synonyms** | Pointer to **[]string** |  | [optional] 
**Description** | Pointer to **string** |  | [optional] 
**GroupPriority** | Pointer to **int32** |  | [optional] 
**Important** | Pointer to **bool** |  | [optional] [default to false]

## Methods

### NewSkill

`func NewSkill() *Skill`

NewSkill instantiates a new Skill object
This constructor will assign default values to properties that have it defined,
and makes sure properties required by API are set, but the set of arguments
will change when the set of required properties is changed

### NewSkillWithDefaults

`func NewSkillWithDefaults() *Skill`

NewSkillWithDefaults instantiates a new Skill object
This constructor will only assign default values to properties that have it defined,
but it doesn't guarantee that properties required by API are set

### GetSynonyms

`func (o *Skill) GetSynonyms() []string`

GetSynonyms returns the Synonyms field if non-nil, zero value otherwise.

### GetSynonymsOk

`func (o *Skill) GetSynonymsOk() (*[]string, bool)`

GetSynonymsOk returns a tuple with the Synonyms field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetSynonyms

`func (o *Skill) SetSynonyms(v []string)`

SetSynonyms sets Synonyms field to given value.

### HasSynonyms

`func (o *Skill) HasSynonyms() bool`

HasSynonyms returns a boolean if a field has been set.

### GetDescription

`func (o *Skill) GetDescription() string`

GetDescription returns the Description field if non-nil, zero value otherwise.

### GetDescriptionOk

`func (o *Skill) GetDescriptionOk() (*string, bool)`

GetDescriptionOk returns a tuple with the Description field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetDescription

`func (o *Skill) SetDescription(v string)`

SetDescription sets Description field to given value.

### HasDescription

`func (o *Skill) HasDescription() bool`

HasDescription returns a boolean if a field has been set.

### GetGroupPriority

`func (o *Skill) GetGroupPriority() int32`

GetGroupPriority returns the GroupPriority field if non-nil, zero value otherwise.

### GetGroupPriorityOk

`func (o *Skill) GetGroupPriorityOk() (*int32, bool)`

GetGroupPriorityOk returns a tuple with the GroupPriority field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetGroupPriority

`func (o *Skill) SetGroupPriority(v int32)`

SetGroupPriority sets GroupPriority field to given value.

### HasGroupPriority

`func (o *Skill) HasGroupPriority() bool`

HasGroupPriority returns a boolean if a field has been set.

### GetImportant

`func (o *Skill) GetImportant() bool`

GetImportant returns the Important field if non-nil, zero value otherwise.

### GetImportantOk

`func (o *Skill) GetImportantOk() (*bool, bool)`

GetImportantOk returns a tuple with the Important field if it's non-nil, zero value otherwise
and a boolean to check if the value has been set.

### SetImportant

`func (o *Skill) SetImportant(v bool)`

SetImportant sets Important field to given value.

### HasImportant

`func (o *Skill) HasImportant() bool`

HasImportant returns a boolean if a field has been set.


[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


