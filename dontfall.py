import pygame
import random
import os
import streamlit as st
import numpy as np
import time

# 1. PAGE CONFIG
st.set_page_config(layout="centered", page_title="Turbo Faller")
st.title("🚀 Turbo Faller: Slick Web Edition")

# 2. STATE INITIALIZATION
if 'game' not in st.session_state:
    st.session_state.game = {
        'px': 185, 'py': 100, 
        'vx': 0, 'vy': 0, 
        'score': 0,
        'last_y': 100,
        'platforms': [[random.randint(0, 300), i] for i in range(150, 600, 150)]
    }

# 3. HEADLESS RENDERER SETUP
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
WIDTH, HEIGHT = 400, 600
canvas = pygame.Surface((WIDTH, HEIGHT))
# Use default font since servers lack custom fonts [cite: 7, 12]
font = pygame.font.SysFont(None, 30)

# 4. CONTROLS
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ LEFT"): st.session_state.game['vx'] -= 12
with col2:
    if st.button("🔄 RESET"):
        del st.session_state.game
        st.rerun()
with col3:
    if st.button("RIGHT ➡️"): st.session_state.game['vx'] += 12

# 5. THE GAME ENGINE (Fragment-style loop)
@st.fragment(run_every=0.05) # Updates 20 times per second
def game_loop():
    g = st.session_state.game
    
    # --- PHYSICS & LOGIC ---
    g['vy'] += 1.3  # Gravity
    g['vx'] *= 0.85 # Friction
    g['px'] += g['vx']
    g['py'] += g['vy']

    # Platform Movement & Collision
    for p in g['platforms']:
        p[1] -= 4 # Constant rising speed
        if p[1] < -20:
            p[1] = HEIGHT
            p[0] = random.randint(0, 300)
            g['score'] += 1
        
        # Collision Logic (Top Land & Bottom Bonk)
        # Land on Top
        if (g['py'] + 30 >= p[1] and g['py'] + 30 <= p[1] + 20 and
            g['px'] + 30 >= p[0] and g['px'] <= p[0] + 100 and g['vy'] > 0):
                
                # Bonus calculation
                fall_dist = g['py'] - g['last_y']
                if fall_dist > 200: g['score'] += 2 # Distance bonus!
                
                g['py'] = p[1] - 30
                g['vy'] = -18
                g['last_y'] = g['py']

        # Bonk Bottom
        elif (g['py'] <= p[1] + 15 and g['py'] >= p[1] and
              g['px'] + 30 >= p[0] and g['px'] <= p[0] + 100 and g['vy'] < 0):
                g['py'] = p[1] + 15
                g['vy'] = 5

    # Screen Bounds
    if g['px'] < 0: g['px'] = 0
    if g['px'] > WIDTH-30: g['px'] = WIDTH-30

    # --- DRAWING ---
    canvas.fill((30, 40, 60)) # Slick Space Blue
    
    # Draw Platforms with Color Transition
    p_color = (min(255, 100 + g['score']*5), 150, 200)
    for p in g['platforms']:
        pygame.draw.rect(canvas, p_color, (p[0], p[1], 100, 15), border_radius=4)
    
    # Draw Player
    pygame.draw.rect(canvas, (240, 240, 240), (g['px'], g['py'], 30, 30), border_radius=6)
    
    # --- OUTPUT ---
    img = pygame.surfarray.array3d(canvas)
    img = np.transpose(img, (1, 0, 2))
    st.image(img, use_container_width=True)
    st.write(f"### Score: {g['score']}")

    # Lose Condition
    if g['py'] > HEIGHT:
        st.error("💥 CRASHED!")
        time.sleep(1)
        del st.session_state.game
        st.rerun()

# Run the loop
game_loop()