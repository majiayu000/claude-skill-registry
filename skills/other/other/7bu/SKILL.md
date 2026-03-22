---
name: 7bu
description: 去不图床(7bu.top)图片上传工具。需要TOKEN才能使用，需前往https://7bu.top注册用户。
---

# 7bu 图床上传工具

去不图床(7bu.top)图片上传。

## ⚠️ 需要 TOKEN

请前往 https://7bu.top 注册用户获取 Token。

## 支持格式
JPEG, JPG, PNG, GIF, BMP, ICO, WEBP

## 上传命令
```bash
curl --location 'https://7bu.top/api/v1/upload' \
--header 'Authorization: Bearer TOKEN' \
--form 'file=@IMAGE'
```

## 触发方式
```
使用7bu技能上传图片：图片路径/URL，TOKEN
```

## 使用示例
```
上传 ~/images/photo.jpg 到7bu图床，TOKEN为xxx
```
