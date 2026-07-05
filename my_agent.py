import os
import streamlit as st
import google.generativeai as genai

# 🔐 यहाँ हमने पुराना पासवर्ड हटा दिया है, अब यह सीधे आपकी लाइव वेबसाइट की तिजोरी (Secrets) से चाबी उठाएगा!
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ तिजोरी (Secrets) में GEMINI_API_KEY नहीं मिली! कृपया Manage app -> Secrets में जाकर इसे सेट करें।")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# 🌐 वेबसाइट का सेटअप और डिजाइन
st.set_page_config(page_title="AI Social Media Auto-Poster", page_icon="🎬", layout="centered")

st.title("🎬 AI Video Automation Platform")
st.write("अपनी वीडियो रील या शॉर्ट्स अपलोड करें। एआई वीडियो को खुद देखकर वायरल कंटेंट लिखेगा!")

# 📁 वेबसाइट पर वीडियो अपलोड करने का बॉक्स
uploaded_file = st.file_uploader("यहाँ अपनी वीडियो फाइल (MP4) अपलोड करें", type=["mp4", "mov", "avi"])

# 🚀 जैसे ही वीडियो अपलोड होगी, जादू शुरू होगा
if uploaded_file is not None:
    st.video(uploaded_file) # वेबसाइट पर वीडियो का प्रीव्यू दिखाना
    
    if st.button("✨ वीडियो स्कैन करें और वायरल पोस्ट बनाएं"):
        with st.spinner("⏳ एआई आपकी वीडियो को देख रहा है... कृपया थोड़ा इंतज़ार करें।"):
            
            try:
                # 1. वीडियो को एक टेम्परेरी फाइल में सुरक्षित करना
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. वीडियो को गूगल एआई सर्वर पर अपलोड करना
                st.write("📹 वीडियो गूगल एआई सर्वर पर अपलोड हो रही है...")
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # 3. जेमिनी को वीडियो के साथ निर्देश (Prompt) देना
                st.write("🧠 एआई वीडियो का गहराई से एनालिसिस कर रहा है...")
                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                
                prompt = """
                तुम एक सोशल मीडिया एक्सपर्ट हो। इस वीडियो को पूरा देखो, समझो कि इसके अंदर क्या चल रहा है या क्या बोला जा रहा है। 
                फिर इसके आधार पर निम्नलिखित चीजें तैयार करो:
                1. 3 सबसे आकर्षक टाइटल्स (YouTube Shorts के लिए)।
                2. 1 सस्पेंस से भरा हुआ इंस्टाग्राम रील्स कैप्शन (हिंदी-इंग्लिश मिक्स भाषा में)।
                3. टॉप 10 वायरल होने वाले हैशटैगส์ (#) जो इस वीडियो को ट्रेंडिंग में ले जाएं।
                """
                
                response = model.generate_content([video_file, prompt])
                
                # 4. टेम्परेरी फाइल को डिलीट करना
                os.remove("temp_video.mp4")
                
                # वेबसाइट स्क्रीन पर रिजल्ट दिखाना
                st.success("🎉 एआई ने वीडियो देखकर पोस्ट डिटेल्स तैयार कर ली हैं!")
                st.subheader("📝 आपकी वायरल पोस्ट की डिटेल्स:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ एक गड़बड़ हो गई: {e}")
