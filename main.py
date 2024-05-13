import character


sniper = character.Character("_______", "SNIPER", hp_max=100, dmg=200, nb_bullets=1, cd_reload=4)
soldat = character.Character("_______", "SOLDAT", hp_max=150, dmg=35, nb_bullets=3, cd_reload=2)
assassin = character.Character("_______", "ASSASSIN", hp_max=75, dmg=50, nb_bullets=3, cd_reload=1)
tank = character.Character("_______", "TANK", hp_max=300, dmg=40, nb_bullets=2, cd_reload=3)



print(tank.username)
