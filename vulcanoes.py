import pandas, folium


data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation <= 1000:
        return 'green'
    elif 1000 < elevation <= 2000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[56.949533,24.172519], tiles=None)
folium.TileLayer('openstreetmap').add_to(map)
folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
    attr='google',
    name='Google street view',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(map)
folium.raster_layers.TileLayer(
    tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
    attr='google',
    name='google Areal',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
    overlay=False,
    control=True,
).add_to(map)

fgv = folium.FeatureGroup(name="Vulcanos") #izveidojam FeatureGroup ar nosaukumu My map. FeatureGroup izmanto karšu slāņu parādīšanai.
for lt, ln, el in zip(lat, lon, elev):
    # ja kā ikonas uz kartes tad=>  fg.add_child(folium.Marker(location=[lt, ln], popup=f"{el} metri", icon=folium.Icon(color=color_producer(el))))
    fgv.add_child(folium.CircleMarker(location=[lt, ln], clustered_marker = True,popup=f"{el} metri", radius=8, fill_color=color_producer(el), color='grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 3_000_000
                                                        else 'orange' if 3_000_000 <= x['properties']['POP2005'] < 10_000_000
                                                        else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("volcanoes.html")
