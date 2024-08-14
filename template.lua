
    
-- This move type is '{move_type}'
-- This move category is '{move_category}' ( put into XML file? )
-- This move PP is {move_PP} (evaluate if this is necessary, usage? conversion?)
-- This move EFFECT/DESCRIPTION is '{move_Effect}' this shoud be reflected in the spell routine

local power = {move_power}
local name = "{move_name}"
local accuracy = {move_accuracy}
local eff = 1 -- change magic effect

-- adapt area of spell
local area = {{ 
    {{0, 0, 0, 0, 0}},
    {{0, 1, 1, 1, 0}},
    {{0, 1, 2, 1, 0}},
    {{0, 1, 1, 1, 0}},
    {{0, 0, 0, 0, 0}}
}}

local combat = Combat()
-- Spell Damage
combat:setMove(power, accuracy, name)
combat:setParameter(COMBAT_PARAM_MAGICAL, FALSE)
-- Spell Animation
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_NORMALDAMAGE)
combat:setArea(createCombatArea(area))
-- Condition to apply?
combat:setParameter(COMBAT_PARAM_CONDITION, CONDITION_ATTRIBUTES) -- REVIEW CONDITION
combat:setParameter(COMBAT_PARAM_CONDITIONCHANCE, 100)
combat:setParameter(COMBAT_PARAM_CONDITIONVALUE, 13)
combat:setParameter(COMBAT_PARAM_CONDITIONTIME, 30)
combat:setParameter(COMBAT_PARAM_CONDITIONSKILL, STAT_DEFENSE)

function onCastSpell(creature, variant, isHotkey)
    creature:say(string.upper(name), TALKTYPE_MONSTER_SAY)
    
    -- remove if not using area
    local pos = creature:getPosition()
    pos.x = pos.x + 1
    pos.y = pos.y + 1
    Position(pos):sendMagicEffect(eff)
    
    return combat:execute(creature, variant)
end
