import numpy as np
import pandas as pd
import geopandas as gpd
from greppo import app

# lecture des fichiers
exf = gpd.read_file('C:/Users/benoit.mirouse/Documents/test/EXFAR00.json')
dep = gpd.read_file('C:/Users/benoit.mirouse/Documents/test/dep.json')
reg = gpd.read_file('C:/Users/benoit.mirouse/Documents/test/reg.json')

# pour obtenir 1/7 de la surface France
k = ((550000/3) / (exf['Recolte de bois'].sum()* np.pi))**0.5

# création des ronds
variables = ["Recolte de bois", "Recolte de bois/Grumes", "Recolte de bois/Bois d'industrie", "Recolte de bois/Bois energie"]
colors = ['brown', 'green', 'blue', 'red']
ronds=list()
for i,v in enumerate(variables):
    r = exf.centroid.buffer(1000*k*exf[v]**0.5)
    r = gpd.GeoDataFrame(r,geometry=0)
    r = r.to_crs(epsg=4326)
    r = pd.merge(r, exf[[v,'Departement']], left_index=True, right_index=True)
    ronds.append(r)

# couches
app.display(name='title', value='Enquete EXFSRI')
for i in range(4):
    app.vector_layer(
        data=ronds[i],
        name=variables[i],
        style={"color":colors[i]},
        visible=False,)
app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",)
app.vector_layer(
    data=reg,
    name="Regions",
    style={"color":'black', "fillOpacity":"0"},
    visible=True,)
app.vector_layer(
    data=dep,
    name="Departements",
    style={"color":'dimgrey', "fillOpacity":"0", "weight":"1"},
    visible=False,)