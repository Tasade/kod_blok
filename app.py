import streamlit as st

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, command):
        if command == "forward":
            self.y += 1
        elif command == "right":
            self.x += 1
        elif command == "left":
            self.x -= 1

st.title("Kod Blok Robot Simülasyonu")

commands = st.text_input(
    "Komutları gir (forward,right,left):",
    "forward,right,forward"
)

if st.button("Çalıştır"):
    robot = Robot()

    for cmd in commands.split(","):
        robot.move(cmd.strip())

    st.success(f"Robot konumu: ({robot.x}, {robot.y})")
