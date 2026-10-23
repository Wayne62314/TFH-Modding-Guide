// Synthetic Frida surface only. No game/process/keyboard access.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function fixture() {
  const memory = new Map(), messages = [];
  let callbacks, detached = false;
  class Pointer {
    constructor(value) { this.value = value; }
    add(n) { return new Pointer(this.value + n); }
    equals(other) { return this.value === other.value; }
    isNull() { return this.value === 0; }
    toInt32() { return this.value | 0; }
    lookup() { if (!memory.has(this.value)) throw Error('Unmapped synthetic address'); return memory.get(this.value); }
    readPointer() { return new Pointer(this.lookup()); }
    readU8() { return this.lookup(); }
    readU32() { return this.lookup(); }
    readS32() { return this.lookup(); }
    readFloat() { return this.lookup(); }
    readU64() { const n = this.lookup(); return {toNumber: () => n, toString: () => String(n)}; }
    readUtf8String(n) { return String(this.lookup()).slice(0, n); }
  }
  const base = 0x10000000, scene = 0x20000000, mode = 0x21000000;
  const set = (address, value) => memory.set(address, value);
  [0x48,0x8b,0xc4,0x55,0x56,0x57,0x41,0x54,0x41,0x55,0x41,0x56].forEach((v,i) => set(base+0x189b7e0+i,v));
  set(base+0x2b0d1e8, scene); set(base+0x2b0cc33, 0);
  set(scene+0x2028, mode); set(mode+0x1e8, 1); set(scene+0x9e4, 10);
  set(scene+0xc48, 7); set(scene+0x9c4, 30);
  set(scene+0xaa8, 0); set(scene+0xab4, 3);
  function string(address, value) {
    set(address, value); set(address+16, value.length); set(address+24, 15);
  }
  for (let i=0; i<2; i++) {
    const actor=0x30000000+i*0x2000, data=0x40000000+i*0x2000, state=0x50000000+i*0x2000;
    set(scene+0xae0+(i?3:0)*8, actor); set(actor+0x88, i+1);
    set(actor+0xc50, data); set(actor+0xc58, state);
    string(data+0xb40, i?'Velvet':'Uni'); string(state+0x10, 'Stand');
    for (const [offset,value] of [[0x120,1000],[0xfc,i?-1:1],[0x1270,1],[0xc78,i?800:300],
                                [0xc7c,0],[0x128,0],[0x134,0]]) set(actor+offset,value);
  }
  const context = vm.createContext({
    Process: {getModuleByName: () => ({base: new Pointer(base)})},
    Interceptor: {attach(address, value) { callbacks=value; return {detach() {detached=true;}}; }},
    rpc: {exports: {}}, send: value => messages.push(value)
  });
  vm.runInContext(fs.readFileSync(path.join(__dirname,'observe_training.js'),'utf8'),context);
  function enter() {
    const invocation = {threadId: 1};
    callbacks.onEnter.call(invocation,[new Pointer(scene),new Pointer(1)]);
    return invocation;
  }
  function leave(invocation, advance=false) {
    if (advance) set(scene+0x9c4,memory.get(scene+0x9c4)+1);
    callbacks.onLeave.call(invocation);
  }
  return {memory,messages,set,base,scene,mode,enter,leave,context,detached:()=>detached,
          samples:()=>messages.filter(m=>m.event==='training_pre')};
}

test('captures pre-state only after a single real counter advance',()=>{
  const f=fixture(), call=f.enter(); f.leave(call,true);
  assert.equal(f.samples().length,1); assert.equal(f.samples()[0].counter,30);
  assert.equal(f.samples()[0].p1.name,'Uni');
});
test('no counter advance produces no sample',()=>{
  const f=fixture(); f.leave(f.enter()); assert.equal(f.samples().length,0);
});
test('ordinary local/online/unknown modes are all refused by this training sample',()=>{
  for(const mode of [0,1,2,11,99]) {
    const f=fixture(); f.set(f.scene+0x9e4,mode); f.leave(f.enter(),true); assert.equal(f.samples().length,0);
  }
});
test('prediction depth survives temporarily cleared global prediction flag',()=>{
  const f=fixture(); f.set(f.base+0x2b0cc33,1); const outer=f.enter();
  f.set(f.base+0x2b0cc33,0); const inner=f.enter();
  f.leave(inner); f.leave(outer,true); assert.equal(f.samples().length,0);
});
test('unpredicted nested update invalidates outer sample',()=>{
  const f=fixture(), outer=f.enter(), inner=f.enter();
  f.leave(inner); f.leave(outer,true); assert.equal(f.samples().length,0);
});
test('team mismatch is rejected',()=>{
  const f=fixture(); f.set(0x30000000+0x88,2); f.leave(f.enter(),true);
  assert.equal(f.samples().length,0); assert.ok(f.messages.some(m=>m.event==='read_error'));
});
test('stop detaches and suppresses later observations',()=>{
  const f=fixture(); f.context.rpc.exports.stop(); assert.equal(f.detached(),true);
  f.leave(f.enter(),true); assert.equal(f.samples().length,0);
});
