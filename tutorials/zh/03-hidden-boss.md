# 3 · Arizona 进场变大熊，奥莉开强化

[教程目录](../README.md) · [English](../en/03-hidden-boss.md)

大熊在普通训练和本地对战中的替换有用户成功记录。奥莉增强和手动三阶段也做过实测。Fred 收尾等功能有自己的限制，照着开一个 Flag 得不到完整剧情 Boss。

## 教程里先试熊

第一课的普通角色关能进入后，在原 `setMatchSettings` 中，`initTrial` 后加：

```lua
preloadSprite("bscout")
initSetPlayerSprite(Player1, "bscout")
initSetPlayerPalette(Player1, 0)
```

这是从旧成功路径提炼的改动，当前新关卡组合仍要实测。先保留原初始化。熊只用已确认的配色 0；拿普通角色的配色编号套上去会增加变量。

改完重新生成候选、安装、从菜单进一次。选角头像有没有熊，暂时不作为验收条件。检查场上本体和实际操作。

## 普通训练里怎么换

在公开源码 `ui/training-hook.js` 搜 `shouldReplace`。它的判断包含：

```javascript
const offline = fightType === 0 || (fightType === 10 && training === 1);
return options.bear && offline && name === 'cow' && callerRva === '0x1773b84';
```

这段要留在原函数里，依赖的参数和 options 都来自该文件。`cow` 是选中 Arizona 后的待加载名；同一个模块检查已知的调用来源。0 在回放里也可能出现，这段模式规则不足以替你鉴别全部场景。

加载钩子接在本构建 RVA `0x1772f40`。满足规则后会走：

```javascript
assign(p1, bear, 6);
scene.add(0x2368).writeS32(0);
```

这里 `p1` 指向场景里的字符串对象，并非角色本体。`bear` 是长期保存的 `Memory.allocUtf8String('bscout')`；6 是字符串字节数。`assign` 使用已核对的原生字符串赋值函数 `0x8fbb0`，声明可在文件里直接找到。别把这两行独立粘进任意回调。

想练习一个小改动，可以把判断里的 `name === 'cow'` 改成你已确认的另一普通角色加载标识。启动完整 UI，只开大熊选项。原来 Arizona 的替换条件会消失，新入口需要重新测。这是选择触发角色，目标仍为 bscout。

## 强化奥莉的位怎么写

读同一文件的 `applyBoss(scene)`。它在外层重置 `0x1773720` 完成后执行，确认 P1 槽位和队伍，才访问角色 Flag 字段。

```javascript
const field = sprite.add(0x590);
const before = field.readU32();
const after = (before | 0x08000000) >>> 0;
if (before !== after) field.writeU32(after);
```

这是原函数内部摘录。原函数还有模式、角色名和可写范围检查，调用位置也受重置流程约束。保留这些条件。

Flag27 的编号从 0 算，掩码为 `1 << 27`。按位或保留其他位。直接 `writeU32(0x08000000)` 会抹掉同一个字里的其他状态。清位也未必撤销已创建的效果，退出后重启比较稳妥。

## 三阶段从哪儿读起

在 `phase3-controller.js` 看请求和超时；到 `phase3-native.js` 找 `makeStateClosure`、`enqueueState` 和位置同步相关实现。包装签名在已公开代码里，状态查找和对象归属也要一起读。

不要直接把当前状态指针改成 `Flight_N_BG` 的地址。我们的早期版本只让 Book 移动，本体没同步；后面才补上这部分。普通 Fred 还依赖供体角色，天火实验要求 P2 普通奥莉。

Velvet 龙卷风退出仍要求重启，Paprika Flag27 的具体效果不清楚。Baihe Supernova 没有成功移植。先选一个已知入口做实验，查不到完整依赖时保留禁用状态。
