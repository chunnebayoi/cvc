import streamlit as st
import requests
import time

# Tiêu đề ứng dụng
st.title("Bot Phân Tích Thị Trường - Unitrade.Trade")

# API Key và URL
API_KEY = st.secrets.get("API_KEY", "fdc2ab610fa442e9b905a4a7ebd47069889e40d45f1d49e78e6674517c53b87f")
API_URL = "https://api.unitrade.space/market-data"  # Thay bằng endpoint thực tế

# Hàm lấy dữ liệu từ API
def fetch_market_data():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi khi lấy dữ liệu: {e}")
        # Dữ liệu giả lập nếu API không hoạt động
        return {"asset": "BTC-USD", "ratio": 74, "signal": "Buy"}

# Hàm phân tích dữ liệu
def analyze_market(data):
    ratio = data.get("ratio", 0)
    signal = data.get("signal", "Chờ")
    
    # Logic phân tích: Nếu API không trả tín hiệu, tự tính dựa trên ratio
    if not signal or signal == "Chờ":
        signal = "Mua" if ratio > 70 else "Chờ"
    
    return ratio, signal

# Lấy dữ liệu và phân tích
market_data = fetch_market_data()
ratio, signal = analyze_market(market_data)

# Hiển thị giao diện giống unitrade.trade
st.subheader("Xu Hướng Là Bạn")
st.markdown("### Chờ Kết Quả")

# Hiển thị tín hiệu
if signal == "Mua":
    st.markdown(
        """
        <div style='text-align: center;'>
            <span style='font-size: 24px; color: green; font-weight: bold;'>▲ Mua</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style='text-align: center;'>
            <span style='font-size: 24px; color: gray; font-weight: bold;'>◉ Chờ</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Hiển thị tỷ lệ và thời gian
st.write(f"**Tỷ lệ:** {round(ratio, 2)}%")
st.write("**Thời gian:** 24s")
st.write(f"**Phiên:** {signal}")

# Tự động cập nhật mỗi 10 giây
time.sleep(10)
st.rerun()