# 2 · 把一关写成有对白的连战章节

[教程目录](../README.md) · [English](../en/02-chapter.md)

先说范围：我们做过教程里的独立连战方案。官方故事选章菜单、任务奖励和存档进度，还没接通。下面的“章节”是在一节教程内连续换对手，退出后从头开始。

先只放两个对手。旧项目计划过十一战，没有完成全部切换的实机验收。

## 把台词和对手放进表

在第一课 `hello.lua` 的初始化之后、`setInit` 之前，加自己的数据：

```lua
local encounters = {
  {sprite = "cow", name = "Arizona", before = "门口的石头又松了。", after = "先停工，听听洞顶的声音。"},
  {sprite = "uni", name = "Oleander", before = "这儿还有人在睡觉。", after = "带上你的书，咱们去外面谈。"}
}
```

示例台词是新写的占位文本。角色的内部名需要逐个核对，`uni` 对应奥莉。预加载放进原来的 `setMatchSettings` 回调内：

```lua
preloadSprite("uni")
disableRoundWins()
disableMatchWin()
```

不要再登记第二个 `setMatchSettings` 去覆盖第一个。场地先沿用第一课能进入的场地，别同时换隐藏角色和地图。

## 每场怎么准备

下面是供你整合进关卡的示意实现，尚未做新版本游戏内测试。放在 `encounters` 后面：

```lua
local function pauseFight()
  disableAi()
  enablePlayerControls(Player1, false)
  enablePlayerControls(Player2, false)
end

local function prepareEncounter(e)
  pauseFight()
  setPlayerSprite(Player2, e.sprite)
  setPlayerPalette(Player2, 0)
  wait(2)
  -- 换角色以后重新取对象，别继续用上一场的 p2。
  getP1():fullHeal()
  getP2():fullHeal()
  getP1():setEnemy(getP2())
  getP2():setEnemy(getP1())
  trialSetupDistance(850)
  getP1().facingDir = FaceDirection.RIGHT
  getP2().facingDir = FaceDirection.LEFT
end

local function fightOne()
  setTrainingOption("OptLifeBar", "Normal")
  setTrainingOption("OptDeathAllowed", "Yes")
  enablePlayerControls(Player1, true)
  enablePlayerControls(Player2, true)
  enableAi()
  local elapsed = 0
  while getP1().lifebar > 0 and getP2().lifebar > 0 and elapsed < 36000 do
    wait(1)
    elapsed = elapsed + 1
  end
  local won = getP1().lifebar > 0 and getP2().lifebar <= 0
  pauseFight()
  return won
end
```

`wait(2)` 是旧方案里使用的短等待值，不能保证任意角色资源两次调度后都准备好。首次接入要观察实际对象和加载结果。这里省略了完整 Boss 的依赖准备。

## 替换 lesson 函数

保留原来的 `setInit`，它仍然调用 `lesson`。把第一课的 `lesson` 换成：

```lua
local function lesson()
  enableTrainingMode()
  for _, e in ipairs(encounters) do
    local won = false
    repeat
      prepareEncounter(e)
      waitForConvo("Trainer", e.name .. ": " .. e.before)
      won = fightOne()
      if not won then
        waitForConvo("Trainer", "这一场再来一次。")
      end
    until won
    waitForConvo("Trainer", e.after)
  end
  endTutorial()
end
```

顺序是数据表、辅助函数、lesson、setInit。Lua 的局部作用域要留意；先定义引用者再声明局部函数，容易引用到全局 nil。

生成器会读取你改过的 `hello.lua`。先恢复第一课安装的包，再用一个全新输出目录生成。别拿候选包当原版再次打补丁。

## 什么时候算这章接上了

先测 Arizona 能否行动和被击败，再看是否切到奥莉。故意输一次，确认重试停留在当前对手。最后退出重进，看有没有遗留 AI 或控制锁定。

要做官方剧情选章，可以从 `Trials/story.xml`、`Trials/Lib/story_helpers.lua`、菜单中的 story 引用继续追。搜到函数名先看实际调用，存档键和奖励写入目前没有完整文档。不要为了出现新菜单就复用一个未知的存档章节编号。
