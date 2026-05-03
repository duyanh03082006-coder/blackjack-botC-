import streamlit as st

st.set_page_config(layout="wide")

# --- INIT ---
if "started" not in st.session_state:
    st.session_state.started = False

if "num_decks" not in st.session_state:
    st.session_state.num_decks = 1

if "num_players" not in st.session_state:
    st.session_state.num_players = 1

if "shoe" not in st.session_state:
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.shoe = {v: 4 for v in values}

if "history" not in st.session_state:
    st.session_state.history = []

# --- FUNCTIONS ---
def init_shoe():
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.shoe = {v: 4 * st.session_state.num_decks for v in values}
    st.session_state.history = []

def add_card(card):
    if st.session_state.shoe[card] > 0:
        st.session_state.shoe[card] -= 1
        st.session_state.history.append(card)

def running_count():
    count = 0
    for c in st.session_state.history:
        if c in ['2','3','4','5','6']:
            count += 1
        elif c in ['10','J','Q','K','A']:
            count -= 1
    return count

# --- SCREEN 1 ---
if not st.session_state.started:

    st.title("🃏 Blackjack Setup")

    st.session_state.num_decks = st.number_input("Số bộ bài", 1, 8, 1)
    st.session_state.num_players = st.number_input("Số người chơi", 1, 6, 1)

    if st.button("🚀 Bắt đầu", use_container_width=True):
        init_shoe()
        st.session_state.started = True
        st.rerun()

# --- SCREEN 2 ---
else:
    st.title("🎰 Blackjack Live")

    # Stats
    total_cards = sum(st.session_state.shoe.values())
    rc = running_count()
    decks_left = total_cards / 52
    tc = rc / decks_left if decks_left > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("🃏 Còn lại", total_cards)
    col2.metric("🧮 Count", rc)
    col3.metric("🎯 True Count", round(tc,2))

    st.divider()

    # Buttons BIG
    st.write("### 👇 Bấm lá bài vừa ra")

    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    cols = st.columns(4)

    for i, v in enumerate(values):
        with cols[i % 4]:
            if st.button(v, use_container_width=True):
                add_card(v)
                st.rerun()

    st.divider()

    # Quick suggestion
    if tc > 2:
        st.success("🔥 NÊN ĐÁNH MẠNH (nhiều 10/A)")
    elif tc < -1:
        st.warning("⚠️ CẨN THẬN (nhiều lá nhỏ)")
    else:
        st.info("😐 Bình thường")

    # Reset
    if st.button("🔄 Chơi lại"):
        st.session_state.started = False
        st.rerun()
