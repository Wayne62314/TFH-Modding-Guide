# Two small examples that do not connect to the game

[English index](../README.en.md) · [中文原文](README.md)

Python 3.10 or newer; no external dependencies:

```powershell
python -m unittest discover -s examples -p 'test_*.py'
python examples/input_edges.py
python examples/read_gfs_index.py --help
```

`read_gfs_index.py` reads only the index of a user-supplied GFS. It validates version, bounds and alignment without extracting or modifying entries. Tests use an in-memory synthetic.txt sample, not game resources.

`input_edges.py` demonstrates legal up/press/held/release transitions for four physical ABCD buttons and the research direction-reflection table. It contains no native derived-field writes, fighter-state forcing, game-process reads or SendInput implementation. It is not a complete mod.

The seven tests validate example bounds and synthetic logic, not game compatibility or combo execution.
