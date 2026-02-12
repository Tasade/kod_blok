import streamlit as st
elif cmd == "⬅ Sol":
self.x -= 1


# ---------------- GRID ÇİZİMİ ----------------


def draw_grid(robot, goal=(5,5), size=6):
grid = np.zeros((size, size))


# robot ve hedef işaretleme
if 0 <= robot.y < size and 0 <= robot.x < size:
grid[robot.y][robot.x] = 1


grid[goal[1]][goal[0]] = 2


fig, ax = plt.subplots()
ax.imshow(grid)


for i in range(size):
for j in range(size):
ax.text(j, i, "",
ha="center", va="center")


ax.set_xticks(range(size))
ax.set_yticks(range(size))
ax.grid(True)
st.pyplot(fig)


# ---------------- SESSION STATE ----------------


if "blocks" not in st.session_state:
st.session_state.blocks = []


st.title("🧩 Kod Blok Robot Atölyesi")


# ---------------- BLOK SEÇİM PANELİ ----------------


st.subheader("1️⃣ Blokları Seç")


col1, col2, col3 = st.columns(3)


if col1.button("⬆ İleri"):
st.session_state.blocks.append("⬆ İleri")


if col2.button("➡ Sağ"):
st.session_state.blocks.append("➡ Sağ")


if col3.button("⬅ Sol"):
st.session_state.blocks.append("⬅ Sol")


# ---------------- BLOK SIRASI (SCRATCH TARZI) ----------------


st.subheader("2️⃣ Algoritma Zinciri")


st.write(" → ".join(st.session_state.blocks) if st.session_state.blocks else "Henüz blok yok")


col4, col5 = st.columns(2)


if col4.button("🗑 Temizle"):
st.session_state.blocks = []


# ---------------- ANİMASYON ----------------


st.subheader("3️⃣ Simülasyonu Çalıştır")


if col5.button("▶ Çalıştır"):
robot = Robot()
goal = (5,5)


placeholder = st.empty()


for cmd in st.session_state.blocks:
robot.move(cmd)
with placeholder.container():
draw_grid(robot, goal)
time.sleep(0.6)


if (robot.x, robot.y) == goal:
st.success("🎯 Hedefe ulaşıldı!")
else:
st.error("❌ Hedef kaçtı, tekrar dene!")
