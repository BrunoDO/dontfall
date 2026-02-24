import pygame
import random
import os
import streamlit as st
import numpy as np
import time

# --- 1. SESSION STATE (The Game's Memory) ---
if 'initialized' not in st.session_state:
    st.session_state.player_y = 100
    st.session_state.player_x = 200
    st.session_state.vel_y = 0
    st.session_state.vel_x = 0
    st.session_state.score = 0
    st.session_state.platforms = [[random.randint(0, 300), i] for i in range(100, 600, 120)]
    st.session_state.initialized = True

# --- 2. HEADLESS SETUP ---
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.Surface((WIDTH, HEIGHT)) # Use a Surface, not a display window
frame_placeholder = st.empty()

# --- 3. CONTROLS ---
# Use columns for a clean layout
col1, col2, col3 = st.columns(3)
with col1:
    move_l = st.button("⬅️ Left")
with col2:
    if st.button("🔄 Reset"):
        del st.session_state.initialized
        st.rerun()
with col3:
    move_r = st.button("Right ➡️")

# --- 4. THE LIVE GAME LOOP ---
# This loop runs continuously on the Streamlit server
while True:
    # Handle Input
    if move_l: st.session_state.vel_x -= 4
    if move_r: st.session_state.vel_x += 4
    st.session_state.vel_x *= 0.9 # Friction
    
    # Physics
    st.session_state.vel_y += 0.8 # Gravity
    st.session_state.player_x += st.session_state.vel_x
    st.session_state.player_y += st.session_state.vel_y
    
    # Screen Wrap/Bounds
    if st.session_state.player_x < 0: st.session_state.player_x = 0
    if st.session_state.player_x > WIDTH - 30: st.session_state.player_x = WIDTH - 30

    # Platform Logic
    for p in st.session_state.platforms:
        p[1] -= 3 # Platforms rise
        if p[1] < 0:
            p[1] = HEIGHT
            p[0] = random.randint(0, 300)
            st.session_state.score += 1
        
        # Collision (Player Y + Size)
        if (st.session_state.player_y + 30 >= p[1] and 
            st.session_state.player_y + 30 <= p[1] + 15 and
            st.session_state.player_x + 30 >= p[0] and 
            st.session_state.player_x <= p[0] + 100 and 
            st.session_state.vel_y > 0):
                st.session_state.vel_y = -16 # Jump!

    # --- 5. DRAWING ---
    screen.fill((30, 40, 60)) # Dark Sky
    # Draw Platforms
    for p in st.session_state.platforms:
        pygame.draw.rect(screen, (80, 150, 255), (p[0], p[1], 100, 15), border_radius=4)
    # Draw Player
    pygame.draw.rect(screen, (255, 60, 90), (st.session_state.player_x, st.session_state.player_y, 30, 30), border_radius=6)
    
    # --- 6. OUTPUT TO WEB ---
    img = pygame.surfarray.array3d(screen)
    img = np.transpose(img, (1, 0, 2))
    frame_placeholder.image(img, caption=f"Score: {st.session_state.score}", use_container_width=True)
    
    # Lose Condition
    if st.session_state.player_y > HEIGHT:
        st.error(f"GAME OVER! Score: {st.session_state.score}")
        time.sleep(2)
        del st.session_state.initialized
        st.rerun()

    # Control the speed of the loop
    time.sleep(0.03)