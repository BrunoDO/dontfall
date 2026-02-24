import pygame
import random
import os
import streamlit as st
import numpy as np
import time

# 1. SETUP PAGE
st.set_page_config(layout="centered", page_title="Turbo Faller")
st.title("🚀 Turbo Faller")

# 2. SESSION STATE INITIALIZATION
if 'game' not in st.session_state:
    st.session_state.game = {
        'px': 200, 'py': 100, 
        'vx': 0, 'vy': 0, 
        'score': 0,
        'platforms': [[random.randint(0, 300), i] for i in range(100, 600, 150)]
    }

# 3. HEADLESS RENDERER
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
WIDTH, HEIGHT = 400, 600
# We use a Surface instead of a display to prevent "Video system not initialized"
canvas = pygame.Surface((WIDTH, HEIGHT))

# 4. CONTROLS (Using columns for layout)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ LEFT"): st.session_state.game['vx'] -= 8
with col2:
    if st.button("🔄 RESET"):
        del st.session_state.game
        st.rerun()
with col3:
    if st.button("RIGHT ➡️"): st.session_state.game['vx'] += 8

# 5. PHYSICS & LOGIC
g = st.session_state.game
g['vy'] += 1.2  # Gravity
g['vx'] *= 0.8  # Friction
g['px'] += g['vx']
g['py'] += g['vy']

# Platform Logic
for p in g['platforms']:
    p[1] -= 4  # Rising speed
    if p[1] < 0:
        p[1] = HEIGHT
        p[0] = random.randint(0, 300)
        g['score'] += 1
    
    # Simple Collision
    if (g['py'] + 30 >= p[1] and g['py'] + 30 <= p[1] + 20 and
        g['px'] + 30 >= p[0] and g['px'] <= p[0] + 100 and g['vy'] > 0):
        g['vy'] = -18

# Boundary Check
if g['px'] < 0: g['px'] = 0
if g['px'] > WIDTH-30: g['px'] = WIDTH-30

# 6. DRAWING
canvas.fill((30, 40, 60))
for p in g['platforms']:
    pygame.draw.rect(canvas, (80, 150, 255), (p[0], p[1], 100, 15), border_radius=4)
pygame.draw.rect(canvas, (255, 60, 90), (g['px'], g['py'], 30, 30), border_radius=6)

# 7. DISPLAY TO STREAMLIT
img = pygame.surfarray.array3d(canvas)
img = np.transpose(img, (1, 0, 2))
st.image(img, use_container_width=True)
st.write(f"### Score: {g['score']}")

# Lose Condition
if g['py'] > HEIGHT:
    st.error("GAME OVER!")
    time.sleep(1)
    del st.session_state.game
    st.rerun()

# 8. AUTO-TICK (The Secret Sauce)
# This causes the page to refresh itself every 100ms
time.sleep(0.1)
st.rerun()