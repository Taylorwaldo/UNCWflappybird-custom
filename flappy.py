# Importing the libraries
import pygame
import sys
import time
import random
import math

# Initializing the pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Game window setup
width, height = 350, 622
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load and scale images once at startup for better performance
try:
    back_img = pygame.image.load("img_46.png").convert()
    floor_img = pygame.image.load("img_50.png").convert()

    # Bird sprites
    bird_up = pygame.image.load("img_47.png").convert_alpha()
    bird_down = pygame.image.load("img_48.png").convert_alpha()
    bird_mid = pygame.image.load("img_49.png").convert_alpha()
    birds = [bird_up, bird_mid, bird_down]

    # Pipe and game over images
    pipe_img = pygame.image.load("greenpipe.png").convert_alpha()
    over_img = pygame.image.load("img_45.png").convert_alpha()

except pygame.error as e:
    print(f"Could not load images: {e}")
    sys.exit()

# Load sound effects
try:
    sfx_wing = pygame.mixer.Sound("audio/assets_audio_sfx_wing.wav")
    sfx_hit = pygame.mixer.Sound("audio/assets_audio_sfx_hit.wav")
    sfx_point = pygame.mixer.Sound("audio/assets_audio_sfx_point.wav")
    sfx_die = pygame.mixer.Sound("audio/assets_audio_sfx_die.wav")
    sfx_swooshing = pygame.mixer.Sound("audio/assets_audio_sfx_swooshing.wav")

    # Adjust volume levels (0.0 to 1.0)
    sfx_wing.set_volume(0.7)
    sfx_hit.set_volume(0.8)
    sfx_point.set_volume(0.6)
    sfx_die.set_volume(0.7)
    sfx_swooshing.set_volume(0.5)

    print("Sound effects loaded successfully!")

except pygame.error as e:
    print(f"Could not load sound effects: {e}")
    # Create dummy sound objects so the game doesn't crash
    sfx_wing = sfx_hit = sfx_point = sfx_die = sfx_swooshing = None


def play_sound(sound):
    """Safely play a sound effect"""
    if sound:
        try:
            sound.play()
        except:
            pass  # Ignore sound errors to keep game running


# Font setup
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Game constants
GRAVITY = 0.8
JUMP_STRENGTH = -8
PIPE_SPEED = 3
FLOOR_SPEED = 1
PIPE_GAP = 180
FPS = 60

# Floor animation
floor_x = 0

# Bird setup
bird_index = 0
bird_rect = birds[0].get_rect(center=(67, height // 2))
bird_velocity_y = 0

# Game state
game_state = "start"  # Can be "start", "playing", or "game_over"
score = 0
high_score = 0
score_time = True
pipes = []

# Particle system for impact effect
particles = []


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-5, -1)
        self.life = 30
        self.max_life = 30

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.2  # Gravity on particles
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        if alpha > 0:
            color = (255, 255, 255, alpha)
            pygame.draw.circle(screen, color[:3], (int(self.x), int(self.y)), 3)


# Optimized functions
def draw_floor():
    """Draw scrolling floor with seamless loop"""
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + floor_img.get_width(), 520))


def create_pipes():
    """Create pipe pair with consistent gap"""
    # Use the original working approach with random choice
    pipe_y = random.choice([300, 350, 400, 450])

    # Create top pipe - positioned with midbottom anchor
    top_pipe = pipe_img.get_rect(midbottom=(width + 50, pipe_y - 150))

    # Create bottom pipe - positioned with midtop anchor
    bottom_pipe = pipe_img.get_rect(midtop=(width + 50, pipe_y))

    return top_pipe, bottom_pipe


def update_pipes():
    """Update pipe positions and handle collisions"""
    global game_state, particles

    for pipe in pipes[:]:  # Iterate over copy to safely remove
        if game_state == "playing":
            pipe.centerx -= PIPE_SPEED

            # Remove off-screen pipes
            if pipe.right < 0:
                pipes.remove(pipe)
                continue

        # Draw pipes with proper orientation
        # Top pipes have their bottom edge above screen center, bottom pipes below
        if pipe.centery < height // 2:  # Top pipe
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:  # Bottom pipe
            screen.blit(pipe_img, pipe)

        # Collision detection with pixel-perfect accuracy
        if bird_rect.colliderect(pipe) and game_state == "playing":
            game_state = "game_over"
            play_sound(sfx_hit)  # Play hit sound on pipe collision
            # Create impact particles
            for _ in range(8):
                particles.append(Particle(bird_rect.centerx, bird_rect.centery))


