# 07 · Stalls, prediction branches and object lifetime

[English index](../../README.en.md) · [中文原文](../07-performance-and-prediction.md)

## Short scripts can still be expensive

Integrating phase 3 into ordinary matches initially caused severe stalls. Some low-level helpers, such as frequent memory-region queries, were much more expensive inside the actual game than isolated microbenchmarks suggested. Per-frame range queries, state-table scans, string/closure allocations and full logging multiply across fighters, children and prediction updates.

We moved expensive queries out of the routine frame path and cached them within a **scene + fighter instance + resource data + generation** scope. Expensive checks run on changes/cache misses; the normal path performs lightweight bounds comparisons. The user reported the stalls resolved, not a universal frame-rate guarantee on every machine.

## Caches need explicit invalidation

```text
New scene / actor / data / generation
    → clear old range, state-table, name and child-object caches
First lookup in this scope
    → verify ranges and identity; cache a bounded number of entries
Subsequent frames
    → lightweight bounds checks; invalidate on rebuild, exit or error
```

Readable/writable mapping only proves that memory remains mapped, not that it still contains the original object. Pool slots can be reused and parent pointers can expire. To find Fred, first identify live objects, then follow parents with a bound to confirm ownership. Never follow arbitrary pointers indefinitely.

State tables and strings have resource lifetimes too. Permanently caching a state address and reusing it after a fighter change/rematch is a classic cause of “worked initially, crashes later.”

## CPU work includes non-real updates

We observed AI prediction-related recursion and input calls. One outer update can perform substantial simulated work through code resembling real battle states/input. Treating every hook as a frame produces duplicate training examples, prediction contamination, false successful throw techs, repeated summons and accelerated clocks.

Isolation needs two layers:

- At the root update, check the prediction flag and track prediction depth so an inner recursion temporarily clearing the flag cannot leak through.
- At every input/contact callback, check the flag again: some prediction input calls may occur without a new root entry.

Also verify main scene, thread, update arguments, real-root depth, nesting and entry/exit counters advancing by exactly one. Rejected records are diagnostic, not fabricated neutral input or real frames.

## Reporting performance

Distinguish a single-API microbenchmark, complete hook duration, native scene-root wall time and user-perceived stalls. Root calls include the game's own work and prediction; not all elapsed time belongs to the collector. Conversely, a fast standalone-process benchmark does not establish in-game performance.

Record sample size, scene, object count, cache hits/invalidations, disk volume and user feedback. Label what p50/p95/p99 actually measure. Batch diagnostics, cap size/duration, detach normally after errors and flush the final batch.

## Do not restart a state every frame

Summoning, vortex and flight should be stateful requests: key edge → queue → confirm entry → wait for completion → restore. Calling “start summon” every frame can continually reset progress; repeated flag/state changes can trap a fighter in a reddish intermediate state.

Stopping a controller differs from undoing an already-entered native effect. Report that a restart is required when cleanup fails; do not force “restoration” through invalid objects. S1's scoped caches, controller and shutdown interfaces provide engineering examples.
