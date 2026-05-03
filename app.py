import streamlit as st

st.set_page_config(page_title="Blackjack Pro Tool", layout="wide")

# --- STATE ---
if "start" not in st.session_state:
    st.session_state.start = False
if "deck" not in st.session_state:
    st.session_state.deck = {}
if "player" not in st.session_state:
    st.session_state.player = []
if "dealer" not in st.session_state:
    st.session_state.dealer = []
if "seen" not in st.session_state:
    st.session_state.seen = []
if "num_decks" not in st.session_state:
    st.session_state.num_decks = 4

# --- INIT ---
def reset():
    cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.deck = {c: 4 * st.session_state.num_decks for c in cards}
    st.session_state.player = []
    st.session_state.dealer = []
    st.session_state.seen = []

def value(c):
    if c in ['J','Q','K']: return 10
    if c == 'A': return 11
    return int(c)

def score(hand):
    total = sum(value(c) for c in hand)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def draw(target, c):
    if st.session_state.deck[c] > 0:
        st.session_state.deck[c] -= 1
        target.append(c)

def add_seen(c):
    if st.session_state.deck[c] > 0:
        st.session_state.deck[c] -= 1
        st.session_state.seen.append(c)

def bust_prob(current):
    total = sum(st.session_state.deck.values())
    bust = 0
    for c, cnt in st.session_state.deck.items():
        if current + value(c) > 21:
            bust += cnt
    return bust / total if total else 0

# --- SETUP ---
if not st.session_state.start:
    st.title("🃏 Blackjack Tool Pro")

    st.session_state.num_decks = st.number_input("Số bộ bài", 1, 8, 4)

    if st.button("🚀 Bắt đầu", use_container_width=True):
        reset()
        st.session_state.start = True
        st.rerun()

# --- MAIN ---
else:
    st.title("🎯 Phân tích + Đếm bài")

    # --- HIỂN THỊ ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🧑 Bạn")
        st.write(st.session_state.player)
        p = score(st.session_state.player)
        st.metric("Điểm", p)

    with c2:
        st.subheader("🎩 Dealer")
        st.write(st.session_state.dealer)
        d = score(st.session_state.dealer)
        st.metric("Điểm", d)

    st.divider()

    # --- PHÂN TÍCH ---
    if st.session_state.player:
        prob = bust_prob(p)
        st.write(f"💀 Bust nếu rút: **{prob*100:.1f}%**")

        if prob > 0.5:
            st.error("❌ NÊN DỪNG")
        elif prob < 0.3:
            st.success("✅ NÊN RÚT")
        else:
            st.info("⚖️ CÂN NHẮC")

    st.divider()

    # --- MODE ---
    mode = st.radio("Thêm bài cho:", ["Bạn", "Dealer", "Bài đã ra"], horizontal=True)

    # --- GRID 3 CỘT ---
    st.write("### 👇 Chọn lá bài")

    cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    cols = st.columns(3)

    for i, c in enumerate(cards):
        with cols[i % 3]:
            if st.button(c, key=f"{mode}_{c}", use_container_width=True):
                if mode == "Bạn":
                    draw(st.session_state.player, c)
                elif mode == "Dealer":
                    draw(st.session_state.dealer, c)
                else:
                    add_seen(c)
                st.rerun()

    st.divider()

    # --- INFO ---
    st.write(f"🧾 Bài đã ra: {len(st.session_state.seen)} lá")

    # --- ACTION ---
    c1, c2 = st.columns(2)

    with c1:
        if st.button("↩️ Undo", use_container_width=True):
            if mode == "Bạn" and st.session_state.player:
                last = st.session_state.player.pop()
                st.session_state.deck[last] += 1
            elif mode == "Dealer" and st.session_state.dealer:
                last = st.session_state.dealer.pop()
                st.session_state.deck[last] += 1
            elif mode == "Bài đã ra" and st.session_state.seen:
                last = st.session_state.seen.pop()
                st.session_state.deck[last] += 1
            st.rerun()

    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.start = False
            st.rerun()