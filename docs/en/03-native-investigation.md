# 03 · Tracing native behavior from Lua interfaces

[English index](../../README.en.md) · [中文原文](../03-native-investigation.md)

## Minimal investigation order

Start with a falsifiable question, such as “At which stage is P1's pending fighter name read?” rather than collecting addresses and changing values.

1. Collect build hashes, archive indexes, fighter/state names and script calls.
2. Observe the normal flow read-only; record mode, caller RVA, object type and entry/exit timing.
3. Compare ordinary and target fighters, and ordinary training versus local CPU.
4. Find the smallest lifecycle point enclosing the required operation.
5. Perform a single-variable runtime experiment with build, function-signature and context checks.
6. Ask the user to verify actions, assets, input and cleanup—not just a write readback or log line.

## Disk bytes may differ from effective running code

At some investigated locations, disk bytes could not directly be analyzed as the effective instructions during normal execution. We used read-only ReadProcessMemory on the loaded module, after checking the build hash, then disassembled those bytes. This does not establish the same behavior at every location/build, and does not require publishing complete code dumps.

The PE exception directory can help locate non-leaf function boundaries. Without a boundary record, use small, bounded reads. Cross-check string references, Lua binding wrappers, RTTI/vtables and known call sites rather than trusting decompiler variable names alone.

Keep VA and RVA distinct: documents/logs retain module-relative RVAs; runtime addresses are loaded base plus RVA. Under ASLR, never reuse a previous run's absolute address. An RVA is still build-specific.

## C++ strings are not arbitrary UTF-8 buffers

Several strings in this build exhibit the MSVC small-string layout: length at +16, capacity at +24; capacity below 16 indicates inline content, otherwise the first field points to heap storage. Check length, capacity and bounds before reading. Prefer a verified native assignment path when writing; do not insert a new C-string pointer into a complex object.

This layout was validated for specific objects/wrappers, not promised for every std::string implementation. Writable memory does not establish correct allocator, ownership, terminator or destruction behavior.

## Read-only observation versus modification

Frida Interceptor can observe arguments, returns and context; NativeFunction can call located native functions (S3). Installing observation hooks is still dynamic instrumentation: do not advertise it as “no injection whatsoever.” Here, “read-only collection” means no input replacement, gameplay-state writes or mutating game-function calls.

For modifications, identify the exact kind: pending load-string replacement, boss flag, native state queue or private input copy. Their stopping and rollback semantics differ. Do not call game methods from an unknown thread, prediction update or half-initialized object.

## Turning crashes into evidence

One hidden-character tutorial crash was an access violation: a scene child pointer was null, then dereferenced at +0x60. That supports a missing/invalid scene dependency, not naming the child “texture” or “fighter resource” without more evidence. An early preload attempt still crashed, disproving the assumption that missing preload was necessarily the sole cause.

Keeping the original tutorial initialization and adding only minimal fighter configuration narrowed the variables. Null-pointer offsets, the final log message and whether a Lua message appeared all need context. Scanning stack memory for addresses is not a reliably unwound call stack; Lua pcall cannot catch a native access violation.

## Combine guardrails

EXE hash → function-byte signature → scene mode → caller/thread → fighter slot/team → object generation/data identity → bounds → phase → one-shot/time limit → readback and observation. No single check alone makes an operation safe.

A readable/writable stale pointer is especially deceptive. Identity should bind at least scene, actor, data, generation and side. Invalidate on scene change, rematch or resource reconstruction. See [chapter 07](07-performance-and-prediction.md).
