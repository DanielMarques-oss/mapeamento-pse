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
    atividades_temas_pse = pd.read_csv(
        "data/RelAtvColetivaMB.csv", skiprows=9, encoding="ISO-8859-1", sep=";", thousands='.'
    ).iloc[:-2]
    parti_temas_pse = pd.read_csv(
        "data/RelPartiAtvColetivaMB.csv", skiprows=9, encoding="ISO-8859-1", sep=";", thousands='.'
    ).iloc[:-2]
    praticas_saude_pse = pd.read_csv(
        "data/RelPratSaude.csv", skiprows=9, encoding="ISO-8859-1", sep=";", thousands='.'
    ).iloc[:-2]

    parti_praticas_saude_pse = pd.read_csv(
        "data/RelPartiPratSaude.csv", skiprows=9, encoding="ISO-8859-1", sep=";", thousands='.'
    ).iloc[:-2]

    escolas = pd.read_csv("data/escolas.csv", sep=";").iloc[:-2]

    return (
        se_shp,
        dim_municipio_chropleth,
        atividades_temas_pse,
        parti_temas_pse,
        praticas_saude_pse,
        parti_praticas_saude_pse,
        escolas,
    )
