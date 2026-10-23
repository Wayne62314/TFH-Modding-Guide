-- Original teaching sample. Requires this game's tutorial runtime.
-- Newly assembled example; not yet playtested as a packaged lesson.
require("LuaLib")
require("TutorialLib")
require("TrialLib")
require("char_data/AllChar")

setMatchSettings(function()
  initTrial("cow", "cow")
  initSkipIntro()
end)

local function lesson()
  enableTrainingMode()
  waitForConvo("Trainer", "Hello from my first lesson.")
  getP1():fullHeal()
  getP1():giveMaxSuper()
  getP1():giveMaxMagic()
  waitForConvo("Trainer", "Health and resources restored. Lesson complete.")
  endTutorial()
end

setInit(function()
  startTrial()
  doRoutine(lesson)
end)
