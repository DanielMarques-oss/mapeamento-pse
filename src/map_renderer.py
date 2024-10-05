import plotly.express as px
import streamlit as st

def render_map(gdf_pse_group, coluna_selecionada):
    zmax = max(gdf_pse_group[coluna_selecionada])
    total = gdf_pse_group[coluna_selecionada].sum(skipna=True)
    
    gdf_pse_group.index = gdf_pse_group['Municipio']

    fig = px.choropleth_mapbox(
        gdf_pse_group,
        width=1200,
        height=800,
        geojson=gdf_pse_group.geometry,
        locations=gdf_pse_group.index,
        color=coluna_selecionada,
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map",
        center={"lat": -10.626485623243966, "lon": -37.072524582987405},
        zoom=7,
        opacity=0.7,
        range_color=[0, zmax],
        labels={coluna_selecionada: coluna_selecionada,
                "index": "Municipio"}
    )

    fig.add_annotation(
        text=f"<em>Total: {total:,.0f}</em>".replace(",", "."),
        x=0.92, y=0.88,
        bordercolor="#27544B",
        borderwidth=2,
        borderpad=4,
        bgcolor="black",
        showarrow=False,
        font=dict(size=26, color="white")
    )

    fig.update_layout(
        title={'text': coluna_selecionada.replace("Parti. de", "Participantes -"), 'y': 0.98, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
        title_font_size=28,
        coloraxis_colorbar=dict(title="")
    )

    fig.update_traces(hoverlabel=dict(
        font=dict(
            size=22,  # Tamanho da fonte do tooltip
            color="white"  # Cor da fonte (opcional)
        )
    ))

    st.plotly_chart(fig)
