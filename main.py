# pip install geopandas
# pip install matplot
# pip install geopandas matplotlib folium

import geopandas as gpd
import pandas as pd
import folium
import re

GEOJSON = "kuntarajat-2018-raw.geojson" 
CSV     = "vakiluku.csv"
OUTPUT  = "suomen_kunnat.html"

#Nimien normalisointi
def normalize(name: str) -> str:
    if not isinstance(name, str):
        return ""
    s = name.strip().casefold()
    s = s.replace("ä", "a").replace("ö", "o").replace("å", "a")
    s = re.sub(r"\s+", " ", s)
    return s

ALIASES = {
    "pedersoren kunta": "pedersore",   
}

gdf_raw = gpd.read_file(GEOJSON)

name_col = "NAMEFIN" if "NAMEFIN" in gdf_raw.columns else (
    "Kunta" if "Kunta" in gdf_raw.columns else (
        "name" if "name" in gdf_raw.columns else None
    )
)
if not name_col:
    raise ValueError(f"Kunnan nimi -saraketta ei löytynyt. Sarakkeet: {list(gdf_raw.columns)}")
print(f"Käytetään kunnannimi-saraketta: {name_col}")

#Pinta ala#
gdf_metric = gdf_raw.to_crs(epsg=3067).copy()
gdf_metric["Pinta_ala_km2"] = gdf_metric.geometry.area / 1e6

gdf = gdf_metric.to_crs(epsg=4326).copy()

vak = pd.read_csv(CSV)

#Yhdistä väkiluvut karttaan
vak_key = vak["Kunta"].map(normalize).replace(ALIASES)
gdf_key = gdf[name_col].map(normalize)

vak2 = pd.DataFrame({"__key": vak_key, "Väkiluku": vak["Väkiluku"]})
gdf["__key"] = gdf_key

gdf = gdf.merge(vak2, on="__key", how="left").drop(columns="__key")

# Raportoi kunnat joilta puuttui väkiluku
puuttuvat = gdf[gdf["Väkiluku"].isna()][name_col].tolist()
if puuttuvat:
    print("Huom. Kuntakartta on vuodelta 2018 ja asukasluvut ovat vuodelta 2025, joten seuraavat kunnat ovat yhdistyneet ja niiden tietoja ei ole saatavilla.")
    for n in puuttuvat[:20]:
        print(" -", n)
    if len(puuttuvat) > 20:
        print(f"... ja {len(puuttuvat)-20} muuta")

m = folium.Map(location=[64.5, 26.0], zoom_start=5)

folium.GeoJson(
    gdf[["geometry"]],
    name="Kuntarajat"
).add_to(m)

points = gdf.geometry.representative_point()

# Lisää markkerit
for (_, row), pt in zip(gdf.iterrows(), points):
    kunta = str(row[name_col])
    ala = row["Pinta_ala_km2"]
    vakiluku = row.get("Väkiluku")
    vak_txt = f"{int(vakiluku):,}".replace(",", " ") if pd.notna(vakiluku) else "–"

    popup = folium.Popup(
        f"<b>{kunta}</b><br>Pinta-ala: {ala:.1f} km²<br>Väkiluku: {vak_txt}",
        max_width=320
    )
    folium.Marker(
        location=[pt.y, pt.x],
        popup=popup,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

folium.LayerControl().add_to(m)
m.save(OUTPUT)
print(f"OK → {OUTPUT}")
