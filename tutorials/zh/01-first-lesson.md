# 1 · 给教程菜单加一关

[教程目录](../README.md) · [English](../en/01-first-lesson.md)

这关只弹两次对话，中间给 P1 回血和补资源。先把菜单到脚本的路径接通，攻击判定留到后面。

这组新示例还没做游戏内测试。用到的接口可以在本构建原教程库里找到。菜单路径和开发脚本槽位沿用我们之前做独立关时的方案。

## 找出要改的两项

游戏关闭后，读取自己的 `data01/trials.gfs`：

```powershell
$gameDir = Read-Host '游戏目录'
py -3.12 examples/read_gfs_index.py (Join-Path $gameDir 'data01/trials.gfs')
```

索引里找：

```text
Trials/01 basic.xml
Trials/training/input_testing.lua
```

第一个是基础教程菜单。第二个是本次借用的现有开发测试脚本槽位，原来的内容会被候选包替换。其他项目若已经占用了它，就会冲突；不要叫它“永远没人用的文件”。

这里只改现有条目。向归档增加全新路径会涉及索引增长、资源查找等问题，这个生成器没实现。

## 看一下关卡代码

打开 [hello.lua](../../examples/lessons/hello.lua)。开头的 `require` 由游戏提供。不要把包里的 `Metas.lua` 声明存根当运行库复制进来。

```lua
setMatchSettings(function()
  initTrial("cow", "cow")
  initSkipIntro()
end)
```

这段登记初始化设置。`cow` 是 Arizona 的内部加载标识。先用普通角色，减少依赖。`initTrial` 在本构建的 `Trials/training/TrialLib.lua` 里；`getP1():fullHeal()` 则能在 `Trials/Lib/LuaLib.lua` 找到包装实现。

```lua
setInit(function()
  startTrial()
  doRoutine(lesson)
end)
```

到初始化回调才启动课程。`lesson` 里有 `waitForConvo`，它需要能等待的 routine。别把整段搬到普通无等待上下文。`wait(n)` 的时间单位也别按毫秒猜。

`Trainer` 是已有对话通道。你会看到游戏原本支持的头像；改台词里的名字不会生成新头像。

## 菜单怎么指向它

[menu-entry.xml](../../examples/lessons/menu-entry.xml) 中的关键属性：

```xml
<Trial id="modAuthorHello" title="Mod author: hello"
       tutorial="trials/training/input_testing.lua"
       file="trials/training/input_testing.lua">
```

这只是标签开头，完整可解析的 XML 在文件里。`id` 保持唯一。路径大小写沿用已观察到的引用，不自行统一。生成器把完整 Trial 插进已知的 `m6Basics` 组。它找不到唯一锚点就报错。

## 生成候选，先别安装

```powershell
$gameDir = Read-Host '游戏目录'
py -3.12 examples/prepare_lesson.py (Join-Path $gameDir 'data01/trials.gfs') --expected-sha256 8e4a65f65ae2812c1a8bfd409f58827012b049935127170eb81b1d5913cec3f6 --output ..\TFH-Hello-local
```

输出目录放仓库外。这个包哈希来自当时核对过的原版，与你的文件不一致时不会输出。别为了过检查，把当前未知文件的哈希随手填进去。

生成器改菜单和 Lua 槽位，重新计算对齐与大小，再检查每项内容。其余条目要保持字节一致。目录里有原包备份、候选包和 `manifest.json`。输出目录已存在也会拒绝。

## 安装与恢复要带哈希

确认游戏已关闭，并且没有其他补丁在排队。下面从指南仓库目录运行：

```powershell
$gameDir = Read-Host '游戏目录'
$lessonOut = (Resolve-Path '..\TFH-Hello-local').Path
$manifest = Get-Content -LiteralPath (Join-Path $lessonOut 'manifest.json') -Raw | ConvertFrom-Json
$target = Join-Path $gameDir 'data01/trials.gfs'
$candidate = Join-Path $lessonOut 'trials.gfs.candidate'
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw '当前包有其他改动，停止' }
if ((Get-FileHash -LiteralPath $candidate).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw '候选校验失败' }
Copy-Item -LiteralPath $candidate -Destination $target
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw '安装后校验失败' }
```

启动游戏，在教程基础组找 `Mod author: hello`。检查菜单存在、进入能看到对话、结束能退出。卡住就记录最后一句台词，先恢复。

恢复时重新关闭游戏，在同一 PowerShell 会话运行；换过终端就重新设置上面的路径和 manifest：

```powershell
$backup = Join-Path $lessonOut 'trials.gfs.original'
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.candidate_sha256) { throw '安装后又有其他改动，停止恢复' }
if ((Get-FileHash -LiteralPath $backup).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw '备份校验失败' }
Copy-Item -LiteralPath $backup -Destination $target
if ((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $manifest.original_sha256) { throw '恢复后校验失败' }
```

| 现象 | 先查这里 |
|---|---|
| 生成器拒绝 | 原包哈希、两项路径、XML 组锚点 |
| 菜单没出现 | 候选是否真装到当前游戏、同名资源是否另有缓存 |
| 有菜单但点了没反应 | tutorial/file 指向的槽位、Lua 编码和语法 |
| 进场就崩 | 先恢复普通角色和原初始化；Lua pcall 接不住原生访问异常 |
