import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Flappy Bird", layout="centered")

# ---------------- CONSTANTS ----------------
GRAVITY = 0.5
FLAP = -7
PIPE_GAP = 6
PIPE_SPEED = 1
WIDTH = 30
HEIGHT = 20
BIRD_X = 5

# ---------------- INITIALIZE ----------------
def init_game():
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipe_x = WIDTH
    st.session_state.pipe_gap = random.randint(4, HEIGHT - PIPE_GAP - 2)
    st.session_state.score = 0
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.flap = False


if "bird_y" not in st.session_state:
    init_game()

# ---------------- KEYBOARD LISTENER ----------------
st.components.v1.html(
    """
    <script>
    document.addEventListener("keydown", function(e) {
        if (e.key === "ArrowUp") {
            window.parent.postMessage("FLAP", "*");
        }
    });
    </script>
    """,
    height=0,
)

# Receive key press
msg = st.experimental_get_query_params()
if "flap" in st.session_state and st.session_state.flap:
    st.session_state.velocity = FLAP
    st.session_state.flap = False

# ---------------- GAME LOGIC ----------------
def update():
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity
    st.session_state.pipe_x -= PIPE_SPEED

    if st.session_state.pipe_x < 0:
        st.session_state.pipe_x = WIDTH
        st.session_state.pipe_gap = random.randint(4, HEIGHT - PIPE_GAP - 2)
        st.session_state.score += 1

    # Collision
    if st.session_state.pipe_x == BIRD_X:
        if not (st.session_state.pipe_gap <
                st.session_state.bird_y <
                st.session_state.pipe_gap + PIPE_GAP):
            st.session_state.game_over = True

    if st.session_state.bird_y <= 0 or st.session_state.bird_y >= HEIGHT:
        st.session_state.game_over = True


def draw():
    screen = []
    for y in range(HEIGHT):
        row = [" "] * WIDTH

        if int(st.session_state.bird_y) == y:
            row[BIRD_X] = "🐦"

        if st.session_state.pipe_x == y:
            for i in range(HEIGHT):
                if not (st.session_state.pipe_gap <
                        i <
                        st.session_state.pipe_gap + PIPE_GAP):
                    row[y] = "🟩"

        screen.append("".join(row))

    st.text("\n".join(screen))


# ---------------- UI ----------------
st.title("🐦 Flappy Bird — Arrow Key Version")
st.markdown(f"### 🏆 Score: {st.session_state.score}")
st.caption("Press ⬆️ Arrow Key to flap")

if not st.session_state.started:
    if st.button("▶ Start Game"):
        st.session_state.started = True
        st.rerun()

if st.session_state.game_over:
    st.error("💥 Game Over")
    if st.button("🔄 Restart"):
        init_game()
        st.rerun()

if st.session_state.started and not st.session_state.game_over:
    update()
    draw()
    time.sleep(0.1)
    st.rerun()
