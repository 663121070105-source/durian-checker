import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอ
st.set_page_config(layout="wide", page_title="Durian Smart AI")

# 2. นี่คือจุดสำคัญ! บรรทัดข้างล่างนี้คือ "เกราะเปิด" ห้ามลบเด็ดขาด
html_code = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Durian Smart AI</title>
    <style>
        /* ส่วนนี้คือ CSS ที่เคยทำให้เกิด Error (0%) ตอนนี้ปลอดภัยแล้วเพราะอยู่ในเครื่องหมายคำพูด */
        body { 
            font-family: 'Sarabun', sans-serif; 
            background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); 
            min-height: 100vh; 
            padding: 20px; 
            margin: 0;
            display: flex;
            justify-content: center;
        }
        .container { 
            width: 100%;
            max-width: 600px; 
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
            text-align: center;
        }
        .header { margin-bottom: 20px; }
        .emoji { font-size: 60px; display: block; margin-bottom: 10px; }
        h1 { color: #2E7D32; margin: 0; font-size: 24px; }
        p { color: #666; margin-top: 5px; }
        
        .scan-box {
            border: 2px dashed #81C784;
            background: #F1F8E9;
            border-radius: 15px;
            padding: 40px;
            margin: 20px 0;
            cursor: pointer;
            transition: 0.3s;
        }
        .scan-box:hover { background: #DCEDC8; }
        
        .btn {
            background: #2E7D32;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
        }
        .btn:hover { background: #1B5E20; }
        
        #resultArea {
            margin-top: 20px;
            display: none;
            background: #FFF3E0;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <span class="emoji">🥭</span>
            <h1>Durian Smart AI</h1>
            <p>ระบบตรวจสอบความสุกทุเรียนอัจฉริยะ</p>
        </div>

        <div class="scan-box" onclick="startScan()">
            <div style="font-size: 40px;">📷</div>
            <p>แตะที่นี่เพื่อถ่ายรูปทุเรียน</p>
        </div>

        <div id="resultArea">
            <h3>กำลังวิเคราะห์...</h3>
        </div>

        <button class="btn" onclick="startScan()">เริ่มวิเคราะห์</button>
    </div>

    <script>
        function startScan() {
            const result = document.getElementById('resultArea');
            result.style.display = 'block';
            result.innerHTML = '<h3>🔄 AI กำลังทำงาน...</h3>';
            
            setTimeout(() => {
                // จำลองผลลัพธ์
                const percent = Math.floor(Math.random() * 20) + 80;
                result.innerHTML = `
                    <h2 style="color: #2E7D32;">✅ ทุเรียนสุกพอดี (Ready)</h2>
                    <p>ความสุก: <strong>${percent}%</strong></p>
                    <p>ก๊าซเอทิลีน: <span style="color:green">ปกติ</span></p>
                    <div style="background:#ddd; height:10px; border-radius:5px; margin-top:10px;">
                        <div style="background:#2E7D32; width:${percent}%; height:10px; border-radius:5px;"></div>
                    </div>
                `;
            }, 2000);
        }
    </script>

</body>
</html>
""" 
# 3. นี่คือจุดสำคัญ! บรรทัดข้างบนนี้คือ "เกราะปิด" (""") ห้ามลืมเด็ดขาด

# 4. สั่งให้ Streamlit แสดงผล
components.html(html_code, height=800, scrolling=True)
