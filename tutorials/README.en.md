# Build a TFH mod, step by step

[中文教程](README.md) · [Research documentation](../README.en.md)

Set up a workspace and add a small tutorial that displays dialogue. Runtime hooks come later. Each lesson identifies where the code belongs, how to check it, and where our knowledge stops.

| Order | Exercise |
|---|---|
| 0 | [Set up a workspace and run the public source](en/00-start-here.md) |
| 1 | [Add a lesson to the tutorial menu](en/01-first-lesson.md) |
| 2 | [Extend a lesson into a dialogue-driven battle chapter](en/02-chapter.md) |
| 3 | [Load Huggles through Arizona and enable Oleander enhancement](en/03-hidden-boss.md) |
| 4 | [Read fighter/match properties and change a few known properties](en/04-properties.md) |
| 5 | [Write a hook that observes gameplay](en/05-hooks.md) |
| 6 | [Send commands and connect features to the UI](en/06-input-and-ui.md) |

The new `hello.lua`, candidate-package builder and training observer are teaching samples. Synthetic tests and syntax checks can run without the game. These newly assembled samples have **not been validated in-game**. Historical successes with Huggles or native input do not validate these new files; their original scope is recorded in the research chapters.

Obtain original game Lua/XML/resources from a copy you are authorized to access. No original archive is included. Runtime examples recognize only the documented EXE build. Stop when a check fails.
