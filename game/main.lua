if arg[2] == "debug" then
    require("lldebugger").start()
end

function love.load()
    love.graphics.clear()
    love.graphics.setColor(1,1,1,1)
    WindowWidth, WindowHeight = love.graphics.getDimensions()

end

function love.update(dt)
end

function love.draw()
    love.graphics.rectangle("fill", 0, 0, WindowWidth, WindowHeight)
    dofile("game/test.lua")
    love.timer.sleep(0.01)
end

local love_errorhandler = love.errorhandler

function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
