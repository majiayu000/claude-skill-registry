---
name: jsdoc
description: '関連クラス: WindowSkillList, WindowSkillStatus <br />'
---

# Class: Scene_Skill

## Extends: [Scene_ItemBase](Scene_ItemBase.md)

### new Scene_Skill ()

[スキル]のシーン。

関連クラス: [Window_SkillList](Window_SkillList.md), [Window_SkillStatus](Window_SkillStatus.md) <br />
関連シーン: [Scene_Menu](Scene_Menu.md)

### Properties:

| Name               | Type                                    | Description                |
| ------------------ | --------------------------------------- | -------------------------- |
| `_skillTypeWindow` | [Window_SkillType](Window_SkillType.md) | スキルタイプ選択ウィンドウ |

### Inherited From

#### [PIXI.DisplayObject](PIXI.DisplayObject.md)

- [(static) mixin (source)](PIXI.DisplayObject.md#static-mixin-source)
- [\_recursivePostUpdateTransform ()](PIXI.DisplayObject.md#_recursivepostupdatetransform-)
- [displayObjectUpdateTransform ()](PIXI.DisplayObject.md#displayobjectupdatetransform-)
- [getBounds (skipUpdate, rect)](PIXI.DisplayObject.md#getbounds-skipupdate-rect--pixirectangle)
- [getGlobalPosition (point, skipUpdate)](PIXI.DisplayObject.md#getglobalposition-point-skipupdate--pixipoint)
- [setParent (container)](PIXI.DisplayObject.md#setparent-container--pixicontainer)
- [setTransform (x, y, scaleX, scaleY, rotation, skewX, skewY, pivotX, pivotY)](PIXI.DisplayObject.md#settransform-x-y-scalex-scaley-rotation-skewx-skewy-pivotx-pivoty--pixidisplayobject)
- [toGlobal (position, point, skipUpdate)](PIXI.DisplayObject.md#toglobal-position-point-skipupdate--pixipoint)
- [toLocal (position, from, point, skipUpdate)](PIXI.DisplayObject.md#tolocal-position-from-point-skipupdate--pixipoint)

#### [PIXI.Container](PIXI.Container.md)

- [addChild (child) ](PIXI.Container.md#addchild-child--pixidisplayobject)
- [addChildAt (child, index)](PIXI.Container.md#addchildat-child-index--pixidisplayobject)
- [calculateBounds ()](PIXI.Container.md#calculatebounds-)
- [destroy ()](PIXI.Container.md#destroy-)
- [getChildAt (index)](PIXI.Container.md#getchildat-index--pixidisplayobject)
- [getChildByName (name)](PIXI.Container.md#getchildbyname-name--pixidisplayobject)
- [getChildIndex (child)](PIXI.Container.md#getchildindex-child--pixidisplayobject)
- [onChildrenChange ()](PIXI.Container.md#onchildrenchange-)
- [removeChild (child)](PIXI.Container.md#removechild-child--pixidisplayobject)
- [removeChildAt (index)](PIXI.Container.md#removechildat-index--pixidisplayobject)
- [removeChildren (beginIndex, endIndex)](PIXI.Container.md#removechildren-beginindex-endindex--arraypixidisplayobject)
- [render (renderer)](PIXI.Container.md#render-renderer)
- [renderAdvanced (renderer)](PIXI.Container.md#renderadvanced-renderer)
- [renderCanvas (renderer)](PIXI.Container.md#rendercanvas-renderer)
- [setChildIndex (child, index)](PIXI.Container.md#setchildindex-child-index)
- [sortChildren ()](PIXI.Container.md#sortchildren-)
- [swapChildren (child, child2)](PIXI.Container.md#swapchildren-child-child2)
- [updateTransform ()](PIXI.Container.md#updatetransform-)

#### [Scene_Base](Scene_Base.md)

- [addWindow (Window)](Scene_Base.md#addwindow-window)
- [attachReservation ()](Scene_Base.md#attachreservation-)
- [checkGameover ()](Scene_Base.md#checkgameover-)
- [createFadeSprite ()](Scene_Base.md#createfadesprite-)
- [createWindowLayer ()](Scene_Base.md#createwindowlayer-)
- [detachReservation ()](Scene_Base.md#detachreservation-)
- [fadeOutAll ()](Scene_Base.md#fadeoutall-)
- [fadeSpeed ()](Scene_Base.md#fadespeed---number)
- [isActive () ](Scene_Base.md#isactive---boolean)
- [isBusy ()](Scene_Base.md#isbusy---boolean)
- [isReady ()](Scene_Base.md#isready---boolean)
- [popScene ()](Scene_Base.md#popscene-)
- [slowFadeSpeed ()](Scene_Base.md#slowfadespeed---number)
- [startFadeIn (duration opt, white opt)](Scene_Base.md#startfadein-duration-opt-white-opt)
- [startFadeOut (duration opt, white opt)](Scene_Base.md#startfadeout-duration-opt-white-opt)
- [stop ()](Scene_Base.md#stop-)
- [terminate ()](Scene_Base.md#terminate-)
- [update ()](Scene_Base.md#update-)
- [updateChildren ()](Scene_Base.md#updatechildren-)
- [updateFade ()](Scene_Base.md#updatefade-)

#### [Scene_MenuBase](Scene_MenuBase.md)

- [actor ()](Scene_MenuBase.md#actor---game_actor)
- [createHelpWindow ()](Scene_MenuBase.md#createhelpwindow-)
- [nextActor ()](Scene_MenuBase.md#nextactor-)
- [previousActor ()](Scene_MenuBase.md#previousactor-)
- [setBackgroundOpacity (opacity)](Scene_MenuBase.md#setbackgroundopacity-opacity)
- [updateActor ()](Scene_MenuBase.md#updateactor-)

#### [Scene_ItemBase](Scene_ItemBase.md)

- [activateItemWindow ()](Scene_ItemBase.md#activateitemwindow-)
- [applyItem ()](Scene_ItemBase.md#applyitem-)
- [canUse ()](Scene_ItemBase.md#canuse---boolean)
- [checkCommonEvent ()](Scene_ItemBase.md#checkcommonevent-)
- [createActorWindow ()](Scene_ItemBase.md#createactorwindow-)
- [create ()](Scene_ItemBase.md#create-)
- [determineItem ()](Scene_ItemBase.md#determineitem-)
- [hideSubWindow (window)](Scene_ItemBase.md#hidesubwindow-window)
- [isCursorLeft ()](Scene_ItemBase.md#iscursorleft---boolean)
- [isItemEffectsValid ()](Scene_ItemBase.md#isitemeffectsvalid---boolean)
- [item ()](Scene_ItemBase.md#item---rpgbusableitem)
- [itemTargetActors ()](Scene_ItemBase.md#itemtargetactors---game_actor)
- [onActorCancel ()](Scene_ItemBase.md#onactorcancel-)
- [onActorOk ()](Scene_ItemBase.md#onactorok-)
- [showSubWindow (window)](Scene_ItemBase.md#showsubwindow-window)

### Methods

#### commandSkill ()

スキル選択を開始。

#### create ()

Overrides: [Scene_ItemBase](Scene_ItemBase.md#create-)

#### createItemWindow ()

スキル項目のウィンドウを生成。

#### createSkillTypeWindow ()

スキルタイプのウィンドウを生成。

#### createStatusWindow ()

ステータスウィンドウを生成。

#### initialize ()

Overrides: [Scene_ItemBase](Scene_ItemBase.md#initialize-)

#### onActorChange ()

Overrides: [Scene_MenuBase](Scene_MenuBase.md#onactorchange-)

#### onItemCancel ()

スキル項目をキャンセルした時に呼ばれるハンドラ。

#### onItemOk ()

スキル項目を決定した時に呼ばれるハンドラ。

#### playSeForItem ()

[スキル使用]に設定された音を再生。

#### refreshActor ()

アクターの再描画。

#### start ()

Overrides: [Scene_Base](Scene_Base.md#start-)

#### useItem ()

Overrides: [Scene_ItemBase](Scene_ItemBase.md#useitem-)

#### user () → {[Game_Actor](Game_Actor.md)}

Overrides: [Scene_ItemBase](Scene_ItemBase.md#user---gameactor)
