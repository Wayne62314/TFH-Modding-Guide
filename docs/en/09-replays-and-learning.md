# 09 · Replays, combo files and offline learning

[English index](../../README.en.md) · [中文原文](../09-replays-and-learning.md)

## Can replay files alone train an AI?

The investigated TFHR files expose both input streams. We have not established that they directly store every frame's positions, actions, resources and world objects. “Read buttons from a file” and “obtain state → action training pairs” are different tasks.

Our process is: parse action labels → replay normally in a matching game version → collect both sides' pre-update observations at a unified real-update entry → independently verify file inputs against actual inputs → export candidates → split by complete match. Direct collection of human-versus-CPU matches avoids saving a replay, but lacks file inputs as an independent answer; state that validation limitation.

## Validated TFHR v12 subset

This subset was checked against 20 local samples; it is not an official complete format:

- Header magic TFHR, u32 version 12; multibyte fields are little-endian.
- After a fixed header, the parser reads length-prefixed fighter names, unexplained fields and stage name, then both input streams.
- Each run record is 8 bytes: duration u8, direction u8, A/B/C/D u8 each, opaque u16.
- duration=0 ends the stream; nonzero duration expands to that many frames.
- Both expanded lengths must match, with cross-checks against a candidate header count and trailing count/sentinel.
- Preserve opaque fields; do not label them random seeds, timestamps or checksums without evidence.

All 20 samples passed these structural checks. Reject truncation at every position, invalid enums, out-of-bounds data and inconsistent tails. One match does not establish identical offsets in other versions.

## TFHC: matching container versions can embed different replay versions

New user recordings are TFHC v3 with embedded TFHR v12; run-length input and training settings are readable. Older teaching samples are also TFHC v3 but embed TFHR v5, which the current parser rejects. Checking only the outer TFHC version is insufficient.

Never/Always guard, infinite resources and dummy recovery settings are important experimental context, not properties of the moves. A file enabling infinite magic does not prove that its combo spends magic; constant resources under infinite replenishment do not establish zero cost. Record user confirmation separately from single-variable testing.

## Align the same causal instant

Reading each fighter's state inside its own input function mixes different stages of one frame. Prefer both fighters' pre-state at the same root-update entry, read actual action labels separately at the native input entry, and keep post-state for audit—not model input.

Find the update-counter/file-frame offset using several changing, unique input windows, then verify the entire segment record by record. Long neutral runs can falsely match. An offset is calibrated for that segment, not a constant for all replays.

We encountered scene-source inputs differing from final native inputs, correlated with copy-routing conditions. R8/source arguments cannot be called “raw replay input” without checking. Built-in combo playback can also have invalid/different root-entry source input while native input matches the file exactly. Keep such records as playback comparisons; do not weaken live-collection validation to admit them into training.

## Data-quality gates

Require exactly one counter advance, no prediction/nesting, complete fighter/resource/world-object observations, known input caller, consistent labels across repeated calls, no duplicate counters or scene-identity conflicts, and a complete final batch on stop. Missing values are not neutral actions. phase=7 is an empirical filter here, not a universal definition of “can act.”

Human demonstrations export only P1 human labels. CPU actions remain diagnostic, not expert demonstrations. A mode-0 source depends on user confirmation; it does not automatically identify replay versus CPU play. Two rounds from one session must not go on opposite sides of a train/validation split.

## Lessons from model iteration

Early models imitated directions/buttons frame by frame. Many frames are held or idle, so simply retaining the previous input has a high baseline. High matching with real input history dropped sharply when using the model's own history, revealing continuation without initiation.

Later experiments used event gating, state-only intent prediction, legal-edge rendering and facing-relative representations. Transform the entire history into the **current** self origin/current facing; do not use a different origin for each historical frame, or mirror already fighter-local vx_local twice.

After adding one human demonstration, Oleander direction matching on the same reused development set rose roughly 37.35% → 42.10%; full-action matching with self-generated input history rose 31.58% → 35.87%. Yet predicted new-press edges fell from 69 to 56, so rare attacks were not demonstrably solved. These are development results, not win rates or independent generalization evidence.

## What does “stress-test match rate” mean here?

World/fighter observations remain fixed to a replay. After a 15-frame warmup, input history comes from the model's predictions and subsequent outputs are compared. This exposes error accumulation better than always supplying true history. However, predicted actions **do not change the replay's next world state**, so this is not closed-loop fighting.

Shadow suggestions, 10-second direction control and sustained direction/attack control are separate later test levels. Validate suggestion age, disabling, side switching and actual attacks before discussing match strength. The more useful next direction is high-level learned choices plus reliable combo execution—not treating input match rate as the endpoint of a playable sparring partner.
