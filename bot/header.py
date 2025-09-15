# header.py
# some important globals

#xpos_heroes = [336, 426, 516, 606, 696, 786, 1076, 1166, 1256, 1346, 1436, 1526]
xpos_heroes = [338, 426, 514, 603, 690, 777, 1106, 1194, 1283, 1370, 1458, 1546]
game_id = '1422450'
steam_path = 'C:/Program Files (x86)/Steam/steam.exe'
open_deadlock_steam = f'"{steam_path}" steam://rungameid/{game_id}'
depth = 10

def init():
    global xpos_heroes
    global open_deadlock_steam
    global depth

