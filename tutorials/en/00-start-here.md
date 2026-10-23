# 0 · Set up the workspace

[Tutorial index](../README.en.md) · [中文](../zh/00-start-here.md)

You should recognize variables, functions and `if`. Python connects to the process; JavaScript inside Frida implements runtime hooks. Tutorial lessons use the game's Lua environment. Installing a standalone Lua interpreter does not make these lessons runnable from a terminal.

Commands below use Windows PowerShell. Close other mod tools and restore a known game baseline. File exercises can be done before starting the game.

## Clone two repositories

```powershell
git clone https://github.com/Wayne62314/TFH-Modding-Guide.git
git clone https://github.com/Wayne62314/TFHMOD.git
```

Keep the directories beside each other. `examples/...` refers to TFH-Modding-Guide; `ui/...` refers to TFHMOD. Create a branch in the relevant repository before editing, for example `git switch -c my-first-mod`.

The implementation reading baseline is `a630d5a8995527520beed628a778231d1eb95751`. Later commits can change documentation or implementation. For exact comparison, check out that commit in a clean copy. Avoid switching an uncommitted working directory back and forth.

## Use Python 3.12

From TFHMOD:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r ui/requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s ui/tests -p 'test_*.py'
```

The requirements pin the research Frida version. Resolve installation errors before proceeding; do not remove version pins just to get past pip. These tests do not establish compatibility with your game.

To open the existing UI from source:

```powershell
.\.venv\Scripts\python.exe ui/gui.py
```

Check that it opens. Before connecting, verify the EXE against the [supported build](../../docs/en/12-build-specific-reference.md):

```powershell
$gameDir = Read-Host 'Game directory'
Get-FileHash -LiteralPath (Join-Path $gameDir "Them's Fightin' Herds.exe") -Algorithm SHA256
```

The research EXE hash is `03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D`. Stop if it differs. GFS archives have independent hashes; a matching EXE does not establish unmodified archives.

## Files to recognize

| File | What to inspect |
|---|---|
| `ui/gui.py` | Backend process discovery, JS assembly, logs and configuration |
| `ui/launcher.py` | `find_game()` process/hash checks; an old CLI entry also remains here, so its old version constant does not identify the entire current UI |
| `ui/training-hook.js` | Pending Arizona-name replacement and enhancement application |
| `ui/phase3-native.js` | State interfaces, position sync, caches and game-thread work |
| `ui/phase3-controller.js` | Requests, waiting, timeout and recovery |
| `ui/i18n.py` | Chinese/English UI strings |

`gui.py` concatenates several JS files in order. Loading training-hook.js alone into Frida leaves missing functions and the `__BASE__` placeholder. Start with the complete existing flow before splitting modules.

## Check something without the game

From TFH-Modding-Guide:

```powershell
py -3.12 -m unittest discover -s examples -p 'test_*.py'
py -3.12 examples/read_gfs_index.py --help
```

If `examples` cannot be found, check your current directory. The next lesson uses the index reader to locate menu and script slots.
