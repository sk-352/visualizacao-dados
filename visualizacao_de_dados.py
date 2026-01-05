import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from funcoes import renomear, outros, rm_outliers

df = pd.read_csv("ecommerce_estatistica.csv")


# Mapa de calor - Correlação entre variáveis
def plot_heatmap(df):
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

    fig_heatmap = px.imshow(
        df_corr,
        title="Mapa de Calor - Correlação entre Variáveis",
        color_continuous_scale="Viridis",
        range_color=[-1, 1],
        labels=dict(
            x="Colunas",
            y="Linhas",
            color="Correlação",
        ),
    )
    return fig_heatmap


# Gráfico de pizza - Distribuição da Categoria Temporada

maiores = outros(df)


def plot_pizza(maiores):
    fig_pizza = px.pie(
        values=maiores.values,
        names=maiores.index,
        title="Pizza - Distribuição da Categoria Temporada",
        hole=0.25,
    )
    return fig_pizza


# Gráfico de densidade - Distribuição de Notas
def plot_density(df):
    fig_density = px.histogram(
        data_frame=df,
        x="Nota",
        marginal="violin",
        color_discrete_sequence=["#99b595"],
        title="Densidade - Distribuição de Notas",
    )
    fig_density.update_layout(
        xaxis_title="Notas",
        yaxis_title="Frequência",
    )

    return fig_density


# Gráfico de Histograma - Distribuição de Preços
def plot_histogram(df):
    fig_hist = px.histogram(
        data_frame=df,
        x="Preço",
        title="Histograma - Distribuição de Preços",
        nbins=50,
        color_discrete_sequence=["#99b595"],
        facet_col_spacing=0.1,
    )
    fig_hist.update_layout(
        xaxis_title="Faixas de Preço",
        yaxis_title="Quantidade de Produtos",
    )

    return fig_hist


# Gráfico de dispersão - Notas x N Avaliações
def plot_scatter(df):
    fig_scatter = px.scatter(
        data_frame=df,
        x="Nota",
        y="N_Avaliações",
        labels={"Nota": "Notas", "N_Avaliações": "Número de Avaliações"},
        title="Gráfico de Dispersão - Notas x N° Avaliações",
        size="N_Avaliações",
        size_max=50,
        opacity=0.8,
    )
    return fig_scatter


# Gráfico de barra - Gênero
dados_genero = renomear(df)


def plot_bar(dados_genero):
    fig_bar = px.bar(
        data_frame=dados_genero,
        x=dados_genero.index,
        y=dados_genero.values,
        labels={"x": "Gênero", "y": "Quantidade"},
        title='Barras - Distribuição da Categoria "Gênero"',
        color=dados_genero.index,
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    return fig_bar


# Grafico de Regressão - N_Avaliações x Qtd_Vendidos_Cod
df_rm_outliers = rm_outliers(df)


def plot_regression(df_rm_outliers):
    fig_regression = px.scatter(
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
        trendline_color_override="#eb8c00",
    )
    return fig_regression


def cria_app(df):
    # Cria app
    app = Dash(__name__)
    server = app.server

    fig_heatmap = plot_heatmap(df)
    fig_pizza = plot_pizza(maiores)
    fig_density = plot_density(df)
    fig_hist = plot_histogram(df)
    fig_scatter = plot_scatter(df)
    fig_bar = plot_bar(dados_genero)
    fig_regression = plot_regression(df_rm_outliers)

    # Aumentando os gráficos
    fig_heatmap.update_layout(height=550)
    fig_pizza.update_layout(height=550)

    # Layout do app
    app.layout = html.Div(
        style={"width": "100%", "padding": "20px"},
        children=[
            # Linha 1: heatmap, pizza
            html.Div(
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "gap": "25px",
                    "width": "100%",
                },
                children=[
                    dcc.Graph(figure=fig_heatmap, style={"flex": "1"}),
                    dcc.Graph(figure=fig_pizza, style={"flex": "1"}),
                ],
            ),
            # Linha 2: densidade, histograma
            html.Div(
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "gap": "25px",
                    "width": "100%",
                },
                children=[
                    dcc.Graph(figure=fig_density, style={"flex": "1"}),
                    dcc.Graph(figure=fig_hist, style={"flex": "1"}),
                ],
            ),
            # Linha 3: dispersão, barra
            html.Div(
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "gap": "25px",
                    "width": "100%",
                },
                children=[
                    dcc.Graph(figure=fig_scatter, style={"flex": "1"}),
                    dcc.Graph(figure=fig_bar, style={"flex": "1"}),
                ],
            ),
            # Linha 4: regressão
            html.Div(
                style={
                    "width": "100%",
                },
                children=dcc.Graph(figure=fig_regression),
            ),
        ],
    )

    return app


if __name__ == "__main__":
    app = cria_app(df)
    app.run(debug=True, port=8050)
