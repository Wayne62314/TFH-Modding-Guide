# 示例怎么跑

[English](README.en.md)

索引和合成输入示例用 Python 3.10 以上，无外部依赖。训练观察器用 Python 3.12 和 TFHMOD 固定的 Frida 依赖。具体连接步骤见[动手教程](../tutorials/README.md)。

```powershell
python -m unittest discover -s examples -p 'test_*.py'
python examples/input_edges.py
python examples/read_gfs_index.py --help
```

read_gfs_index.py只读指定GFS的索引，检查版本/边界/对齐，不提取或修改条目。实际文件由使用者自己提供；仓库测试仅用内存中构造的synthetic.txt样本，不含游戏资源。

input_edges.py演示ABCD四个物理按钮从up到press/held/release的合法转换，以及本研究方向反射表。不含原生派生字段写入、角色状态强切、游戏进程读取或SendInput实现，不能直接拿来作为完整MOD。

`prepare_lesson.py` 读取使用者自己的 GFS，输出原包备份、候选包和 manifest，不安装。使用[第一课](../tutorials/zh/01-first-lesson.md)指定的原包哈希，输出放仓库外，别把候选包上传。`lessons/hello.lua` 和菜单 XML 是新写的教学内容，需要游戏库才能运行。

`observe_training.py` 加载 `observe_training.js`，在指定构建的普通训练里只读采样。它安装动态观察钩子，不修改玩法字段，不发送指令。新示例游戏内验证待完成。

```powershell
node --check examples/observe_training.js
node --test examples/test_observer.cjs
```

Python 测试覆盖合成索引、输入边沿和候选包重排。Node 测试使用虚构的内存和 Frida 接口，检查计数、模式、预测与停止。测试过程不连接游戏，不能用通过数量代替兼容性验收。
