<p align="center">
  <img src="https://github.com/Taylorwaldo/UNCWflappybird-custom/blob/main/readme_media/title_readme.v1.cropped.png?raw=true" alt="Image Alt" />
</p>

A faithful recreation of the classic Flappy Bird game built with Python and Pygame, featuring smooth animations, particle effects, and authentic gameplay mechanics.


### Gameplay
Navigate your bird through an endless series of green pipes by tapping the spacebar to flap and stay airborne. Each pipe you pass increases your score - but be careful, one wrong move and it's game over!

<p align="center">
  <img src="https://github.com/Taylorwaldo/UNCWflappybird-custom/blob/main/readme_media/Screen%20Recording%202025-09-01%20at%203.50.58%20PM.gif?raw=true" alt="Demo GIF" width="400"/>
</p>


### Features

-> Authentic Gameplay - Faithful recreation of the original Flappy Bird mechanics

-> Smooth Animations - Wing flapping, bird rotation, and scrolling backgrounds

-> Particle Effects - Impact particles when colliding with pipes or ground

-> Sound Effects - Wing flaps, scoring, collisions, and game over sounds

-> Score Tracking - Current score display with persistent high score

-> Multiple Game States - Start screen, gameplay, and game over screens

-> Optimized Performance - Efficient rendering and asset management


### Getting Started
Prerequisites

Python 3.7 or higher
Pygame library


### Installation
Clone the repository


```bash
git clone https://github.com/yourusername/flappy-bird.git
cd flappy-bird
```

### Install dependencies

```bash
pip install pygame
```

### Run the game

```bash
python flappy_bird.py
```

Controls

| Key | Action |
|-----|--------|
| `SPACE` | Flap wings / Start game / Restart after game over |
| `ESC` or closing window | Quit game |

### Configuration

The game can be easily customized by adjusting parameters in the constants section:

```python
# Game constants
GRAVITY = 0.8           # Bird fall speed
JUMP_STRENGTH = -8      # Bird jump power
PIPE_SPEED = 3          # Pipe movement speed
FLOOR_SPEED = 1         # Floor scrolling speed
PIPE_GAP = 180         # Gap between pipes
FPS = 60               # Frame rate
```

### Known Issues

Sound effects may not work on some systems - game will continue without audio

Requires specific image and sound files to be present in correct directories



### Acknowledgments

Original Flappy Bird game created by Dong Nguyen

Pygame community for comprehensive documentation and tutorials

Open-source contributors for sound effects and sprite assets
