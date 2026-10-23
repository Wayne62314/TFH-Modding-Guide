# 13 · Development roadmap, useful failures and next steps

[English index](../../README.en.md) · [中文原文](../13-development-roadmap.md)

## How the projects accumulated shared knowledge

| Stage | Question | Reusable information | Outcome/boundary |
|---|---|---|---|
| Resource inventory | Where are scripts and hidden fighters? | GFS indexes, keys, Lua/XML/INI, candidate identifiers | Read-only index, not complete FOIT decompilation |
| Selection edits | Why is confirmation wrong? | Presentation/valid selection/actual loading layers | Slot editing was not the final solution |
| Minimal tutorial | Can the player control the bear? | Original initialization/preload and crash-exposed scene dependencies | User success after preserving original flow |
| Ordinary modes | Can we avoid a special tutorial? | Native loader/caller, pending names, P1 restriction, mode combinations | Training/local CPU/two-player verified individually |
| Basic bosses | Is an enhancement flag enough? | Flag layout and outer-reset timing | Enhancement is not a complete boss |
| Phase 3/Fred | Who controls body, children and cleanup? | State queue, position sync, ownership, collision dependencies, request state machine | Manual-control experiment, not full story reproduction |
| Performance | Why does it work but stall? | Native-query costs, scoped caches, fewer scans/logs | User-confirmed smoothness, not all-machine guarantee |
| Cross-character moves | Hitboxes without animation; one-shot summons | State names, atlases, donor resources and exits are distinct | Conditional successes and failures retained |
| Defense/tech | Why does a success log not match gameplay? | Contact/input separation, ordinary-throw scope, prediction contamination | Offline tests with remaining boundary misses |
| Native/keyboard input | How do directions/attacks actually execute? | Facing transforms, base/derived bytes, legal edges, focus/stop | Input history no longer the sole evidence |
| Replay/human data | Can replay files alone teach? | Input formats, same-frame pre-state, independent alignment, segmentation, privacy | Candidates are not certified expert data |
| Model iteration | Why high matching but rare attacks? | Hold baseline, history errors, relative coordinates, closed-loop distinction | Weaknesses disclosed; no inflated win-rate claims |
| Combo execution | Must all material be recorded manually? | Built-in library, nodes, hit-confirm suffixes, timing/state checks | First built-in route user-tested |

The shared foundation is: form hypotheses from resources, observe read-only at identified lifecycle points, validate a minimal intervention, then encode useful results in guarded adapters/tests. Not every mod began from zero, and no universal decompiler generated them automatically.

## The most reusable assets are not ZIP files

- Separation of resource, presentation and gameplay layers.
- Validated connection points for loading, reset, real updates, input and state lifecycles.
- Explicit fighter, scene, generation, thread and mode constraints.
- Methods distinguishing raw input, final input, displayed commands and actual actions.
- A data pipeline that detects prediction, duplicate and future-information contamination.
- Separation between normal-input execution and named action sequences.
- Failures and counterexamples: preload alone did not explain a crash; same names did not supply presentation; writing a bit did not port a boss.

## Missing information

Complete FOIT execution/compiler specifications; full resource-search/cache priority; all-fighter state/cancel/frame windows; native AI sequence selection and arbitrary intermediate-node continuation; generic independent resource preload; reliable complete boss exits; all mode/network protocols; independent strong-model evaluation and closed-loop metrics.

Do not conceal these gaps by expanding whitelists or forcing state transitions. Research can proceed on several fronts, but each begins with a small question.

## Minimal workflow for another mod author

1. Choose one explicit goal, fighter and mode; do not change assets, rules, UI and networking simultaneously.
2. Pin the build and back up resources. List required scripts/states/objects before replacing entire archives.
3. Observe normal flow and target differences read-only at a consistent moment.
4. Change one variable, with explicit stop and rollback.
5. Check actual actions, input, resources, frame timing, completion and rematches.
6. Return to the original for failure comparisons; missing logs and missing animations are not the same failure.
7. Expand only with evidence; retain scopes and unknowns.
8. Publish documentation/patches, not a private research directory.

Counterexamples are welcome: provide a build hash, minimal reproduction and sanitized results. Differences between builds are useful evidence, not obstacles to bypass.
