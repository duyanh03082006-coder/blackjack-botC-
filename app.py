import streamlit as st
import pandas as pd

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Blackjack Analytics Pro", layout="wide")

# --- KHỞI TẠO DỮ LIỆU ---
if "started" not in st.session_state:
    st.session_state.started = False
if "shoe" not in st.session_state:
    st.session_state.shoe = {}
if "history" not in st.session_state:
    st.session_state.history = []

# --- HÀM HỖ TRỢ ---
def init_game(num_decks):
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.shoe = {v: 4 * num_decks for v in values}
    st.session_state.history = []

def record_cards(cards):
    for card in cards:
        if card and st.session_state.shoe[card] > 0:
            st.session_state.shoe[card] -= 1
            st.session_state.history.append(card)

def get_counts():
    rc = 0
    for c in st.session_state.history:
        if c in ['2','3','4','5','6']: rc += 1
        elif c in ['10','J','Q','K','A']: rc -= 1
    
    total_left = sum(st.session_state.shoe.values())
    decks_left = max(total_left / 52, 0.5)
    tc = rc / decks_left
    return rc, tc, total_left

# --- MÀN HÌNH 1: SETUP ---
if not st.session_state.started:
    st.title("🃏 Blackjack Setup")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        num_decks = st.number_input("Số bộ bài", 1, 8, 4)
    with col_s2:
        num_players = st.number_input("Số người chơi (không tính cái)", 1, 5, 1)
    
    if st.button("🚀 BẮT ĐẦU VÁN MỚI", use_container_width=True):
        st.session_state.num_decks = num_decks
        st.session_state.num_players = num_players
        init_game(num_decks)
        st.session_state.started = True
        st.rerun()

# --- MÀN HÌNH 2: LIVE TRACKING ---
else:
    rc, tc, total_left = get_counts()
    
    # --- SIDEBAR: THỐNG KÊ & BIỂU ĐỒ ---
    with st.sidebar:
        st.header("📊 Thống kê bộ bài")
        st.metric("True Count", round(tc, 2), delta=round(tc, 1))
        st.write(f"Bài còn lại: {total_left} lá")
        
        # Tạo dữ liệu biểu đồ
        df_chart = pd.DataFrame({
            "Lá bài": list(st.session_state.shoe.keys()),
            "Số lượng": list(st.session_state.shoe.values())
        })
        st.bar_chart(df_chart.set_index("Lá bài"))
        
        if st.button("🔄 Reset toàn bộ"):
            st.session_state.started = False
            st.rerun()

    # --- GIAO DIỆN NHẬP BÀI THEO VÒNG ---
    st.title("🎰 Blackjack Live Tracking")
    
    with st.expander("📥 NHẬP BÀI VỪA RA TRONG VÒNG NÀY", expanded=True):
        input_cols = st.columns(st.session_state.num_players + 1)
        round_cards = []
        
        # Nhập bài Dealer
        with input_cols[0]:
            st.subheader("Dealer")
            d_card = st.selectbox("Lá ngửa cái", [""] + ['2','3','4','5','6','7','8','9','10','J','Q','K','A'], key="dealer_card")
            if d_card: round_cards.append(d_card)
        
        # Nhập bài người chơi
        for i in range(st.session_state.num_players):
            with input_cols[i+1]:
                st.subheader(f"P{i+1}")
                p_cards = st.multiselect(f"Lá bài P{i+1}", ['2','3','4','5','6','7','8','9','10','J','Q','K','A'], key=f"p{i}")
                round_cards.extend(p_cards)
        
        if st.button("✅ Xác nhận vòng này", use_container_width=True):
            record_cards(round_cards)
            st.rerun()

    st.divider()

    # --- PHÂN TÍCH & GỢI Ý ---
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.write("### 💡 Chiến thuật cược")
        if tc >= 3: st.success("🔥 **CƯỢC MẠNH:** Lợi thế lớn cho người chơi!")
        elif tc >= 1: st.info("👍 **Tăng cược nhẹ:** Bài đang ấm dần.")
        elif tc <= -2: st.error("⚠️ **CƯỢC TỐI THIỂU:** Nhà cái đang cầm bài nhỏ nhiều.")
        else: st.write("😐 **Cược bình thường.**")

    with col_r:
        st.write("### 🧠 Dự đoán Dealer")
        if d_card in ['4', '5', '6']:
            st.warning(f"Lá {d_card} là lá 'xấu' của cái. Tỉ lệ Dealer Quắc (Bust) rất cao.")
        elif d_card in ['A', '10', 'J', 'Q', 'K']:
            st.error(f"Lá {d_card} là lá mạnh. Dealer dễ có điểm cao (17-21).")
        elif d_card:
            st.write(f"Dealer đang cầm lá {d_card}. Đánh theo chiến thuật cơ bản.")

    # Lịch sử
    st.caption(f"Lịch sử 20 lá gần nhất: {', '.join(st.session_state.history[-20:])}")
