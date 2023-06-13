import streamlit as st

from app.helpers import load_audio_segment, plot_audio

def _load_example(name: str):
    st.markdown("<center><h3> Оригинал </h3></center>", unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        auseg = load_audio_segment(f"samples/{name}", "mp3")
        plot_audio(auseg, step=50)
    with cols[1]:
        audio_file = open(f"samples/{name}", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes)
    
    for file in ["vocals.mp3", "drums.mp3", "bass.mp3", "other.mp3"]:
        st.markdown("<br>", unsafe_allow_html=True)
        label = file.split(".")[0].capitalize()
        label = {
            "Drums": "🥁",
            "Bass": "🎸",
            "Other": "🎹",
            "Vocals": "🎤",
        }.get(label)  + " " + label
        st.markdown("<center><h3>" + label + "</h3></center>", unsafe_allow_html=True)

        cols = st.columns(2)
        with cols[0]:
            auseg = load_audio_segment(f"samples/{name.split('.mp3')[0]}/{file}", "mp3")
            plot_audio(auseg, step=50)
        with cols[1]:
            audio_file = open(f"samples/{name.split('.mp3')[0]}/{file}", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes)
    

def show_examples():
    with st.columns([2, 8, 1])[1]:
        selection = st.selectbox("Выберите любой трек из примеров, чтобы сразу увидеть результат", ["Queen - We Will Rock You", "Stephen Sanchez - Until I Found You", "Michael Jackson - Billie Jean"])
    if selection == "Queen - We Will Rock You":
        _load_example("Queen - We Will Rock You.mp3")
    elif selection == "Stephen Sanchez - Until I Found You":
        _load_example("Stephen Sanchez - Until I Found You.mp3")
    elif selection == "Michael Jackson - Billie Jean":
        _load_example("Michael Jackson - Billie Jean.mp3")
