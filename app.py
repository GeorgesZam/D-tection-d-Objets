import streamlit as st
import folium
import requests
from geopy.geocoders import Nominatim

# Fonction pour convertir une adresse en coordonnées géographiques
def geocode(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Fonction pour obtenir l'itinéraire depuis OpenRouteService
def get_route(start_coords, end_coords, api_key):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [
            [start_coords[1], start_coords[0]],
            [end_coords[1], end_coords[0]]
        ],
        "options": {
            "avoid_features": ["tollways"]
        }
    }
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Interface utilisateur Streamlit
st.title("GPS - Itinéraire le moins cher")
api_key = st.text_input("Entrez votre clé API OpenRouteService")
start_address = st.text_input("Adresse de départ")
end_address = st.text_input("Adresse d'arrivée")

if st.button("Calculer l'itinéraire"):
    start_coords = geocode(start_address)
    end_coords = geocode(end_address)
    
    if start_coords and end_coords:
        route_data = get_route(start_coords, end_coords, api_key)
        
        if "routes" in route_data:
            route_coords = [(coord[1], coord[0]) for coord in route_data["routes"][0]["geometry"]["coordinates"]]
            
            # Visualisez l'itinéraire
            route_map = folium.Map(location=[(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2], zoom_start=13)
            folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)
            folium.Marker(location=start_coords, popup="Départ").add_to(route_map)
            folium.Marker(location=end_coords, popup="Arrivée").add_to(route_map)
            
            # Affichez la carte dans Streamlit
            route_map.save("route.html")
            st.markdown('<iframe src="route.html" width="100%" height="500"></iframe>', unsafe_allow_html=True)
        else:
            st.error("Erreur lors de la récupération de l'itinéraire.")
    else:
        st.error("Impossible de géocoder l'une des adresses. Veuillez vérifier les adresses et réessayer.")
