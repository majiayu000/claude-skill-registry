# Coreseek使用技巧

### 1. 结果集过滤
* SetIDRange （设置查询ID范围）
原型： function SetIDRange($min, $max)
设置接受的文档ID范围。参数必须是整数。默认是0和0，意思是不限制范围。
此调用执行后，只有ID在$min和$max（包括$min和$max）之间的文档会被匹配。

* SetFilter （设置属性过滤）
原型： function SetFilter ( $attribute, $values, $exclude=false )
增加整数值过滤器。
此调用在已有的过滤器列表中添加新的过滤器。$attribute是属性名。$values是整数数组。$exclude是布尔值，它控制是接受匹配的文档（默认模式，即$exclude为false时）还是拒绝它们。
只有当索引中$attribute列的值与$values中的任一值匹配时文档才会被匹配（或者拒绝，如果$exclude值为true）

* SetFilterRange （设置属性范围）
原型： function SetFilterRange ( $attribute, $min, $max, $exclude=false )
添加新的整数范围过滤器。
此调用在已有的过滤器列表中添加新的过滤器。$attribute是属性名,$min、$max定义了一个整数闭区间，$exclude布尔值，它控制是接受匹配的文档（默认模式，即$exclude为false时）还是拒绝它们。
只有当索引中$attribute列的值落在$min 和 $max之间（包括$min 和 $max），文档才会被匹配（或者拒绝，如果$exclude值为true）。

* SetFilterFloatRange （设置浮点数范围）
原型： function SetFilterFloatRange ( $attribute, $min, $max, $exclude=false )
增加新的浮点数范围过滤器。
此调用在已有的过滤器列表中添加新的过滤器。$attribute是属性名,$min,$max定义了一个浮点数闭区间，$exclude必须是布尔值，它控制是接受匹配的文档（默认模式，即$exclude为false时）还是拒绝它们。
只有当索引中$attribute列的值落在$min 和 $max之间（包括$min 和 $max），文档才会被匹配（或者拒绝，如果$exclude值为true）。

### 2. 匹配技巧

Sphinx默认搜索一个关键词，默认会匹配所有索引中的字段。

* 关键词与或运算
```
(@name "花千骨")|(@alias "花千骨") 查询表达是用"|"组合表达或
@(name,alias) "花千骨" 与上等同
@name "花千骨" @actor "赵丽颖" 查询表达式空格表达与
```
* 关键词非运算
@name "花千骨" -"赵丽颖" 搜索包含花千骨，不包含赵丽颖的记录
@name "红高粱" @channel -("电视剧") 搜索非电视剧频道的红高粱, name和channel字段可以为逗号表达式的值
@body python -(php|perl) body字段必须含有词“python”，但既没有“php”也没有“perl”

* 全字段匹配
@* "花千骨" 任何字段出现花千骨都匹配

* 关键词严格匹配
```
@name "花千骨"~0 名称严格匹配"花千骨"三个字，只有这三个字都是出现的记录才会命中，等同SQL：name like '%花千骨%'
@name ="花千骨" 同上
```

* 关键词绝对匹配
```
@name "^花千骨$"~0 只匹配名称是"花千骨"三个字的记录，等同SQL：name = '花千骨'
```

* 关键词宽泛匹配
```
@name "花千骨传奇"/4 不考虑顺序，任意匹配"花千骨传奇"中四个字即可
```

* 严格有序搜索符（即"在前"搜索符）
```
@name '花' << '千' << '骨' name列出现'花','千','骨'三个字且要保持顺序，"花朵千万个骨朵"可命中，'千万个花骨朵'不可命中
```

