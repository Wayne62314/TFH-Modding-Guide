# 02 · Resource files, templates and actual loading paths

[English index](../../README.en.md) · [中文原文](../02-assets-and-script-routing.md)

## File map

| File/directory clue | Role in this investigation | Common mistake |
|---|---|---|
| data01/*.gfs | Indexed Reverge resource archives | Treating them as ZIPs or overwriting everything |
| characters-foits.gfs / temp/*.foit | Serialized fighter data and state/resource name clues | Assuming a discovered name means the state implementation is decoded |
| ai-libs.gfs / AI/*.lua | Action definitions, predicates and goal selection | Treating them as actual animation code |
| AI/decisions/*.xml | Behavior-tree/phase-flow clues | Re-enabling a complete old tree merely because it exists |
| AI/combos/*/*.ini | Named action sequences and parameters | Treating them as frame-by-frame input or fully validated combos |
| trials.gfs / Trials/... | Tutorial menus/scripts and story/boss orchestration | Rebuilding initialization while omitting scene dependencies |
| ui*.gfs | Character-select and other UI resources | Expecting a UI edit alone to load a valid fighter |
| Scripts/src/Farm/resources/*.tfhres | Samples contained SQLite tables/cache records | Assuming every file with the extension has the same structure |
| .tfhr / .tfhc | Match replay/training-combo input material | Assuming every frame's full world state is stored |

Identifiers differ by case and context: load selections commonly use cow, uni and bscout; runtime data names include Uni and Velvet. Record actual values at each layer rather than lowercasing everything indiscriminately.

## GFS: begin with a read-only index

The inspected Reverge Package File version is 1.1, with big-endian index values: an initial u32 supplies the data-region offset, followed by u64-length-prefixed strings and an entry count. Entries contain path, size and alignment. Advance data offsets according to each entry's alignment; content does not simply begin after the filename.

Validate version, index bounds, safe integer ranges, entry/string limits, nonzero alignment, entry ranges within the file and non-overlap between index and data. Repacking must preserve path, content and alignment semantics, with byte-for-byte comparisons of untouched entries.

The [read-only index example](../../examples/read_gfs_index.py) reads directory information only: it does not extract, execute or modify entries. It illustrates the sampled format, not a universal GFS library. Never use it to “repair” an unknown version.

## TFHRES and caches

The inspected resources_prod/lobbymaps_prod samples expose SQLite schemas including cached_textfile, cached_image and filemap_record. They offer clues about logical names, source paths and cached text/images. Open read-only and inspect the schema first; do not edit every table. Velvet Beautifier's TFHResource management shows backup, clone, Upsert and save steps (S2).

A cached path does not prove that editing the original disk file will affect the next load: a packaged or cached version may still win. Resource keys, development source paths and current reads are different things.

## template, temp and Scripts do not define priority by name

`temp/` can be part of a serialized resource's archive path, not a disposable temporary folder. `template` may be a referenced template or merely a development example. A `*.template.lua` can also be our own generation source while the generated Lua is what gets packed.

To establish execution:

1. Start at the current menu/XML/load key and record its exact logical reference.
2. Locate the entry in this build's archive index; compare the extracted copy with the entry hash.
3. Inspect `require`, initialization callbacks and resource lookup APIs, recording static references as candidates first.
4. Observe loads/calls read-only. If modification is necessary, back up first, add one unique lightweight diagnostic marker and verify when it is reached.
5. Remove the marker and check untouched entries/current installation hashes. Avoid changing multiple same-named copies simultaneously.

We have not established that “the template directory always contains the production scripts,” nor recovered every resource search order. Prove which copy loads from the actual call chain.

## Credit third-party tools without overstating dependence

Velvet Beautifier supplied important references for resource formats, archive modification/restoration, TFHRES and level installation. Later tools were not simply its “hidden character switch”: fighter load points, lifecycles, derived input fields, boss control and prediction isolation required separate investigation.

Do not omit upstream work or claim all runtime discoveries were already an upstream SDK. Link specific sources and licenses; do not distribute complete game archives. See [sources](../../SOURCES.en.md).
