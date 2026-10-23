# 4 · Read fighter and match properties

[Tutorial index](../README.en.md) · [中文](../zh/04-properties.md)

There are two paths: Lua inside your lesson, and an external runtime tool. Put Lua examples into your lesson. Begin external work with the read-only training observer.

## Health and resources inside the lesson

In a routine after initialization, reacquire P1:

```lua
local p1 = getP1()
print("HP=" .. tostring(p1.Lifebar))
print("max HP=" .. tostring(p1:maxLife()))
p1:fullHeal()
p1:setSuperLevel(1)
p1:giveMaxMagic()
```

Inspect wrappers in this build's Trials/Lib/LuaLib.lua. setSuperLevel scales by the internal per-level unit; its source does not provide complete bounds checking. This example sets one level—first verify the fighter's maximum. setMagicLevel has a similar issue, and mechanics differ across characters.

To try half maximum health at the same location:

```lua
local maxHp = p1:maxLife()
p1.Lifebar = math.max(1, math.floor(maxHp * 0.5))
```

Training may refill health automatically; check OptLifeBar. Recoverable life, displayed health and death handling may depend on other fields. This tests current HP, not a complete health-system modification. Historical scripts use both lifebar and Lifebar; follow this build's wrapper spelling Lifebar rather than generalizing case behavior across all properties.

Movement also has wrappers such as trialSetupDistance and spriteSnapPosition. Flight requires body, Book and cached-position synchronization; a raw x/y write may move only part of the representation.

## Run the external read-only observer

From TFH-Modding-Guide, using the neighboring TFHMOD virtual environment:

```powershell
Get-Process -Name "Them's Fightin' Herds" | Select-Object Id,ProcessName
..\TFHMOD\.venv\Scripts\python.exe examples/observe_training.py --pid 1234
```

Replace 1234 with your PID. Enter ordinary free training with any fighters and close other tools. The observer accepts mode 10, the observed training flag and phase 7 only. Press Enter in its terminal to detach.

This new observer has no in-game acceptance test yet. It uses previously investigated fields/signatures and attempts a sample every 30 counter values. It sends only when the root call advances the counter by exactly one. It does not substitute input or call mutating game functions.

p1/p2 contain data name, state, position, facing, HP and raw super/magic. counter identifies the pre-update entry. Output is not continuous frame data; do not treat it as a ready training dataset.

## How fields are read

See fighter() in [observe_training.js](../../examples/observe_training.js). Lookup goes main scene → current slot → actor → data/state.

```javascript
const slot = scene.add(0xaa8).readS32();
const actor = scene.add(0xae0 + slot * 8).readPointer();
const hp = actor.add(0x120).readFloat();
const x = actor.add(0xc78).readS32();
```

Checks are omitted in this explanatory excerpt. The full file checks slot range and team first. P1 uses 0xaa8, P2 0xab4. The first pool object is not necessarily P1.

| Field | Type/read | Caveat |
|---|---|---|
| actor+0xfc | float facing, observed ±1 | Read current value after side switches |
| actor+0x120 | float HP | HP loss alone cannot attribute a hit |
| actor+0x128 / 12c / 130 | float super / max / per-level | Read the actual per-level unit |
| actor+0x134 / 138 / 13c | float magic / max / per-level | Character maxima differ |
| actor+0xc78 / c7c | s32 observed x/y | Additional synchronized positions exist |
| actor+0xc50 → data+0xb40 | pointer then string | Data name Uni can differ from load name uni |
| actor+0xc58 → state+0x10 | pointer then string | State name is not a cancel window |
| actor+0x1270 | u64 | Part of generation identity |

For an external write, first study public applyBoss. If you have already verified current P1, scene and generation inside the correct game-thread callback, and confirmed ordinary actionable training, a one-time HP decrease is a small experiment:

```javascript
// Insert only after complete callback validation; this does not install a hook.
const hpField = actor.add(0x120);
const oldHp = hpField.readFloat();
if (!Number.isFinite(oldHp) || oldHp <= 1) throw Error('Invalid HP');
hpField.writeFloat(Math.max(1, oldHp - 1));
```

Consume one manual request once and record before/after. Do not run it every frame. Check writable bounds and discard requests on stop/rematch. Prefer lesson wrappers for healing; this guide does not provide an external maximum-HP location.

## Match properties come from scene

| Known location | Observation |
|---|---|
| main module+0x2b0d1e8 | Current main-scene pointer |
| scene+0x9e4, u32 | Mode type |
| scene+0x9c4, u32 | Update counter |
| scene+0xc48, u32 | Phase; 7 is empirical |
| scene+0x20d0 / 2130 | Pending fighter names, each a C++ string object |
| scene+0xa68 / a70 | Object-pool bounds, observed stride 0x14a0 |

The pool contains summons and possibly presentation objects. Bound traversal, check liveness, then inspect parents/team. Identical names can belong to different sides. Complete attack classification is unfinished.

Reliable native layouts for round timer, wins and save properties are not supplied here. Tutorials expose initialization APIs such as initSetMatchTimer and disableRoundWins; these do not establish corresponding ordinary-match memory offsets.
