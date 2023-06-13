import logging
import os
from pathlib import Path

import requests
import streamlit as st
from app.examples import show_examples

from demucs_runner import separator
from lib.st_custom_components import st_audiorec
from helpers import load_audio_segment, plot_audio

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

max_duration = 10  # in seconds

model = "htdemucs"
extensions = ["mp3", "wav", "ogg", "flac"]  # we will look for all those file types.
two_stems = None   # only separate one stems from the rest, for instance

# Options for the output audio.
mp3 = True
mp3_rate = 320
float32 = False  # output as float 32 wavs, unsused if 'mp3' is True.
int24 = False  # output as int24 wavs, unused if 'mp3' is True.
# You cannot set both `float32 = True` and `int24 = True` !!


out_path = Path("/tmp")
in_path = Path("/tmp")

    
def run():
    st.set_page_config(layout="wide")

    st.markdown("<h1><center>Divide</center></h1>", unsafe_allow_html=True)
    st.markdown("<center><i>Сервис для разделения аудиофайлов на: вокал, бас, ударные и другой инстурментал</i></center>", unsafe_allow_html=True)
    st.markdown("""
                <style>
                    .st-af {
                        font-size: 1.5rem;
                        align-items: center;
                        padding-right: 2rem;
                    }
                </style>
                """,
                unsafe_allow_html=True,
    )
    filename = None
    st.markdown("<h2><center>Загрузить файл</center></h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Выберите файл", type=extensions, key="file", help="Поддерживаемые форматы: mp3, wav, ogg, flac.")
    if uploaded_file is not None:
        with open(in_path / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())    
        filename = uploaded_file.name        
                
    if filename is not None:
        song = load_audio_segment(in_path / filename, filename.split(".")[-1])
        
        n_secs = round(len(song) / 1000)
        audio_file = open(in_path / filename, "rb")
        audio_bytes = audio_file.read()
        start_time = st.slider("Начать с", min_value=0, max_value=n_secs, step=1, value=0, help=f"Максимальный отрезок {max_duration} секунд.")
        _ = st.audio(audio_bytes, start_time=start_time)
        end_time = min(start_time + max_duration, n_secs)
        song = song[start_time*1000:end_time*1000]
        tot_time = end_time - start_time
        st.info(f"Аудиофайл будет обрабатываться от {start_time} до {end_time} секунд.", icon="⏱")
        execute = st.button("Начать обработку 🎶", type="primary")
        if execute:
            song.export(in_path / filename, format=filename.split(".")[-1])
            with st.spinner(f"Разделение аудиофайла займет около {round(tot_time*3.6)} секунд..."):
                separator(
                    tracks=[in_path / filename],
                    out=out_path,
                    model=model,
                    device="cpu",
                    shifts=1,
                    overlap=0.5,
                    stem=two_stems,
                    int24=int24,
                    float32=float32,
                    clip_mode="rescale",
                    mp3=mp3,
                    mp3_bitrate=mp3_rate,
                    jobs=os.cpu_count(),
                    verbose=True,
                )

            last_dir = ".".join(filename.split(".")[:-1])
            for file in ["vocals.mp3", "drums.mp3", "bass.mp3", "other.mp3"]:
                file = out_path / Path(model) / last_dir / file
                st.markdown("<hr>", unsafe_allow_html=True)
                label = file.name.split(".")[0].replace("_", " ").capitalize()
                # add emoji to label
                label = {
                    "Drums": "🥁",
                    "Bass": "🎸",
                    "Other": "🎹",
                    "Vocals": "🎤",
                }.get(label) + " " + label
                st.markdown("<center><h3>" + label + "</h3></center>", unsafe_allow_html=True)
 
                cols = st.columns(2)
                with cols[0]:
                   auseg = load_audio_segment(file, "mp3")
                   plot_audio(auseg)
                with cols[1]:
                    audio_file = open(file, "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes)
                    
if __name__ == "__main__":
    run()
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("Примеры", expanded=False):
        show_examples()