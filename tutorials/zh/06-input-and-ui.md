# 6 · 发送指令，接到 UI

[教程目录](../README.md) · [English](../en/06-input-and-ui.md)

有两种可用线索。教程脚本里能找到运动输入接口；普通对战里，我们验证过私有原生输入副本。先把一招的执行弄明白，再做持续控制。

## 教程里的输入接口

在自己游戏包里看 `Trials/training/TestBed.lua`。这个文件把一串输入整理成 Lua 表，再交给 `sysInputMotion(Player1, ...)`。`p1Motion` 是那里定义的局部辅助函数，换一个文件未必能调用。

在自己的教程 routine 里，可以做这个待测小实验：

```lua
-- 这个调用形状来自 TestBed；新关卡里的效果要自己验证。
sysInputMotion(Player1, {DirN, BtnA, DirN})
```

观察是否真的出轻攻击，随后是否正常释放。一次列表项对应多少更新、输入在什么条件下被接受，应沿本构建实现和运行结果继续查，别先承诺精确帧数。

方向/按钮常量可以相加，例如现有脚本使用 `DirF + BtnA`。它们属于该 Lua 输入接口。内存输入结构里的方向码是另一套表示，`DirF` 不能直接当作字节写进去。

## 普通训练的原生输入

本构建已确认的调用点在 RVA `0x1775820`，后面的返回位置为 `0x1775825`。在这里观察到 RCX 是 actor，RDX 指向输入。它位于函数内部的调用指令处，不能把函数入口 `args` 的说明不加区分地套过来。

下面是流程摘录，依赖项故意保留名字。这份指南没有附完整的原生输入注入器；只粘这一段无法运行：

```javascript
// 已通过版本、调用点、真实更新、P1、焦点和模式检查之后。
Memory.copy(inputCopy, original, 0x50);
inputCopy.writeU8(screenDirection);
applyDerivedButtonChannels(inputCopy, rawButtons);
this.context.rdx = inputCopy;
```

`inputCopy` 是保持存活的私有内存。`original` 来自当前调用的 RDX。`applyDerivedButtonChannels` 是你需要根据本构建聚合规则实现的适配器，这里没有提供实现。它要同时写 ABCD 基础通道、别名和聚合通道。缺掉后两部分，输入历史可能显示 A，人物却不攻击。

研究期实际输入执行器已经测通过，但完整执行器没有放进这个公开指南。这里提供已发现的布局、合成边沿示例和接入流程；要独立重写，仍须做手动输入对照。

## 按钮要有边沿

原始状态：0 新按下，3 保持，1 松开，4 未按。单次 A 的基础通道应经历：

```text
更新 n：   [0,4,4,4]
更新 n+1： [1,4,4,4]
更新 n+2： [4,4,4,4]
```

这只是 ABCD 基础状态，不包含派生字段。运行 [input_edges.py](../../examples/input_edges.py) 看布尔目标输入怎么变成合法边沿。已校准别名 A=[3,19,25]、B=[4,20,26]、C=[5,18,24]、D=[6,17,23]；9..14 的聚合规则有阈值和优先级，需对照本构建函数 `0x1747110`。

同一真实计数的重复输入回调应得到同一份输入。下一计数才推进 press/held/release。一个全局 inputCopy 也不能被其他线程或递归调用同时覆盖。

## 换边时怎么拉后

用 actor+0xfc 的当前朝向。面向右时，原始方向 4 为左，作为后方向；面向左时，后方向变成 0。蹲后对应 3 或 1。完整反射表是 `[4,3,2,1,0,7,6,5,8]`。

当时两侧方向实验都通过了。人物正在转身时仍要读当前值，别只在接管开始读一次。相对方向转换后，原始字节才写进输入结构。

## 从一次 A 开始验

先禁用自动决策，让人工触发一次 A。对手站着不动。输入历史有 A 之后，还要看到本体做轻攻击。接着试 B/C/D 和同时 B+C；拆投需在原生规则允许的窗口里发生，单纯显示 B+C 不算拆投成功。

持续控制要补指令年龄、超时和松键。手动输入、失焦、暂停和模式改变应该取消接管。某些释放需要等下次有效输入回调；停止时仍有 release pending 就报告出来，不伪装成已经清干净。

## 接 UI 的一个小练习

先别加新钩子，可以在现有界面给熊替换换一个显示名称，跟一遍配置流：

1. `gui.py` 的 `BooleanVar` 和复选框取值，经 `options()` 形成字典。
2. Backend 串行队列把配置交给 JS 的 `rpc.exports.configure`；连接前配置还会写入初始 options，避免加载时短暂启用默认功能。
3. `training-hook.js` 检查布尔类型，再交给对应模块。

真要新增 `myFeature`，需要在这些位置都增加字段，并给 `i18n.py` 补英文。只加一个复选框不会改变游戏。新选项默认关；读到它的模块缺失就报错。看看现有 `tianNova`，未成功的功能会被拒绝启用。

源码测试可从 TFHMOD 目录运行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s ui/tests -p 'test_*.py'
node --test ui/tests/*.test.cjs
```

Windows 终端如果不展开 Node 的通配符，用 PowerShell 遍历后逐个运行：

```powershell
Get-ChildItem ui/tests -Filter '*.test.cjs' | ForEach-Object { node --test $_.FullName; if ($LASTEXITCODE -ne 0) { throw 'JS test failed' } }
```

需要便携包时读 `ui/build_ui.ps1` 和 `ui/package_ui.py`，它们有实际构建依赖。先按脚本参数做本地构建，再从全新目录解压测试，保留 `_internal`。本轮文档更新没有生成新的 MOD 发行包。
