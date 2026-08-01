---
name: appendix-antarctics-noname
description: <summary>图片展示</summary>
---

# 附录C：充能条技能示例

## 1. 效果展示
- 描述完善
- 名称、颜色均可自定义
- 支持UI、标记两种模式
- 支持个别角色关闭
- 支持上限修改、获取方式修改
<details>
<summary>图片展示</summary>

![支持UI显示](Images/enery3.png)
![支持多种颜色](Images/enery4.png)
![支持标记展示](Images/enery5.png)
![描述丰富](Images/enery1.png)
![根据背景变换颜色](Images/enery2.png)

</details>

## 2. 使用示例
举个例子：

想要实现技能效果：```当你受到伤害后，获得5点怒气。你无法通过除此以外的效果获得怒气。```

那就创建一个技能，技能效果为受伤时触发``` player: "damageEnd" ```

初始化```player.zmld```，然后在效果中使用```game.changeNp()```来获取能量即可！

示例：

```javascript
nuqi: {
    trigger: {
        player: "damageEnd"
    },
    forced: true,
    init(player, skill) {
        player.zmld = {
            Skip: ["gameStart", "useCardBegin", "gainBegin", "phaseBeginStart", "damageBegin"], // 跳过 游戏开始时、回合开始时、使用牌时、获得牌时、造成伤害、受到伤害时的能量回复
            Name: "怒气条", // 充能条名称为
            Color: "#DC143C", // 颜色为：猩红色，支持渐变色
            Max: 15, // 充能条上限
            Np: 2, // 充能起始值
        }
    },
    content () {
        "step 0"
        game.changeNp(5) // 获得五点充能，获取历史显示为“因【怒气】：+5”，可以自定义原因
        "step 1"
        if (player.zmld.Np >= player.zmld.Max) {
            game.changeNp(-10, "怒火攻心") // 怒气值不小于上限时，扣除10点充能
            game.changeNp(-5, "怒火焚天", trigger.source) // 扣除攻击者5点能量
        }
    }
}
```
### 图片：
#### 初始能量条：
![能量](./Images/example1.png)
#### 历史记录：
![能量](./Images/example2.png)
#### 对其他人能量条无变化：
![能量](./Images/example3.png)
#### 对其他人能量条修改：
![能量](./Images/example4.png)
#### 支持渐变色：
```javascript
Color: "linear-gradient(90deg, #c01c28 0%, #ff7800 50%, #ffb380 100%, #c01c28 200%)"
```
![能量](./Images/example5.png)


## 3. 技能代码

- 此代码仅提供使用方法注释，对于实现方式不提供注释

