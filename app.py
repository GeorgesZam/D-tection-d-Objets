import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, VideoFrame

class ObjectDetectionTransformer(VideoTransformerBase):
    def transform(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # Pour l'exemple, on dessine un rectangle vert autour de l'image
        height, width, _ = img.shape
        cv2.rectangle(img, (50, 50), (width - 50, height - 50), (0, 255, 0), 10)
        return VideoFrame.from_ndarray(img, format="bgr24")

# Interface utilisateur
st.title("Détection d'Objets avec Caméra")
st.write("Utilisez votre caméra pour capturer des images et détecter des objets.")

# Capture vidéo via la caméra du navigateur
webrtc_ctx = webrtc_streamer(
    key="example", 
    video_transformer_factory=ObjectDetectionTransformer,
    media_stream_constraints={
        "video": True,
        "audio": False
    }
)

if webrtc_ctx.video_transformer:
    webrtc_ctx.video_transformer.flip = st.checkbox("Flip", value=True)
