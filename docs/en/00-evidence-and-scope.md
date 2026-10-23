# 00 · What counts as knowing something?

[English index](../../README.en.md) · [中文原文](../00-evidence-and-scope.md)

## Evidence levels

| Level | What it supports | What it does not establish |
|---|---|---|
| File evidence | An archive or script contains a name, branch or configuration | That this path is currently executed |
| Static native evidence | A function in this build reads or writes a field | That the field means the same thing in every context |
| Read-only runtime observation | A value appeared at a particular object or call site | That changing it is safe or that it is the root cause |
| Single-variable experiment | A change produces a reproducible difference under stated conditions | That it works in other modes or with other characters |
| User playtest | The user confirmed a specific gameplay result | Coverage of every round, rematch and cleanup path |
| Integration/release validation | A package or integrated version passed specified checks | That unit tests prove full game compatibility |

These notes distinguish tested results, source-based inferences, candidates and unknowns. A historical “pending test” note may predate a later successful playtest. Conversely, an early success does not validate every module added afterward.

## Writing an evidence-backed claim

For each conclusion, record at least: executable hash, source type, mode and both characters, observation timing, intervention, result, limitations and the next test that could disprove it. Public reports should retain only fields needed for reproduction and remove process-absolute addresses, participant identifiers and local machine paths.

For example: “In free training on this build, with P1 Oleander, synchronizing base and derived buttons at the native input entry produced both an A in input history and an actual light attack.” This is more useful than “writing A worked”: it separates display from execution and identifies the intervention point.

## The project's most important counterexamples

- A visible character-select slot does not prove that confirming it loads the same fighter.
- An A in input history does not prove that attack processing received a complete button state.
- Reading back a flag does not prove that the entire boss behavior was ported.
- ThrowTech in a CPU prediction branch does not prove that the real match teched a throw.
- A state name in a `.foit` does not establish complete animation frames, child objects or exit paths.
- Readable/writable memory does not establish that an object belongs to this match or is the same generation.
- Successful file parsing does not prove that the resulting data is trainable or that a model can fight.
- Successful built-in playback does not prove that a custom input executor reproduces it.

## Scope

Research used owned game resources, public tool sources and user-authorized offline experiments. We have not reconstructed the complete engine source, all mode entries, all FOIT instructions, complete frame data or the network protocol. “The game has not updated in a long time” is not a substitute for a hash check.

See [sources](../../SOURCES.en.md). Private raw records are represented only by sanitized summaries, not fictitious public download links.
