# 11 · Engineering, testing, releases and publication boundaries

[English index](../../README.en.md) · [中文原文](../11-testing-packaging-and-publication.md)

## Roll back the two modification paths separately

**Resource patches:** with the game closed, back up target archives and record pre-install/candidate/post-install hashes. Edit only required entries; compare untouched content byte for byte. Refuse to overwrite unknown later modifications. Uninstall multiple patches in reverse dependency order; an earliest backup must not blindly overwrite later changes.

**Runtime tools:** verify hash/signatures before hooking; check scene, fighter, thread and generation; provide time limits and manual stop. Detaching does not undo every gameplay effect. UI should explain when toggles apply and when reload/restart is required.

## Describe mode whitelists accurately

Historical tools used both broad “0..14 excluding 1/11” rules and narrower character-tool rules limited to 0 or training combinations. **Neither is a per-mode playtest matrix.** Later name mapping identified 11 as LEADERBOARD; an old comment calling it online was inaccurate. Conservative rejection may remain, but documentation must correct the meaning.

Excluding a mode number is not complete network isolation. Connections, rollback, prediction, replays and local scenes are not fully reconstructed. Publish the smallest validated scope; close the tool and restart before online play.

## Test matrix

| Dimension | Minimum checks |
|---|---|
| Archive edits | Index bounds, safe paths, alignment, untouched entries, restored hashes |
| Native interfaces | Wrong-build rejection, signatures, nulls, scene/team, generation, exit |
| Input | Original buffer unchanged, derived fields, press/held/release, simultaneous buttons, repeat callbacks |
| State control | Startup, waiting, hit/interruption, timeout, repeated summons, destruction/rematches |
| Modes | Training/local CPU/two-player tested separately; reject unknown/online |
| Data | Prediction exclusion, same-frame pre-state, alignment, deduplication, tail flush, whole-match splits |
| UI | Async connection, language switching, unsuccessful features disabled, stop/error messages |
| Packaging | New directory, non-ASCII/space paths, no global Python/Tk, full extraction, self-check |

Simulated tests cover boundaries, not the real game. Distinguish standalone-module playtests, integrated regression and fresh-machine compatibility in release notes.

## GUI and shareable packages

We separate Python connection/logging from JS gameplay hooks. The UI works asynchronously rather than blocking its main thread on process queries. Language switching should change text only—not silently modify options, reconnect or enable features. Document conflicts involving function keys, U pause and Y cleanup.

Early Setup/Start scripts depended on local Python/Frida and failed after relocation. Later PyInstaller packages bundled Python, Frida, Tcl/Tk and other runtime dependencies. Preserve the whole `_internal` directory, not just the EXE. GitHub's automatic Source code ZIP is not the portable app.

Extract portable tools to a separate writable directory; the game folder is unnecessary. Use a new directory for each version instead of mixing old files. Include sources, dependency licenses, checksums and a bug-report format. Do not recommend disabling security software for unsigned-tool warnings.

## Performance and recovery are acceptance criteria

Test more than transformation or attacks: loss of focus, pause, return of control, round end, repeated rematches, key releases, log limits and process exit matter. A working feature that blocks for many milliseconds each frame is still unsuitable for release.

Design shutdown as cleanup request → attempt in the correct thread/context → confirm completion or report pending. Do not destroy game objects from the wrong thread for an “instant exit.”

## Privacy and asset checklist

Generate a new public repository from an allowlist. Do not delete a few private files and change repository visibility: Git history can retain data. Exclude credentials, raw replays/player names/accounts, local paths/process addresses, dumps, full GFS/FOIT/textures, original-package backups and unauthorized assets.

Suitable public material includes original explanations, synthetic examples, verifiable build hashes/RVAs, reviewed statistics, public-source links and failed conclusions. Tools depending on external game assets should distribute patches/scripts/installers, not entire game packages. A public repository does not license third-party assets automatically.
