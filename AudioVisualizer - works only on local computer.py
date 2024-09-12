import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import struct
import random

# Audio stream configuration
RATE = 44100  # Sampling rate in Hz
CHUNK = 1024  # Number of audio samples per frame

def audio_stream():
    # Initialize pyaudio object
    p = pyaudio.PyAudio()

    # Open a stream to listen to the microphone input
    stream = p.open(format=pyaudio.paInt16,  # 16-bit resolution
                    channels=1,  # 1 channel (mono)
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    return stream

def get_audio_data(stream):
    # Read data from audio stream
    data = stream.read(CHUNK)
    # Unpack audio data and convert to numpy array
    data_np = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 128
    return data_np

def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def get_color_by_amplitude(audio_data):
    avg_amplitude = np.mean(audio_data)
    color_value = int((avg_amplitude / 256) * 255)
    return "#{:02x}{:02x}ff".format(color_value, 255 - color_value)

def visualize_waveform(audio_data, color, fig, ax):
    ax.clear()
    ax.plot(audio_data, color=color)
    ax.set_ylim(0, 256)
    ax.set_xlim(0, len(audio_data))
    ax.set_title("Waveform")
    ax.set_facecolor('black')
    return fig

def visualize_bars(audio_data, color, fig, ax):
    ax.clear()
    ax.bar(np.arange(len(audio_data)), audio_data, color=color)
    ax.set_ylim(0, 256)
    ax.set_xlim(0, len(audio_data))
    ax.set_title("Bar Pattern")
    ax.set_facecolor('black')
    return fig

def visualize_circular(audio_data, color, fig, ax):
    ax.clear()
    angles = np.linspace(0, 2 * np.pi, len(audio_data))
    ax.plot(angles, audio_data, color=color)
    ax.set_ylim(0, 256)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_title("Circular Pattern")
    ax.set_facecolor('black')
    return fig

def visualize_scatter(audio_data, color, fig, ax):
    ax.clear()
    scatter_colors = [get_random_color() for _ in audio_data] if random_color_toggle else [get_color_by_amplitude([y]) for y in audio_data]
    ax.scatter(np.arange(len(audio_data)), audio_data, color=scatter_colors)
    ax.set_ylim(0, 256)
    ax.set_xlim(0, len(audio_data))
    ax.set_title("Scatterplot Pattern")
    ax.set_facecolor('black')
    return fig

# Streamlit app UI
st.title("Real-Time Audio Visualizer")
st.write("This app captures your computer's microphone input and generates real-time visual patterns.")

# Sidebar for user input
st.sidebar.title("Customize Visualization")
pattern = st.sidebar.selectbox("Choose a pattern", ["Waveform", "Bar Pattern", "Circular", "Scatterplot"])
default_color = st.sidebar.color_picker("Pick a color", "#00f900")  # Default is a bright green
random_color_toggle = st.sidebar.checkbox("Random color over time")
y_axis_color_toggle = st.sidebar.checkbox("Color based on amplitude")

# Initialize the audio stream
stream = audio_stream()

# Create the plot
fig, ax = plt.subplots()

# Stream real-time audio data and update the plot
#if st.button('Start Visualizer'):
if 1==1:
    # Continuously stream and visualize the data
    placeholder = st.empty()
    while True:
        # Capture audio data
        audio_data = get_audio_data(stream)

        # Determine the color based on user selection
        if random_color_toggle:
            color = get_random_color()
        elif y_axis_color_toggle:
            color = get_color_by_amplitude(audio_data)
        else:
            color = default_color

        # Select the visualization pattern
        if pattern == "Waveform":
            fig = visualize_waveform(audio_data, color, fig, ax)
        elif pattern == "Bar Pattern":
            fig = visualize_bars(audio_data, color, fig, ax)
        elif pattern == "Circular":
            fig = visualize_circular(audio_data, color, fig, ax)
        elif pattern == "Scatterplot":
            fig = visualize_scatter(audio_data, color, fig, ax)

        # Display the plot in Streamlit
        placeholder.pyplot(fig)
