---
id: skill
title: Skill
description: Behaviour Twin KIT
---

<div style={{display:'block'}}>
  <div style={{display:'inline-block', verticalAlign:'top'}}>

![Behaviour Twin KIT -- Remaining useful Life banner](@site/static/img/kit-icons/behaviour-twin-rul-kit-icon-mini.svg)

  </div>
  <div style={{display:'inline-block', fontSize:17, color:'rgb(255,166,1)', marginLeft:7, verticalAlign:'top', paddingTop:6}}>
Behaviour Twin KIT -- Remaining useful Life
  </div>
</div>

Applies to roles: *RuL skill provider* and *RuL consumer*

## SKILL DEFINITION

The example skill below is inteded to calculate RuL values of a vehicle part.

The *consumer* is also the *skill proivder*. It requests the calculation by providing the vehicle identification numbers (VINs) of the vehicles. The *data provider* is an OEM, the manufacturer of the vehicles. It provides the load data in form of load spectra. The supplier of the part (component of interest) provides the related RuL calculation service, which accepts load spectra as input arguments.

The *skill provider* (in this example the consumer, but could also be the *data provider*/OEM or a third party or a CAB body), has to implement the skill and register it over the *Agent Plane API*.

In the current example, a RuL skill for a gearbox is implemented with the [SPARQL 1.1 Query Language ![(external link)](/icons/external-link.svg)](https://www.w3.org/TR/sparql11-query/) as a query. The query is a federated query, which means that it is split into two parts, one for the *data provider*/OEM and one for the *calculation service provider*/supplier. In the first part, the OEM-owned reliability asset is queried to collect the load data of the vehicles with the given VINs and in the second part, the gathered data is fed back into the respective supplier EDC connector/agent to perform a RuL calculation.

For more information regarding skill development, registration and invocation options, see [Agents KIT's Operation View](../../../../knowledge-agents-kit/operation-view/agent-edc).

### FULL EXAMPLE

```sparql
################################################################
# Copyright (c) 2022-2024 T-Systems International GmbH
# Copyright (c) 2022-2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# Copyright (c) 2022-2024 ZF Friedrichshafen AG
# Copyright (c) 2022-2024 Allgemeiner Deutscher Automobil-Club e.V. (ADAC)
# Copyright (c) 2022-2024 Mercedes-Benz AG
# Copyright (c) 2022-2024 Contributors to the Catena-X Association
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
################################################################
# Sample for a Federated (Consumer-Deployed) SPARQL Skill which
#  - Jumps into an OEM-owned reliability asset given a set of candidate VINs
#  - Feeds the gathered data back into the respective supplier connector/agent
#.   to perform a health indication
# Author: cgjung
# (c) 2023-2024 Catena-X association
################################################################

PREFIX cx-common:       <https://w3id.org/catenax/ontology/common#>
PREFIX cx-core:         <https://w3id.org/catenax/ontology/core#>
PREFIX cx-vehicle:      <https://w3id.org/catenax/ontology/vehicle#>
PREFIX cx-reliability:  <https://w3id.org/catenax/ontology/reliability#>
PREFIX cx-behaviour:    <https://w3id.org/catenax/ontology/behaviour#>
PREFIX rdf:             <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:            <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:             <http://www.w3.org/2001/XMLSchema#>
PREFIX json:            <https://json-schema.org/draft/2020-12/schema#>
PREFIX bpnl:            <bpn:legal:>

################################################################
# Sample for a Federated (Consumer-Deployed) SPARQL Skill which
#  - Jumps into an OEM-owned reliability asset given a set of candidate VANs
#  - Feeds the gathered data back into the respective supplier connector/agent
#.   to perform a health indication
# Author: cgjung
# (c) 2023-2024 Catena-X association
################################################################

SELECT ?vehicle ?vin ?aggregate ?assembly ?supplier ?lc ?operatingTime ?mileage ?recordDate ?ls_type ?ls_name ?ls_value ?ls_unit ?ls_method ?ls_channels ?ls_classes ?ls_values ?distanceKm ?timeHours WHERE {

  VALUES (?vin ?aggregate ?ls_type) {
      ("@vin"^^xsd:string "Differential Gear"^^xsd:string "GearOil"^^xsd:string)
  }

  bpnl:BPNL000000000OEM cx-common:hasConnector ?oemEDC .
  ?oemEDC cx-common:offers [ rdfs:isDefinedBy <https://w3id.org/catenax/ontology/reliability> ; cx-common:id ?reliabilityAssetId ] .

  SERVICE ?oemEDC {
      GRAPH ?reliabilityAssetId {
        ?vehicle rdf:type cx-vehicle:Vehicle ;
            cx-vehicle:vehicleIdentificationNumber ?vin .

        ?assembly rdf:type cx-vehicle:Part ;
            cx-vehicle:name ?aggregate ;
            cx-vehicle:isPartOf ?vehicle ;
            cx-vehicle:supplier ?supplier .

        ?teleAnalysis rdf:type cx-reliability:Analysis ;
            cx-reliability:analysedObject ?assembly ;
            cx-reliability:operatingHoursOfVehicle ?operatingTime ;
            cx-reliability:mileageOfVehicle ?mileage ;
            cx-core:startDateTime ?recordDate ;
            cx-reliability:result [
                cx-core:id ?ls_type ;
                cx-core:name ?ls_name ;
                cx-reliability:countingValue ?ls_value ;
                cx-reliability:countingUnit ?ls_unit ;
                cx-reliability:countingMethod ?ls_method ;
                cx-reliability:channels ?ls_channels ;
                cx-reliability:classes ?ls_classes ;
                cx-reliability:values ?ls_values
            ] .
    } # OEM#GRAPH

    ?supplier cx-common:hasConnector ?supplierEDC.
    ?supplierEDC cx-common:offers [ rdfs:isDefinedBy <https://w3id.org/catenax/ontology/behaviour> ; cx-common:id ?prognosisAssetId ] .

    SERVICE ?supplierEDC {
        GRAPH ?prognosisAssetId {
            ?invocation a cx-behaviour:RemainingUsefulLife ;
                    cx-behaviour:sender bpnl:BPNL00000003AYRE ;
                    cx-behaviour:senderConnector ?oemEDC ;
                    cx-behaviour:recipient ?supplier ;
                    cx-behaviour:recipientConnector ?supplierEDC ;
                    cx-behaviour:targetDate ?recordDate ;
                    cx-behaviour:timeStamp ?recordDate ;
                    cx-behaviour:component "GearBox" ;
                    cx-behaviour:statusDate ?recordDate ;
                    cx-behaviour:statusOperatingHours ?operatingTime ;
                    cx-behaviour:statusMileage ?mileage ;
                    cx-behaviour:countingValue ?ls_value ;
                    cx-behaviour:countingUnit ?ls_unit ;
                    cx-behaviour:countingMethod ?ls_method ;
                    cx-behaviour:headerChannels ?ls_channels ;
                    cx-behaviour:bodyClasses ?ls_classes ;
                    cx-behaviour:bodyCountsList ?ls_values ;
                    cx-behaviour:remainingOperatingHours ?timeHours ;
                    cx-behaviour:remainingRunningDistance ?distanceKm .
        } # SUPPLIER#GRAPH
    } # SUPPLIER#CATALOG

  } # OEM#CATALOG

} # SELECT
```

### DETAILED INFORMATION

#### SELECT STATEMENT

The select statement defines, which data should be returned.

```sparql
SELECT ?vehicle ?vin ?aggregate ?assembly ?supplier ?lc ?operatingTime ?mileage ?recordDate ?ls_type ?ls_name ?ls_value ?ls_unit ?ls_method ?ls_channels ?ls_classes ?ls_values ?distanceKm ?timeHours WHERE {
```

#### PARAMETERS

The parameter `vin` (list of VINs for vehicles of interest) is the only external parameter that is provided by the caller of this skill. `aggregate` is set to `Differential Gear` to identify the component of interest (gearbox). `ls_type` is set to `GearOil`. This is done, because prognosis functions for the given gearbox can provide RuL values for that.

```sparql
  VALUES (?vin ?aggregate ?ls_type) {
      ("@vin"^^xsd:string "Differential Gear"^^xsd:string "GearOil"^^xsd:string)
  }
```

#### ASSET RESOLUTION

The OEM's business partner number (BPNL) is known. A entity can have only one BPNL, but more than one EDC connectors. Therefore, the connector which provides the reliability asset (usage data asset for reliability related use cases), must be resolved. In addition, the ID of the offered asset is also resolved.

```sparql
  bpnl:BPNL000000000OEM cx-common:hasConnector ?oemEDC .
  ?oemEDC cx-common:offers [ rdfs:isDefinedBy <https://w3id.org/catenax/ontology/reliability ; cx-common:id ?reliabilityAssetId ] .
```

#### RESOLVING VEHICLE, PART OF INTEREST, ITS SUPPLIER AND THE RELATED LOAD DATA

At the OEM's EDC connector, the graph asset of the usage data is requested. Doing so, a sub-skill is transferred to the OEM's Knowledge Agent. At the OEM, the vehicle is resolved by its VIN. Then, the part of interrest (assembly) and its supplier are resolved by the part's name. At the end, the load for that part can be resolved.

```sparql
  SERVICE ?oemEDC {
      GRAPH ?reliabilityAssetId {
        ?vehicle rdf:type cx-vehicle:Vehicle ;
            cx-vehicle:vehicleIdentificationNumber ?vin .

        ?assembly rdf:type cx-vehicle:Part ;
            cx-vehicle:name ?aggregate ;
            cx-vehicle:isPartOf ?vehicle ;
            cx-vehicle:supplier ?supplier .

        ?teleAnalysis rdf:type cx-reliability:Analysis ;
            cx-reliability:analysedObject ?assembly ;
            cx-reliability:operatingHoursOfVehicle ?operatingTime ;
            cx-reliability:mileageOfVehicle ?mileage ;
            cx-core:startDateTime ?recordDate ;
            cx-reliability:result [
                cx-core:id ?ls_type ;
                cx-core:name ?ls_name ;
                cx-reliability:countingValue ?ls_value ;
                cx-reliability:countingUnit ?ls_unit ;
                cx-reliability:countingMethod ?ls_method ;
                cx-reliability:channels ?ls_channels ;
                cx-reliability:classes ?ls_classes ;
                cx-reliability:values ?ls_values
            ] .
    } # OEM#GRAPH
```

#### RESOLVING CALCULATION SERVICE ASSET AT SUPPLIER

At the OEM, the supplier of the part of interest gets resolved, as well as the related asset for the RuL calculation.

```sparql
    ?supplier cx-common:hasConnector ?supplierEDC.
    ?supplierEDC cx-common:offers [ rdfs:isDefinedBy <https://w3id.org/catenax/ontology/behaviour> ; cx-common:id ?prognosisAssetId ] .
```

#### INVOKE CALCULATION SERVICE AT SUPPLIER

At the supplier's EDC connector, the graph asset of the RuL calculation service is requested. Doing so, a sub-skill is transferred to the supplier's Knowledge Agent. At the supplier, the RuL calculation service is called implicit due to its service binding to the knowledge graph. The result then is bound to the knowledge graph.

```sparql
    SERVICE ?supplierEDC {
        GRAPH ?prognosisAssetId {
            ?invocation a cx-behaviour:RemainingUsefulLife ;
                    cx-behaviour:sender bpnl:BPNL00000003AYRE ;
                    cx-behaviour:senderConnector ?oemEDC ;
                    cx-behaviour:recipient ?supplier ;
                    cx-behaviour:recipientConnector ?supplierEDC ;
                    cx-behaviour:targetDate ?recordDate ;
                    cx-behaviour:timeStamp ?recordDate ;
                    cx-behaviour:component "GearBox" ;
                    cx-behaviour:statusDate ?recordDate ;
                    cx-behaviour:statusOperatingHours ?operatingTime ;
                    cx-behaviour:statusMileage ?mileage ;
                    cx-behaviour:countingValue ?ls_value ;
                    cx-behaviour:countingUnit ?ls_unit ;
                    cx-behaviour:countingMethod ?ls_method ;
                    cx-behaviour:headerChannels ?ls_channels ;
                    cx-behaviour:bodyClasses ?ls_classes ;
                    cx-behaviour:bodyCountsList ?ls_values ;
                    cx-behaviour:remainingOperatingHours ?timeHours ;
                    cx-behaviour:remainingRunningDistance ?distanceKm .
        } # SUPPLIER#GRAPH
    } # SUPPLIER#CATALOG

  } # OEM#CATALOG

} # SELECT
```

## SKILL REGISTRATION AND INVOCATION

For skill registration and invocation, have a look at the [general Development View](../../../software-development-view/skill#skill-registration).
