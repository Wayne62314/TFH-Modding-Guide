# 3 · Load Huggles through Arizona; enhance Oleander

[Tutorial index](../README.en.md) · [中文](../zh/03-hidden-boss.md)

Huggles replacement in ordinary training/local matches has successful user reports. Oleander enhancement and manual phase-3 experiments were also tested. Fred cleanup has separate limits; enabling one flag does not deliver a complete story boss.

## Try the bear in your lesson

After the ordinary-fighter lesson works, add these lines after initTrial in the existing setMatchSettings:

```lua
preloadSprite("bscout")
initSetPlayerSprite(Player1, "bscout")
initSetPlayerPalette(Player1, 0)
```

This change is distilled from an earlier successful path; this newly assembled lesson combination still needs playtesting. Preserve existing initialization and use known bear palette 0. Borrowing a regular fighter's palette adds an unnecessary variable.

Rebuild/install the candidate and enter through its menu. Judge the actual in-battle body and controls, not whether character select shows a bear portrait.

## Replace the load in ordinary training

Search the public ui/training-hook.js for shouldReplace. Its conditions include:

```javascript
const offline = fightType === 0 || (fightType === 10 && training === 1);
return options.bear && offline && name === 'cow' && callerRva === '0x1773b84';
```

Keep this inside its original function: parameters/options come from that file. cow is Arizona's pending load name. The module also filters a known caller. Mode 0 can occur in replays; this rule alone does not identify every context.

The build's load hook is at RVA 0x1772f40. Once conditions pass:

```javascript
assign(p1, bear, 6);
scene.add(0x2368).writeS32(0);
```

p1 here points to the scene's string object, not the fighter. bear is a retained Memory.allocUtf8String('bscout'); 6 is its byte length. assign uses verified native string assignment at 0x8fbb0; find its declaration in the file. These two lines cannot be pasted into an arbitrary callback.

For a small exercise, change name === 'cow' to another ordinary fighter's **verified** loading identifier. Start the full UI with only Huggles enabled. Arizona no longer triggers it; the new selection path needs testing. This changes the trigger fighter, while the target remains bscout.

## Write the Oleander enhancement bit

Read applyBoss(scene) in the same file. It runs after outer reset 0x1773720, checks P1's slot/team and then accesses the flag field:

```javascript
const field = sprite.add(0x590);
const before = field.readU32();
const after = (before | 0x08000000) >>> 0;
if (before !== after) field.writeU32(after);
```

This excerpt comes from inside the function. Keep its mode, fighter-name and writable-range checks, as well as its reset-lifecycle constraints.

Flag27 is zero-indexed, mask 1 << 27. OR preserves other bits. writeU32(0x08000000) alone would erase other flags in the word. Clearing the bit may not undo existing effects; restart for a reliable comparison.

## Where to read about phase 3

Read requests/timeouts in phase3-controller.js, then makeStateClosure, enqueueState and position synchronization in phase3-native.js. Public code includes the wrapper signatures; state lookup and ownership checks belong with them.

Do not directly replace the current state pointer with Flight_N_BG's address. Early experiments moved Book without synchronizing Oleander's body. Ordinary Fred additionally needs donor resources: the Tianhuo experiment requires ordinary P2 Oleander.

Velvet's tornado still requires restarting after use. Paprika Flag27's exact effects remain unclear. Baihe Supernova was not successfully ported. Choose a known entry first; keep features disabled while dependencies remain unresolved.
