import pygame
import random
import os

# --- 1. SETUP & CONSTANTS ---
WIDTH, HEIGHT = 400, 600
PLAYER_SIZE = 30
PLATFORM_HEIGHT = 15
SKY_BLUE = (30, 40, 60)   
ACCENT_RED = (255, 60, 90) 
WHITE = (240, 240, 240)
GOLD = (255, 215, 0) # For bonus text

# --- 2. INITIALIZATION ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turbo Faller: High-Stakes Edition")
clock = pygame.time.Clock()
font_main = pygame.font.SysFont("Verdana", 40, bold=True)
font_small = pygame.font.SysFont("Verdana", 18, bold=True)
font_bonus = pygame.font.SysFont("Verdana", 24, bold=True)

state = "MENU"

def load_high_score():
    try:
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
    except Exception:
        return 0
    return 0

def save_high_score(new_high):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(new_high))
    except Exception as e:
        print(f"Could not save score: {e}")

high_score = load_high_score()

def reset_game():
    return (
        pygame.Rect(WIDTH // 2 - 15, 100, PLAYER_SIZE, PLAYER_SIZE), 
        0, 0, 0, 0,
        [pygame.Rect(random.randint(0, WIDTH-100), i, 100, PLATFORM_HEIGHT) for i in range(100, HEIGHT, 120)],
        [], # trail
        100, # last_jump_y (to track fall distance)
        []   # floating_texts (for bonus popups)
    )

player, player_vel_y, player_vel_x, score, shake, platforms, trail, last_jump_y, float_texts = reset_game()

# --- 4. MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if state in ["MENU", "GAME_OVER"]:
                player, player_vel_y, player_vel_x, score, shake, platforms, trail, last_jump_y, float_texts = reset_game()
                state = "PLAYING"

    if state == "MENU":
        screen.fill(SKY_BLUE)
        screen.blit(font_main.render("TURBO FALLER", True, WHITE), (WIDTH//2 - 140, 220))
        screen.blit(font_small.render("PRESS SPACE", True, (150, 160, 180)), (WIDTH//2 - 70, 300))

    elif state == "GAME_OVER":
        screen.fill((20, 20, 25))
        screen.blit(font_main.render("CRASHED", True, ACCENT_RED), (WIDTH//2 - 100, 220))
        screen.blit(font_small.render(f"FINAL: {score} | BEST: {high_score}", True, WHITE), (WIDTH//2 - 110, 300))

    elif state == "PLAYING":
        level = score / 20  
        current_speed = min(7.5, 2.4 + (level * 1.2))
        current_gravity = min(2.1, 0.75 + (level * 0.15))
        current_jump = max(-21, -15 - (level * 1.1))
        
        # 1. Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_vel_x -= (1.3 + level*0.2)
        elif keys[pygame.K_RIGHT]: player_vel_x += (1.3 + level*0.2)
        else: player_vel_x *= 0.88
        player_vel_x = max(-13, min(13, player_vel_x))
        player.x += player_vel_x

        # 2. Trail & Wall Bounce
        trail.append(player.copy()); 
        if len(trail) > 6: trail.pop(0)
        if player.left < 0 or player.right > WIDTH:
            player.left = 0 if player.left < 0 else WIDTH - PLAYER_SIZE
            player_vel_x *= -1.1; shake = 3

        # 3. Vertical & Ceiling
        player_vel_y += current_gravity
        player.y += player_vel_y
        if player.top < 0: player.top, player_vel_y, shake = 0, 4, 2

        # 4. Collision & Scoring Logic
        for plat in platforms:
            plat.y -= current_speed
            if plat.y < -PLATFORM_HEIGHT:
                plat.y, plat.width, plat.x = HEIGHT, max(40, 100 - (score//5)*7), random.randint(0, WIDTH-40)
                # Standard point for clearing a platform
                score += 1

            if player.colliderect(plat) and player_vel_y > 0:
                if player.bottom <= plat.bottom + 15:
                    # --- SCORING CALCULATIONS ---
                    fall_dist = player.y - last_jump_y
                    points_to_add = 1
                    msg = ""

                    # Distance Bonus (Every 200 pixels of falling adds a point)
                    if fall_dist > 200:
                        bonus = int(fall_dist // 200)
                        points_to_add += bonus
                        msg += f"FALL +{bonus} "

                    # Center Bonus (Middle 30% of platform)
                    plat_center = plat.x + plat.width/2
                    if abs(player.centerx - plat_center) < plat.width * 0.15:
                        points_to_add *= 2
                        msg += "PERFECT 2x"
                        shake = 10 # Big shake for perfect landing

                    score += points_to_add
                    if msg: float_texts.append({"y": player.y, "x": player.x, "t": msg, "life": 40})
                    
                    # Reset jump state
                    player.bottom, player_vel_y = plat.top, current_jump
                    last_jump_y = player.y
                    shake = max(shake, 3)

                elif player_vel_y < 0 and player.top >= plat.top:
                    player.top, player_vel_y, shake = plat.bottom, 4, 2

        # 5. UI & Floating Text Logic
        for ft in float_texts[:]:
            ft["y"] -= 2; ft["life"] -= 1
            if ft["life"] <= 0: float_texts.remove(ft)

        if player.top > HEIGHT:
            if score > high_score: 
                high_score = score
                with open("highscore.txt", "w") as f: f.write(str(high_score))
            state = "GAME_OVER"

        # 6. Final Render
        shake_off = (random.randint(-shake, shake), random.randint(-shake, shake)) if shake > 0 else (0,0)
        if shake > 0: shake -= 1
        canvas = pygame.Surface((WIDTH, HEIGHT))
        canvas.fill(SKY_BLUE)

        for i, pos in enumerate(trail):
            s = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE)); s.set_alpha((i+1)*30); s.fill(ACCENT_RED)
            canvas.blit(s, pos)

        for plat in platforms:
            pygame.draw.rect(canvas, (min(255, 100+score*5), max(40, 200-score*5), 200), plat, border_radius=4)
        
        pygame.draw.rect(canvas, WHITE, player, border_radius=6)
        
        for ft in float_texts:
            canvas.blit(font_bonus.render(ft["t"], True, GOLD), (ft["x"] - 20, ft["y"] - 20))

        canvas.blit(font_small.render(f"SCORE: {score}", True, WHITE), (20, 20))
        screen.blit(canvas, shake_off)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()