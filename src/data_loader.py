import pandas as pd
import geopandas as gpd
import streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    """
    Carrega e processa diversos conjuntos de dados geoespaciais e CSV para uso em um dashboard Streamlit.
    
    Returns:
        - se_shp (GeoDataFrame): Shapefile dos municípios do SE do Brasil, com CRS definido como EPSG:4326.
        - dim_municipio (DataFrame): Dados municipais lidos de um arquivo CSV.
        - atividades_temas_pse (DataFrame): Relatório de atividades coletivas PSE, lido e filtrado de um CSV.
        - parti_temas_pse (DataFrame): Relatório de participação em atividades coletivas PSE, lido e filtrado de um CSV.
        - praticas_saude_pse (DataFrame): Relatório de práticas de saúde PSE, lido e filtrado de um CSV.
        - parti_praticas_saude_pse (DataFrame): Relatório de participação em práticas de saúde PSE, lido e filtrado de um CSV.
        - escolas (DataFrame): Dados de escolas, lidos de um arquivo CSV.
    """

    # Carrega o shapefile de municípios da região Sudeste do Brasil e define o sistema de referência de coordenadas (CRS)
    se_shp = gpd.read_file(r"data/SE_Municipios_2022.shp").set_crs("epsg:4326")
    
    # Adiciona uma nova coluna 'geoid' convertendo os índices para string
    se_shp["geoid"] = se_shp.index.astype(str)
    
    # Converte a coluna 'CD_MUN' (código do município) para string
    se_shp["CD_MUN"] = se_shp["CD_MUN"].astype(str)

    # Carrega dados municipais de um arquivo CSV, garantindo que o campo 'id_municipio_ibge' seja lido como string
    dim_municipio_chropleth = pd.read_csv(r"data/dimMunicipio.csv", dtype={'id_municipio_ibge': str})

    # Carrega e filtra o relatório de atividades coletivas PSE, removendo as últimas duas linhas e excluindo a primeira coluna
    atividades_temas_pse = pd.read_csv(
        "data/RelAtvColetivaMB.csv", 
        skiprows=9,  # Ignora as primeiras 9 linhas
        encoding="ISO-8859-1",  # Define a codificação correta do arquivo
        sep=";",  # Delimitador de colunas
        thousands='.',  # Identifica o separador de milhares
        dtype={'Ibge': str, "INEP (Escolas/Creche)": str},  # Define colunas específicas como string
    ).iloc[:-2, 1:]  # Remove as últimas duas linhas e a primeira coluna

    # Carrega e filtra o relatório de participação em atividades coletivas PSE
    parti_temas_pse = pd.read_csv(
        "data/RelPartiAtvColetivaMB.csv", 
        skiprows=9,
        encoding="ISO-8859-1",
        sep=";", 
        thousands='.',
        dtype={'Ibge': str, "INEP (Escolas/Creche)": str}
    ).iloc[:-2, 1:]

    # Carrega e filtra o relatório de práticas de saúde PSE
    praticas_saude_pse = pd.read_csv(
        "data/RelPratSaude.csv", 
        skiprows=9,
        encoding="ISO-8859-1", 
        sep=";", 
        thousands='.',
        dtype={'Ibge': str, "INEP (Escolas/Creche)": str}
    ).iloc[:-2, 1:]

    # Carrega e filtra o relatório de participação em práticas de saúde PSE
    parti_praticas_saude_pse = pd.read_csv(
        "data/RelPartiPratSaude.csv", 
        skiprows=9,
        encoding="ISO-8859-1", 
        sep=";", 
        thousands='.',
        dtype={'Ibge': str, "INEP (Escolas/Creche)": str}
    ).iloc[:-2, 1:]

    # Carrega o arquivo CSV contendo dados das escolas, garantindo que o campo 'Código INEP' seja lido como string
    escolas = pd.read_csv("data/escolas.csv", sep=";", dtype={"Código INEP": str})

    # Retorna todos os DataFrames carregados e processados
    return (
        se_shp,
        dim_municipio_chropleth,
        atividades_temas_pse,
        parti_temas_pse,
        praticas_saude_pse,
        parti_praticas_saude_pse,
        escolas,
    )
