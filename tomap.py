import folium

# Set the center location of the map (e.g., Taipei 101)
center_lat = 25.033964
center_lng = 121.564468

# Create a map object
mymap = folium.Map(location=[center_lat, center_lng], zoom_start=15)

# Add markers (you can add multiple markers)
folium.Marker(
    [25.033964, 121.564468],
    popup="Taipei 101",
    tooltip="Click for more",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(mymap)

folium.Marker(
    [25.037516, 121.5637],
    popup="MRT City Hall Station",
    tooltip="MRT Station",
    icon=folium.Icon(color='blue')
).add_to(mymap)

# Save the map to an HTML file
mymap.save("map_with_markers.html")
