import pandas as pd
import geopandas as gpd
import streamlit as st

def transform_data(
    se_shp,
    dim_municipio_chropleth,
    atividades_temas_pse,
    parti_temas_pse,
    praticas_saude_pse,
    parti_praticas_saude_pse,
    escolas,
):
    # Preprocessar e combinar os dados
    se_shp["CD_MUN"] = se_shp["CD_MUN"].astype(str)

    dim_municipio_chropleth["id_municipio_ibge"] = dim_municipio_chropleth[
        "id_municipio_ibge"
    ].astype(str)
    se_shp = se_shp.merge(
        dim_municipio_chropleth[["id_municipio_ibge", "ds_regiao_saude"]],
        left_on="CD_MUN",
        right_on="id_municipio_ibge",
    )

    se_shp["id_municipio_ibge"] = se_shp["id_municipio_ibge"].apply(
        lambda x: str(x)[:6]
    )

    # Ajustar tipos de dados para evitar conflitos ao fazer merge
    atividades_temas_pse["Ibge"] = atividades_temas_pse["Ibge"].astype(str)
    parti_temas_pse["Ibge"] = parti_temas_pse["Ibge"].astype(str)
    praticas_saude_pse["Ibge"] = praticas_saude_pse["Ibge"].astype(str)
    parti_praticas_saude_pse["Ibge"] = parti_praticas_saude_pse["Ibge"].astype(str)
   
    nova_colunas_parti_temas_pse = [
        (
            f"Participantes: {col}"
            if col not in ["Uf", "Ibge", "Municipio", "INEP (Escolas/Creche)"]
            else col
        )
        for col in parti_temas_pse.columns
    ]
    parti_temas_pse.columns = nova_colunas_parti_temas_pse

    nova_colunas_parti_praticas_saude_pse = [
        (
            f"Participantes: {col}"
            if col not in ["Uf", "Ibge", "Municipio", "INEP (Escolas/Creche)"]
            else col
        )
        for col in parti_praticas_saude_pse.columns
    ]

    parti_praticas_saude_pse.columns = nova_colunas_parti_praticas_saude_pse
    
    # Agrupando os dados
    grouped_atividades_praticas_com_inep = (
        praticas_saude_pse.groupby(["Ibge", "Municipio", "INEP (Escolas/Creche)"])[
            praticas_saude_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    grouped_parti_praticas_pse_com_inep = (
        parti_praticas_saude_pse.groupby(
            ["Ibge", "Municipio", "INEP (Escolas/Creche)"]
        )[parti_praticas_saude_pse.iloc[:, 4:-1].columns]
        .sum()
        .reset_index()
    )

    pse_praticas_com_inep = grouped_atividades_praticas_com_inep.merge(
        grouped_parti_praticas_pse_com_inep, how="outer"
    )

    # Agrupando os dados
    grouped_atividades_temas_com_inep = (
        atividades_temas_pse.groupby(["Ibge", "Municipio", "INEP (Escolas/Creche)"])[
            atividades_temas_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )
    grouped_parti_temas_pse_com_inep = (
        parti_temas_pse.groupby(["Ibge", "Municipio", "INEP (Escolas/Creche)"])[
            parti_temas_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    pse_temas_com_inep = grouped_atividades_temas_com_inep.merge(
        grouped_parti_temas_pse_com_inep, how="outer"
    )

    grouped_atividades_praticas_com_inep = (
        praticas_saude_pse.groupby(["Ibge", "Municipio", "INEP (Escolas/Creche)"])[
            praticas_saude_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    grouped_parti_praticas_pse_com_inep = (
        parti_praticas_saude_pse.groupby(
            ["Ibge", "Municipio", "INEP (Escolas/Creche)"]
        )[parti_praticas_saude_pse.iloc[:, 4:-1].columns]
        .sum()
        .reset_index()
    )

    pse_praticas_com_inep = grouped_atividades_praticas_com_inep.merge(
        grouped_parti_praticas_pse_com_inep, how="outer"
    )

    pse_temas_praticas_com_inep = pd.merge(
        pse_temas_com_inep,
        pse_praticas_com_inep.drop(columns=["Ibge", "Municipio"]),
        left_on="INEP (Escolas/Creche)",
        right_on="INEP (Escolas/Creche)",
        how="left",
    ).drop(columns="Ibge")
    pse_temas_praticas_com_inep["INEP (Escolas/Creche)"] = (
        pse_temas_praticas_com_inep["INEP (Escolas/Creche)"].astype(int).astype(str)
    )
    pse_temas_praticas_com_inep["Municipio"] = pse_temas_praticas_com_inep[
        "Municipio"
    ].str.title()

    escolas["Código INEP"] = escolas["Código INEP"].astype(int).astype(str)
    escolas["Escola"] = escolas["Escola"].str.title()
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep.merge(
        escolas[["Código INEP", "Escola"]],
        left_on="INEP (Escolas/Creche)",
        right_on="Código INEP",
        how='left'
    ).drop(columns=["Código INEP"])


    col_escola = pse_temas_praticas_com_inep.pop("Escola")
    pse_temas_praticas_com_inep.insert(2, col_escola.name, col_escola)

    # Agrupando os dados
    grouped_atividades_temas = (
        atividades_temas_pse.groupby(["Ibge", "Municipio"])[
            atividades_temas_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )
    grouped_parti_temas_pse = (
        parti_temas_pse.groupby(["Ibge", "Municipio"])[
            parti_temas_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    # Agrupando os dados
    grouped_atividades_praticas = (
        praticas_saude_pse.groupby(["Ibge", "Municipio"])[
            praticas_saude_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    grouped_parti_praticas_pse = (
        parti_praticas_saude_pse.groupby(["Ibge", "Municipio"])[
            parti_praticas_saude_pse.iloc[:, 4:-1].columns
        ]
        .sum()
        .reset_index()
    )

    pse_praticas = grouped_atividades_praticas.merge(
        grouped_parti_praticas_pse, how="outer"
    )

    pse_temas = grouped_atividades_temas.merge(grouped_parti_temas_pse, how="outer")
    # Ajustar tipo de dado para evitar conflitos ao fazer merge
    pse_temas["Ibge"] = pse_temas["Ibge"].astype(str).apply(lambda x: str(x)[:6])
    pse_praticas["Ibge"] = pse_praticas["Ibge"].astype(str).apply(lambda x: str(x)[:6])
    se_shp["id_municipio_ibge"] = se_shp["id_municipio_ibge"].apply(
        lambda x: str(x)[:6]
    )

    pse_temas = pd.merge(
        se_shp[["geometry", "geoid", "id_municipio_ibge", "NM_MUN", "ds_regiao_saude"]],
        pse_temas.drop(columns=["Municipio"]),
        right_on="Ibge",
        left_on="id_municipio_ibge",
        how="left",
    ).drop(columns=["Ibge"])

    pse_temas_praticas = pd.merge(
        pse_temas,
        pse_praticas.drop(columns=["Municipio"]),
        left_on="id_municipio_ibge",
        right_on="Ibge",
        how="left",
    ).drop(columns=["Ibge"])

    pse_temas_praticas.rename(
        columns={
            "ds_regiao_saude": "Região de Saúde",
            "NM_MUN": "Municipio",
            "id_municipio_ibge": "Ibge",
        },
        inplace=True,
    )
    
    pse_temas_praticas["Municipio"] = pse_temas_praticas["Municipio"].str.title()

    # Filtrando colunas indesejadas
    pse_temas_praticas = pse_temas_praticas[
        [col for col in pse_temas_praticas.columns if "Unnamed" not in col]
    ]

    col_name_agravos = pse_temas_praticas.columns[
        pse_temas_praticas.columns.str.startswith("Agravos")
    ][0]
    col_index_agravos = pse_temas_praticas.columns.get_loc(col_name_agravos)

    col_name_parti_sema_saude = pse_temas_praticas.columns[
        pse_temas_praticas.columns.str.startswith(
            "Participantes: Semana saúde na escola"
        )
    ][0]
    col_index_parti_sema_saude = pse_temas_praticas.columns.get_loc(
        col_name_parti_sema_saude
    )

    col_name_sit_vac = pse_temas_praticas.columns[
        pse_temas_praticas.columns.str.startswith("Participantes: Verificação da sit")
    ][0]
    col_index_sit_vac = pse_temas_praticas.columns.get_loc(col_name_sit_vac)

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Autocuidado de pessoas com doenças crônicas"
            if x.startswith("Autocuidado")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Ações de combate ao Aedes aegypti"
            if x.startswith("Ações de combate ao")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Dependência Química / Tabaco / Álcool / Outras Drogas"
            if x.startswith("Depen")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Plantas medicinais / fitoterapia" if x.startswith("Plantas") else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Envelhecimento / Climatério / Andropausa / Etc."
            if x.startswith("Envelhe")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Prevenção da violência e promoção da cultura de paz"
            if x.startswith("Prevenção da vio")
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Autocuidado de pessoas com doenças crônicas"
            if "Participantes:" in x and "Autocuidado" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Ações de combate ao Aedes aegypti"
            if "Participantes:" in x and "Ações de combate ao" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Dependência Química / Tabaco / Álcool / Outras Drogas"
            if "Participantes:" in x and "Depen" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Plantas medicinais / fitoterapia"
            if "Participantes:" in x and "Plantas" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Envelhecimento / Climatério / Andropausa / Etc."
            if "Participantes:" in x and "Envelhe" in x
            else x
        ),
        inplace=True,
    )

    pse_temas_praticas.rename(
        columns=lambda x: (
            "Participantes: Prevenção da violência e promoção da cultura de paz"
            if "Participantes:" in x and "vio" in x
            else x
        ),
        inplace=True,
    )
    
    colunas_agg = pse_temas_praticas.columns[col_index_agravos:]

    pse_temas_praticas[colunas_agg] = pse_temas_praticas[colunas_agg].fillna(0)

    pse_temas_praticas_group = (
        pse_temas_praticas.groupby(
            ["Região de Saúde", "Ibge", "Municipio", "geometry"], dropna=False
        )[colunas_agg]
        .sum()
        .reset_index()
    )

    pse_temas_praticas_group[colunas_agg].fillna(0, inplace=True)

    pse_temas_praticas_group.columns = [
        (
            f"T. {col}"
            if i in range(col_index_agravos - 1, col_index_parti_sema_saude)
            else col
        )
        for i, col in enumerate(pse_temas_praticas_group.columns)
    ]
    pse_temas_praticas_group.columns = [
        (
            f"P. {col}"
            if i in range(col_index_parti_sema_saude, col_index_sit_vac)
            else col
        )
        for i, col in enumerate(pse_temas_praticas_group.columns)
    ]
    pse_temas_praticas_group.columns = pse_temas_praticas_group.columns.str.replace('Escovação dental supervisionad', 'Escovação dental supervisionada')
    pse_temas_praticas_com_inep.columns = pse_temas_praticas_com_inep.columns.str.replace('Escovação dental supervisionad', 'Escovação dental supervisionada')  
    
    colunas_agg = pse_temas_praticas_group.columns[col_index_agravos - 1 :]
    gdf_pse_temas_praticas_group = gpd.GeoDataFrame(
        pse_temas_praticas_group, geometry="geometry"
    )
    pse_temas_praticas_com_inep = pse_temas_praticas_com_inep.merge(
        pse_temas_praticas[["Municipio", "Região de Saúde"]],
        left_on="Municipio",
        right_on="Municipio",
    )
    col_regiao_saude = pse_temas_praticas_com_inep.pop("Região de Saúde")
    pse_temas_praticas_com_inep.insert(0, col_regiao_saude.name, col_regiao_saude)
    
    new_column_names = gdf_pse_temas_praticas_group.columns[4:]
    pse_temas_praticas_com_inep['Escola'].fillna("Não Encontrada", inplace=True)
    pse_temas_praticas_com_inep.columns = list(
        pse_temas_praticas_com_inep.columns[:4]
    ) + list(
        new_column_names
    )  # Mantendo as duas primeiras colunas e renomeando as restantes

    gdf_pse_temas_praticas_group      
    return gdf_pse_temas_praticas_group, colunas_agg, pse_temas_praticas_com_inep
