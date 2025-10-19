import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('ecommerce_estatistica.csv')

pd.set_option('display.max_columns', None)

print(df.head())

print(f'\nInformações do DataFrame: {df.info()}')

print(f'\nDescrição do DataFrame: {df.describe()}')

print(f'\nValores únicos: {df.nunique()}')

# Mudando o estilo da tabela
sns.set_style('darkgrid')
sns.set_palette('coolwarm')


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
x_genero = df['Gênero'].value_counts().index
y_genero = df['Gênero'].value_counts().values
dados_genero = pd.Series(y_genero, index=x_genero)

# Renomeando os indices
dados_genero = dados_genero.rename(
    index={
        'Sem gênero infantil': 'Infantil Genérico',
        'roupa para gordinha pluss P ao 52': 'Plus Size',
    }
)

plt.figure(figsize=(12, 6))
plt.bar(dados_genero.index, dados_genero.values, color='#99b595')
plt.title('Barras - Distribuição da Categoria "Gênero"')
plt.ylabel('Quantidade')
plt.show()


# Gráfico de pizza - Distribuição da Categoria Temporada
x_temp = df['Temporada'].value_counts().index
y_temp = df['Temporada'].value_counts().values
dados_temp = pd.Series(y_temp, index=x_temp)

# Define o limite de 5% do total
limite = 0.05 * dados_temp.sum()

# Agrupa os valores menores que 5%
maiores = dados_temp[dados_temp >= limite]
menores = dados_temp[dados_temp < limite]

# Adiciona a categoria 'Outros'
if not menores.empty:
    maiores['Outros'] = menores.sum()

# Plota o gráfico
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


# Removendo outliers com IQR - N_Avaliações_MinMax x Qtd_Vendidos_Cod
Avalicoes_Q1 = df['N_Avaliações'].quantile(0.25)
Avalicoes_Q3 = df['N_Avaliações'].quantile(0.75)
Vendidos_Q1 = df['Qtd_Vendidos_Cod'].quantile(0.25)
Vendidos_Q3 = df['Qtd_Vendidos_Cod'].quantile(0.75)

IQR_Avalicoes = Avalicoes_Q3 - Avalicoes_Q1
IQR_Vendidos = Vendidos_Q3 - Vendidos_Q1

limite_alto_Avalicoes = Avalicoes_Q3 + 1.5 * IQR_Avalicoes

limite_alto_Vendidos = Vendidos_Q3 + 1.5 * IQR_Vendidos

df_rm_outliers = df[
    (df['N_Avaliações'] <= limite_alto_Avalicoes)
    & (df['Qtd_Vendidos_Cod'] <= limite_alto_Vendidos)
]

# Gráfico de Regressão - N_Avaliações_MinMax x Qtd_Vendidos_Cod
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
