import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, cmd):
        if cmd == "forward": self.y += 1
        elif cmd == "right": self.x += 1
        elif cmd == "left": self.x -= 1

LEVELS = {
    1: {"goal": (3, 3), "obstacles": []},
    2: {"goal": (4, 4), "obstacles": [(2, 2), (1, 3)]},
    3: {"goal": (5, 5), "obstacles": [(2, 2), (3, 2), (2, 3)]},
}

def draw_grid(robot, level, size=6):
    data = LEVELS[level]
    goal = data["goal"]
    obstacles = data["obstacles"]
    grid = np.zeros((size, size))

    for ox, oy in obstacles: grid[oy][ox] = -1
    if 0 <= robot.y < size and 0 <= robot.x < size: grid[robot.y][robot.x] = 1
    grid[goal[1]][goal[0]] = 2

    fig, ax = plt.subplots()
    ax.imshow(grid)
    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True)
    return fig

if "blocks" not in st.session_state: st.session_state.blocks = []
if "score" not in st.session_state: st.session_state.score = 0
if "preview_robot" not in st.session_state: st.session_state.preview_robot = Robot()

st.title("Kod Blok Robot Oyunu")

level = st.selectbox("Seviye Sec", [1, 2, 3])

st.subheader("Oyun Alani")

grid_placeholder = st.empty()
fig = draw_grid(st.session_state.preview_robot, level)
grid_placeholder.pyplot(fig)

st.subheader("Kontrol Paneli")

b1, b2, b3, b4, b5 = st.columns(5)

if b1.button("Forward"): st.session_state.blocks.append("forward")
if b2.button("Right"): st.session_state.blocks.append("right")
if b3.button("Left"): st.session_state.blocks.append("left")
if b4.button("Temizle"): st.session_state.blocks = []

st.write("Algoritma:", " -> ".join(st.session_state.blocks) or "(Bos)")

if b5.button("Calistir"):
    robot = Robot()
    st.session_state.preview_robot = robot

    data = LEVELS[level]
    goal = data["goal"]
    obstacles = data["obstacles"]
    crashed = False

    for cmd in st.session_state.blocks:
        robot.move(cmd)

        if (robot.x, robot.y) in obstacles:
            crashed = True
            break

        fig = draw_grid(robot, level)
        grid_placeholder.pyplot(fig)
        time.sleep(0.5)

    if crashed:
        st.error("Engele carptin!")
    elif (robot.x, robot.y) == goal:
        gained = max(10 - len(st.session_state.blocks), 1)
        st.session_state.score += gained
        st.success(f"Hedefe ulasildi! +{gained} puan")
    else:
        st.warning("Hedefe ulasilamadi")

st.subheader(f"Toplam Skor: {st.session_state.score}")
