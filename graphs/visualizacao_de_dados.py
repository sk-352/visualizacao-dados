import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from funcoes import print_infos, renomear, outros, rm_outliers

df = pd.read_csv('ecommerce_estatistica.csv')

print_infos()


# Mudando estilo de gráficos
sns.set_style('darkgrid')
sns.set_palette('pastel')

# Mapa de calor - Correlação entre variáveis
df_corr = df[
    [
        'Nota_MinMax',
        'N_Avaliações_MinMax',
        'Desconto_MinMax',
        'Preço_MinMax',
        'Marca_Cod',
        'Material_Cod',
        'Temporada_Cod',
        'Qtd_Vendidos_Cod',
        'Marca_Freq',
        'Material_Freq',
    ]
].corr()

plt.figure(figsize=(12, 12))
sns.heatmap(df_corr, annot=True, fmt='.2f')
plt.title('Mapa de Calor - Correlação entre Variáveis')
plt.xticks(rotation=-28)
plt.tight_layout()
plt.show()


# Gráfico de Histograma - Distribuição de Preços
plt.figure(figsize=(10, 6))
plt.hist(df['Preço'], bins=50, color='green', alpha=0.8)
plt.title('Histograma - Distribuição de Preços')
plt.xlabel('Preços dos Produtos em R$')
plt.xticks(ticks=range(0, int(df['Preço'].max()) + 50, 50))
plt.ylabel('Frequência')
plt.grid(True)
plt.show()


# Gráfico de dispersão - Nota MinMax x N_Avaliações_MinMax
sns.jointplot(
    x='Nota',
    y='N_Avaliações',
    data=df,
    kind='scatter',
    color='#863e9c',
)
plt.xlabel('Notas')
plt.ylabel('Número de Avaliações')
plt.show()


# Gráfico de barra - Gênero
dados_genero = renomear(df)

plt.figure(figsize=(12, 6))
plt.bar(dados_genero.index, dados_genero.values, color='#99b595')
plt.title('Barras - Distribuição da Categoria "Gênero"')
plt.ylabel('Quantidade')
plt.show()


# Gráfico de pizza - Distribuição da Categoria Temporada
maiores = outros(df)

plt.figure(figsize=(8, 6))
plt.pie(maiores, labels=maiores.index, autopct='%1.1f%%', startangle=90)
plt.title('Pizza - Distribuição da Categoria Temporada')
plt.show()


# Gráfico de densidade
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Nota'], fill=True, color='#863e9c')
plt.title('Densidade - Distribuição de Notas')
plt.xlabel('Nota')
plt.ylabel('Densidade')
plt.show()


# Gráfico de Regressão - N_Avaliações_MinMax x Qtd_Vendidos_Cod
df_rm_outliers = rm_outliers(df)

plt.figure(figsize=(10, 6))
sns.regplot(
    x='N_Avaliações',
    y='Qtd_Vendidos_Cod',
    data=df_rm_outliers,
    color='#278f65',
)
plt.title('Regressão - Número de Avaliações x Quantidade Vendida')
plt.xlabel('Número de Avaliações')
plt.ylabel('Quantidade Vendida')
plt.show()
