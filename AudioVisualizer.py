import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av

# Audio processing class using WebRTC
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.data = None

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio frame to numpy array
        audio = frame.to_ndarray()
        # Store the first audio channel for processing
        self.data = audio[:, 0]
        return frame

# Visualize waveform
def visualize_waveform(audio_data, color, fig, ax):
    ax.clear()
    ax.plot(audio_data, color=color)
    ax.set_ylim(-1.0, 1.0)  # Normalize audio data to between -1 and 1
    ax.set_xlim(0, len(audio_data))
    ax.set_title("Waveform")
    ax.set_facecolor('black')
    return fig

# Visualize bar pattern
def visualize_bars(audio_data, color, fig, ax):
    ax.clear()
    ax.bar(np.arange(len(audio_data)), audio_data, color=color)
    ax.set_ylim(-1.0, 1.0)  # Normalize audio data to between -1 and 1
    ax.set_xlim(0, len(audio_data))
    ax.set_title("Bar Pattern")
    ax.set_facecolor('black')
    return fig

# Visualize circular pattern
def visualize_circular(audio_data, color, fig, ax):
    ax.clear()
    angles = np.linspace(0, 2 * np.pi, len(audio_data))
    ax.plot(angles, audio_data, color=color)
    ax.set_ylim(-1.0, 1.0)  # Normalize audio data to between -1 and 1
    ax.set_xlim(0, 2 * np.pi)
    ax.set_title("Circular Pattern")
    ax.set_facecolor('black')
    return fig

# Streamlit app UI
st.title("Real-Time Music Visualizer with WebRTC")
st.write("This app captures your browser's microphone input and generates real-time visual patterns.")

# Sidebar for user input
st.sidebar.title("Customize Visualization")
pattern = st.sidebar.selectbox("Choose a pattern", ["Waveform", "Bar Pattern", "Circular"])
default_color = st.sidebar.color_picker("Pick a color", "#00f900")  # Default is a bright green

# Set up WebRTC for real-time audio capture
webrtc_ctx = webrtc_streamer(
    key="audio-stream",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=1024,
    audio_processor_factory=AudioProcessor,  # Replacing deprecated argument
    media_stream_constraints={"audio": True, "video": False},
)

# Create the plot
fig, ax = plt.subplots()

# If audio is being processed
if webrtc_ctx.audio_receiver:
    processor = webrtc_ctx.audio_processor
    placeholder = st.empty()
    
    if processor and processor.data is not None:
        audio_data = processor.data

        # Select the visualization pattern
        if pattern == "Waveform":
            fig = visualize_waveform(audio_data, default_color, fig, ax)
        elif pattern == "Bar Pattern":
            fig = visualize_bars(audio_data, default_color, fig, ax)
        elif pattern == "Circular":
            fig = visualize_circular(audio_data, default_color, fig, ax)

        # Display the plot in Streamlit
        placeholder.pyplot(fig)
    else:
        st.write("Waiting for audio input...")
