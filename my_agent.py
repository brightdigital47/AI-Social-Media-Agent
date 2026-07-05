import os
import streamlit as st
import google.generativeai as genai

# 🔐 तिजोरी (Secrets) से सुरक्षित तरीके से चाबी उठाना
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# 🌐 वेबसाइट का सेटअप और डिजाइन
st.set_page_config(
    page_title="ViraLens AI - Video Automation", 
    page_icon="🎬", 
    layout="wide"
)

# 🗂️ साइडबार (Sidebar) का डिजाइन
with st.sidebar:
    st.title("🤖 ViraLens AI")
    st.write("आपका सोशल मीडिया एआई कोपायलट।")
    st.markdown("---")
    st.subheader("⚙️ Connected Accounts")
    st.checkbox("🔴 YouTube Shorts", value=False, disabled=True)
    st.checkbox("📸 Instagram Reels", value=False, disabled=True)
    st.info("💡 ऑटो-पोस्टिंग फीचर्स जल्द आ रहे हैं!")
    st.markdown("---")
    st.markdown("Developed by **Bright Digital**")

# 🏛️ मुख्य पेज का डिजाइन (2 Columns Layout)
col1, col2 = st.columns(2)

with col1:
    st.title("🎬 AI Video Automation Platform")
    st.write("अपनी रील या शॉर्ट्स अपलोड करें। एआई वीडियो को खुद स्कैन करके सबसे बेस्ट वायरल कंटेंट तैयार करेगा।")
    
    # वीडियो अपलोडर बॉक्स
    uploaded_file = st.file_uploader("यहाँ अपनी video फाइल (MP4) अपलोड करें", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)

with col2:
    st.markdown("### 📊 AI Analytics & Content Hub")
    st.write("आपके वीडियो का रिजल्ट यहाँ दिखाई देगा:")
    
    if uploaded_file is not None:
        if st.button("✨ वीडियो स्कैन करें और वायरल पोस्ट बनाएं"):
            with st.spinner("🧠 एआई वीडियो का गहराई से एनालिसिस कर रहा है..."):
                try:
                    # टेम्परेरी फाइल बनाना
                    with open("temp_video.mp4", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    video_file = genai.upload_file(path="temp_video.mp4")
                    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                    
                    prompt = """
                    तुम एक सोशल मीडिया एक्सपर्ट हो। इस वीडियो को पूरा देखो और समझो।
                    इसके आधार पर निम्नलिखित चीजें सुंदर पॉइंट्स में तैयार करो:
                    1. 🔥 3 धमाकेदार टाइटल्स (YouTube Shorts के लिए)।
                    2. 📝 1 सस्पेंस से भरा हुआ इंस्टाग्राम रील्स कैप्शन (हिंदी-इंग्लिश मिक्स भाषा में)।
                    3. 🚀 टॉप 10 वायरल होने वाले हैशटैगส์ (#)।
                    """
                    
                    response = model.generate_content([video_file, prompt])
                    os.remove("temp_video.mp4")
                    
                    # सीधा रिस्पॉन्स दिखाना
                    st.success("🎉 पोस्ट डिटेल्स तैयार हैं!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ एक गड़बड़ हो गई: {e}")
    else:
        st.info("👈 शुरुआत करने के लिए बाईं तरफ एक वीडियो फाइल अपलोड करें।")
