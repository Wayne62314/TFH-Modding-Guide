# Running the examples

[English index](../README.en.md) · [中文原文](README.md)

Index/synthetic-input examples require Python 3.10+ without external dependencies. The training observer uses Python 3.12 and TFHMOD's pinned Frida dependency. See the [hands-on tutorials](../tutorials/README.en.md) for connection steps.

```powershell
python -m unittest discover -s examples -p 'test_*.py'
python examples/input_edges.py
python examples/read_gfs_index.py --help
```

`read_gfs_index.py` reads only the index of a user-supplied GFS. It validates version, bounds and alignment without extracting or modifying entries. Tests use an in-memory synthetic.txt sample, not game resources.

`input_edges.py` demonstrates legal up/press/held/release transitions for four physical ABCD buttons and the research direction-reflection table. It contains no native derived-field writes, fighter-state forcing, game-process reads or SendInput implementation. It is not a complete mod.

`prepare_lesson.py` reads a user-supplied GFS and outputs a backup, candidate and manifest, without installing. Use the original hash specified in [lesson 1](../tutorials/en/01-first-lesson.md), keep output outside the repository and never upload the candidate. `lessons/hello.lua` and menu XML are original teaching content requiring game libraries.

`observe_training.py` loads `observe_training.js` for read-only sampling in ordinary training on the specified build. It dynamically instruments execution, without gameplay-field writes or submitted input. Live validation of the new samples is pending.

```powershell
node --check examples/observe_training.js
node --test examples/test_observer.cjs
```

Python tests cover synthetic indexes, input edges and candidate repacking. Node tests use fictional memory/Frida surfaces for counter, mode, prediction and stop checks. Tests do not connect to the game; pass counts do not establish game compatibility.
