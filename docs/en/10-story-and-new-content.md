# 10 · What other mods can this knowledge support?

[English index](../../README.en.md) · [中文原文](../10-story-and-new-content.md)

## A standalone tutorial lesson: a manageable starting point

The tutorial framework already supplies entry, stage, fighter setup, dialogue, goals, update callbacks and retry. We designed a standalone “Revenge of the Clawed Animals” lesson: an original salt-cave story, 11 consecutive opponents, pre/post-fight dialogue and failure retry. It is a fan scenario, not an official story continuation. A separate entry and static checks do not establish playtested transitions across all 11 fights.

Keep original dialogue in separate data and gameplay in generation templates, producing the packaged script. Point a menu item to the new entry while retaining other lessons. Do not replace every basic tutorial to add one lesson, or call repurposing a slot a complete new mode.

Existing dialogue channels can be reused, but a default teacher portrait does not establish unique portraits, voices or complete illustration layouts for every speaker. Validate UI, art assets, speaker identifiers and dialogue text separately.

## Rewriting story mode around another protagonist

This is more than replacing a name with the bear. Original scenes may require specific movement, quest triggers, cameras, platforms, skill tutorials, NPC behavior and rewards. Check reachability, death/retry, quest state, resources, transitions, saves and presentation for every affected stage.

Start with an isolated scene that does not alter save rewards. A controllable bear in one tutorial is not proof that the entire story can be completed as Huggles.

## Skins and palettes

Investigate textures, atlases/frame mappings, palettes and resource keys. Finding a DDS/PNG does not establish a working replacement: check caching, compression, atlas layout, alpha, palette systems, dimensions and load priority. Portraits, battle frames and effects may be separate.

We have not completed a universal skin importer or established that one image can replace every asset. Begin with one-resource replacement/restoration tests; do not distribute complete game archives.

## Custom fighters

A full fighter generally needs a valid identifier, loading/selection/preview, animations/atlases, states/cancels/input, collision and attack properties, sound/effects, resources/summons, victory/defeat/rematches, tutorials/AI and an installation/distribution pipeline.

We understand parts of state directories and runtime entries, but **do not have a complete FOIT compiler/state editor or a reconstruction of all serialized instructions**. Existing-state experiments are not a full new-character toolchain. A practical progression is reversible action/presentation experiments on existing fighters, then incremental asset-tool development.

## Cross-character moves

Dependencies form layers: action execution → body frames/visibility → separate effects/projectiles → ownership/contact → resource loading → destruction/restoration. Substitute layer by layer, not by first copying a state pointer. Loading dependencies through the opponent is a controlled diagnostic, not a final installation strategy.

## Offline sparring and player-server bots

Offline sparring first needs reliable execution, timing, route context and diverse data. Server bots additionally need clear identity, player consent, input synchronization, rollback, seat management and server protocols. We have not completed that chain. Removing existing tools' network restrictions is not a deployment plan.

## Suggested progression

One-shot read-only observation → minimal existing-fighter/input experiment → standalone tutorial lesson → conditional boss control → validated action graphs/combo execution → model choices → broader fighter/resource tooling. Difficulty depends on lifecycle and dependencies, not line count alone.
