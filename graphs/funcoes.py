import pandas as pd

df = pd.read_csv("ecommerce_estatistica.csv")


# Print informações importantes
def print_infos():
    pd.set_option("display.max_columns", None)
    print(df.head())
    print(f"\nInformações do DataFrame: {df.info()}")
    print(f"\nDescrição do DataFrame: {df.describe()}")
    print(f"\nValores únicos: {df.nunique()}")


# Renomear os indices
def renomear(df):
    x_genero = df["Gênero"].value_counts().index
    y_genero = df["Gênero"].value_counts().values
    dados_genero = pd.Series(y_genero, index=x_genero)

    # Renomeando os indices
    dados_genero = dados_genero.rename(
        index={
            "Sem gênero infantil": "Infantil Genérico",
            "roupa para gordinha pluss P ao 52": "Plus Size",
        }
    )
    return dados_genero


# Nova categoria: Outros
def outros(df):
    x_temp = df["Temporada"].value_counts().index
    y_temp = df["Temporada"].value_counts().values
    dados_temp = pd.Series(y_temp, index=x_temp)

    # Define o limite de 5% do total
    limite = 0.05 * dados_temp.sum()

    # Agrupa os valores menores que 5%
    maiores = dados_temp[dados_temp >= limite]
    menores = dados_temp[dados_temp < limite]

    # Adiciona a categoria 'Outros'
    if not menores.empty:
        maiores["Outros"] = menores.sum()

    return maiores


# Removendo outliers com IQR
def rm_outliers(df):
    Avalicoes_Q1 = df["N_Avaliações"].quantile(0.25)
    Avalicoes_Q3 = df["N_Avaliações"].quantile(0.75)
    Vendidos_Q1 = df["Qtd_Vendidos_Cod"].quantile(0.25)
    Vendidos_Q3 = df["Qtd_Vendidos_Cod"].quantile(0.75)

    IQR_Avalicoes = Avalicoes_Q3 - Avalicoes_Q1
    IQR_Vendidos = Vendidos_Q3 - Vendidos_Q1

    limite_alto_Avalicoes = Avalicoes_Q3 + 1.5 * IQR_Avalicoes

    limite_alto_Vendidos = Vendidos_Q3 + 1.5 * IQR_Vendidos

    df_rm_outliers = df[
        (df["N_Avaliações"] <= limite_alto_Avalicoes)
        & (df["Qtd_Vendidos_Cod"] <= limite_alto_Vendidos)
    ]

    return df_rm_outliers

