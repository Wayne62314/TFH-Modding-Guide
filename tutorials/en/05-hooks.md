# 5 · Write an observation hook

[Tutorial index](../README.en.md) · [中文](../zh/05-hooks.md)

A hook inserts your handling when execution reaches a location. Record a normal call before changing arguments. The accompanying files are a [Python connector](../../examples/observe_training.py) and [JS observer](../../examples/observe_training.js).

They are new teaching code with offline checks; live validation is pending. Historical research-observer successes do not validate these new files.

## Python's role

observe_training.py resolves the selected PID's EXE, verifies its filename/hash, then attaches. --help works without Frida; actual attachment requires it.

The essential calls are:

```python
session = frida.attach(args.pid)
script = session.create_script(source)
script.on('message', on_message)
script.load()
```

on_message represents your callback; the full file uses a printing lambda. script.load() executes top-level JS, installing hooks that then wait for game calls. JS send({...}) returns messages here; it does not automatically execute PowerShell.

## JavaScript inside Frida

```javascript
const base = Process.getModuleByName("Them's Fightin' Herds.exe").base;
```

Use the current loaded base plus RVA, not an earlier process's absolute address. The full example checks bytes at 0x189b7e0 before hooking. Another tool occupying the site may cause rejection; restart without it rather than deleting checks.

This simplified shape explains callbacks. It lacks build/mode safeguards and must not be loaded alone:

```javascript
Interceptor.attach(base.add(0x189b7e0), {
  onEnter(args) {
    this.scene = args[0];
    this.before = this.scene.add(0x9c4).readU32();
  },
  onLeave() {
    const after = this.scene.add(0x9c4).readU32();
    if (((after - this.before) >>> 0) === 1) {
      send({event: 'one_update', before: this.before, after});
    }
  }
});
```

this stores invocation-local state. Every function entry is not a new frame. The actual sample checks the main scene/update argument, tracks recursion by thread, and carries prediction depth across inner calls temporarily clearing the flag. It captures both fighters at entry and audits the counter at exit before sending the entry snapshot.

## Add one observation

Run the observer and inspect training_pre. Then add a known field to fighter()'s returned object, for example:

```javascript
superMaxRaw: actor.add(0x12c).readFloat(),
```

Keep object commas valid. Restart the observer and compare against training settings. Stable numbers alone are insufficient; consistently reading the wrong field also looks stable.

For a new function, establish its signature from actual Lua bindings/call sites. A pointer-looking x64 argument does not establish an actor. NativeFunction additionally needs correct return/argument types; a wrong declaration can crash beyond what ordinary JS try/catch can reliably recover.

## Queue a one-time modification

Let RPC register only a request, such as pending = {kind: 'lower_hp_once', scope: ...}. Revalidate identity inside a verified game-update callback, then apply lesson 4's one-time write. Consume/clear the request; invalidate on scene change, timeout or manual stop.

Do not call fighter-state methods directly from the RPC thread. Public gui.py likewise requests shutdown and waits for game-thread handling, sometimes receiving pending.

## Detach

The full observer retains its hook and exposes RPC stop() to detach it. The connector attempts stop in finally, then detaches the session. Keep an explicit exit path in your own tools.

Read-only observation does not undo another tool's effects. If you add state/resource modifications, detachment does not establish complete restoration.

| Problem | Checks |
|---|---|
| ready but no snapshots | Ordinary training, empirical phase 7, genuinely unpaused |
| read_error | Slots/team/string layout; this sample stops sampling after three read errors |
| Many repeats in one frame | Root recursion/prediction; callback count is a bad clock |
| Stalls while enabled | Avoid full resource scans/logs every frame; this example samples intermittently |
