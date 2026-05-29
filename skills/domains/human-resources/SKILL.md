---
# required metadata

title: Recruiting request skill
description: This article describes the Recruiting request skill entity for Dynamics 365 Human Resources.
author: jaredha
ms.date: 02/05/2021
ms.topic: article
ms.prod: 
ms.technology: 

# optional metadata

# ms.search.form: 
audience: Application User
# ms.devlang: 
# ms.tgt_pltfrm: 
ms.custom: 
ms.assetid: 
ms.search.region: Global
# ms.search.industry: 
ms.author: jaredha
ms.search.validFrom: 2021-02-05
ms.dyn365.ops.version: Human Resources
---

# Recruiting request skill


[!INCLUDE [PEAP](../includes/peap-1.md)]

[!include [Applies to Human Resources](../includes/applies-to-hr.md)]

This article describes the Recruiting request skill entity for Dynamics 365 Human Resources.

Physical name: mshr_hcmrecruitingrequestskillentity

### Description

Describes skill requirements for a RecruitingRequest.

### JSON representation

```json
{
    "mshr_recruitingrequestid": "String",
    "mshr_skillid": "String",
    "mshr_skilldescription": "String",
    "mshr_ratinglevelid": "String",
    "mshr_ratingmodelid": "String",
    "mshr_ratingleveldescription": "String",
    "mshr_dataareaid": "String",
    "_mshr_dataareaid_id_value": "Guid",
    "mshr_primaryfield": "String",
    "_mshr_fk_recruitingrequest_id_value": "Guid",
    "_mshr_fk_skill_id_value": "Guid",
    "_mshr_fk_ratinglevel_id_value": "Guid",
    "_mshr_fk_ratingmodel_id_value": "Guid",
    "mshr_hcmrecruitingrequestskillentityid": "Guid"
}
```

### Properties

| Property<br>**Physical name**<br>***Type*** | Use | Description |
| --- | --- | --- |
| **Recruiting Request Skill Entity ID**<br>mshr_hcmrecruitingrequestskillentityid<br>*GUID* | Read-only<br>Required | System-generated unique identifier for the **Recruiting Request Skill** record. |
| **Recruiting Request ID**<br>mshr_recruitingrequestid<br>*String* | Write-once<br>Required | The user-readable unique identifier of the associated recruiting request. |
| **Recruiting Request ID Value**<br>_mshr_fk_recruitingrequest_id_value<br>*GUID* | Read-only<br>Required<br> Foreign key: mshr_hcmrecruitingrequestentityid of mshr_hcmrecruitingrequestentity entity | System-generated unique identifier of the associated recruiting request. |
| **Skill ID**<br>mshr_skillid<br>*String*<br> | Write-once<br>Required | The user-readable unique identifier of the required skill. |
| **Skill ID Value**<br>_mshr_fk_skill_id_value<br>*GUID* | Read-only<br>Required<br>Foreign key: mshr_hcmskillentityid of mshr_hcmskillentity entity | System-generated unique identifier of the required skill. |
| **Rating Level ID**<br>mshr_ratinglevelid<br>*String* | Write-once<br>Optional | The required skill level value selected for the job, based on the rating model assigned to the skill. |
| **Rating Level ID Value**<br>_mshr_fk_ratinglevel_id_value<br>*GUID* | Read-only<br>Optional<br>Foreign key: mshr_hcmratinglevelentityid of mshr_hcmratinglevelentity entity | System-generated unique identifier for the level. |
| **Skill Description**<br>mshr_skilldescription<br>*String* | Read-only<br>Required | The skill description. |
| **Rating Level Description**<br>mshr_ratingleveldescription<br>*String* | Read-only<br>Optional | The description of the selected skill level. |
| **Data Area ID**<br>mshr_dataareaid<br>*String* | Read/write<br>Optional | Specifies the legal entity (company). |
| **Data Area ID Value**<br>_mshr_dataareaid_id_value<br>*GUID* | Read-only<br>Optional<br>Foreign key: cdm_companyid of cdm_company entity | System-generated GUID value identifying the legal entity (company). |
| **Primary Field**<br>mshr_primaryfield<br>*String* | Read-only<br>Required | Concatenation of Recruiting Request value and Skill ID as another method to uniquely identify the record. |
| **Rating Model ID**<br>mshr_ratingmodelid<br>*String* | Read-write<br>Required | The rating model used to rate the skill. |
| **Rating Model ID Value**<br>_mshr_fk_hcmratingmodel_id_value<br>*GUID* | Read-only<br>Required<br>Foreign key: mshr_hcmratingmodelentityid of mshr_hcmratingmodelentity entity | System-generated unique identifier of the rating model used to rate the skill. |

## See also

[Applicant Tracking System integration API introduction](hr-admin-integration-ats-api-introduction.md)<br>
[Example query for Recruiting request](hr-admin-integration-ats-api-recruiting-request-example-query.md)


[!INCLUDE[footer-include](../includes/footer-banner.md)]
