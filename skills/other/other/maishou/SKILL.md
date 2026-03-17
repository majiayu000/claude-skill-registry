---
name: maishou
description: 商品价格全网对比技能，获取商品在淘宝(Taobao)、天猫(TMall)、京东(JD.com)、拼多多(PinDuoDuo)、抖音(Douyin)、快手(KaiShou)的最优价格、优惠券，当用户想购物或者获取优惠信息时使用。Get the best price, coupons for goods on Chinese e-commerce platforms, compare product prices, and use when users want to shop or get discount information.
---

# 买手技能
全网比价，获取中国在线购物平台商品价格、优惠券

```yaml
# 参数解释
source:
  0: 全部
  1: 淘宝/天猫
  2: 京东
  3: 拼多多
  4: 苏宁
  5: 唯品会
  6: 考拉
  7: 抖音
  8: 快手
  10: 1688
```

## 搜索商品
```shell
uv run scripts/main.py search --source=0 --keyword='{keyword}'
uv run scripts/main.py search --source=0 --keyword='{keyword}' --page=2
```

## 商品详情及购买链接
```shell
uv run scripts/main.py detail --source={source} --id={goodsId}
```
