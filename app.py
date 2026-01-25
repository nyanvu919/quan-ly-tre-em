import streamlit as st
import json

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hồ Sơ", page_icon="📝", layout="centered")

# --- GIẤU NÚT MENU & HEADER (CHỐNG ĐĂNG NHẬP) ---
hide_style = """
    <style>
    #MainMenu {visibility: hidden;} 
    header {visibility: hidden;} 
    footer {visibility: hidden;} 
    .stApp {margin-top: -60px;}
    
    /* Trang trí khung lịch trình */
    .lich-box {
        background-color: #f8f9fa; /* Nền trắng xám */
        color: #000000;             /* QUAN TRỌNG: Ép chữ màu ĐEN */
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #2196F3;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Trang trí tên */
    .ten-be {
        text-align: center;
        color: #1565C0;
        font-weight: bold;
        margin-bottom: 5px;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- HÀM ĐỌC DỮ LIỆU ---
@st.cache_data(ttl=5) # Làm mới mỗi 5 giây
def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# --- XỬ LÝ HIỂN THỊ ---
query_params = st.query_params
child_id = query_params.get("id", None)
data = load_data()

# Nếu có ID và tìm thấy trong dữ liệu
if child_id and child_id in data:
    info = data[child_id]

    # 1. ẢNH ĐẠI DIỆN (Canh giữa)
    if info.get('anh'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(info['anh'], use_column_width=True)

    # 2. THÔNG TIN CƠ BẢN
    st.markdown(f"<h1 class='ten-be'>{info['ten']}</h1>", unsafe_allow_html=True)
    
    # Hiển thị tuổi giới tính nằm ngang cho gọn
    c1, c2 = st.columns(2)
    with c1: st.info(f"🎂 **Tuổi:** {info['tuoi']}")
    with c2: st.info(f"⚧ **Giới tính:** {info['gioi_tinh']}")

    st.write("") # Khoảng trắng
    st.markdown("---") # Đường kẻ ngang phân cách
    
    # 3. LỊCH SINH HOẠT (HIỆN LUÔN Ở DƯỚI)
    st.subheader("📅 Lịch trình & Ghi chú")
    
    # Nếu chưa nhập lịch thì hiện thông báo
    if not info['lich'].strip():
        st.warning("Chưa có thông tin ghi chú cho hôm nay.")
    else:
        # Xử lý xuống dòng để hiển thị đẹp
        noi_dung = info['lich'].replace("\n", "<br>")
        # In ra trong khung đẹp (Chữ đen nền trắng)
        st.markdown(f'<div class="lich-box">{noi_dung}</div>', unsafe_allow_html=True)

# Nếu không có ID hoặc link sai
else:
    st.warning("⚠️ Vui lòng quét mã QR để xem thông tin.")
