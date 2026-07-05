import os
import streamlit as st
import google.generativeai as genai

# 🔐 तिजोरी (Secrets) से सुरक्षित तरीके से चाबी उठाना
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# 🌐 वेबसाइट का सेटअप और डिजाइन (Modern Dark Theme Wide Layout)
st.set_page_config(
    page_title="ViraLens AI - Video Automation", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 वेबसाइट को प्रोफेशनल लुक देने के लिए कस्टम CSS (ChatGPT जैसा लुक)
st.markdown("""
    <style>
    .main { background-color: #0B0F19; color: #FFFFFF; }
    .stButton>button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    .report-box {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_with_html=True)

# 🗂️ प्रोफेशनल साइडबार (Sidebar) का डिजाइन
with st.sidebar:
    st.image("https://icons8.com", width=80)
    st.title("ViraLens AI")
    st.caption("The Ultimate Social Media Copilot")
    st.markdown("---")
    st.subheader("⚙️ Connected Accounts")
    st.checkbox("🔴 YouTube Shorts", value=False, disabled=True)
    st.checkbox("📸 Instagram Reels", value=False, disabled=True)
    st.checkbox("🔵 Facebook Shorts", value=False, disabled=True)
    st.info("💡 API इंटीग्रेशन जल्द ही आ रहा है!")
    st.markdown("---")
    st.markdown("Developed with ❤️ by **Bright Digital**")

# 🏛️ मुख्य पेज का डिजाइन (2 Columns Layout)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<h1 style='color: #6366F1;'>🎬 AI Video Automation Platform</h1>", unsafe_with_html=True)
    st.write("अपनी रील या शॉर्ट्स अपलोड करें। हमारा एडवांस एआई वीडियो को खुद स्कैन करके सबसे बेस्ट वायरल कंटेंट तैयार करेगा।")
    
    # अपलोडर बॉक्स
    uploaded_file = st.file_uploader("यहाँ अपनी वीडियो फाइल (MP4) अपलोड करें", type=["mp4", "mov", "avi"])
    
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
                    3. 🚀 टॉप 10 वायरल होने वाले हैशटैग्स (#)।
                    """
                    
                    response = model.generate_content([video_file, prompt])
                    os.remove("temp_video.mp4")
                    
                    # प्रोफेशनल रिपोर्ट बॉक्स में रिजल्ट दिखाना
                    st.success("🎉 पोस्ट डिटेल्स तैयार हैं!")
                    st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_with_html=True)
                    
                except Exception as e:
                    st.error(f"❌ एक गड़बड़ हो गई: {e}")
    else:
        st.info("👈 शुरुआत करने के लिए बाईं तरफ एक वीडियो फाइल अपलोड करें।")
