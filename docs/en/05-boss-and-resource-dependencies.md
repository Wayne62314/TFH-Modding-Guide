# 05 · A boss is not a switch: phases, resources and cleanup

[English index](../../README.en.md) · [中文原文](../05-boss-and-resource-dependencies.md)

## Four separate meanings of “playable boss”

1. Flag enhancement: a flag selects an existing enhanced branch.
2. Action access: the player can enter a particular boss state.
3. Scene control: flight, camera, wind, obstacles, summons and phase changes.
4. Complete battle loop: resources, damage, exits, hit reactions, rematches and normal control all behave sensibly.

Completing only the first is an enhancement/flag experiment, not a full boss. Forcing entry into a state does not port the story controller.

## Oleander: Flag27, phase 3 and Book

Basic enhancement sets Flag27 after fighter initialization using a confirmed flag layout. Readback proves the write, not that all hidden moves are available.

Phase 3 additionally depends on states such as Flight_Start, Flight_N_BG and HomingSparkCast, player-input acceptance, spatial movement and child objects. Early WASD moved Book but not Oleander's body. A “fighter” is not just one x/y pair: we needed the original story's position-synchronization method and checks of body, Book, actual/cached positions and camera relationships.

The tutorial sandbox retained Free Play initialization and omitted the original boss's autonomous AI to avoid overriding player control. Ordinary-match integration then traced Lua binding wrappers to native state queuing, input and synchronization. Sandbox success did not establish support in every local mode.

## Fred and vortex

Boss Fred needs states, resources, ownership, scene dependencies and exit paths. Some flows depend on collision/semi-entity slots; the story also arranges maps and phases. An ordinary-stage controller must supply minimal necessary dependencies rather than loading an entire boss map and confusing the mode.

Engineering measures included a summon queue, cooldown, waiting for Intro to finish, locating only Fred actually owned by P1, rejecting ambiguous multiple objects, rechecking generations during cleanup, and cleaning children before parents. Do not pick the first object named FredBoss, or pass Frida-allocated memory to the game's free.

The “reddish Oleander, no more skills after vortex” failure suggests incomplete state, input acceptance or effect restoration. Repair should follow native exit flows, not write Stand or rebuild the fighter every frame. A historical report of the opponent temporarily looking like Arizona was not reproducibly resolved; do not claim its root cause is fully understood.

## Tianhuo Backdraft and borrowing from Baihe

Old Tianhuo AI retains ground/air Backdraft clues; Baihe also has same-named states and related atlas references. Some old registration/decision calls are commented out. A name's presence does not mean it is enabled by default.

The user verified ground A/B/C attack effects with different knockback distances, but body animation/effects were missing. Borrowing related Baihe states also produced disappearance or no animation. The supported conclusion is “attack logic is reachable, presentation dependencies are incomplete,” not “the full boss is restored.”

Same-named animation/resource indexes may be meaningful only in their own fighter data. Moving a name, state pointer or fighter into that state does not supply atlases, projectiles, sound, parenting, input or destruction relationships. Check state bodies, visibility, frame references and dependencies layer by layer. Historical asset-reuse claims do not prove wholesale interchangeability.

## Cross-character ordinary Fred and Supernova

The Tianhuo/ordinary-Fred experiment requires ordinary Oleander as P2 so the game loads dependencies normally before the object is created/called. This is a diagnostic **resource donor** condition—not arbitrary-opponent support or a completed independent preload. Repeated summons also require the old object to exit and cooldown to recover.

A minimal experiment with Baihe's two-meter Supernova objects did not produce usable orbs or the complete performance; the UI remains disabled. **Failures are useful development information.** An object name and one creation attempt do not justify promises of damage, a two-meter cost or a full super.

## Velvet / Paprika

Velvet's Boss_Install, Boss_Wind_Idle and Boss_IceL/M/H can serve as experimental entries. Story wind push is applied continuously by Lua, so the tornado state alone is not the entire wind field. Exit, hiding and cleanup retain dependencies; the public tool explicitly requires restarting after use.

Paprika's story phase sets Flag27, but foreground leaps/teleports also depend on behavior trees and stage flow. The user confirmed the flag experiment runs; its actual enhancement effects remain unclear. This does not establish access to all foreground boss attacks.

Standalone experiments and integrated UI features may have different validation levels. Public S1 source is an interface/guardrail reference, not a guarantee of complete boss ports.
