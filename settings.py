
# Window
WIDTH = 960
HEIGHT = 540


# Frame rate
FPS = 60

# Text
TEXT_COLOR = (253, 253, 218)
FONT_NAME = 'font/manaspc.ttf'
FONT_SIZE = 16
TITLE_SIZE = 70

# Health bars
HEALTH_RED = (191, 51, 6)
HEALTH_GREEN = (0, 244, 143)
HEALTH_BORDER = (0, 0, 0)
BORDER_RADIUS = 10
BORDER_WIDTH = 1

# Game 
PLAYER_MAX_HP = 40
PLAYER_STRENGTH = 8
PLAYER_START_POTIONS = 3
POTION_EFFECT = 15


animation_frames =  { # Number of images per animation
    'Hero': {'Idle': 9, 'Run': 8,'Attack': 7,'Hurt': 3,'Death':7,},
    'Bat': {'Idle': 9,'Run': 9,'Attack': 7,'Hurt': 3,'Death':7,},
    'Monster': {'Idle': 9,'Run': 8,'Attack': 7,'Hurt': 3,'Death':7,},
    'PlagueDoctor': {'Idle': 9,'Run': 6,'Attack': 7,'Hurt': 3,'Death':7},
}

enemy_x_pos = [650, 775]

enemy_info = {
    "Bat": {"strength": 6, "max_hp": 15, "start_potions": 0},
    "Monster": {"strength": 6, "max_hp": 20, "start_potions": 0},
    "PlagueDoctor": {"strength": 7, "max_hp": 20, "start_potions": 1},
}
