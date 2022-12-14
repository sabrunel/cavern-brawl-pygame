
# Window
WIDTH = 960
HEIGHT = 540

# Assets directories
GRAPHICS_DIR = 'assets/graphics/'
SOUNDS_DIR = 'assets/sounds/'
FONTS_DIR = 'assets/fonts/'

# Frame rate
FPS = 60

# Text
TEXT_COLOR = (253, 253, 218)
FONT_NAME = 'manaspc.ttf'
FONT_SIZE = 16
TITLE_SIZE = 70

# Animations
collectible_animation_frames = {
    'Health' : 6,
}

projectile_animation_frames = {
    'Dagger' : 1,
    'Orb' : 4,
}

particle_animation_frames = {
    'Attack': 5,
    'RangedAttack': 3,
}

character_animation_frames =  { # Number of images per animation
    'Hero': {'Idle': 9, 'Run': 8, 'Jump': 4, 'Attack': 7, 'Attack2': 7, 'Attack3': 7, 'AttackUp': 7, 'RangedAttack': 7, 'Hurt': 3,'Death':7,},
    'Bat': {'Idle': 9,'Run': 9,'Attack': 7,'Hurt': 3,'Death':7,},
    'Monster': {'Idle': 11,'Run': 8,'Attack': 7,'Hurt': 3,'Death':7,},
    'PlagueDoctor': {'Idle': 7,'Run': 6,'Attack': 7,'Hurt': 3,'Death':7},
}

# Health bars
HEALTH_BORDER = (45,45,45)
HEALTH_RED = (191, 51, 6)
HEALTH_GREY = (35,35,35)
HEALTH_GREEN = (0, 244, 143)
BORDER_WIDTH = 2

# Game
GROUND_Y = 480 
HEAL_EFFECT = 15

fighter_info = {
    "Hero": {"y_offset": 0, "strength": 8, "max_hp": 40, "velocity": 4, "hurtbox" : [24, 50, (42, 75)], "hitbox": [0, 0, (84 ,75)]},
    "Bat": {"y_offset": -250, "strength": 6, "max_hp": 15, "velocity": 1, "hurtbox" : [0, 0, (64, 64)], "hitbox": [0, 0, (64, 64)]},
    "Monster": {"y_offset": -10,"strength": 6, "max_hp": 20, "velocity": 2, "hurtbox" : [0, 26, (46, 40)], "hitbox": [32, 0, (30, 40)]},
    "PlagueDoctor": {"y_offset": -5,"strength": 7, "max_hp": 20, "velocity": 1, "hurtbox" : [10, 46, (52, 82)], "hitbox": [45, 0, (45 , 82)]},
}

projectile_info = {
    'Dagger' : {'velocity' : 10},
    'Orb' : {'velocity': 5}
}