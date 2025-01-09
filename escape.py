import pygame
import sys
import random
import time
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BOXXED UP")

# Set up colors
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (128, 0, 128)
brown = (165, 42, 42)

# Set up the player
player_size = 40
player_x = (width - player_size) // 2
player_y = height - player_size - 10
player_speed = 5
player_health = 3

# Set up the enemies
num_enemies = 10
enemy_size = 2 * player_size
enemies = []

# Ensure initial positions of enemies are not too close to the player
for _ in range(num_enemies):
    enemy_x = random.randint(0, width - enemy_size)
    enemy_y = random.randint(0, height // 2)
    while (
        player_x < enemy_x + enemy_size
        and player_x + player_size > enemy_x
        and player_y < enemy_y + enemy_size
        and player_y + player_size > enemy_y
    ):
        enemy_x = random.randint(0, width - enemy_size)
        enemy_y = random.randint(0, height // 2)
    enemies.append({'x': enemy_x, 'y': enemy_y, 'speed': random.randint(2, 5), 'type': 'red'})

# Set up the power-up boxes
num_powerups = 1
powerups = []

# Set up the star power-up
num_stars = 1
stars = []

# Set up the clock
clock = pygame.time.Clock()

# Initialize score and high score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Initialize timer and game state
start_time = time.time()
game_over = False
speed_up_timer = 0
teleport_timer = 0
teleport_duration = 15
teleport_interval = 180  # 3 seconds (60 frames per second)
star_timer = 0
star_duration = 180  # 3 seconds (60 frames per second)

# Stream of attack control
stream_attack_duration = 3 * 60  # 3 seconds (60 frames per second)
stream_attack_timer = 0
stream_attack_interval = 60  # 1 second intervals between each stream attack

# Star power-up control
star_powerup_duration = 3 * 60  # 3 seconds (60 frames per second)
star_powerup_timer = 0
star_powerup_interval = 60  # 1 second intervals between each star power-up

# Stream of attack flag
stream_attack_active = False

paused = False

# Scoring rate control
scoring_rate = 10  # Increase this value for a slower scoring rate

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    if not paused:
        if not game_over:
            for enemy in enemies:
                if (
                    player_x < enemy['x'] + enemy_size
                    and player_x + player_size > enemy['x']
                    and player_y < enemy['y'] + enemy_size
                    and player_y + player_size > enemy['y']
                ):
                    print("Hit by enemy!")
                    player_health -= 1
                    if player_health == 0:
                        print("Game Over!")
                        if score > high_score:
                            high_score = score
                        score = 0
                        player_health = 3
                        start_time = time.time()
                        game_over = True
                    else:
                        enemy['x'] = random.randint(0, width - enemy_size)
                        enemy['y'] = random.randint(0, height // 2)
                        while (
                            player_x < enemy['x'] + enemy_size
                            and player_x + player_size > enemy['x']
                            and player_y < enemy['y'] + enemy_size
                            and player_y + player_size > enemy['y']
                        ):
                            enemy['x'] = random.randint(0, width - enemy_size)
                            enemy['y'] = random.randint(0, height // 2)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < width - player_size:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < height - player_size:
                player_y += player_speed

            if random.random() < 0.01 and len(powerups) < num_powerups:
                powerup_type = 'purple'
                powerups.append({'x': random.randint(0, width - player_size),
                                 'y': random.randint(0, height // 2),
                                 'type': powerup_type,
                                 'timer': 600})

            if random.random() < 0.01 and len(stars) < num_stars:
                stars.append({'x': random.randint(0, width - player_size),
                              'y': random.randint(0, height // 2),
                              'type': 'star',
                              'timer': 600})

            for powerup in powerups:
                powerup['y'] += 2
                if (
                    player_x < powerup['x'] + player_size
                    and player_x + player_size > powerup['x']
                    and player_y < powerup['y'] + player_size
                    and player_y + player_size > powerup['y']
                ):
                    if powerup['type'] == 'purple':
                        print("Hit by purple box! Teleporting...")
                        teleport_timer = teleport_duration * teleport_interval
                        powerups.remove(powerup)

            for star in stars:
                star['y'] += 2
                if (
                    player_x < star['x'] + player_size
                    and player_x + player_size > star['x']
                    and player_y < star['y'] + player_size
                    and player_y + player_size > star['y']
                ):
                    print("Hit by star! Initiating stream of attacks...")
                    stream_attack_active = True
                    star_powerup_timer = star_powerup_duration
                    stars.remove(star)

            for enemy in enemies:
                enemy['y'] += enemy['speed']
                if enemy['y'] > height:
                    enemy['x'] = random.randint(0, width - enemy_size)
                    enemy['y'] = random.randint(0, height // 2)
                    while (
                        player_x < enemy['x'] + enemy_size
                        and player_x + player_size > enemy['x']
                        and player_y < enemy['y'] + enemy_size
                        and player_y + player_size > enemy['y']
                    ):
                        enemy['x'] = random.randint(0, width - enemy_size)
                        enemy['y'] = random.randint(0, height // 2)

            # Teleport the player every 3 seconds for 15 seconds
            if teleport_timer > 0:
                if teleport_timer % teleport_interval == 0:
                    player_x = random.randint(0, width - player_size)
                    player_y = random.randint(0, height // 2)
                teleport_timer -= 1

            # Execute stream of attacks for 3 seconds
            if stream_attack_active and stream_attack_timer > 0:
                if stream_attack_timer % stream_attack_interval == 0:
                    for i in range(3):  # 3 lines of attacks
                        attack_type = random.choice(['red', 'green', 'black', 'purple'])
                        attack_y = i * (height // 4)  # Evenly distribute lines vertically
                        attack_x = width
                        attack_speed = -5
                        enemies.append({'x': attack_x, 'y': attack_y, 'speed': attack_speed, 'type': attack_type})
                stream_attack_timer -= 1
            else:
                stream_attack_active = False

            # Execute stream of attacks for 3 seconds in reverse direction
            if star_powerup_timer > 0:
                if star_powerup_timer % stream_attack_interval == 0:
                    for i in range(3):  # 3 lines of attacks
                        attack_type = random.choice(['red', 'green', 'black', 'purple'])
                        attack_y = i * (height // 4)  # Evenly distribute lines vertically
                        attack_x = 0 - enemy_size
                        attack_speed = 5
                        enemies.append({'x': attack_x, 'y': attack_y, 'speed': attack_speed, 'type': attack_type})
                star_powerup_timer -= 1

            # Increment score every few frames
            if pygame.time.get_ticks() % scoring_rate == 0:
                score += 1

        else:
            screen.fill(white)
            game_over_text = font.render("Game Over!", True, red)
            screen.blit(game_over_text, (width // 2 - 100, height // 2 - 50))
            score_text = font.render(f"Score: {score}", True, blue)
            screen.blit(score_text, (width // 2 - 50, height // 2))
            high_score_text = font.render(f"High Score: {high_score}", True, blue)
            screen.blit(high_score_text, (width // 2 - 80, height // 2 + 50))
            play_again_text = font.render("Press SPACE to play again", True, blue)
            screen.blit(play_again_text, (width // 2 - 150, height // 2 + 100))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_over = False
                start_time = time.time()
                player_x = (width - player_size) // 2
                player_y = height - player_size - 10
                enemies = []
                for _ in range(num_enemies):
                    enemy_x = random.randint(0, width - enemy_size)
                    enemy_y = random.randint(0, height // 2)
                    while (
                        player_x < enemy_x + enemy_size
                        and player_x + player_size > enemy_x
                        and player_y < enemy_y + enemy_size
                        and player_y + player_size > enemy_y
                    ):
                        enemy_x = random.randint(0, width - enemy_size)
                        enemy_y = random.randint(0, height // 2)
                    enemies.append({'x': enemy_x, 'y': enemy_y, 'speed': random.randint(2, 5), 'type': 'red'})
                powerups = []

        if not game_over:
            elapsed_time = time.time() - start_time
            screen.fill(white)
            pygame.draw.rect(screen, blue, (player_x, player_y, player_size, player_size))

            for enemy in enemies:
                if 'type' in enemy:
                    if enemy['type'] == 'red':
                        pygame.draw.rect(screen, red, (enemy['x'], enemy['y'], enemy_size, enemy_size))
                    elif enemy['type'] == 'green':
                        pygame.draw.rect(screen, green, (enemy['x'], enemy['y'], enemy_size, enemy_size))
                    elif enemy['type'] == 'black':
                        pygame.draw.rect(screen, white, (enemy['x'], enemy['y'], enemy_size, enemy_size))
                    elif enemy['type'] == 'purple':
                        pygame.draw.rect(screen, purple, (enemy['x'], enemy['y'], enemy_size, enemy_size))
                else:
                    pygame.draw.rect(screen, red, (enemy['x'], enemy['y'], enemy_size, enemy_size))

            for powerup in powerups:
                if powerup['type'] == 'purple':
                    pygame.draw.rect(screen, purple, (powerup['x'], powerup['y'], player_size, player_size))

            for star in stars:
                pygame.draw.rect(screen, brown, (star['x'], star['y'], player_size, player_size))

            score_text = font.render(f"Score: {score}", True, blue)
            screen.blit(score_text, (10, 10))
            high_score_text = font.render(f"High Score: {high_score}", True, blue)
            screen.blit(high_score_text, (10, 50))

            time_text = font.render(f"Time: {int(elapsed_time)} seconds", True, blue)
            screen.blit(time_text, (10, 90))

            health_bar_text = font.render(f"Health: {player_health}", True, blue)
            screen.blit(health_bar_text, (width - 150, 10))

    else:
        screen.fill(white)
        pause_text = font.render("Paused", True, blue)
        screen.blit(pause_text, (width // 2 - 50, height // 2 - 20))

    pygame.display.flip()
    clock.tick(60)
