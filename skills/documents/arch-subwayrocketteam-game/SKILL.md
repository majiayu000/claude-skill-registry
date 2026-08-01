---
name: arch-subwayrocketteam-game
description: PassiveSkill < Skill
---

PassiveSkill < [Skill](https://github.com/SubwayRocketTeam/game/blob/master/doc/arch/Skill.md)
====

* 보유하고 있으면 특정한 효과를 주는 스킬

PassiveSkill이 가지는 프로퍼티
----
* mp, attack 등의 Attribute에 적용될 보너스 수치 리스트

PassiveSkill이 할 수 있는 액션
----
* 일정 시간 마다 작업 (periodic work)

추가 기재
----
* 보유하고 있다가 보유하지 않게 될 수도 있다 : 버프
* 마이너스 효과도 가능 : 디버프
