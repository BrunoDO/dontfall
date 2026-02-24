import pygame
import random
import os
import streamlit as st
import numpy as np

# --- 1. STREAMLIT SETUP ---
st.set_page_config(layout="centered", page_title="Turbo Faller")
st.title("🚀 Turbo Faller: Online Edition")
# Placeholders for the game screen and input
frame_placeholder = st.empty()
input_placeholder = st.empty()

# --- 2. SETUP & CONSTANTS ---
WIDTH, HEIGHT = 400, 600
PLAYER_SIZE = 30
PLATFORM_HEIGHT = 15
SKY_BLUE = (30, 40, 60)   
ACCENT_RED = (255, 60, 90) 
WHITE = (240, 240, 240)

# Headless Pygame Env
os.environ["SDL_VIDEODRIVER"] = "dummy" 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Use default font for Streamlit compatibility
font_small = pygame.font.SysFont(None, 24)

# --- 3. GAME STATE ---
if 'game_state' not in st.session_state:
    st.session_state.player = pygame.Rect(WIDTH // 2 - 15, 100, PLAYER_SIZE, PLAYER_SIZE)
    st.session_state.platforms = [pygame.Rect(random.randint(0, WIDTH-100), i, 100, PLATFORM_HEIGHT) for i in range(100, HEIGHT, 120)]
    st.session_state.score = 0
    st.session_state.vel_y = 0
    st.session_state.vel_x = 0

# --- 4. WEB INPUT ---
# Streamlit uses buttons/sliders for web input since it can't "hold" keys easily
col1, col2, col3 = st.columns(3)
with col1:
    move_left = st.button("⬅️ Left")
with col2:
    reset = st.button("🔄 Reset")
with col3:
    move_right = st.button("Right ➡️")

if reset:
    st.session_state.clear()
    st.rerun()

# --- 5. GAME LOGIC ---
# Adjust velocity based on buttons
if move_left: st.session_state.vel_x -= 5
if move_right: st.session_state.vel_x += 5
st.session_state.vel_x *= 0.9 # Friction

# Gravity and Physics
st.session_state.vel_y += 0.8
st.session_state.player.x += st.session_state.vel_x
st.session_state.player.y += st.session_state.vel_y

# Platform Movement
for plat in st.session_state.platforms:
    plat.y -= 3
    if plat.y < 0:
        plat.y = HEIGHT
        plat.x = random.randint(0, WIDTH-100)
        st.session_state.score += 1
    
    if st.session_state.player.colliderect(plat) and st.session_state.vel_y > 0:
        st.session_state.player.bottom = plat.top
        st.session_state.vel_y = -15

# --- 6. RENDER TO WEB ---
screen.fill(SKY_BLUE)
for plat in st.session_state.platforms:
    pygame.draw.rect(screen, (100, 200, 255), plat)
pygame.draw.rect(screen, ACCENT_RED, st.session_state.player)

# Convert Pygame surface to RGB array for Streamlit
img_array = pygame.surfarray.array3d(screen)
img_array = np.transpose(img_array, (1, 0, 2))
frame_placeholder.image(img_array, caption=f"Score: {st.session_state.score}")

# Auto-refresh the app
st.button("Tick Game") # Temporary trigger for testing