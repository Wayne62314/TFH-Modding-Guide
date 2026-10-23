# 1 · Add a lesson to the tutorial menu

[Tutorial index](../README.en.md) · [中文](../zh/01-first-lesson.md)

This lesson displays two conversations and restores P1 health/resources between them. Establish the menu-to-script path before adding combat logic.

These new samples have not been playtested in-game. Their interfaces can be found in this build's tutorial libraries. Menu routing and the development-script slot follow our earlier standalone-lesson approach.

## Locate two entries

With the game closed, inspect your own data01/trials.gfs:

```powershell
$gameDir = Read-Host 'Game directory'
py -3.12 examples/read_gfs_index.py (Join-Path $gameDir 'data01/trials.gfs')
```

Find:

```text
Trials/01 basic.xml
Trials/training/input_testing.lua
```

The first is a basic-tutorial menu. The second is an existing development-test script slot borrowed by this sample. Its previous content is replaced in the candidate. Another mod using it will conflict; do not assume it is universally unused.

This builder changes existing entries only. Adding a completely new archive path requires index-growth and resource-lookup work that it does not implement.

## Read the lesson

Open [hello.lua](../../examples/lessons/hello.lua). The game supplies its required libraries. Do not copy Metas.lua declaration stubs into your mod as runtime implementations.

```lua
setMatchSettings(function()
  initTrial("cow", "cow")
  initSkipIntro()
end)
```

This registers initialization settings. cow is Arizona's internal loading identifier. Begin with ordinary fighters to reduce dependencies. initTrial is in this build's Trials/training/TrialLib.lua; the fullHeal wrapper is in Trials/Lib/LuaLib.lua.

```lua
setInit(function()
  startTrial()
  doRoutine(lesson)
end)
```

The initialization callback starts the lesson. Its waitForConvo calls need a yielding routine; do not move the whole body into an arbitrary non-yielding context. Do not assume wait(n) measures milliseconds.

Trainer is an existing dialogue channel. Expect its supported portrait; changing a speaker's name in text does not create artwork.

## Route the menu entry

Important attributes from [menu-entry.xml](../../examples/lessons/menu-entry.xml):

```xml
<Trial id="modAuthorHello" title="Mod author: hello"
       tutorial="trials/training/input_testing.lua"
       file="trials/training/input_testing.lua">
```

This is only the opening tag. The file contains complete, parseable XML. Keep the id unique and preserve observed reference casing. The builder inserts the complete Trial into the known m6Basics group and rejects a missing/ambiguous anchor.

## Prepare, without installing

```powershell
$gameDir = Read-Host 'Game directory'
py -3.12 examples/prepare_lesson.py (Join-Path $gameDir 'data01/trials.gfs') --expected-sha256 8e4a65f65ae2812c1a8bfd409f58827012b049935127170eb81b1d5913cec3f6 --output ..\TFH-Hello-local
```

Keep output outside the repository. This hash identifies the original archive checked during research. A mismatch produces no output; do not replace it with the hash of an unknown installation merely to bypass the check.

The builder changes menu/Lua entries, recalculates sizes/alignment and verifies every entry's content. Untouched entries must remain byte-identical. Output contains the original backup, candidate and manifest.json. An existing output directory is refused.

## Install and restore with hash checks

Make sure the game is closed and no other patch is being installed. Run from the guide repository:

```powershell
$gameDir = Read-Host 'Game directory'
$lessonOut = (Resolve-Path '..\TFH-Hello-local').Path
$manifest = Get-Content -LiteralPath (Join-Path $lessonOut 'manifest.json') -Raw | ConvertFrom-Json
$target = Join-Path $gameDir 'data01/trials.gfs'
$candidate = Join-Path $lessonOut 'trials.gfs.candidate'
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw 'Archive has other changes; stop' }
if ((Get-FileHash -LiteralPath $candidate).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw 'Candidate hash mismatch' }
Copy-Item -LiteralPath $candidate -Destination $target
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw 'Post-install hash mismatch' }
```

Start the game and find Mod author: hello in basic tutorials. Check menu visibility, dialogue on entry and a normal exit. If stuck, record the last dialogue and restore.

Close the game again before restoring. Use the same PowerShell session, or recreate the paths/manifest above:

```powershell
$backup = Join-Path $lessonOut 'trials.gfs.original'
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw 'Further changes detected; stop restoration' }
if ((Get-FileHash -LiteralPath $backup).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw 'Backup hash mismatch' }
Copy-Item -LiteralPath $backup -Destination $target
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw 'Post-restore hash mismatch' }
```

| Symptom | First checks |
|---|---|
| Builder refuses | Original hash, entry paths, XML group anchor |
| Menu entry absent | Correct game's candidate installed, duplicate/cached resources |
| Entry does nothing | tutorial/file routing, Lua encoding/syntax |
| Crash on entry | Restore ordinary fighters/original initialization first; pcall cannot catch native access violations |
