# 2 · Extend a lesson into a battle chapter with dialogue

[Tutorial index](../README.en.md) · [中文](../zh/02-chapter.md)

Our implemented design was a standalone tutorial battle sequence. Official story chapter selection, quest rewards and saved progression remain unconnected. “Chapter” here means successive opponents inside one lesson; exiting resets progress.

Start with two opponents. The earlier project planned eleven battles without completing all transition playtests.

## Store dialogue and opponents in a table

In lesson 1's hello.lua, after initialization registration and before setInit, add:

```lua
local encounters = {
  {sprite = "cow", name = "Arizona", before = "The stones by the entrance are loose again.", after = "Stop digging. Listen to the ceiling."},
  {sprite = "uni", name = "Oleander", before = "Someone is still sleeping here.", after = "Bring your book. Let's talk outside."}
}
```

These are original placeholder lines. Verify internal fighter names individually; uni is Oleander. Inside the existing setMatchSettings callback, add:

```lua
preloadSprite("uni")
disableRoundWins()
disableMatchWin()
```

Do not register a second setMatchSettings and overwrite the first. Keep lesson 1's working stage initially, rather than changing hidden fighters and maps together.

## Prepare each battle

This illustrative implementation is for integration into your lesson; the newly assembled version is not in-game validated. Place it after encounters:

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
  -- Reacquire fighters after replacement; do not retain the previous p2.
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

wait(2) is the old design's short delay, not a guarantee that every fighter's resources are ready after two scheduler steps. Observe actual objects/loading on first integration. Complete boss dependency preparation is omitted here.

## Replace the lesson function

Keep setInit calling lesson, and replace the original lesson body:

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
        waitForConvo("Trainer", "Try this opponent again.")
      end
    until won
    waitForConvo("Trainer", e.after)
  end
  endTutorial()
end
```

Order: data, helpers, lesson, setInit. Watch Lua local scope; a caller defined before a later local function declaration can refer to a nil global.

The builder reads your edited hello.lua. Restore lesson 1's installed archive first, then generate into a new output directory. Do not patch a candidate as though it were the original.

## Validate transitions

Check that Arizona can act/be defeated, then that Oleander loads. Lose intentionally and verify retry stays on the current opponent. Exit/re-enter and inspect lingering AI or control locks.

For official story chapter selection, follow Trials/story.xml, Trials/Lib/story_helpers.lua and story-menu references. Inspect actual calls before relying on names. Save keys and reward writes are not fully documented. Do not reuse an unknown saved-chapter ID just to make a menu entry appear.
