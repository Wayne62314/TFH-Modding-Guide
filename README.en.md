# TFH Modding Guide: from resource investigation to runtime mods

**English documentation** · [中文文档](README.md)

A public developer guide for Them's Fightin' Herds mod authors—not an official SDK or a complete decompilation. Published October 23, 2026; research records mainly extend through October 22, 2026. Validation concerns one Windows x64 game build.

This guide explains **how “I want to play the hidden bear” developed into fighter replacement, boss-state experiments, a story-lesson project, native input, combo execution and offline AI: what information made each step possible, and what remains unproven.**

All 14 chapters and the supporting reference documents now have English versions. These are translations of the Chinese research notes, not additional game validation. Technical identifiers, addresses, evidence levels and limitations are preserved. If you find a discrepancy, report the chapter and build rather than interpreting a translation as new evidence.

## Three essential distinctions

1. The game is not “all Lua.” Its native engine handles objects, state execution, input, resources and collision; Lua/XML/INI provide substantial gameplay orchestration, goals and configuration.
2. A resource, state name or flag is a clue. Loading context, execution path, ownership and cleanup still need validation.
3. Resource patches, process-memory changes, native-input substitution and Windows keyboard simulation are different approaches. “No game files changed” does not mean gameplay is unchanged.

## Full English chapter index

For code-led exercises, start with the **[hands-on tutorials](tutorials/README.en.md)**: environment setup, a new tutorial lesson, a battle chapter, hidden bosses, fighter/match properties, Frida hooks, input and UI integration. Newly written samples state their own validation status. [中文动手教程](tutorials/README.md).

| Question | Chapter |
|---|---|
| What counts as evidence, inference or success? | [00 · Evidence and scope](docs/en/00-evidence-and-scope.md) |
| How do the engine, entry points and Lua interact? | [01 · Engine and lifecycle](docs/en/01-engine-and-lifecycle.md) |
| What are GFS, TFHRES and FOIT? Which template/temp files run? | [02 · Assets and script routing](docs/en/02-assets-and-script-routing.md) |
| How can native functions be investigated without an SDK? | [03 · Native investigation](docs/en/03-native-investigation.md) |
| Why was adding a selection slot insufficient for Huggles? | [04 · Huggles case study](docs/en/04-huggles-case-study.md) |
| What do phase-3 Oleander, Fred and cross-character moves depend on? | [05 · Boss and resource dependencies](docs/en/05-boss-and-resource-dependencies.md) |
| How do defense, throw techs and input approaches differ? | [06 · Input and defense](docs/en/06-input-and-defense.md) |
| How were stalls, prediction calls and stale pointers handled? | [07 · Performance and prediction](docs/en/07-performance-and-prediction.md) |
| How do built-in AI sequences and mid-route continuation work? | [08 · Built-in AI and combos](docs/en/08-built-in-ai-and-combos.md) |
| Can replay files train an AI? What does input matching measure? | [09 · Replays and learning](docs/en/09-replays-and-learning.md) |
| How feasible are story mods, skins and new fighters? | [10 · Story and new content](docs/en/10-story-and-new-content.md) |
| How should a mod be tested, packaged, rolled back and published? | [11 · Testing, packaging and publication](docs/en/11-testing-packaging-and-publication.md) |
| Which build-specific fields and entry points were identified? | [12 · Build-specific reference](docs/en/12-build-specific-reference.md) |
| What was learned across projects, and what is still missing? | [13 · Development roadmap](docs/en/13-development-roadmap.md) |

Supporting documents: [sources and provenance](SOURCES.en.md), [glossary](GLOSSARY.en.md), [publication/privacy/rights](PUBLICATION.en.md), [safe examples](examples/README.en.md).

## Completed does not mean universally supported

- **User-tested:** Huggles replacement in ordinary offline training/local matches; Oleander enhancement/manual-flight experiments; native directions/ABCD; some ordinary ground/air-throw assistance tests; user-recorded combo reproduction; 5C hit continuation; the first imported built-in Oleander AI route.
- **Conditional/incomplete:** repeated Fred summons and vortex cleanup, Velvet tornado, Paprika Flag27, cross-character ordinary Fred, jump/landing defense boundaries and unused-move animations.
- **Not established:** complete story-boss ports, Baihe Supernova transfer, universal fighter/scene input AI, a complete skin/new-fighter toolchain, strong autonomous sparring or network bots.

Modules and versions may have been tested separately. Integrated regression is a different task; this list is not one comprehensively validated release package. Read each chapter's evidence boundaries.

## Public implementation references

- [TFHMOD](https://github.com/Wayne62314/TFHMOD): public character-tool sources, experimental UI and usage guides.
- [Velvet Beautifier reference repository](https://github.com/Wayne62314/velvet-beautifier): important resource-format, packaging and installation references; respect its upstream and licenses.
- [Official Frida JavaScript API](https://frida.re/docs/javascript-api/): runtime observation, NativeFunction, Interceptor and related interfaces.

This repository was written separately, without importing private research history. **It contains no private raw traces, replays, participant information, game assets, memory dumps, models or credentials.** Starter examples process indexes and synthetic input. Hands-on lessons additionally supply a candidate-package builder, original Lua lesson and read-only training observer. The observer attaches through Frida but submits no input. The builder prepares local output without installing it. New samples still require in-game validation.

## Supported build and boundaries

Studied executable SHA256:

```text
03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D
```

RVAs/fields are not a stable SDK. Revalidate function signatures, object semantics and conditions on another build; do not bypass checks.

All runtime experiments are for authorized offline environments. Do not remove network restrictions, bypass anti-cheat or disable security software. Owning a server does not establish knowledge of client synchronization/rollback protocols or other players' consent to assistance tools.
