import pandas as pd
import geopandas as gpd
import streamlit as st

def transform_data(
    se_shp,
    dim_municipio,
    atividades_temas_pse,
    parti_temas_pse,
    praticas_saude_pse,
    parti_praticas_saude_pse,
    escolas,
):
    """
    Função para transformar e combinar vários datasets relacionados às atividades 
    coletivas de saúde e escolas com informações geográficas.

    Parameters:
        se_shp (GeoDataFrame): Shapefile dos municípios.
        dim_municipio (DataFrame): Dimensão de municípios, contendo ID e região de saúde.
        atividades_temas_pse (DataFrame): Atividades relacionadas a temas de saúde do PSE.
        parti_temas_pse (DataFrame): Participação em atividades relacionadas a temas de saúde do PSE.
        praticas_saude_pse (DataFrame): Práticas de saúde do PSE.
        parti_praticas_saude_pse (DataFrame): Participação em práticas de saúde do PSE.
        escolas (DataFrame): Informações sobre as escolas.

    Returns:
        tuple: 
            - GeoDataFrame com os dados agregados e combinados geograficamente.
            - Lista com as colunas que representam os agregados de dados.
            - DataFrame com os dados combinados sem a geometria.
    """

    # Combinar shapefile com a tabela de municípios e regiões de saúde
    se_shp = se_shp.merge(
        dim_municipio[["id_municipio_ibge", "ds_regiao_saude"]],
        left_on="CD_MUN",
        right_on="id_municipio_ibge",
    )

    # Aplicar formatação de 6 dígitos ao ID do município
    se_shp["id_municipio_ibge"] = se_shp["id_municipio_ibge"].apply(
        lambda x: str(x)[:6]
    )
   
    # Renomear as colunas de participação em temas do PSE
    nova_colunas_parti_temas_pse = [
        (
            f"Participantes: {col}"
            if col not in ["Uf", "Ibge", "Municipio", "INEP (Escolas/Creche)"]
            else col
        )
        for col in parti_temas_pse.columns
    ]
    parti_temas_pse.columns = nova_colunas_parti_temas_pse

    # Renomear as colunas de participação em práticas de saúde do PSE
    nova_colunas_parti_praticas_saude_pse = [
        (
            f"Participantes: {col}"
            if col not in ["Uf", "Ibge", "Municipio", "INEP (Escolas/Creche)"]
            else col
        )
        for col in parti_praticas_saude_pse.columns
    ]

    parti_praticas_saude_pse.columns = nova_colunas_parti_praticas_saude_pse
    
    # Combinar práticas de saúde com participação nas práticas (usando INEP como chave)
    praticas_e_parti_saude_pse_com_inep = praticas_saude_pse.drop(columns=["Ibge", "Municipio"]).merge(
        parti_praticas_saude_pse, how="outer", left_on="INEP (Escolas/Creche)", right_on="INEP (Escolas/Creche)"
    )

    # Combinar atividades com participação em temas do PSE (usando INEP como chave)
    atividades_e_parti_temas_pse_com_inep = atividades_temas_pse.merge(
        parti_temas_pse.drop(columns=["Ibge", "Municipio"]), how="outer", left_on="INEP (Escolas/Creche)", right_on="INEP (Escolas/Creche)"
    )
    
    # Combinar todas as informações (atividades, práticas, participação) com INEP como chave
    pse_temas_praticas_com_inep = pd.merge(
        atividades_e_parti_temas_pse_com_inep,
        praticas_e_parti_saude_pse_com_inep.drop(columns=["Municipio", "Ibge"]),
        left_on="INEP (Escolas/Creche)",
        right_on="INEP (Escolas/Creche)",
        how="outer",
    )


    # Formatar o nome dos municípios em maiúscula inicial
    pse_temas_praticas_com_inep["Municipio"] = pse_temas_praticas_com_inep[
        "Municipio"
    ].str.title()

    # Formatar o nome das escolas
    escolas["Escola"] = escolas["Escola"].str.title()

    # Combinar as escolas com os dados do PSE e ajustar a posição da coluna "Escola"
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep.merge(
        escolas[["Código INEP", "Escola"]],
        left_on="INEP (Escolas/Creche)",
        right_on="Código INEP",
        how='left'
    ).drop(columns=["Código INEP"])
    
    col_escola = pse_temas_praticas_com_inep.pop("Escola")
    pse_temas_praticas_com_inep.insert(3, col_escola.name, col_escola)
    
    # Remover colunas "Unnamed" indesejadas
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep[
        [col for col in pse_temas_praticas_com_inep.columns if "Unnamed" not in col]
    ]

    # Renomear colunas específicas para melhor entendimento
    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Autocuidado de pessoas com doenças crônicas"
            if x.startswith("Autocuidado")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Ações de combate ao Aedes aegypti"
            if x.startswith("Ações de combate ao")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Dependência Química / Tabaco / Álcool / Outras Drogas"
            if x.startswith("Depen")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Plantas medicinais / fitoterapia" if x.startswith("Plantas") else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Envelhecimento / Climatério / Andropausa / Etc."
            if x.startswith("Envelhe")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Prevenção da violência e promoção da cultura de paz"
            if x.startswith("Prevenção da vio")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Autocuidado de pessoas com doenças crônicas"
            if "Participantes:" in x and "Autocuidado" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Ações de combate ao Aedes aegypti"
            if "Participantes:" in x and "Ações de combate ao" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Dependência Química / Tabaco / Álcool / Outras Drogas"
            if "Participantes:" in x and "Depen" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Plantas medicinais / fitoterapia"
            if "Participantes:" in x and "Plantas" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Envelhecimento / Climatério / Andropausa / Etc."
            if "Participantes:" in x and "Envelhe" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas_com_inep.rename(
        columns=lambda x: (
            "Participantes: Prevenção da violência e promoção da cultura de paz"
            if "Participantes:" in x and "vio" in x
            else x
        ),
        inplace=True,
    )
    
    pse_temas_praticas_com_inep.columns = pse_temas_praticas_com_inep.columns.str.replace('Escovação dental supervisionad', 'Escovação dental supervisionada')

    # Combinar dados geográficos (shapefile) com os dados processados do PSE
    pse_temas_praticas_com_inep = pd.merge(
        se_shp[["geometry", "geoid", "id_municipio_ibge", "ds_regiao_saude", "NM_MUN"]],
        pse_temas_praticas_com_inep.drop(columns=["Municipio"]),
        right_on="Ibge",
        left_on="id_municipio_ibge",
        how="left",
    ).drop(columns=["id_municipio_ibge", "Ibge"])
    

    # Renomear algumas colunas importantes para clareza
    pse_temas_praticas_com_inep.rename(
        columns={
            "ds_regiao_saude": "Região de Saúde",
            "NM_MUN": "Municipio",
            "id_municipio_ibge": "Ibge"
        },
        inplace=True,
    )
    
    # Atribuir prefixos às colunas para agrupar visualmente categorias semelhantes
    col_name_agravos = pse_temas_praticas_com_inep.columns[
        pse_temas_praticas_com_inep.columns.str.startswith("Agravos")
    ][0]
    
    col_index_agravos = pse_temas_praticas_com_inep.columns.get_loc(col_name_agravos)

    col_name_parti_sema_saude = pse_temas_praticas_com_inep.columns[
        pse_temas_praticas_com_inep.columns.str.startswith(
            "Participantes: Semana saúde na escola"
        )
    ][0]

    col_index_parti_sema_saude = pse_temas_praticas_com_inep.columns.get_loc(
        col_name_parti_sema_saude
    )

    col_name_sit_vac = pse_temas_praticas_com_inep.columns[
        pse_temas_praticas_com_inep.columns.str.startswith("Participantes: Verificação da sit")
    ][0]

    col_index_sit_vac = pse_temas_praticas_com_inep.columns.get_loc(col_name_sit_vac)
   
    pse_temas_praticas_com_inep.columns = [
        (
            f"T. {col}"
            if i in range(col_index_agravos, col_index_parti_sema_saude + 1)
            else col
        )
        for i, col in enumerate(pse_temas_praticas_com_inep.columns)
    ]
    pse_temas_praticas_com_inep.columns = [
        (
            f"P. {col}"
            if i in range(col_index_parti_sema_saude + 1, col_index_sit_vac + 1)
            else col
        )
        for i, col in enumerate(pse_temas_praticas_com_inep.columns)
    ]
    
    # Preencher valores NaN com zero nas colunas agregadas
    colunas_agg = pse_temas_praticas_com_inep.columns[col_index_agravos:]
    
    pse_temas_praticas_com_inep[colunas_agg] = pse_temas_praticas_com_inep[colunas_agg].fillna(0)

    # Preencher valores faltantes na coluna "Escola"
    pse_temas_praticas_com_inep['Escola'].fillna("Não Encontrada", inplace=True)

    # Agrupar os dados por região de saúde, município e geometria, somando os valores das colunas agregadas
    pse_temas_praticas_sem_inep_group = (
        pse_temas_praticas_com_inep.groupby(
            ["Região de Saúde", "Municipio", "geometry"], dropna=False
        )[colunas_agg]
        .sum()
        .reset_index()
    )

    # Preencher valores NaN com zero nas colunas agregadas
    pse_temas_praticas_sem_inep_group[colunas_agg].fillna(0, inplace=True)

    # Converter DataFrame para GeoDataFrame, mantendo a geometria
    gdf_pse_temas_praticas_sem_inep_group = gpd.GeoDataFrame(
        pse_temas_praticas_sem_inep_group, geometry="geometry"
    )
    
    return gdf_pse_temas_praticas_sem_inep_group, colunas_agg, pse_temas_praticas_com_inep.drop(columns=["geometry", "geoid"])
