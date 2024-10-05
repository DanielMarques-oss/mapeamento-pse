import streamlit as st
from data_loader import load_data
from data_transformer import transform_data
from map_renderer import render_map
import os
from datetime import datetime


st.set_page_config(page_title="Análise de Atividades PSE", layout="wide")

# Carregar dados
se_shp, dim_municipio_chropleth, atividades_pse_jan_ago2024, parti_pse_jan_ago2024 = load_data()

# Transformar dados
gdf_pse_group, colunas_agg, col_index_agravos = transform_data(
    se_shp, dim_municipio_chropleth, atividades_pse_jan_ago2024, parti_pse_jan_ago2024
)

# Sidebar para filtros

colunas_disponiveis = list(colunas_agg)

filtro_opcoes = st.sidebar.selectbox("Escolha o nível de filtro:", ["Sergipe", "Região de Saúde"], index=0)

if filtro_opcoes == "Região de Saúde":
    regioes = gdf_pse_group["Região de Saúde"].unique()

    regiao_selecionada = st.sidebar.selectbox("Selecione a Região de Saúde", options=regioes)
    
    # Filtrar dados pela região de saúde
    gdf_pse_group = gdf_pse_group[gdf_pse_group['Região de Saúde'] == regiao_selecionada]

coluna_selecionada = st.sidebar.selectbox("Selecione o tema para saúde", options=colunas_disponiveis)


# Obtendo a última data de atualização do arquivo
modification_time = os.path.getmtime(r"data/RelAtvColetivaMB.csv")

# Convertendo o timestamp para um objeto datetime
modification_time = datetime.fromtimestamp(modification_time)

# Formatando a data no formato brasileiro (DD/MM/AAAA)
formatted_date = modification_time.strftime("%d/%m/%Y")

st.markdown("## Heatmap das atividades do Programa Saúde na Escola (SE), 2024")
st.write("")
# Renderizar o mapa com os filtros aplicados
render_map(gdf_pse_group, coluna_selecionada)

st.write("Data da última atualização:", formatted_date)