def update_score():
    """Handle scoring system"""
    global score, score_time, high_score

    if game_state == "playing" and pipes:
        for pipe in pipes:
            # Score when bird passes pipe center
            if (bird_rect.centerx > pipe.centerx and
                    bird_rect.centerx < pipe.centerx + PIPE_SPEED + 5 and
                    score_time):
                score += 1
                play_sound(sfx_point)  # Play point sound when scoring
                score_time = False
                break

        # Reset scoring flag when no pipes are in scoring zone
        if not any(abs(pipe.centerx - bird_rect.centerx) < 10 for pipe in pipes):
            score_time = True

    # Update high score
    if score > high_score:
        high_score = score


def draw_score(current_game_state):
    """Draw score with better formatting"""
    if current_game_state == "playing":
        score_text = score_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        # Add shadow for better readability
        shadow_text = score_font.render(str(int(score)), True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(width // 2 + 2, 68))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(score_text, score_rect)

    elif current_game_state == "game_over":
        score_text = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
        screen.blit(high_score_text, high_score_rect)


def reset_game():
    """Reset all game variables for restart"""
    global game_state, score, bird_velocity_y, bird_rect, score_time, particles
    game_state = "start"
    pipes.clear()
    particles.clear()
    bird_velocity_y = 0
    bird_rect.center = (67, height // 2)
    score = 0
    score_time = True
    play_sound(sfx_swooshing)  # Play swoosh sound on game restart


def update_particles():
    """Update and draw particle effects"""
    for particle in particles[:]:
        particle.update()
        if particle.life <= 0:
            particles.remove(particle)
        else:
            particle.draw(screen)


# Event timers
bird_flap = pygame.USEREVENT
create_pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)
pygame.time.set_timer(create_pipe_event, 1200)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "playing"
                    play_sound(sfx_wing)  # Play wing flap sound on first jump
                elif game_state == "playing":
                    bird_velocity_y = JUMP_STRENGTH
                    play_sound(sfx_wing)  # Play wing flap sound on jump
                elif game_state == "game_over":
                    reset_game()

        elif event.type == bird_flap and game_state == "playing":
            # Animate bird sprite only during gameplay
            bird_index = (bird_index + 1) % len(birds)
            old_center = bird_rect.center
            bird_rect = birds[bird_index].get_rect(center=old_center)

        elif event.type == create_pipe_event and game_state == "playing":
            pipes.extend(create_pipes())

    # Clear screen
    screen.blit(back_img, (0, 0))

    # Game logic based on current state
    if game_state == "start":
        # Start screen - bird hovering, no physics
        # Bird gently bobs up and down
        bob_offset = math.sin(pygame.time.get_ticks() * 0.005) * 3
        bird_display_rect = bird_rect.copy()
        bird_display_rect.centery += bob_offset

        # Draw non-rotating bird
        screen.blit(birds[bird_index], bird_display_rect)

        # Show title screen
        screen.blit(over_img, over_img.get_rect(center=(width // 2, height // 2)))

        # Show high score if there is one
        if high_score > 0:
            high_score_text = score_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
            screen.blit(high_score_text, high_score_rect)

    elif game_state == "playing":
        # Active gameplay
        # Bird physics
        bird_velocity_y += GRAVITY
        bird_rect.centery += bird_velocity_y

        # Boundary checking
        if bird_rect.top <= 0:
            bird_rect.top = 0
            bird_velocity_y = 0
        elif bird_rect.bottom >= 520:  # Floor collision
            game_state = "game_over"
            play_sound(sfx_die)  # Play death sound on ground collision
            # Create ground impact particles
            for _ in range(6):
                particles.append(Particle(bird_rect.centerx, bird_rect.bottom))

        # Update floor position
        floor_x -= FLOOR_SPEED
        if floor_x <= -floor_img.get_width():
            floor_x = 0

        # Bird rendering with smooth rotation
        rotation_angle = max(-25, min(25, bird_velocity_y * -4))
        rotated_bird = pygame.transform.rotozoom(birds[bird_index], rotation_angle, 1)
        bird_render_rect = rotated_bird.get_rect(center=bird_rect.center)
        screen.blit(rotated_bird, bird_render_rect)

        # Update game elements
        update_pipes()
        update_score()
        draw_score("playing")

    elif game_state == "game_over":
        # Game over state - frozen gameplay
        # Draw bird in frozen state
        rotation_angle = max(-25, min(25, bird_velocity_y * -4))
        rotated_bird = pygame.transform.rotozoom(birds[bird_index], rotation_angle, 1)
        bird_render_rect = rotated_bird.get_rect(center=bird_rect.center)
        screen.blit(rotated_bird, bird_render_rect)

        # Draw frozen pipes
        update_pipes()  # This handles drawing without movement

        # Particle effects
        update_particles()

        # Game over overlay
        screen.blit(over_img, over_img.get_rect(center=(width // 2, height // 2)))
        draw_score("game_over")

    # Always draw floor last (on top)
    draw_floor()

    # Update display
    pygame.display.flip()

# Cleanup
pygame.quit()
sys.exit()