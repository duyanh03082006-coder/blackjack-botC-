import streamlit as st

# --- CẤU TRÚC GIAO DIỆN ---
st.set_page_config(page_title="Máy Tính Bài Blackjack", layout="wide")

# --- KHỞI TẠO DỮ LIỆU (SESSION STATE) ---
if "bat_dau" not in st.session_state:
    st.session_state.bat_dau = False
if "danh_sach_bai" not in st.session_state:
    st.session_state.danh_sach_bai = {}
if "lich_su" not in st.session_state:
    st.session_state.lich_su = []
if "so_bo" not in st.session_state:
    st.session_state.so_bo = 4

def lam_moi_bai():
    cac_la = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.danh_sach_bai = {la: 4 * st.session_state.so_bo for la in cac_la}
    st.session_state.lich_su = []

def bam_la_bai(ten_la):
    if st.session_state.danh_sach_bai[ten_la] > 0:
        st.session_state.danh_sach_bai[ten_la] -= 1
        st.session_state.lich_su.append(ten_la)

def hoan_tac():
    if st.session_state.lich_su:
        la_cu_cung = st.session_state.lich_su.pop()
        st.session_state.danh_sach_bai[la_cu_cung] += 1

# --- MÀN HÌNH CÀI ĐẶT ---
if not st.session_state.bat_dau:
    st.title("🃏 Cài đặt đơn giản")
    st.session_state.so_bo = st.number_input("Dùng mấy bộ bài?", min_value=1, max_value=8, value=4)
    
    if st.button("BẮT ĐẦU CHƠI", use_container_width=True):
        lam_moi_bai()
        st.session_state.bat_dau = True
        st.rerun()

# --- MÀN HÌNH CHƠI CHÍNH ---
else:
    # 1. Tính toán con số đơn giản (Hi-Lo system)
    diem_dem = 0
    for la in st.session_state.lich_su:
        if la in ['2','3','4','5','6']: 
            diem_dem += 1
        elif la in ['10','J','Q','K','A']: 
            diem_dem -= 1
    
    tong_con_lai = sum(st.session_state.danh_sach_bai.values())
    decks_con_lai = tong_con_lai / 52
    do_nong = diem_dem / decks_con_lai if decks_con_lai > 0.1 else diem_dem

    # 2. Hiển thị trạng thái bằng màu sắc
    st.write(f"### Tình hình hiện tại:")
    
    col_status, col_count = st.columns(2)
    with col_status:
        if do_nong >= 2:
            st.success("🔥 BÀI ĐANG ĐẸP (Nên đánh mạnh)")
        elif do_nong <= -2:
            st.error("❄️ BÀI ĐANG XẤU (Nên đánh nhỏ)")
        else:
            st.info("😐 Bài bình thường")
            
    with col_count:
        st.metric("Số bài còn lại", f"{tong_con_lai} lá")

    st.divider()

    # 3. Nút bấm lá bài (Thiết kế nút bấm to, dễ chạm)
    st.write("### 👇 Vừa ra lá gì, bấm lá đó:")
    
    # Hàng 1: Bài nhỏ
    cols1 = st.columns(5)
    for i, la in enumerate(['2', '3', '4', '5', '6']):
        with cols1[i]:
            if st.button(la, key=f"btn_{la}", use_container_width=True):
                bam_la_bai(la)
                st.rerun()
                
    # Hàng 2: Bài trung bình và lớn
    cols2 = st.columns(4)
    for i, la in enumerate(['7', '8', '9', '10']):
        with cols2[i]:
            if st.button(la, key=f"btn_{la}", use_container_width=True):
                bam_la_bai(la)
                st.rerun()
                
    # Hàng 3: Bài Tây
    cols3 = st.columns(4)
    for i, la in enumerate(['J', 'Q', 'K', 'A']):
        with cols3[i]:
            if st.button(la, key=f"btn_{la}", use_container_width=True):
                bam_la_bai(la)
                st.rerun()

    st.divider()

    # 4. Dự báo tỉ lệ lá bài sắp tới
    if tong_con_lai > 0:
        la_nho = sum([st.session_state.danh_sach_bai[v] for v in ['2','3','4','5','6']])
        la_lon = sum([st.session_state.danh_sach_bai[v] for v in ['10','J','Q','K','A']])
        
        c_nho, c_lon = st.columns(2)
        c_nho.write(f"Tỉ lệ bài NHỎ (2-6): **{int(la_nho/tong_con_lai*100)}%**")
        c_nho.progress(la_nho/tong_con_lai)
        
        c_lon.write(f"Tỉ lệ bài LỚN (10-A): **{int(la_lon/tong_con_lai*100)}%**")
        c_lon.progress(la_lon/tong_con_lai)

    # 5. Chức năng phụ
    st.write("---")
    c_undo, c_reset = st.columns(2)
    with c_undo:
        if st.button("⏪ Bấm nhầm (Xóa lá cuối)", use_container_width=True):
            hoan_tac()
            st.rerun()
    with c_reset:
        if st.button("🔄 Đổi bộ mới / Cài lại", use_container_width=True):
            st.session_state.bat_dau = False
            st.rerun()
