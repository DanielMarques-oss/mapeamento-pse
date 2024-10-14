import plotly.express as px  # Biblioteca para visualizações interativas com Plotly Express
import streamlit as st  # Biblioteca para construção de aplicativos web interativos

# Função para renderizar o mapa coroplético interativo
def render_map(gdf_pse_group, coluna_selecionada):

    """
    Renderiza um mapa coroplético interativo utilizando dados geoespaciais e uma coluna selecionada.

    Parameters:
    gdf_pse_group (GeoDataFrame): DataFrame contendo os dados geoespaciais e a coluna selecionada para o mapa.
    coluna_selecionada (str): Nome da coluna que será usada para colorir o mapa.

    O mapa exibe a soma dos valores da coluna selecionada e permite a visualização
    dos municípios através de uma geometria com estilo de mapa aberto (OpenStreetMap).
    """

    # Definir o valor máximo da coluna selecionada (para a escala de cores do mapa)
    zmax = max(gdf_pse_group[coluna_selecionada])

    # Somar os valores da coluna selecionada, ignorando valores nulos
    total = gdf_pse_group[coluna_selecionada].sum(skipna=True)

    # Definir o índice do DataFrame como a coluna 'Municipio'
    gdf_pse_group.index = gdf_pse_group["Municipio"]

    # Criar o mapa coroplético usando o Plotly Express
    fig = px.choropleth_mapbox(
        gdf_pse_group,  # Dados geográficos e quantitativos
        width=1200,  # Largura do gráfico
        height=800,  # Altura do gráfico
        geojson=gdf_pse_group.geometry,  # Geometria (polígonos) dos municípios
        locations=gdf_pse_group.index,  # Localização dos dados (índice é o município)
        color=coluna_selecionada,  # Coluna usada para colorir o mapa
        color_continuous_scale="Viridis",  # Escala de cores contínua para melhorar a acessibilidade
        mapbox_style="open-street-map",  # Estilo do mapa de fundo (OpenStreetMap)
        center={"lat": -10.626485623243966, "lon": -37.072524582987405},  # Centro do mapa (latitude e longitude)
        zoom=7,  # Nível de zoom do mapa
        opacity=0.7,  # Opacidade das áreas coloridas
        range_color=[0, zmax],  # Intervalo de cores do mapa (de 0 ao valor máximo da coluna)
        labels={coluna_selecionada: coluna_selecionada, "index": "Municipio"},  # Rótulos do mapa
    )

    # Adicionar uma anotação no gráfico, exibindo o total dos valores da coluna selecionada
    fig.add_annotation(
        text=f"<em>Total: {total:,.0f}</em>".replace(",", "."),  # Texto da anotação com o total formatado
        x=0.92,  # Posição no eixo x da anotação (direita)
        y=0.88,  # Posição no eixo y da anotação (topo)
        bordercolor="#27544B",  # Cor da borda da anotação
        borderwidth=2,  # Largura da borda
        borderpad=4,  # Espaço interno da borda
        bgcolor="black",  # Cor de fundo da anotação
        showarrow=False,  # Desativa a seta na anotação
        font=dict(size=26, color="white"),  # Definições da fonte (tamanho e cor)
    )

    # Atualizar o layout do gráfico, incluindo o título
    fig.update_layout(
        title={
            "text": coluna_selecionada.replace("Parti. de", "Participantes -"),  # Texto do título (substitui parte do texto)
            "y": 0.98,  # Posição vertical do título
            "x": 0.5,  # Centraliza o título horizontalmente
            "xanchor": "center",  # Alinhamento horizontal do título
            "yanchor": "top",  # Alinhamento vertical do título
        },
        title_font_size=28,  # Tamanho da fonte do título
        coloraxis_colorbar=dict(title=""),  # Remove o título da barra de cores
    )

    # Atualizar o estilo dos rótulos que aparecem ao passar o mouse (tooltips)
    fig.update_traces(
        hoverlabel=dict(
            font=dict(
                size=22,  # Tamanho da fonte dos tooltips
                color="white",  # Cor da fonte dos tooltips (opcional)
            )
        )
    )

    # Exibir o gráfico no aplicativo Streamlit
    st.plotly_chart(fig)
