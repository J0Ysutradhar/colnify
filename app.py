import streamlit as st
import requests
import os

# Set up Streamlit multipage navigation
st.set_page_config(page_title="Clonify", page_icon="🔊", layout="wide")

# Sidebar navigation
st.sidebar.title("MetaxSoul Studio")
page = st.sidebar.radio("Go to", ["Text to Speech", "Voice Cloner"])

# API Headers new vr
headers = {
                "AUTHORIZATION": "ak-cce693da67ce45e9a47cbc172278d672",
                "X-USER-ID": "YeYce8PYkGVA3QEM8uU1KO79C9Y2",
                "Content-Type": "application/json"
            }
#play old vr
HEADERS = {
    "accept": "application/json",
    "AUTHORIZATION": "f8bba56ae13444929b9c7decf7dd1f2e",
    "X-USER-ID": "3folRXPfRlPupj0RzWHuCPq4tAo2"
}
# --------------------------------------
# PAGE 1: TEXT TO SPEECH (Existing Functionality)
# --------------------------------------
if page == "Text to Speech":
    st.title("🎤 Clonify Ai- Text to Speech")

    txt = st.text_area("Enter Text:")
    
    # Language selection
    languages = {
        "English": "english",
        "Bengali": "bengali",
        "Hindi": "hindi",
        "Korean": "korean",
        "Japanese": "japanese",
        "Spanish": "spanish",
        "Arabic": "arabic",
        "French": "french",
        "Chinese": "mandarin",
        "German": "german",
    }
    language = st.selectbox("Select Language:", list(languages.keys()))

    # Voice selection
    voices = {
        
        "Celebrety's Voice👇":"s3://voice-cloning-zero-shot/57539b64-ff1a-4f8a-926f-7fefb5427f93/srk/manifest.json",
        "Sharuk Khan":"s3://voice-cloning-zero-shot/57539b64-ff1a-4f8a-926f-7fefb5427f93/srk/manifest.json",
        "MD Younus": "s3://voice-cloning-zero-shot/616478fb-18e7-42da-829f-218da2d7108b/joy/manifest.json",
        "Joy": "s3://voice-cloning-zero-shot/d8b5837f-38b1-4d9e-ab74-6c552f2e0632/original/manifest.json",
        "Modi": "s3://voice-cloning-zero-shot/ad8d759d-818a-4218-8680-1cf79ccbcb2e/original/manifest.json",
        "--------------------------------":"null",
        "Adolfo": "s3://voice-cloning-zero-shot/d82d246c-148b-457f-9668-37b789520891/adolfosaad/manifest.json",
        "Olivia": "s3://voice-cloning-zero-shot/9fc626dc-f6df-4f47-a112-39461e8066aa/oliviaadvertisingsaad/manifest.json",
        "Billy": "s3://voice-cloning-zero-shot/37e5af8b-800a-4a76-8f31-4203315f8a9e/billysaad/manifest.json",
        "Bryan": "s3://voice-cloning-zero-shot/4c627545-b9c0-4791-ae8e-f48f5475247c/bryansaad/manifest.json",

        "🛠️ Use Custom Voice": "custom"
    }
    voice = st.selectbox("Select Voice Model:", list(voices.keys()))

    # If user selects custom voice, show input field
    custom_voice_url = ""
    if voice == "🛠️ Use Custom Voice":
        custom_voice_url = st.text_input("Enter Custom Voice Link (s3://...):")

    # Emotion selection
    emotions = {
        "Male Happy": "male_happy",
        "Male Sad": "male_sad",
        "Male Angry": "male_angry",
        "Male Fearful": "male_fearful",
        "Male Surprised": "male_surprised",
        "Female Happy": "female_happy",
        "Female Sad": "female_sad",
        "Female Angry": "female_angry",
        "Female Fearful": "female_fearful",
        "Female Surprised": "female_surprised",
    }
    emotion = st.selectbox("Emotion:", list(emotions.keys()))

    # Voice speed slider
    speed = st.slider("Voice Speed:", min_value=0.8, max_value=1.5, value=0.95, step=0.01)

    # Submit button
    if st.button("Generate Voice"):
        if txt:
            selected_voice = custom_voice_url if voice == "🛠️ Use Custom Voice" else voices[voice]

            if voice == "🛠️ Use Custom Voice" and not custom_voice_url:
                st.warning("Please enter a custom voice link.")
            else:
                payload = {
                    "model": "PlayDialog",
                    "speed": speed,
                    "text": txt,
                    "voice": selected_voice,
                    "language": languages[language],
                    "outputFormat": "wav",
                    "emotion": emotions[emotion],
                    "voice_conditioning_seconds": 20,
                    "voice_conditioning_seconds_2": 20,
                    "voice_guidance": 3,
                    "style_guidance": 20,
                    "text_guidance": 1
                }

                response = requests.post("https://api.play.ai/api/v1/tts/stream", json=payload, headers=headers)

                try:
                    response.raise_for_status()
                    output_filename = "output.wav"
                    with open(output_filename, "wb") as audio_file:
                        audio_file.write(response.content)
                    st.success("Audio generated successfully!")
                    st.audio(output_filename, format="audio/wav")
                except requests.exceptions.HTTPError as err:
                    st.error(f"Error: {err}")
                    st.text(response.text)
        else:
            st.warning("Please enter some text.")

# --------------------------------------
# PAGE 2: VOICE CLONER
# --------------------------------------
elif page == "Voice Cloner":
    st.title("🎙️ Voice Cloner - Clone voice instantly")
    st.caption("Create anyone voice colne with 30sec of audio")

    uploaded_file = st.file_uploader("Upload a voice sample (MP3)", type=["mp3"])
    voice_name = st.text_input("Enter a name for the cloned voice:")

    if st.button("Clone Voice"):
        if uploaded_file and voice_name:
            temp_filename = "temp_voice.mp3"
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Open file separately before passing it to requests
            with open(temp_filename, "rb") as audio_file:
                files = {"sample_file": (temp_filename, audio_file, "audio/mpeg")}
                payload = {"voice_name": voice_name}  # Simple dictionary

                response = requests.post(
                    "https://api.play.ht/api/v2/cloned-voices/instant",
                    data=payload,  # 🔥 FIX: Use 'data' instead of 'json'
                    files=files,
                    headers=HEADERS
                )

            try:
                response.raise_for_status()
                response_data = response.json()
                cloned_voice_id = response_data.get("id", "No ID found")  # Extract "id"

                # Display only the "id" for the user
                st.success("Voice cloned successfully!")
                st.write("🔗 **Cloned Voice ID:**")
                st.code(cloned_voice_id, language="plaintext")

            except requests.exceptions.HTTPError as err:
                st.error(f"Error: {err}")
                st.text(response.text)

            # Clean up temporary file
            os.remove(temp_filename)

        else:
            st.warning("Please upload a file and enter a voice name.")
    st.markdown("_________________")
    st.caption("Having problem with voice clone?")
    st.markdown(" Email me with the voice file"
    " I will notify you with the cloned voice"
    " E-mail: joysutradharpc@gmail.com")
    st.markdown("_________________")
    ##### Disclaime
    st.markdown("This Ai tool is only for ***Educational Purposes***.")
    st.markdown("Don't Misuse this tool")
    
