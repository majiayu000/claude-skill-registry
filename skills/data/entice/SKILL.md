---
name: entice
description: Enables you to use skills and the skillbar and such.
---

## Topic `skill`

Enables you to use skills and the skillbar and such.

_Note: Skills in the skillbar can have the id 0 to identify
empty skillbar slots._

---

Asynchroneous initial message after successful join

```
initial
- unlocked_skills // overall available skills
- skillbar        // your current skillbar as list of skill-ids
```

---

Synchroneous client requests.

Setting a skillbar slot:

```
skillbar:set
- slot            // the slot index of the skillbar (0-based, i.e. has to be between 0-7)
- id              // the id of the skill to be placed there, or 0 for deletion
```

Success:

```
skillbar:ok
- skillbar        // your current skillbar as list of skill-ids
```

Failure: (No permission to change skillbar)

```
skillbar:error
- reason          // the reason why the server couldn't perform the skillbar-change
```

Casting a skill:

```
cast
- slot            // the slot index on the skillbar that you want to cast
- target          // the entity-id of the target - if this is invalid or not set, it defaults
                  // to your own entitys id
```

Success:

```
cast:ok
```

Failure: (Already casting a skill, or still recharging)

```
cast:error
- slot            // the index of the skillbar-slot that you tried to use
- reason          // the reason why the cast could not be performed
```

---

Asynchroneous server events.

Skill-Casting & skill-recharging:
You will be notified when a player starts casting a skill and also when the casting was
successful. After a cast, the skill might need to recharge. In this case the
recharge time will be more than 0 and you will also be notified that a recharge has ended.
If the recharge time of a skill is 0, there will be no notification that the recharge has ended (it never took place).

Notification that an entity starts to cast a skill:
(This might is not sent if the casting is instantaneous)

```
cast:start        // -> Start of the casting process, if cast-time is not 0
- entity          // entity id of the caster
- target          // entity id of the target (defaults to caster entity id if no target given)
- slot            // the index of the skillbar-slot that the player used
- skill           // the id of the skill the player used
- cast_time       // the actual cast-time in milliseconds
```

```
cast:end          // -> End of the casting process, if cast-time is not 0
- entity          // entity id of the caster
- target          // entity id of the target (defaults to caster entity id if no target given)
- slot            // the index of the skillbar-slot that the player used
- skill           // the id of the skill the player used
- recharge_time   // the actual recharge-time in milliseconds
```

Skill casting failures:
(Note that in a future release some of these failures might also be handled already during
the start of the casting process, for example range checks and parameter checks)

```
cast:interrupt
- entity          // entity id of the caster
- target          // entity id of the target (defaults to caster entity id if no target given)
- slot            // the index of the skillbar-slot that the player used
- skill           // the id of the skill the player used
- recharge_time   // the actual recharge-time in milliseconds
- reason          // why the skill casting could not be performed
```

Skill recharge events:

```
recharge:end      // -> End of the recharge process, if recharge-time is not 0
- entity          // entity id of the caster
- slot            // the index of the skillbar-slot that the player used
- skill           // the id of the skill the player used
```

After-cast delay end events:

```
after_cast:end    // -> End of the after-cast delay
- entity          // entity id of the caster
```

---
