import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from funcoes import print_infos, renomear, outros, rm_outliers

df = pd.read_csv("ecommerce_estatistica.csv")

print_infos()


# Mudando estilo de gráficos
sns.set_style("darkgrid")
sns.set_palette("pastel")

# Mapa de calor - Correlação entre variáveis
df_corr = df[
    [
        "Nota_MinMax",
        "N_Avaliações_MinMax",
        "Desconto_MinMax",
        "Preço_MinMax",
        "Marca_Cod",
        "Material_Cod",
        "Temporada_Cod",
        "Qtd_Vendidos_Cod",
        "Marca_Freq",
        "Material_Freq",
    ]
].corr()

plt.figure(figsize=(12, 12))
sns.heatmap(df_corr, annot=True, fmt=".2f")
plt.title("Mapa de Calor - Correlação entre Variáveis")
plt.xticks(rotation=-28)
plt.tight_layout()
plt.show()


# Gráfico de pizza - Distribuição da Categoria Temporada
maiores = outros(df)

plt.figure(figsize=(8, 6))
plt.pie(maiores, labels=maiores.index, autopct="%1.1f%%", startangle=90)
plt.title("Pizza - Distribuição da Categoria Temporada")
plt.show()


# Gráfico de densidade - Distribuição de Notas
plt.figure(figsize=(10, 6))
sns.kdeplot(df["Nota"], fill=True, color="#863e9c")
plt.title("Densidade - Distribuição de Notas")
plt.xlabel("Nota")
plt.ylabel("Densidade")
plt.show()


# Gráfico de Histograma - Distribuição de Preços
fig = px.histogram(
    data_frame=df,
    x="Preço",
    title="Histograma - Distribuição de Preços",
    nbins=50,
    color_discrete_sequence=["#99b595"],
    facet_col_spacing=0.1,
)
fig.show()


# Gráfico de dispersão - Notas x N Avaliações
fig = px.scatter(
    data_frame=df,
    x="Nota",
    y="N_Avaliações",
    labels={"Nota": "Notas", "N_Avaliações": "Número de Avaliações"},
    title="Gráfico de Dispersão - Notas x N° Avaliações",
    size="N_Avaliações",
    size_max=50,
    opacity=0.8,
)
fig.show()


# Gráfico de barra - Gênero
dados_genero = renomear(df)

fig = px.bar(
    data_frame=dados_genero,
    x=dados_genero.index,
    y=dados_genero.values,
    labels={"x": "Gênero", "y": "Quantidade"},
    title='Barras - Distribuição da Categoria "Gênero"',
    color=dados_genero.index,
    color_discrete_sequence=px.colors.qualitative.Set3,
)
fig.show()


# Grafico de Regressão - N_Avaliações x Qtd_Vendidos_Cod
df_rm_outliers = rm_outliers(df)

fig = px.scatter(
    data_frame=df_rm_outliers,
    x="N_Avaliações",
    y="Qtd_Vendidos_Cod",
    size="N_Avaliações",
    labels={
        "N_Avaliações": "Número de Avaliações",
        "Qtd_Vendidos_Cod": "Quantidade Vendida",
    },
    title="Regressão - Número de Avaliações x Quantidade Vendida",
    trendline="ols",
    trendline_color_override="#eb8c00"
)
fig.show()
