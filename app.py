import streamlit as st
import json

# --- CẤU HÌNH BẢO MẬT ---
STAFF_PIN = "1234" 

# --- CẤU HÌNH GIAO DIỆN & STYLE ---
st.set_page_config(page_title="Hồ Sơ Chăm Sóc", page_icon="📝", layout="centered")

hide_style = """
    <style>
    #MainMenu, header, footer {visibility: hidden;} 
    .stApp {margin-top: -60px;}
    .public-info {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
    .schedule-item {background-color: #fff; border-left: 5px solid #1565C0; padding: 10px; margin-bottom: 8px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); color: #000000;}
    .completed {border-left: 5px solid #4CAF50 !important;} /* Màu xanh lá cho mục hoàn thành */
    .ten-be {color: #1565C0; font-weight: bold; text-align: center;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- HÀM ĐỌC DỮ LIỆU ---
@st.cache_data(ttl=5) 
def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# --- HIỂN THỊ HỒ SƠ ---
def show_profile(info):
    
    # 1. ẢNH ĐẠI DIỆN
    if info.get('anh'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(info['anh'], use_column_width=True)

    st.markdown(f"<h2 class='ten-be'>{info['ten']}</h2>", unsafe_allow_html=True)
    
    # --- MỤC CÔNG KHAI ---
    st.markdown("### 🔑 Thông tin Cơ bản (Công khai)")
    st.markdown("<div class='public-info'>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.info(f"🎂 **Tuổi:** {info.get('tuoi', 'N/A')}")
    c2.info(f"⚧ **Giới tính:** {info.get('gioi_tinh', 'N/A')}")
    st.info(f"⚖️ **Cân nặng:** {info.get('can_nang', 'N/A')} kg")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---") 
    
    # --- NÚT CHUYỂN SANG CHẾ ĐỘ NHÂN VIÊN ---
    if st.button("🔐 Xem Lịch Sinh Hoạt (Dành cho Nhân viên)"):
        st.session_state['login_mode'] = True
        st.rerun()

# --- HIỂN THỊ CHẾ ĐỘ NHÂN VIÊN ---
def show_staff_view(info):
    st.header(f"📅 Lịch trình của {info['ten']}")
    
    # Lịch sinh hoạt
    schedule = info.get('schedule', [])
    for item in schedule:
        completed_class = "completed" if item.get('completed') else ""
        icon = "✅" if item.get('completed') else "⏳"
        
        st.markdown(
            f"""
            <div class='schedule-item {completed_class}'>
                <strong>{icon} {item.get('time', 'Chưa đặt giờ')}</strong><br>
                {item.get('name', 'Hoạt động')}
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("📝 Ghi chú Nhân viên")
    st.info(info.get('ghi_chu', 'Chưa có ghi chú hôm nay.'))

    if st.button("⬅️ Quay lại Hồ sơ (Công khai)"):
        st.session_state['login_mode'] = False
        st.session_state['logged_in'] = False
        st.rerun()

# --- HÀM CHÍNH ---
def main():
    
    # Khởi tạo state
    if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
    if 'login_mode' not in st.session_state: st.session_state['login_mode'] = False
        
    query_params = st.query_params
    child_id = query_params.get("id", None)
    data = load_data()

    if not child_id or child_id not in data:
        st.warning("⚠️ Vui lòng quét mã QR để xem hồ sơ của em bé.")
        return

    info = data[child_id]
    
    # --- LOGIC CHÍNH ---
    
    # 1. Nếu đang ở chế độ đăng nhập nhưng chưa đăng nhập
    if st.session_state['login_mode'] and not st.session_state['logged_in']:
        
        st.header("🔐 Đăng nhập Nhân viên")
        with st.form("login_form"):
            password = st.text_input("Mã PIN (Mã mẫu: 1234)", type="password")
            submitted = st.form_submit_button("Đăng nhập")
            
            if submitted:
                if password == STAFF_PIN:
                    st.session_state['logged_in'] = True
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Sai mã PIN.")
        
        if st.button("⬅️ Quay lại Hồ sơ (Công khai)"):
            st.session_state['login_mode'] = False
            st.rerun()

    # 2. Nếu đã đăng nhập
    elif st.session_state['logged_in']:
        show_staff_view(info)
        
    # 3. Chế độ Công khai (Mặc định)
    else:
        show_profile(info)

if __name__ == "__main__":
    main()```
