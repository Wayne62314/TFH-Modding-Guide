# 06 · Defense and input: four different approaches

[English index](../../README.en.md) · [中文原文](../06-input-and-defense.md)

| Approach | Intervention point | Project experience |
|---|---|---|
| Contact-result/flag assistance | Temporary flags/results near hit resolution | Some instant blocks, not genuine directional input |
| Private native-input copy | Private structure passed to fighter input processing | Both input history and actual actions can work; useful for combos/AI |
| Windows SendInput | OS keyboard events | Focus, bindings and scheduling matter; more likely to arrive late |
| State forcing/queuing | Fighter state system | Used for boss experiments; not normal input or proof of combo execution |

## Basic input encoding

In the studied structure, offset 0 is direction and offsets 3/4/5/6 are A/B/C/D. Raw button states are 0=new press, 1=release, 3=held, 4=up. Internal ML classes may instead use indexes 0/1/2/3; document conversions explicitly.

Individually verified screen directions include 0=right, 1=down-right, 2=down, 3=down-left, 4=left, 8=neutral. Reflection is `[4,3,2,1,0,7,6,5,8]`. Upper diagonals were used in execution routes but not every direction received identical independent calibration. Facing differs from screen position: read actual facing instead of always holding the physical A key.

## Critical pitfall: A is displayed, but no attack happens

Changing only base A/B/C/D bytes displayed A in input history without making Oleander attack. A same-session “manual A → manually triggered single A” comparison exposed missing derived fields. B/C/D and B+C sampling then calibrated the remaining fields; the user confirmed actual attacks.

Calibrated mappings for this build are A=[3,19,25], B=[4,20,26], C=[5,18,24], D=[6,17,23]. Channels 9..14 are aggregates: count press/release/held over specified button sets, then generate values using thresholds. Native rules have priorities; simply OR-ing “any button held” into every aggregate is incorrect.

This mapping comes from normal manual input and native aggregation in this build. It is not a keyboard scan-code mapping or a cross-build promise. The [synthetic input example](../../examples/input_edges.py) demonstrates legal edges only and is not a complete injector.

## Private input copies

At a verified call site, copy the complete known input range, change only controlled directions/buttons and derived channels, then substitute the pointer for that call. Do not modify a shared raw buffer. Preserve unrelated flags and unknown fields. The private allocation must remain alive throughout actual consumption; do not pass a short-lived object to asynchronous consumers.

Advance scheduling at most once per real update. Repeated input calls at the same counter must see identical edges, not press on the first call and held on the second. When splicing routes, regenerate edges from what is actually held; do not paste a recording's mid-sequence held state blindly.

## Defense and throw-tech findings

Early instant-block assistance temporarily used Flag25 at identified contact points and selected native defense results, retaining normal chip damage. That does not imply a back direction appears in input history, nor does it constitute a learned AI.

Ordinary throw assistance instead sends B+C at the real input entry and lets native rules determine whether a tech is legal. Coverage is limited to recognized ordinary front/back and air throws, not forced command-grab escapes or arbitrary expansion to hitstun/non-defendable states. CPU prediction once logged success without a real-match tech, making true-state confirmation and prediction isolation essential.

Air defense cannot be defined solely as y above ground: jump startup, double-jump transitions and landing boundaries have their own rules. Some boundaries still miss defense. Do not claim 100% success across every fighter/state.

## Why keyboard simulation can be late

Observation, Python/JS communication, OS event queues, focus and game sampling all add latency. Sending back through SendInput only at contact is often too late; decisions must precede impact using classified startups or projectile arrival. An incorrect mode rule once skipped the entire system, with the same apparent “too slow/not blocking” symptom. Check whether input was actually submitted before tuning timing.

Native input does not solve when to defend, which guard height to choose or whether defense is legal. It is a more direct execution layer. The CPU's forward simulation does not mean we recovered a reusable general defense-decision interface.

## Public-use boundaries

These mechanisms are discussed for authorized offline experiments only. This repository does not publish private assistance tools, online-unrestricted variants or anti-cheat bypasses. Frequent writes, input contention and missing releases can break normal control. Manual input, loss of focus, pause, mode change and F10 should stop experiments; do not remove safeguards to improve apparent success rates.
