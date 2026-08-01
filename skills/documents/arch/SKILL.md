---
name: arch
description: ActiveSkill < Skill
---

ActiveSkill < [Skill](https://github.com/SubwayRocketTeam/game/blob/master/doc/arch/Skill.md)
====

* Unit이 사용할 수 있는 스킬

ActiveSkill이 가지는 프로퍼티
----
* 스킬의 사용 기간 : Player의 경직 시간
* 이동 속도 비율 : 스킬 사용 기간동안 speed에 곱해질 값
* 쿨타임
* MP 코스트

ActiveSkill이 할 수 있는 액션
----
* 스킬의 사용

추가 기재
----
* Unit은 경직, 쿨타임, MP코스트의 영향을 받지 않는다.
* 위의 속성들은 Player에게만 적용됨
* 이동 속도 비율이 0일 경우, 시전 기간 동안 이동 불가 스킬
* 이동 속도 비율이 1일 경우, 시전 중에도 원래의 이동 속도로 이동할 수 있다.
