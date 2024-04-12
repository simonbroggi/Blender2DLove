print("Hello Blender True Löve")
local images = {}
images["logos/love-game-icon.png"] = love.graphics.newImage("logos/love-game-icon.png")
images["logos/love-app-icon.png"] = love.graphics.newImage("logos/love-app-icon.png")
images["logos/love-logo.png"] = love.graphics.newImage("logos/love-logo.png")
love.graphics.draw(images["logos/love-logo.png"], 0.0, 0.4000000059604645, -0.0, 1.0, 1.0, 0.0, 380.0)
love.graphics.draw(images["logos/love-game-icon.png"], 20.0, 20.0, -0.0, 1.0, 1.0, 2.8308271794230677e-05, -6.103515625e-05)
love.graphics.draw(images["logos/love-app-icon.png"], -100.0, 500.0, -0.0, 0.5369744896888733, 0.5369744896888733, 0.0, 512.0)
