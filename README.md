# AudioVisualizer
Simple Audio Visualizer


A simple Streamlit app that listens to the audio input of a computer and generates real-time visual patterns based on the rhythm or amplitude of the music.

The first idea was to use the pyaudio library to capture sound and matplotlib or plotly to generate visualizations, which will be displayed in Streamlit.
This worked fine on the computer locally, but not deployed on streamlit sharing.

The second try uses Streamlit WebRTC which should be able to run on Streamlit Sharing...
.. but it still does not work. So don't go to https://simpleaudiovisualizer.streamlit.app/
