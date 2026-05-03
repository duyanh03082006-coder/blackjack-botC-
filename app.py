import streamlit as st

st.set_page_config(page_title="Blackjack Decision Tool", layout="wide")

# --- SESSION ---
if "start" not in st.session_state:
    st.session_state.start = False
if "deck" not in st.session_state:
    st.session_state.deck = {}
if "player" not in st.session_state:
    st.session_state.player = []
if "dealer" not in st.session_state:
    st.session_state.dealer = []
if "num_decks" not in st.session_state:
    st.session_state.num_decks = 4

# --- INIT ---
def reset_game():
    cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.deck = {c: 4 * st.session_state.num_decks for c in cards}
    st.session_state.player = []
    st.session_state.dealer = []

def card_value(card):
    if card in ['J','Q','K']: return 10
    if card == 'A': return 11
    return int(card)

def calc_score(hand):
    total = sum(card_value(c) for c in hand)
    aces = hand.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def add_card(target, card):
    if st.session_state.deck[card] > 0:
        st.session_state.deck[card] -= 1
        target.append(card)

def bust_probability(score):
    total_cards = sum(st.session_state.deck.values())
    bust = 0
    for c, count in st.session_state.deck.items():
        val = card_value(c)
        if score + val > 21:
            bust += count
    return bust / total_cards if total_cards > 0 else 0

# --- SETUP ---
if not st.session_state.start:
    st.title("🃏 Blackjack Decision Tool")

    st.session_state.num_decks = st.number_input("Số bộ bài", 1, 8, 4)

    if st.button("🚀 Bắt đầu", use_container_width=True):
        reset_game()
        st.session_state.start = True
        st.rerun()

# --- MAIN ---
else:
    st.title("🎯 Quyết định rút bài")

    # --- HIỂN THỊ BÀI ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧑 Bạn")
        st.write(st.session_state.player)
        p_score = calc_score(st.session_state.player)
        st.metric("Điểm", p_score)

    with col2:
        st.subheader("🎩 Dealer")
        st.write(st.session_state.dealer)
        d_score = calc_score(st.session_state.dealer)
        st.metric("Điểm (hiện tại)", d_score)

    st.divider()

    # --- PHÂN TÍCH ---
    if st.session_state.player:
        bust_prob = bust_probability(p_score)

        st.write(f"💀 Xác suất BUST nếu rút: **{bust_prob*100:.1f}%**")

        if bust_prob > 0.5:
            st.error("❌ NÊN DỪNG")
        elif bust_prob < 0.3:
            st.success("✅ NÊN RÚT")
        else:
            st.info("⚖️ CÂN NHẮC")

    st.divider()

    # --- INPUT MODE ---
    mode = st.radio("Thêm bài cho:", ["Bạn", "Dealer"], horizontal=True)

    target = st.session_state.player if mode == "Bạn" else st.session_state.dealer

    st.write("### 👇 Chọn lá bài")

    cards = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

    cols = st.columns(3)

    for i, c in enumerate(cards):
        with cols[i % 3]:
            if st.button(c, key=f"{mode}_{c}", use_container_width=True):
                add_card(target, c)
                st.rerun()

    st.divider()

    # --- ACTION ---
    c1, c2 = st.columns(2)

    with c1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.start = False
            st.rerun()

    with c2:
        if st.button("↩️ Undo", use_container_width=True):
            if mode == "Bạn" and st.session_state.player:
                last = st.session_state.player.pop()
                st.session_state.deck[last] += 1
            elif mode == "Dealer" and st.session_state.dealer:
                last = st.session_state.dealer.pop()
                st.session_state.deck[last] += 1
            st.rerun()