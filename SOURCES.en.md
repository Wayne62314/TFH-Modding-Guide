# Sources and reproducibility

[English index](README.en.md) · [中文原文](SOURCES.md)

These notes are primarily original summaries of the developer's projects and authorized offline experiments. Research records mainly extend through October 22, 2026; publication was prepared October 23, 2026. Public references below help inspect implementations. This repository does not copy complete game scripts or private experiment directories.

## S1 · Public TFHMOD source

[Project](https://github.com/Wayne62314/TFHMOD). Source reviewed at commit `a630d5a8995527520beed628a778231d1eb95751`. If a link fails or files change, check the commit first; changes on main do not retroactively redefine historical experiments.

- [Load/reset/enhancement hooks](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/training-hook.js): P1 replacement, mode combinations, Flag27 and module configuration.
- [Phase-3 native adapter](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/phase3-native.js): scoped range caches, state queuing, positions, object ownership and restoration.
- [Phase-3 controller](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/phase3-controller.js): requests, waits, timeouts, recovery and error lockout.
- [Additional boss experiments](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/boss-extras.js): restricted Paprika/Velvet entry points and limitations.
- [Tianhuo summons](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/tian-summons.js): prerequisites including ordinary P2 Oleander; unsuccessful Supernova remains disabled.
- [English usage guide](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/USAGE.en.txt): versions, installation and known limits—not proof of every integrated gameplay regression.

## S2 · Velvet Beautifier

[Reference repository](https://github.com/Wayne62314/velvet-beautifier), reviewed at `ce2b09e63531bda79e33990a89f5ab866b9f591b`. It has its own upstream, contribution history and licenses; it is not our original work.

- [Process documentation](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/PROCESS.md): backups, restoration, GFS/TFHRES and mod application order.
- [GFS utilities](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/VelvetBeautifier/GFS/Utils.cs): archive extraction/creation usage.
- [TFHResource management](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/VelvetBeautifier/TFHResource/Manager.cs): resource paths, clone/merge/save and rollback.

Its role was primarily format/installation reference. This does not establish that native lifecycle, input, prediction isolation and AI-data investigation were already upstream features.

## S3 · Tool interfaces

- [Frida JavaScript API](https://frida.re/docs/javascript-api/): Interceptor, NativeFunction, NativePointer, Memory, Process, etc. Tool API documentation is not evidence for TFH object layouts.
- [Microsoft PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format): RVA, entry points, sections and exception-directory concepts. Game-specific semantics still require local validation.

## L1 · Resource paths owners can inspect themselves

These are logical archive paths/names, **not downloadable assets in this repository**:

- ai-libs.gfs: AI/uni.lua, AI/common_goat.lua, AI/tianhuo.lua, AI/baihe.lua, AI/combos/uni/*.ini and related decisions XML.
- trials.gfs: Trials/story/bossMultistage.lua, oleander_round3.xml, platforming/paprika_fight.lua, velvet_fight.lua, training libraries and menu XML.
- characters-foits.gfs: temp/tianhuo.foit, temp/baihe.foit and other serialized fighter data; names/state candidates are not complete instruction decoding.
- Local resources_prod/lobbymaps_prod TFHRES schema, plus read-only parsing of 20 TFHR and 3 named TFHC samples.

## L2 · Results whose raw records are not public

These notes include sanitized summaries of crashes/runtime sampling, model comparisons and user playtests. Raw logs, replays, dumps, participant information and models are not included, and no links requiring private-repository access are provided. Readers cannot independently reproduce every historical observation from this text alone. Retest on the matching build under equivalent conditions and report evidence levels as in [chapter 00](docs/en/00-evidence-and-scope.md).

Synthetic example tests validate the examples themselves. They do not replace original-game experiments or establish complete support for all formats/builds.
