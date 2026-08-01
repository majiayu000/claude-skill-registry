---
name: 9-4008-delskill
description: '|:----    |:-------    |:--- |---|------      |'
---

### 删除技能
`delskill`

|参数|类型|空|默认|注释|
|:----    |:-------    |:--- |---|------      |
|play     |`object`    |否   |    |   玩家对象 |
|skillid | `integer`    |否   |    |   技能ID  |

```lua
function main(self)
    local lv = getskillinfo(self,11,1)
    if lv and lv &gt;0 then
        delskill(self, 11)
        say(self,"删除雷电术")
    else
        addskill(self, 11, 3)
        say(self,"获得雷电术")
    end
end
```

