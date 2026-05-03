import streamlit as st

# --- CẤU TRÚC GIAO DIỆN ---
st.set_page_config(page_title="Máy Tính Bài", layout="wide")

# --- KHỞI TẠO DỮ LIỆU ---
if "kho_bai" not in st.session_state:
    st.session_state.update({
        "bat_dau": False,
        "danh_sach_bai": {},
        "lich_su": [],
        "dang_nhap_cho": "Cái", # Mặc định là nhập bài cho Nhà Cái
        "so_bo": 4
    })

def lam_moi_bai():
    # Mỗi bộ có 4 lá mỗi loại (2, 3, 4... A)
    cac_la = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    st.session_state.danh_sach_bai = {la: 4 * st.session_state.so_bo for la in cac_la}
    st.session_state.lich_su = []

def bam_la_bai(ten_la):
    if st.session_state.danh_sach_bai[ten_la] > 0:
        st.session_state.danh_sach_bai[ten_la] -= 1
        # Lưu lại lá bài và người nhận để nếu nhầm thì xóa
        st.session_state.lich_su.append(ten_la)

def hoan_tac():
    if st.session_state.lich_su:
        la_cu_cung = st.session_state.lich_su.pop()
        st.session_state.danh_sach_bai[la_cu_cung] += 1

# --- MÀN HÌNH CÀI ĐẶT ---
if not st.session_state.bat_dau:
    st.title("🃏 Cài đặt đơn giản")
    st.session_state.so_bo = st.selectbox("Dùng mấy bộ bài?", [1, 2, 4, 6, 8], index=2)
    
    if st.button("BẮT ĐẦU CHƠI", use_container_width=True):
        lam_moi_bai()
        st.session_state.bat_dau = True
        st.rerun()

# --- MÀN HÌNH CHƠI CHÍNH ---
else:
    # 1. Tính toán con số đơn giản
    diem_dem = 0
    for la in st.session_state.lich_su:
        if la in ['2','3','4','5','6']: diem_dem += 1
        elif la in ['10','J','Q','K','A']: diem_dem -= 1
    
    tong_con_lai = sum(st.session_state.danh_sach_bai.values())
    # Tính toán độ "nóng" của bài (Thay cho True Count)
    do_nong = diem_dem / (tong_con_lai / 52) if tong_con_lai > 0 else 0

    # 2. Hiển thị trạng thái bằng màu sắc
    st.subheader("Tình hình hiện tại:")
    c1, c2 = st.columns(2)
    
    with c1:
        if do_nong >= 2:
            st.success(f"🔥 BÀI ĐANG ĐẸP (Nên đánh mạnh)")
        elif do_nong <= -2:
            st.error(f"❄️ BÀI ĐANG XẤU (Nên đánh nhỏ)")
        else:
            st.info(f"😐 Bài bình thường")
            
    with c2:
        st.metric("Số bài còn lại", f"{tong_con_lai} lá")

    st.divider()

    # 3. Nút bấm lá bài (Làm thật to để dễ chạm)
    st.write("### 👇 Vừa ra lá gì, bấm lá đó:")
    
    hang1 = st.columns(4)
    hang2 = st.columns(4)
    hang3 = st.columns(5)
    
    tat_ca_la = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    
    # Chia nút vào các hàng cho gọn
    for i, la in enumerate(tat_ca_la):
        if i < 4: col = hang1[i]
        elif i < 8: col = hang2[i-4]
        else: col = hang3[i-8]
        
        with col:
            if st.button(la, key=f"btn_{la}", use_container_width=True, height=80):
                bam_la_bai(la)
                st.rerun()

    st.divider()

    # 4. Công cụ hỗ trợ nhanh
    col_trai, col_phai = st.columns(2)
    
    with col_trai:
        if st.button("⏪ BẤM NHẦM (Xóa lá vừa nhập)", use_container_width=True):
            hoan_tac()
            st.rerun()
            
    with col_phai:
        if st.button("🔄 ĐỔI BỘ BÀI MỚI", use_container_width=True):
            st.session_state.bat_dau = False
            st.rerun()

    # 5. Dự báo tỉ lệ (Dùng thanh màu cho dễ nhìn)
    st.write("### 📈 Dự báo lá tiếp theo:")
    la_nho = sum([st.session_state.danh_sach_bai[v] for v in ['2','3','4','5','6']])
    la_lon = sum([st.session_state.danh_sach_bai[v] for v in ['10','J','Q','K','A']])
    
    st.write(f"Tỉ lệ ra bài NHỎ (2-6): {int(la_nho/tong_con_lai*100) if tong_con_lai > 0 else 0}%")
    st.progress(la_nho/tong_con_lai if tong_con_lai > 0 else 0)
    
    st.write(f"Tỉ lệ ra bài LỚN (10-A): {int(la_lon/tong_con_lai*100) if tong_con_lai > 0 else 0}%")
    st.progress(la_lon/tong_con_lai if tong_con_lai > 0 else 0)
