# Harjoitustyö3 - Paikkatiedon käsittely #
#### Oskar Kotala, Heikki Lähdesmäki ####


#### Johdanto ####

Tämä on harjoitustyö, jossa käytimme Geopandas- ja Folium-kirjastoja paikkatiedon käsittelyyn. Tavoitteena oli hakea Suomen kuntarajat, laskea niiden pinta-alat, yhdistää väkilukudata kuntiin ja esittää tulokset kartalla.
Työn lopputuloksena syntyi ohjelma, joka tuottaa HTML-muotoisen kartan, jossa näkyy kuntarajat ja tietoa kunnista (pinta-ala ja väkiluku) klikatessa.



#### Sisältö ja rakenne ####

Projektissa on neljä tiedostoa:

1. main.py — pääohjelma, joka tekee datan käsittelyn ja tuottaa kartan.
2. kuntarajat-2018-raw.geojson — kuntarajat paikkatietomuodossa.
3. vakiluku.csv — taulukko, jossa on kuntien väkiluvut.
4. suomen_kunnat.html — ohjelman tuottama kartta.

Ohjelma lukee kuntarajat GeoJSON-tiedostosta ja väkiluvut CSV:stä. Se laskee jokaiselle kunnalle pinta-alan (km2), yhdistää väkiluvun samaan taulukkoon ja piirtää ne kartalle.


#### Miten ohjelma toimii ####

1. Datan lukeminen: GeoPandas lukee GeoJSON-tiedoston, josta saadaan kuntien rajat ja nimet. CSV-tiedostosta luetaan väkiluvut Pandasilla.

2. Nimien yhdistäminen: Koska kuntien nimet voivat erota eri aineistoissa esim ääkköset jotka aiheuttivat paljon harmia, ne normalisoidaan pienaakkosiksi ja skandit korvataan.

3. Pinta-alan laskenta: Koordinaatisto muunnetaan ensin metriyksikköön, jotta pinta-alat voidaan laskea neliömetreinä. Tulos muutetaan neliökilometreiksi.

4. Datan yhdistäminen: Väkilukudata liitetään kuntarajoihin yhdistämällä nimet.

5. Kartta: Foliumilla piirretään Suomen kartta, johon lisätään kuntarajat ja markkerit kuntien keskikohtiin. Markkerin popup näyttää kunnan nimen, pinta-alan ja väkiluvun.


#### Lopputulos ####

Lopputuloksena on HTML-kartta (suomen_kunnat.html), jota voi tarkastella selaimessa. Karttaa voi zoomata ja klikata kuntia. Popup-ikkunassa näkyy:

- Kunnan nimi
- Pinta-ala (km2)
- Väkiluku


#### Käytetyt kirjastot ja työkalut ####

- GeoPandas
- Pandas
- Folium
- Matplotlib