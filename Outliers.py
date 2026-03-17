import pandas as pd
from scipy import stats

pd.set_option('display.width', None)

df = pd.read_csv('clientes_limpeza.csv')

df_filtro_basico = df[df['idade'] > 100]

print('Filtro básico \n', df_filtro_basico[['nome', 'idade']])

# Indentificando outliers (informações dos clientes) com Z-score (diz quantos desvios-padrão um valor está acima oui abaixo da média).
z_score = stats.zscore(df['idade'].dropna()) # .dropna() utilizado apenas para caso de os valores nulos não estivessem tratados
outliers_z = df[z_score >= 3]
print("Outliers pelo Z-score:\n", outliers_z)

# Filtrar Outliers com Z-score (de forma mais rápida e organizada)
df_zscore = df[(stats.zscore(df['idade']) < 3)]

# Identificar Outlier com IQR
Q1 = df['idade'].quantile(0.25)
Q3 = df['idade'].quantile(0.75)
IQR = Q3 - Q1

limite_baixo = 1
limite_alto = 100

print("Limites IQR: ", limite_baixo, limite_alto)


# Filtrar outliers com IQR
df_iqr = df[(df['idade'] < limite_baixo) & (df['idade'] >= limite_alto)]
print("Limites de IQR: ", limite_baixo, "e", limite_alto)

# Filtrar endereços inválidos
df['endereco'] = df['endereco'].apply(lambda x: 'Endereço inválido' if len(x.split('\n')) < 3 else x)

# Tratar campos de texto
df['nome'] = df['nome'].apply(lambda x: 'Nome inválido' if isinstance(x, str) and len(x) > 50 else x)
print("Qtd de registros com nomes Grandes: ", (df['nome'] == 'Nome inválido').sum())

print('Dados com Outliers tratados: \n', df)

# Salvar dataframe
df.to_csv('clientes_remove_outliers.csv', index=False)
