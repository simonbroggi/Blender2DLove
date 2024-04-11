print("Hello Blender True Löve")
local images = {}
images["logos/love-logo.png"] = love.graphics.newImage("logos/love-logo.png")
images["logos/love-game-icon.png"] = love.graphics.newImage("logos/love-game-icon.png")
images["logos/love-app-icon.png"] = love.graphics.newImage("logos/love-app-icon.png")
love.graphics.draw(images["logos/love-app-icon.png"], 6.262423038482666, 6.851303577423096, 0.0, 0.5369744896888733, 0.5369744896888733, 0.0, 512.0)
love.graphics.draw(images["logos/love-game-icon.png"], 0.0, -0.0, 0.0, 0.464616060256958, 0.464616060256958, 0.0, 1024.0)
love.graphics.draw(images["logos/love-logo.png"], 2.5499632358551025, 1.2037529945373535, 0.5510384440422058, 1.0, 1.0, -512.0, 570.0)
