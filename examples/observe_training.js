'use strict';
// New teaching implementation of observed interfaces; NOT yet live-playtested.
// Training only. No writes, NativeFunction calls or input substitution.
const base = Process.getModuleByName("Them's Fightin' Herds.exe").base;
const signature = [0x48,0x8b,0xc4,0x55,0x56,0x57,0x41,0x54,0x41,0x55,0x41,0x56];
for (let i = 0; i < signature.length; i++) {
  if (base.add(0x189b7e0 + i).readU8() !== signature[i]) {
    throw Error('Unsupported or occupied update hook; restart without other tools');
  }
}
const threads = new Map();
let enabled = true;
let errors = 0;
function readString(object) {
  const size = object.add(16).readU64().toNumber();
  const capacity = object.add(24).readU64().toNumber();
  if (!Number.isSafeInteger(size) || !Number.isSafeInteger(capacity) ||
      size < 0 || size > 128 || capacity < size) throw Error('Invalid string');
  return (capacity < 16 ? object : object.readPointer()).readUtf8String(size);
}
function fighter(scene, slotOffset, side) {
  const slot = scene.add(slotOffset).readS32();
  if (slot < (side === 1 ? 0 : 3) || slot > (side === 1 ? 2 : 5)) throw Error('Invalid slot');
  const actor = scene.add(0xae0 + slot * 8).readPointer();
  if (actor.isNull() || actor.add(0x88).readFloat() !== side) throw Error('Invalid team');
  const data = actor.add(0xc50).readPointer();
  const state = actor.add(0xc58).readPointer();
  if (data.isNull() || state.isNull()) throw Error('Missing fighter data/state');
  const hp = actor.add(0x120).readFloat();
  const facing = actor.add(0xfc).readFloat();
  if (!Number.isFinite(hp) || ![1, -1].includes(facing)) throw Error('Invalid fighter values');
  return {
    side, name: readString(data.add(0xb40)), state: readString(state.add(0x10)),
    generation: actor.add(0x1270).readU64().toString(), hp, facing,
    x: actor.add(0xc78).readS32(), y: actor.add(0xc7c).readS32(),
    superRaw: actor.add(0x128).readFloat(), magicRaw: actor.add(0x134).readFloat()
  };
}
const hook = Interceptor.attach(base.add(0x189b7e0), {
  onEnter(args) {
    this.tracked = false;
    if (!enabled || (args[1].toInt32() & 255) !== 1) return;
    const scene = args[0];
    if (!scene.equals(base.add(0x2b0d1e8).readPointer())) return;
    let t = threads.get(this.threadId);
    if (!t) { t = { depth: 0, prediction: 0, active: null }; threads.set(this.threadId, t); }
    this.t = t;
    this.tracked = true;
    this.predicted = t.prediction > 0 || base.add(0x2b0cc33).readU8() !== 0;
    if (this.predicted) { t.prediction++; return; }
    t.depth++;
    this.owner = t.depth === 1;
    if (!this.owner) { if (t.active) t.active.nested = true; return; }
    t.active = null;
    try {
      const mode = scene.add(0x2028).readPointer();
      if (scene.add(0x9e4).readU32() !== 10 || mode.isNull() ||
          mode.add(0x1e8).readU8() !== 1 || scene.add(0xc48).readU32() !== 7) return;
      const counter = scene.add(0x9c4).readU32();
      if (counter % 30 !== 0) return;
      t.active = { scene, counter, nested: false, row: {
        event: 'training_pre', counter, mode: 10, phase: 7,
        p1: fighter(scene, 0xaa8, 1), p2: fighter(scene, 0xab4, 2)
      } };
    } catch (error) {
      if (++errors <= 3) send({event: 'read_error', message: String(error)});
      if (errors >= 3) enabled = false;
    }
  },
  onLeave() {
    if (!this.tracked) return;
    const t = this.t;
    if (this.predicted) { t.prediction--; return; }
    t.depth--;
    if (!this.owner) return;
    const a = t.active;
    t.active = null;
    if (!a || a.nested || !enabled) return;
    try {
      if (!a.scene.equals(base.add(0x2b0d1e8).readPointer()) ||
          base.add(0x2b0cc33).readU8() !== 0 ||
          a.scene.add(0x9e4).readU32() !== 10 || a.scene.add(0xc48).readU32() !== 7) return;
      if (((a.scene.add(0x9c4).readU32() - a.counter) >>> 0) === 1) send(a.row);
    } catch (error) {
      enabled = false;
      send({event: 'read_error', message: String(error)});
    }
  }
});
rpc.exports = { stop() { enabled = false; hook.detach(); threads.clear(); return { stopped: true }; } };
send({event: 'ready', readOnly: true, mode: 10, phase7IsEmpirical: true,
      sampleEveryCounters: 30, liveValidation: 'pending'});
