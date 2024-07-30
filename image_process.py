import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from io import BytesIO
import base64
from streamlit_option_menu import option_menu
from google.cloud import texttospeech
from google.cloud import speech
from google.oauth2.service_account import Credentials

# Function to reset Streamlit state

GOOGLE_API_KEY = 'AIzaSyBJk0fGQlA54CgIP7tH9DYNzn1xzOUofe4'
genai.configure(api_key=GOOGLE_API_KEY)

credentials = Credentials.from_service_account_file(
    'avian-serenity-427813-m3-21c0537027ca.json')

# def reset_state():
#     for key in st.session_state.keys():
#         del st.session_state[key]

# Function to play audio


def play_audio(file_path):
    audio_file = open(file_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')


st.set_page_config(
    page_title="OPTI GUIDE",
    page_icon="🧐",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "VISUAL OPTIONS",
        ["Upload Image", "Capture Image"],
        menu_icon='Home',
        icons=["image-fill", "camera-fill"],
        default_index=0
    )


# if 'restart' in st.session_state and st.session_state['restart']:
#     reset_state()


if user_picked == 'Upload Image':

    st.title("***OptiGuide***")

    st.markdown(
        "<h5 style='color: skyblue;'>UPLOAD YOUR IMAGE HERE:</h5>",
        unsafe_allow_html=True
    )

    # File uploader
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        # st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Save uploaded file to a temporary path
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        file_path = "temp_image.png"

        # Step 2: Process the Image using Multimodal LLM
        sample_file = genai.upload_file(
            path=file_path, display_name="Sample drawing")
        image_file = genai.get_file(name=sample_file.name)

        system_prompt = """

                You are a friendly, helpful Visual Guide for people with visual impairments or difficulties. Your task is to analyze images and provide concise, informative descriptions to help users navigate their surroundings safely and confidently.

                For each image:

                1. Quickly assess the scene for any immediate dangers or obstacles. If present, start your response with a clear, calm warning.

                2. Describe the main elements of the scene in a brief, easy-to-understand manner. Focus on:
                - General setting (indoor/outdoor, type of room/environment)
                - Key objects or structures
                - Relative positions of important elements
                - Any text or signs visible in the image

                3. Mention any relevant details that could affect movement or interaction, such as:
                - Surface conditions (wet floors, uneven terrain)
                - Lighting conditions
                - Presence of people or animals

                4. Use clear, simple language and avoid technical terms.

                5. Speak in a warm, friendly tone as if you're right beside the user. Use phrases like "To your left," "In front of you," or "About 10 steps ahead."

                6. If the image is unclear or you're unsure about certain elements, say so honestly.

                7. Keep your description under 100 words unless more detail is crucial for safety.

                Remember, your goal is to help the user form a mental picture of their surroundings quickly and safely. Be their trusted companion and guide.

        """

        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(
            [system_prompt, sample_file])

        generated_text = response.text
        # st.write("Generated Text:")
        # st.write(generated_text)

# ---------------------------------------------------------------------------------------

        client = texttospeech.TextToSpeechClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=response.text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name='en-US-Journey-F'
        )

        # en-US-Journey-F
        # en-US-Wavenet-F

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,

            speaking_rate=1,
            pitch=1
        )

        audio_response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # audio_bytes = open(audio_response.audio_content, "rb").read()
        st.audio(audio_response.audio_content)

# ---------------------------------------------------------------------------------------

        # Step 3: Convert Text to Speech using gTTS
        # tts = gTTS(text=generated_text, lang='en')
        # tts.save("output.mp3")

        # # Step 4: Play the Audio
        # play_audio("output.mp3")

        st.write('Please Select "BROWSE FILES" button to upload new image.')

        # Step 5: Restart Button
        # if st.button('Restart'):
        #     # st.session_state['restart'] = True
        #     st.experimental_rerun()
    else:
        # st.write("Please upload an image.")
        pass

if user_picked == 'Capture Image':

    st.title("***OptiGuide***")

    st.markdown(
        "<h5 style='color: skyblue;'>CAPTURE YOUR PICTURE HERE:</h5>",
        unsafe_allow_html=True
    )
    picture = st.camera_input("")

    if picture:
        with open("cap_image.png", "wb") as f:
            f.write(picture.getbuffer())

        file_path = "cap_image.png"

        sample_file = genai.upload_file(
            path=file_path, display_name="Sample drawing")
        image_file = genai.get_file(name=sample_file.name)

        system_prompt = """

                You are a friendly, helpful Visual Guide for people with visual impairments or difficulties. Your task is to analyze images and provide concise, informative descriptions to help users navigate their surroundings safely and confidently.

                For each image:

                1. Quickly assess the scene for any immediate dangers or obstacles. If present, start your response with a clear, calm warning.

                2. Describe the main elements of the scene in a brief, easy-to-understand manner. Focus on:
                - General setting (indoor/outdoor, type of room/environment)
                - Key objects or structures
                - Relative positions of important elements
                - Any text or signs visible in the image

                3. Mention any relevant details that could affect movement or interaction, such as:
                - Surface conditions (wet floors, uneven terrain)
                - Lighting conditions
                - Presence of people or animals

                4. Use clear, simple language and avoid technical terms.

                5. Speak in a warm, friendly tone as if you're right beside the user. Use phrases like "To your left," "In front of you," or "About 10 steps ahead."

                6. If the image is unclear or you're unsure about certain elements, say so honestly.

                7. Keep your description under 100 words unless more detail is crucial for safety.

                Remember, your goal is to help the user form a mental picture of their surroundings quickly and safely. Be their trusted companion and guide.

        """

        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest")
        response = model.generate_content(
            [system_prompt, sample_file])

        generated_text = response.text
        # st.write("Generated Text:")
        # st.write(generated_text)

# ----------------------------------------------------------------------------

        client = texttospeech.TextToSpeechClient(credentials=credentials)

        synthesis_input = texttospeech.SynthesisInput(text=response.text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name='en-US-Journey-F'
        )

        # en-US-Journey-F
        # en-US-Wavenet-F

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,

            speaking_rate=1,
            pitch=1
        )

        audio_response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # audio_bytes = open(audio_response.audio_content, "rb").read()
        st.audio(audio_response.audio_content)

# ------------------------------------------------------------------------------

        # Step 3: Convert Text to Speech using gTTS
        # tts = gTTS(text=generated_text, lang='en')
        # tts.save("output.mp3")

        # # Step 4: Play the Audio
        # play_audio("output.mp3")

        st.write('Please Select "CLEAR PHOTO" button to CAPTURE a new image.')
