import streamlit as st
from roboflow import Roboflow
from PIL import Image
import numpy as np

# ตั้งค่ารหัสผ่านและข้อมูลโปรเจกต์
# ใช้รหัส API Key ที่คุณให้มาโดยตรง
ROBOFLOW_API_KEY = "rf_qx1IlPFbPmRVtwQr57gkMhb25zs1" 
PROJECT_NAME = "durian-detection-zb1dk"
VERSION_NUMBER = 3  # เวอร์ชันล่าสุดที่คุณแบ่งข้อมูล 70/20/10

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Durian Smart AI")
st.title("🍈 Durian Smart AI Mobile")
st.write("วิธีใช้งาน: ถ่ายรูปทุเรียนเพื่อให้ AI ตรวจสอบความสุก")

# โหลดโมเดลจาก Roboflow
rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project(PROJECT_NAME)
model = project.version(VERSION_NUMBER).model

# ส่วนของการอัปโหลดรูปภาพ
img_file = st.camera_input("ถ่ายรูปทุเรียน")

if img_file:
    image = Image.open(img_file)
    # ส่งรูปไปให้ AI ตรวจสอบ
    prediction = model.predict(image).json()
    
    # แสดงรูปภาพ
    st.image(image, caption="รูปที่ถ่าย", use_container_width=True)
    
    # แสดงผลลัพธ์
    st.write("### ผลการตรวจสอบ:")
    if prediction['predictions']:
        for pred in prediction['predictions']:
            st.success(f"พบ: {pred['class']} (ความมั่นใจ: {pred['confidence']:.2%})")
    else:
        st.warning("ไม่พบข้อมูลทุเรียนในภาพ กรุณาลองใหม่อีกครั้ง")
