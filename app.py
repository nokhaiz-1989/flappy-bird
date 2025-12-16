import streamlit as st
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Flappy Bird", layout="centered")

# ---------------- CONSTANTS ----------------
GRAVITY = 0.6
FLAP_STRENGTH = -8
PIPE_GAP = 6
PIPE_SPEED = 1
SCREEN_HEIGHT = 20
SCREEN_WIDTH = 30
BIRD_X = 5


# ---------------- FUNCTIONS ----------------
def init_game():
    st.session_state.bird_y = SCREEN_HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipe_x = SCREEN_WIDTH
    st.session_state.pipe_gap_y = random.randint(4, SCREEN_HEIGHT - PIPE_GAP - 2)
    st.session_state.score = 0
    st.session_state.started = False
    st.session_state.game_over = False


def flap():
    st.session_state.velocity = FLAP_STRENGTH


def update_game():
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity
    st.session_state.pipe_x -= PIPE_SPEED

    # Pipe reset
    if st.session_state.pipe_x < 0:
        st.session_state.pipe_x = SCREEN_WIDTH
        st.session_state.pipe_gap_y = random.randint(4, SCREEN_HEIGHT - PIPE_GAP - 2)
        st.session_state.score += 1

    # Collision with pipe
    if st.session_state.pipe_x == BIRD_X:
        if not (
            st.session_state.pipe_gap_y
            < st.session_state.bird_y
            < st.session_state.pipe_gap_y + PIPE_GAP
        ):
            st.session_state.game_over = True

    # Ground / ceiling collision
    if st.session_state.bird_y <= 0 or st.session_state.bird_y >= SCREEN_HEIGHT:
        st.session_state.game_over = True


def draw_game():
    screen = []

    for y in range(SCREEN_HEIGHT):
        row = [" "] * SCREEN_WIDTH

        # Bird
        if int(st.session_state.bird_y) == y:
            row[BIRD_X] = "🐦"

        # Pipe
        if st.session_state.pipe_x == y:
            for i in range(SCREEN_HEIGHT):
                if not (
                    st.session_state.pipe_gap_y
                    < i
                    < st.session_state.pipe_gap_y + PIPE_GAP
                ):
                    row[y] = "🟩"

        screen.append("".join(row))

    st.text("\n".join(screen))


# ---------------- INITIALIZE ----------------
if "bird_y" not in st.session_state:
    init_game()

# ---------------- UI ----------------
st.title("🐦 Flappy Bird (Functional Version)")
st.markdown(f"### 🏆 Score: {st.session_state.score}")

if not st.session_state.started:
    if st.button("▶ Start"):
        st.session_state.started = True
        st.rerun()

if st.session_state.game_over:
    st.error("💥 Game Over")
    if st.button("🔄 Restart"):
        init_game()
        st.rerun()

if st.session_state.started and not st.session_state.game_over:
    if st.button("🕊 Flap"):
        flap()

    update_game()
    draw_game()

    time.sleep(0.1)
    st.rerun()
