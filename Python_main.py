import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math
import os
from dotenv import load_dotenv
from hair_chatbot import hair_chatbot_response

load_dotenv()

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, color=(128, 128, 128))

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_face_shape(landmarks, img_width, img_height):
    lm = [(int(pt.x * img_width), int(pt.y * img_height))
          for pt in landmarks.landmark]

    forehead_l = lm[54]
    forehead_r = lm[284]
    cheek_l = lm[234]
    cheek_r = lm[454]
    jaw_l = lm[172]
    jaw_r = lm[397]
    forehead_top = lm[10]
    chin_bottom = lm[152]

    forehead_width = calculate_distance(forehead_l, forehead_r)
    cheekbone_width = calculate_distance(cheek_l, cheek_r)
    jawline_width = calculate_distance(jaw_l, jaw_r)
    face_length = calculate_distance(forehead_top, chin_bottom)

    if face_length == 0 or cheekbone_width == 0:
        return "Undetermined"

    length_cheek_ratio = face_length / cheekbone_width
    shape = "Undetermined"

    if length_cheek_ratio > 1.65:
        shape = "Oblong/Rectangle"
    elif abs(face_length - cheekbone_width) < face_length * 0.10 and \
         abs(cheekbone_width - forehead_width) < cheekbone_width * 0.12:
        shape = "Square"
    elif abs(face_length - cheekbone_width) < face_length * 0.15 and \
         cheekbone_width > forehead_width:
        shape = "Round"
    elif cheekbone_width > forehead_width and cheekbone_width > jawline_width:
        shape = "Diamond"
    elif forehead_width >= cheekbone_width * 0.95 and jawline_width < forehead_width * 0.85:
        shape = "Heart"
    else:
        shape = "Oval"

    return shape

suggestions = {
    ("Oval", "Female"): ["Long layers", "Shoulder-length waves", "Blunt bob"],
    ("Oval", "Male"): ["Classic Taper", "Pompadour", "Side part"],
    ("Round", "Female"): ["Long layers", "High updos", "Textured lob"],
    ("Round", "Male"): ["Undercut", "Pompadour", "Spiky texture"],
    ("Square", "Female"): ["Wavy textures", "Side-swept bangs"],
    ("Square", "Male"): ["Textured crops", "Classic side part"],
    ("Oblong/Rectangle", "Female"): ["Bangs", "Chin-length bobs"],
    ("Oblong/Rectangle", "Male"): ["Side part", "Crew cut"],
    ("Heart", "Female"): ["Chin-length bobs", "Side part"],
    ("Heart", "Male"): ["Textured quiff", "Side part", "Beard"],
    ("Diamond", "Female"): ["Curtain bangs", "Chin-length bobs"],
    ("Diamond", "Male"): ["Textured crops", "Messy styles"]
}

st.set_page_config(layout="wide", page_title="AI Hairstyle Suggester")
st.title("AI Hairstyle Suggester & Hair Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Upload a photo or ask me about hair care."}]

col1, col2 = st.columns([0.55, 0.45])

with col1:
    st.header("1. Analysis")
    gender = st.radio("Gender:", ('Female', 'Male'), horizontal=True)
    uploaded_file = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"])
    show_landmarks = st.checkbox("Show Landmarks")

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.image(image_rgb, caption='Uploaded Image', use_column_width=True)

        with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True) as face_mesh:
            results = face_mesh.process(image_rgb)
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                h, w, _ = image_rgb.shape
                shape = get_face_shape(face_landmarks, w, h)
                st.success(f"Estimated Shape: {shape}")
                
                key = (shape, gender)
                if key in suggestions:
                    st.subheader("Recommendations:")
                    for s in suggestions[key]:
                        st.markdown(f"- {s}")

with col2:
    st.header("2. Hair Chatbot")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = hair_chatbot_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})