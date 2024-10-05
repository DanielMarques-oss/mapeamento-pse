import pandas as pd
import geopandas as gpd
import streamlit as st

def transform_data(se_shp, dim_municipio_chropleth, atividades_pse2024, parti_pse):
    # Preprocessar e combinar os dados
    se_shp['CD_MUN'] = se_shp['CD_MUN'].astype(str)

    
    dim_municipio_chropleth['id_municipio_ibge'] = dim_municipio_chropleth['id_municipio_ibge'].astype(str)
    se_shp = se_shp.merge(dim_municipio_chropleth[['id_municipio_ibge', 'ds_regiao_saude']],
                          left_on='CD_MUN', right_on='id_municipio_ibge')

    se_shp['id_municipio_ibge'] = se_shp['id_municipio_ibge'].apply(lambda x: str(x)[:6])

    # Ajustar tipos de dados para evitar conflitos ao fazer merge
    atividades_pse2024['Ibge'] = atividades_pse2024['Ibge'].astype(str)
    parti_pse['Ibge'] = parti_pse['Ibge'].astype(str)
    
    nova_colunas_parti = [f"Participantes: {col}" if col not in ['Uf', 'Ibge', 'Municipio'] else col for col in parti_pse.columns]
    parti_pse.columns = nova_colunas_parti

    # Agrupando os dados
    grouped_atividades = atividades_pse2024.groupby(['Ibge', 'Municipio'])[atividades_pse2024.iloc[:, 4:-1].columns].sum().reset_index()
    grouped_parti = parti_pse.groupby(['Ibge', 'Municipio'])[parti_pse.iloc[:, 4:-1].columns].sum().reset_index()

    pse = grouped_atividades.merge(grouped_parti, how='inner')
    
    # Ajustar tipo de dado para evitar conflitos ao fazer merge
    pse['Ibge'] = pse['Ibge'].astype(str).apply(lambda x: str(x)[:6])
    se_shp['id_municipio_ibge'] = se_shp['id_municipio_ibge'].apply(lambda x: str(x)[:6])

    pse = pd.merge(pse, se_shp[['geometry', 'geoid', 'id_municipio_ibge', 'ds_regiao_saude']],
                               left_on='Ibge', right_on='id_municipio_ibge', how='left')

    pse.rename(columns={'ds_regiao_saude': 'Região de Saúde'}, inplace=True)

    pse['Municipio'] = pse['Municipio'].str.title()

    # Filtrando colunas indesejadas
    pse = pse[[col for col in pse.columns if 'Unnamed' not in col]]

    col_name_agravos = pse.columns[pse.columns.str.startswith("Agravos")][0]
    col_index_agravos = pse.columns.get_loc(col_name_agravos)

    col_name_part_semana = pse.columns[pse.columns.str.startswith("Participantes: Semana")][0]
    col_index_part_semana = pse.columns.get_loc(col_name_part_semana)
    
    pse.rename(columns=lambda x: "Autocuidado de pessoas com doenças crônicas" if x.startswith("Autocuidado") else x, inplace=True)

    pse.rename(columns=lambda x: "Ações de combate ao Aedes aegypti" if x.startswith("Ações de combate ao") else x, inplace=True)

    pse.rename(columns=lambda x: "Dependência Química / Tabaco / Álcool / Outras Drogas" if x.startswith("Depen") else x, inplace=True)

    pse.rename(columns=lambda x: "Plantas medicinais / fitoterapia" if x.startswith("Plantas") else x, inplace=True)

    pse.rename(columns=lambda x: "Envelhecimento / Climatério / Andropausa / Etc." if x.startswith("Envelhe") else x, inplace=True)

    pse.rename(columns=lambda x: "Prevenção da violência e promoção da cultura de paz" if x.startswith("Prevenção da vio") else x, inplace=True)

    ###
    
    pse.rename(columns=lambda x: "Participantes: Autocuidado de pessoas com doenças crônicas" if "Participantes:" in x and "Autocuidado" in x else x, inplace=True)

    pse.rename(columns=lambda x: "Participantes: Ações de combate ao Aedes aegypti" if "Participantes:" in x and "Ações de combate ao" in x else x, inplace=True)

    pse.rename(columns=lambda x: "Participantes: Dependência Química / Tabaco / Álcool / Outras Drogas" if "Participantes:" in x and "Depen" in x else x, inplace=True)

    pse.rename(columns=lambda x: "Participantes: Plantas medicinais / fitoterapia" if "Participantes:" in x and "Plantas" in x else x, inplace=True)

    pse.rename(columns=lambda x: "Participantes: Envelhecimento / Climatério / Andropausa / Etc." if "Participantes:" in x and "Envelhe" in x else x, inplace=True)

    pse.rename(columns=lambda x: "Participantes: Prevenção da violência e promoção da cultura de paz" if "Participantes:" in x and "vio" in x else x, inplace=True)
    

    
    colunas_agg = pse.columns[col_index_agravos:col_index_part_semana]
    
    
    pse_group = pse.groupby(["Região de Saúde", "Municipio", "geometry"])[colunas_agg].sum().reset_index()
    
    
    gdf_pse_group = gpd.GeoDataFrame(pse_group, geometry='geometry')
    
    return gdf_pse_group, colunas_agg, col_index_agravos
