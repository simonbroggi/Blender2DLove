if arg[2] == "debug" then
    require("lldebugger").start()
end

function love.load()
    require("test")
    love.graphics.setColor(1,1,1,1)
    love.graphics.circle("fill", 20,20,20)
    love.graphics.present()
    love.timer.sleep(2)
    love.event.quit()
end

local love_errorhandler = love.errorhandler

function love.errorhandler(msg)
    if lldebugger then
        error(msg, 2)
    else
        return love_errorhandler(msg)
    end
end
