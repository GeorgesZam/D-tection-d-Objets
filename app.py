import streamlit as st
import cv2
from PIL import Image
import numpy as np

# Fonction de détection d'objets (à implémenter)
def detect_objects(image):
    # Code pour détecter les objets
    return image

# Interface utilisateur
st.title("Détection d'Objets")
uploaded_file = st.file_uploader("Choisissez une image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Image chargée', use_column_width=True)
    
    # Détection d'objets
    result_image = detect_objects(np.array(image))
    st.image(result_image, caption='Image avec objets détectés', use_column_width=True)
