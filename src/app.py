import streamlit as st  # Biblioteca para construção de aplicativos interativos
from data_loader import load_data  # Função para carregar dados de fontes externas
from data_transformer import transform_data  # Função para transformar e preparar dados
from map_renderer import render_map  # Função para renderizar o mapa interativo
import csv  # Biblioteca para manipulação de arquivos CSV

# Carrega variáveis de ambiente a partir do arquivo .env
# load_dotenv()

# Obtém o valor da chave da API a partir das variáveis de ambiente (desativado por enquanto)
# api_key = os.getenv("API_KEY")

# Configuração da página no Streamlit (título, layout e ícone)
st.set_page_config(
    page_title="Análise de Atividades PSE",  # Título da aba
    layout="wide",  # Layout com largura máxima
    page_icon="📖",  # Ícone da aba
)

# Carregar dados de diferentes fontes, como shapefile, dados de atividades e escolas
(
    se_shp,  # Dados geográficos dos municípios
    dim_municipio_chropleth,  # Dimensão de municípios para o mapa coroplético
    atividades_temas_pse,  # Dados sobre as atividades relacionadas a temas de saúde do PSE
    parti_temas_pse,  # Dados sobre a participação nas atividades do PSE
    praticas_saude_pse,  # Dados sobre as práticas de saúde do PSE
    parti_praticas_saude_pse,  # Dados sobre a participação nas práticas de saúde do PSE
    escolas,  # Dados sobre as escolas
) = load_data()

# Transformar os dados carregados para prepará-los para visualização e análise
gdf_temas_praticas_pse_group, colunas_agg, pse_temas_praticas_com_inep = transform_data(
    se_shp,  # Dados geográficos
    dim_municipio_chropleth,  # Dimensão de municípios para o mapa
    atividades_temas_pse,  # Atividades do PSE
    parti_temas_pse,  # Participação nas atividades do PSE
    praticas_saude_pse,  # Práticas de saúde do PSE
    parti_praticas_saude_pse,  # Participação nas práticas de saúde do PSE
    escolas,  # Dados das escolas
)

# Sidebar com filtros interativos para o usuário
colunas_disponiveis = list(colunas_agg)  # Colunas disponíveis para filtro

# Obter as diferentes regiões de saúde para filtro
regioes = gdf_temas_praticas_pse_group["Região de Saúde"].unique()

# Criar um seletor para escolher uma região de saúde na barra lateral
regiao_selecionada = st.sidebar.selectbox(
    "Selecione a região de saúde:",  # Título do seletor
    ["Todas"] + list(regioes),  # Opções: Todas ou uma lista das regiões de saúde
)

# Se uma região específica for selecionada, filtra os dados
if regiao_selecionada != "Todas":
    # Filtrar o GeoDataFrame com base na região selecionada
    gdf_temas_praticas_pse_group = gdf_temas_praticas_pse_group[
        gdf_temas_praticas_pse_group["Região de Saúde"] == regiao_selecionada
    ]
    # Filtrar os dados do PSE com base na região selecionada
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Região de Saúde"] == regiao_selecionada
    ]

# Criar um seletor para escolher um município na barra lateral
municipio_selecionado = st.sidebar.selectbox(
    "Selecione o município:",  # Título do seletor
    ["Todos"]
    + list(gdf_temas_praticas_pse_group["Municipio"].unique()),  # Lista de municípios
)

# Se um município específico for selecionado, filtra os dados
if municipio_selecionado != "Todos":
    # Filtrar os dados do PSE com base no município selecionado
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Municipio"] == municipio_selecionado
    ]
    # Filtrar o GeoDataFrame com base no município selecionado
    gdf_temas_praticas_pse_group = gdf_temas_praticas_pse_group[
        gdf_temas_praticas_pse_group["Municipio"] == municipio_selecionado
    ]

# Criar um seletor para escolher uma escola na barra lateral
escola_selecionada = st.sidebar.selectbox(
    "Selecione a Escola",  # Título do seletor
    options=["Todas"]
    + list(pse_temas_praticas_com_inep["Escola"].unique()),  # Lista de escolas
)

# Se uma escola específica for selecionada, filtra os dados
if escola_selecionada != "Todas":
    # Filtrar os dados do PSE com base na escola selecionada
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        pse_temas_praticas_com_inep["Escola"] == escola_selecionada
    ]

# Criar um seletor para escolher um tema ou prática de saúde na barra lateral
coluna_selecionada = st.sidebar.selectbox(
    "Tema (T) ou prática (P) para saúde",  # Título do seletor
    options=colunas_disponiveis,  # Lista de colunas de temas/práticas disponíveis
)

# Título da seção de análise do mapa
st.markdown("## Heatmap das atividades do Programa Saúde na Escola (SE), 2024")

# Renderizar o mapa interativo com base nos filtros selecionados
render_map(gdf_temas_praticas_pse_group, coluna_selecionada)

# Exibir uma tabela com temas e práticas agregados por município
st.markdown("### Tabela com temas e práticas por município")
st.write("*A vírgula está como separador de milhar e o ponto como separador decimal")
st.dataframe(gdf_temas_praticas_pse_group.drop(columns="geometry"), hide_index=True)

# Exibir uma tabela com temas e práticas por escola
st.markdown("### Tabela com temas e práticas por escola")
st.dataframe(
    pse_temas_praticas_com_inep.sort_values(
        by=["Região de Saúde", "Municipio", "Escola"]
    ),
    hide_index=True,  # Esconder o índice da tabela
)

# Abrir e ler um arquivo CSV, delimitado por vírgula, com encoding ISO-8859-1, para identificar as competências a que se referem os dados
with open("data/RelAtvColetivaMB.csv", newline="", encoding="ISO-8859-1") as csvfile:
    leitor_csv = csv.reader(csvfile, delimiter=",")  # Leitor de CSV

    # Ignorar as duas primeiras linhas e exibir a terceira linha, a das competências
    for i, linha in enumerate(leitor_csv):
        if i == 3:  # A terceira linha está no índice 2 (começa de 0)
            st.write(linha[0])  # Exibir a primeira célula da terceira linha
            break  # Interromper o loop após exibir a terceira linha
