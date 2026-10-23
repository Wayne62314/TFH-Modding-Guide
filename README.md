# TFH Modding Guide：从资源调查到运行时 MOD 的开发笔记

面向 Them’s Fightin’ Herds MOD 作者的公开开发文档。不是官方SDK，也不是完整反编译源码。公开整理日期：2026-10-23；研究记录主要截至2026-10-22，验证环境为 Windows x64 的一个固定游戏构建。

这份文档回答：**我们怎样从“想玩隐藏大熊”一步步做到角色替换、Boss 状态实验、剧情关卡、原生输入、连段与离线AI；每一步用了什么有效信息，哪些结论仍不能下。**

## 最重要的三点

1. 游戏不是“所有内容都在Lua里”。原生引擎处理对象、状态执行、输入、资源和碰撞；Lua/XML/INI等负责大量玩法编排、目标和配置。
2. 一份资源、一个状态名或一个Flag的存在，只能证明有这个线索。必须再验证加载上下文、执行路径、所有权和收尾。
3. 资源补丁、内存状态修改、原生输入替换、Windows模拟按键，是不同方法。不能用“没改游戏文件”来暗示没有修改游戏行为。

## 阅读路线

| 你想解决的问题 | 章节 |
|---|---|
| 如何区分证据、推测与成功 | [00 证据与适用范围](docs/00-evidence-and-scope.md) |
| 游戏入口、Lua和引擎如何分工 | [01 运行结构](docs/01-engine-and-lifecycle.md) |
| .gfs/.tfhres/.foit、template与temp怎么查 | [02 文件与资源](docs/02-assets-and-script-routing.md) |
| 没有SDK时怎样定位运行时函数 | [03 原生调查方法](docs/03-native-investigation.md) |
| 大熊为什么不能只加一个选角格 | [04 大熊开发复盘](docs/04-huggles-case-study.md) |
| 奥莉三阶段、Fred、Velvet/Paprika/天火移植 | [05 Boss与跨角色资源](docs/05-boss-and-resource-dependencies.md) |
| 防御、拆投、直接输入和模拟键盘 | [06 输入与接触系统](docs/06-input-and-defense.md) |
| 缓存、卡顿、预测调用与失效指针 | [07 性能与生命周期](docs/07-performance-and-prediction.md) |
| 内置连段与任意中间节点接续 | [08 原生AI与连段](docs/08-built-in-ai-and-combos.md) |
| TFHR/TFHC、数据对齐、学习模型 | [09 回放和离线AI](docs/09-replays-and-learning.md) |
| 剧情、新关、皮肤、自制角色可以做到多少 | [10 MOD方向](docs/10-story-and-new-content.md) |
| 如何测试、发Release、回滚和脱敏 | [11 工程与发布](docs/11-testing-packaging-and-publication.md) |
| 本构建关键字段及定位置信度 | [12 地址与字段参考](docs/12-build-specific-reference.md) |
| 做过哪些实验、还缺哪些信息 | [13 项目路线与未知项](docs/13-development-roadmap.md) |

另见 [资料来源](SOURCES.md)、[术语表](GLOSSARY.md)、[公开范围与权利说明](PUBLICATION.md)。[英文概览](README.en.md) 方便非中文作者判断是否相关；详细正文目前以中文为主。

## 已完成不等于全部可用

- **用户实测**：普通离线训练/本地对战中的大熊替换；奥莉强化、手动飞行相关实验；原生输入方向/ABCD；普通地投/空投的部分离线辅助测试；用户录制连段复现；5C命中接续；第一条内置奥莉AI连段执行。
- **有条件/不完整**：Fred反复召唤和漩涡收尾、Velvet龙卷风、Paprika Flag27、跨角色普通Fred、起跳/落地边界防御、未使用招式的动画。
- **不能宣称已完成**：完整剧情Boss移植、Baihe Supernova移植、任意角色/场景通用输入AI、完整皮肤/新角色工具链、高水平自主陪练、联网机器人。

不同版本、不同模块可能只经过独立测试，集成后的回归是另一件事。详见各章节证据等级，不把整张清单当作一个已全面验证的发行包。

## 可以公开参考的源码

- [TFHMOD](https://github.com/Wayne62314/TFHMOD)：已公开的角色工具源码、实验UI与使用说明。
- [Velvet Beautifier参考仓库](https://github.com/Wayne62314/velvet-beautifier)：资源格式、打包/安装流程的重要参考；应同时尊重其上游与许可证。
- [Frida官方JavaScript API](https://frida.re/docs/javascript-api/)：运行时观察与NativeFunction/Interceptor等接口文档。

本仓库单独编写，不是私密研究仓库的改公开分支。**不包含原始私人日志、录像、参与者资料、游戏资源、内存转储、模型或凭据。** 提供的两个小示例只读索引或处理合成输入，不会连接游戏或注入操作。

## 适用构建与边界

研究构建EXE SHA256：`03E20EECE23F39FB1012061A5A7FF92F4B63DA23EB8EB641CF6EE379CBCE373D`。本仓库的RVA/字段不是稳定SDK。其他构建不得直接套用；先重新确认函数签名、对象语义和测试条件。

所有运行时实验仅限自己授权的离线环境。不要取消联网保护、尝试绕过反作弊或关闭安全软件。服务器所有权不等于已掌握客户端同步/回滚协议，也不代表其他玩家同意被辅助工具影响。
