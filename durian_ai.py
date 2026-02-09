import streamlit as st
from roboflow import Roboflow
from PIL import Image

ROBOFLOW_API_KEY = "rf_qx1IlPFbPmRVtwQr57gkMhb25zs1" 
PROJECT_NAME = "durian-detection-zb1dk"
VERSION_NUMBER = 3

st.set_page_config(page_title="Durian Smart AI")
st.title("🍈 Durian Smart AI Mobile")
st.write("วิธีใช้งาน: ถ่ายรูปทุเรียนเพื่อให้ AI ตรวจสอบความสุก")


try:
    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project(PROJECT_NAME)
    model = project.version(VERSION_NUMBER).model

  
    img_file = st.camera_input("กดปุ่มด้านล่างเพื่อถ่ายรูปทุเรียน")

    if img_file:
        image = Image.open(img_file)
        prediction = model.predict(image).json()
        st.image(image, caption="รูปของคุณ", use_container_width=True)
        
        st.write("### ผลการตรวจสอบ:")
        if prediction['predictions']:
            for pred in prediction['predictions']:
                st.success(f"พบ: {pred['class']} (ความแม่นยำ: {pred['confidence']:.2%})")
        else:
            st.warning("ไม่พบข้อมูลทุเรียนในภาพ")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
