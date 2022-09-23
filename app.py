# import des packages et lecture des fichiers
import numpy as np, pandas as pd, geopandas as gpd
from greppo import app
exf = gpd.read_file('/EXFAR00.json')
dep = gpd.read_file('/dep.json')
reg = gpd.read_file('/reg.json')

# création des ronds
variables = ["Recolte de bois", "Recolte de bois/Grumes", "Recolte de bois/Bois d'industrie", "Recolte de bois/Bois energie"]
colors = ['brown', 'green', 'blue', 'red']
k = ((550000/3) / (exf['Recolte de bois'].sum()* np.pi))**0.5 # pour obtenir 1/7 de la surface France
ronds=list()
for i,v in enumerate(variables):
    r = exf.centroid.buffer(1000*k*exf[v]**0.5)
    r = gpd.GeoDataFrame(r,geometry=0)
    r = r.to_crs(epsg=4326)
    r = pd.merge(r, exf[[v,'Departement']], left_index=True, right_index=True)
    ronds.append(r)

# appel des couches
app.display(name='title', value='Enquete EXFSRI 2020')
for i in range(4):
    app.vector_layer(
        data=ronds[i],
        name=variables[i],
        style={"color":colors[i]},
        visible=False,)
app.base_layer(
    name="Open Street Map",
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",)
app.base_layer(
    name="Open Street Map",
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",)
app.vector_layer(
    data=reg,
    name="Regions",
    style={"color":'black', "fillOpacity":"0"},)
app.vector_layer(
    data=dep,
    name="Departements",
    style={"color":'dimgrey', "fillOpacity":"0", "weight":"1"},
    visible=False,)
