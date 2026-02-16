import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอ
st.set_page_config(layout="wide", page_title="Durian Smart AI")

# --- จุดสำคัญคือบรรทัดนี้! เปิดเกราะป้องกันโค้ด HTML ---
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI</title>
    <style>
        /* ตรงนี้คือจุดที่เคย Error ตอนนี้ปลอดภัยแล้ว */
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); min-height: 100vh; padding: 20px; }
        
        /* CSS ส่วนอื่นๆ */
        .container { max-width: 700px; margin: 0 auto; background: white; padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #558B2F; margin-bottom: 10px; }
        .btn { background: #81C784; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 10px; cursor: pointer; margin: 10px; }
        .btn:hover { background: #66BB6A; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🥭 Durian Smart AI</h1>
        <p>ระบบตรวจสอบความสุกทุเรียน</p>
        <hr style="margin: 20px 0; border: 0; border-top: 1px solid #eee;">
        
        <div id="resultArea" style="padding: 20px; background: #F1F8E9; border-radius: 10px; margin-bottom: 20px;">
            <h3>📷 พร้อมใช้งาน</h3>
            <p>กรุณากดปุ่มเพื่อเริ่มสแกน</p>
        </div>

        <button class="btn" onclick="simulateScan()">🔍 สแกนทุเรียน</button>
    </div>

    <script>
        function simulateScan() {
            const resultArea = document.getElementById('resultArea');
            resultArea.innerHTML = '<h3>🔄 กำลังวิเคราะห์...</h3>';
            
            setTimeout(() => {
                // สุ่มผลลัพธ์เพื่อทดสอบ
                const ripeness = Math.floor(Math.random() * 30) + 70; 
                resultArea.innerHTML = `
                    <h2 style="color: #2E7D32;">✅ ทุเรียนสุกพอดี</h2>
                    <p>ความสุก: <strong>${ripeness}%</strong></p>
                    <p>คำแนะนำ: พร้อมรับประทาน</p>
                `;
            }, 1500);
        }
    </script>
</body>
</html>
""" 
# --- ปิดเกราะป้องกันตรงนี้ ห้ามลืม! ---

# สั่งให้ Streamlit แสดงผล HTML
components.html(html_code, height=600, scrolling=True)
