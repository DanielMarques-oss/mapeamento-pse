import streamlit as st
from data_loader import load_data
from data_transformer import transform_data
from map_renderer import render_map
from dotenv import load_dotenv
import os
import csv


load_dotenv()
api_key = os.getenv("API_KEY")

st.set_page_config(
    page_title="Análise de Atividades PSE", layout="wide", page_icon="📖"
)

# Carregar dados
(
    se_shp,
    dim_municipio_chropleth,
    atividades_temas_pse,
    parti_temas_pse,
    praticas_saude_pse,
    parti_praticas_saude_pse,
    escolas,
) = load_data()

# Transformar dados
gdf_temas_praticas_pse_group, colunas_agg, pse_temas_praticas_com_inep = transform_data(
    se_shp,
    dim_municipio_chropleth,
    atividades_temas_pse,
    parti_temas_pse,
    praticas_saude_pse,
    parti_praticas_saude_pse,
    escolas,
)

# Sidebar para filtros

colunas_disponiveis = list(colunas_agg)




regioes = gdf_temas_praticas_pse_group["Região de Saúde"].unique()

regiao_selecionada = st.sidebar.selectbox(
    "Selecione a região de saúde:",
    ["Todas"] + list(regioes),
)

if regiao_selecionada != "Todas":

    # Filtrar dados pela região de saúde
    gdf_temas_praticas_pse_group = gdf_temas_praticas_pse_group[
        gdf_temas_praticas_pse_group["Região de Saúde"] == regiao_selecionada
    ]

    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Região de Saúde"] == regiao_selecionada
    ]

municipio_selecionado = st.sidebar.selectbox(
    "Selecione o município:",
    ["Todos"] + list(gdf_temas_praticas_pse_group["Municipio"].unique()),
)

if municipio_selecionado != "Todos":
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Municipio"] == municipio_selecionado
    ]
    gdf_temas_praticas_pse_group = gdf_temas_praticas_pse_group[
        gdf_temas_praticas_pse_group["Municipio"] == municipio_selecionado
    ]

escola_selecionada = st.sidebar.selectbox(
    "Selecione a Escola",
    options=["Todas"] + list(pse_temas_praticas_com_inep["Escola"].unique()),
)

if escola_selecionada != "Todas":

    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Escola"] == escola_selecionada
    ]


coluna_selecionada = st.sidebar.selectbox(
    "Tema (T) ou prática (P) para saúde", options=colunas_disponiveis
)

st.markdown("## Heatmap das atividades do Programa Saúde na Escola (SE), 2024")

# Renderizar o mapa com os filtros aplicados
render_map(gdf_temas_praticas_pse_group, coluna_selecionada)

st.markdown("### Tabela com temas e práticas por município")
st.write("*A vírgula está como separador de milhar e o ponto como separador decimal")
st.dataframe(gdf_temas_praticas_pse_group.drop(columns="geometry"), hide_index=True)
st.markdown("### Tabela com temas e práticas por escola")

st.dataframe(
    pse_temas_praticas_com_inep.sort_values(
        by=["Região de Saúde", "Municipio", "Escola"]
    ),
    hide_index=True,
)
with open("data/RelAtvColetivaMB.csv", newline="", encoding="ISO-8859-1") as csvfile:
    leitor_csv = csv.reader(csvfile, delimiter=",")

    # Ignora as duas primeiras linhas
    for i, linha in enumerate(leitor_csv):
        if i == 3:  # A terceira linha está no índice 2 (indexação começa em 0)
            st.write(linha[0])
            break  # Para o loop após imprimir a terceira linha
