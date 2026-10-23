# 0 · 先把目录和环境弄好

[教程目录](../README.md) · [English](../en/00-start-here.md)

需要能看懂变量、函数和 `if`。Python 负责连接进程，Frida 里的 JavaScript 负责钩子。教程关卡用游戏自己的 Lua 环境。电脑装了 Lua，也不能在普通终端直接运行这些关卡。

下面使用 Windows PowerShell。先关闭其他修改器，游戏文件恢复到你确认过的原版。你可以先做文件练习，暂时不用启动游戏。

## 拉两份代码

```powershell
git clone https://github.com/Wayne62314/TFH-Modding-Guide.git
git clone https://github.com/Wayne62314/TFHMOD.git
```

两个文件夹放一起。以后看到 `examples/...`，从 `TFH-Modding-Guide` 目录找；看到 `ui/...`，去 `TFHMOD` 找。修改前自己开个 Git 分支，例如在对应仓库运行 `git switch -c my-first-mod`。

公开实现的阅读基线是 `a630d5a8995527520beed628a778231d1eb95751`。新提交可能只改文档，也可能改实现。需要严格对照时，在干净副本切到该提交。别在有未保存修改的目录里来回切。

## Python 用 3.12

在 `TFHMOD` 目录运行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r ui/requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s ui/tests -p 'test_*.py'
```

`requirements.txt` 固定了当时使用的 Frida 版本。pip 失败时先处理环境，别直接删依赖版本。上面的测试不证明你的游戏兼容。

想从源码开现有界面，可以运行：

```powershell
.\.venv\Scripts\python.exe ui/gui.py
```

先检查界面有没有打开。连接游戏前核对 EXE。对照 [支持构建](../../docs/12-build-specific-reference.md)，在你自己的游戏目录查 SHA256：

```powershell
$gameDir = Read-Host '游戏目录'
Get-FileHash -LiteralPath (Join-Path $gameDir "Them's Fightin' Herds.exe") -Algorithm SHA256
```

EXE 的研究哈希是 `03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D`。不一致就停。GFS 还有自己的哈希，EXE 相同也不能说明包没被改过。

## 先认识几个文件

| 文件 | 读它时看什么 |
|---|---|
| `ui/gui.py` | Backend 怎么查进程、拼接 JS、收日志、发送配置 |
| `ui/launcher.py` | `find_game()` 怎么检查进程和 EXE 哈希；文件里有旧命令行入口，先别照它的旧版本号判断整个 UI |
| `ui/training-hook.js` | Arizona 的待加载名在哪儿换，强化在哪儿设置 |
| `ui/phase3-native.js` | 状态接口、位置同步、缓存、线程上的工作 |
| `ui/phase3-controller.js` | 请求怎样等待、超时和恢复 |
| `ui/i18n.py` | 中英文界面文字 |

`gui.py` 会按顺序拼接多个 JS。单独把 `training-hook.js` 塞给 Frida 会缺函数，还会留下 `__BASE__` 占位符。先用完整启动流程跑通，之后再拆。

## 做一个不碰游戏的检查

在 `TFH-Modding-Guide` 目录运行：

```powershell
py -3.12 -m unittest discover -s examples -p 'test_*.py'
py -3.12 examples/read_gfs_index.py --help
```

如果终端提示找不到 `examples`，当前目录不对。下一课会用索引工具找菜单和脚本槽位。
