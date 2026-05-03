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

# --- PIXEL CARD ---
def render_cards(cards):
    html = ""
    for c in cards:
        color = "red" if c in ['10','J','Q','K','A'] else "black"

        html += f"""
        <div style="
            display:inline-block;
            width:40px;
            height:55px;
            margin:3px;
            border:2px solid black;
            border-radius:4px;
            background:white;
            font-family:monospace;
            font-size:16px;
            font-weight:bold;
            color:{color};
            text-align:center;
            line-height:55px;
            box-shadow:2px 2px 0px #000;
        ">
            {c}
        </div>
        """
    return html

# --- SETUP ---
if not st.session_state.start:
    st.title("🃏 Blackjack Pro Tool")

    st.session_state.num_decks = st.number_input("Số bộ bài", 1, 8, 4)

    if st.button("🚀 Bắt đầu", use_container_width=True):
        reset()
        st.session_state.start = True
        st.rerun()

# --- MAIN ---
else:
    left, right = st.columns([1,1])

    # ================= LEFT =================
    with left:
        st.write("### 👇 Chọn lá bài")

        mode = st.radio("Thêm vào:", ["Bạn", "Dealer", "Bài đã ra"], horizontal=True)

        cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

        st.markdown("""
        <style>
        .small-btn button {
            height: 45px;
            font-size: 16px;
            margin: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

        cols = st.columns(3)

        for i, c in enumerate(cards):
            with cols[i % 3]:
                st.markdown('<div class="small-btn">', unsafe_allow_html=True)
                if st.button(c, key=f"{mode}_{c}", use_container_width=True):
                    if mode == "Bạn":
                        draw(st.session_state.player, c)
                    elif mode == "Dealer":
                        draw(st.session_state.dealer, c)
                    else:
                        add_seen(c)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # ================= RIGHT =================
    with right:
        st.write("### 🧑 Bạn")
        st.markdown(render_cards(st.session_state.player), unsafe_allow_html=True)
        p = score(st.session_state.player)
        st.metric("Điểm", p)

        st.write("### 🎩 Dealer")
        st.markdown(render_cards(st.session_state.dealer), unsafe_allow_html=True)
        d = score(st.session_state.dealer)
        st.metric("Điểm", d)

        st.write("### 🧾 Bài đã ra")
        st.markdown(render_cards(st.session_state.seen), unsafe_allow_html=True)

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

    # --- ACTION ---
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        if st.button("↩️ Undo", use_container_width=True):
            if st.session_state.player:
                last = st.session_state.player.pop()
                st.session_state.deck[last] += 1
            st.rerun()

    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.start = False
            st.rerun()