import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub

# DATASET: https://www.kaggle.com/datasets/fireballbyedimyrnmom/cyber-incidents-up-to-2020
caminho_dados = kagglehub.dataset_download(
    "fireballbyedimyrnmom/cyber-incidents-up-to-2020", path='cyber-operations-incidents.csv')
dados = pd.read_csv(caminho_dados)

dados['Patrocinador'] = dados['Sponsor'].fillna('Desconhecido')
dados['Patrocinador'] = dados['Patrocinador'].str.split(', ')
dados = dados.explode('Patrocinador')

traducao_paises = {
    'Russian Federation': 'Rússia',
    "Korea (Democratic People's Republic of)": 'Coreia do Norte',
    'Australia': 'Austrália',
    'Palestine, State of': 'Palestina',
    'Iran (Islamic Republic of)': 'Irã',
    'Saudi Arabia': 'Arábia Saudita',
    'Syrian Arab Republic': 'Síria',
    'China': 'China',
    'Turkey': 'Turquia',
    'Vietnam': 'Vietnã',
    'Pakistan': 'Paquistão',
    'Israel': 'Israel',
    'Korea (Republic of)': 'Coreia do Sul',
    'Togo': 'Togo',
    'United States of America': 'Estados Unidos',
    'United Arab Emirates': 'Emirados Árabes Unidos',
    'United States': 'Estados Unidos',
    'Hong Kong': 'Hong Kong',
    'China, Russian Federation': 'China',
    'Egypt': 'Egito',
    'Uzbekistan': 'Uzbequistão',
    'Morocco': 'Marrocos',
    'Netherlands': 'Países Baixos',
    'United Kingdom': 'Reino Unido',
    'Lebanon': 'Líbano',
    'Mexico': 'México',
    'Ethiopia': 'Etiópia',
    'Panama': 'Panamá',
    'Indonesia': 'Indonésia',
    'Kazakhstan': 'Cazaquistão',
    'Uganda': 'Uganda',
    'Spain': 'Espanha',
    'France': 'França',
    'India': 'Índia',
    'Taiwan': 'Taiwan',
    'Desconhecido': 'Desconhecido'
}

dados['Patrocinador'] = dados['Patrocinador'].replace(traducao_paises)
dados = dados[dados['Patrocinador'] != 'Desconhecido']  # tira nulos

ataques_por_pais = dados.groupby(
    'Patrocinador').size().reset_index(name='Total_Ataques')

total_ataques = ataques_por_pais['Total_Ataques'].sum()
top_10_paises = ataques_por_pais.nlargest(10, 'Total_Ataques')
top_10_paises['Porcentagem'] = (
    top_10_paises['Total_Ataques'] / total_ataques * 100).round(2)

# barras
plt.figure(figsize=(12, 8))
barras = sns.barplot(
    x='Total_Ataques',
    y='Patrocinador',
    data=top_10_paises,
    palette={pais: '#2986cc' if i < 3 else '#bdddf5' for i,
             pais in enumerate(top_10_paises['Patrocinador'])}
)
barras.set_yticklabels(barras.get_yticklabels(), fontsize=14)

# porcentagem dos top 3
for i, (pais, porcentagem, total) in enumerate(zip(top_10_paises['Patrocinador'], top_10_paises['Porcentagem'], top_10_paises['Total_Ataques'])):
    if i < 3:
        barras.text(
            total - total / 2,  # bota na metade da barra
            i,
            f"{porcentagem}%",
            color="black",
            va="center",
            fontweight="bold",
            fontsize=12
        )

plt.title('Distribuição global de ataques cibernéticos apoiados por Estados: Principais países de 2005 a 2020 (Fonte: Council of Foreign Relations)', fontsize=16)
plt.xlabel('Número total de Ataques Cibernéticos', fontsize=14)
plt.ylabel('Países envolvidos em Ataques Cibernéticos', fontsize=14)
plt.tight_layout()
plt.show()

print(ataques_por_pais)
