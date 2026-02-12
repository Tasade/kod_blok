import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

# ---------------- ROBOT ----------------

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, cmd):
        if cmd == "forward":
            self.y += 1
        elif cmd == "right":
            self.x += 1
        elif cmd == "left":
            self.x -= 1

# ---------------- GRID ----------------

def draw_grid(robot, goal=(5, 5), size=6):
    grid = np.zeros((size, size))

    if 0 <= robot.y < size and 0 <= robot.x < size:
        grid[robot.y][robot.x] = 1

    grid[goal[1]][goal[0]] = 2

    fig, ax = plt.subplots()
    ax.imshow(grid)

    ax.set_xticks(range(size))
    ax.set_yticks(range(size))
    ax.grid(True)

    st.pyplot(fig)

# ---------------- STATE ----------------

if "blocks" not in st.session_state:
    st.session_state.blocks = []

st.title("Kod Blok Robot Atolyesi")

# ---------------- BUTTONS ----------------

col1, col2, col3 = st.columns(3)

if col1.button("Forward"):
    st.session_state.blocks.append("forward")

if col2.button("Right"):
    st.session_state.blocks.append("right")

if col3.button("Left"):
    st.session_state.blocks.append("left")

st.write("Algoritma:", " -> ".join(st.session_state.blocks))

col4, col5 = st.columns(2)

if col4.button("Temizle"):
    st.session_state.blocks = []

# ---------------- RUN ----------------

if col5.button("Calistir"):
    robot = Robot()
    goal = (5, 5)

    placeholder = st.empty()

    for cmd in st.session_state.blocks:
        robot.move(cmd)
        with placeholder.container():
            draw_grid(robot, goal)
        time.sleep(0.5)

    if (robot.x, robot.y) == goal:
        st.success("Hedefe ulasildi!")
    else:
        st.error("Tekrar dene!")
