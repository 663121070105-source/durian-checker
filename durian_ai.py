import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Durian Test", layout="wide")


html_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* สาเหตุที่เคย Error คือ Python อ่านตรงนี้ไม่รู้เรื่องถ้าไม่มีฟันหนูครอบ */
        body { 
            font-family: sans-serif; 
            background: linear-gradient(135deg, #E8F5E9 0%, #FFF9C4 100%); 
            padding: 50px; 
            text-align: center;
        }
        .box {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        h1 { color: #2E7D32; }
    </style>
</head>
<body>
    <div class="box">
        <h1>✅ ยินดีด้วย! คุณแก้ Error สำเร็จแล้ว</h1>
        <p>ตอนนี้ระบบ Python อ่านโค้ด HTML ได้ถูกต้องแล้วครับ</p>
        <div style="font-size: 50px;">🥭</div>
    </div>
</body>
</html>
""" 

components.html(html_code, height=600)
