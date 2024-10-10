import pandas as pd
import geopandas as gpd
import streamlit as st


@st.cache_data(ttl=3600)
def load_data():
    # Carrega os arquivos de dados
    se_shp = gpd.read_file(r"data/SE_Municipios_2022.shp").set_crs("epsg:4326")
    se_shp["geoid"] = se_shp.index.astype(str)
    dim_municipio_chropleth = pd.read_csv(r"data/dimMunicipio.csv")

    # Carregar dados das atividades e participações
    atividades_pse = pd.read_csv(
        "data/RelAtvColetivaMB.csv", skiprows=9, encoding="ISO-8859-1", sep=";"
    ).iloc[:-2]
    parti_pse = pd.read_csv(
        "data/RelPartiAtvColetivaMB.csv", skiprows=9, encoding="ISO-8859-1", sep=";"
    ).iloc[:-2]

    return se_shp, dim_municipio_chropleth, atividades_pse, parti_pse
