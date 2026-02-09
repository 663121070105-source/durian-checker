import streamlit as st
from roboflow import Roboflow
from PIL import Image
import os

ROBOFLOW_API_KEY = "aUQh6GrqTow8tSgITsZK" # ใช้รหัส Private Key ของคุณ
PROJECT_NAME = "durian-detection-zb1dk"
VERSION_NUMBER = 3

st.set_page_config(page_title="Durian Smart AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    .status-box { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍈 Durian Smart AI Pro")
st.write("ระบบตรวจสอบทุเรียนอัจฉริยะด้วยเทคโนโลยี AI")



col1, col2 = st.columns(2) # ปรับเป็น 2 คอลัมน์
with col1:
    st.metric("ความแม่นยำ (mAP)", "91.8%") # ข้อมูลจาก v3
with col2:
    st.metric("ความถูกต้อง", "92.2%") # ข้อมูลจาก v3

st.divider()


option = st.radio("เลือกวิธีตรวจสอบ:", ("📸 ถ่ายรูปจากกล้อง", "📁 อัปโหลดรูปภาพจากเครื่อง"))

img_file = None
if option == "📸 ถ่ายรูปจากกล้อง":
    img_file = st.camera_input("กดเพื่อถ่ายรูปทุเรียน")
else:
    img_file = st.file_uploader("เลือกไฟล์รูปภาพทุเรียน...", type=["jpg", "jpeg", "png"])


if img_file:
    with st.spinner('AI กำลังวิเคราะห์เนื้อทุเรียน...'):
        image = Image.open(img_file)
        
        # แก้ปัญหา path ด้วยการบันทึกไฟล์ชั่วคราว
        temp_path = "temp_scan.jpg"
        image.save(temp_path)
        
        try:
            rf = Roboflow(api_key=ROBOFLOW_API_KEY)
            project = rf.workspace().project(PROJECT_NAME)
            model = project.version(VERSION_NUMBER).model
            
            # ส่งไป Scan
            prediction = model.predict(temp_path).json()
            
            st.image(image, caption="รูปภาพที่ส่งตรวจ", use_container_width=True)
            
            st.subheader("🔍 ผลการวิเคราะห์")
            if prediction['predictions']:
                for pred in prediction['predictions']:
                    confidence = pred['confidence'] * 100
                    st.success(f"✅ ตรวจพบ: **{pred['class']}**")
                    st.progress(pred['confidence']) # เพิ่มแถบแสดงความมั่นใจ
                    st.write(f"ระดับความมั่นใจ: {confidence:.2f}%")
            else:
                st.warning("⚠️ ไม่พบข้อมูลทุเรียนในภาพนี้ กรุณาลองใหม่อีกครั้ง")
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
        
   
        if os.path.exists(temp_path):
            os.remove(temp_path)

st.divider()
st.info("💡 คำแนะนำ: ควรตรวจสอบทุเรียนในที่ที่มีแสงสว่างเพียงพอเพื่อให้ AI ทำงานได้แม่นยำที่สุด")


