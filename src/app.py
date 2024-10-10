import pandas as pd
import streamlit as st
from data_loader import load_data
from data_transformer import transform_data
from map_renderer import render_map
import os
from datetime import datetime
import csv




st.set_page_config(page_title="Análise de Atividades PSE", layout="wide", page_icon="📖")

# Carregar dados
se_shp, dim_municipio_chropleth, atividades_pse_jan_ago2024, parti_pse_jan_ago2024 = (
    load_data()
)

# Transformar dados
gdf_pse_group, colunas_agg, col_index_agravos = transform_data(
    se_shp, dim_municipio_chropleth, atividades_pse_jan_ago2024, parti_pse_jan_ago2024
)

# Sidebar para filtros

colunas_disponiveis = list(colunas_agg)

filtro_opcoes = st.sidebar.selectbox(
    "Escolha o nível de filtro:", ["Sergipe", "Região de Saúde"], index=0
)

if filtro_opcoes == "Região de Saúde":
    regioes = gdf_pse_group["Região de Saúde"].unique()

    regiao_selecionada = st.sidebar.selectbox(
        "Selecione a Região de Saúde", options=regioes
    )

    # Filtrar dados pela região de saúde
    gdf_pse_group = gdf_pse_group[
        gdf_pse_group["Região de Saúde"] == regiao_selecionada
    ]

coluna_selecionada = st.sidebar.selectbox(
    "Selecione o tema para saúde", options=colunas_disponiveis
)

st.markdown("## Heatmap das atividades do Programa Saúde na Escola (SE), 2024")
st.write("")
# Renderizar o mapa com os filtros aplicados
render_map(gdf_pse_group, coluna_selecionada)

st.dataframe(gdf_pse_group.drop(columns="geometry"), hide_index=True)

with open('data/RelAtvColetivaMB.csv', newline='', encoding='ISO-8859-1') as csvfile:
    leitor_csv = csv.reader(csvfile, delimiter=',')
    
    # Ignora as duas primeiras linhas
    for i, linha in enumerate(leitor_csv):
        if i == 3:  # A terceira linha está no índice 2 (indexação começa em 0)
            st.write(linha[0])
            break  # Para o loop após imprimir a terceira linha

