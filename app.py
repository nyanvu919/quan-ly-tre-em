import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image

# --- CẤU HÌNH DỮ LIỆU ---
DATA_TRE_EM = {
    "001": {
        "ten": "Nguyễn Văn A",
        "tuoi": 10,
        "gioi_tinh": "Nam",
        "anh": "https://api.dicebear.com/7.x/avataaars/png?seed=A", 
        "lich": [
            {"Gio": "07:00", "Viec": "Ăn sáng / Uống thuốc"},
            {"Gio": "09:00", "Viec": "Tập vật lý trị liệu"},
            {"Gio": "11:30", "Viec": "Ăn trưa"},
            {"Gio": "14:00", "Viec": "Nghe nhạc"},
        ]
    },
    "002": {
        "ten": "Trần Thị B",
        "tuoi": 12,
        "gioi_tinh": "Nữ",
        "anh": "https://api.dicebear.com/7.x/avataaars/png?seed=B",
        "lich": [
            {"Gio": "07:00", "Viec": "Ăn sáng"},
            {"Gio": "08:30", "Viec": "Học kỹ năng"},
            {"Gio": "12:00", "Viec": "Ngủ trưa"},
        ]
    }
}

def main():
    st.set_page_config(page_title="Hồ Sơ Chăm Sóc", page_icon="❤️", layout="centered")
    
    # CSS tùy chỉnh giao diện
    st.markdown("""
        <style>
        .big-font { font-size:22px !important; font-weight: bold; color: #2E86C1; }
        .box-item { background-color: #f0f2f6; padding: 10px; border-radius: 8px; margin-bottom: 8px; }
        </style>
    """, unsafe_allow_html=True)

    # Lấy ID từ trên thanh địa chỉ
    query_params = st.query_params
    child_id = query_params.get("id", None)

    # --- TRƯỜNG HỢP 1: TRANG QUẢN LÝ (ADMIN) ---
    if not child_id:
        st.title("🖨️ Tạo Mã QR")
        st.info("Dành cho quản lý để in mã QR dán lên thẻ/giường.")

        # Ô nhập địa chỉ trang web hiện tại
        # Khi bạn deploy xong, bạn copy link web dán vào đây để tạo mã QR đúng
        app_url = st.text_input("Nhập link trang web của bạn vào đây:", value="https://quan-ly-tre-em.streamlit.app")
        
        chon_id = st.selectbox("Chọn tên bé:", list(DATA_TRE_EM.keys()), format_func=lambda x: DATA_TRE_EM[x]['ten'])
        
        if st.button("Tạo mã QR"):
            info = DATA_TRE_EM[chon_id]
            # Link đầy đủ
            final_link = f"{app_url}/?id={chon_id}"
            
            # Tạo ảnh QR
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(final_link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Hiển thị
            col1, col2 = st.columns([1, 1])
            with col1:
                buf = BytesIO()
                img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.image(byte_im, width=200)
            with col2:
                st.success(f"Đã tạo cho: {info['ten']}")
                st.write(f"Link: {final_link}")
                st.download_button("Tải ảnh QR về", data=byte_im, file_name=f"QR_{info['ten']}.png", mime="image/png")

    # --- TRƯỜNG HỢP 2: NGƯỜI DÙNG QUÉT MÃ ---
    else:
        if child_id in DATA_TRE_EM:
            info = DATA_TRE_EM[child_id]
            
            # Giao diện Tabs (Slide)
            tab1, tab2 = st.tabs(["👤 HỒ SƠ", "📅 LỊCH TRÌNH"])

            with tab1:
                st.image(info['anh'], width=150)
                st.markdown(f'<p class="big-font">{info["ten"]}</p>', unsafe_allow_html=True)
                st.write(f"Năm nay: **{info['tuoi']} tuổi**")
                st.write(f"Giới tính: **{info['gioi_tinh']}**")
                st.info("Vuốt sang tab 'Lịch Trình' để xem chi tiết 👉")

            with tab2:
                st.subheader(f"Lịch của {info['ten']}")
                for item in info['lich']:
                    st.markdown(
                        f"""<div class="box-item">
                            <b>🕒 {item['Gio']}</b>: {item['Viec']}
                        </div>""", 
                        unsafe_allow_html=True
                    )
                
                if st.button("🏠 Về trang chủ"):
                    st.query_params.clear()
                    st.rerun()
        else:
            st.error("Không tìm thấy thông tin!")

if __name__ == "__main__":
    main()
