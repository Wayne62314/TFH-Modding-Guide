# 4 · 读取人物和对局属性

[教程目录](../README.md) · [English](../en/04-properties.md)

这一课分教程内 Lua 和外部运行时两条路径。Lua 例子放回自己的关卡。外部例子用训练观察器，先只读。

## 在关卡里回血，改能量

进入初始化后的 routine，重新取得 P1：

```lua
local p1 = getP1()
print("HP=" .. tostring(p1.Lifebar))
print("max HP=" .. tostring(p1:maxLife()))
p1:fullHeal()
p1:setSuperLevel(1)
p1:giveMaxMagic()
```

这些包装可在本构建 `Trials/Lib/LuaLib.lua` 核对。`setSuperLevel` 使用每格能量的内部单位，源码没有替你做完整边界限制。上例设一格，先确认角色上限。`setMagicLevel` 也有同类问题，角色机制不同不要乱给常数。

要做“血量变成最大血量的一半”，可以在同一个位置试：

```lua
local maxHp = p1:maxLife()
p1.Lifebar = math.max(1, math.floor(maxHp * 0.5))
```

训练模式可能自动回血，先检查 `OptLifeBar`。红血、显示血条和死亡流程未必只依赖这个字段；这行适合验证当前生命值，别直接叫它完整生命系统修改。`lifebar` 和 `Lifebar` 在旧代码里都有出现，先沿本构建包装使用的 `Lifebar` 写法，别自行概括所有属性大小写规则。

移动也有包装：教程里能找到 `trialSetupDistance` 和 `spriteSnapPosition`。飞行时本体、Book 和缓存位置需要同步，直接写 x/y 可能只动一部分。

## 外部先运行只读观察器

在 `TFH-Modding-Guide` 目录运行。需要第一课旁边的 TFHMOD 虚拟环境：

```powershell
Get-Process -Name "Them's Fightin' Herds" | Select-Object Id,ProcessName
..\TFHMOD\.venv\Scripts\python.exe examples/observe_training.py --pid 1234
```

把 1234 换成自己的 PID。先进入普通自由训练；角色自选，其他工具关闭。观察器只接受 mode 10、已观察的训练标志及 phase 7。回到终端按 Enter 断开。

这份新观察器还没有游戏内验收。它沿用已调查过的字段和函数签名。每隔 30 个计数尝试输出一次，通过根更新前后恰好推进 1 的检查才发送。它不会替换输入，也不调用游戏的修改性函数。

输出里的 `p1`、`p2` 会有角色名、动作名、位置、朝向、HP，以及原始能量和魔力。`counter` 对应更新入口前的编号。日志没有连续每帧，不要直接拿去当训练数据。

## 字段到底怎么读

在 [observe_training.js](../../examples/observe_training.js) 的 `fighter()` 看实际代码。定位顺序是主 scene → 当前槽位 → actor → data/state。

```javascript
const slot = scene.add(0xaa8).readS32();
const actor = scene.add(0xae0 + slot * 8).readPointer();
const hp = actor.add(0x120).readFloat();
const x = actor.add(0xc78).readS32();
```

这是省去检查的讲解摘录；完整文件先检查槽位范围和队伍。0xaa8 对应 P1 槽，P2 用 0xab4。不要把池子里的第一个对象认成 P1。

| 字段 | 类型和读法 | 注意 |
|---|---|---|
| actor+0xfc | float，朝向，观察值为 ±1 | 换边后读取当前值 |
| actor+0x120 | float，HP | 生命下降本身不能判定哪招命中 |
| actor+0x128 / 12c / 130 | float，super / max / per-level | 每格单位要读出来 |
| actor+0x134 / 138 / 13c | float，magic / max / per-level | 各角色上限不同 |
| actor+0xc78 / c7c | s32，观察到的 x/y | 还有其他同步位置 |
| actor+0xc50 → data+0xb40 | 指针后读字符串 | 数据名可能为 Uni，加载名却为 uni |
| actor+0xc58 → state+0x10 | 指针后读字符串 | 当前动作名不等于可取消窗口 |
| actor+0x1270 | u64 | 身份代数的一部分 |

想用外部钩子写属性，先看公开 `applyBoss` 的写入模式。若你已经在正确游戏线程的回调里检查了当前 P1、scene 和 generation，且明确处于可操作的普通训练，可以把当前 HP 降一点作为单次实验：

```javascript
// 只供插入完整校验后的回调；此段没有安装钩子。
const hpField = actor.add(0x120);
const oldHp = hpField.readFloat();
if (!Number.isFinite(oldHp) || oldHp <= 1) throw Error('Invalid HP');
hpField.writeFloat(Math.max(1, oldHp - 1));
```

每次人工请求只做一次，记录前后值。不要加到每帧循环让它一直扣血。内存范围须确认可写，停止和重赛时丢掉请求。回血优先用教程里的包装，外部的最大生命值位置这里还没给出。

## 对局属性从 scene 取

| 已知位置 | 目前能读到什么 |
|---|---|
| 主模块+0x2b0d1e8 | 当前主 scene 指针 |
| scene+0x9e4，u32 | 模式类型 |
| scene+0x9c4，u32 | 更新计数 |
| scene+0xc48，u32 | 阶段，7 是经验过滤值 |
| scene+0x20d0 / 2130 | 待加载双方名；各为 C++ 字符串对象 |
| scene+0xa68 / a70 | 对象池范围，观察步长 0x14a0 |

对象池里有召唤物，也可能有表现对象。遍历要设数量上限，先查存活位，再读父级和队伍；名字相同也可能属于另一侧。完整攻击分类目前没做出来。

回合计时、胜场和存档属性没有在这里提供可靠的原生布局。教程初始化能用 `initSetMatchTimer`、`disableRoundWins` 等接口；不要据此猜普通对战里对应内存偏移。
