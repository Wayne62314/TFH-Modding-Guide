# 04 · Huggles: from failed selection to battle-load replacement

[English index](../../README.en.md) · [中文原文](../04-huggles-case-study.md)

## Initial goal and failures

The goal was player-controlled Huggles. File investigation found the candidate internal name bscout, plus preload and fighter setup in story-boss initialization. Initial selection-list/Arizona replacement attempts left the Arizona preview and sometimes selected another fighter on confirmation. This showed that the edit affected the flow, not that a valid target fighter had entered battle.

Separate at least three layers:

- **Selection presentation:** slots, portraits, names and preview animations.
- **Selection validity/submission:** acceptance of an identifier, fallback or alternative selection.
- **Battle instantiation:** actual fighter data, palette, states and resources loaded.

“There are only so many UI slots” does not establish that editing the UI is necessary. Nor does random fallback identify a particular validation function unless that branch has been traced.

## Why start in a tutorial?

Tutorials already provide a working scene, targets, dialogue and fighter-initialization interfaces. Retaining the original movement lesson and adding minimal bear settings to its existing matchSettings callback preserved more engine dependencies than reconstructing a whole free-test scene.

The first custom initialization crashed. Preloading and removing training features did not resolve it. We reduced the change further, kept the original flow, and the user eventually obtained a controllable bear. This established a working minimal path, not a complete causal reconstruction of every earlier crash.

## Moving into ordinary training/local matches

After tutorial success, we investigated native loading after normal selection. The scene held pending P1/P2 names. At a verified call site, we replaced P1's cow with bscout and let the native loader continue. We used the game's string-assignment logic for C++ string ownership and limited the bear to known palette 0.

This does not replace Arizona's atlas/FOIT files or redirect ordinary training into a tutorial. P2 remains unchanged. The preview can remain Arizona because it belongs to an earlier layer; the actual in-battle fighter is the primary acceptance criterion.

Local CPU and local two-player were sampled and tested separately. Ordinary training also has a mode=10, training-flag=1 route. An early rule recognizing only 0 caused the shared package to “do nothing”; logs led to a correction. **An incorrect whitelist can look like a completely nonfunctional feature.** Do not first assume asset corruption.

## Information that made this mod possible

| Information | Use |
|---|---|
| bscout resources/story references | Real internal fighter candidate |
| Original tutorial initialization callback | Working minimal load environment |
| Scene dependency exposed by crashes | Avoiding excessive scene reconstruction |
| Pending names and verified caller | Precise P1 replacement in ordinary modes |
| std::string assignment/function bytes | Correct string lifetime and build rejection |
| Mode/training combination | Application only in investigated offline paths |
| Actual playtests | Entry, movement, jumping and attacks—not just a changed string |

## Coverage

The user tested bear replacement in ordinary free training, local CPU and local two-player. Hidden enemies may lack a regular fighter's complete victory, rematch, palette or UI assets; test these separately. Closing the tool does not immediately restore an existing bear instance. Reload, or fully restart when necessary.

See S1's loading hook. Read the reasoning before the RVAs so that you know why a location was used and when not to use it.
