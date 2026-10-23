# TFH modding research notes

This public documentation explains a local, evidence-driven development process for Them’s Fightin’ Herds mods: package inspection, Lua/native boundaries, hidden-character loading, experimental boss controls, native input, replay alignment and offline AI.

The detailed chapters are currently Chinese. Start with the [chapter index](README.md). Important distinctions:

- An existing state name does not prove its animation, assets or cleanup work in another character/scene.
- Character-select presentation is separate from the fighter loaded into battle.
- Resource patches, process-memory changes, native-input substitution and OS keyboard simulation are different approaches.
- The first imported Oleander AI combo was user-tested. That is not proof of a strong autonomous fighting model or support for every built-in route.
- Published offsets describe one verified executable build, not a general SDK.

This repository contains newly written explanations, synthetic examples and provenance references only. No private traces, player replays, game assets, memory dumps, credentials or private-repository history are included. Existing public implementation: [TFHMOD](https://github.com/Wayne62314/TFHMOD).

Offline, authorized research only. Do not remove network restrictions or treat a local whitelist as an anti-cheat guarantee. See [publication boundaries](PUBLICATION.md) and [sources](SOURCES.md).
