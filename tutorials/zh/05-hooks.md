# 5 · 写一个观察钩子

[教程目录](../README.md) · [English](../en/05-hooks.md)

钩子让你在函数经过某个位置时插入自己的处理。先记录一次正常调用，再考虑改参数。本文配套的是 [Python 连接器](../../examples/observe_training.py) 和 [JS 观察器](../../examples/observe_training.js)。

它们是新写的教学代码，做过离线检查，游戏内验证待完成。别把研究时期观察器的成功记录算到这份新文件头上。

## Python 这一侧做什么

`observe_training.py` 先用指定 PID 查 EXE 路径，核对文件名和 SHA256，再调用 `frida.attach`。Python 的 `--help` 不需要安装 Frida，真实连接才需要。

核心几行：

```python
session = frida.attach(args.pid)
script = session.create_script(source)
script.on('message', on_message)
script.load()
```

`on_message` 在这个摘录里表示你自己的回调，完整文件用 lambda 把消息打印出来。`script.load()` 会执行 JS 顶层代码，随后钩子才开始等游戏调用。JavaScript 的 `send({...})` 回到这里，不会自动执行 PowerShell。

## Frida 里的 JavaScript

```javascript
const base = Process.getModuleByName("Them's Fightin' Herds.exe").base;
```

用实际加载基址加 RVA。不要粘贴上一轮进程的绝对地址。完整例子安装前还检查 `0x189b7e0` 的字节签名。有其他工具先占了这段代码，检查可能失败；重启游戏清掉旧工具，别删检查。

理解回调可以先看这个简化形状。它没有版本/模式保护，不能单独拿去连接游戏：

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

`this` 保存当前这次调用的状态。不要把每次进函数都当新的一帧。实际例子检查主 scene 和更新参数，按线程跟踪递归；预测深度覆盖内部临时清标志的情况。入口时采双方状态，出口只审计计数，满足条件才把入口快照发出去。

## 怎样一步步加观察项

先运行现有观察器，看看 `training_pre`。接着在 `fighter()` 的返回对象里加一个你已验证的字段，例如：

```javascript
superMaxRaw: actor.add(0x12c).readFloat(),
```

注意对象里的逗号。重新启动观察器，改变训练设置做对照。数值应当与预期一起变化；读到了稳定数字还不够，可能只是稳定读错。

如果要观察某个新函数，先从实际 Lua 绑定和调用点确认签名。x64 下某个参数恰好看起来像指针，并不足以证明它是 actor。`NativeFunction` 还需要正确返回类型和参数类型；猜错会崩，不会被普通 JS try/catch 可靠救回来。

## 一次修改怎么挂上去

让 RPC 只登记请求，例如 `pending = {kind: 'lower_hp_once', scope: ...}`。在已经验证的游戏更新回调中重新核对身份，再执行第四课的单次写入。请求消费后清空；换场、超时、人工停止都作废。

不要在 Python 调 RPC 的线程里直接调用角色状态方法。公开 `gui.py` 的清理流程也是先请求 shutdown，等游戏线程处理，有时要返回 pending。

## 钩子关掉以后

完整观察器保留 `hook`，RPC `stop()` 调 `detach()`。连接器在 finally 里尝试 stop，再断开会话。新手写自己的工具也要保留这条退出路径。

只读观察不会主动撤销其他工具留下的效果。若你另外加过状态或资源修改，断开不代表恢复完成。

| 问题 | 看哪里 |
|---|---|
| ready 有了，快照没有 | 当前是否普通训练、phase 是否为经验值 7、有没有真的取消暂停 |
| read_error | 槽位、队伍、字符串布局；三次读取错误后本例停采 |
| 同一帧重复很多次 | 根调用递归和预测过滤；按 callback 次数计时很容易错 |
| 开着就卡 | 不要每帧扫描所有资源和写完整日志；这个例子只做间隔采样 |
