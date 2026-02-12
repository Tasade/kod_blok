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
    st.pyplot(fig)


if "blocks" not in st.session_state: st.session_state.blocks = []
if "score" not in st.session_state: st.session_state.score = 0


st.title("Kod Blok Robot Oyunu")

level = st.selectbox("Seviye Sec", [1, 2, 3])

col1, col2, col3 = st.columns(3)

if col1.button("Forward"): st.session_state.blocks.append("forward")
if col2.button("Right"): st.session_state.blocks.append("right")
if col3.button("Left"): st.session_state.blocks.append("left")

st.write("Algoritma:", " -> ".join(st.session_state.blocks))

col4, col5 = st.columns(2)

if col4.button("Temizle"): st.session_state.blocks = []

if col5.button("Calistir"):
    robot = Robot()
    data = LEVELS[level]
    goal = data["goal"]
    obstacles = data["obstacles"]
    placeholder = st.empty()
    crashed = False

    for cmd in st.session_state.blocks:
        robot.move(cmd)

        if (robot.x, robot.y) in obstacles:
            crashed = True
            break

        with placeholder.container(): draw_grid(robot, level)

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
