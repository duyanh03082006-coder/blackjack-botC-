import streamlit as st
import pandas as pd

st.set_page_config(page_title="Blackjack Bot Pro++", layout="wide")

st.title("🃏 Blackjack Bot Pro++")
st.subheader("Tool đếm bài + gợi ý chiến thuật")

# --- INIT ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'num_decks' not in st.session_state:
    st.session_state.num_decks = 1
if 'current_shoe' not in st.session_state:
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.current_shoe = {v: 4 for v in values}

# --- FUNCTIONS ---
def reset_game():
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.current_shoe = {v: 4 * st.session_state.num_decks for v in values}
    st.session_state.history = []

def add_card(val):
    if st.session_state.current_shoe[val] > 0:
        st.session_state.current_shoe[val] -= 1
        st.session_state.history.append(val)

def undo():
    if st.session_state.history:
        last = st.session_state.history.pop()
        st.session_state.current_shoe[last] += 1

def card_value(card):
    if card in ['J','Q','K']:
        return 10
    if card == 'A':
        return 11
    return int(card)

def hand_total(cards):
    total = sum(card_value(c) for c in cards)
    aces = cards.count('A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def running_count():
    count = 0
    for c in st.session_state.history:
        if c in ['2','3','4','5','6']:
            count += 1
        elif c in ['10','J','Q','K','A']:
            count -= 1
    return count

def bust_probability(player_cards):
    total = hand_total(player_cards)
    total_cards = sum(st.session_state.current_shoe.values())
    
    bust_cards = 0
    for card, count in st.session_state.current_shoe.items():
        if count > 0:
            new_total = hand_total(player_cards + [card])
            if new_total > 21:
                bust_cards += count
    
    return bust_cards / total_cards if total_cards > 0 else 0

def suggest_action(player_cards, dealer_card):
    total = hand_total(player_cards)
    
    if total <= 11:
        return "HIT"
    if total >= 17:
        return "STAND"
    
    if 12 <= total <= 16:
        if dealer_card in ['7','8','9','10','A']:
            return "HIT"
        else:
            return "STAND"
    
    return "HIT"

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Cài đặt")
    new_decks = st.number_input("Số bộ bài", 1, 8, st.session_state.num_decks)
    if new_decks != st.session_state.num_decks:
        st.session_state.num_decks = new_decks
        reset_game()
    
    if st.button("Reset"):
        reset_game()
    if st.button("Undo"):
        undo()

# --- UI ---
values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

st.write("### Chọn lá bài:")
cols = st.columns(7)
for i, v in enumerate(values):
    with cols[i % 7]:
        if st.button(v):
            add_card(v)

st.divider()

# --- PLAYER INPUT ---
st.write("### Nhập bài của bạn")
player_input = st.text_input("Ví dụ: 10,A hoặc 9,7")
dealer_card = st.selectbox("Lá nhà cái", values)

player_cards = [x.strip() for x in player_input.split(",") if x.strip() in values]

# --- STATS ---
total_cards = sum(st.session_state.current_shoe.values())
rc = running_count()
remaining_decks = total_cards / 52
true_count = rc / remaining_decks if remaining_decks > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("🧮 Running Count", rc)
col2.metric("🎯 True Count", round(true_count, 2))
col3.metric("🃏 Còn lại", total_cards)

# --- ANALYSIS ---
if player_cards:
    total = hand_total(player_cards)
    bust_prob = bust_probability(player_cards)
    action = suggest_action(player_cards, dealer_card)

    st.write(f"### Tổng điểm: **{total}**")
    st.write(f"💥 Xác suất bust nếu rút: **{round(bust_prob*100,2)}%**")
    
    if action == "HIT":
        st.warning("👉 NÊN RÚT (HIT)")
    else:
        st.success("👉 NÊN DỪNG (STAND)")

# --- TABLE ---
data = []
for v in values:
    count = st.session_state.current_shoe[v]
    prob = count / total_cards * 100 if total_cards else 0
    data.append({"Lá": v, "Còn": count, "%": round(prob,2)})

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

# --- HISTORY ---
with st.expander("Lịch sử"):
    st.write(", ".join(st.session_state.history))
