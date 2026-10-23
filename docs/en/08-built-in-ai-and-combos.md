# 08 · Built-in AI and combos: do not relearn every fundamental from scratch

[English index](../../README.en.md) · [中文原文](../08-built-in-ai-and-combos.md)

## Evidence for three layers

In this build, AI Lua defines action inputs, pre/postconditions, chain levels, effect-prediction horizons and scoring hints for native AI interfaces. INI files hold named action sequences; character scripts configure their combo directories. Higher-level logic chooses goals based on distance, hit reactions, defense, knockdown and summons.

The built-in CPU therefore has at least goal selection, action definitions and sequence execution. It is neither merely a fixed frame macro nor evidence of a neural network training online during player matches. Prediction calls establish simulation/evaluation, not learned-weight updates.

## Action levels and exceptional cancels

Oleander's script registers 5A, 2A, 5B, 2B, 5C and 2C as levels 1..6. Chain thresholds quickly reject unsuitable actions within sequences. Forward normals, 3C, specials and supers have additional definitions; nil/-1 has not been proved to mean “cancelable at any time.”

Player-described rules are useful hypotheses: upward normal chains, some same-button down-direction transitions, some forward-normal exceptions, 3C jump cancels, special/super hierarchies and the blocked-6C exception. Implementation must also consider fighter states, ground/air, hit/block and tested windows. Do not hardcode a universal alphabetically ordered cancel graph. D may be a character-specific mechanic, not always a fourth normal-attack tier.

## AI and tutorial libraries are different materials

The extracted AI/combos/uni directory contains 22 INIs covering ordinary routes, B starters, midscreen/corner, Fred and helper sequences. The recursive AI combo directories contain 365 files including backups; these are not 365 distinct validated combos.

Trials/combos contains 106 teaching TFHC files, including 14 for Oleander: 4 beginner, 5 intermediate and 5 master. This is a separate dataset with different embedded replay versions from current user recordings; see [chapter 09](09-replays-and-learning.md). This public repository summarizes structure without distributing the game files.

Filenames can mislead: one B_START file actually starts with 2A. Read the sequence instead of classifying by filename alone. Fields chance/max_jd/max_attempts_per_move/min_level exist, but their underlying semantics are not fully recovered. Do not arbitrarily interpret 5 as exactly a 5% activation probability.

## First user-tested built-in route

We selected uni_2_WORK_B_START.ini's order: 5B → 5C → 3C → UF_10 → UF_10 → j.A → j.B → j.C. The adjacent UF nodes maintain directional input continuously; their presence does not automatically establish a double jump.

Actions were mapped to normal input and actual states. Attack nodes advance only after observing the target action plus new opponent damage and a hit-reaction state. Direction nodes use real-update counts; airborne buttons wait for actual takeoff. Retries/timeouts are bounded. The user confirmed successful complete execution.

**The imported material is the game's action order; the executor is our experimental implementation, not a call into the entire native CPU combo engine.** Native effect scoring and max_jd were not fully reproduced. This proves the first route, not all 22 or every distance/opponent.

## Pressure into hit-confirm: the current move is the continuation node

If 5C hits during a pressure sequence, treat that 5C as already executed in the ground-hit route. Do not restart with 5B or repeat 5C. Requirements:

1. Confirm the actual target 5C state, not merely a C input.
2. Use new hit evidence to distinguish an earlier hit reaction and block chip; HP loss alone is insufficient.
3. Align the elapsed time of this move, not the start of the full route.
4. Check opponent height, distance, current combo restrictions and resources.
5. Regenerate subsequent edges from actually held buttons.
6. If the window is unavailable, continue original pressure or exit; never force states to manufacture success.

This restricted branch received successful user feedback. Repeated pressure pushes the opponent away, so splicing cannot continue indefinitely. Attribution currently cross-checks state/new damage, not low-level per-attack IDs; independent projectiles remain an attribution risk.

## Suggested learning-AI architecture

A high-level model selects approaches, starters and routes. An executor maintains the current node, cancel/hit windows and cleanup, preventing frame-by-frame model output from stealing control until completion/interruption. Learn **when to choose which route**, rather than expecting a few replays to teach every button frame.

The built-in library reduces recording effort; it does not solve neutral, mix-ups, defense, resource management or adaptation. Pressure is not automatically a gapless blockstring. An opponent returning to Stand establishes a recovery interval, not by itself a punish or an unsafe route.
