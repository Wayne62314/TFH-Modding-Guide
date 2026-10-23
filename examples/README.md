# 两个不连接游戏的小示例

[English](README.en.md)

Python 3.10以上，无外部依赖：

```powershell
python -m unittest discover -s examples -p 'test_*.py'
python examples/input_edges.py
python examples/read_gfs_index.py --help
```

read_gfs_index.py只读指定GFS的索引，检查版本/边界/对齐，不提取或修改条目。实际文件由使用者自己提供；仓库测试仅用内存中构造的synthetic.txt样本，不含游戏资源。

input_edges.py演示ABCD四个物理按钮从up到press/held/release的合法转换，以及本研究方向反射表。不含原生派生字段写入、角色状态强切、游戏进程读取或SendInput实现，不能直接拿来作为完整MOD。

这7项测试证明示例的边界和合成逻辑，不等同于游戏兼容性/连段测试。
