# 6 · Send commands and connect the UI

[Tutorial index](../README.en.md) · [中文](../zh/06-input-and-ui.md)

Two investigated paths are useful: motion input in tutorial scripts, and private native-input copies in ordinary battles. Understand one actual attack before attempting sustained control.

## Tutorial input

Inspect Trials/training/TestBed.lua in your own game archives. It assembles input into a Lua table and calls sysInputMotion(Player1, ...). p1Motion is a local helper there; another file may not have it.

Inside your tutorial routine, try this pending-validation experiment:

```lua
-- Call shape observed in TestBed; verify behavior in the new lesson.
sysInputMotion(Player1, {DirN, BtnA, DirN})
```

Check an actual light attack and subsequent release. How many updates each list item occupies, and when input is accepted, require tracing/testing in this build; do not promise exact frames yet.

Existing scripts combine constants, for example DirF + BtnA. Those constants belong to the Lua motion API. Raw native direction bytes use a separate representation; do not write DirF directly into that structure.

## Native input in ordinary training

The verified call instruction is RVA 0x1775820, returning to 0x1775825. RCX was observed as actor, RDX as input. This is a mid-function call instruction, so do not blindly apply function-entry args conventions.

This dependency-bearing excerpt illustrates the flow. The guide does not include a complete native-input injector; pasting it alone will not run:

```javascript
// After build/site/real-update/P1/focus/mode validation.
Memory.copy(inputCopy, original, 0x50);
inputCopy.writeU8(screenDirection);
applyDerivedButtonChannels(inputCopy, rawButtons);
this.context.rdx = inputCopy;
```

inputCopy is retained private memory; original is the current call's RDX. applyDerivedButtonChannels is an adapter **you must implement** using this build's aggregation rules; no implementation is supplied here. It must write ABCD base channels, aliases and aggregates. Missing the latter fields can display A without producing an attack.

The research executor passed gameplay tests, but its complete implementation is not published in this guide. We provide discovered layouts, synthetic edges and the integration path. An independent implementation still needs manual-input comparisons.

## Buttons need edges

Raw states: 0=new press, 3=held, 1=release, 4=up. A single A's base channels should follow:

```text
update n:   [0,4,4,4]
update n+1: [1,4,4,4]
update n+2: [4,4,4,4]
```

These are only base ABCD states. Run [input_edges.py](../../examples/input_edges.py) to see Boolean targets rendered into legal edges. Calibrated aliases: A=[3,19,25], B=[4,20,26], C=[5,18,24], D=[6,17,23]. Aggregate channels 9..14 have thresholds/priorities; inspect this build's 0x1747110 implementation.

Repeated callbacks for one real counter need identical input. Advance edges only on the next counter. One global inputCopy must not be overwritten concurrently by another thread or recursive consumer.

## Hold back after switching sides

Read current facing at actor+0xfc. Facing right: raw direction 4=left is back. Facing left: back becomes 0. Down-back is 3 or 1 respectively. Full reflection is [4,3,2,1,0,7,6,5,8].

Both-side direction tests passed historically. Read current facing during turns, not just when control begins. Convert relative direction before writing the raw byte.

## Validate one A first

Disable automatic decisions and manually trigger one A against a stationary opponent. After seeing A in input history, confirm the body actually attacks. Then test B/C/D and simultaneous B+C. A throw tech must occur within native eligibility; displayed B+C alone is insufficient.

Sustained control needs command-age limits, timeout and release handling. Manual input, lost focus, pause and mode changes should cancel. Some releases must wait for the next valid input callback; report release pending rather than claiming cleanup completed.

## A small UI exercise

Start by renaming the existing bear option without adding hooks, then follow configuration:

1. gui.py collects BooleanVar/checkbox values into options().
2. A serialized Backend queue passes them to JS rpc.exports.configure. Initial options are also configured before load to avoid briefly enabling defaults.
3. training-hook.js validates Boolean types and forwards settings to modules.

A real myFeature needs fields at all those points plus English strings in i18n.py. A checkbox alone has no gameplay effect. Default new options off; fail when their adapter is missing. Existing tianNova illustrates refusal to enable an unsuccessful feature.

From TFHMOD, run source tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s ui/tests -p 'test_*.py'
node --test ui/tests/*.test.cjs
```

If Windows does not expand Node's glob, enumerate in PowerShell:

```powershell
Get-ChildItem ui/tests -Filter '*.test.cjs' | ForEach-Object { node --test $_.FullName; if ($LASTEXITCODE -ne 0) { throw 'JS test failed' } }
```

For portable builds, inspect ui/build_ui.ps1 and ui/package_ui.py for their actual dependencies/arguments. Build locally, extract into a fresh directory and retain _internal. This documentation update does not create a new mod release package.
