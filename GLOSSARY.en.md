# Glossary

[English index](README.en.md) · [中文原文](GLOSSARY.md)

| Term | Meaning in these notes |
|---|---|
| P1/P2 | Fighter side/team context, not any arbitrary object numbered 0/1 |
| cow / uni / bscout | Observed internal fighter identifiers; distinguish UI names and differently cased data names |
| 5B / 2C / j.C | Numpad directional notation plus button: 5 neutral, 2 down, 6 forward, j airborne; not raw in-memory direction codes |
| state | Current native fighter action/state; its name is not an animation frame or cancel window |
| pre/post | Snapshots before/after the same update entry; model observations use pre, post is audit-only |
| scene | Scene object, not just visual background; also holds mode, fighters and internal dependencies |
| scope/generation | Lifetime identity for caches/operations; distinguishes different object generations at one address |
| RVA/VA | Module-relative address/current process virtual address; neither is a cross-build stable interface |
| hitstun/blockstun | Hit/block recovery restriction; cannot be inferred solely from HP loss or “opponent is attacking” |
| hitstop | Hit-freeze-related process; timing/input need testing, not equivalent to host sleep |
| node/sequence | Action node/named sequence, not necessarily a full fixed-frame recording |
| hit confirm | Choosing continuation after confirming a hit; avoid attribution errors from old hitstun, chip and separate projectiles |
| pressure sequence | Continued pressure after blocks; not necessarily gapless or automatically safe |
| true combo/true blockstring | Specific continuity preventing escape; no formal all-fighter proof was completed here |
| resource donor | Another normally loaded fighter supplying dependencies for diagnosis, not a completed independent port |
| shadow | Suggestions without input execution |
| teacher-forced | Evaluation supplied with real input history, potentially hiding accumulation of prediction errors |
| fixed-observation stress test | Model-generated input history while fighter/world observations stay fixed to replay; not closed-loop play |
| BC | Behavior cloning/supervised imitation; one sparring session does not automatically update the model |
| whitelist | Allowed modes/states, not proof that every item was tested or networking fully isolated |
