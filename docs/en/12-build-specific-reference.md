# 12 · Native entries and field reference for the studied build

[English index](../../README.en.md) · [中文原文](../12-build-specific-reference.md)

**Research notes apply only to EXE SHA256 `03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D`.** RVAs are relative to the loaded main module; object offsets are relative to verified objects, not process-absolute addresses. Do not delete checks to accommodate another build.

“Used in an experiment” is not an SDK guarantee. Experiments have different restrictions; combining offsets does not automatically produce a safe program. First read [native methods](03-native-investigation.md) and [scopes](07-performance-and-prediction.md).

## Entries/globals

| RVA | Use in this investigation | Evidence and boundaries |
|---|---|---|
| 0x1772f40 | Battle-load observation/pending P1 replacement | Used by public character tool; caller must match |
| 0x1773b84 | Allowed return location for hidden-fighter replacement | Caller filter, not an independent function entry |
| 0x1773720 | Enhancement/controller application after outer reset | Public tool verifies prologue |
| 0x8fbb0 | Native string assignment | Build-specific arguments/allocator, not generic memcpy |
| 0x1780f40 | Fighter flag-setter layout reference | Cross-checked wrapper and implementation |
| 0x189b7e0 | Scene root update | Verify main scene, update arguments, depth/thread/prediction |
| 0x17617a0 | Native input-processing entry | Collect actual fighter input |
| 0x1775820 / 0x1775825 | Verified input call / return address | Former for private-input substitution; latter validates collection source |
| 0x1747110 | Button-aggregation reference | Compared against manual ABCD/B+C; not OS key codes |
| 0x3e3170 / 0x1795980 | State-closure construction / queuing | Used by public phase-3 implementation; requires state table, ownership, correct thread |
| 0x2b0d1e8 | Main-scene pointer location | Re-read contents; do not permanently cache pointer |
| 0x2b0cc33 | Byte used for AI-prediction isolation | Requires depth tracking and callback rechecks; not a full network detector |

## Scene fields

| Offset | Observed type | Use/limitation |
|---|---|---|
| +0x9e4 | u32 | Battle/scene type; 0 alone cannot distinguish replay/live play |
| +0x9c4 | u32 | Update counter; entry/exit delta of 1 is a sampling gate |
| +0xc48 | u32 | Phase; 7 is an empirical filter, not universal action eligibility |
| +0xaa8 / +0xab4 | s32 | Current P1/P2 slots; checked ranges 0..2 and 3..5 |
| +0xae0 + slot*8 | pointer | Slot-to-fighter lookup; check null/team/identity |
| +0xa68 / +0xa70 | pointer | Object-pool range; observed stride 0x14a0, bounded count/liveness checks |
| +0x2028 | pointer | Current mode object; check non-null first |
| mode object +0x1e8 | u8 | Auxiliary observed training flag, not a universal mode classifier |
| +0x20d0 / +0x2130 | string object | Pending fighter names; do not overwrite as raw C strings |
| +0x2368 | s32 | P1 palette setting used for bear replacement; known palette only |

## Fighter and associated data

| Offset/path | Type | Meaning |
|---|---|---|
| actor+0x88 | float | Team value: observed 1=P1 side, 2=P2 side |
| actor+0x90 | float | Observed control-related field; **identity semantics not fully validated** |
| actor+0xfc | float | Actual facing, expected ±1 here |
| actor+0x120 | float | HP for change audits; not sufficient alone for hit confirmation |
| actor+0x128..0x13c | floats | super/max/per-level, magic/max/per-level; verify scaling |
| actor+0x324 / +0x328 | float | vx_local/vy; horizontal value already fighter-local |
| actor+0x590 onward | u32 bitfields | Flag groups; Flag27 is 0x08000000 in this build; do not overwrite entire word |
| actor+0xc50 → data+0xb40 | pointer → string | Data name; case may differ from selection identifier |
| actor+0xc58 → state+0x10 | pointer → string | Current state name, not animation frame number |
| actor+0xc78 / +0xc7c | s32 | Observed x/y; other synchronized positions exist; avoid bare writes |
| actor+0x1270 | u64 | Part of identity scope, helps detect generation changes |
| actor+0xb30 | pointer | Parent clue; bounded traversal within live-object set only |
| actor+0x1262, bit 0x40 | bit | One pool-inactivity check, not proof of ownership |
| actor+0x1260, bit 0x08 | bit | One attack-active condition; do not dereference attack data arbitrarily when inactive |

Unlisted fields are not off-limits to research; these notes simply lack sufficient conclusions. Preserve resource units: Oleander and Velvet magic must not be interpreted using one fixed maximum.

## Correcting the type mapping

The build's type-name function at 0x18b34c0 and jump table provide: 0 MULTIPLAYER_LOCAL; 1 MULTIPLAYER_ONLINE; 2 AI_VANILLA; 3 AI_STORY; 4 AI_ARCADE_STORY; 5 AI_ARCADE_RANDOM; 9 TUTORIAL; 10 TRAINING; 11 LEADERBOARD; 12 CREDITS; 13 STORE; 14 GALLERY; 15 NONE. No unconfirmed meanings are assigned to 6/7/8.

This is a name mapping, not proof of testing every mode. 0 can also appear during replays. Old comments treated 11 as online and conservatively rejected it, but name evidence does not support that description. Do not copy a historical broad whitelist as “all offline battles validated.”

See [sources](../../SOURCES.en.md) for public implementation anchors and reproduction clues. Private ASLR addresses and complete dumps are not included.
