import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from geopy.geocoders import Nominatim

# Fonction pour convertir une adresse en coordonnées géographiques
def geocode(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Fonction pour calculer le coût d'une route
def calculate_edge_cost(u, v, data):
    max_speed = data.get("maxspeed", "50")
    if isinstance(max_speed, list):
        max_speed = max_speed[0]
    max_speed = int(max_speed.split()[0])
    
    # Coût basé sur la limitation de vitesse
    cost = 1 / max_speed
    
    # Augmentez le coût si la route est en zone urbaine
    if "urban" in data.get("tags", []):
        cost *= 1.5
    
    return cost

# Téléchargez le graphe de la région
place_name = "Paris, France"
graph = ox.graph_from_place(place_name, network_type='drive')

# Simplifiez le graphe
graph = ox.simplify_graph(graph)

# Filtrez les routes avec péages
graph = ox.remove_isolated_nodes(graph)

# Appliquer la fonction de coût aux arêtes du graphe
for u, v, data in graph.edges(data=True):
    data["cost"] = calculate_edge_cost(u, v, data)

# Interface utilisateur Streamlit
st.title("GPS - Itinéraire le moins cher")

start_address = st.text_input("Adresse de départ")
end_address = st.text_input("Adresse d'arrivée")

if st.button("Calculer l'itinéraire"):
    start_coords = geocode(start_address)
    end_coords = geocode(end_address)
    
    if start_coords and end_coords:
        start_lat, start_lon = start_coords
        end_lat, end_lon = end_coords
        
        source = ox.distance.nearest_nodes(graph, X=start_lon, Y=start_lat)
        target = ox.distance.nearest_nodes(graph, X=end_lon, Y=end_lat)
        
        # Utilisez Dijkstra pour trouver le chemin le moins cher
        route = nx.shortest_path(graph, source, target, weight="cost")
        
        # Visualisez l'itinéraire
        route_map = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=13)
        route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)
        folium.Marker(location=start_coords, popup="Départ").add_to(route_map)
        folium.Marker(location=end_coords, popup="Arrivée").add_to(route_map)
        
        # Affichez la carte dans Streamlit
        route_map.save("route.html")
        st.markdown('<iframe src="route.html" width="100%" height="500"></iframe>', unsafe_allow_html=True)
    else:
        st.error("Impossible de géocoder l'une des adresses. Veuillez vérifier les adresses et réessayer.")
