# Hairstyle-Recommending-chatbot
# 💇‍♂️ AI Hairstyle Suggester & Hair Chatbot

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

### 🛡️ Smart Grooming & Scalp Care Assistant
An intelligent personal grooming platform that combines **Computer Vision** and **Generative AI**. This application estimates your face shape through landmark detection to suggest the most flattering hairstyles and features a specialized AI chatbot for expert hair and scalp care advice.

---

## 📌 Project Highlights

* **Face Shape Analysis:** Uses **MediaPipe Face Mesh** to map 468+ facial landmarks and calculate geometry-based shapes (Oval, Round, Square, Heart, Diamond).
* **Smart Recommendations:** Tailored hairstyle suggestions categorized by both face shape and gender.
* **AI Hair Consultant:** Integrated **Groq (Llama 3)** chatbot to provide professional advice on hair fall, dandruff, and routine care.
* **Real-time UI:** Built with **Streamlit** for a seamless, dual-column experience (Analysis & Chat).

---

## 📊 How It Works



1.  **Landmark Extraction:** Detects specific coordinate points on the forehead, cheekbones, and jawline.
2.  **Geometric Ratios:** Compares Face Length vs. Cheekbone Width using Euclidean distance formulas.
3.  **Classification Logic:**
    * **Square:** Length and Width are nearly equal with a strong jawline.
    * **Round:** Similar to square but with softer, curved angles.
    * **Oblong:** Face length is significantly greater than the cheek width ($Ratio > 1.65$).

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Computer Vision:** OpenCV, MediaPipe
* **LLM Integration:** Groq API (Llama3-70b-8192)
* **Environment:** Python-Dotenv

---
