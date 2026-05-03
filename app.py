import streamlit as st
import pandas as pd
import re

# --- CẤU HÌNH ---
st.set_page_config(page_title="Blackjack Ultimate Analyzer", layout="wide")

if "started" not in st.session_state:
    st.session_state.started = False
if "shoe" not in st.session_state:
    st.session_state.shoe = {}
if "history" not in st.session_state:
    st.session_state.history = []

def init_game(num_decks):
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.shoe = {v: 4 * num_decks for v in values}
    st.session_state.history = []

def record_cards(card_string):
    cards = re.findall(r'[2-9]|10|[JQKA]', card_string.upper())
    for card in cards:
        if card in st.session_state.shoe and st.session_state.shoe[card] > 0:
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
    st.title("🃏 Blackjack Pro Setup")
    c1, c2, c3 = st.columns(3)
    num_decks = c1.number_input("Số bộ bài", 1, 8, 4)
    num_players = c2.number_input("Số người chơi khác", 1, 5, 1)
    your_pos = c3.selectbox("Vị trí của bạn", [f"P{i+1}" for i in range(num_players + 1)])
    
    if st.button("🚀 BẮT ĐẦU VÁN MỚI", use_container_width=True):
        st.session_state.num_decks = num_decks
        st.session_state.num_players = num_players + 1 # Tổng số người ngồi bàn
        st.session_state.your_pos = your_pos
        init_game(num_decks)
        st.session_state.started = True
        st.rerun()

# --- MÀN HÌNH 2: LIVE ANALYTICS ---
else:
    rc, tc, total_left = get_counts()
    
    # --- SIDEBAR: XÁC SUẤT CHI TIẾT ---
    with st.sidebar:
        st.header("🎯 Xác suất bốc bài")
        if total_left > 0:
            # Tính % cho từng loại bài
            prob_data = []
            # Nhóm bài Nhỏ (2-6), Trung bình (7-9), Lớn (10-A)
            low_cards = sum([st.session_state.shoe[v] for v in ['2','3','4','5','6']])
            med_cards = sum([st.session_state.shoe[v] for v in ['7','8','9']])
            high_cards = sum([st.session_state.shoe[v] for v in ['10','J','Q','K','A']])
            
            prob_data.append({"Nhóm": "Lá Thấp (2-6)", "Tỷ lệ": f"{(low_cards/total_left)*100:.1f}%"})
            prob_data.append({"Nhóm": "Lá Trung (7-9)", "Tỷ lệ": f"{(med_cards/total_left)*100:.1f}%"})
            prob_data.append({"Nhóm": "Lá Cao (10-A)", "Tỷ lệ": f"{(high_cards/total_left)*100:.1f}%"})
            st.table(pd.DataFrame(prob_data))
            
            # Biểu đồ chi tiết từng lá
            st.write("**Số lượng lá còn lại:**")
            df_chart = pd.DataFrame({"Lá": st.session_state.shoe.keys(), "Còn": st.session_state.shoe.values()})
            st.bar_chart(df_chart.set_index("Lá"))

        if st.button("🔄 Reset Game"):
            st.session_state.started = False
            st.rerun()

    st.title(f"🎰 Blackjack Live - Bạn là `{st.session_state.your_pos}`")

    # --- NHẬP LIỆU THEO VÒNG ---
    with st.form("round_input"):
        st.write("### 📝 Nhập bài lộ diện (Cách nhau bằng dấu cách)")
        cols = st.columns(st.session_state.num_players + 1)
        
        inputs = []
        # Dealer
        with cols[0]:
            st.subheader("🏦 Dealer")
            d = st.text_input("Lá ngửa", key="d_in", placeholder="Vd: A")
            inputs.append(d)
        
        # Players
        for i in range(st.session_state.num_players):
            p_name = f"P{i+1}"
            is_you = "(BẠN)" if p_name == st.session_state.your_pos else ""
            with cols[i+1]:
                st.subheader(f"👤 {p_name} {is_you}")
                p = st.text_input(f"Lá bài", key=f"p{i}_in", placeholder="Vd: 8 8")
                inputs.append(p)
        
        if st.form_submit_button("XÁC NHẬN VÒNG NÀY", use_container_width=True):
            for item in inputs:
                record_cards(item)
            st.rerun()

    # --- LỜI KHUYÊN CHIẾN THUẬT ---
    st.divider()
    c_info, c_advice = st.columns([1, 2])
    
    with c_info:
        st.metric("True Count", round(tc, 2))
        st.metric("Running Count", rc)
        
    with c_advice:
        st.write("### 💡 Lời khuyên cho bạn")
        # Logic lời khuyên đơn giản dựa trên True Count
        if tc >= 2:
            st.success(f"🔥 **ƯU THẾ LỚN:** Hệ thống bài lớn (10, A) còn cực nhiều. Nếu bạn `{st.session_state.your_pos}` đang có bài tốt, hãy xem xét Double Down hoặc cược lớn.")
        elif tc <= -2:
            st.error("⚠️ **RỦI RO CAO:** Bài nhỏ còn quá nhiều. Dealer rất khó quắc. Nên đánh an toàn, cược tối thiểu.")
        else:
            st.info("😐 **TRẠNG THÁI CÂN BẰNG:** Đánh theo chiến thuật cơ bản (Basic Strategy).")
            
        # Dự đoán lá tiếp theo
        max_card = max(st.session_state.shoe, key=st.session_state.shoe.get)
        st.write(f"👉 Lá bài có khả năng xuất hiện tiếp theo cao nhất: **{max_card}**")

    # Lịch sử
    with st.expander("Xem lịch sử bài đã ra"):
        st.write(", ".join(st.session_state.history))
