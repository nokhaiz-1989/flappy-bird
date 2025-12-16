import streamlit as st
import time
import random

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Flappy Bird - Streamlit", layout="centered")

# ----------------- GAME CONSTANTS -----------------
GRAVITY = 0.6
FLAP_STRENGTH = -8
PIPE_GAP = 10
PIPE_SPEED = 1

# ----------------- SESSION STATE INIT -----------------
if "bird_y" not in st.session_state:
    st.session_state.bird_y = 10
    st.session_state.velocity = 0
    st.session_state.pipe_x = 30
    st.session_state.pipe_gap_y = random.randint(5, 15)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.started = False

# ----------------- TITLE -----------------
st.title("🐦 Flappy Bird (Streamlit Edition)")

# ----------------- START / RESTART -----------------
if not st.session_state.started:
    if st.button("▶ Start Game"):
        st.session_state.started = True
        st.experimental_rerun()

if st.session_state.game_over:
    st.error("💥 Game Over!")
    if st.button("🔄 Restart"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()

# ----------------- GAME CONTROLS -----------------
if st.session_state.started and not st.session_state.game_over:
    if st.button("🕊 Flap"):
        st.session_state.velocity = FLAP_STRENGTH

# ----------------- GAME LOOP -----------------
if st.session_state.started and not st.session_state.game_over:
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity
    st.session_state.pipe_x -= PIPE_SPEED

    # Reset pipe
    if st.session_state.pipe_x < 0:
        st.session_state.pipe_x = 30
        st.session_state.pipe_gap_y = random.randint(5, 15)
        st.session_state.score += 1

    # Collision detection
    if (
        st.session_state.pipe_x == 5
        and not (
            st.session_state.pipe_gap_y
            < st.session_state.bird_y
            < st.session_state.pipe_gap_y + PIPE_GAP
        )
    ):
        st.session_state.game_over = True

    if st.session_state.bird_y < 0 or st.session_state.bird_y > 25:
        st.session_state.game_over = True

# ----------------- DRAW GAME -----------------
game_area = []

for y in range(25):
    row = [" "] * 30

    # Bird
    if int(st.session_state.bird_y) == y:
        row[5] = "🐦"

    # Pipes
    if st.session_state.pipe_x == y:
        for i in range(25):
            if not (
                st.session_state.pipe_gap_y
                < i
                < st.session_state.pipe_gap_y + PIPE_GAP
            ):
                row[y] = "🟩"

    game_area.append("".join(row))

st.text("\n".join(game_area))

# ----------------- SCORE -----------------
st.markdown(f"### 🏆 Score: {st.session_state.score}")

# ----------------- FRAME RATE -----------------
if st.session_state.started and not st.session_state.game_over:
    time.sleep(0.1)
    st.experimental_rerun()
