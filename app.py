import streamlit as st
import json
import qrcode
from io import BytesIO

st.set_page_config(page_title="Hồ Sơ", page_icon="❤️", layout="centered")

# Hàm đọc dữ liệu file JSON
@st.cache_data(ttl=30) # Tự làm mới sau 30 giây
def load_data_local():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# Lấy ID từ URL
query_params = st.query_params
child_id = query_params.get("id", None)
data = load_data_local()

# CSS làm đẹp
st.markdown("""
    <style>
    .card { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- TRANG 1: QUẢN LÝ TẠO QR (Chỉ hiện khi vào trực tiếp web) ---
if not child_id:
    st.title("🖨️ In Mã QR")
    st.info("Dữ liệu được cập nhật từ phần mềm trên máy tính.")
    
    # Nhập link web của bạn
    base_url = st.text_input("Link Web:", "https://ten-app-cua-ban.streamlit.app")
    
    if data:
        chon = st.selectbox("Chọn bé:", list(data.keys()), format_func=lambda x: data[x]['ten'])
        if st.button("Tạo QR"):
            url = f"{base_url}/?id={chon}"
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), width=200)
            st.download_button("Tải về", buf.getvalue(), "qr.png", "image/png")
    else:
        st.warning("Chưa có dữ liệu. Hãy nhập từ phần mềm máy tính.")

# --- TRANG 2: KHÁCH XEM (Khi quét QR) ---
else:
    if child_id in data:
        info = data[child_id]
        
        tab1, tab2 = st.tabs(["👤 HỒ SƠ", "📅 LỊCH TRÌNH"])
        
        with tab1:
            if info['anh']: st.image(info['anh'], use_column_width=True)
            st.title(info['ten'])
            st.write(f"Tuổi: {info['tuoi']} | Giới tính: {info['gioi_tinh']}")
            st.info("👉 Vuốt sang Lịch Trình để xem chi tiết.")
            
        with tab2:
            st.subheader("Lịch hôm nay")
            content = info['lich'].replace("\n", "<br>")
            st.markdown(f'<div class="card">{content}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏠 Về trang chủ"):
                st.query_params.clear()
                st.rerun()
    else:
        st.error("Không tìm thấy thông tin!")