```javascript
/* ================================== 充能实现 ==============================
* 问题反馈：Q 1337515813
* 请分别修改：historyLimit、event.style函数。
* 其中，historyLimit为历史记录长度，为0时不显示。
* event.style为能量显示类型，若为1，则以UI形式显示，若为2，则以标记形式显示。
* 若仅需部分角色使用，请为lib.skill._zmld_np添加filter
*
支持参数：
* 修改玩家充能
* @param {Object} player - 修改对象，默认为自身
* @param {number} number - 修改数值，支持正负。
* @param {string} reason - 修改原因，不填则采用事件名。
*
	game.changeNp(): 充能修改
	game.changeMaxNp(): 充能上限修改

数据获取：
player.zmld.Np: 当前充能
player.zmld.Max: 充能最大值
player.zmld.History: 充能历史
player.zmld.Gained: 累计获得
player.zmld.Lost: 累计失去
数据修改：
player.zmld.Name: 充能名称
player.zmld.Color: 充能颜色
player.zmld.Enable: 是否启用
player.zmld.Image: 标记显示下，采用图片展示能量。

* 角色充能跳过规则
* 用于声明当前角色跳过的充能事件集合，支持两种配置方式：
*
* 1. 函数式条件 (Function)
*    - 命名规则：函数名必须与目标事件名称严格一致（如'useCardBegin'对应同名事件）
*    - 返回值：返回 true 时跳过充能，false 则正常执行
*    - 示例：检测到使用筹码卡时跳过充能
*      player.zmld.Skip.push(function useCardBegin() {
*          return this.cards.some(c => c.gaintag.includes('zm_chouma'))
*      })
*    // 对应事件自动传参，使用this调用。
* 2. 字符串直接匹配 (String)
*    - 完全匹配事件名称时强制跳过
*    - 示例：无条件跳过'gameStart'和技能'wusheng'事件
*      player.zmld.Skip.push(['gameStart',"wusheng"])
*   可用事件： gameStart、phaseBeginStart、useCardBegin、damageBegin、gainBegin
*
* 示例：
* init(player){
* player.zmld = {
*   Skip : [
*       "wusheng",
*       "gameStart",
*       "gainBegin",
*       function useCardBegin(){
*       if(this.card.name =="sha") return true
*       if(this.cards.some(card=> card.gaintag.includes("dc_shangyu"))) return true
*       return false
*       }]
*   }
* }
* // 效果：游戏开始、获得牌时、使用技能武圣时、使用“杀”时、使用“赏誉”牌时，无法获得能量。
*
player.zmld.Skip:[]
*/
game.NpContent = function (player) {
	if (player == undefined) player = _status.event.player;
	let historyHtml = '';
	let historyLimit = lib.config?.extension_综漫乱斗_zmld_np_history || 10;
	if (historyLimit > 0) {
		let history = player.zmld?.History || [];
		if (history.length > 0) {
			historyHtml = '<div style="white-space:nowrap;">最近变化：</div>' +
				history.slice(0, historyLimit).map(record => {
					let color = record.change > 0 ? (lib.config.menu_style == "wood" ? "#1E8449" : "#33d17a") : (lib.config.menu_style == "wood" ? "#CC0000" : "#ff6b6b");
					let sign = record.change > 0 ? '+' : '';
					return `<div style="font-size:0.8em; color:${color}; white-space:nowrap;">• ${record.reason}: ${sign}${record.change}</div>`;
				}).join('');
		}
	}

	const totalGained = player.zmld?.Gained || 0;
	const totalLost = player.zmld?.Lost || 0;

	return `
					<div style="white-space:nowrap;">当前充能：<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">${player.zmld?.Np}/${player.zmld?.Max}</span></div>
				<div style="white-space:nowrap;">累计获得：<span style="color:${lib.config.menu_style == "wood" ? "#1E8449" : "#33d17a"}">${totalGained}</span></div>
				<div style="white-space:nowrap;">累计失去：<span style="color:${lib.config.menu_style == "wood" ? "#CC0000" : "#ff6b6b"}">${totalLost}</span></div>
				${historyHtml}
				<div style="white-space:nowrap;">获取方式：</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">游戏开始</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">15</span>点能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">回合开始</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">5</span>点能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">使用牌</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">1</span>点能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">获得牌</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">等量</span>能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">造成伤害</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">等量</span>能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• <span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">受到伤害</span>时获得<span style="color:${lib.config.menu_style == "wood" ? "#3366FF" : "#66CCFF"}">等量</span>能量</div>
				<div style="font-size:0.9em;white-space:nowrap;">• 部分<span style="color:${lib.config.menu_style == "wood" ? "#CC6600" : "#ff7800"}">角色技能</span>可获取能量</div>
				`;
}

game.changeNp = function () {
	for (var i = 0; i < arguments.length; i++) {
		if (typeof arguments[i] === 'number') var change = arguments[i];
		else if (typeof arguments[i] === "string") var reason = arguments[i];
		else if (typeof arguments[i] === "object") var player = arguments[i];
	}
	if (player == undefined) player = _status.event.player;
	if (!change) return false;
	if (player.zmld?.Skip.length > 0) {
		let match = player.zmld?.Skip.find((func) =>
			(typeof func == 'function' ? func.name : func) == (_status.event.getParent(1).skill == "_zmld_np" ? _status.event.getParent(1).triggername : _status.event.getParent(1).skill)
		)
		if (typeof match == 'function') {
			if (match.call(_status.event.getParent(3))) {
				get.event().trigger('np_change');
				return false
			}
		}
		else if (typeof match == 'string') {
			get.event().trigger('np_change');
			return false
		};
	}
	const currentNp = player.zmld.Np || 0;
	const maxNp = player.zmld.Max || 100;
	const newNp = currentNp + change;

	if (currentNp >= maxNp && change > 0) return false;

	if (!reason) {
		let eventName = get.translation(_status.event.name || '未知来源');
		reason = `因【${eventName}】`;
	}

	game.broadcastAll(function (player, change, reason, newNp) {
		if (!player.zmld.Gained) player.zmld.Gained = 0;
		if (!player.zmld.Lost) player.zmld.Lost = 0;
		if (!player.zmld.History) player.zmld.History = [];

		if (change > 0) {
			const actualGain = Math.min(change, player.zmld.Max - player.zmld.Np);
			player.zmld.Gained += actualGain;
		} else {
			player.zmld.Lost += Math.abs(change);
		}

		player.zmld.Np = Math.max(0, Math.min(newNp, player.zmld.Max));

		player.zmld.History.unshift({
			change: change,
			reason: reason
		});
		if (player.zmld.History.length > 10) {
			player.zmld.History.pop();
		}

		get.event().trigger('np_change');
	}, player, change, reason, newNp);
	return true
}

game.changeMaxNp = function () {
	for (var i = 0; i < arguments.length; i++) {
		if (typeof arguments[i] === 'number') var change = arguments[i];
		else if (typeof arguments[i] === "string") var reason = arguments[i];
		else if (typeof arguments[i] === "object") var player = arguments[i];
	}
	if (player == undefined) player = _status.event.player;
	if (!change) return false;
	if (change < 0) change = 0;
	if (change === player.zmld.Max) return false;

	if (!reason) {
		let eventName = get.translation(_status.event.name || '未知来源');
		reason = eventName.includes('【') ? eventName : `因【${eventName}】`;
	}

	game.broadcastAll(function (player, change, reason) {
		let oldMax = player.zmld.Max || 100;
		player.zmld.Max = change;
		if (player.zmld.Np >= player.zmld.Max) {
			player.zmld.Np = player.zmld.Max;
		}

		if (!player.zmld.History) {
			player.zmld.History = [];
		}

		let diff = change - oldMax;
		if (diff !== 0) {
			player.zmld.History.unshift({
				change: diff,
				reason: `${reason}上限${diff > 0 ? '增加' : '减少'}`
			});
			if (player.zmld.History.length > 10) {
				player.zmld.History.pop();
			}
		}

		get.event().trigger('np_change');
	}, player, change, reason);
	return true
}

lib.skill._zmld_np = {
	trigger: {
		global: ["gameStart"],
		player: ["phaseBeginStart", "useCardBegin", "damageBegin", "gainBegin", "np_change"],
		source: "damageBegin"
	},
	marktext: "Np",
	intro: {
		name: `
							<div style="text-align:center">
							<div style="font-size:1.2em">${_status.event.player?.zmld.Name || "能量条"}</div>
							<div style="font-size:0.7em; white-space:nowrap; color:${lib.config.menu_style == "wood" ? "888" : "#aaa"}">用于《综漫乱斗》扩展</div>
							</div>
						`,
		markcount (storage, player) {
			return player.zmld.Np;
		},
		content (storage, player) {
			return game.NpContent();
		},
		...{ ..._status.event.player?.zmld.Image ? { markimage: player.zmld.Image } : {} },
	},
	lastDo: true,
	forced: true,
	popup: false,
	silent: true,
	fixed: true,
	superCharlotte: true,
	create(player) {
		game.broadcastAll(function (player) {
			let double = player.classList.contains('fullskin2') && lib.config.layout !== 'long2';
			const width = player.node.avatar.clientWidth;
			let w = width * (double ? 2 : 1);
			const bar = ui.create.div();
			bar.className = 'energy-bar';

			const isMobile = lib.device == 'android' || lib.device == 'ios';
			const heightMultiplier = isMobile ? 0.15 : 0.1;
			const topOffset = lib.config.extension_综漫乱斗_zmld_ui_top != 0 ? lib.config.extension_综漫乱斗_zmld_ui_top : isMobile ? 0.2 : 0.15;

			bar.style.cssText = `
								z-index: 3;
								width: ${w * 1.05}px;
								height: ${w * heightMultiplier}px;
								position: absolute;
								top: ${w * -topOffset}px;
								border: 2px solid rgba(0, 0, 0, 0.9);
								border-radius: ${w * 0.05}px;
								background: rgba(0, 0, 0, 0.6);
								overflow: hidden;
								box-sizing: border-box;
								box-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
							`;
			bar.setNodeIntro(
				`
								<div style="text-align:center">
								<div style="font-size:1.2em">${player.zmld.Name}</div>
								<div style="font-size:0.7em; white-space:nowrap; color:${lib.config.menu_style == "wood" ? "888" : "#aaa"}">用于《综漫乱斗》扩展</div>
								</div>
								`,
				game.NpContent(player)
			);
			const fill = ui.create.div();
			fill.className = 'energy-fill';
			fill.style.cssText = `
								width: 0%;
								height: 100%;
								position: absolute;
								left: 0;
								top: 0;
								transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
								opacity: 1;
								background-size: 200% 100%;
							`;
			const label = ui.create.div();
			label.className = 'energy-label';
			label.style.cssText = `
								position: absolute;
								width: 100%;
								height: 100%;
								display: flex;
								align-items: center;
								justify-content: center;
								color: #ffffff;
								font-size: ${w * 0.08}px;
								font-weight: bold;
								text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
								z-index: 1;
							`;
			bar.appendChild(fill);
			bar.appendChild(label);
			player.appendChild(bar);
		}, player);
	},
	content () {
		'step 0'
		event.style = lib.config?.extension_综漫乱斗_zmld_np || 1
		if (event.triggername == 'gameStart') {
			game.broadcastAll(function (player) {
				player.zmld = {
					Np: player.zmld?.Np || 0,
					Max: player.zmld?.Max || 100,
					History: player.zmld?.History || null,
					Gained: player.zmld?.Gained || null,
					Lost: player.zmld?.Lost || null,
					Enable: player.zmld?.Enable ?? true,
					Skip: player.zmld?.Skip || [],
					Name: player.zmld?.Name || "能量条",
					Color: player.zmld?.Color || null
				}
			}, player);
			if (!player.zmld.Enable) return;
			if (!player.hasSkill('subplayer')) {
				if (event.style == '1') {
					lib.skill._zmld_np.create(player)
				}
				else if (event.style == '2') {
					player.updateMark("_zmld_np");
					player.markSkill("_zmld_np");
				}
			}
		}
		'step 1'
		if (event.triggername != 'np_change') {
			let change = 0;
			let reason = '';
			if (trigger && trigger.skill) {
				let skillName = get.translation(trigger.skill);
				skillName = skillName.includes('【') ? skillName : `【${skillName}】`;
				reason = `因${skillName}`;
			}
			else if (event.triggername == "gainBegin") {
				change = trigger.cards.length;
				let source = trigger.source || '系统';
				if (typeof source === 'object' && source.name) {
					source = get.translation(source.name);
				}
				reason += source === '系统' ? '获得牌' : `从${source}获得牌`;
			}
			else if (event.triggername == "phaseBeginStart") {
				change = 5;
				reason += '回合开始';
			}
			else if (event.triggername == "damageBegin") {
				change = trigger.num;
				if (player == trigger.source) {
					let target = trigger.player;
					reason += `对${get.translation(target.name)}造成伤害`;
				} else {
					let source = trigger.source;
					reason += source ? `受到${get.translation(source.name)}的伤害` : '受到伤害';
				}
			}
			else if (event.triggername == "useCardBegin") {
				change = 1;
				let cardName = get.translation(trigger.card.name);
				reason += `使用【${cardName}】`;
			}
			else if (event.triggername == "gameStart") {
				change = 15;
				reason += '游戏开始';
			}

			game.changeNp(player, change, reason);
			event.finish();
		} else {
			game.broadcastAll(function (player) {
				if (event.style == '1') {
					if (!player.zmld.Enable) {
						player.querySelector('.energy-bar')?.delete()
						return
					};
					if (!player.querySelector('.energy-bar')) {
						player.unmarkSkill("_zmld_np")
						lib.skill._zmld_np.create(player)
					}
					let energy = player.zmld.Np || 0;
					let maxEnergy = player.zmld.Max || 100;
					const bar = player.querySelector('.energy-bar');
					if (!bar) return;
					const fill = bar.querySelector('.energy-fill');
					const label = bar.querySelector('.energy-label');
					if (fill && label) {
						let percentage = (energy / maxEnergy) * 100;
						fill.style.width = `${percentage >= 0 ? percentage : 0}%`;
						const gradient = player.zmld?.Color || `${percentage <= 25 ?
							'linear-gradient(90deg, #1a5fb4 0%, #3584e4 50%, #62a0ea 100%, #1a5fb4 200%)' :
							percentage <= 50 ?
								'linear-gradient(90deg, #26a269 0%, #33d17a 50%, #8ff0a4 100%, #26a269 200%)' :
								percentage <= 75 ?
									'linear-gradient(90deg, #e66100 0%, #ffa348 50%, #ffbe6f 100%, #e66100 200%)' :
									'linear-gradient(90deg, #c01c28 0%, #ff7800 50%, #ffb380 100%, #c01c28 200%)'}`;
						fill.style.background = gradient;
						fill.style.boxShadow = `0 0 15px ${percentage <= 25 ? '#3584e4cc' :
							percentage <= 50 ? '#33d17acc' :
								percentage <= 75 ? '#ffa348cc' :
									'${lib.config.menu_style == "wood" ?  "#CC6600":"#ff7800"}cc'
							}`;
						label.innerHTML = `${Math.round(energy)}/${maxEnergy}`;
						label.style.textShadow = `0 0 8px ${percentage <= 25 ? '#3584e4' :
							percentage <= 50 ? '#33d17a' :
								percentage <= 75 ? '#ffa348' :
									'${lib.config.menu_style == "wood" ?  "#CC6600":"#ff7800"}'
							}`;

						bar.nodeContent = game.NpContent(player);
					}
				}
				else if (event.style == '2') {
					if (!player.zmld.Enable) {
						player.unmarkSkill("_zmld_np")
						return
					};
					if (player.querySelector('.energy-bar')) {
						player.querySelector('.energy-bar')?.delete()
					}
					player.updateMark("_zmld_np");
				}
			}, player);
		}
	}
}
```
