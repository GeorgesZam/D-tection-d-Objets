import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from PIL import Image

# Détection d'objets (exemple simple, à remplacer par un modèle de détection réel)
class ObjectDetectionTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Traitement de l'image pour la détection d'objets (à implémenter)
        # Exemple : dessin d'un rectangle sur l'image
        height, width, _ = img.shape
        cv2.rectangle(img, (0, 0), (width, height), (0, 255, 0), 10)
        return img

# Interface utilisateur
st.title("Détection d'Objets avec Caméra")
st.write("Utilisez votre caméra pour capturer des images et détecter des objets.")

# Capture vidéo via la caméra du navigateur
webrtc_streamer(key="example", video_transformer_factory=ObjectDetectionTransformer)
