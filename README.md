## Project overview

This project was inspired by the tutorial series from [Coding With Russ](https://www.youtube.com/playlist?list=PLjcN1EyupaQnvpv61iriF8Ax9dKra-MhZ) on Youtube, creating a Final Fantasy style RPG battle game with Pygame.

It is a simple turn-based combat game where a cute red-haired hero faces pairs of random enemies in a gloomy cavern setting.

![preview](./assets/game_preview.png)

### Resources

Assets used for this game were adapted from [Szadiart's platformer set](https://szadiart.itch.io/rocky-world-platformer-set) and [Shikashi's icon pack](https://cheekyinkling.itch.io/shikashis-fantasy-icons-pack).

### Requirements

Requirements for using this code are available in the `requirements.txt` file.

Each package can be installed using the Pip command, or in conda with:

`conda create --name <env> --file requirements.txt`


### Run the game

Open the command line and navigate to the folder containing `main.py`

Then simply type:

`python main.py`

Select an enemy to attack it, then watch as the turn unfolds and your enemies fight back.

Keep attacking them or use your health potions to regain precious HP.

As you emerge victorious from the brawl, or lay dead on the cavern floor, new random sets of enemies can be generated to continue playing.


## What I learned

This project started as a one evening code-along session, as I was learning the basics of Pygame (events, game loop, sprites...).

With the core set of classes and mechanics in place in a single file by the end of the tutorial, I worked on improving the structure of the code, creating a minimal and reusable game engine for later Python projects.


