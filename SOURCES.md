# 资料来源与可复核性

[English](SOURCES.en.md)

本文主要是开发者对自己项目和授权离线实验的原创汇总。研究记录主要截至2026-10-22，公开整理于2026-10-23。以下公开链接可帮助阅读实现；本仓库不复制完整游戏脚本或私密实验目录。

## S1 · 已公开TFHMOD源码

[项目主页](https://github.com/Wayne62314/TFHMOD)。本文阅读的源码提交：`a630d5a8995527520beed628a778231d1eb95751`。如发现链接不可达或对应文件改变，请先核对提交，不用main的变化反推旧实验。

- [加载/重置/增强钩子](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/training-hook.js)：P1替换、模式组合、Flag27及模块配置。
- [三阶段原生适配](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/phase3-native.js)：作用域范围缓存、状态排队、位置、对象归属及恢复。
- [三阶段控制器](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/phase3-controller.js)：请求、等待、超时、恢复与错误闭锁。
- [Boss附加实验](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/boss-extras.js)：Paprika/Velvet的受限入口和限制。
- [天火召唤实验](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/tian-summons.js)：依赖P2普通奥莉等条件；未成功Supernova保持禁用。
- [英文使用说明](https://github.com/Wayne62314/TFHMOD/blob/a630d5a8995527520beed628a778231d1eb95751/ui/USAGE.en.txt)：版本、安装和已知限制，不等于每项完成游戏回归。

## S2 · Velvet Beautifier

[参考仓库](https://github.com/Wayne62314/velvet-beautifier)，阅读提交`ce2b09e63531bda79e33990a89f5ab866b9f591b`。该项目有自己的上游、贡献历史和许可，不能把它当成我们的原创。

- [流程说明](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/PROCESS.md)：备份、恢复、GFS/TFHRES与MOD应用顺序。
- [GFS相关工具](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/VelvetBeautifier/GFS/Utils.cs)：归档提取/创建的使用方式。
- [TFHResource管理](https://github.com/Wayne62314/velvet-beautifier/blob/ce2b09e63531bda79e33990a89f5ab866b9f591b/VelvetBeautifier/TFHResource/Manager.cs)：资源路径、克隆/合并/保存与回退。

这项依赖主要提供格式/安装参考，不能据此声称后续原生生命周期、输入、预测隔离和AI数据研究也都是上游已提供的功能。

## S3 · 工具接口资料

- [Frida JavaScript API](https://frida.re/docs/javascript-api/)：Interceptor、NativeFunction、NativePointer、Memory、Process等。这里只解释接口类别，不把工具文档当作TFH对象布局证据。
- [Microsoft PE格式文档](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format)：RVA、入口、节与异常目录概念。具体游戏语义仍需本地验证。

## L1 · 持有游戏者可自行核对的资源路径

这些是逻辑包内路径/名称，**不是本仓库可下载素材**：

- ai-libs.gfs：AI/uni.lua、AI/common_goat.lua、AI/tianhuo.lua、AI/baihe.lua、AI/combos/uni/*.ini及相关decisions XML。
- trials.gfs：Trials/story/bossMultistage.lua、oleander_round3.xml、platforming/paprika_fight.lua、velvet_fight.lua、训练库及菜单XML。
- characters-foits.gfs：temp/tianhuo.foit、temp/baihe.foit等序列化角色数据；角色名/状态候选不等于完整指令解码。
- 本机resources_prod/lobbymaps_prod TFHRES schema与20份TFHR、3份命名TFHC样本的只读解析。

## L2 · 未公开原始记录的结果

本文含对崩溃/运行时采样、模型对照和用户游玩反馈的脱敏总结。原始日志、录像、内存转储、参与者资料和模型不在本仓库，也不提供需要访问私人仓库的链接。公众不能仅凭本文独立复现每条历史观察；应在匹配构建、相同条件下重新测试，并按00章报告证据等级。

本仓库的合成示例测试只验证示例自身，不替代原游戏实验，也不伪称对所有游戏格式/构建完整支持。

## T1 · 动手教程的代码出处

[动手教程](tutorials/README.md) 用公开 S1 实现解释加载、Flag 和 UI 配置流。另读了本机构建的 `Trials/training/TrialLib.lua`、`TutorialLib.lua`、`TestBed.lua` 及 `Trials/Lib/LuaLib.lua`，核对教程生命周期、属性包装与输入调用形状；`Doc/Metas.lua` 只作接口声明线索，不当实现。

本轮 `hello.lua`、候选生成器、训练观察器及其测试为新写教学代码。菜单/脚本槽位来自早期独立关方案，观察字段沿用研究结果。新组合没有游戏内验收。候选工具本地输出的原包和候选都不能随贡献上传；公开仓库只保留代码和合成测试。
