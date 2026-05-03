import streamlit as st

# --- CẤU TRÚC GIAO DIỆN ---
st.set_page_config(page_title="Máy Tính Bài", layout="wide")

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
    # 1. Tính toán con số đơn giản
    diem_dem = 0
    for la in st.session_state.lich_su:
        if la in ['2','3','4','5','6']: 
            diem_dem += 1
        elif la in ['10','J','Q','K','A']: 
            diem_dem -= 1
    
    tong_con_lai = sum(st.session_state.danh_sach_bai.values())
    # Tính độ "nóng" (True Count)
    decks_con_lai = tong_con_lai / 52
    do_nong = diem_dem / decks_con_lai if decks_con_lai > 0.2 else diem_dem

    # 2. Hiển thị trạng thái
    st.write(f"### Tình hình bài hiện tại:")
    
    col_status, col_count = st.columns(2)
    with col_status:
        if do_nong >= 2:
            st.success("🔥 BÀI ĐANG ĐẸP (Ưu thế người chơi)")
        elif do_nong <= -2:
            st.error("❄️ BÀI ĐANG XẤU (Ưu thế nhà cái)")
        else:
            st.info("😐 Bài bình thường")
            
    with col_count:
        st.metric("Số bài còn lại", f"{tong_con_lai} lá")

    st.divider()

    # 3. Nút bấm lá bài (Thiết kế lại dạng lưới để không lỗi)
    st.write("### 👇 Bấm lá bài vừa lật:")
    
    cac_nhom_la = [
        ['2', '3', '4', '5'],
        ['6', '7', '8', '9'],
        ['10', 'J', 'Q', 'K', 'A']
    ]
    
    for nhom in cac_nhom_la:
        cols = st.columns(len(nhom))
        for i, la hay trong enumerate(nhom):
            with cols[i]:
                if st.button(nhom[i], key=f"btn_{nhom[i]}", use_container_width=True):
                    bam_la_bai(nhom[i])
                    st.rerun()

    st.divider()

    # 4. Dự báo tỉ lệ
    st.write("### 📈 Khả năng bốc trúng:")
    if tong_con_lai > 0:
        la_nho = sum([st.session_state.danh_sach_bai[v] for v in ['2','3','4','5','6']])
        la_lon = sum([st.session_state.danh_sach_bai[v] for v in ['10','J','Q','K','A']])
        
        c_nho, c_lon = st.columns(2)
        c_nho.write(f"Lá NHỎ (2-6): **{int(la_nho/tong_con_lai*100)}%**")
        c_nho.progress(la_nho/tong_con_lai)
        
        c_lon.write(f"Lá LỚN (10-A): **{int(la_lon/tong_con_lai*100)}%**")
        c_lon.progress(la_lon/tong_con_lai)

    # 5. Nút chức năng phụ
    st.write("---")
    c_back, c_reset = st.columns(2)
    with c_back:
        if st.button("⏪ Bấm nhầm (Hoàn tác)", use_container_width=True):
            hoan_tac()
            st.rerun()
    with c_reset:
        if st.button("🔄 Đổi bộ mới / Cài lại", use_container_width=True):
            st.session_state.bat_dau = False
            st.rerun()
